"""
S01E02 — findhim

Wśród podejrzanych z S01E01 znajdź tego, który przebywał najbliżej jednej z elektrowni
atomowych, ustal jego poziom dostępu i wyślij (imię, nazwisko, accessLevel, kod elektrowni)
do `/verify`.

`findhim_locations.json` z huba celowo NIE zawiera współrzędnych elektrowni — tylko nazwy
miast (potwierdzone community notes, `doc/s01e02_aid4u_comments.md`, wątek Łukasz Barszcz).
Współrzędne siedmiu miast z tej konkretnej listy są więc zaszyte w kodzie (`_CITY_COORDS`) —
to fakty geograficzne, nie coś, co LLM powinien zgadywać z pamięci przy każdym wywołaniu:
community notes są zgodne, że poleganie na współrzędnych "z głowy" modelu jest główną
przyczyną niepowodzeń tego zadania (błędy rzędu dziesiątek-setek km, patrz komentarze
Wiktora Flisa i Tomasza Budzińskiego). Odległość liczy deterministyczne narzędzie
(`nearest_active_plant`, Haversine) — LLM tylko orkiestruje kolejność wywołań (Function
Calling, cel dydaktyczny odcinka) i porównuje już policzone, małe liczby dystansu.

Architektura: `LLMClient.run_agent_loop()` (ten sam mechanizm co s02e04_mailbox) z czterema
narzędziami. Lista podejrzanych NIE jest pobierana na nowo — jest wczytywana z
`data/run-history/`, czyli z odpowiedzi faktycznie wysłanej do huba w S01E01 (ten sam plik,
zweryfikowany już flagą SURVIVORS), zgodnie ze wskazówką zadania ("chodzi tylko o osoby,
które wysyłałeś jako podejrzanych do Hubu").
"""

from __future__ import annotations

import json
import math
import unicodedata
from collections.abc import Callable
from pathlib import Path
from typing import Any

import httpx

from core.hub import HubClient
from core.llm import LLMMessage
from core.llm.types import Tool
from core.tasks import BaseTask, task
from tasks.s01e02_findhim.prompts import SYSTEM_AGENT_FINDHIM, build_kickoff_prompt

HUB_TASK_NAME = "findhim"
LOCATION_API_PATH = "/api/location"
ACCESS_LEVEL_API_PATH = "/api/accesslevel"

_MAX_ITERATIONS = 25
_RUN_HISTORY_DIR = Path("data/run-history")

# Współrzędne centrów miast, w których stoją elektrownie z findhim_locations.json.
# Zaszyte celowo — patrz docstring modułu. Klucze znormalizowane przez `_normalize_city()`
# (bez polskich znaków diakrytycznych, lowercase), żeby drobne różnice zapisu nazwy miasta
# zwróconej przez hub (wielkość liter, "Chelmno" vs "Chełmno") nie psuły dopasowania.
_CITY_COORDS: dict[str, tuple[float, float]] = {
    "zabrze": (50.3212, 18.7857),
    "piotrkow trybunalski": (51.4048, 19.7031),
    "grudziadz": (53.4837, 18.7536),
    "tczew": (54.0925, 18.7997),
    "radom": (51.4027, 21.1471),
    "chelmno": (53.3489, 18.4243),
    "zarnowiec": (54.7761, 18.0553),
}


def _normalize_city(name: str) -> str:
    """Usuwa polskie znaki diakrytyczne i normalizuje wielkość liter do dopasowania w _CITY_COORDS."""
    decomposed = unicodedata.normalize("NFKD", name)
    ascii_only = "".join(c for c in decomposed if not unicodedata.combining(c))
    return ascii_only.strip().lower()


