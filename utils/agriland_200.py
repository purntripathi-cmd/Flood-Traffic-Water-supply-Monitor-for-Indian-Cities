"""
AgriLand-200 Inventory Aggregator & Multi-Tier Verification Engine
Specialized for the 200 km radial buffer around Varanasi (25.3176° N, 82.9739° E)

Geographic Scope:
- UP Purvanchal (9 Districts): Varanasi, Chandauli, Mirzapur, Jaunpur, Ghazipur, Azamgarh, Prayagraj, Bhadohi, Sonbhadra
- Bihar Border Belt (3 Districts): Kaimur (Bhabua), Buxar, Rohtas (Sasaram)
- MP Border Belt (2 Districts): Rewa, Singrauli

Core Engines:
1. Normalization Engine: Converts local units (Purvanchal Pakka Bigha, Kachha Bigha, Biswa, Kattha, Dhur) to Standard Acres & Sq.M.
2. Geo-Spatial Radial Filter: Precise geodesic haversine radial distance from Varanasi Zero-Point.
3. Due Diligence Scoring Model (0-100): Khasra/Khatauni verification (+30), SARFAESI bank clearance (+25), 12-Yr Barah Sala (+20), Dakhil-Kharij (+15), Road access (+10).
4. Multi-Tier Ingestion & Intelligence Manager: Organizes listings into Tiers 1 through 5.
"""

import math
from typing import Dict, Any, List, Optional, Tuple

# Geodesic Zero-Point: Varanasi (Dashashwamedh / Cantt Central Datum)
VARANASI_LAT = 25.3176
VARANASI_LNG = 82.9739
MAX_BUFFER_KM = 200.0

# 14 Districts strictly in the 200 km radius
DISTRICTS_IN_SCOPE = [
    "Varanasi",
    "Chandauli",
    "Mirzapur",
    "Jaunpur",
    "Ghazipur",
    "Azamgarh",
    "Prayagraj",
    "Bhadohi",
    "Sonbhadra",
    "Kaimur",
    "Buxar",
    "Rohtas",
    "Rewa",
    "Singrauli"
]

# District metadata with state and typical soil profile
DISTRICT_PROFILES = {
    "Varanasi": {"state": "Uttar Pradesh", "zone": "UP Purvanchal", "soil": "Deep Gangetic Silt Loam (Khadar / Bangar)", "irrigation": "Ganga / Varuna Canals & Deep Aquifers"},
    "Chandauli": {"state": "Uttar Pradesh", "zone": "UP Purvanchal", "soil": "Alluvial Clay Loam (Grain Bowl of UP - GI Kalanamak)", "irrigation": "Chandraprabha & Karmanasa Canal Systems"},
    "Mirzapur": {"state": "Uttar Pradesh", "zone": "UP Purvanchal", "soil": "Vindhyan Red Loam & Black Soil with Stone Sub-stratum", "irrigation": "Sirsi & Meja Reservoirs, Tubewells"},
    "Jaunpur": {"state": "Uttar Pradesh", "zone": "UP Purvanchal", "soil": "Fine Sandy Loam (Gomti Basin - High Potash)", "irrigation": "Gomti Lift Canals & Deep Borewells"},
    "Ghazipur": {"state": "Uttar Pradesh", "zone": "UP Purvanchal", "soil": "Fertile Gangetic Loam (Aromatic Roses & Mentha)", "irrigation": "Ganga & Karmnasa Rivers"},
    "Azamgarh": {"state": "Uttar Pradesh", "zone": "UP Purvanchal", "soil": "Heavy Alluvial Clay Loam (Tamsa Basin)", "irrigation": "Sharda Sahayak Canal Network"},
    "Prayagraj": {"state": "Uttar Pradesh", "zone": "UP Purvanchal", "soil": "Alluvial Bluff & Fine Sand Loam (GI Allahabad Safeda Guava)", "irrigation": "Ganga / Yamuna Doab Canal Systems"},
    "Bhadohi": {"state": "Uttar Pradesh", "zone": "UP Purvanchal", "soil": "Silt Loam with High Organic Carbon (Seed Multiplication)", "irrigation": "Tubewells & Minor Canals"},
    "Sonbhadra": {"state": "Uttar Pradesh", "zone": "UP Purvanchal", "soil": "Vindhyan Plateau Black Loam & Mineral Silt", "irrigation": "Rihand & Kanhar Irrigation Systems"},
    "Kaimur": {"state": "Bihar", "zone": "Bihar Border Belt", "soil": "Rich Sone-Karmanasa Alluvial Loam (Rice-Wheat-Pulses)", "irrigation": "Son High-Level Canal"},
    "Buxar": {"state": "Bihar", "zone": "Bihar Border Belt", "soil": "Gangetic Floodplain Silt Loam (High Nitrogen)", "irrigation": "Son Canal & Ganga Pumping"},
    "Rohtas": {"state": "Bihar", "zone": "Bihar Border Belt", "soil": "Alluvial Clay (Granary of Bihar - Basmati Paddy)", "irrigation": "Sone Barrage Canal System"},
    "Rewa": {"state": "Madhya Pradesh", "zone": "MP Border Belt", "soil": "Vindhyan Plateau Red-Black Mixed Loam", "irrigation": "Tons & Bansagar Canal Networks"},
    "Singrauli": {"state": "Madhya Pradesh", "zone": "MP Border Belt", "soil": "Plateau Loamy Red Soil with High Iron", "irrigation": "Rihand Reservoir Perimeter & Springs"}
}

