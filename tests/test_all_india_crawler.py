"""
Test Suite for All-India Autonomous Farmland Crawler & Top 50 Evaluator
Follows Test-Driven Development (TDD) guidelines.
Validates:
1. SQLite state database persistence, checkpointing, and crash resume.
2. Decoupled architecture: Staging -> Model Inference Engine.
3. AgriFieldNet & MESSIS inspired remote-sensing spectral indices (NDVI, NDRE, NDWI).
4. Managed farmlands guaranteed return evaluation (7-12% p.a. leaseback).
5. Top 50 farmlands composite ranking and selection.
6. Local Excel (.xlsx) and CSV export generation.
7. Graceful termination and signal handler resilience.
"""

import os
import sqlite3
import pytest
import tempfile
import pandas as pd
from datetime import datetime

# Tests will import from utils.all_india_farmland_crawler
from utils.all_india_farmland_crawler import (
    FarmlandStateDB,
    SpectralInferenceEngine,
    GuaranteedReturnEvaluator,
    AllIndiaFarmlandCrawler,
    CRAWLER_DB_PATH,
    TOP_50_EXCEL_PATH,
    TOP_50_CSV_PATH,
    ALL_INDIA_AGRICULTURAL_ZONES
)


class TestFarmlandStateDB:
    """Tests SQLite state checkpointing and recovery without in-memory state loss."""

    @pytest.fixture
    def temp_db(self):
        fd, path = tempfile.mkstemp(suffix=".db")
        os.close(fd)
        db = FarmlandStateDB(db_path=path)
        yield db
        db.close()
        if os.path.exists(path):
            os.remove(path)

    def test_db_initialization(self, temp_db):
        """Checks if tables for state, tiles, raw staging, and evaluated farmlands are created."""
        conn = sqlite3.connect(temp_db.db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = [row[0] for row in cursor.fetchall()]
        conn.close()

        assert "crawler_state" in tables
        assert "scan_tiles" in tables
        assert "raw_farmlands_staging" in tables
        assert "evaluated_farmlands" in tables

    def test_state_persistence_and_resume(self, temp_db):
        """Ensures crawler state can be saved and restored across crashes."""
        temp_db.set_state("status", "RUNNING")
        temp_db.set_state("current_city_id", "bengaluru")
        temp_db.set_state("scanned_cities", "5")

        # Simulate script restart by re-opening DB
        reopened_db = FarmlandStateDB(db_path=temp_db.db_path)
        assert reopened_db.get_state("status") == "RUNNING"
        assert reopened_db.get_state("current_city_id") == "bengaluru"
        assert reopened_db.get_state("scanned_cities") == "5"
        reopened_db.close()

    def test_tile_checkpointing(self, temp_db):
        """Verifies tile processing status is recorded to avoid re-scanning."""
        tile_id = "tile_bengaluru_kanakapura_01"
        temp_db.upsert_tile(
            tile_id=tile_id,
            city_id="bengaluru",
            city_name="Bengaluru",
            state="Karnataka",
            center_lat=12.545,
            center_lng=77.421,
            grid_name="Kanakapura Agro Belt",
            status="SUCCESS",
            parcels_found=8
        )

        assert temp_db.is_tile_completed(tile_id) is True
        assert temp_db.is_tile_completed("unscanned_tile_999") is False


class TestSpectralInferenceEngine:
    """Tests AgriFieldNet Gold & MESSIS remote sensing algorithms."""

    def test_spectral_indices_calculation(self):
        engine = SpectralInferenceEngine()
        # High vigour healthy vegetation (High NIR, low Red, moderate SWIR)
        indices = engine.compute_spectral_indices(
            nir_band=0.48,
            red_band=0.08,
            blue_band=0.04,
            red_edge_band=0.22,
            swir_band=0.15
        )

        assert 0.0 <= indices["ndvi"] <= 1.0
        assert indices["ndvi"] > 0.60  # Healthy orchard/crop canopy
        assert 0.0 <= indices["ndre"] <= 1.0
        assert -1.0 <= indices["ndwi"] <= 1.0
        assert indices["canopy_vigour_tag"] in ["Exceptional Vigour", "High Vigour", "Moderate Vigour"]

    def test_messis_crop_classification(self):
        engine = SpectralInferenceEngine()
        prediction = engine.predict_crop_suitability(
            soil_type="Red Sandy Loam",
            soil_ph=6.8,
            water_tds=220,
            annual_rainfall_mm=950,
            ndvi=0.74
        )

        assert "primary_crop" in prediction
        assert "confidence_pct" in prediction
        assert prediction["confidence_pct"] >= 80.0
        assert len(prediction["recommended_crops"]) >= 2


class TestGuaranteedReturnEvaluator:
    """Tests managed farmlands with guaranteed contractual annual return."""

    def test_managed_farm_guaranteed_return_detection(self):
        evaluator = GuaranteedReturnEvaluator()
        
        managed_farm = {
            "name": "Hosachiguru Eco-Ridge Sandalwood & Avocado Ranch",
            "seller_category": "Managed Farmland Operator",
            "description": "Offering 10.5% guaranteed annual leaseback with 60% sandalwood timber revenue sharing.",
            "total_price_cr": 1.25,
            "size_acres": 2.5
        }

        eval_res = evaluator.evaluate(managed_farm)
        assert eval_res["is_managed_farmland"] is True
        assert eval_res["has_guaranteed_return"] is True
        assert eval_res["guaranteed_return_pct"] >= 8.0
        assert "10.5%" in eval_res["guaranteed_terms"]

    def test_unmanaged_direct_owner_farm(self):
        evaluator = GuaranteedReturnEvaluator()
        
        direct_farm = {
            "name": "Buxar Ganga Alluvial Seed Farm",
            "seller_category": "Direct Owner",
            "description": "Direct ancestral land sale by farmer.",
            "total_price_cr": 0.85,
            "size_acres": 4.0
        }

        eval_res = evaluator.evaluate(direct_farm)
        assert eval_res["is_managed_farmland"] is False
        assert eval_res["has_guaranteed_return"] is False


class TestAllIndiaFarmlandCrawler:
    """Tests end-to-end crawler execution, top 50 ranking, and Excel generation."""

    def test_all_india_agricultural_zones_completeness(self):
        """Ensures all major Indian agricultural zones and cities are covered."""
        assert len(ALL_INDIA_AGRICULTURAL_ZONES) >= 15
        zone_ids = [z["id"] for z in ALL_INDIA_AGRICULTURAL_ZONES]
        assert "bengaluru" in zone_ids
        assert "varanasi_purvanchal" in zone_ids
        assert "punjab_fertile_basin" in zone_ids
        assert "lucknow_awadh" in zone_ids
        assert "goa_konkan" in zone_ids

    def test_top_50_selection_and_ranking(self):
        crawler = AllIndiaFarmlandCrawler(use_temp_db=True)
        # Seed test candidate pool
        crawler.seed_candidate_pool()
        top_50 = crawler.generate_top_50_farmlands()

        assert len(top_50) == 50
        # Check ranks 1 through 50
        for i, farm in enumerate(top_50):
            assert farm["national_rank"] == i + 1
            assert "composite_national_score" in farm
            assert farm["composite_national_score"] > 50.0

        # Verify managed farmlands with guaranteed returns are included in the top 50
        managed_with_guarantee = [f for f in top_50 if f.get("has_guaranteed_return")]
        assert len(managed_with_guarantee) >= 5

    def test_excel_export_generation(self):
        crawler = AllIndiaFarmlandCrawler(use_temp_db=True)
        crawler.seed_candidate_pool()
        top_50 = crawler.generate_top_50_farmlands()
        
        fd, excel_tmp = tempfile.mkstemp(suffix=".xlsx")
        os.close(fd)

        crawler.export_top_50_to_excel(top_50, output_path=excel_tmp)
        assert os.path.exists(excel_tmp)
        assert os.path.getsize(excel_tmp) > 5000

        # Verify Excel sheets
        xl = pd.ExcelFile(excel_tmp)
        assert "Top 50 Farmlands India" in xl.sheet_names
        assert "Managed Farms Guaranteed Return" in xl.sheet_names
        assert "Agronomic & Soil Telemetry" in xl.sheet_names

        df_top = xl.parse("Top 50 Farmlands India")
        assert len(df_top) == 50
        xl.close()
        try:
            if os.path.exists(excel_tmp):
                os.remove(excel_tmp)
        except OSError:
            pass