def _haversine_km(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """Odległość na kuli ziemskiej (promień 6371 km) między dwoma punktami lat/lon w stopniach."""
    r = 6371.0
    p1, p2 = math.radians(lat1), math.radians(lat2)
    d_phi = math.radians(lat2 - lat1)
    d_lambda = math.radians(lon2 - lon1)
    a = math.sin(d_phi / 2) ** 2 + math.cos(p1) * math.cos(p2) * math.sin(d_lambda / 2) ** 2
    return 2 * r * math.asin(math.sqrt(a))


# ─── Wczytywanie danych wejściowych (czyste funkcje) ─────────────────────────


def _load_suspects() -> list[dict]:
    """Wczytuje listę podejrzanych z ostatniego zapisanego wyniku S01E01.

    `BaseTask._save_output()` nazywa plik wg klucza cache'u wejściowego zadania
    (`people.csv`), nie wg treści — stąd rozszerzenie ".csv" mimo że w środku jest JSON.
    """
    candidates = sorted(_RUN_HISTORY_DIR.glob("s01e01-*-people.csv"))
    if not candidates:
        raise RuntimeError(
            "Brak zapisanego wyniku S01E01 w data/run-history/ — uruchom najpierw "
            "`uv run run.py solve s01e01`, findhim potrzebuje dokładnie tej listy podejrzanych."
        )
    return json.loads(candidates[-1].read_text(encoding="utf-8"))


def parse_plants(raw: bytes) -> list[dict]:
    """Parsuje `findhim_locations.json` i dokłada współrzędne miast z `_CITY_COORDS`.

    Rzuca `KeyError` z czytelnym komunikatem, jeśli hub zwróci miasto spoza znanej siódemki —
    lepiej to zobaczyć od razu niż dostać cichy, błędny wynik dystansu.
    """
    power_plants = json.loads(raw.decode("utf-8"))["power_plants"]
    plants = []
    for city, meta in power_plants.items():
        key = _normalize_city(city)
        if key not in _CITY_COORDS:
            raise KeyError(
                f"Brak zaszytych współrzędnych dla miasta {city!r} — dopisz je do _CITY_COORDS."
            )
        lat, lon = _CITY_COORDS[key]
        plants.append(
            {
                "city": city,
                "code": meta["code"],
                "is_active": bool(meta.get("is_active", True)),
                "latitude": lat,
                "longitude": lon,
            }
        )
    return plants


# ─── Narzędzia — definicje dla LLMClient.run_agent_loop ──────────────────────

GET_PERSON_LOCATIONS_TOOL = Tool(
    name="get_person_locations",
    description=(
        "Pobiera znane lokalizacje (lista {latitude, longitude}) danej osoby z "
        "POST /api/location. Wywołaj dla każdego podejrzanego z listy."
    ),
    parameters={
        "type": "object",
        "properties": {
            "name": {"type": "string", "description": "Imię podejrzanego."},
            "surname": {"type": "string", "description": "Nazwisko podejrzanego."},
        },
        "required": ["name", "surname"],
    },
)

NEAREST_ACTIVE_PLANT_TOOL = Tool(
    name="nearest_active_plant",
    description=(
        "Liczy (wzorem Haversine, deterministycznie) odległość od podanych lokalizacji do "
        "każdej AKTYWNEJ elektrowni i zwraca tę najbliższą wraz z dystansem w km. Podaj "
        "WPROST listę lokalizacji zwróconą przez get_person_locations — nie licz odległości "
        "sam, nie zgaduj współrzędnych elektrowni."
    ),
    parameters={
        "type": "object",
        "properties": {
            "locations": {
                "type": "array",
                "description": "Lokalizacje z get_person_locations, bez zmian.",
                "items": {
                    "type": "object",
                    "properties": {
                        "latitude": {"type": "number"},
                        "longitude": {"type": "number"},
                    },
                    "required": ["latitude", "longitude"],
                },
            },
        },
        "required": ["locations"],
    },
)

GET_ACCESS_LEVEL_TOOL = Tool(
    name="get_access_level",
    description="Pobiera poziom dostępu (accessLevel) danej osoby z POST /api/accesslevel.",
    parameters={
        "type": "object",
        "properties": {
            "name": {"type": "string", "description": "Imię."},
            "surname": {"type": "string", "description": "Nazwisko."},
            "birth_year": {
                "type": "integer",
                "description": "Rok urodzenia (z danych wejściowych, pole 'born').",
            },
        },
        "required": ["name", "surname", "birth_year"],
    },
)

SUBMIT_ANSWER_TOOL = Tool(
    name="submit_answer",
    description=(
        "Wysyła finalną odpowiedź do huba (POST /verify, task='findhim'). Hub odpowie czy "
        "kandydat jest poprawny (flaga) czy trzeba spróbować z kolejną osobą."
    ),
    parameters={
        "type": "object",
        "properties": {
            "name": {"type": "string", "description": "Imię kandydata."},
            "surname": {"type": "string", "description": "Nazwisko kandydata."},
            "access_level": {"type": "integer", "description": "accessLevel z get_access_level."},
            "power_plant": {
                "type": "string",
                "description": "Kod elektrowni (format PWR0000PL) z nearest_active_plant.",
            },
        },
        "required": ["name", "surname", "access_level", "power_plant"],
    },
)

FINDHIM_TOOLS = [
    GET_PERSON_LOCATIONS_TOOL,
    NEAREST_ACTIVE_PLANT_TOOL,
    GET_ACCESS_LEVEL_TOOL,
    SUBMIT_ANSWER_TOOL,
]


def build_tool_executor(
    hub: HubClient, plants: list[dict], *, dry_run: bool
) -> tuple[Callable[[str, dict[str, Any]], str], dict[str, Any]]:
    """Zamyka `hub`/`plants`/`dry_run` w closure; `state` trzyma ostatnią próbę submit_answer
    i złapaną flagę między wywołaniami narzędzi w jednej pętli agentowej (patrz s02e04_mailbox
    dla tego samego wzorca)."""
    state: dict[str, Any] = {"last_submission": None, "flag": None}
    known_codes = {p["code"] for p in plants}

    def get_person_locations(name: str, surname: str) -> str:
        response = hub.post_api(LOCATION_API_PATH, {"name": name, "surname": surname})
        return json.dumps(response, ensure_ascii=False)

    def nearest_active_plant(locations: list[dict]) -> str:
        active = [p for p in plants if p["is_active"]]
        if not active or not locations:
            return json.dumps(
                {"ok": False, "message": "Brak aktywnych elektrowni albo pustych lokalizacji."},
                ensure_ascii=False,
            )
        best_distance = math.inf
        best_plant = None
        for loc in locations:
            for plant in active:
                d = _haversine_km(
                    float(loc["latitude"]), float(loc["longitude"]),
                    plant["latitude"], plant["longitude"],
                )
                if d < best_distance:
                    best_distance = d
                    best_plant = plant
        return json.dumps(
            {
                "plant_city": best_plant["city"],
                "plant_code": best_plant["code"],
                "distance_km": round(best_distance, 3),
            },
            ensure_ascii=False,
        )

    def get_access_level(name: str, surname: str, birth_year: int) -> str:
        response = hub.post_api(
            ACCESS_LEVEL_API_PATH,
            {"name": name, "surname": surname, "birthYear": int(birth_year)},
        )
        return json.dumps(response, ensure_ascii=False)

    def submit_answer(name: str, surname: str, access_level: int, power_plant: str) -> str:
        """Waliduje kod elektrowni lokalnie (musi być jednym ze znanych), potem POST /verify."""
        if power_plant not in known_codes:
            return json.dumps(
                {
                    "ok": False,
                    "message": (
                        f"Lokalna walidacja (bez wysyłki do huba): {power_plant!r} nie jest "
                        f"żadnym ze znanych kodów elektrowni: {sorted(known_codes)}."
                    ),
                },
                ensure_ascii=False,
            )

        submission = {
            "name": name,
            "surname": surname,
            "accessLevel": int(access_level),
            "powerPlant": power_plant,
        }
        state["last_submission"] = submission

        if dry_run:
            return json.dumps({"ok": True, "dry_run": True, "would_submit": submission}, ensure_ascii=False)

        try:
            response = hub.submit(HUB_TASK_NAME, submission)
        except httpx.HTTPStatusError as exc:
            if exc.response.status_code >= 500:
                raise
            try:
                body: Any = exc.response.json()
            except ValueError:
                body = exc.response.text
            return json.dumps(
                {"ok": False, "http_status": exc.response.status_code, "error": body},
                ensure_ascii=False,
            )

        flag = hub.get_flag(response)
        if flag:
            state["flag"] = flag
        return json.dumps(response, ensure_ascii=False)

    def tool_executor(name: str, args: dict[str, Any]) -> str:
        """Dispatcher przekazywany do LLMClient.run_agent_loop — routuje po nazwie narzędzia."""
        if name == "get_person_locations":
            return get_person_locations(args["name"], args["surname"])
        if name == "nearest_active_plant":
            return nearest_active_plant(args["locations"])
        if name == "get_access_level":
            return get_access_level(args["name"], args["surname"], args["birth_year"])
        if name == "submit_answer":
            return submit_answer(args["name"], args["surname"], args["access_level"], args["power_plant"])
        raise ValueError(f"Unknown tool: {name}")

    return tool_executor, state


# ─── Task ─────────────────────────────────────────────────────────────────────


@task("s01e02", hub_name="findhim")
class FindhimTask(BaseTask):
    """Agentowe (Function Calling) namierzenie podejrzanego widzianego blisko elektrowni."""

    _captured_flag: str | None = None

    def fetch_data(self) -> bytes:
        return self.cache.get_or_fetch(
            "findhim_locations.json",
            lambda: self.hub.get_data("findhim_locations.json"),
        )

    def solve(self, data: bytes) -> dict:
        plants = parse_plants(data)
        suspects = _load_suspects()
        if not suspects:
            raise ValueError("Lista podejrzanych z S01E01 jest pusta.")

        executor, state = build_tool_executor(self.hub, plants, dry_run=self.dry_run)
        messages = [LLMMessage.user(build_kickoff_prompt(suspects, plants))]

        self.llm.run_agent_loop(
            messages,
            FINDHIM_TOOLS,
            executor,
            system=SYSTEM_AGENT_FINDHIM,
            max_iterations=_MAX_ITERATIONS,
        )

        self._captured_flag = state["flag"]

        if state["last_submission"] is None:
            raise RuntimeError(
                "Agent nie wywołał ani razu submit_answer w ciągu "
                f"{_MAX_ITERATIONS} iteracji — brak odpowiedzi do wysłania."
            )

        return state["last_submission"]

    def _submit(self, task_name: str, answer: Any) -> str | None:
        """Pomija redundantny finalny POST /verify, jeśli submit_answer już złapał flagę w pętli."""
        if self._captured_flag:
            return self._captured_flag
        return super()._submit(task_name, answer)