# 5-Tier Core Data Sources Framework
TIER_DEFINITIONS = {
    "tier_1": {
        "title": "Government Land Registries",
        "sources": ["UP Bhulekh", "UP Stamp & Registration (IGRSUP)", "Bihar Bhumi", "MP Bhulekh"],
        "attributes": ["Khasra / Khatauni Record", "12-Year Encumbrance (Barah Sala)", "Co-Sharer Count", "Mutation (Dakhil-Kharij) Status"],
        "badge": "🏛️ Tier 1: Govt Land Registry Verified",
        "color": "#10B981"
    },
    "tier_2": {
        "title": "Bank Distress / SARFAESI Auctions",
        "sources": ["IBAPI", "Bank Auctions India", "Eauctions India"],
        "attributes": ["Reserve Price Discount", "EMD Cutoffs", "Authorized Officer Contact", "SARFAESI Sec 13(4) Possession"],
        "badge": "🏦 Tier 2: Bank SARFAESI Distress Auction",
        "color": "#F59E0B"
    },
    "tier_3": {
        "title": "Verified Real Estate Portals",
        "sources": ["SFarmsIndia", "Farmland India", "99acres", "MagicBricks"],
        "attributes": ["Market Asking Rate", "Per-Acre / Bigha Rate", "Water Source Claims", "Highway Proximity"],
        "badge": "🌐 Tier 3: Verified Agri-Portal Listing",
        "color": "#38BDF8"
    },
    "tier_4": {
        "title": "Social & Video Media (Direct Leads)",
        "sources": ["YouTube", "Facebook", "X (Twitter)"],
        "attributes": ["Direct Owner Contact", "Drone Parcel Walk Video", "Road Frontage Footage", "NHAI Corridor Lead"],
        "badge": "🎥 Tier 4: Social / Video Direct Farmer Lead",
        "color": "#818CF8"
    },
    "tier_5": {
        "title": "Newspaper Notices & e-Papers",
        "sources": ["Amar Ujala", "Dainik Jagran", "Hindustan Purvanchal"],
        "attributes": ["Court Auction Notice (सार्वजनिक सूचना)", "Possession Notice", "Title Dispute Caveat Check"],
        "badge": "📰 Tier 5: E-Paper Legal Notice Cleared",
        "color": "#A855F7"
    }
}


