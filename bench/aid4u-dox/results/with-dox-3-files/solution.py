"""
S01E02 — findhim

Spośród podejrzanych z S01E01 (tag 'transport') ustala, kto był widziany
najbliżej jednej z elektrowni atomowych, jaki ma poziom dostępu i przy której
elektrowni go zauważono.

Nazwa zadania w hubie: findhim
"""

from __future__ import annotations

import json
import math
from pathlib import Path
from typing import Any

from core.tasks import BaseTask, task
from tasks.s01e01_people.prompts import SYSTEM_TAGGING
from tasks.s01e01_people.solution import (
    TARGET_TAG,
    TaggingResponse,
    apply_tags,
    build_tagging_prompt,
    filter_by_tag,
    filter_candidates,
    format_answer,
    parse_csv,
)

SUSPECTS_CACHE_PATH = Path("data/output/s01e01_people/suspects.json")

# findhim_locations.json (patrz fetch_data) podaje elektrownie WYŁĄCZNIE po nazwie
# miasta + kodzie, bez współrzędnych, a /api/location zwraca lat/lon — więc żeby
# policzyć odległość, współrzędne tych konkretnych siedmiu miast trzeba dołożyć
# ręcznie (centroidy miast, nie samych elektrowni). Klucze MUSZĄ być identyczne
# ze stringami z findhim_locations.json (w tym "Chelmno" bez "ł" — tak jest
# zapisane po stronie huba).
POWER_PLANT_CITY_COORDS: dict[str, tuple[float, float]] = {
    "Zabrze": (50.3249, 18.7857),
    "Piotrków Trybunalski": (51.4053, 19.7031),
    "Grudziądz": (53.4837, 18.7536),
    "Tczew": (54.0924, 18.7997),
    "Radom": (51.4027, 21.1471),
    "Chelmno": (53.3487, 18.4306),
    "Żarnowiec": (54.7952, 18.0912),
}


# ─── Czyste funkcje (łatwe do testowania jednostkowego) ──────────────────────


def parse_power_plants(raw: bytes) -> dict[str, dict]:
    """Parsuje findhim_locations.json do {miasto: {is_active, power, code}}."""
    return json.loads(raw)["power_plants"]


def haversine_km(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """Odległość po kuli ziemskiej (promień 6371 km) między dwoma punktami."""
    r = 6371.0
    p1, p2 = math.radians(lat1), math.radians(lat2)
    dphi = math.radians(lat2 - lat1)
    dlmb = math.radians(lon2 - lon1)
    a = math.sin(dphi / 2) ** 2 + math.cos(p1) * math.cos(p2) * math.sin(dlmb / 2) ** 2
    return 2 * r * math.asin(math.sqrt(a))


def find_closest_match(
    suspects: list[dict],
    locations_by_suspect: dict[tuple[str, str], list[dict]],
    power_plants: dict[str, dict],
) -> tuple[dict, str]:
    """
    Dla każdego zaobserwowanego punktu każdego podejrzanego liczy odległość do
    każdej elektrowni i zwraca (podejrzany, miasto_elektrowni) o globalnie
    najmniejszej odległości. Czysta funkcja — testowalna bez mocków hub/LLM.
    """
    best_distance = math.inf
    best_suspect: dict | None = None
    best_plant: str | None = None

    for suspect in suspects:
        key = (suspect["name"], suspect["surname"])
        for point in locations_by_suspect.get(key, []):
            for plant_city in power_plants:
                plant_lat, plant_lon = POWER_PLANT_CITY_COORDS[plant_city]
                distance = haversine_km(point["latitude"], point["longitude"], plant_lat, plant_lon)
                if distance < best_distance:
                    best_distance = distance
                    best_suspect = suspect
                    best_plant = plant_city

    if best_suspect is None or best_plant is None:
        raise ValueError("Brak dopasowania — żaden podejrzany nie ma zarejestrowanych lokalizacji")

    return best_suspect, best_plant


# ─── Task ─────────────────────────────────────────────────────────────────────


@task("s01e02", hub_name="findhim")
class FindhimTask(BaseTask):
    def fetch_data(self) -> bytes:
        return self.cache.get_or_fetch(
            "findhim_locations.json",
            lambda: self.hub.get_data("findhim_locations.json"),
        )

    def _load_or_build_suspects(self) -> list[dict]:
        """
        Lista podejrzanych (tag 'transport') pochodzi z S01E01. Jeśli był już
        raz policzony i zapisany (data/output/s01e01_people/suspects.json — patrz
        data/AGENTS.md), używamy go bez ponownego wywołania LLM. W przeciwnym
        razie odtwarzamy dokładnie ten sam pipeline co PeopleTask.solve() i
        zapisujemy wynik do ponownego użycia.
        """
        if SUSPECTS_CACHE_PATH.exists():
            return json.loads(SUSPECTS_CACHE_PATH.read_text(encoding="utf-8"))

        from core.llm import LLMMessage

        people_csv = self.hub.get_data("people.csv")
        candidates = filter_candidates(parse_csv(people_csv))
        prompt = build_tagging_prompt(candidates)
        tagged = self.llm.structured(
            [LLMMessage.user(prompt)], TaggingResponse, system=SYSTEM_TAGGING
        )
        with_tags = apply_tags(candidates, tagged.results)
        suspects = format_answer(filter_by_tag(with_tags, TARGET_TAG))

        SUSPECTS_CACHE_PATH.parent.mkdir(parents=True, exist_ok=True)
        SUSPECTS_CACHE_PATH.write_text(
            json.dumps(suspects, ensure_ascii=False, indent=2), encoding="utf-8"
        )
        return suspects

    def solve(self, data: bytes) -> Any:
        power_plants = parse_power_plants(data)
        suspects = self._load_or_build_suspects()
        if not suspects:
            raise ValueError("Brak podejrzanych — sprawdź data/output/s01e01_people/suspects.json")

        locations_by_suspect = {
            (s["name"], s["surname"]): self.hub.post_api(
                "/api/location", {"name": s["name"], "surname": s["surname"]}
            )
            for s in suspects
        }

        suspect, plant_city = find_closest_match(suspects, locations_by_suspect, power_plants)

        access = self.hub.post_api(
            "/api/accesslevel",
            {
                "name": suspect["name"],
                "surname": suspect["surname"],
                "birthYear": suspect["born"],
            },
        )

        return {
            "name": suspect["name"],
            "surname": suspect["surname"],
            "accessLevel": access["accessLevel"],
            "powerPlant": power_plants[plant_city]["code"],
        }
