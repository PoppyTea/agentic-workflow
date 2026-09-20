"""
Testy dla S01E02 — findhim.

Unit testy (szybkie, offline) + jeden integration test E2E przez hub
(pytest -m integration), analogicznie do tasks/s01e01_people/test_solution.py.
"""

from __future__ import annotations

import json

import pytest

from tasks.s01e02_findhim.solution import (
    CITY_COORDS,
    PowerPlant,
    _birth_year,
    haversine_km,
    nearest_active_plant,
    parse_power_plants,
)

# ─── haversine_km ─────────────────────────────────────────────────────────────


class TestHaversineKm:
    def test_same_point_is_zero(self):
        assert haversine_km(50.0, 18.0, 50.0, 18.0) == pytest.approx(0.0, abs=1e-6)

    def test_known_distance_warsaw_krakow(self):
        # Warszawa (52.2297, 21.0122) ↔ Kraków (50.0647, 19.9450) ≈ 252 km
        d = haversine_km(52.2297, 21.0122, 50.0647, 19.9450)
        assert d == pytest.approx(252, abs=5)

    def test_symmetric(self):
        d1 = haversine_km(50.3249, 18.7857, 53.4837, 18.7536)
        d2 = haversine_km(53.4837, 18.7536, 50.3249, 18.7857)
        assert d1 == pytest.approx(d2)


# ─── parse_power_plants ────────────────────────────────────────────────────────

SAMPLE_LOCATIONS_JSON = json.dumps(
    {
        "power_plants": {
            "Zabrze": {"is_active": True, "power": "35 MW", "code": "PWR3847PL"},
            "Żarnowiec": {"is_active": False, "power": "0 MW", "code": "PWR6132PL"},
        }
    }
).encode()


class TestParsePowerPlants:
    def test_returns_plant_per_entry(self):
        plants = parse_power_plants(SAMPLE_LOCATIONS_JSON)
        assert len(plants) == 2

    def test_uses_hardcoded_coords(self):
        plants = parse_power_plants(SAMPLE_LOCATIONS_JSON)
        zabrze = next(p for p in plants if p.city == "Zabrze")
        assert (zabrze.lat, zabrze.lon) == CITY_COORDS["Zabrze"]

    def test_preserves_active_flag(self):
        plants = parse_power_plants(SAMPLE_LOCATIONS_JSON)
        active = {p.city: p.is_active for p in plants}
        assert active == {"Zabrze": True, "Żarnowiec": False}

    def test_unknown_city_raises(self):
        raw = json.dumps(
            {"power_plants": {"Atlantis": {"is_active": True, "power": "1 MW", "code": "PWR0000PL"}}}
        ).encode()
        with pytest.raises(ValueError, match="Atlantis"):
            parse_power_plants(raw)


# ─── nearest_active_plant ──────────────────────────────────────────────────────


class TestNearestActivePlant:
    def test_ignores_inactive_plants(self):
        plants = [
            PowerPlant(city="Active", code="A", is_active=True, lat=50.0, lon=18.0),
            PowerPlant(city="Inactive", code="B", is_active=False, lat=50.0001, lon=18.0001),
        ]
        # Lokalizacja dosłownie na "Inactive" — powinna i tak trafić do "Active".
        locations = [{"latitude": 50.0001, "longitude": 18.0001}]
        best = nearest_active_plant(locations, plants)
        assert best is not None
        plant, _distance = best
        assert plant.city == "Active"

    def test_picks_closest_of_multiple_locations(self):
        plants = [PowerPlant(city="P", code="C", is_active=True, lat=50.0, lon=18.0)]
        locations = [
            {"latitude": 60.0, "longitude": 18.0},  # daleko
            {"latitude": 50.001, "longitude": 18.001},  # blisko
        ]
        best = nearest_active_plant(locations, plants)
        assert best is not None
        _plant, distance = best
        assert distance < 1.0

    def test_empty_locations_returns_none(self):
        plants = [PowerPlant(city="P", code="C", is_active=True, lat=50.0, lon=18.0)]
        assert nearest_active_plant([], plants) is None

    def test_no_active_plants_returns_none(self):
        plants = [PowerPlant(city="P", code="C", is_active=False, lat=50.0, lon=18.0)]
        locations = [{"latitude": 50.0, "longitude": 18.0}]
        assert nearest_active_plant(locations, plants) is None


# ─── _birth_year ────────────────────────────────────────────────────────────────


class TestBirthYear:
    def test_extracts_year_from_iso_date(self):
        assert _birth_year({"birthDate": "1986-06-24"}) == 1986

    def test_falls_back_to_born(self):
        assert _birth_year({"born": "1990"}) == 1990


# ─── Integration test ─────────────────────────────────────────────────────────


@pytest.mark.integration
def test_full_solution_against_hub():
    """
    Pełne E2E: odtwarza podejrzanych z S01E01, odpytuje /api/location i
    /api/accesslevel na żywo, submituje do huba.
    Uruchom świadomie: uv run pytest -m integration tasks/s01e02_findhim/
    """
    from core.config import get_config
    from core.hub import HubClient
    from core.llm import LLMClient, create_provider
    from core.observability.setup import setup_observability

    setup_observability()
    cfg = get_config()

    hub = HubClient()
    provider = create_provider("gemini-2.5-flash", cfg)
    llm = LLMClient(provider)

    from tasks.s01e02_findhim.solution import FindhimTask

    task_instance = FindhimTask(hub, llm)
    flag = task_instance.run()

    assert flag is not None, "Nie otrzymano flagi — sprawdź odpowiedź w logach"
    assert flag.startswith("{FLG:")
