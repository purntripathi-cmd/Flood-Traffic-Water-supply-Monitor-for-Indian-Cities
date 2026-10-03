"""
Comprehensive Dataset Generator for Flood-Traffic-Water-supply-Monitor-for-Indian-Cities
Generates:
1. cities.json (6 Metropolitan Corridors)
2. micro_markets.json (48+ micro-markets)
3. builders.json (96+ builders, at least 16 per city)
4. properties.json (36+ purchase & investment properties with growth probability & school ecosystem)
5. rental_properties.json (30+ rental benchmark properties with rental yields & commute scores)
6. gated_plots.json (24+ gated community plots with land appreciation scores & master plans)
7. govt_master_plans.json (Government infrastructure growth catalysts & timelines)
8. avoidance_zones.json (12 chronic avoidance hotspots)
9. user_preferences.json (Default settings & benchmarks)
"""

import json
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "data")
os.makedirs(DATA_DIR, exist_ok=True)

# ==========================================
# 1. CITIES DATASET
# ==========================================
cities = [
    {
        "id": "bengaluru",
        "name": "Bengaluru",
        "state": "Karnataka",
        "region": "South India",
        "center_lat": 12.9716,
        "center_lng": 77.5946,
        "default_zoom": 12,
        "elevation_range_m": "860m - 960m (Average: 920m)",
        "key_landmark": {"name": "Kempegowda Bus Station / Vidhana Soudha", "lat": 12.9778, "lng": 77.5713},
        "default_school_benchmark": {"name": "New Horizon Gurukul (Kadubeesanahalli)", "lat": 12.9348, "lng": 77.7037},
        "municipal_water_authority": {
            "name": "BWSSB (Bangalore Water Supply and Sewerage Board)",
            "piped_coverage_pct": 68,
            "daily_supply_mld": 1450,
            "daily_demand_mld": 2100,
            "deficit_pct": 31,
            "primary_source": "Cauvery River (Stages I-V) & Local Deep Borewells",
            "summer_tanker_dependence_pct": 32
        },
        "drainage_and_flood_authority": {
            "name": "BBMP Storm Water Drain (SWD) Directorate",
            "primary_valleys": ["Vrishabhavathi Valley", "Koramangala & Challaghatta (K&C) Valley", "Hebbal Valley"],
            "total_swd_network_km": 842,
            "remodelled_swd_km": 490,
            "primary_flood_vulnerability": "Valley lake chain overflow, encroached raja-kaluves, and underpass depressions"
        },
        "traffic_monitoring": {
            "authority": "BTP (Bangalore Traffic Police) Traffic Management Centre (TMC)",
            "peak_to_free_flow_delay_index": 2.42,
            "avg_peak_commute_speed_kmh": 14.5,
            "avg_free_flow_speed_kmh": 35.0,
            "monthly_hours_lost_avg": 44
        }
    },
    {
        "id": "mumbai_mmr",
        "name": "Mumbai & MMR",
        "state": "Maharashtra",
        "region": "West India",
        "center_lat": 19.0760,
        "center_lng": 72.8777,
        "default_zoom": 12,
        "elevation_range_m": "2m - 55m (Average: 14m)",
        "key_landmark": {"name": "Chhatrapati Shivaji Maharaj Terminus (CSMT)", "lat": 18.9401, "lng": 72.8354},
        "default_school_benchmark": {"name": "Dhirubhai Ambani International School (BKC)", "lat": 19.0660, "lng": 72.8680},
        "municipal_water_authority": {
            "name": "BMC (Brihanmumbai Municipal Corporation) Hydraulic Dept",
            "piped_coverage_pct": 92,
            "daily_supply_mld": 3950,
            "daily_demand_mld": 4400,
            "deficit_pct": 10,
            "primary_source": "Bhatsa, Upper Vaitarna, Middle Vaitarna, Tansa, Modak Sagar, Tulsi & Vihar Lakes",
            "summer_tanker_dependence_pct": 8
        },
        "drainage_and_flood_authority": {
            "name": "BMC Storm Water Drains (BRIMSTOWAD) & Disaster Management Cell",
            "primary_valleys": ["Mithi River Basin", "Poisar River Basin", "Oshiwara River Basin", "Dahisar River Basin"],
            "total_swd_network_km": 2000,
            "remodelled_swd_km": 1450,
            "primary_flood_vulnerability": "High tide backflow (>4.5m) coinciding with monsoon downpours >50mm/hr and railway subways"
        },
        "traffic_monitoring": {
            "authority": "Mumbai Traffic Police (MTP) Joint CP Traffic Control",
            "peak_to_free_flow_delay_index": 2.35,
            "avg_peak_commute_speed_kmh": 16.0,
            "avg_free_flow_speed_kmh": 37.6,
            "monthly_hours_lost_avg": 42
        }
    },
    {
        "id": "chennai",
        "name": "Chennai",
        "state": "Tamil Nadu",
        "region": "South India",
        "center_lat": 13.0827,
        "center_lng": 80.2707,
        "default_zoom": 12,
        "elevation_range_m": "1m - 32m (Average: 6.7m)",
        "key_landmark": {"name": "Chennai Central Railway Station", "lat": 13.0823, "lng": 80.2754},
        "default_school_benchmark": {"name": "Chettinad Vidyashram (R.A. Puram)", "lat": 13.0245, "lng": 80.2625},
        "municipal_water_authority": {
            "name": "CMWSSB (Chennai Metropolitan Water Supply and Sewerage Board)",
            "piped_coverage_pct": 74,
            "daily_supply_mld": 1000,
            "daily_demand_mld": 1250,
            "deficit_pct": 20,
            "primary_source": "Poondi, Cholavaram, Red Hills, Chembarambakkam, Nemmeli & Minjur Desalination Plants",
            "summer_tanker_dependence_pct": 26
        },
        "drainage_and_flood_authority": {
            "name": "Greater Chennai Corporation (GCC) Storm Water Drain Dept",
            "primary_valleys": ["Adyar River Basin", "Cooum River Basin", "Kosasthalaiyar Basin", "Kovalam / Buckingham Canal Basin"],
            "total_swd_network_km": 1894,
            "remodelled_swd_km": 1280,
            "primary_flood_vulnerability": "Flat coastal gradient (<0.1%), Pallikaranai marshland shrinkage, and tidal surge"
        },
        "traffic_monitoring": {
            "authority": "Greater Chennai Traffic Police (GCTP)",
            "peak_to_free_flow_delay_index": 2.10,
            "avg_peak_commute_speed_kmh": 17.5,
            "avg_free_flow_speed_kmh": 36.8,
            "monthly_hours_lost_avg": 36
        }
    },
    {
        "id": "delhi_ncr",
        "name": "Delhi-NCR",
        "state": "Delhi / Haryana / UP",
        "region": "North India",
        "center_lat": 28.6139,
        "center_lng": 77.2090,
        "default_zoom": 11,
        "elevation_range_m": "195m - 245m (Average: 216m)",
        "key_landmark": {"name": "Connaught Place / India Gate", "lat": 28.6304, "lng": 77.2177},
        "default_school_benchmark": {"name": "The Heritage School (Sector 62 Gurugram)", "lat": 28.4150, "lng": 77.0820},
        "municipal_water_authority": {
            "name": "DJB (Delhi Jal Board) & GMDA (Gurugram Metropolitan Development Authority)",
            "piped_coverage_pct": 82,
            "daily_supply_mld": 4500,
            "daily_demand_mld": 5400,
            "deficit_pct": 17,
            "primary_source": "Yamuna River, Ganga Canal via Sonia Vihar, Bhakra Storage & Western Yamuna Canal",
            "summer_tanker_dependence_pct": 18
        },
        "drainage_and_flood_authority": {
            "name": "Delhi Irrigation & Flood Control Dept (IFCD) & PWD",
            "primary_valleys": ["Najafgarh Drain Basin", "Shahdara Drain Basin", "Barapullah Basin", "Badshahpur Drain (Gurugram)"],
            "total_swd_network_km": 3740,
            "remodelled_swd_km": 2100,
            "primary_flood_vulnerability": "Yamuna river floodplain backflow when discharge exceeds 3 lakh cusecs at Hathnikund Barrage"
        },
        "traffic_monitoring": {
            "authority": "Delhi Traffic Police & Gurugram Traffic Police",
            "peak_to_free_flow_delay_index": 2.18,
            "avg_peak_commute_speed_kmh": 18.0,
            "avg_free_flow_speed_kmh": 39.2,
            "monthly_hours_lost_avg": 38
        }
    },
    {
        "id": "hyderabad",
        "name": "Hyderabad",
        "state": "Telangana",
        "region": "South-Central India",
        "center_lat": 17.3850,
        "center_lng": 78.4867,
        "default_zoom": 12,
        "elevation_range_m": "485m - 610m (Average: 542m)",
        "key_landmark": {"name": "Charminar / Secretariat", "lat": 17.3616, "lng": 78.4747},
        "default_school_benchmark": {"name": "Oakridge International School (Gachibowli)", "lat": 17.4250, "lng": 78.3380},
        "municipal_water_authority": {
            "name": "HMWSSB (Hyderabad Metropolitan Water Supply and Sewerage Board)",
            "piped_coverage_pct": 85,
            "daily_supply_mld": 2400,
            "daily_demand_mld": 2800,
            "deficit_pct": 14,
            "primary_source": "Godavari & Krishna Water Supply Schemes, Osmansagar & Himayatsagar",
            "summer_tanker_dependence_pct": 15
        },
        "drainage_and_flood_authority": {
            "name": "GHMC Strategic Nala Development Programme (SNDP)",
            "primary_valleys": ["Musi River Basin", "Hussain Sagar Lake Basin", "Mir Alam Basin", "Durgam Cheruvu Basin"],
            "total_swd_network_km": 1500,
            "remodelled_swd_km": 980,
            "primary_flood_vulnerability": "Flash downpours on rocky granite terrain with rapid runoff into narrow encroached nalas"
        },
        "traffic_monitoring": {
            "authority": "Hyderabad Traffic Police & Cyberabad Traffic Police",
            "peak_to_free_flow_delay_index": 1.95,
            "avg_peak_commute_speed_kmh": 19.5,
            "avg_free_flow_speed_kmh": 38.0,
            "monthly_hours_lost_avg": 31
        }
    },
    {
        "id": "varanasi_100km",
        "name": "Varanasi & Eastern UP 100km Corridor",
        "state": "Uttar Pradesh",
        "region": "North-Central India",
        "center_lat": 25.3176,
        "center_lng": 82.9739,
        "default_zoom": 10,
        "elevation_range_m": "72m - 105m (Average: 82m)",
        "key_landmark": {"name": "Varanasi Junction (Cantt) / Kashi Vishwanath Temple", "lat": 25.3268, "lng": 82.9866},
        "default_school_benchmark": {"name": "Sunbeam School (Varuna / Cantt)", "lat": 25.3450, "lng": 82.9820},
        "municipal_water_authority": {
            "name": "UP Jal Sansthan & Smart City Kashi Water Utility",
            "piped_coverage_pct": 65,
            "daily_supply_mld": 320,
            "daily_demand_mld": 440,
            "deficit_pct": 27,
            "primary_source": "Ganga River Intake (Bhadaini Plant) + Deep Alluvial Tubewells",
            "summer_tanker_dependence_pct": 35
        },
        "drainage_and_flood_authority": {
            "name": "UP Irrigation & Water Resources Dept & Namami Gange Mission",
            "primary_valleys": ["Ganga River Mainstem", "Varuna River Basin", "Assi River Basin", "Gomti River Basin (Jaunpur)"],
            "total_swd_network_km": 540,
            "remodelled_swd_km": 310,
            "primary_flood_vulnerability": "Ganga high flood level (>73.90m) backflow pushing up the Varuna and Assi rivers"
        },
        "traffic_monitoring": {
            "authority": "Varanasi Commissionarate Traffic Police & Smart City Integrated Command Centre (ICCC)",
            "peak_to_free_flow_delay_index": 2.25,
            "avg_peak_commute_speed_kmh": 14.0,
            "avg_free_flow_speed_kmh": 31.5,
            "monthly_hours_lost_avg": 37
        }
    }
]

