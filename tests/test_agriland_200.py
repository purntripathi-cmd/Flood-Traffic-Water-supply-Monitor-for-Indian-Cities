"""
Test Suite for AgriLand-200 Inventory Aggregator & Verification Engine
(Varanasi 200 km Radial Agro-Zone)
Tests cover:
1. Normalization Engine: Land unit conversions (Purvanchal Pakka Bigha, Kachha Bigha, Biswa, Kattha, Dhur to Acres & Sqm)
2. Geo-Spatial Radial Buffer: 200 km distance filtering around Varanasi (25.3176° N, 82.9739° E)
3. Due Diligence Scoring Model (0-100): Khasra, SARFAESI, 12-Yr Barah Sala, Dakhil-Kharij, Road access
4. Tier Source Categorization: Tier 1 (Govt) to Tier 5 (e-Paper Public Notices)
5. Inventory Integrity: Validation of ingested listings across UP, Bihar, and MP border districts
"""

import pytest
import math
import os
import json

from utils.agriland_200 import (
    VARANASI_LAT,
    VARANASI_LNG,
    MAX_BUFFER_KM,
    DISTRICTS_IN_SCOPE,
    TIER_DEFINITIONS,
    LandUnitConverter,
    GeoSpatialRadialFilter,
    DueDiligenceScoringModel,
    TierSourcesManager,
    AgriLand200Engine
)


# =====================================================================
# 1. TEST SUITE: LAND UNIT NORMALIZATION ENGINE
# =====================================================================
class TestLandUnitConverter:
    """Verifies precision conversion of Purvanchal, Bihar, and Central Indian land units."""

    def test_pakka_bigha_conversion(self):
        # In Purvanchal (Varanasi, Chandauli, Jaunpur, Ghazipur):
        # 1 Pakka Bigha = 20 Biswa = 27,225 sq.ft = 2,529.285 sq.m = 0.625 Acres (5/8 of an Acre)
        acres = LandUnitConverter.to_acres(1.0, "pakka_bigha")
        assert math.isclose(acres, 0.625, rel_tol=1e-3)

        sqm = LandUnitConverter.to_sqm(1.0, "pakka_bigha")
        assert math.isclose(sqm, 2529.285, rel_tol=1e-2)

        # 4 Pakka Bigha should be exactly 2.5 Acres
        assert math.isclose(LandUnitConverter.to_acres(4.0, "pakka_bigha"), 2.5, rel_tol=1e-3)

    def test_kachha_bigha_conversion(self):
        # 1 Kachha Bigha is 1/3 of a Pakka Bigha = 9,075 sq.ft = 843.09 sq.m = ~0.20833 Acres
        acres = LandUnitConverter.to_acres(1.0, "kachha_bigha")
        assert math.isclose(acres, 0.20833, rel_tol=1e-3)

    def test_biswa_conversion(self):
        # 1 Biswa = 1/20 of Pakka Bigha = 1,361.25 sq.ft = 0.03125 Acres
        acres = LandUnitConverter.to_acres(20.0, "biswa")
        assert math.isclose(acres, 0.625, rel_tol=1e-3)  # 20 Biswa = 1 Pakka Bigha

    def test_bihar_kattha_and_dhur_conversion(self):
        # In Bihar border belt (Kaimur, Buxar, Rohtas):
        # 1 Bigha = 20 Kattha; 1 Kattha = 20 Dhur; 1 Kattha = 1,361.25 sq.ft = 0.03125 Acres
        kattha_acres = LandUnitConverter.to_acres(20.0, "kattha")
        assert math.isclose(kattha_acres, 0.625, rel_tol=1e-3)

        dhur_acres = LandUnitConverter.to_acres(400.0, "dhur")
        assert math.isclose(dhur_acres, 0.625, rel_tol=1e-3)

    def test_hectare_and_guntha_conversion(self):
        # 1 Hectare = 2.47105 Acres
        assert math.isclose(LandUnitConverter.to_acres(1.0, "hectare"), 2.47105, rel_tol=1e-3)
        # 1 Guntha = 0.025 Acres
        assert math.isclose(LandUnitConverter.to_acres(40.0, "guntha"), 1.0, rel_tol=1e-3)

    def test_format_all_units(self):
        # Given 2.5 Acres, should return formatted strings across all regional conventions
        res = LandUnitConverter.format_all_units(2.5)
        assert res["acres"] == 2.5
        assert math.isclose(res["pakka_bigha"], 4.0, rel_tol=1e-2)
        assert math.isclose(res["biswa"], 80.0, rel_tol=1e-2)
        assert math.isclose(res["kattha"], 80.0, rel_tol=1e-2)
        assert "pakka_bigha_display" in res
        assert "sq_metres_display" in res