# =====================================================================
# 1. NORMALIZATION ENGINE: MULTI-UNIT CONVERTER
# =====================================================================
class LandUnitConverter:
    """
    Standard conversion factors for regional Indian land measurements.
    Baseline reference: Standard International Acre (43,560 sq.ft = 4,046.85642 sq.m)
    """

    # Exact conversion factors to standard ACRES
    UNIT_TO_ACRE = {
        "acre": 1.0,
        "pakka_bigha": 0.625,               # 20 Biswa = 27,225 sqft = 2529.285 sqm = 5/8 Acre (Purvanchal UP)
        "kachha_bigha": 0.625 / 3.0,        # 1/3 of Pakka Bigha = 9,075 sqft = ~0.20833 Acres
        "biswa": 0.625 / 20.0,              # 1/20 of Pakka Bigha = 1,361.25 sqft = 0.03125 Acres
        "kattha": 0.625 / 20.0,             # Bihar border standard: 20 Kattha = 1 Bigha = 1,361.25 sqft
        "dhur": (0.625 / 20.0) / 20.0,      # 1/20 of Kattha = 68.0625 sqft = 0.0015625 Acres
        "hectare": 2.4710538,               # 10,000 sq.m = 2.47105 Acres
        "guntha": 0.025,                    # 1,089 sq.ft = 40 Gunthas per Acre
        "sq_metres": 0.00024710538,
        "sq_feet": 1.0 / 43560.0
    }

    SQ_METRES_PER_ACRE = 4046.8564224
    SQ_FEET_PER_ACRE = 43560.0

    @classmethod
    def to_acres(cls, value: float, unit: str) -> float:
        """Converts any recognized land measurement unit to standard Acres."""
        unit_key = unit.lower().strip().replace(" ", "_").replace("-", "_")
        factor = cls.UNIT_TO_ACRE.get(unit_key)
        if factor is None:
            # Fallback heuristic
            if "pakka" in unit_key or "bigha" in unit_key and "kachha" not in unit_key:
                factor = cls.UNIT_TO_ACRE["pakka_bigha"]
            elif "kachha" in unit_key:
                factor = cls.UNIT_TO_ACRE["kachha_bigha"]
            elif "biswa" in unit_key:
                factor = cls.UNIT_TO_ACRE["biswa"]
            elif "kattha" in unit_key:
                factor = cls.UNIT_TO_ACRE["kattha"]
            elif "dhur" in unit_key:
                factor = cls.UNIT_TO_ACRE["dhur"]
            elif "hectare" in unit_key or "ha" in unit_key:
                factor = cls.UNIT_TO_ACRE["hectare"]
            elif "guntha" in unit_key:
                factor = cls.UNIT_TO_ACRE["guntha"]
            else:
                factor = 1.0
        return float(value) * factor

    @classmethod
    def to_sqm(cls, value: float, unit: str) -> float:
        """Converts any recognized land measurement unit to square metres."""
        acres = cls.to_acres(value, unit)
        return acres * cls.SQ_METRES_PER_ACRE

    @classmethod
    def format_all_units(cls, acres: float) -> Dict[str, Any]:
        """Returns standard conversions across all regional and statutory units."""
        pakka_bigha = acres / cls.UNIT_TO_ACRE["pakka_bigha"]
        biswa = pakka_bigha * 20.0
        kattha = acres / cls.UNIT_TO_ACRE["kattha"]
        dhur = kattha * 20.0
        hectares = acres / cls.UNIT_TO_ACRE["hectare"]
        sq_m = acres * cls.SQ_METRES_PER_ACRE
        sq_ft = acres * cls.SQ_FEET_PER_ACRE

        return {
            "acres": round(acres, 3),
            "hectares": round(hectares, 3),
            "pakka_bigha": round(pakka_bigha, 2),
            "biswa": round(biswa, 1),
            "kattha": round(kattha, 1),
            "dhur": round(dhur, 1),
            "sq_metres": round(sq_m, 1),
            "sq_feet": round(sq_ft, 0),
            "pakka_bigha_display": f"{pakka_bigha:.2f} Pakka Bigha ({biswa:.1f} Biswa)",
            "kattha_display": f"{kattha:.1f} Kattha ({dhur:.0f} Dhur)",
            "sq_metres_display": f"{sq_m:,.1f} sq.m",
            "sq_feet_display": f"{sq_ft:,.0f} sq.ft",
            "summary_tag": f"{acres:.2f} Acres • {pakka_bigha:.2f} Bigha • {hectares:.2f} Ha"
        }


# =====================================================================
# 2. GEO-SPATIAL RADIAL FILTER (200 KM BUFFER)
# =====================================================================
class GeoSpatialRadialFilter:
    """
    Calculates geodesic distance from Varanasi Zero-Point (25.3176° N, 82.9739° E)
    and enforces the strict 200 km regional boundary constraint.
    """

    EARTH_RADIUS_KM = 6371.0

    @classmethod
    def calculate_distance_km(cls, lat: float, lng: float, origin_lat: float = VARANASI_LAT, origin_lng: float = VARANASI_LNG) -> float:
        """Haversine formula calculating great-circle distance between two coordinates in km."""
        phi1 = math.radians(origin_lat)
        phi2 = math.radians(lat)
        delta_phi = math.radians(lat - origin_lat)
        delta_lambda = math.radians(lng - origin_lng)

        a = math.sin(delta_phi / 2.0) ** 2 + \
            math.cos(phi1) * math.cos(phi2) * (math.sin(delta_lambda / 2.0) ** 2)
        c = 2.0 * math.atan2(math.sqrt(a), math.sqrt(1.0 - a))
        return cls.EARTH_RADIUS_KM * c

    @classmethod
    def is_within_buffer(cls, lat: float, lng: float, buffer_km: float = MAX_BUFFER_KM) -> bool:
        """Checks if a location is strictly within the specified buffer radius (default: 200 km)."""
        dist = cls.calculate_distance_km(lat, lng)
        return dist <= buffer_km