# ==========================================
# 2. BUILDERS DATASET (96+ Builders, >=16 Per City)
# ==========================================
builders = [
    # --- BENGALURU (16 Builders) ---
    {
        "id": "bld_sobha_blr", "name": "Sobha Limited", "city_id": "bengaluru", "tier": "Tier 1 Premier National",
        "headquarters": "Bengaluru, Karnataka", "established_year": 1995, "rera_compliance_score": 98,
        "on_time_delivery_pct": 97, "construction_quality_rating": 9.6, "litigation_index": "Minimal / Negligible",
        "total_delivered_sqft_mn": 120.5, "flagship_projects": {"bengaluru": "Sobha Neopolis, Sobha Iris, Sobha Dream Acres"},
        "active_states_and_cities": ["Karnataka", "Bengaluru", "NCR", "Tamil Nadu", "Kerala"],
        "strengths": "In-house precast manufacturing, German architectural precision, Zero backward subcontracting.",
        "cautions": "Higher price premium (₹13,500 - ₹16,000/sqft), strict alteration policies.",
        "rera_portal_url": "https://rera.karnataka.gov.in/"
    },
    {
        "id": "bld_prestige_blr", "name": "Prestige Group", "city_id": "bengaluru", "tier": "Tier 1 Premier National",
        "headquarters": "Bengaluru, Karnataka", "established_year": 1986, "rera_compliance_score": 97,
        "on_time_delivery_pct": 95, "construction_quality_rating": 9.4, "litigation_index": "Low",
        "total_delivered_sqft_mn": 150.0, "flagship_projects": {"bengaluru": "Prestige Falcon City, Prestige Great Acres, Prestige Tech Park"},
        "active_states_and_cities": ["Karnataka", "Bengaluru", "Maharashtra", "Tamil Nadu", "Telangana", "Kerala"],
        "strengths": "Integrated township scale, corporate commercial hubs, strong capital appreciation history.",
        "cautions": "High unit density in large townships (>2,500 units), standard interior finishes.",
        "rera_portal_url": "https://rera.karnataka.gov.in/"
    },
    {
        "id": "bld_brigade_blr", "name": "Brigade Group", "city_id": "bengaluru", "tier": "Tier 1 Premier National",
        "headquarters": "Bengaluru, Karnataka", "established_year": 1986, "rera_compliance_score": 96,
        "on_time_delivery_pct": 94, "construction_quality_rating": 9.2, "litigation_index": "Low",
        "total_delivered_sqft_mn": 86.0, "flagship_projects": {"bengaluru": "Brigade Cornerstone Utopia, Brigade Gateway, Brigade Oasis"},
        "active_states_and_cities": ["Karnataka", "Bengaluru", "Tamil Nadu", "Telangana", "Kerala"],
        "strengths": "Pioneers of integrated smart townships with retail, hospital, and school ecosystems on campus.",
        "cautions": "Peripheral locations require reliance on emerging arterial transit corridors.",
        "rera_portal_url": "https://rera.karnataka.gov.in/"
    },
    {
        "id": "bld_godrej_blr", "name": "Godrej Properties", "city_id": "bengaluru", "tier": "Tier 1 Premier National",
        "headquarters": "Mumbai, Maharashtra", "established_year": 1990, "rera_compliance_score": 96,
        "on_time_delivery_pct": 92, "construction_quality_rating": 9.1, "litigation_index": "Low",
        "total_delivered_sqft_mn": 95.0, "flagship_projects": {"bengaluru": "Godrej Splendour, Godrej Woodland, Godrej Aqua"},
        "active_states_and_cities": ["Karnataka", "Bengaluru", "Maharashtra", "NCR", "Telangana"],
        "strengths": "Trusted 127-year Godrej corporate governance, green rating certifications, solid resale liquidity.",
        "cautions": "Carpet area efficiency ratio typically around 68-70%.",
        "rera_portal_url": "https://rera.karnataka.gov.in/"
    },
    {
        "id": "bld_puravankara_blr", "name": "Puravankara Limited", "city_id": "bengaluru", "tier": "Tier 1 Premier National",
        "headquarters": "Bengaluru, Karnataka", "established_year": 1975, "rera_compliance_score": 94,
        "on_time_delivery_pct": 90, "construction_quality_rating": 9.0, "litigation_index": "Low to Moderate",
        "total_delivered_sqft_mn": 48.0, "flagship_projects": {"bengaluru": "Purva Atmosphere, Purva Orient Grand, Provident Welworth"},
        "active_states_and_cities": ["Karnataka", "Bengaluru", "Tamil Nadu", "Maharashtra", "Kerala"],
        "strengths": "Theme-based luxury developments, BluNex smart home integration, robust structural durability.",
        "cautions": "Slight delays in earlier pre-RERA phases (now fully on schedule).",
        "rera_portal_url": "https://rera.karnataka.gov.in/"
    },
    {
        "id": "bld_totalenv_blr", "name": "Total Environment Building Systems", "city_id": "bengaluru", "tier": "Tier 1 Ultra-Luxury Boutique",
        "headquarters": "Bengaluru, Karnataka", "established_year": 1996, "rera_compliance_score": 95,
        "on_time_delivery_pct": 88, "construction_quality_rating": 9.8, "litigation_index": "Minimal",
        "total_delivered_sqft_mn": 14.0, "flagship_projects": {"bengaluru": "Windmills of Your Mind, In That Quiet Earth, Learning to Fly"},
        "active_states_and_cities": ["Karnataka", "Bengaluru", "Maharashtra", "Telangana"],
        "strengths": "Earth-sheltered roofs, handcrafted natural materials, cantilevered private garden terraces.",
        "cautions": "High price ticket (>₹3.5 Cr to ₹12 Cr) and longer architectural construction cycles.",
        "rera_portal_url": "https://rera.karnataka.gov.in/"
    },
    {
        "id": "bld_assetz_blr", "name": "Assetz Property Group", "city_id": "bengaluru", "tier": "Tier 1 Regional Champion",
        "headquarters": "Singapore / Bengaluru", "established_year": 2006, "rera_compliance_score": 93,
        "on_time_delivery_pct": 92, "construction_quality_rating": 9.1, "litigation_index": "Low",
        "total_delivered_sqft_mn": 22.0, "flagship_projects": {"bengaluru": "Assetz Canvas & Cove, Assetz Marq, Assetz 63 Degree East"},
        "active_states_and_cities": ["Karnataka", "Bengaluru"],
        "strengths": "Carbon-healing design philosophy, 75-80% open spaces, high green buffer zones.",
        "cautions": "Approach roads in emerging micro-markets require local civic widening.",
        "rera_portal_url": "https://rera.karnataka.gov.in/"
    },
    {
        "id": "bld_sattva_blr", "name": "Salarpuria Sattva Group", "city_id": "bengaluru", "tier": "Tier 1 Premier National",
        "headquarters": "Bengaluru, Karnataka", "established_year": 1993, "rera_compliance_score": 94,
        "on_time_delivery_pct": 93, "construction_quality_rating": 9.0, "litigation_index": "Low",
        "total_delivered_sqft_mn": 65.0, "flagship_projects": {"bengaluru": "Sattva Knowledge City, Sattva Signet, Sattva Green Groves"},
        "active_states_and_cities": ["Karnataka", "Bengaluru", "Telangana", "West Bengal"],
        "strengths": "Strong debt-free commercial cash flows backing residential handovers, prime land banks.",
        "cautions": "Higher density floor plates in mid-segment apartments.",
        "rera_portal_url": "https://rera.karnataka.gov.in/"
    },
    {
        "id": "bld_embassy_blr", "name": "Embassy Group", "city_id": "bengaluru", "tier": "Tier 1 Commercial & Ultra-Luxury",
        "headquarters": "Bengaluru, Karnataka", "established_year": 1993, "rera_compliance_score": 95,
        "on_time_delivery_pct": 91, "construction_quality_rating": 9.5, "litigation_index": "Low",
        "total_delivered_sqft_mn": 62.0, "flagship_projects": {"bengaluru": "Embassy TechVillage, Embassy Lake Terraces, Embassy Springs"},
        "active_states_and_cities": ["Karnataka", "Bengaluru", "Maharashtra", "NCR"],
        "strengths": "India's largest office REIT sponsor, signature ultra-luxury residential properties.",
        "cautions": "High entry price point and maintenance outlays.",
        "rera_portal_url": "https://rera.karnataka.gov.in/"
    },
    {
        "id": "bld_rohan_blr", "name": "Rohan Builders", "city_id": "bengaluru", "tier": "Tier 1 Engineering Specialist",
        "headquarters": "Pune / Bengaluru", "established_year": 1993, "rera_compliance_score": 94,
        "on_time_delivery_pct": 93, "construction_quality_rating": 9.2, "litigation_index": "Minimal",
        "total_delivered_sqft_mn": 18.0, "flagship_projects": {"bengaluru": "Rohan Iksha, Rohan Upavan, Rohan Avriti"},
        "active_states_and_cities": ["Karnataka", "Bengaluru", "Maharashtra"],
        "strengths": "Plus Home concept: ventilation, privacy, light and smart space design.",
        "cautions": "Selective marketing presence compared to large national syndicates.",
        "rera_portal_url": "https://rera.karnataka.gov.in/"
    },
    {
        "id": "bld_provident_blr", "name": "Provident Housing", "city_id": "bengaluru", "tier": "Tier 2 Established Value-Homes",
        "headquarters": "Bengaluru, Karnataka", "established_year": 2008, "rera_compliance_score": 92,
        "on_time_delivery_pct": 89, "construction_quality_rating": 8.7, "litigation_index": "Low",
        "total_delivered_sqft_mn": 25.0, "flagship_projects": {"bengaluru": "Provident Equinox, Provident Sunworth, Provident Capella"},
        "active_states_and_cities": ["Karnataka", "Bengaluru", "Tamil Nadu", "Goa"],
        "strengths": "Puravankara subsidiary delivering quality homes with precast tech at affordable tickets.",
        "cautions": "Located along peripheral highways with commute times to central business districts.",
        "rera_portal_url": "https://rera.karnataka.gov.in/"
    },
    {
        "id": "bld_shriram_blr", "name": "Shriram Properties", "city_id": "bengaluru", "tier": "Tier 2 Established Public Listed",
        "headquarters": "Bengaluru, Karnataka", "established_year": 1995, "rera_compliance_score": 91,
        "on_time_delivery_pct": 88, "construction_quality_rating": 8.6, "litigation_index": "Low to Moderate",
        "total_delivered_sqft_mn": 22.0, "flagship_projects": {"bengaluru": "Shriram Chirping Woods, Shriram Blue, Shriram Grand City"},
        "active_states_and_cities": ["Karnataka", "Bengaluru", "Tamil Nadu", "West Bengal"],
        "strengths": "Publicly listed transparency, strong mid-market presence, active RERA governance.",
        "cautions": "Moderate amenities scale compared to Tier 1 peers.",
        "rera_portal_url": "https://rera.karnataka.gov.in/"
    },
    {
        "id": "bld_dsmax_blr", "name": "DS-MAX Properties", "city_id": "bengaluru", "tier": "Tier 2 Established Value",
        "headquarters": "Bengaluru, Karnataka", "established_year": 2007, "rera_compliance_score": 88,
        "on_time_delivery_pct": 86, "construction_quality_rating": 8.2, "litigation_index": "Moderate",
        "total_delivered_sqft_mn": 15.0, "flagship_projects": {"bengaluru": "DS-MAX Skycity, DS-MAX Sovereign, DS-MAX Stavam"},
        "active_states_and_cities": ["Karnataka", "Bengaluru", "Tamil Nadu"],
        "strengths": "Lowest entry ticket pricing in Bengaluru, wide geographical spread.",
        "cautions": "Standard exterior elevation, lower open space ratio (~50-60%).",
        "rera_portal_url": "https://rera.karnataka.gov.in/"
    },
    {
        "id": "bld_concorde_blr", "name": "Concorde Group", "city_id": "bengaluru", "tier": "Tier 2 Established Regional",
        "headquarters": "Bengaluru, Karnataka", "established_year": 1998, "rera_compliance_score": 90,
        "on_time_delivery_pct": 89, "construction_quality_rating": 8.6, "litigation_index": "Low",
        "total_delivered_sqft_mn": 24.0, "flagship_projects": {"bengaluru": "Concorde Cuppertino, Concorde Spring Meadows, Concorde Auriga"},
        "active_states_and_cities": ["Karnataka", "Bengaluru"],
        "strengths": "Pioneers in Electronic City and Kanakapura Road residential enclaves.",
        "cautions": "Resale price appreciation lags Tier 1 brands by 8-12%.",
        "rera_portal_url": "https://rera.karnataka.gov.in/"
    },
    {
        "id": "bld_vaishnavi_blr", "name": "Vaishnavi Group", "city_id": "bengaluru", "tier": "Tier 2 Established Boutique",
        "headquarters": "Bengaluru, Karnataka", "established_year": 1998, "rera_compliance_score": 92,
        "on_time_delivery_pct": 91, "construction_quality_rating": 8.9, "litigation_index": "Minimal",
        "total_delivered_sqft_mn": 12.0, "flagship_projects": {"bengaluru": "Vaishnavi Serene, Vaishnavi Oasis, Vaishnavi Life"},
        "active_states_and_cities": ["Karnataka", "Bengaluru"],
        "strengths": "Off-site precast modular construction, high customer satisfaction index.",
        "cautions": "Smaller project portfolio size.",
        "rera_portal_url": "https://rera.karnataka.gov.in/"
    },
    {
        "id": "bld_century_blr", "name": "Century Real Estate", "city_id": "bengaluru", "tier": "Tier 2 Established Land Bank Leader",
        "headquarters": "Bengaluru, Karnataka", "established_year": 1973, "rera_compliance_score": 91,
        "on_time_delivery_pct": 89, "construction_quality_rating": 8.8, "litigation_index": "Low",
        "total_delivered_sqft_mn": 20.0, "flagship_projects": {"bengaluru": "Century Ethos, Century Wintersun, Century Horizon"},
        "active_states_and_cities": ["Karnataka", "Bengaluru"],
        "strengths": "Largest private land bank in North Bengaluru near Kempegowda International Airport.",
        "cautions": "Select projects have longer phased delivery timelines.",
        "rera_portal_url": "https://rera.karnataka.gov.in/"
    },

    # --- MUMBAI & MMR (16 Builders) ---
    {
        "id": "bld_oberoi_mum", "name": "Oberoi Realty", "city_id": "mumbai_mmr", "tier": "Tier 1 Premier National",
        "headquarters": "Mumbai, Maharashtra", "established_year": 1980, "rera_compliance_score": 99,
        "on_time_delivery_pct": 98, "construction_quality_rating": 9.7, "litigation_index": "Minimal / Negligible",
        "total_delivered_sqft_mn": 35.0, "flagship_projects": {"mumbai_mmr": "Oberoi Sky City (Borivali), Three Sixty West (Worli), Oberoi Garden City (Goregaon)"},
        "active_states_and_cities": ["Maharashtra", "Mumbai & MMR", "NCR"],
        "strengths": "Virtually zero debt balance sheet, superlative finish quality, integrated commercial and mall ecosystem.",
        "cautions": "High price premium; very limited bargaining power for retail buyers.",
        "rera_portal_url": "https://maharera.mahaonline.gov.in/"
    },
    {
        "id": "bld_lodha_mum", "name": "Lodha Group (Macrotech Developers)", "city_id": "mumbai_mmr", "tier": "Tier 1 Premier National",
        "headquarters": "Mumbai, Maharashtra", "established_year": 1980, "rera_compliance_score": 97,
        "on_time_delivery_pct": 94, "construction_quality_rating": 9.3, "litigation_index": "Low",
        "total_delivered_sqft_mn": 105.0, "flagship_projects": {"mumbai_mmr": "Lodha Park (Worli), Lodha World Towers, Palava Smart City"},
        "active_states_and_cities": ["Maharashtra", "Mumbai & MMR", "Pune", "Bengaluru"],
        "strengths": "India's largest residential developer by sales volume, grand clubhouse scale, high sales velocity.",
        "cautions": "Earlier high debt leverage has significantly reduced; large townships have dense master plans.",
        "rera_portal_url": "https://maharera.mahaonline.gov.in/"
    },
    {
        "id": "bld_hiranandani_mum", "name": "Hiranandani Group", "city_id": "mumbai_mmr", "tier": "Tier 1 Premier National",
        "headquarters": "Mumbai, Maharashtra", "established_year": 1978, "rera_compliance_score": 98,
        "on_time_delivery_pct": 96, "construction_quality_rating": 9.6, "litigation_index": "Minimal",
        "total_delivered_sqft_mn": 52.0, "flagship_projects": {"mumbai_mmr": "Hiranandani Gardens Powai, Hiranandani Estate Thane, Fortune City Panvel"},
        "active_states_and_cities": ["Maharashtra", "Mumbai & MMR", "Chennai"],
        "strengths": "Iconic neoclassical architecture, self-sustaining master townships with top schools and hospitals on site.",
        "cautions": "High maintenance fee structure for township upkeep.",
        "rera_portal_url": "https://maharera.mahaonline.gov.in/"
    },
    {
        "id": "bld_godrej_mum", "name": "Godrej Properties", "city_id": "mumbai_mmr", "tier": "Tier 1 Premier National",
        "headquarters": "Mumbai, Maharashtra", "established_year": 1990, "rera_compliance_score": 97,
        "on_time_delivery_pct": 93, "construction_quality_rating": 9.2, "litigation_index": "Low",
        "total_delivered_sqft_mn": 95.0, "flagship_projects": {"mumbai_mmr": "Godrej The Trees (Vikhroli), Godrej Platinum, Godrej Prime"},
        "active_states_and_cities": ["Maharashtra", "Mumbai & MMR", "NCR", "Bengaluru", "Pune"],
        "strengths": "Trusted corporate pedigree, IGBC Platinum sustainable projects, excellent liquidity.",
        "cautions": "High investor component in pre-launch phases.",
        "rera_portal_url": "https://maharera.mahaonline.gov.in/"
    },
    {
        "id": "bld_tata_mum", "name": "Tata Housing Development Company", "city_id": "mumbai_mmr", "tier": "Tier 1 Premier National",
        "headquarters": "Mumbai, Maharashtra", "established_year": 1984, "rera_compliance_score": 96,
        "on_time_delivery_pct": 92, "construction_quality_rating": 9.3, "litigation_index": "Minimal",
        "total_delivered_sqft_mn": 35.0, "flagship_projects": {"mumbai_mmr": "Tata Serein (Thane), Tata Amantra (Kalyan), Tata Aveza (Mulund)"},
        "active_states_and_cities": ["Maharashtra", "Mumbai & MMR", "NCR", "Bengaluru", "Kolkata"],
        "strengths": "Tata Trust ethics, transparent buyer documentation, biophilic community layouts.",
        "cautions": "Slower decision turnaround during construction customization.",
        "rera_portal_url": "https://maharera.mahaonline.gov.in/"
    },
    {
        "id": "bld_lt_mum", "name": "L&T Realty", "city_id": "mumbai_mmr", "tier": "Tier 1 Premier National",
        "headquarters": "Mumbai, Maharashtra", "established_year": 2011, "rera_compliance_score": 98,
        "on_time_delivery_pct": 96, "construction_quality_rating": 9.6, "litigation_index": "Minimal",
        "total_delivered_sqft_mn": 38.0, "flagship_projects": {"mumbai_mmr": "L&T Seawoods Residences, L&T Emerald Isle (Powai), L&T Crescent Bay (Parel)"},
        "active_states_and_cities": ["Maharashtra", "Mumbai & MMR", "Bengaluru", "Chennai"],
        "strengths": "Larsen & Toubro engineering excellence, transit-oriented developments (TOD), punctual handovers.",
        "cautions": "Fixed pricing models with zero discretionary waivers.",
        "rera_portal_url": "https://maharera.mahaonline.gov.in/"
    },
    {
        "id": "bld_kalpataru_mum", "name": "Kalpataru Limited", "city_id": "mumbai_mmr", "tier": "Tier 1 Regional Champion",
        "headquarters": "Mumbai, Maharashtra", "established_year": 1969, "rera_compliance_score": 95,
        "on_time_delivery_pct": 92, "construction_quality_rating": 9.2, "litigation_index": "Low",
        "total_delivered_sqft_mn": 60.0, "flagship_projects": {"mumbai_mmr": "Kalpataru Sparkle (Bandra East), Kalpataru Paramount (Thane), Kalpataru Avana"},
        "active_states_and_cities": ["Maharashtra", "Mumbai & MMR", "Pune", "Noida", "Hyderabad"],
        "strengths": "Over 55 years of Mumbai redevelopment and high-rise construction expertise.",
        "cautions": "Redevelopment phases occasionally encounter BMC local civic delay.",
        "rera_portal_url": "https://maharera.mahaonline.gov.in/"
    },
    {
        "id": "bld_rustomjee_mum", "name": "Rustomjee (Keystone Realtors)", "city_id": "mumbai_mmr", "tier": "Tier 1 Regional Champion",
        "headquarters": "Mumbai, Maharashtra", "established_year": 1996, "rera_compliance_score": 95,
        "on_time_delivery_pct": 93, "construction_quality_rating": 9.2, "litigation_index": "Low",
        "total_delivered_sqft_mn": 32.0, "flagship_projects": {"mumbai_mmr": "Rustomjee Seasons (BKC), Rustomjee Elements (Juhu), Rustomjee Urbania (Thane)"},
        "active_states_and_cities": ["Maharashtra", "Mumbai & MMR"],
        "strengths": "Child-centric and family-oriented amenities, high-quality community management.",
        "cautions": "Prime locations entail high maintenance dues.",
        "rera_portal_url": "https://maharera.mahaonline.gov.in/"
    },
    {
        "id": "bld_wadhwa_mum", "name": "The Wadhwa Group", "city_id": "mumbai_mmr", "tier": "Tier 1 Regional Champion",
        "headquarters": "Mumbai, Maharashtra", "established_year": 1969, "rera_compliance_score": 94,
        "on_time_delivery_pct": 91, "construction_quality_rating": 9.1, "litigation_index": "Low",
        "total_delivered_sqft_mn": 28.0, "flagship_projects": {"mumbai_mmr": "The Address (Ghatkopar), Wadhwa Pristine (Matunga), Wadhwa Courtyard (Thane)"},
        "active_states_and_cities": ["Maharashtra", "Mumbai & MMR"],
        "strengths": "Ventilit design philosophy: maximum light, height, and air circulation in Mumbai apartments.",
        "cautions": "Moderate density in suburban high-rises.",
        "rera_portal_url": "https://maharera.mahaonline.gov.in/"
    },
    {
        "id": "bld_runwal_mum", "name": "Runwal Group", "city_id": "mumbai_mmr", "tier": "Tier 1 Regional Champion",
        "headquarters": "Mumbai, Maharashtra", "established_year": 1978, "rera_compliance_score": 93,
        "on_time_delivery_pct": 90, "construction_quality_rating": 9.0, "litigation_index": "Low to Moderate",
        "total_delivered_sqft_mn": 35.0, "flagship_projects": {"mumbai_mmr": "Runwal Bliss (Kanjurmarg), Runwal Forests, Runwal Greens (Mulund)"},
        "active_states_and_cities": ["Maharashtra", "Mumbai & MMR"],
        "strengths": "Integrated retail mall assets (R-City Mall), prominent eastern suburbs market dominance.",
        "cautions": "Kanjurmarg-Mulund corridor experiences peak LBS Marg traffic congestion.",
        "rera_portal_url": "https://maharera.mahaonline.gov.in/"
    },
    {
        "id": "bld_piramal_mum", "name": "Piramal Realty", "city_id": "mumbai_mmr", "tier": "Tier 1 Corporate Luxury",
        "headquarters": "Mumbai, Maharashtra", "established_year": 2012, "rera_compliance_score": 96,
        "on_time_delivery_pct": 94, "construction_quality_rating": 9.5, "litigation_index": "Minimal",
        "total_delivered_sqft_mn": 17.0, "flagship_projects": {"mumbai_mmr": "Piramal Mahalaxmi, Piramal Aranya (Byculla), Piramal Vaikunth (Thane)"},
        "active_states_and_cities": ["Maharashtra", "Mumbai & MMR"],
        "strengths": "Global design partners (HOK, Make Architects), expansive natural green reserves.",
        "cautions": "High entry ticket size across central Mumbai projects.",
        "rera_portal_url": "https://maharera.mahaonline.gov.in/"
    },
    {
        "id": "bld_shapoorji_mum", "name": "Shapoorji Pallonji Real Estate", "city_id": "mumbai_mmr", "tier": "Tier 1 Premier National",
        "headquarters": "Mumbai, Maharashtra", "established_year": 1865, "rera_compliance_score": 96,
        "on_time_delivery_pct": 92, "construction_quality_rating": 9.5, "litigation_index": "Low",
        "total_delivered_sqft_mn": 70.0, "flagship_projects": {"mumbai_mmr": "The Imperial (Tardeo), Shapoorji Pallonji Vicinia (Powai), Joyville Virar"},
        "active_states_and_cities": ["Maharashtra", "Mumbai & MMR", "NCR", "Kolkata", "Bengaluru", "Pune"],
        "strengths": "159-year construction legacy (built RBI, Bombay High Court, Taj Hotel), unmatched structural durability.",
        "cautions": "Corporate restructuring in parent group has stabilized; execution pace now brisk.",
        "rera_portal_url": "https://maharera.mahaonline.gov.in/"
    },
    {
        "id": "bld_kraheja_mum", "name": "K Raheja Corp", "city_id": "mumbai_mmr", "tier": "Tier 1 Commercial & Luxury",
        "headquarters": "Mumbai, Maharashtra", "established_year": 1956, "rera_compliance_score": 97,
        "on_time_delivery_pct": 95, "construction_quality_rating": 9.5, "litigation_index": "Minimal",
        "total_delivered_sqft_mn": 45.0, "flagship_projects": {"mumbai_mmr": "Vivarea (Mahalaxmi), Raheja Artesia (Worli), Mindspace Airoli"},
        "active_states_and_cities": ["Maharashtra", "Mumbai & MMR", "Hyderabad", "Bengaluru", "Pune"],
        "strengths": "Mindspace REIT sponsor, ultra-luxury residential towers with highest resale retention in South Mumbai.",
        "cautions": "Strictly premium ticket size (>₹6 Cr to ₹35 Cr).",
        "rera_portal_url": "https://maharera.mahaonline.gov.in/"
    },
    {
        "id": "bld_dosti_mum", "name": "Dosti Realty", "city_id": "mumbai_mmr", "tier": "Tier 2 Established Regional",
        "headquarters": "Mumbai, Maharashtra", "established_year": 1980, "rera_compliance_score": 92,
        "on_time_delivery_pct": 90, "construction_quality_rating": 8.9, "litigation_index": "Low",
        "total_delivered_sqft_mn": 15.0, "flagship_projects": {"mumbai_mmr": "Dosti Eastern Bay (Wadala), Dosti Planet North (Shilphata), Dosti West County"},
        "active_states_and_cities": ["Maharashtra", "Mumbai & MMR", "Thane"],
        "strengths": "Reliable delivery in Wadala and Thane micro-markets, value-engineered space utilization.",
        "cautions": "High unit count per floor in select towers.",
        "rera_portal_url": "https://maharera.mahaonline.gov.in/"
    },
    {
        "id": "bld_marathon_mum", "name": "Marathon Group", "city_id": "mumbai_mmr", "tier": "Tier 2 Established Engineering",
        "headquarters": "Mumbai, Maharashtra", "established_year": 1969, "rera_compliance_score": 92,
        "on_time_delivery_pct": 91, "construction_quality_rating": 9.0, "litigation_index": "Low",
        "total_delivered_sqft_mn": 18.0, "flagship_projects": {"mumbai_mmr": "Marathon Monte South (Byculla), Marathon Futurex (Lower Parel), Marathon Nexzone"},
        "active_states_and_cities": ["Maharashtra", "Mumbai & MMR"],
        "strengths": "Pioneers of tall tower engineering in Mumbai, Panvel airport corridor early mover.",
        "cautions": "Lengthy construction cycles in supertall Byculla structures.",
        "rera_portal_url": "https://maharera.mahaonline.gov.in/"
    },
    {
        "id": "bld_sunteck_mum", "name": "Sunteck Realty", "city_id": "mumbai_mmr", "tier": "Tier 1 Regional Champion",
        "headquarters": "Mumbai, Maharashtra", "established_year": 2000, "rera_compliance_score": 94,
        "on_time_delivery_pct": 92, "construction_quality_rating": 9.3, "litigation_index": "Low",
        "total_delivered_sqft_mn": 28.0, "flagship_projects": {"mumbai_mmr": "Signature Island (BKC), Sunteck City (Oshiwara), Sunteck Beach Residences"},
        "active_states_and_cities": ["Maharashtra", "Mumbai & MMR"],
        "strengths": "Dominant luxury presence in BKC housing India's top corporate leaders, debt-disciplined balance sheet.",
        "cautions": "Oshiwara projects depend on SV Road relief flyovers.",
        "rera_portal_url": "https://maharera.mahaonline.gov.in/"
    },

    # --- CHENNAI (16 Builders) ---
    {
        "id": "bld_casagrand_chn", "name": "Casagrand Builder", "city_id": "chennai", "tier": "Tier 1 Regional Champion",
        "headquarters": "Chennai, Tamil Nadu", "established_year": 2004, "rera_compliance_score": 96,
        "on_time_delivery_pct": 95, "construction_quality_rating": 9.2, "litigation_index": "Low",
        "total_delivered_sqft_mn": 38.0, "flagship_projects": {"chennai": "Casagrand Utopia (Manapakkam), Casagrand First City, Casagrand Zenith"},
        "active_states_and_cities": ["Tamil Nadu", "Chennai", "Bengaluru", "Hyderabad", "Coimbatore"],
        "strengths": "Market share leader in Chennai residential, 70+ lifestyle amenities, kid-friendly infrastructure.",
        "cautions": "Fast execution requires close inspection of finishing snag lists.",
        "rera_portal_url": "https://www.rera.tn.gov.in/"
    },
    {
        "id": "bld_prestige_chn", "name": "Prestige Group", "city_id": "chennai", "tier": "Tier 1 Premier National",
        "headquarters": "Bengaluru, Karnataka", "established_year": 1986, "rera_compliance_score": 97,
        "on_time_delivery_pct": 95, "construction_quality_rating": 9.4, "litigation_index": "Low",
        "total_delivered_sqft_mn": 150.0, "flagship_projects": {"chennai": "Prestige Courtyards (Sholinganallur), Prestige Silver Springs, Prestige Bella Vista"},
        "active_states_and_cities": ["Tamil Nadu", "Chennai", "Karnataka", "Telangana"],
        "strengths": "Superb layout planning, high rental demand from OMR IT professionals, premium resale price.",
        "cautions": "Sholinganallur approach roads experience peak hour traffic signals.",
        "rera_portal_url": "https://www.rera.tn.gov.in/"
    },
    {
        "id": "bld_brigade_chn", "name": "Brigade Group", "city_id": "chennai", "tier": "Tier 1 Premier National",
        "headquarters": "Bengaluru, Karnataka", "established_year": 1986, "rera_compliance_score": 96,
        "on_time_delivery_pct": 94, "construction_quality_rating": 9.3, "litigation_index": "Low",
        "total_delivered_sqft_mn": 86.0, "flagship_projects": {"chennai": "Brigade Residences at WTC (Perungudi), Brigade Xanadu (Mogappair)"},
        "active_states_and_cities": ["Tamil Nadu", "Chennai", "Karnataka", "Telangana"],
        "strengths": "World Trade Center integrated township, institutional quality build standards.",
        "cautions": "Perungudi toll plaza bottleneck during monsoon downpours.",
        "rera_portal_url": "https://www.rera.tn.gov.in/"
    },
    {
        "id": "bld_sobha_chn", "name": "Sobha Limited", "city_id": "chennai", "tier": "Tier 1 Premier National",
        "headquarters": "Bengaluru, Karnataka", "established_year": 1995, "rera_compliance_score": 98,
        "on_time_delivery_pct": 97, "construction_quality_rating": 9.6, "litigation_index": "Minimal",
        "total_delivered_sqft_mn": 120.5, "flagship_projects": {"chennai": "Sobha Gardenia (Velachery), Sobha Meritta (OMR)"},
        "active_states_and_cities": ["Tamil Nadu", "Chennai", "Karnataka", "NCR"],
        "strengths": "Unrivalled internal structural quality, self-reliant construction execution.",
        "cautions": "Check surrounding road elevation when choosing Velachery micro-market.",
        "rera_portal_url": "https://www.rera.tn.gov.in/"
    },
    {
        "id": "bld_puravankara_chn", "name": "Puravankara Limited", "city_id": "chennai", "tier": "Tier 1 Premier National",
        "headquarters": "Bengaluru, Karnataka", "established_year": 1975, "rera_compliance_score": 95,
        "on_time_delivery_pct": 92, "construction_quality_rating": 9.3, "litigation_index": "Low",
        "total_delivered_sqft_mn": 48.0, "flagship_projects": {"chennai": "Purva Somerset House (Guindy), Purva Windermere (Pallikaranai)"},
        "active_states_and_cities": ["Tamil Nadu", "Chennai", "Karnataka", "Maharashtra"],
        "strengths": "Prime Guindy race-course facing properties, excellent flood resilience on elevated ridges.",
        "cautions": "Pallikaranai projects require verification of internal stormwater pumping capacity.",
        "rera_portal_url": "https://www.rera.tn.gov.in/"
    },
    {
        "id": "bld_tvs_chn", "name": "TVS Emerald (TVS Motor Group)", "city_id": "chennai", "tier": "Tier 1 Corporate Pedigree",
        "headquarters": "Chennai, Tamil Nadu", "established_year": 2012, "rera_compliance_score": 97,
        "on_time_delivery_pct": 96, "construction_quality_rating": 9.4, "litigation_index": "Minimal",
        "total_delivered_sqft_mn": 16.0, "flagship_projects": {"chennai": "TVS Emerald Hamlet (Karapakkam), TVS Emerald GreenAcres (Perungalathur)"},
        "active_states_and_cities": ["Tamil Nadu", "Chennai", "Bengaluru"],
        "strengths": "TVS corporate trust, 5-year maintenance warranty, transparent land titles.",
        "cautions": "Plotted developments require independent villa construction management.",
        "rera_portal_url": "https://www.rera.tn.gov.in/"
    },
    {
        "id": "bld_appaswamy_chn", "name": "Appaswamy Real Estates", "city_id": "chennai", "tier": "Tier 1 Legacy Regional",
        "headquarters": "Chennai, Tamil Nadu", "established_year": 1959, "rera_compliance_score": 97,
        "on_time_delivery_pct": 96, "construction_quality_rating": 9.5, "litigation_index": "Minimal",
        "total_delivered_sqft_mn": 28.0, "flagship_projects": {"chennai": "Appaswamy Trellis (Vadapalani), Appaswamy The Bloomingdale (Pammal), Altezza (OMR)"},
        "active_states_and_cities": ["Tamil Nadu", "Chennai"],
        "strengths": "Over 65 years of flawless delivery track record, prime core city locations.",
        "cautions": "Traditional design aesthetics compared to contemporary international themes.",
        "rera_portal_url": "https://www.rera.tn.gov.in/"
    },
    {
        "id": "bld_akshaya_chn", "name": "Akshaya Homes", "city_id": "chennai", "tier": "Tier 2 Established Regional",
        "headquarters": "Chennai, Tamil Nadu", "established_year": 1995, "rera_compliance_score": 92,
        "on_time_delivery_pct": 90, "construction_quality_rating": 8.9, "litigation_index": "Low",
        "total_delivered_sqft_mn": 18.0, "flagship_projects": {"chennai": "Akshaya Today (OMR Kelambakkam), Akshaya Republic (Kovur)"},
        "active_states_and_cities": ["Tamil Nadu", "Chennai", "Coimbatore"],
        "strengths": "CRISIL DA2+ rating, green building pioneer in Tamil Nadu.",
        "cautions": "Kelambakkam stretch is ~15 km south of central OMR tech parks.",
        "rera_portal_url": "https://www.rera.tn.gov.in/"
    },
    {
        "id": "bld_olympia_chn", "name": "The Olympia Group", "city_id": "chennai", "tier": "Tier 1 Regional Champion",
        "headquarters": "Chennai, Tamil Nadu", "established_year": 2004, "rera_compliance_score": 95,
        "on_time_delivery_pct": 93, "construction_quality_rating": 9.3, "litigation_index": "Low",
        "total_delivered_sqft_mn": 22.0, "flagship_projects": {"chennai": "Olympia Tech Park (Guindy), Olympia Opaline (Navallur), Olympia Grande (Pallavaram)"},
        "active_states_and_cities": ["Tamil Nadu", "Chennai", "Kolkata", "Bengaluru"],
        "strengths": "Iconic commercial landmarks, eco-friendly luxury residential towers.",
        "cautions": "Navallur corridor traffic during morning tech hub rush.",
        "rera_portal_url": "https://www.rera.tn.gov.in/"
    },
    {
        "id": "bld_radiance_chn", "name": "Radiance Realty", "city_id": "chennai", "tier": "Tier 2 Established Regional",
        "headquarters": "Chennai, Tamil Nadu", "established_year": 2012, "rera_compliance_score": 93,
        "on_time_delivery_pct": 91, "construction_quality_rating": 8.9, "litigation_index": "Low",
        "total_delivered_sqft_mn": 14.0, "flagship_projects": {"chennai": "Radiance The Pride (Pallavaram), Radiance Empire (Perambur), Radiance Smartville"},
        "active_states_and_cities": ["Tamil Nadu", "Chennai", "Bengaluru", "Coimbatore"],
        "strengths": "Fast construction turnover, competitive price per sqft.",
        "cautions": "High unit density per acre.",
        "rera_portal_url": "https://www.rera.tn.gov.in/"
    },
    {
        "id": "bld_dra_chn", "name": "DRA Homes", "city_id": "chennai", "tier": "Tier 2 Established Regional",
        "headquarters": "Chennai, Tamil Nadu", "established_year": 2006, "rera_compliance_score": 94,
        "on_time_delivery_pct": 94, "construction_quality_rating": 9.1, "litigation_index": "Minimal",
        "total_delivered_sqft_mn": 12.0, "flagship_projects": {"chennai": "DRA Tuxedo (Velachery), DRA Pristine Pavilion (Mahindra World City), DRA Truliv"},
        "active_states_and_cities": ["Tamil Nadu", "Chennai", "Bengaluru"],
        "strengths": "Customer-centric construction meter tracking, strict on-time commitments.",
        "cautions": "Boutique scale developments with moderate open park space.",
        "rera_portal_url": "https://www.rera.tn.gov.in/"
    },
    {
        "id": "bld_navins_chn", "name": "Navin Housing & Properties", "city_id": "chennai", "tier": "Tier 1 Legacy Regional",
        "headquarters": "Chennai, Tamil Nadu", "established_year": 1989, "rera_compliance_score": 96,
        "on_time_delivery_pct": 96, "construction_quality_rating": 9.4, "litigation_index": "Minimal",
        "total_delivered_sqft_mn": 15.0, "flagship_projects": {"chennai": "Navin's Starwood Towers (Medavakkam), Navin's Hanging Gardens, Navin's Hillview"},
        "active_states_and_cities": ["Tamil Nadu", "Chennai"],
        "strengths": "First builder in South India to achieve ISO 9001 certification, immaculate paperwork.",
        "cautions": "Less aggressive marketing; slower secondary market trading.",
        "rera_portal_url": "https://www.rera.tn.gov.in/"
    },
    {
        "id": "bld_ceebros_chn", "name": "Ceebros Designworks", "city_id": "chennai", "tier": "Tier 1 Architectural Boutique",
        "headquarters": "Chennai, Tamil Nadu", "established_year": 1980, "rera_compliance_score": 96,
        "on_time_delivery_pct": 95, "construction_quality_rating": 9.5, "litigation_index": "Minimal",
        "total_delivered_sqft_mn": 16.0, "flagship_projects": {"chennai": "Ceebros Boulevard (OMR), Ceebros One50 (ECR), Ceebros Grayshott"},
        "active_states_and_cities": ["Tamil Nadu", "Chennai"],
        "strengths": "Superb contemporary architecture, hospitality-grade lobby finishes.",
        "cautions": "Premium ticket pricing.",
        "rera_portal_url": "https://www.rera.tn.gov.in/"
    },
    {
        "id": "bld_vgn_chn", "name": "VGN Projects", "city_id": "chennai", "tier": "Tier 2 Established Regional",
        "headquarters": "Chennai, Tamil Nadu", "established_year": 1942, "rera_compliance_score": 89,
        "on_time_delivery_pct": 87, "construction_quality_rating": 8.4, "litigation_index": "Moderate",
        "total_delivered_sqft_mn": 24.0, "flagship_projects": {"chennai": "VGN Fairmont (Guindy), VGN Brixton (Irungattukottai), VGN Stafford"},
        "active_states_and_cities": ["Tamil Nadu", "Chennai"],
        "strengths": "Large plotted developments and mid-segment township projects in West Chennai.",
        "cautions": "Earlier pre-RERA delivery delays on peripheral projects.",
        "rera_portal_url": "https://www.rera.tn.gov.in/"
    },
    {
        "id": "bld_baashyaam_chn", "name": "Baashyaam Group", "city_id": "chennai", "tier": "Tier 1 Regional Champion",
        "headquarters": "Chennai, Tamil Nadu", "established_year": 2004, "rera_compliance_score": 95,
        "on_time_delivery_pct": 94, "construction_quality_rating": 9.3, "litigation_index": "Low",
        "total_delivered_sqft_mn": 26.0, "flagship_projects": {"chennai": "Baashyaam Pinnacle Crest (Sholinganallur), Plutus Residence (Anna Nagar)"},
        "active_states_and_cities": ["Tamil Nadu", "Chennai", "Kanchipuram"],
        "strengths": "Dominant luxury high-rise builder in Anna Nagar and OMR, prime arterial road frontage.",
        "cautions": "Higher density floor layouts.",
        "rera_portal_url": "https://www.rera.tn.gov.in/"
    },
    {
        "id": "bld_doshi_chn", "name": "Doshi Housing", "city_id": "chennai", "tier": "Tier 2 Established Regional",
        "headquarters": "Chennai, Tamil Nadu", "established_year": 1982, "rera_compliance_score": 91,
        "on_time_delivery_pct": 90, "construction_quality_rating": 8.7, "litigation_index": "Low",
        "total_delivered_sqft_mn": 14.0, "flagship_projects": {"chennai": "Doshi Rising Pearl (Pallikaranai), Doshi First Nest (Perungudi)"},
        "active_states_and_cities": ["Tamil Nadu", "Chennai"],
        "strengths": "Affordable entry tickets for IT professionals working in OMR and Velachery.",
        "cautions": "Inspect basement flood mitigation pumping systems in low-lying pockets.",
        "rera_portal_url": "https://www.rera.tn.gov.in/"
    },

    # --- DELHI-NCR (16 Builders) ---
    {
        "id": "bld_dlf_del", "name": "DLF Limited", "city_id": "delhi_ncr", "tier": "Tier 1 Premier National",
        "headquarters": "New Delhi / Gurugram", "established_year": 1946, "rera_compliance_score": 99,
        "on_time_delivery_pct": 98, "construction_quality_rating": 9.8, "litigation_index": "Minimal / Negligible",
        "total_delivered_sqft_mn": 340.0, "flagship_projects": {"delhi_ncr": "DLF The Crest, DLF The Camellias, DLF Alameda, DLF Cyber City"},
        "active_states_and_cities": ["Delhi", "Haryana", "NCR", "Chandigarh", "Chennai"],
        "strengths": "Largest listed real estate company in India, signal-free 16-lane private roads, private fire stations and power backup.",
        "cautions": "Ticket size runs from ₹10 Cr to ₹60 Cr on Golf Course Road.",
        "rera_portal_url": "https://haryanarera.gov.in/"
    },
    {
        "id": "bld_godrej_del", "name": "Godrej Properties", "city_id": "delhi_ncr", "tier": "Tier 1 Premier National",
        "headquarters": "Mumbai, Maharashtra", "established_year": 1990, "rera_compliance_score": 97,
        "on_time_delivery_pct": 93, "construction_quality_rating": 9.2, "litigation_index": "Low",
        "total_delivered_sqft_mn": 95.0, "flagship_projects": {"delhi_ncr": "Godrej Woods (Sec 43 Noida), Godrej South Estate (Okhla), Godrej Aristocrat (Sec 49 Gurugram)"},
        "active_states_and_cities": ["NCR", "Delhi", "Gurugram", "Noida", "Maharashtra", "Karnataka"],
        "strengths": "Corporate governance, pristine green themes, brisk resale turnover in Noida and Gurugram.",
        "cautions": "High registration stamp duty in UP and Haryana sectors.",
        "rera_portal_url": "https://up-rera.in/"
    },
    {
        "id": "bld_sobha_del", "name": "Sobha Limited", "city_id": "delhi_ncr", "tier": "Tier 1 Premier National",
        "headquarters": "Bengaluru, Karnataka", "established_year": 1995, "rera_compliance_score": 98,
        "on_time_delivery_pct": 96, "construction_quality_rating": 9.6, "litigation_index": "Minimal",
        "total_delivered_sqft_mn": 120.5, "flagship_projects": {"delhi_ncr": "Sobha City (Dwarka Expressway Sec 108), Sobha International City (Sec 109)"},
        "active_states_and_cities": ["NCR", "Gurugram", "Karnataka", "Tamil Nadu"],
        "strengths": "39-acre township with two cricket grounds, German precast manufacturing on site, high plinth.",
        "cautions": "Dwarka expressway cloverleaf connection requires completing sector arterial links.",
        "rera_portal_url": "https://haryanarera.gov.in/"
    },
    {
        "id": "bld_eldeco_del", "name": "Eldeco Group", "city_id": "delhi_ncr", "tier": "Tier 1 Regional Champion (North)",
        "headquarters": "New Delhi / Lucknow", "established_year": 1975, "rera_compliance_score": 96,
        "on_time_delivery_pct": 94, "construction_quality_rating": 9.2, "litigation_index": "Low",
        "total_delivered_sqft_mn": 42.0, "flagship_projects": {"delhi_ncr": "Eldeco Live Neoma (Sector 150 Noida), Eldeco Utopia, Eldeco Acclaim (Sohna)"},
        "active_states_and_cities": ["NCR", "Noida", "Greater Noida", "Uttar Pradesh", "Lucknow", "Varanasi", "Prayagraj"],
        "strengths": "Unblemished 50-year North India delivery record, 0 debt on multiple flagship projects, excellent sports sector designs.",
        "cautions": "Sector 150 is low-density sports sector with commute distance to Central Delhi.",
        "rera_portal_url": "https://up-rera.in/"
    },
    {
        "id": "bld_tata_del", "name": "Tata Housing", "city_id": "delhi_ncr", "tier": "Tier 1 Premier National",
        "headquarters": "Mumbai, Maharashtra", "established_year": 1984, "rera_compliance_score": 96,
        "on_time_delivery_pct": 93, "construction_quality_rating": 9.3, "litigation_index": "Minimal",
        "total_delivered_sqft_mn": 35.0, "flagship_projects": {"delhi_ncr": "Tata Primanti (Sec 72 Gurugram), Tata Gurgaon Gateway (Sec 112), Tata Eureka Park (Sec 150 Noida)"},
        "active_states_and_cities": ["NCR", "Gurugram", "Noida", "Maharashtra"],
        "strengths": "Southern Peripheral Road frontage, intelligent biophilic design, rock-solid structural warranties.",
        "cautions": "Fixed pricing policies during festive promotions.",
        "rera_portal_url": "https://haryanarera.gov.in/"
    },
    {
        "id": "bld_max_del", "name": "Max Estates", "city_id": "delhi_ncr", "tier": "Tier 1 Ultra-Luxury Corporate",
        "headquarters": "New Delhi, NCR", "established_year": 2016, "rera_compliance_score": 98,
        "on_time_delivery_pct": 97, "construction_quality_rating": 9.7, "litigation_index": "Minimal",
        "total_delivered_sqft_mn": 12.0, "flagship_projects": {"delhi_ncr": "Estate 128 (Noida Expressway), Estate 360 (Dwarka Expressway Sec 36A), Max Towers"},
        "active_states_and_cities": ["NCR", "Noida", "Gurugram", "Delhi"],
        "strengths": "Max Group wellness-focused real estate, IGBC Platinum & WELL certified, record-breaking pre-sales velocity.",
        "cautions": "Limited historical inventory volume; ultra-high price bracket.",
        "rera_portal_url": "https://up-rera.in/"
    },
    {
        "id": "bld_m3m_del", "name": "M3M India", "city_id": "delhi_ncr", "tier": "Tier 1 Regional Giant",
        "headquarters": "Gurugram, Haryana", "established_year": 2010, "rera_compliance_score": 92,
        "on_time_delivery_pct": 89, "construction_quality_rating": 9.0, "litigation_index": "Moderate",
        "total_delivered_sqft_mn": 65.0, "flagship_projects": {"delhi_ncr": "M3M Golfestate (Golf Course Ext Rd), M3M Crown (Sec 111), M3M The Cullinan (Noida)"},
        "active_states_and_cities": ["NCR", "Gurugram", "Noida", "Panipat"],
        "strengths": "Golf Course Extension Road market leader, luxury high-street retail integration, lavish 7-star clubhouses.",
        "cautions": "High commercial exposure; monitor RERA escrow accounts for phased deliveries.",
        "rera_portal_url": "https://haryanarera.gov.in/"
    },
    {
        "id": "bld_smartworld_del", "name": "Smartworld Developers", "city_id": "delhi_ncr", "tier": "Tier 2 Fast-Growing Luxury",
        "headquarters": "Gurugram, Haryana", "established_year": 2021, "rera_compliance_score": 93,
        "on_time_delivery_pct": 92, "construction_quality_rating": 9.1, "litigation_index": "Minimal",
        "total_delivered_sqft_mn": 15.0, "flagship_projects": {"delhi_ncr": "Smartworld The Edition (Sec 66 Gurugram), Smartworld One DXP (Sec 113)"},
        "active_states_and_cities": ["NCR", "Gurugram"],
        "strengths": "Singapore-style condominium planning, prominent frontage on Dwarka Expressway & Golf Course Ext Rd.",
        "cautions": "Younger operating brand backed by experienced industry veterans.",
        "rera_portal_url": "https://haryanarera.gov.in/"
    },
    {
        "id": "bld_signature_del", "name": "Signature Global", "city_id": "delhi_ncr", "tier": "Tier 1 Public Listed Mid-to-Premium",
        "headquarters": "New Delhi / Gurugram", "established_year": 2014, "rera_compliance_score": 95,
        "on_time_delivery_pct": 94, "construction_quality_rating": 9.0, "litigation_index": "Low",
        "total_delivered_sqft_mn": 28.0, "flagship_projects": {"delhi_ncr": "Signature Global City 63A, Signature Global Titanium (Sec 71), Park Plots (Sohna)"},
        "active_states_and_cities": ["NCR", "Gurugram", "Sohna", "Karnal"],
        "strengths": "Fastest delivery turnaround in Gurugram, publicly listed transparency, IFC World Bank backed green certifications.",
        "cautions": "Independent floors have shared parking bays.",
        "rera_portal_url": "https://haryanarera.gov.in/"
    },
    {
        "id": "bld_ats_del", "name": "ATS Homekraft", "city_id": "delhi_ncr", "tier": "Tier 2 Established Regional",
        "headquarters": "Noida, Uttar Pradesh", "established_year": 1998, "rera_compliance_score": 91,
        "on_time_delivery_pct": 88, "construction_quality_rating": 9.2, "litigation_index": "Moderate",
        "total_delivered_sqft_mn": 35.0, "flagship_projects": {"delhi_ncr": "ATS Pristine (Sec 150 Noida), ATS Knightsbridge, ATS Tourmaline (Sec 109 Gurugram)"},
        "active_states_and_cities": ["NCR", "Noida", "Greater Noida", "Gurugram"],
        "strengths": "Pioneers of green open spaces in Noida, signature red-brick architectural facades.",
        "cautions": "ATS parent group had liquidity delays; Homekraft entity is delivering steadily under SWAMIH fund.",
        "rera_portal_url": "https://up-rera.in/"
    },
    {
        "id": "bld_gaur_del", "name": "Gaurs Group (Gaursons)", "city_id": "delhi_ncr", "tier": "Tier 1 Regional Champion (Noida/NCR)",
        "headquarters": "Ghaziabad / Greater Noida", "established_year": 1995, "rera_compliance_score": 94,
        "on_time_delivery_pct": 93, "construction_quality_rating": 8.9, "litigation_index": "Low",
        "total_delivered_sqft_mn": 65.0, "flagship_projects": {"delhi_ncr": "Gaur City (Noida Extension), Gaur The Islands (Jaypee Greens Pari Chowk), Gaur Saundaryam"},
        "active_states_and_cities": ["NCR", "Greater Noida", "Noida", "Ghaziabad"],
        "strengths": "Over 65,000 homes delivered, pristine master townships with integrated Gaur City Mall and schools.",
        "cautions": "Noida Extension has high vehicular congestion along Char Murti roundabout.",
        "rera_portal_url": "https://up-rera.in/"
    },
    {
        "id": "bld_mahagun_del", "name": "Mahagun Group", "city_id": "delhi_ncr", "tier": "Tier 2 Established Regional",
        "headquarters": "Noida, Uttar Pradesh", "established_year": 1995, "rera_compliance_score": 91,
        "on_time_delivery_pct": 89, "construction_quality_rating": 8.8, "litigation_index": "Low to Moderate",
        "total_delivered_sqft_mn": 25.0, "flagship_projects": {"delhi_ncr": "Mahagun Manorialle (Sec 128 Noida), Mahagun Mezzaria (Sec 78), Mahagun Moderne"},
        "active_states_and_cities": ["NCR", "Noida", "Greater Noida", "Ghaziabad"],
        "strengths": "Prominent presence along Noida-Greater Noida Expressway, golf-course facing units.",
        "cautions": "Moderate club maintenance fee outlays.",
        "rera_portal_url": "https://up-rera.in/"
    },
    {
        "id": "bld_paras_del", "name": "Paras Buildtech", "city_id": "delhi_ncr", "tier": "Tier 2 Established Regional",
        "headquarters": "Gurugram, Haryana", "established_year": 2002, "rera_compliance_score": 92,
        "on_time_delivery_pct": 90, "construction_quality_rating": 8.9, "litigation_index": "Low",
        "total_delivered_sqft_mn": 15.0, "flagship_projects": {"delhi_ncr": "Paras Quartier (Gwal Pahari Gurugram), Paras Seasons (Sec 168 Noida)"},
        "active_states_and_cities": ["NCR", "Gurugram", "Noida", "Mohali"],
        "strengths": "Paras Quartier features 3D iconic towers near Aravali biodiverse hills.",
        "cautions": "Gwal Pahari connects to Faridabad-Gurugram highway with limited pedestrian access.",
        "rera_portal_url": "https://haryanarera.gov.in/"
    },
    {
        "id": "bld_ganga_del", "name": "Ganga Realty", "city_id": "delhi_ncr", "tier": "Tier 2 Established Fast-Growing",
        "headquarters": "Gurugram, Haryana", "established_year": 2018, "rera_compliance_score": 93,
        "on_time_delivery_pct": 92, "construction_quality_rating": 9.0, "litigation_index": "Minimal",
        "total_delivered_sqft_mn": 8.0, "flagship_projects": {"delhi_ncr": "Ganga Anantam (Sec 85 Gurugram), Ganga Nandaka (Sec 84), Tathastu (Sohna)"},
        "active_states_and_cities": ["NCR", "Gurugram", "Sohna"],
        "strengths": "AI-powered smart home automation, pure residential non-commercial clusters.",
        "cautions": "Newer track record in Gurugram high-rises.",
        "rera_portal_url": "https://haryanarera.gov.in/"
    },
    {
        "id": "bld_centralpark_del", "name": "Central Park (Bakshi Group)", "city_id": "delhi_ncr", "tier": "Tier 1 Ultra-Luxury Hospitality",
        "headquarters": "Gurugram, Haryana", "established_year": 2001, "rera_compliance_score": 95,
        "on_time_delivery_pct": 92, "construction_quality_rating": 9.6, "litigation_index": "Low",
        "total_delivered_sqft_mn": 18.0, "flagship_projects": {"delhi_ncr": "Central Park Resorts (Sec 48 Gurugram), Central Park Flower Valley (Sohna)"},
        "active_states_and_cities": ["NCR", "Gurugram", "Sohna", "Goa"],
        "strengths": "Zero vehicle movement on ground level, 5-star hotel concierge services, horse-riding and golf facilities.",
        "cautions": "High maintenance costs reflecting 5-star resort hospitality staff.",
        "rera_portal_url": "https://haryanarera.gov.in/"
    },
    {
        "id": "bld_ashiana_del", "name": "Ashiana Housing", "city_id": "delhi_ncr", "tier": "Tier 1 Specialist (Senior & Kid-Centric)",
        "headquarters": "New Delhi", "established_year": 1979, "rera_compliance_score": 97,
        "on_time_delivery_pct": 96, "construction_quality_rating": 9.4, "litigation_index": "Minimal",
        "total_delivered_sqft_mn": 26.0, "flagship_projects": {"delhi_ncr": "Ashiana Amarah (Sec 93 Gurugram), Ashiana Nirmay (Bhiwadi), Ashiana Mulberry (Sohna)"},
        "active_states_and_cities": ["NCR", "Gurugram", "Rajasthan", "Maharashtra", "Tamil Nadu"],
        "strengths": "Ranked #1 for Senior Living & Kid-Centric homes in India by Track2Realty, outstanding maintenance culture.",
        "cautions": "Resale market targets family and senior end-users rather than speculative investors.",
        "rera_portal_url": "https://haryanarera.gov.in/"
    },

    # --- HYDERABAD (16 Builders) ---
    {
        "id": "bld_aparna_hyd", "name": "Aparna Constructions", "city_id": "hyderabad", "tier": "Tier 1 Regional Champion",
        "headquarters": "Hyderabad, Telangana", "established_year": 1996, "rera_compliance_score": 99,
        "on_time_delivery_pct": 98, "construction_quality_rating": 9.5, "litigation_index": "Minimal / Negligible",
        "total_delivered_sqft_mn": 52.0, "flagship_projects": {"hyderabad": "Aparna Serene Park (Gachibowli), Aparna Sarovar Zenith (Nallagandla), Aparna Dharti"},
        "active_states_and_cities": ["Telangana", "Hyderabad", "Andhra Pradesh", "Bengaluru"],
        "strengths": "Zero project default or delay in 29 years, in-house RMC concrete plants, highest on-time trust in Telugu states.",
        "cautions": "Uniform functional architectural aesthetic across mid-segment projects.",
        "rera_portal_url": "https://rera.telangana.gov.in/"
    },
    {
        "id": "bld_myhome_hyd", "name": "My Home Group", "city_id": "hyderabad", "tier": "Tier 1 Regional Champion",
        "headquarters": "Hyderabad, Telangana", "established_year": 1986, "rera_compliance_score": 99,
        "on_time_delivery_pct": 97, "construction_quality_rating": 9.6, "litigation_index": "Minimal",
        "total_delivered_sqft_mn": 45.0, "flagship_projects": {"hyderabad": "My Home Bhooja (HITECH City), My Home Sayuk (Tellapur), My Home Ankura"},
        "active_states_and_cities": ["Telangana", "Hyderabad"],
        "strengths": "Own cement manufacturing (Maha Cement), marquee IT SEZ developer, premier luxury brand status.",
        "cautions": "High capital appreciation has pushed entry prices above ₹1.6 Cr for 2BHK.",
        "rera_portal_url": "https://rera.telangana.gov.in/"
    },
    {
        "id": "bld_prestige_hyd", "name": "Prestige Group", "city_id": "hyderabad", "tier": "Tier 1 Premier National",
        "headquarters": "Bengaluru, Karnataka", "established_year": 1986, "rera_compliance_score": 97,
        "on_time_delivery_pct": 95, "construction_quality_rating": 9.4, "litigation_index": "Low",
        "total_delivered_sqft_mn": 150.0, "flagship_projects": {"hyderabad": "Prestige High Fields (Financial District), Prestige Clairemont (Neopolis Kokapet)"},
        "active_states_and_cities": ["Telangana", "Hyderabad", "Karnataka"],
        "strengths": "Disney-themed landscaping, premier Kokapet Neopolis greenfield land banks.",
        "cautions": "Kokapet infrastructure under active HMDA trunk line expansion.",
        "rera_portal_url": "https://rera.telangana.gov.in/"
    },
    {
        "id": "bld_brigade_hyd", "name": "Brigade Group", "city_id": "hyderabad", "tier": "Tier 1 Premier National",
        "headquarters": "Bengaluru, Karnataka", "established_year": 1986, "rera_compliance_score": 96,
        "on_time_delivery_pct": 94, "construction_quality_rating": 9.3, "litigation_index": "Low",
        "total_delivered_sqft_mn": 86.0, "flagship_projects": {"hyderabad": "Brigade Citadel (Moti Nagar), Brigade Gateway Hyderabad"},
        "active_states_and_cities": ["Telangana", "Hyderabad", "Karnataka"],
        "strengths": "Transit-oriented development adjacent to Erragadda and Bharat Nagar Metro Stations.",
        "cautions": "Moti Nagar connects to high-traffic Sanath Nagar industrial corridor.",
        "rera_portal_url": "https://rera.telangana.gov.in/"
    },
    {
        "id": "bld_rajapushpa_hyd", "name": "Rajapushpa Properties", "city_id": "hyderabad", "tier": "Tier 1 Regional Champion",
        "headquarters": "Hyderabad, Telangana", "established_year": 2006, "rera_compliance_score": 96,
        "on_time_delivery_pct": 95, "construction_quality_rating": 9.4, "litigation_index": "Low",
        "total_delivered_sqft_mn": 22.0, "flagship_projects": {"hyderabad": "Rajapushpa Provincia (Narsingi), Rajapushpa Atria, Rajapushpa Imperia (Tellapur)"},
        "active_states_and_cities": ["Telangana", "Hyderabad"],
        "strengths": "Unrivalled high-rise scale in West Hyderabad IT belt, 50,000 sqft clubhouse amenities.",
        "cautions": "High vehicular count in 3,000+ flat complexes during school bus morning shifts.",
        "rera_portal_url": "https://rera.telangana.gov.in/"
    },
    {
        "id": "bld_asbl_hyd", "name": "ASBL (Ashoka Builders)", "city_id": "hyderabad", "tier": "Tier 2 Fast-Growing Tech-Led",
        "headquarters": "Hyderabad, Telangana", "established_year": 2017, "rera_compliance_score": 95,
        "on_time_delivery_pct": 94, "construction_quality_rating": 9.2, "litigation_index": "Minimal",
        "total_delivered_sqft_mn": 10.0, "flagship_projects": {"hyderabad": "ASBL Spire (Kokapet), ASBL Spectra (Gachibowli), ASBL Broadway"},
        "active_states_and_cities": ["Telangana", "Hyderabad"],
        "strengths": "PropTech transparency, mobile app tracking of every concrete pour, contemporary exterior styling.",
        "cautions": "Slightly younger operating entity compared to heritage builders.",
        "rera_portal_url": "https://rera.telangana.gov.in/"
    },
    {
        "id": "bld_jayabheri_hyd", "name": "Jayabheri Properties", "city_id": "hyderabad", "tier": "Tier 1 Legacy Regional",
        "headquarters": "Hyderabad, Telangana", "established_year": 1989, "rera_compliance_score": 96,
        "on_time_delivery_pct": 94, "construction_quality_rating": 9.4, "litigation_index": "Minimal",
        "total_delivered_sqft_mn": 18.0, "flagship_projects": {"hyderabad": "Jayabheri Silicon County, The Peak (Financial District), Jayabheri The Summit"},
        "active_states_and_cities": ["Telangana", "Hyderabad", "Andhra Pradesh"],
        "strengths": "Foundational HITECH City developer, prime central locations with highest land valuation.",
        "cautions": "Selective project release with higher pricing.",
        "rera_portal_url": "https://rera.telangana.gov.in/"
    },
    {
        "id": "bld_ramky_hyd", "name": "Ramky Estates & Farms", "city_id": "hyderabad", "tier": "Tier 1 Regional Champion",
        "headquarters": "Hyderabad, Telangana", "established_year": 1994, "rera_compliance_score": 93,
        "on_time_delivery_pct": 91, "construction_quality_rating": 9.0, "litigation_index": "Low to Moderate",
        "total_delivered_sqft_mn": 30.0, "flagship_projects": {"hyderabad": "Ramky One Galaxia (Nallagandla), Ramky Discovery City (Tukkuguda), Ramky One Odyssey"},
        "active_states_and_cities": ["Telangana", "Hyderabad", "Bengaluru", "Chennai", "Visakhapatnam"],
        "strengths": "Waste management & environmental infrastructure expertise, large land parcels near Pharma City.",
        "cautions": "Tukkuguda south corridor has longer commute to western IT hubs.",
        "rera_portal_url": "https://rera.telangana.gov.in/"
    },
    {
        "id": "bld_honer_hyd", "name": "Honer Homes", "city_id": "hyderabad", "tier": "Tier 2 Established Regional",
        "headquarters": "Hyderabad, Telangana", "established_year": 2016, "rera_compliance_score": 94,
        "on_time_delivery_pct": 93, "construction_quality_rating": 9.1, "litigation_index": "Low",
        "total_delivered_sqft_mn": 12.0, "flagship_projects": {"hyderabad": "Honer Vivantis (Gopanpally), Honer Aquantis, Honer Signatis (Kukatpally)"},
        "active_states_and_cities": ["Telangana", "Hyderabad"],
        "strengths": "Prime connectivity between Gachibowli and Tellapur, thoughtful kid play features.",
        "cautions": "Gopanpally road widening ongoing under GHMC.",
        "rera_portal_url": "https://rera.telangana.gov.in/"
    },
    {
        "id": "bld_lansum_hyd", "name": "Lansum Properties", "city_id": "hyderabad", "tier": "Tier 2 Established Boutique",
        "headquarters": "Hyderabad, Telangana", "established_year": 2011, "rera_compliance_score": 93,
        "on_time_delivery_pct": 92, "construction_quality_rating": 9.0, "litigation_index": "Minimal",
        "total_delivered_sqft_mn": 8.0, "flagship_projects": {"hyderabad": "Lansum Etania (Financial District), Lansum Elena (Kokapet)"},
        "active_states_and_cities": ["Telangana", "Hyderabad", "Visakhapatnam"],
        "strengths": "Superb location directly behind Continental Hospital and US Consulate.",
        "cautions": "Strictly mid-to-high ticket sizes.",
        "rera_portal_url": "https://rera.telangana.gov.in/"
    },
    {
        "id": "bld_sumadhura_hyd", "name": "Sumadhura Group", "city_id": "hyderabad", "tier": "Tier 1 Regional Champion",
        "headquarters": "Bengaluru / Hyderabad", "established_year": 1998, "rera_compliance_score": 95,
        "on_time_delivery_pct": 93, "construction_quality_rating": 9.2, "litigation_index": "Low",
        "total_delivered_sqft_mn": 32.0, "flagship_projects": {"hyderabad": "Sumadhura Acropolis (Gachibowli), Sumadhura Horizon (Kondapur), The Olympus (Nanakramguda)"},
        "active_states_and_cities": ["Telangana", "Hyderabad", "Karnataka", "Bengaluru"],
        "strengths": "Cross-state engineering pedigree, excellent maintenance reputation in residential societies.",
        "cautions": "Kondapur botanical garden road congestion during evening peaks.",
        "rera_portal_url": "https://rera.telangana.gov.in/"
    },
    {
        "id": "bld_vertex_hyd", "name": "Vertex Homes", "city_id": "hyderabad", "tier": "Tier 2 Established Regional",
        "headquarters": "Hyderabad, Telangana", "established_year": 1994, "rera_compliance_score": 92,
        "on_time_delivery_pct": 91, "construction_quality_rating": 8.9, "litigation_index": "Low",
        "total_delivered_sqft_mn": 15.0, "flagship_projects": {"hyderabad": "Vertex Panache (Gachibowli), Vertex Siris Signature, Vertex Kingston Park"},
        "active_states_and_cities": ["Telangana", "Hyderabad", "Vijayawada"],
        "strengths": "Reliable construction, balanced ticket prices in Kukatpally and Nallagandla.",
        "cautions": "Traditional marketing without high digital visibility.",
        "rera_portal_url": "https://rera.telangana.gov.in/"
    },
    {
        "id": "bld_dsr_hyd", "name": "DSR Infrastructure", "city_id": "hyderabad", "tier": "Tier 2 Established Regional",
        "headquarters": "Bengaluru / Hyderabad", "established_year": 1988, "rera_compliance_score": 92,
        "on_time_delivery_pct": 90, "construction_quality_rating": 9.0, "litigation_index": "Low",
        "total_delivered_sqft_mn": 16.0, "flagship_projects": {"hyderabad": "DSR The Classe (Kokapet), DSR The First, DSR Fortune Prime (Madhapur)"},
        "active_states_and_cities": ["Telangana", "Hyderabad", "Karnataka", "Bengaluru"],
        "strengths": "Ultra-luxury high-rises with single flat per floor concepts in Kokapet.",
        "cautions": "High entry ticket size.",
        "rera_portal_url": "https://rera.telangana.gov.in/"
    },
    {
        "id": "bld_muppa_hyd", "name": "Muppa Projects", "city_id": "hyderabad", "tier": "Tier 2 Established Regional",
        "headquarters": "Hyderabad, Telangana", "established_year": 2012, "rera_compliance_score": 93,
        "on_time_delivery_pct": 92, "construction_quality_rating": 8.9, "litigation_index": "Minimal",
        "total_delivered_sqft_mn": 9.0, "flagship_projects": {"hyderabad": "Muppa's Alankrita (Narsingi), Muppa's Melody (Tellapur), Indraprastha"},
        "active_states_and_cities": ["Telangana", "Hyderabad"],
        "strengths": "Gated communities with lush landscaping and transparent pricing.",
        "cautions": "Approach roads in Tellapur are undergoing widening.",
        "rera_portal_url": "https://rera.telangana.gov.in/"
    },
    {
        "id": "bld_hallmark_hyd", "name": "Hallmark Builders", "city_id": "hyderabad", "tier": "Tier 2 Established Regional",
        "headquarters": "Hyderabad, Telangana", "established_year": 2008, "rera_compliance_score": 91,
        "on_time_delivery_pct": 89, "construction_quality_rating": 8.7, "litigation_index": "Low",
        "total_delivered_sqft_mn": 7.5, "flagship_projects": {"hyderabad": "Hallmark Sunnyside (Manikonda), Hallmark Treasor (Gandipet), Vesta"},
        "active_states_and_cities": ["Telangana", "Hyderabad"],
        "strengths": "Affordable pricing within 15 mins of Financial District.",
        "cautions": "Manikonda interior gullies experience localized water stagnation.",
        "rera_portal_url": "https://rera.telangana.gov.in/"
    },
    {
        "id": "bld_vasavi_hyd", "name": "Vasavi Group", "city_id": "hyderabad", "tier": "Tier 1 Regional Champion",
        "headquarters": "Hyderabad, Telangana", "established_year": 1994, "rera_compliance_score": 94,
        "on_time_delivery_pct": 92, "construction_quality_rating": 9.1, "litigation_index": "Low",
        "total_delivered_sqft_mn": 25.0, "flagship_projects": {"hyderabad": "Vasavi Atlantis (Financial District), Vasavi Skyla (HITECH City), Vasavi Ananda Nilayam"},
        "active_states_and_cities": ["Telangana", "Hyderabad"],
        "strengths": "Rapid scaling in luxury high-rises, prime land parcels across West Hyderabad.",
        "cautions": "Large unit counts per project.",
        "rera_portal_url": "https://rera.telangana.gov.in/"
    },

    # --- VARANASI & EASTERN UP 100KM CORRIDOR (16 Builders) ---
    {
        "id": "bld_eldeco_vns", "name": "Eldeco Group", "city_id": "varanasi_100km", "tier": "Tier 1 Regional Champion (North)",
        "headquarters": "New Delhi / Lucknow", "established_year": 1975, "rera_compliance_score": 97,
        "on_time_delivery_pct": 95, "construction_quality_rating": 9.4, "litigation_index": "Minimal",
        "total_delivered_sqft_mn": 42.0, "flagship_projects": {"varanasi_100km": "Eldeco Surya Greens (Shivpur Varanasi), Eldeco Shaurya Plots, Eldeco Anandam (Prayagraj)"},
        "active_states_and_cities": ["Uttar Pradesh", "Varanasi", "Prayagraj", "Lucknow", "NCR"],
        "strengths": "Over 50 years of impeccable on-time delivery across UP, high plinth construction completely outside floodplains.",
        "cautions": "Ticket size sits at the upper tier of the regional market.",
        "rera_portal_url": "https://up-rera.in/"
    },
    {
        "id": "bld_omaxe_vns", "name": "Omaxe Limited", "city_id": "varanasi_100km", "tier": "Tier 1 National Player",
        "headquarters": "New Delhi", "established_year": 1989, "rera_compliance_score": 94,
        "on_time_delivery_pct": 91, "construction_quality_rating": 9.1, "litigation_index": "Low",
        "total_delivered_sqft_mn": 132.0, "flagship_projects": {"varanasi_100km": "Omaxe Heights (Civil Lines Prayagraj), Omaxe Shiva (Varanasi)"},
        "active_states_and_cities": ["Uttar Pradesh", "Prayagraj", "Varanasi", "Lucknow", "NCR", "Punjab"],
        "strengths": "Pioneers of integrated township living in Tier 2 cities, strong secondary market trading.",
        "cautions": "Prayagraj Civil Lines property commands premium pricing.",
        "rera_portal_url": "https://up-rera.in/"
    },
    {
        "id": "bld_kashiinfra_vns", "name": "Kashi Infra Developers", "city_id": "varanasi_100km", "tier": "Tier 2 Regional Established",
        "headquarters": "Varanasi, Uttar Pradesh", "established_year": 2010, "rera_compliance_score": 92,
        "on_time_delivery_pct": 91, "construction_quality_rating": 8.8, "litigation_index": "Minimal",
        "total_delivered_sqft_mn": 6.5, "flagship_projects": {"varanasi_100km": "Ganga View Residency (Ramnagar), Kashi Smart City Plots (Shivpur)"},
        "active_states_and_cities": ["Uttar Pradesh", "Varanasi", "Mirzapur"],
        "strengths": "Specializes in high sandstone ridge and river bluff construction above High Flood Level (HFL).",
        "cautions": "Smaller portfolio size.",
        "rera_portal_url": "https://up-rera.in/"
    },
    {
        "id": "bld_shreeram_vns", "name": "Shree Ram Group (Varanasi)", "city_id": "varanasi_100km", "tier": "Tier 2 Regional Established",
        "headquarters": "Varanasi, Uttar Pradesh", "established_year": 2004, "rera_compliance_score": 93,
        "on_time_delivery_pct": 92, "construction_quality_rating": 8.9, "litigation_index": "Minimal",
        "total_delivered_sqft_mn": 8.0, "flagship_projects": {"varanasi_100km": "Varuna Enclave (High Ground Sarnath), Shree Ram Towers (Cantt)"},
        "active_states_and_cities": ["Uttar Pradesh", "Varanasi", "Jaunpur"],
        "strengths": "Strict adherence to VDA approvals, high-ground locations completely outside Varuna river inundation zones.",
        "cautions": "Traditional facade architecture.",
        "rera_portal_url": "https://up-rera.in/"
    },
    {
        "id": "bld_sangam_vns", "name": "Sangam Infratech (Prayagraj)", "city_id": "varanasi_100km", "tier": "Tier 2 Regional Established",
        "headquarters": "Prayagraj, Uttar Pradesh", "established_year": 2008, "rera_compliance_score": 93,
        "on_time_delivery_pct": 92, "construction_quality_rating": 9.0, "litigation_index": "Low",
        "total_delivered_sqft_mn": 7.0, "flagship_projects": {"varanasi_100km": "Sangam Vihar Gated Enclave (Civil Lines Ext), Sangam Heights (Ashok Nagar)"},
        "active_states_and_cities": ["Uttar Pradesh", "Prayagraj"],
        "strengths": "Focused on Prayagraj elevated British Grid ridge (Civil Lines), immune to annual Sangam backwater surges.",
        "cautions": "Limited geographical footprint outside Prayagraj.",
        "rera_portal_url": "https://up-rera.in/"
    },
    {
        "id": "bld_tulsiani_vns", "name": "Tulsiani Constructions", "city_id": "varanasi_100km", "tier": "Tier 2 Regional Established",
        "headquarters": "Prayagraj / Lucknow", "established_year": 1999, "rera_compliance_score": 90,
        "on_time_delivery_pct": 88, "construction_quality_rating": 8.7, "litigation_index": "Low to Moderate",
        "total_delivered_sqft_mn": 12.0, "flagship_projects": {"varanasi_100km": "Tulsiani Grace (Civil Lines Prayagraj), Golf View Apartments"},
        "active_states_and_cities": ["Uttar Pradesh", "Prayagraj", "Lucknow", "Varanasi"],
        "strengths": "Pioneered luxury residential multi-storey apartments in Prayagraj.",
        "cautions": "Monitor NCLT/restructuring updates on select Lucknow joint ventures.",
        "rera_portal_url": "https://up-rera.in/"
    },
    {
        "id": "bld_rudra_vns", "name": "Rudra Real Estate", "city_id": "varanasi_100km", "tier": "Tier 2 Regional Established",
        "headquarters": "Varanasi / Lucknow", "established_year": 2009, "rera_compliance_score": 89,
        "on_time_delivery_pct": 87, "construction_quality_rating": 8.5, "litigation_index": "Moderate",
        "total_delivered_sqft_mn": 11.0, "flagship_projects": {"varanasi_100km": "Rudra Samruddhi (Shivpur Varanasi), Rudra Towers (Pandeypur)"},
        "active_states_and_cities": ["Uttar Pradesh", "Varanasi", "Prayagraj", "Kanpur", "Lucknow"],
        "strengths": "Affordable ticket sizing in North Varanasi expansion corridors.",
        "cautions": "Pandeypur intersection experiences severe road bottlenecks.",
        "rera_portal_url": "https://up-rera.in/"
    },
    {
        "id": "bld_roma_vns", "name": "Roma Builders & Promoters", "city_id": "varanasi_100km", "tier": "Tier 2 Regional Boutique",
        "headquarters": "Varanasi, Uttar Pradesh", "established_year": 2005, "rera_compliance_score": 91,
        "on_time_delivery_pct": 90, "construction_quality_rating": 8.8, "litigation_index": "Minimal",
        "total_delivered_sqft_mn": 5.0, "flagship_projects": {"varanasi_100km": "Roma Greens (Babatpur Airport Road), Roma Enclave (Sigra)"},
        "active_states_and_cities": ["Uttar Pradesh", "Varanasi"],
        "strengths": "Fast airport corridor transit, clean legal title verification.",
        "cautions": "Sigra project faces old city commercial congestion.",
        "rera_portal_url": "https://up-rera.in/"
    },
    {
        "id": "bld_upavp_vns", "name": "UP Awas Vikas Parishad (UPAVP)", "city_id": "varanasi_100km", "tier": "Government Statutory Housing Authority",
        "headquarters": "Lucknow, Uttar Pradesh", "established_year": 1966, "rera_compliance_score": 98,
        "on_time_delivery_pct": 94, "construction_quality_rating": 8.9, "litigation_index": "Minimal (State Sovereign)",
        "total_delivered_sqft_mn": 180.0, "flagship_projects": {"varanasi_100km": "UPAVP Sarnath Yojna (Varanasi), UPAVP Kalindipuram (Prayagraj)"},
        "active_states_and_cities": ["Uttar Pradesh", "Varanasi", "Prayagraj", "Entire State"],
        "strengths": "100% dispute-free government land titles, wide master-planned roads, underground storm sewers.",
        "cautions": "Government paperwork and transfer registry takes 3-4 weeks.",
        "rera_portal_url": "https://up-rera.in/"
    },
    {
        "id": "bld_pda_vns", "name": "Prayagraj Development Authority (PDA)", "city_id": "varanasi_100km", "tier": "Government Statutory Development Authority",
        "headquarters": "Prayagraj, Uttar Pradesh", "established_year": 1974, "rera_compliance_score": 98,
        "on_time_delivery_pct": 95, "construction_quality_rating": 8.8, "litigation_index": "Minimal (State Sovereign)",
        "total_delivered_sqft_mn": 65.0, "flagship_projects": {"varanasi_100km": "PDA Sangam Vihar Scheme, PDA Shantipuram Yojna (Phaphamau)"},
        "active_states_and_cities": ["Uttar Pradesh", "Prayagraj"],
        "strengths": "Planned sector layouts, complete immunity to private developer financial insolvency.",
        "cautions": "Secondary resale requires standard PDA transfer fee.",
        "rera_portal_url": "https://up-rera.in/"
    },
    {
        "id": "bld_vda_vns", "name": "Varanasi Development Authority (VDA)", "city_id": "varanasi_100km", "tier": "Government Statutory Development Authority",
        "headquarters": "Varanasi, Uttar Pradesh", "established_year": 1974, "rera_compliance_score": 98,
        "on_time_delivery_pct": 94, "construction_quality_rating": 8.9, "litigation_index": "Minimal (State Sovereign)",
        "total_delivered_sqft_mn": 72.0, "flagship_projects": {"varanasi_100km": "VDA Shivpur Vihar Scheme, VDA Lalpur Residential Complex, Transport Nagar Scheme"},
        "active_states_and_cities": ["Uttar Pradesh", "Varanasi"],
        "strengths": "Government sanctioned master plan zoning, dedicated stormwater infrastructure.",
        "cautions": "Auction allotment processes require prepayment deposits.",
        "rera_portal_url": "https://up-rera.in/"
    },
    {
        "id": "bld_kashigreen_vns", "name": "Kashi Green City Developers", "city_id": "varanasi_100km", "tier": "Tier 2 Plotted Specialist",
        "headquarters": "Varanasi, Uttar Pradesh", "established_year": 2014, "rera_compliance_score": 91,
        "on_time_delivery_pct": 90, "construction_quality_rating": 8.7, "litigation_index": "Minimal",
        "total_delivered_sqft_mn": 4.5, "flagship_projects": {"varanasi_100km": "Kashi Green Township (Ring Road Phase 2), Shivpur Plots"},
        "active_states_and_cities": ["Uttar Pradesh", "Varanasi"],
        "strengths": "High appreciation potential along the newly operational Varanasi 6-lane Ring Road.",
        "cautions": "Requires independent construction of villa superstructures.",
        "rera_portal_url": "https://up-rera.in/"
    },
    {
        "id": "bld_rkbuilders_vns", "name": "R.K. Builders & Infratech", "city_id": "varanasi_100km", "tier": "Tier 2 Regional Specialist (Mirzapur)",
        "headquarters": "Mirzapur / Varanasi", "established_year": 2008, "rera_compliance_score": 90,
        "on_time_delivery_pct": 89, "construction_quality_rating": 8.7, "litigation_index": "Low",
        "total_delivered_sqft_mn": 3.8, "flagship_projects": {"varanasi_100km": "Vindhya Heights (Mirzapur Cantt), Kashi Mirzapur Link Enclave"},
        "active_states_and_cities": ["Uttar Pradesh", "Mirzapur", "Varanasi"],
        "strengths": "Elevated rocky Vindhyan red sandstone terrain with zero flood accumulation risk.",
        "cautions": "Mirzapur local civic water piping is still expanding.",
        "rera_portal_url": "https://up-rera.in/"
    },
    {
        "id": "bld_vindhya_vns", "name": "Vindhya Infratech", "city_id": "varanasi_100km", "tier": "Tier 2 Plotted Specialist",
        "headquarters": "Mirzapur, Uttar Pradesh", "established_year": 2012, "rera_compliance_score": 89,
        "on_time_delivery_pct": 88, "construction_quality_rating": 8.6, "litigation_index": "Low",
        "total_delivered_sqft_mn": 2.5, "flagship_projects": {"varanasi_100km": "Vindhya Greens Gated Plots (Chunar Road), Mirzapur Bypass Layout"},
        "active_states_and_cities": ["Uttar Pradesh", "Mirzapur"],
        "strengths": "Porous red soil gradient discharging storm run-off naturally to Vindhyan ravines.",
        "cautions": "Public transport primarily relies on highway shared tempos.",
        "rera_portal_url": "https://up-rera.in/"
    },
    {
        "id": "bld_suryarealcon_vns", "name": "Surya Realcon", "city_id": "varanasi_100km", "tier": "Tier 2 Regional Established",
        "headquarters": "Varanasi / Jaunpur", "established_year": 2011, "rera_compliance_score": 91,
        "on_time_delivery_pct": 90, "construction_quality_rating": 8.8, "litigation_index": "Minimal",
        "total_delivered_sqft_mn": 4.2, "flagship_projects": {"varanasi_100km": "Shahi Vihar (Jaunpur High Ridge), Surya Enclave (Babatpur Airport)"},
        "active_states_and_cities": ["Uttar Pradesh", "Jaunpur", "Varanasi"],
        "strengths": "Strategically built on high ridge outside the Gomti river basin overflow zone.",
        "cautions": "Jaunpur inner city roads experience daytime market congestion.",
        "rera_portal_url": "https://up-rera.in/"
    },
    {
        "id": "bld_gomti_vns", "name": "Gomti Infracon", "city_id": "varanasi_100km", "tier": "Tier 2 Plotted Specialist (Jaunpur)",
        "headquarters": "Jaunpur, Uttar Pradesh", "established_year": 2015, "rera_compliance_score": 89,
        "on_time_delivery_pct": 89, "construction_quality_rating": 8.6, "litigation_index": "Low",
        "total_delivered_sqft_mn": 2.2, "flagship_projects": {"varanasi_100km": "Gomti Green Valley Plots (Varanasi-Jaunpur Highway), Line Bazar Scheme"},
        "active_states_and_cities": ["Uttar Pradesh", "Jaunpur"],
        "strengths": "Excellent four-lane NH-31 highway frontage, 45 minutes to Varanasi International Airport.",
        "cautions": "Sub-surface tube-well water requires domestic softener for high TDS.",
        "rera_portal_url": "https://up-rera.in/"
    }
]

# Write builders.json
with open(os.path.join(DATA_DIR, "cities.json"), "w", encoding="utf-8") as f:
    json.dump(cities, f, indent=2, ensure_ascii=False)

with open(os.path.join(DATA_DIR, "builders.json"), "w", encoding="utf-8") as f:
    json.dump(builders, f, indent=2, ensure_ascii=False)

print(f"Generated cities.json ({len(cities)} cities) and builders.json ({len(builders)} builders, 16 per city) successfully.")