# =====================================================================
# 2. TEST SUITE: GEO-SPATIAL 200 KM RADIAL BUFFER FILTER
# =====================================================================
class TestGeoSpatialRadialFilter:
    """Verifies that listings strictly within 200 km radial buffer of Varanasi are included."""

    def test_varanasi_zero_point(self):
        dist = GeoSpatialRadialFilter.calculate_distance_km(VARANASI_LAT, VARANASI_LNG)
        assert math.isclose(dist, 0.0, abs_tol=0.1)
        assert GeoSpatialRadialFilter.is_within_buffer(VARANASI_LAT, VARANASI_LNG) is True

    def test_core_up_purvanchal_districts(self):
        # Chandauli (~30 km)
        chandauli_dist = GeoSpatialRadialFilter.calculate_distance_km(25.2585, 83.2662)
        assert chandauli_dist < 45.0
        assert GeoSpatialRadialFilter.is_within_buffer(25.2585, 83.2662) is True

        # Mirzapur (~48 km)
        mirzapur_dist = GeoSpatialRadialFilter.calculate_distance_km(25.1337, 82.5644)
        assert mirzapur_dist < 60.0
        assert GeoSpatialRadialFilter.is_within_buffer(25.1337, 82.5644) is True

        # Jaunpur (~58 km)
        jaunpur_dist = GeoSpatialRadialFilter.calculate_distance_km(25.7464, 82.6837)
        assert jaunpur_dist < 75.0
        assert GeoSpatialRadialFilter.is_within_buffer(25.7464, 82.6837) is True

        # Ghazipur (~68 km)
        ghazipur_dist = GeoSpatialRadialFilter.calculate_distance_km(25.5869, 83.5770)
        assert ghazipur_dist < 85.0
        assert GeoSpatialRadialFilter.is_within_buffer(25.5869, 83.5770) is True

        # Prayagraj (~115 km)
        prayagraj_dist = GeoSpatialRadialFilter.calculate_distance_km(25.4358, 81.8463)
        assert prayagraj_dist < 130.0
        assert GeoSpatialRadialFilter.is_within_buffer(25.4358, 81.8463) is True

        # Azamgarh (~90 km)
        azamgarh_dist = GeoSpatialRadialFilter.calculate_distance_km(26.0689, 83.1836)
        assert azamgarh_dist < 115.0
        assert GeoSpatialRadialFilter.is_within_buffer(26.0689, 83.1836) is True

        # Sonbhadra / Robertsganj (~85 km)
        sonbhadra_dist = GeoSpatialRadialFilter.calculate_distance_km(24.6858, 83.0658)
        assert sonbhadra_dist < 105.0
        assert GeoSpatialRadialFilter.is_within_buffer(24.6858, 83.0658) is True

    def test_bihar_border_belt(self):
        # Kaimur / Bhabua (~85 km)
        kaimur_dist = GeoSpatialRadialFilter.calculate_distance_km(25.0450, 83.6150)
        assert kaimur_dist < 100.0
        assert GeoSpatialRadialFilter.is_within_buffer(25.0450, 83.6150) is True

        # Buxar (~115 km)
        buxar_dist = GeoSpatialRadialFilter.calculate_distance_km(25.5647, 83.9777)
        assert buxar_dist < 135.0
        assert GeoSpatialRadialFilter.is_within_buffer(25.5647, 83.9777) is True

        # Rohtas / Sasaram (~130 km)
        rohtas_dist = GeoSpatialRadialFilter.calculate_distance_km(24.9528, 84.0317)
        assert rohtas_dist < 155.0
        assert GeoSpatialRadialFilter.is_within_buffer(24.9528, 84.0317) is True

    def test_mp_border_belt(self):
        # Rewa (~185 km)
        rewa_dist = GeoSpatialRadialFilter.calculate_distance_km(24.5362, 81.3037)
        assert rewa_dist < 200.0
        assert GeoSpatialRadialFilter.is_within_buffer(24.5362, 81.3037) is True

        # Singrauli (~175 km)
        singrauli_dist = GeoSpatialRadialFilter.calculate_distance_km(24.1992, 82.6645)
        assert singrauli_dist < 200.0
        assert GeoSpatialRadialFilter.is_within_buffer(24.1992, 82.6645) is True

    def test_out_of_bounds_locations(self):
        # Lucknow (~285 km from Varanasi) -> OUT OF 200 KM BUFFER
        assert GeoSpatialRadialFilter.is_within_buffer(26.8467, 80.9462) is False
        # Patna (~220 km from Varanasi) -> OUT OF 200 KM BUFFER
        assert GeoSpatialRadialFilter.is_within_buffer(25.5941, 85.1376) is False
        # Bengaluru (~1500 km) -> OUT OF BUFFER
        assert GeoSpatialRadialFilter.is_within_buffer(12.9716, 77.5946) is False