# =====================================================================
# 3. DUE DILIGENCE SCORING MODEL (0-100)
# =====================================================================
class DueDiligenceScoringModel:
    """
    Calculates a rigorous due diligence score (0-100) based on statutory records,
    bank debt clearance, mutation status, physical approach, and environmental risks.
    """

    MAX_SCORE = 100

    @classmethod
    def calculate_score(cls, record: Dict[str, Any]) -> Dict[str, Any]:
        """
        Scoring Rubric:
        - Khasra / Khatauni verified on State Portal (UP/Bihar/MP Bhulekh): +30 pts
        - SARFAESI / Bank Debt Clearance / Free of Mortgage: +25 pts
        - 12-Year Barah Sala Clean Encumbrance Certificate: +20 pts
        - Mutation (Dakhil-Kharij) completed in buyer/seller ledger: +15 pts
        - Paved Approach Road / NHAI highway connectivity: +10 pts

        Deductions & Penalties:
        - Active Co-Sharer Dispute / Civil Court Partition Suit: -25 pts
        - Inundation Depression / Monsoon Tal Basin Waterlogging: -20 pts
        - Usar / High-Salinity / Alkaline Soil (pH > 8.5 or < 5.5): -15 pts
        """
        score = 0
        breakdown = []

        # Positive criteria
        if record.get("has_khasra_verification", False):
            score += 30
            breakdown.append("✅ +30 pts: Khasra/Khatauni Verified on Official State Bhulekh Portal")
        else:
            breakdown.append("❌ 0 pts: Khasra / Khatauni unverified or pending revenue extraction")

        if record.get("sarfaesi_bank_clearance", False):
            score += 25
            breakdown.append("✅ +25 pts: Free of SARFAESI bank attachment & mortgage debt cleared")
        else:
            breakdown.append("⚠️ 0 pts: Active bank auction or mortgage debt attachment (Conditional)")

        if record.get("barah_sala_encumbrance_clean", False):
            score += 20
            breakdown.append("✅ +20 pts: 12-Year Barah Sala (Encumbrance Certificate) clean & unblemished")
        else:
            breakdown.append("⚠️ 0 pts: 12-Year Barah Sala search pending or has prior encumbrance traces")

        if record.get("dakhil_kharij_mutated", False):
            score += 15
            breakdown.append("✅ +15 pts: Formal Dakhil-Kharij (Mutation) registered in Sub-Registrar ledger")
        else:
            breakdown.append("⚠️ 0 pts: Mutation (Dakhil-Kharij) incomplete or held under family succession")

        if record.get("paved_road_approach", False):
            score += 10
            breakdown.append("✅ +10 pts: Paved Pakka Road / NHAI corridor frontage with legal right of way")
        else:
            breakdown.append("⚠️ 0 pts: Mud trail approach (Chak-marg) without dedicated asphalt frontage")

        # Penalties
        if record.get("has_co_sharer_dispute", False):
            score -= 25
            breakdown.append("🚨 -25 pts PENALTY: Active co-sharer partition dispute or caveat lodged")

        if record.get("in_flood_depression_tal", False):
            score -= 20
            breakdown.append("🌊 -20 pts PENALTY: Monsoon Tal inundation basin (Seasonal backflow risk)")

        if record.get("is_usar_saline_soil", False):
            score -= 15
            breakdown.append("🌾 -15 pts PENALTY: Usar / High-saline soil requiring chemical gypsum reclamation")

        # Clamp between 0 and 100
        score = max(0, min(cls.MAX_SCORE, score))

        # Assign Sovereign/Institutional Grade
        if score >= 90:
            grade = "A+ Sovereign Grade"
            verdict = "🟢 Ready to Register — Bankable, unencumbered & immediate possession"
            is_bankable = True
        elif score >= 75:
            grade = "A Institutional Clear"
            verdict = "🟢 Clean Title — Standard mutation & routine boundary verification"
            is_bankable = True
        elif score >= 60:
            grade = "B Bankable with Minor Covenants"
            verdict = "🟡 Low Risk — Verify physical boundary possession and mutation slip"
            is_bankable = True
        elif score >= 45:
            grade = "C Conditional Clearance"
            verdict = "🟠 Moderate Risk — Requires formal revenue advocate search & NOC from co-sharers"
            is_bankable = False
        else:
            grade = "F High Legal / Physical Hazard"
            verdict = "🔴 Avoid / High Risk — Heavy legal dispute, SARFAESI encumbrance or inundation"
            is_bankable = False

        return {
            "score": score,
            "grade": grade,
            "verdict": verdict,
            "is_bankable": is_bankable,
            "breakdown": breakdown
        }


