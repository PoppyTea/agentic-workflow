"""
S01E02 — findhim

Znajdź podejrzanego (z listy wysłanej w S01E01, tag 'transport'), który widziany
był bardzo blisko jednej z elektrowni atomowych, ustal jego poziom dostępu i kod
elektrowni.

Nazwa zadania w hubie: findhim

Zadanie jest w pełni deterministyczne (patrz doc/s01e02_aid4u_comments.md —
konsensus komentarzy kursu): jedyny krok z LLM to odtworzenie listy podejrzanych
z S01E01 (tagowanie zawodów). Reszta to dwa wywołania API hubu i geometria.
"""

from __future__ import annotations

import json
import math
from typing import Any

from pydantic import BaseModel

from core.llm import LLMMessage
from core.tasks import BaseTask, task
from tasks.s01e01_people.prompts import SYSTEM_TAGGING, USER_TAGGING  # noqa: F401 — USER_TAGGING używany w build_tagging_prompt
from tasks.s01e01_people.solution import (
    TaggingResponse,
    apply_tags,
    build_tagging_prompt,
    filter_by_tag,
    filter_candidates,
    parse_csv,
)

TARGET_TAG = "transport"

# findhim_locations.json zwraca elektrownie WYŁĄCZNIE z nazwą miasta, bez współrzędnych
# (potwierdzone empirycznie na żywym endpoincie — patrz doc/s01e02_zadanie.md, wskazówka
# Łukasza Barszcza). Współrzędne miast hardcodujemy zamiast prosić o nie LLM: zadanie jest
# w pełni deterministyczne, a halucynacje koordynatów przez model to najczęstsza
# udokumentowana przyczyna błędnego wyniku w tym zadaniu (patrz doc/s01e02_aid4u_comments.md
# — wielu studentów zgłasza błędy 130-250 km przy pytaniu modelu o współrzędne).
CITY_COORDS: dict[str, tuple[float, float]] = {
    "Zabrze": (50.3249, 18.7857),
    "Piotrków Trybunalski": (51.4050, 19.7031),
    "Grudziądz": (53.4837, 18.7536),
    "Tczew": (54.0924, 18.7997),
    "Radom": (51.4027, 21.1471),
    "Chelmno": (53.3494, 18.4239),
    "Żarnowiec": (54.7686, 18.1706),
}


class PowerPlant(BaseModel):
    city: str
    code: str
    is_active: bool
    lat: float
    lon: float


# ─── Czyste funkcje (łatwe do testowania jednostkowego) ──────────────────────


def haversine_km(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """Odległość po powierzchni kuli ziemskiej (promień 6371 km)."""
    radius = 6371.0
    p1, p2 = math.radians(lat1), math.radians(lat2)
    dphi = math.radians(lat2 - lat1)
    dlambda = math.radians(lon2 - lon1)
    a = math.sin(dphi / 2) ** 2 + math.cos(p1) * math.cos(p2) * math.sin(dlambda / 2) ** 2
    return 2 * radius * math.asin(math.sqrt(a))


def parse_power_plants(raw: bytes) -> list[PowerPlant]:
    """Parsuje findhim_locations.json i dokłada twarde koordynaty z CITY_COORDS."""
    body = json.loads(raw)
    plants = []
    for city, info in body["power_plants"].items():
        if city not in CITY_COORDS:
            raise ValueError(f"Brak twardych koordynatów dla miasta '{city}' — dopisz do CITY_COORDS")
        lat, lon = CITY_COORDS[city]
        plants.append(
            PowerPlant(city=city, code=info["code"], is_active=bool(info["is_active"]), lat=lat, lon=lon)
        )
    return plants


def nearest_active_plant(
    locations: list[dict], plants: list[PowerPlant]
) -> tuple[PowerPlant, float] | None:
    """
    Najbliższa AKTYWNA elektrownia spośród wszystkich lokalizacji jednej osoby.

    Zwraca (elektrownia, dystans_km) albo None gdy brak lokalizacji/aktywnych elektrowni.
    """
    best: tuple[PowerPlant, float] | None = None
    for loc in locations:
        lat, lon = loc["latitude"], loc["longitude"]
        for plant in plants:
            if not plant.is_active:
                continue
            distance = haversine_km(lat, lon, plant.lat, plant.lon)
            if best is None or distance < best[1]:
                best = (plant, distance)
    return best


def _birth_year(suspect: dict) -> int:
    """Wyciąga rok urodzenia z danych osoby (birthDate w formacie ISO z huba)."""
    raw = suspect.get("birthDate") or suspect.get("born") or suspect.get("year_of_birth")
    return int(str(raw).split("-")[0])


# ─── Task ─────────────────────────────────────────────────────────────────────


@task("s01e02", hub_name="findhim")
class FindhimTask(BaseTask):
    def fetch_data(self) -> dict[str, bytes]:
        locations = self.cache.get_or_fetch(
            "findhim_locations.json",
            lambda: self.hub.get_data("findhim_locations.json"),
        )
        people_csv = self.cache.get_or_fetch(
            "people.csv",
            lambda: self.hub.get_data("people.csv"),
        )
        return {"locations": locations, "people_csv": people_csv}

    def _suspects(self, people_csv: bytes) -> list[dict]:
        """
        Odtwarza listę podejrzanych wysłaną w S01E01 (mężczyźni 20-40 lat z Grudziądza,
        tag zawodu 'transport') — dokładnie to samo filtrowanie i tagowanie co
        PeopleTask.solve(), bez ponownej submisji do huba.
        """
        all_people = parse_csv(people_csv)
        candidates = filter_candidates(all_people)
        if not candidates:
            raise ValueError("Brak kandydatów z S01E01 — sprawdź people.csv")

        prompt = build_tagging_prompt(candidates)
        tagged = self.llm.structured(
            [LLMMessage.user(prompt)], TaggingResponse, system=SYSTEM_TAGGING
        )
        with_tags = apply_tags(candidates, tagged.results)
        suspects = filter_by_tag(with_tags, TARGET_TAG)
        if not suspects:
            raise ValueError("Brak podejrzanych z tagiem 'transport' — sprawdź tagowanie S01E01")
        return suspects

    def solve(self, data: dict[str, bytes]) -> Any:
        import logfire

        plants = parse_power_plants(data["locations"])
        suspects = self._suspects(data["people_csv"])

        best: tuple[dict, PowerPlant, float] | None = None
        for suspect in suspects:
            locations = self.hub.post_api(
                "/api/location", {"name": suspect["name"], "surname": suspect["surname"]}
            )
            candidate = nearest_active_plant(locations, plants)
            if candidate is None:
                continue
            plant, distance = candidate
            logfire.info(
                "Dystans podejrzanego od najbliższej elektrowni",
                name=suspect["name"],
                surname=suspect["surname"],
                plant=plant.city,
                distance_km=round(distance, 2),
            )
            if best is None or distance < best[2]:
                best = (suspect, plant, distance)

        if best is None:
            raise ValueError("Żaden podejrzany nie ma lokalizacji blisko aktywnej elektrowni")

        suspect, plant, distance = best
        logfire.info(
            "Wytypowano podejrzanego",
            name=suspect["name"],
            surname=suspect["surname"],
            plant=plant.city,
            code=plant.code,
            distance_km=round(distance, 2),
        )

        access = self.hub.post_api(
            "/api/accesslevel",
            {
                "name": suspect["name"],
                "surname": suspect["surname"],
                "birthYear": _birth_year(suspect),
            },
        )

        return {
            "name": suspect["name"],
            "surname": suspect["surname"],
            "accessLevel": access["accessLevel"],
            "powerPlant": plant.code,
        }