# =====================================================================
# 3. TEST SUITE: DUE DILIGENCE SCORING MODEL (0-100)
# =====================================================================
class TestDueDiligenceScoringModel:
    """Tests composite legal, debt-clearance, and access audit scoring."""

    def test_perfect_due_diligence_score(self):
        record = {
            "has_khasra_verification": True,          # +30
            "sarfaesi_bank_clearance": True,          # +25
            "barah_sala_encumbrance_clean": True,     # +20
            "dakhil_kharij_mutated": True,            # +15
            "paved_road_approach": True,              # +10
            "has_co_sharer_dispute": False,           # -25 penalty if True
            "in_flood_depression_tal": False,         # -20 penalty if True
            "is_usar_saline_soil": False              # -15 penalty if True
        }
        res = DueDiligenceScoringModel.calculate_score(record)
        assert res["score"] == 100
        assert res["grade"] == "A+ Sovereign Grade"
        assert res["is_bankable"] is True

    def test_distressed_auction_with_encumbrance_penalty(self):
        record = {
            "has_khasra_verification": True,          # +30
            "sarfaesi_bank_clearance": False,         # 0 (Active bank auction recovery)
            "barah_sala_encumbrance_clean": False,    # 0 (Carries prior mortgage)
            "dakhil_kharij_mutated": True,            # +15
            "paved_road_approach": True,              # +10
            "has_co_sharer_dispute": False,
            "in_flood_depression_tal": False,
            "is_usar_saline_soil": False
        }
        res = DueDiligenceScoringModel.calculate_score(record)
        assert res["score"] == 55
        assert res["grade"] == "C Conditional Clearance"

    def test_severe_dispute_penalty_clamping(self):
        # Extreme penalty case should clamp at 0 and not go negative
        record = {
            "has_khasra_verification": False,
            "sarfaesi_bank_clearance": False,
            "barah_sala_encumbrance_clean": False,
            "dakhil_kharij_mutated": False,
            "paved_road_approach": False,
            "has_co_sharer_dispute": True,
            "in_flood_depression_tal": True,
            "is_usar_saline_soil": True
        }
        res = DueDiligenceScoringModel.calculate_score(record)
        assert res["score"] == 0
        assert res["grade"] == "F High Legal / Physical Hazard"


# =====================================================================
# 4. TEST SUITE: TIER SOURCES CATEGORIZATION
# =====================================================================
class TestTierSourcesManager:
    """Tests 5-tier classification of land intelligence sources."""

    def test_tier_definitions(self):
        assert "tier_1" in TIER_DEFINITIONS
        assert "tier_2" in TIER_DEFINITIONS
        assert "tier_3" in TIER_DEFINITIONS
        assert "tier_4" in TIER_DEFINITIONS
        assert "tier_5" in TIER_DEFINITIONS

        assert "UP Bhulekh" in TIER_DEFINITIONS["tier_1"]["sources"]
        assert "IBAPI" in TIER_DEFINITIONS["tier_2"]["sources"]
        assert "SFarmsIndia" in TIER_DEFINITIONS["tier_3"]["sources"]
        assert "YouTube" in TIER_DEFINITIONS["tier_4"]["sources"]
        assert "Amar Ujala" in TIER_DEFINITIONS["tier_5"]["sources"]

    def test_categorize_source(self):
        assert TierSourcesManager.get_tier("UP Bhulekh Portal RTC") == "Tier 1: Government Land Registry"
        assert TierSourcesManager.get_tier("IBAPI Bank SARFAESI Auction") == "Tier 2: Bank Distress / SARFAESI Auction"
        assert TierSourcesManager.get_tier("SFarmsIndia Direct Listing") == "Tier 3: Verified Real Estate Portal"
        assert TierSourcesManager.get_tier("YouTube Purvanchal Drone Walk Lead") == "Tier 4: Social / Video Direct Lead"
        assert TierSourcesManager.get_tier("Amar Ujala Court Notice E-Paper") == "Tier 5: Newspaper Public Notice"


