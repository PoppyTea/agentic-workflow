"""
S01E02 — findhim

Dla podejrzanych z S01E01 (transport, Grudziądz) ustal, który z nich był
widziany najbliżej elektrowni atomowej, jaki ma poziom dostępu i przy której
elektrowni go namierzono. Raport idzie do /verify.

Nazwa zadania w hubie: findhim
"""

from __future__ import annotations

import json
import math
from pathlib import Path
from typing import Any

from core.tasks import BaseTask, task

_SUSPECTS_PATH = Path("data/output/s01e01_people/suspects.json")

# findhim_locations.json podaje elektrownie WYŁĄCZNIE po nazwie miasta (bez
# współrzędnych), a /api/location zwraca surowe lat/lon bez żadnej nazwy —
# dopasowanie wymaga więc znajomości położenia tych miast. Współrzędne są
# statyczną wiedzą geograficzną (miasta istnieją naprawdę), nie wymagają
# zewnętrznego geokodera.
POWER_PLANT_CITY_COORDS: dict[str, tuple[float, float]] = {
    "Zabrze": (50.3249, 18.7857),
    "Piotrków Trybunalski": (51.4055, 19.7031),
    "Grudziądz": (53.4837, 18.7536),
    "Tczew": (54.0924, 18.8000),
    "Radom": (51.4027, 21.1471),
    "Chelmno": (53.3499, 18.4249),
    "Żarnowiec": (54.7667, 18.0500),
}


# ─── Czyste funkcje (łatwe do testowania jednostkowego) ──────────────────────


def haversine_km(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """Odległość po powierzchni kuli ziemskiej (promień 6371 km) w kilometrach."""
    r = 6371.0
    p1, p2 = math.radians(lat1), math.radians(lat2)
    d_phi = math.radians(lat2 - lat1)
    d_lambda = math.radians(lon2 - lon1)
    a = math.sin(d_phi / 2) ** 2 + math.cos(p1) * math.cos(p2) * math.sin(d_lambda / 2) ** 2
    return 2 * r * math.asin(math.sqrt(a))


def load_suspects() -> list[dict]:
    """Wczytuje podejrzanych zdobytych w S01E01 (transport, Grudziądz)."""
    return json.loads(_SUSPECTS_PATH.read_text(encoding="utf-8"))


def parse_power_plants(raw: bytes) -> dict[str, dict]:
    """Parsuje findhim_locations.json do mapy miasto→{is_active, power, code}."""
    return json.loads(raw)["power_plants"]


def find_closest_match(
    suspects: list[dict],
    locations_by_suspect: dict[tuple[str, str], list[dict]],
    power_plants: dict[str, dict],
) -> dict | None:
    """
    Dla każdego podejrzanego i każdej znanej lokalizacji, znajduje najbliższą
    elektrownię (po znanych współrzędnych miasta). Zwraca globalnie najlepsze
    dopasowanie: {suspect, city, code, distance_km}, albo None gdy brak danych.
    """
    best: dict | None = None
    for suspect in suspects:
        key = (suspect["name"], suspect["surname"])
        for coord in locations_by_suspect.get(key, []):
            for city, plant in power_plants.items():
                city_coord = POWER_PLANT_CITY_COORDS.get(city)
                if city_coord is None:
                    continue
                distance_km = haversine_km(
                    coord["latitude"], coord["longitude"], *city_coord
                )
                if best is None or distance_km < best["distance_km"]:
                    best = {
                        "suspect": suspect,
                        "city": city,
                        "code": plant["code"],
                        "distance_km": distance_km,
                    }
    return best


def format_answer(suspect: dict, access_level: int, power_plant_code: str) -> dict:
    """Formatuje odpowiedź w strukturze wymaganej przez hub."""
    return {
        "name": suspect["name"],
        "surname": suspect["surname"],
        "accessLevel": access_level,
        "powerPlant": power_plant_code,
    }


# ─── Task ─────────────────────────────────────────────────────────────────────


@task("s01e02", hub_name="findhim")
class FindhimTask(BaseTask):
    def fetch_data(self) -> dict:
        locations_raw = self.cache.get_or_fetch(
            "findhim_locations.json",
            lambda: self.hub.get_data("findhim_locations.json"),
        )
        power_plants = parse_power_plants(locations_raw)
        suspects = load_suspects()

        locations_by_suspect = {
            (suspect["name"], suspect["surname"]): self.hub.post_api(
                "/api/location",
                {"name": suspect["name"], "surname": suspect["surname"]},
            )
            for suspect in suspects
        }

        return {
            "power_plants": power_plants,
            "suspects": suspects,
            "locations_by_suspect": locations_by_suspect,
        }

    def solve(self, data: dict) -> Any:
        match = find_closest_match(
            data["suspects"], data["locations_by_suspect"], data["power_plants"]
        )
        if match is None:
            raise ValueError("Brak dopasowania podejrzany↔elektrownia — sprawdź dane wejściowe")

        suspect = match["suspect"]
        access = self.hub.post_api(
            "/api/accesslevel",
            {
                "name": suspect["name"],
                "surname": suspect["surname"],
                "birthYear": suspect["born"],
            },
        )

        return format_answer(suspect, access["accessLevel"], match["code"])