# =====================================================================
# 4. TIER SOURCES INTELLIGENCE MANAGER
# =====================================================================
class TierSourcesManager:
    """Manages the 5 tiers of land intelligence and portals."""

    @classmethod
    def get_tier(cls, source_name: str) -> str:
        s = str(source_name).lower()
        if any(k in s for k in ["amar ujala", "dainik jagran", "hindustan", "e-paper", "public notice", "सार्वजनिक सूचना"]):
            return "Tier 5: Newspaper Public Notice"
        elif any(k in s for k in ["youtube", "facebook", "twitter", "x.com", "drone", "direct lead", "social"]):
            return "Tier 4: Social / Video Direct Lead"
        elif any(k in s for k in ["ibapi", "sarfaesi", "bank auction", "eauction", "pnb", "sbi", "distress"]):
            return "Tier 2: Bank Distress / SARFAESI Auction"
        elif any(k in s for k in ["sfarmsindia", "farmland india", "99acres", "magicbricks", "housing"]):
            return "Tier 3: Verified Real Estate Portal"
        elif any(k in s for k in ["bhulekh", "igrsup", "bihar bhumi", "mp bhulekh", "rtc", "khasra", "revenue", "bhoomi"]):
            return "Tier 1: Government Land Registry"
        return "Tier 1: Government Land Registry"

    @classmethod
    def get_tier_badge(cls, tier_str: str) -> str:
        t = tier_str.lower()
        if "tier 1" in t:
            return "🏛️ Tier 1: Govt Registry"
        elif "tier 2" in t:
            return "🏦 Tier 2: Bank SARFAESI Auction"
        elif "tier 3" in t:
            return "🌐 Tier 3: Verified Portal"
        elif "tier 4" in t:
            return "🎥 Tier 4: Direct Drone Lead"
        elif "tier 5" in t:
            return "📰 Tier 5: E-Paper Notice"
        return "🏛️ Tier 1: Govt Registry"


# =====================================================================
# 5. AGRI-LAND 200 ORCHESTRATION ENGINE
# =====================================================================
class AgriLand200Engine:
    """High-level facade for aggregating, filtering, and enriching listings."""

    @classmethod
    def process_listing(cls, listing: Dict[str, Any]) -> Dict[str, Any]:
        """Enriches an agricultural parcel listing with unit conversions, geodesic radial distance, and due diligence score."""
        enriched = dict(listing)

        # 1. Geodesic distance from Varanasi Zero-Point
        lat = enriched.get("lat", VARANASI_LAT)
        lng = enriched.get("lng", VARANASI_LNG)
        radial_km = GeoSpatialRadialFilter.calculate_distance_km(lat, lng)
        enriched["radial_distance_from_varanasi_km"] = round(radial_km, 1)
        enriched["is_within_200km_buffer"] = radial_km <= MAX_BUFFER_KM

        # 2. Land Unit Conversions
        raw_size = enriched.get("size_acres", 1.0)
        unit_meta = LandUnitConverter.format_all_units(raw_size)
        enriched["unit_meta"] = unit_meta
        if "size_local_units" not in enriched or not enriched["size_local_units"]:
            enriched["size_local_units"] = f"{raw_size} Acres ({unit_meta['pakka_bigha']} Pakka Bigha / {unit_meta['biswa']} Biswa)"

        # 3. Due Diligence Scoring
        dd_res = DueDiligenceScoringModel.calculate_score(enriched)
        enriched["due_diligence_score"] = dd_res["score"]
        enriched["due_diligence_grade"] = dd_res["grade"]
        enriched["due_diligence_verdict"] = dd_res["verdict"]
        enriched["due_diligence_breakdown"] = dd_res["breakdown"]
        enriched["is_bankable"] = dd_res["is_bankable"]

        # 4. Source Tier
        source_name = enriched.get("source_name", "UP Bhulekh Portal")
        tier_category = TierSourcesManager.get_tier(source_name)
        enriched["sourcing_tier"] = tier_category
        enriched["sourcing_tier_badge"] = TierSourcesManager.get_tier_badge(tier_category)

        return enriched