# =====================================================================
# 5. TEST SUITE: AGRI-LAND 200 INVENTORY INTEGRITY
# =====================================================================
class TestAgriLand200InventoryIntegrity:
    """Verifies that all 200 km regional listings satisfy data contracts."""

    def test_districts_in_scope_list(self):
        # 9 UP districts + 3 Bihar border districts + 2 MP border districts = 14 districts
        assert len(DISTRICTS_IN_SCOPE) == 14
        assert "Varanasi" in DISTRICTS_IN_SCOPE
        assert "Chandauli" in DISTRICTS_IN_SCOPE
        assert "Mirzapur" in DISTRICTS_IN_SCOPE
        assert "Jaunpur" in DISTRICTS_IN_SCOPE
        assert "Ghazipur" in DISTRICTS_IN_SCOPE
        assert "Azamgarh" in DISTRICTS_IN_SCOPE
        assert "Prayagraj" in DISTRICTS_IN_SCOPE
        assert "Bhadohi" in DISTRICTS_IN_SCOPE
        assert "Sonbhadra" in DISTRICTS_IN_SCOPE
        assert "Kaimur" in DISTRICTS_IN_SCOPE
        assert "Buxar" in DISTRICTS_IN_SCOPE
        assert "Rohtas" in DISTRICTS_IN_SCOPE
        assert "Rewa" in DISTRICTS_IN_SCOPE
        assert "Singrauli" in DISTRICTS_IN_SCOPE

    def test_ingested_farmlands_json_in_buffer(self):
        farmlands_path = os.path.join(os.path.dirname(__file__), "..", "data", "farmlands.json")
        assert os.path.exists(farmlands_path), "farmlands.json must exist"
        with open(farmlands_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        var_farms = [f for f in data if f.get("city_id") == "varanasi_100km"]
        assert len(var_farms) >= 14, f"Expected at least 14 AgriLand-200 parcels, got {len(var_farms)}"

        # Verify all parcels are strictly within 200 km
        for farm in var_farms:
            dist = farm.get("radial_distance_from_varanasi_km")
            assert dist is not None, f"Farm {farm['id']} missing radial distance"
            assert dist <= 200.0, f"Farm {farm['id']} is {dist} km from Varanasi (>200 km)"
            assert "due_diligence_score" in farm
            assert 0 <= farm["due_diligence_score"] <= 100
            assert "khasra_khatauni_number" in farm
            assert "contact_phone" in farm
            assert "sourcing_tier" in farm

    def test_three_state_coverage_and_tiers(self):
        farmlands_path = os.path.join(os.path.dirname(__file__), "..", "data", "farmlands.json")
        with open(farmlands_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        var_farms = [f for f in data if f.get("city_id") == "varanasi_100km"]

        states = {f.get("regional_state") for f in var_farms}
        assert "Uttar Pradesh" in states
        assert "Bihar" in states
        assert "Madhya Pradesh" in states

        # Verify Tiers
        tiers = {f.get("sourcing_tier") for f in var_farms}
        assert any("Tier 1" in t for t in tiers), "Tier 1 must be present"
        assert any("Tier 2" in t for t in tiers), "Tier 2 Bank Auction must be present"
        assert any("Tier 3" in t for t in tiers), "Tier 3 Portals must be present"
        assert any("Tier 4" in t for t in tiers), "Tier 4 Video/Drone leads must be present"
        assert any("Tier 5" in t for t in tiers), "Tier 5 e-Paper notices must be present"


# =====================================================================
# 6. TEST SUITE: DEDICATED VARANASI 200 KM BUFFER DATASET & ARTIFACTS
# =====================================================================
class TestDedicatedVaranasiBufferDataset:
    """Verifies that the standalone data/agriland_200_varanasi.json and CSV/Excel exports exist and are valid."""

    @pytest.fixture
    def varanasi_dataset(self):
        json_path = os.path.join(os.path.dirname(__file__), "..", "data", "agriland_200_varanasi.json")
        assert os.path.exists(json_path), "Dedicated agriland_200_varanasi.json must exist"
        with open(json_path, "r", encoding="utf-8") as f:
            return json.load(f)

    def test_varanasi_json_minimum_volume(self, varanasi_dataset):
        # Must contain at least 50 verified parcels (currently 76)
        assert len(varanasi_dataset) >= 50, f"Expected >= 50 parcels, found {len(varanasi_dataset)}"

    def test_varanasi_proper_density(self, varanasi_dataset):
        # Core Varanasi district must have at least 10 detailed parcels
        v_parcels = [f for f in varanasi_dataset if f.get("regional_district") == "Varanasi"]
        assert len(v_parcels) >= 10, f"Expected >= 10 parcels in Varanasi district, found {len(v_parcels)}"

    def test_all_14_districts_represented(self, varanasi_dataset):
        present_districts = {f.get("regional_district") for f in varanasi_dataset}
        for dist in DISTRICTS_IN_SCOPE:
            assert dist in present_districts, f"District {dist} missing from dedicated Varanasi dataset"

    def test_strict_radial_distance_enforcement(self, varanasi_dataset):
        for f in varanasi_dataset:
            dist = f.get("radial_distance_from_varanasi_km", 999)
            assert dist <= 200.0, f"Parcel {f['id']} exceeds 200 km limit: {dist} km"

    def test_master_csv_and_excel_exports_exist(self):
        csv_path = os.path.join(os.path.dirname(__file__), "..", "data", "csv_exports", "agriland_200_varanasi_buffer_master.csv")
        assert os.path.exists(csv_path), "Master CSV export must exist"
        excel_path = os.path.join(os.path.dirname(__file__), "..", "data", "agriland_200_varanasi_buffer_master.xlsx")
        assert os.path.exists(excel_path), "Master Excel export must exist"


# =====================================================================
# 6. TEST SUITE: FARMLAND TELEMETRY CARD ROBUSTNESS & POLYMORPHISM
# =====================================================================
class TestFarmlandHtmlTelemetryCardRobustness:
    """Verifies that farmland HTML presentation cards handle list, dict, str, and None crop payloads without crashing."""

    def test_list_supported_crops_does_not_raise(self):
        from utils.farmland_view import render_agronomic_telemetry_html, render_seller_contact_card_html
        farm = {
            "name": "Kashi Vedic Agro Estate",
            "supported_crops": ["Certified Sandalwood (Chandan)", "VNR Bihi Guava", "Hass Avocado"],
            "soil_type": "Rich Gangetic Loam",
            "soil_ph": 7.4,
            "organic_carbon_pct": 0.85,
            "water_source": "Perennial Deep Tubewell",
            "water_tds_ppm": 210,
            "drip_irrigation_installed": True,
            "power_supply": "Dedicated 3-Phase Line",
            "annual_agro_yield_estimate_lakhs": 9.5
        }
        html = render_agronomic_telemetry_html(farm)
        assert "Certified Sandalwood (Chandan)" in html
        assert "VNR Bihi Guava" in html
        assert "Hass Avocado" in html

    def test_dict_supported_crops_does_not_raise(self):
        from utils.farmland_view import render_agronomic_telemetry_html
        farm = {
            "name": "Awadh High-Value Plantation",
            "supported_crops": {
                "high_value_crops": "Malihabad Dussehri Mango & Dragonfruit",
                "soil_suitability_score": 98,
                "irrigation_feasibility": "High"
            }
        }
        html = render_agronomic_telemetry_html(farm)
        assert "Malihabad Dussehri Mango & Dragonfruit" in html

    def test_str_and_none_supported_crops(self):
        from utils.farmland_view import render_agronomic_telemetry_html
        for val in ["Avocado, Teakwood, Guava", None, {}]:
            farm = {"name": "Test Farm", "supported_crops": val}
            html = render_agronomic_telemetry_html(farm)
            assert isinstance(html, str)
            assert len(html) > 50

    def test_all_existing_data_parcels_render_cleanly(self):
        from utils.farmland_view import render_agronomic_telemetry_html, render_seller_contact_card_html, render_agriland_200_audit_html
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        with open(os.path.join(base_dir, "data", "farmlands.json"), "r", encoding="utf-8") as f:
            farms = json.load(f)
        with open(os.path.join(base_dir, "data", "agriland_200_varanasi.json"), "r", encoding="utf-8") as f:
            agri = json.load(f)

        for farm in farms + agri:
            h1 = render_agronomic_telemetry_html(farm)
            h2 = render_seller_contact_card_html(farm)
            h3 = render_agriland_200_audit_html(farm)
            assert isinstance(h1, str)
            assert isinstance(h2, str)
            assert isinstance(h3, str)



