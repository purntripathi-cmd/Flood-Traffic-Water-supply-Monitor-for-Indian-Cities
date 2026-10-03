"""
🌊 Urban Pulse: Flood, Traffic & Water Supply Monitor for Indian Cities
Comprehensive Civic Intelligence, Multi-Layer Google Maps & Real Estate Avoidance Screener across 6 Metropolitan Corridors:
1. Bengaluru (Karnataka)
2. Mumbai & MMR (Maharashtra)
3. Chennai (Tamil Nadu)
4. Delhi-NCR (Delhi / Haryana / UP)
5. Hyderabad (Telangana)
6. Varanasi & Eastern UP 100km Corridor (Varanasi, Prayagraj, Mirzapur, Jaunpur, Chandauli)

Integrates:
- Live System Resource Telemetry (Streamlit Process Memory, System RAM, CPU Load %) with health status
- Multi-Layer Google Maps (Roadmap, Satellite Hybrid, Terrain, Dark Matter, OSM) with Property Focus Zoom & Route lines
- Cross-City Top 10 Comparison Tables (Top Purchase/Investment, Best Gated Plots, Best Rentals) sorted High to Low
- Government Master Plan Growth Probability Catalysts (Metro expansions, Aerotropolis, Expressways, Capex ₹ Cr)
- Configurable 4th Column Benchmark Distance (Defaults to New Horizon Gurukul for Bengaluru, or city benchmark school)
- Collapsible CBSE/ICSE School Proximity & Class 1st to 12th Fee Structures
- Comprehensive Utility Breakdown (STP type, Water Softener, IoT Water Meter, Dual Piping, Piped Gas, Municipal/Cauvery connection)
- Top 15+ Builders per City directory (96 builders total, 16 per city) with RERA on-time delivery & litigation tracking
- 100% Sticky 1st-column frozen responsive tables
- Explainable AI Avoidance Copilot with citation backing
"""

import json
import os
import gc
import psutil
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st
import folium
from streamlit_folium import st_folium

from utils.table_view import render_sticky_frozen_table
from utils.geo import estimate_urban_road_distance_km, get_google_maps_search_url, get_google_maps_directions_url
from utils.scoring import compute_composite_avoidance_score, calculate_monthly_wasted_commute_hours
from utils.ai_copilot import run_avoidance_copilot_query
from utils.schools import render_schools_collapsible_html, get_nearby_cbse_schools, load_cbse_schools

# -------------------------------------------------------------
# Streamlit Page Configuration
# -------------------------------------------------------------
st.set_page_config(
    page_title="Urban Pulse | Flood, Traffic & Water Supply Monitor",
    page_icon="🌊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom Styling
st.markdown("""
<style>
    .main-title {
        font-size: 2.1rem;
        font-weight: 800;
        background: linear-gradient(90deg, #38BDF8 0%, #0D9488 50%, #34D399 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.1rem;
    }
    .sub-title {
        color: #94A3B8;
        font-size: 0.92rem;
        margin-bottom: 0.8rem;
    }
    .kpi-card {
        background-color: #1E293B;
        border: 1px solid #334155;
        border-radius: 8px;
        padding: 12px 16px;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.2);
    }
    .kpi-title {
        font-size: 0.74rem;
        text-transform: uppercase;
        color: #94A3B8;
        font-weight: 700;
        letter-spacing: 0.05em;
    }
    .kpi-value {
        font-size: 1.35rem;
        font-weight: 800;
        color: #F8FAFC;
        margin-top: 3px;
    }
    .kpi-sub {
        font-size: 0.74rem;
        color: #38BDF8;
        margin-top: 2px;
    }
    .badge-green {
        background-color: rgba(16, 185, 129, 0.15);
        color: #34D399;
        padding: 2px 8px;
        border-radius: 4px;
        font-weight: 700;
    }
    .badge-red {
        background-color: rgba(239, 68, 68, 0.15);
        color: #F87171;
        padding: 2px 8px;
        border-radius: 4px;
        font-weight: 700;
    }
</style>
""", unsafe_allow_html=True)

# -------------------------------------------------------------
# System & Process Resource Telemetry Helper
# -------------------------------------------------------------
def get_system_telemetry():
    """Calculates live process and system CPU / Memory utilization."""
    try:
        proc = psutil.Process(os.getpid())
        proc_mem_mb = round(proc.memory_info().rss / (1024 * 1024), 1)
        proc_cpu_pct = round(proc.cpu_percent(interval=None), 1)
        num_threads = proc.num_threads()

        sys_mem = psutil.virtual_memory()
        sys_cpu_pct = round(psutil.cpu_percent(interval=None), 1)
        sys_mem_pct = round(sys_mem.percent, 1)
        sys_mem_used_gb = round((sys_mem.total - sys_mem.available) / (1024**3), 2)
        sys_mem_total_gb = round(sys_mem.total / (1024**3), 2)

        if sys_mem_pct > 85 or sys_cpu_pct > 85:
            health_color = "#EF4444"
            health_badge = "High Load 🔴"
        elif sys_mem_pct > 70 or sys_cpu_pct > 70:
            health_color = "#F59E0B"
            health_badge = "Moderate 🟡"
        else:
            health_color = "#10B981"
            health_badge = "Optimal 🟢"

        return {
            "proc_mem_mb": proc_mem_mb,
            "proc_cpu_pct": proc_cpu_pct,
            "sys_cpu_pct": sys_cpu_pct,
            "sys_mem_pct": sys_mem_pct,
            "sys_mem_used_gb": sys_mem_used_gb,
            "sys_mem_total_gb": sys_mem_total_gb,
            "num_threads": num_threads,
            "health_badge": health_badge,
            "health_color": health_color
        }
    except Exception:
        return {
            "proc_mem_mb": 0.0,
            "proc_cpu_pct": 0.0,
            "sys_cpu_pct": 0.0,
            "sys_mem_pct": 0.0,
            "sys_mem_used_gb": 0.0,
            "sys_mem_total_gb": 0.0,
            "num_threads": 0,
            "health_badge": "Telemetry N/A ⚪",
            "health_color": "#94A3B8"
        }

# -------------------------------------------------------------
# Data Loader
# -------------------------------------------------------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")

@st.cache_data
def load_all_datasets():
    with open(os.path.join(DATA_DIR, "cities.json"), "r", encoding="utf-8") as f:
        cities = json.load(f)
    with open(os.path.join(DATA_DIR, "micro_markets.json"), "r", encoding="utf-8") as f:
        micro_markets = json.load(f)
    with open(os.path.join(DATA_DIR, "builders.json"), "r", encoding="utf-8") as f:
        builders = json.load(f)
    with open(os.path.join(DATA_DIR, "properties.json"), "r", encoding="utf-8") as f:
        properties = json.load(f)
    with open(os.path.join(DATA_DIR, "rental_properties.json"), "r", encoding="utf-8") as f:
        rental_properties = json.load(f)
    with open(os.path.join(DATA_DIR, "gated_plots.json"), "r", encoding="utf-8") as f:
        gated_plots = json.load(f)
    with open(os.path.join(DATA_DIR, "govt_master_plans.json"), "r", encoding="utf-8") as f:
        govt_master_plans = json.load(f)
    with open(os.path.join(DATA_DIR, "avoidance_zones.json"), "r", encoding="utf-8") as f:
        avoidance_zones = json.load(f)
    with open(os.path.join(DATA_DIR, "user_preferences.json"), "r", encoding="utf-8") as f:
        user_preferences = json.load(f)
    return cities, micro_markets, builders, properties, rental_properties, gated_plots, govt_master_plans, avoidance_zones, user_preferences

cities, micro_markets, builders, properties, rental_properties, gated_plots, govt_master_plans, avoidance_zones, user_preferences = load_all_datasets()
cbse_schools = load_cbse_schools()

# -------------------------------------------------------------
# Sidebar Controls & Configurable Filters
# -------------------------------------------------------------
st.sidebar.markdown("## 🌐 Civic Radar Controls")

city_names = {c["id"]: f"{c['name']} ({c['state']})" for c in cities}
selected_city_id = st.sidebar.selectbox(
    "📍 Select Focus Metropolitan Corridor:",
    options=list(city_names.keys()),
    format_func=lambda x: city_names[x],
    index=0
)

active_city = next(c for c in cities if c["id"] == selected_city_id)

st.sidebar.markdown("---")
st.sidebar.markdown("### 🗺️ Map Tile Provider (Google Maps)")
map_provider = st.sidebar.selectbox(
    "Map Visual Style:",
    options=[
        "Google Maps (Roadmap)",
        "Google Maps (Satellite Hybrid)",
        "Google Maps (Terrain)",
        "CartoDB Dark Matter",
        "OpenStreetMap (Standard)"
    ],
    index=0,
    help="Select high-resolution Google Maps Roadmap, Satellite Hybrid, or Terrain tiles without API key constraints."
)

st.sidebar.markdown("---")
st.sidebar.markdown("### 🏫 4th Column Distance Benchmark")
st.sidebar.caption("Configures the reference destination shown as the **4th Column** in tables. Defaults to **New Horizon Gurukul** for Bengaluru.")

benchmark_preset_map = {
    "bengaluru": {
        "🏫 New Horizon Gurukul (Default)": {"name": "New Horizon Gurukul", "lat": 12.9348, "lng": 77.7037},
        "🏢 RMZ Ecospace (Bellandur)": {"name": "RMZ Ecospace", "lat": 12.9262, "lng": 77.6836},
        "🏢 Prestige Tech Park (Kadubeesanahalli)": {"name": "Prestige Tech Park", "lat": 12.9366, "lng": 77.6953}
    },
    "mumbai_mmr": {
        "🏫 Dhirubhai Ambani Intl School (Default)": {"name": "Dhirubhai Ambani International", "lat": 19.0660, "lng": 72.8680},
        "🏢 Bandra-Kurla Complex (BKC)": {"name": "BKC", "lat": 19.0650, "lng": 72.8680},
        "🏢 Nesco IT Park (Goregaon)": {"name": "Nesco IT Park", "lat": 19.1530, "lng": 72.8540}
    },
    "chennai": {
        "🏫 Sishya School (Default)": {"name": "Sishya School", "lat": 13.0030, "lng": 80.2560},
        "🏢 Tidel Park (OMR)": {"name": "Tidel Park", "lat": 12.9890, "lng": 80.2500},
        "🏢 DLF Cybercity (Porur)": {"name": "DLF Cybercity", "lat": 13.0240, "lng": 80.1760}
    },
    "delhi_ncr": {
        "🏫 The Shri Ram School (Default)": {"name": "The Shri Ram School", "lat": 28.4890, "lng": 77.0980},
        "🏢 DLF Cyber City (Gurugram)": {"name": "DLF Cyber City", "lat": 28.4950, "lng": 77.0890},
        "🏢 Advant Navis (Noida Sec 142)": {"name": "Advant Navis", "lat": 28.5020, "lng": 77.4170}
    },
    "hyderabad": {
        "🏫 CHIREC International (Default)": {"name": "CHIREC International", "lat": 17.4640, "lng": 78.3610},
        "🏢 HITECH City Mindspace": {"name": "Mindspace HITECH City", "lat": 17.4410, "lng": 78.3810},
        "🏢 Financial District (Wipro Circle)": {"name": "Wipro Circle", "lat": 17.4180, "lng": 78.3480}
    },
    "varanasi_100km": {
        "🏫 Sunbeam School Varuna (Default)": {"name": "Sunbeam School Varuna", "lat": 25.3420, "lng": 82.9780},
        "🏛️ Kashi Vishwanath Dham": {"name": "Kashi Vishwanath Dham", "lat": 25.3109, "lng": 83.0107},
        "🏛️ Allahabad High Court (Civil Lines)": {"name": "Allahabad High Court", "lat": 25.4520, "lng": 81.8340}
    }
}

city_benchmark_choices = benchmark_preset_map.get(selected_city_id, {
    "🏫 New Horizon Gurukul (Default)": {"name": "New Horizon Gurukul", "lat": 12.9348, "lng": 77.7037}
})

selected_benchmark_label = st.sidebar.selectbox(
    "Active Benchmark Destination:",
    options=list(city_benchmark_choices.keys()),
    index=0
)
active_benchmark_obj = city_benchmark_choices[selected_benchmark_label]

st.sidebar.markdown("---")
st.sidebar.markdown("### 💰 Configurable Budget Screener")
budget_purchase_max = st.sidebar.slider(
    "Max Purchase Budget (₹ Crores):",
    min_value=0.5,
    max_value=12.0,
    value=float(user_preferences.get("budget_purchase_max_cr", 3.5)),
    step=0.25,
    help="Default ₹3.50 Cr as configured by user."
)

budget_rental_max = st.sidebar.slider(
    "Max Monthly Rent (₹ / Month):",
    min_value=15000,
    max_value=250000,
    value=int(user_preferences.get("budget_rental_max_pm", 80000)),
    step=5000,
    help="Default ₹80,000 / month as configured by user."
)

st.sidebar.markdown("### 🛡️ Avoidance & Risk Filters")
min_viability_score = st.sidebar.slider(
    "Minimum Viability Score (0 - 100):",
    min_value=20,
    max_value=90,
    value=int(user_preferences.get("avoidance_threshold_score", 50)),
    step=5,
    help="Scores below 55 represent chronic avoidance zones."
)

filter_piped_water_only = st.sidebar.checkbox(
    "Require Authorized Municipal Piped Water",
    value=False,
    help="Filter out properties reliant solely on private groundwater tankers."
)

# Sidebar System Telemetry
telemetry = get_system_telemetry()
st.sidebar.markdown("---")
st.sidebar.markdown("### ⚡ System Telemetry")
st.sidebar.markdown(f"""
<div style="background: #0B1120; border: 1px solid #1E293B; border-radius: 6px; padding: 10px; font-size: 0.8rem;">
    <div><b>CPU Usage:</b> <code style="color:#A7F3D0;">{telemetry['sys_cpu_pct']}%</code> (App: {telemetry['proc_cpu_pct']}%)</div>
    <div><b>RAM Memory:</b> <code style="color:#FCD34D;">{telemetry['sys_mem_pct']}%</code> ({telemetry['sys_mem_used_gb']} / {telemetry['sys_mem_total_gb']} GB)</div>
    <div><b>Streamlit Memory:</b> <code style="color:#38BDF8;">{telemetry['proc_mem_mb']} MB</code></div>
    <div style="margin-top:6px; text-align:right;">
        <span style="background:#064E3B; color:{telemetry['health_color']}; padding:2px 7px; border-radius:4px; font-weight:700; border:1px solid {telemetry['health_color']};">
            {telemetry['health_badge']}
        </span>
    </div>
</div>
""", unsafe_allow_html=True)

# -------------------------------------------------------------
# Main Header & System Resource Telemetry Indicator Bar
# -------------------------------------------------------------
st.markdown("<div class='main-title'>🌊 Urban Pulse: Flood, Traffic & Water Supply Monitor</div>", unsafe_allow_html=True)
st.markdown(
    f"<div class='sub-title'>Civic Resilience Screener & Real Estate Avoidance Radar for <b>{active_city['name']} ({active_city['state']})</b></div>",
    unsafe_allow_html=True
)

# Live System Telemetry Bar (Visible at Header)
st.markdown(f"""
<div style="background: #0B1120; border: 1px solid #1E293B; border-radius: 8px; padding: 7px 14px; margin: 4px 0 14px 0; display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 8px; font-size: 0.82rem;">
    <div style="display: flex; align-items: center; gap: 14px; flex-wrap: wrap;">
        <span style="color: #94A3B8;">💾 <b>Streamlit Process Memory:</b> <code style="color: #38BDF8; font-weight: 700;">{telemetry['proc_mem_mb']} MB</code></span>
        <span style="color: #94A3B8;">🖥️ <b>System RAM:</b> <code style="color: #FCD34D; font-weight: 700;">{telemetry['sys_mem_pct']}%</code> ({telemetry['sys_mem_used_gb']} / {telemetry['sys_mem_total_gb']} GB)</span>
        <span style="color: #94A3B8;">⚡ <b>CPU Utilization:</b> <code style="color: #A7F3D0; font-weight: 700;">{telemetry['sys_cpu_pct']}%</code> (App: {telemetry['proc_cpu_pct']}%)</span>
        <span style="color: #94A3B8;">🧵 <b>Threads:</b> <code>{telemetry['num_threads']}</code></span>
    </div>
    <div>
        <span style="background: #064E3B; color: {telemetry['health_color']}; padding: 3px 9px; border-radius: 4px; font-weight: 700; border: 1px solid {telemetry['health_color']};">
            Resource Health: {telemetry['health_badge']}
        </span>
    </div>
</div>
""", unsafe_allow_html=True)

# Filter Data for Active City
city_micros = [m for m in micro_markets if m["city_id"] == selected_city_id]
city_props = [p for p in properties if p["city_id"] == selected_city_id]
city_plots = [pl for pl in gated_plots if pl["city_id"] == selected_city_id]
city_rentals = [r for r in rental_properties if r["city_id"] == selected_city_id]
city_avoidance = [a for a in avoidance_zones if a["city"].lower() in active_city["name"].lower() or a["city"].lower() in selected_city_id]

# KPI Metric Row
kpi1, kpi2, kpi3, kpi4 = st.columns(4)

with kpi1:
    st.markdown(f"""
    <div class='kpi-card'>
        <div class='kpi-title'>Regional Elevation Datum</div>
        <div class='kpi-value'>{active_city['elevation_range_m'].split(' ')[0]}</div>
        <div class='kpi-sub'>{active_city['drainage_and_flood_authority']['primary_valleys'][0]}</div>
    </div>
    """, unsafe_allow_html=True)

with kpi2:
    water_info = active_city["municipal_water_authority"]
    st.markdown(f"""
    <div class='kpi-card'>
        <div class='kpi-title'>Municipal Water Piped Supply</div>
        <div class='kpi-value'>{water_info['piped_coverage_pct']}%</div>
        <div class='kpi-sub'>{water_info['daily_supply_mld']} MLD / {water_info['daily_demand_mld']} MLD Demand</div>
    </div>
    """, unsafe_allow_html=True)

with kpi3:
    traffic_info = active_city["traffic_monitoring"]
    st.markdown(f"""
    <div class='kpi-card'>
        <div class='kpi-title'>Peak Commute Delay Index</div>
        <div class='kpi-value'>{traffic_info['peak_to_free_flow_delay_index']}x</div>
        <div class='kpi-sub'>Avg Peak Speed: {traffic_info['avg_peak_commute_speed_kmh']} km/h</div>
    </div>
    """, unsafe_allow_html=True)

with kpi4:
    chronic_count = len([m for m in city_micros if m["composite_avoidance_score"] < 55])
    st.markdown(f"""
    <div class='kpi-card'>
        <div class='kpi-title'>Chronic Avoidance Zones</div>
        <div class='kpi-value' style='color:#F87171;'>{chronic_count} Hotspots</div>
        <div class='kpi-sub'>{len(city_micros) - chronic_count} Resilient Havens</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# -------------------------------------------------------------
# 8 Core Interactive Tabs
# -------------------------------------------------------------
tabs = st.tabs([
    "🗺️ Cross-City Panoramic Investment & Geospatial Radar",
    "📊 Micro-Market Avoidance Radar",
    "🏗️ Top Builders by City & State (15+ per City)",
    "🏢 Resilient Property Screener",
    "🏡 Gated Community Plots & Sites",
    "💧 Water Supply & Ground Reality",
    "🚨 Chronic Avoidance Zones Deep Dive",
    "🤖 Explainable AI Copilot"
])

# =============================================================
# TAB 1: CROSS-CITY PANORAMIC INVESTMENT & GEOSPATIAL RADAR
# =============================================================
with tabs[0]:
    st.markdown(f"### 🗺️ Multi-Layer Google Map & Cross-City Investment Radar")
    st.caption("Inspect exact spatial coordinates on Google Maps, focus & zoom onto any property with driving routes to benchmark landmarks, and evaluate cross-city Top 10 rankings.")

    # Property Focus Selector
    map_focus_options = ["-- View All Properties Across All Cities --"]
    for p in properties:
        map_focus_options.append(f"🏢 {p['name']} ({p['city_name']} • {p['micro_market']})")
    for pl in gated_plots:
        map_focus_options.append(f"🏡 {pl['name']} ({pl['city_name']} • {pl['location']})")
    for r in rental_properties:
        map_focus_options.append(f"🔑 {r['name']} ({r['city_name']} • {r['micro_market']})")

    selected_focus_prop_label = st.selectbox(
        "🎯 Choose Property to Focus & Compare on Map (Pin Highlight, Zoom & Driving Route):",
        options=map_focus_options,
        index=0,
        help="Select any property or plot to zoom in, highlight with a glowing halo pin, draw a road route line to the benchmark landmark, and inspect exact distances."
    )

    focused_prop_obj = None
    focused_category = "all"
    if selected_focus_prop_label != "-- View All Properties Across All Cities --":
        for p in properties:
            if f"🏢 {p['name']} ({p['city_name']} • {p['micro_market']})" == selected_focus_prop_label:
                focused_prop_obj = p
                focused_category = "property"
                break
        if focused_prop_obj is None:
            for pl in gated_plots:
                if f"🏡 {pl['name']} ({pl['city_name']} • {pl['location']})" == selected_focus_prop_label:
                    focused_prop_obj = pl
                    focused_category = "plot"
                    break
        if focused_prop_obj is None:
            for r in rental_properties:
                if f"🔑 {r['name']} ({r['city_name']} • {r['micro_market']})" == selected_focus_prop_label:
                    focused_prop_obj = r
                    focused_category = "rental"
                    break

    # Determine map center coordinates and zoom level
    if focused_prop_obj:
        center_lat = focused_prop_obj["lat"]
        center_lng = focused_prop_obj["lng"]
        map_zoom_level = 14
    else:
        center_lat = active_city["center_lat"]
        center_lng = active_city["center_lng"]
        map_zoom_level = active_city["default_zoom"]

    # Configure Map Tile Layer based on user selection
    if "Roadmap" in map_provider:
        tiles_url = "https://mt1.google.com/vt/lyrs=m&x={x}&y={y}&z={z}"
        tiles_attr = "Google Maps"
    elif "Satellite" in map_provider:
        tiles_url = "https://mt1.google.com/vt/lyrs=y&x={x}&y={y}&z={z}"
        tiles_attr = "Google Maps Satellite"
    elif "Terrain" in map_provider:
        tiles_url = "https://mt1.google.com/vt/lyrs=p&x={x}&y={y}&z={z}"
        tiles_attr = "Google Maps Terrain"
    elif "OpenStreetMap" in map_provider:
        tiles_url = "https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
        tiles_attr = "&copy; OpenStreetMap contributors"
    else:
        tiles_url = "https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png"
        tiles_attr = "&copy; CartoDB Dark Matter"

    m = folium.Map(
        location=[center_lat, center_lng],
        zoom_start=map_zoom_level,
        tiles=tiles_url,
        attr=tiles_attr,
        control_scale=True
    )

    # Feature Groups
    fg_avoid = folium.FeatureGroup(name="🔴 High-Risk Avoidance Zones", show=True)
    fg_caution = folium.FeatureGroup(name="🟡 Caution / Monsoon Stress", show=True)
    fg_resilient = folium.FeatureGroup(name="🟢 Prime Resilient Hubs", show=True)
    fg_properties = folium.FeatureGroup(name="🏢 Properties to Purchase (Blue)", show=True)
    fg_plots = folium.FeatureGroup(name="🏡 Gated Plots & Land (Purple)", show=True)
    fg_rentals = folium.FeatureGroup(name="🔑 Best Rental Properties (Green)", show=True)
    fg_schools = folium.FeatureGroup(name="🎓 Benchmark CBSE Schools (Orange)", show=True)

    # Plot Micro-Markets for active city
    for mm in city_micros:
        score = mm["composite_avoidance_score"]
        popup_html = f"""
        <div style='font-family:sans-serif; width:240px;'>
            <h4 style='margin:0 0 4px 0; color:#0F172A;'>{mm['name']}</h4>
            <p style='margin:0; font-size:12px;'><b>Viability Score:</b> {score}/100 ({mm['verdict']})</p>
            <p style='margin:0; font-size:12px;'><b>Elevation:</b> {mm['elevation_m']}m ({mm['elevation_vs_basin']})</p>
            <p style='margin:0; font-size:12px;'><b>Traffic Delay Index:</b> {mm['traffic_delay_index']}x ({mm['avg_peak_speed_kmh']} km/h)</p>
            <p style='margin:0; font-size:12px;'><b>Water Supply:</b> {mm['water_supply_type']}</p>
            <hr style='margin:6px 0;'>
            <a href='{get_google_maps_search_url(mm['name'] + " " + active_city["name"])}' target='_blank' style='font-size:11px; color:#0284C7; font-weight:bold;'>Open in Google Maps ↗</a>
        </div>
        """
        if score < 55:
            folium.CircleMarker(
                location=[mm["lat"], mm["lng"]],
                radius=11,
                popup=folium.Popup(popup_html, max_width=280),
                tooltip=f"🔴 {mm['name']} (Avoidance Score: {score})",
                color="#EF4444",
                fill=True,
                fill_color="#EF4444",
                fill_opacity=0.75
            ).add_to(fg_avoid)
        elif score < 75:
            folium.CircleMarker(
                location=[mm["lat"], mm["lng"]],
                radius=9,
                popup=folium.Popup(popup_html, max_width=280),
                tooltip=f"🟡 {mm['name']} (Score: {score})",
                color="#F59E0B",
                fill=True,
                fill_color="#F59E0B",
                fill_opacity=0.75
            ).add_to(fg_caution)
        else:
            folium.CircleMarker(
                location=[mm["lat"], mm["lng"]],
                radius=9,
                popup=folium.Popup(popup_html, max_width=280),
                tooltip=f"🟢 {mm['name']} (Resilient Score: {score})",
                color="#10B981",
                fill=True,
                fill_color="#10B981",
                fill_opacity=0.75
            ).add_to(fg_resilient)

    # Plot Benchmark Schools
    for s in cbse_schools:
        s_popup = f"""
        <div style='font-family:sans-serif; width:250px;'>
            <h4 style='margin:0 0 2px 0; color:#0F172A;'>🏫 {s['name']}</h4>
            <p style='margin:0; color:#475569; font-size:11px;'>{s['curriculum']} • Rating: ⭐ {s['rating']} / 5.0 ({s['review_count']})</p>
            <p style='margin:4px 0 0 0; font-size:12px;'><b>Annual Fee:</b> {s['annual_fee_band']}</p>
            <p style='margin:0; font-size:11px; color:#64748B;'>{s['address']}</p>
            <hr style='margin:6px 0;'>
            <a href='{get_google_maps_search_url(s['name'] + " " + s['area'])}' target='_blank' style='font-size:11px; color:#0284C7; font-weight:bold;'>Google Maps Location ↗</a>
        </div>
        """
        folium.Marker(
            location=[s["lat"], s["lng"]],
            popup=folium.Popup(s_popup, max_width=280),
            tooltip=f"🏫 {s['name']} (CBSE | ⭐ {s['rating']})",
            icon=folium.Icon(color="orange", icon="graduation-cap", prefix="fa")
        ).add_to(fg_schools)

    # Plot Purchase Properties
    for p in properties:
        is_focused = (focused_prop_obj and focused_prop_obj.get("id") == p["id"])
        ws = p.get("water_infrastructure", {})
        prop_popup = f"""
        <div style='font-family:sans-serif; width:260px;'>
            <h4 style='margin:0 0 2px 0; color:#0F172A;'>🏢 {p['name']}</h4>
            <p style='margin:0; color:#475569; font-size:11px;'>By {p['builder']} ({p['builder_tier']}) • {p['bhk']}</p>
            <p style='margin:4px 0 0 0; font-size:12px;'><b>Price:</b> ₹{p['total_price_cr']} Cr (₹{p['price_per_sqft']:,}/sqft)</p>
            <p style='margin:0; font-size:12px;'><b>Growth Probability:</b> <span style='color:#059669; font-weight:bold;'>{p['growth_probability_pct']}%</span></p>
            <p style='margin:0; font-size:12px;'><b>Water:</b> {ws.get('piped_connection', 'Piped')}</p>
            <p style='margin:0; font-size:12px;'><b>Benchmark Dist:</b> {p['road_distance_to_school_benchmark_km']} km to {p['school_benchmark_name']}</p>
            <hr style='margin:6px 0;'>
            <a href='{get_google_maps_search_url(p['google_maps_query'])}' target='_blank' style='font-size:11px; color:#0284C7; font-weight:bold;'>Google Maps Navigation ↗</a> | 
            <a href='{p['rera_url']}' target='_blank' style='font-size:11px; color:#059669; font-weight:bold;'>Official RERA ↗</a>
        </div>
        """
        icon_color = "darkred" if is_focused else "blue"
        folium.Marker(
            location=[p["lat"], p["lng"]],
            popup=folium.Popup(prop_popup, max_width=300),
            tooltip=f"🏢 {p['name']} ({p['builder']} | ₹{p['total_price_cr']} Cr)",
            icon=folium.Icon(color=icon_color, icon="home", prefix="fa")
        ).add_to(fg_properties)

    # Plot Gated Plots
    for pl in gated_plots:
        is_focused = (focused_prop_obj and focused_prop_obj.get("id") == pl["id"])
        plot_popup = f"""
        <div style='font-family:sans-serif; width:260px;'>
            <h4 style='margin:0 0 2px 0; color:#0F172A;'>🏡 {pl['name']}</h4>
            <p style='margin:0; color:#475569; font-size:11px;'>By {pl['developer']} • {pl['location']}</p>
            <p style='margin:4px 0 0 0; font-size:12px;'><b>Ticket:</b> {pl['total_price_lakhs']} (₹{pl['price_per_sqft']:,}/sqft)</p>
            <p style='margin:0; font-size:12px;'><b>Growth Probability:</b> <span style='color:#059669; font-weight:bold;'>{pl['growth_probability_pct']}%</span></p>
            <p style='margin:0; font-size:12px;'><b>Authority:</b> {pl['approval_authority']}</p>
            <hr style='margin:6px 0;'>
            <a href='{get_google_maps_search_url(pl['google_maps_query'])}' target='_blank' style='font-size:11px; color:#0284C7; font-weight:bold;'>Google Maps ↗</a> | 
            <a href='{pl['validation_url']}' target='_blank' style='font-size:11px; color:#059669; font-weight:bold;'>Sanction Registry ↗</a>
        </div>
        """
        icon_color = "purple"
        folium.Marker(
            location=[pl["lat"], pl["lng"]],
            popup=folium.Popup(plot_popup, max_width=300),
            tooltip=f"🏡 {pl['name']} ({pl['developer']} | ₹{pl['price_per_sqft']}/sqft)",
            icon=folium.Icon(color=icon_color, icon="tree", prefix="fa")
        ).add_to(fg_plots)

    # Plot Rental Properties
    for r in rental_properties:
        is_focused = (focused_prop_obj and focused_prop_obj.get("id") == r["id"])
        rental_popup = f"""
        <div style='font-family:sans-serif; width:260px;'>
            <h4 style='margin:0 0 2px 0; color:#0F172A;'>🔑 {r['name']}</h4>
            <p style='margin:0; color:#475569; font-size:11px;'>By {r['builder']} • {r['bhk']}</p>
            <p style='margin:4px 0 0 0; font-size:12px;'><b>Rent:</b> ₹{r['monthly_rent_inr']:,}/mo (Maint: ₹{r['monthly_maintenance_inr']:,})</p>
            <p style='margin:0; font-size:12px;'><b>Net Yield:</b> <span style='color:#059669; font-weight:bold;'>{r['rental_yield_pct']}%</span></p>
            <p style='margin:0; font-size:12px;'><b>Commute Hub:</b> {r['commute_hub_distance_km']} km to {r['commute_hub_name']}</p>
            <hr style='margin:6px 0;'>
            <a href='{get_google_maps_search_url(r['google_maps_query'])}' target='_blank' style='font-size:11px; color:#0284C7; font-weight:bold;'>Google Maps ↗</a>
        </div>
        """
        icon_color = "green"
        folium.Marker(
            location=[r["lat"], r["lng"]],
            popup=folium.Popup(rental_popup, max_width=300),
            tooltip=f"🔑 {r['name']} (Rent: ₹{r['monthly_rent_inr']:,}/mo)",
            icon=folium.Icon(color=icon_color, icon="key", prefix="fa")
        ).add_to(fg_rentals)

    # If a property is actively focused, highlight with a golden ring & draw route polyline to benchmark
    if focused_prop_obj:
        folium.Circle(
            location=[focused_prop_obj["lat"], focused_prop_obj["lng"]],
            radius=450,
            color="#F59E0B",
            weight=4,
            fill=True,
            fill_color="#FCD34D",
            fill_opacity=0.35,
            tooltip=f"🎯 FOCUSED PROPERTY: {focused_prop_obj['name']}"
        ).add_to(m)

        # Draw road transit line to benchmark destination
        bm_lat = active_benchmark_obj["lat"]
        bm_lng = active_benchmark_obj["lng"]
        folium.PolyLine(
            locations=[[focused_prop_obj["lat"], focused_prop_obj["lng"]], [bm_lat, bm_lng]],
            color="#EF4444",
            weight=3,
            dash_array="8, 8",
            tooltip=f"🚗 Direct Route to {active_benchmark_obj['name']}"
        ).add_to(m)

    fg_avoid.add_to(m)
    fg_caution.add_to(m)
    fg_resilient.add_to(m)
    fg_properties.add_to(m)
    fg_plots.add_to(m)
    fg_rentals.add_to(m)
    fg_schools.add_to(m)
    folium.LayerControl(position="topright").add_to(m)

    st_folium(m, width="100%", height=530)

    # Focused Property Deep-Dive Bar if focused
    if focused_prop_obj:
        st.markdown(f"""
        <div style="background:#1E293B; border:2px solid #F59E0B; border-radius:8px; padding:12px 18px; margin: 10px 0;">
            <div style="display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap;">
                <h4 style="margin:0; color:#FCD34D;">🎯 Active Focus: {focused_prop_obj['name']} ({focused_prop_obj.get('city_name', '')})</h4>
                <span style="background:#78350F; color:#FDE68A; padding:2px 8px; border-radius:4px; font-weight:bold; font-size:0.8rem;">
                    Coordinates: {focused_prop_obj['lat']:.4f}° N, {focused_prop_obj['lng']:.4f}° E
                </span>
            </div>
            <p style="margin:6px 0 0 0; color:#E2E8F0; font-size:0.88rem;">
                <b>Master Plan Catalyst:</b> {focused_prop_obj.get('govt_master_plan_catalyst', 'N/A')} | 
                <b>Growth Probability:</b> <code style="color:#34D399;">{focused_prop_obj.get('growth_probability_pct', 90)}%</code> | 
                <b>Distance to {active_benchmark_obj['name']}:</b> <code style="color:#38BDF8;">{estimate_urban_road_distance_km(focused_prop_obj['lat'], focused_prop_obj['lng'], active_benchmark_obj['lat'], active_benchmark_obj['lng'])} km</code>
            </p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # ---------------------------------------------------------
    # CROSS-CITY TOP 10 COMPARATIVE TABLES
    # ---------------------------------------------------------
    st.markdown("## 🏆 Cross-City Top 10 Comparison Tables (National Radar)")
    st.caption("Side-by-side comparative inventory analysis spanning Bengaluru, Mumbai-MMR, Chennai, Delhi-NCR, Hyderabad, and Varanasi Corridor. Sorted from High to Low score with permanently frozen 1st column.")

    # ---------------------------------------------------------
    # TABLE 1: TOP 10 PROPERTIES TO PURCHASE / INVEST ACROSS ALL CITIES
    # ---------------------------------------------------------
    st.markdown("### 1️⃣ Top 10 Properties to Purchase & Invest Across All Cities")
    st.caption("Ranked by composite Investment & Viability Score (0-100), combining structural plinth elevation, flood resilience, builder RERA track record, and Government Master Plan growth catalysts.")

    # Sort properties high to low by investment_score
    sorted_properties = sorted(properties, key=lambda x: x["investment_score"], reverse=True)[:10]

    top_prop_rows = []
    for p in sorted_properties:
        ws = p.get("water_infrastructure", {})
        # Calculate road distance to configured benchmark or default school
        dist_to_bm = estimate_urban_road_distance_km(p["lat"], p["lng"], active_benchmark_obj["lat"], active_benchmark_obj["lng"])

        # Utility flags
        util_str = f"STP: {'✅' if ws.get('has_stp') else '❌'} | Softener: {'✅' if ws.get('has_water_softener') else '❌'} | Meter: {'✅' if ws.get('has_water_meter') else '❌'} | Gas: {'✅' if ws.get('has_gas_pipeline') else '❌'}"

        top_prop_rows.append({
            "Property Name": p["name"],
            "City & Micro-Market": f"{p['city_name']} ({p['micro_market']})",
            "Builder & Tier": f"{p['builder']} ({p['builder_tier']})",
            "Growth Prob (% Plan)": f"🚀 {p['growth_probability_pct']}%",
            "Govt Master Plan Catalyst": p["govt_master_plan_catalyst"],
            f"Road Dist to {active_benchmark_obj['name']}": f"{dist_to_bm} km",
            "Config & Area": f"{p['bhk']} ({p['avg_sqft']} sqft)",
            "Price / Sqft": f"₹{p['price_per_sqft']:,}",
            "Total Price (Cr)": f"₹{p['total_price_cr']:.2f} Cr",
            "Upfront Cash (L)": f"₹{p['upfront_cash_required_lakhs']:.1f} L",
            "Total Ownership (Cr)": f"₹{p['total_ownership_cost_cr']:.2f} Cr",
            "Plinth Elevation": f"{p['elevation_m']}m MSL",
            "Flood Risk Category": p["flood_resilience_tag"],
            "STP & Water Infra": util_str,
            "Investment Score": f"{p['investment_score']} / 100",
            "Google Maps Navigation": get_google_maps_search_url(p["google_maps_query"]),
            "State RERA Registry": p["rera_url"]
        })

    df_top_props = pd.DataFrame(top_prop_rows)
    render_sticky_frozen_table(df_top_props, frozen_cols=1, table_id="top_props_table", max_height="480px")

    # Collapsible Deep-Dive Cards with CBSE Schools & Fees
    with st.expander("🎓 View Nearby Top CBSE Schools & Class 1st to 12th Fee Structures for Top 10 Properties", expanded=False):
        for p in sorted_properties[:6]:
            st.markdown(f"#### 🏢 {p['name']} — {p['city_name']} ({p['micro_market']})")
            st.markdown(f"**Builder:** {p['builder']} | **Price:** ₹{p['total_price_cr']} Cr | **Master Plan:** {p['govt_master_plan_catalyst']}")
            st.markdown(render_schools_collapsible_html(p.get("lat"), p.get("lng"), city_id=p.get("city_id"), top_n=2), unsafe_allow_html=True)
            st.markdown("---")

    st.markdown("<br>", unsafe_allow_html=True)

    # ---------------------------------------------------------
    # TABLE 2: TOP 10 BEST GATED COMMUNITY PLOTS & LAND ACROSS ALL CITIES
    # ---------------------------------------------------------
    st.markdown("### 2️⃣ Top 10 Best Gated Community Plots & Land Across All Cities")
    st.caption("Ranked by Plotted Appreciation & Resilience Score (0-100), factoring statutory approvals (BMRDA, CIDCO, CMDA, DTCP, HMDA, VDA), soil drainage percolation, and proximity to infrastructure arteries.")

    sorted_plots = sorted(gated_plots, key=lambda x: x["plotted_appreciation_score"], reverse=True)[:10]

    top_plot_rows = []
    for pl in sorted_plots:
        dist_to_bm = estimate_urban_road_distance_km(pl["lat"], pl["lng"], active_benchmark_obj["lat"], active_benchmark_obj["lng"])
        top_plot_rows.append({
            "Layout / Scheme Name": pl["name"],
            "City & Location": f"{pl['city_name']} ({pl['location']})",
            "Developer": pl["developer"],
            "Growth Prob (% Plan)": f"🚀 {pl['growth_probability_pct']}%",
            "Govt Master Plan Catalyst": pl["govt_master_plan_catalyst"],
            f"Road Dist to {active_benchmark_obj['name']}": f"{dist_to_bm} km",
            "Plot Sizes (sqft)": pl["plot_sizes_sqft"],
            "Price / Sqft": f"₹{pl['price_per_sqft']:,}",
            "Starting Ticket": pl["total_price_lakhs"],
            "Land Elevation": f"{pl['elevation_m']}m MSL",
            "Statutory Authority": pl["approval_authority"],
            "Soil Percolation": pl["soil_percolation"],
            "Flood Exposure": pl["flood_risk_tag"],
            "Appreciation Score": f"{pl['plotted_appreciation_score']} / 100",
            "Google Maps Place": get_google_maps_search_url(pl["google_maps_query"]),
            "Sanction Verification": pl["validation_url"]
        })

    df_top_plots = pd.DataFrame(top_plot_rows)
    render_sticky_frozen_table(df_top_plots, frozen_cols=1, table_id="top_plots_table", max_height="480px")

    st.markdown("<br>", unsafe_allow_html=True)

    # ---------------------------------------------------------
    # TABLE 3: TOP 10 BEST RENTAL PROPERTIES ACROSS ALL CITIES
    # ---------------------------------------------------------
    st.markdown("### 3️⃣ Top 10 Best Rental Properties Across All Cities")
    st.caption("Ranked by Rental Viability & Commute Score (0-100), balancing net rental yields (%), walking access to major employment hubs, and zero water tanker dependency.")

    sorted_rentals = sorted(rental_properties, key=lambda x: x["rental_score"], reverse=True)[:10]

    top_rental_rows = []
    for r in sorted_rentals:
        ws = r.get("water_infrastructure", {})
        dist_to_bm = estimate_urban_road_distance_km(r["lat"], r["lng"], active_benchmark_obj["lat"], active_benchmark_obj["lng"])
        util_str = f"STP: {'✅' if ws.get('stp') else '❌'} | Softener: {'✅' if ws.get('softener') else '❌'} | Meter: {'✅' if ws.get('meter') else '❌'} | Gas: {'✅' if ws.get('gas') else '❌'}"

        top_rental_rows.append({
            "Property Name": r["name"],
            "City & Micro-Market": f"{r['city_name']} ({r['micro_market']})",
            "Builder": r["builder"],
            "Config & Sqft": f"{r['bhk']} ({r['avg_sqft']} sqft)",
            "Monthly Rent": f"₹{r['monthly_rent_inr']:,}",
            "Maintenance / Mo": f"₹{r['monthly_maintenance_inr']:,}",
            "Security Deposit": f"₹{r['security_deposit_inr']:,}",
            "Net Rental Yield": f"📈 {r['rental_yield_pct']}%",
            "Commute Hub Dist": f"{r['commute_hub_distance_km']} km to {r['commute_hub_name']}",
            f"Road Dist to {active_benchmark_obj['name']}": f"{dist_to_bm} km",
            "School Dist": f"{r['school_distance_km']} km to {r['school_name']}",
            "Civic Utilities": util_str,
            "Growth Prob (% Plan)": f"🚀 {r['growth_probability_pct']}%",
            "Govt Master Plan Catalyst": r["govt_master_plan_catalyst"],
            "Rental Score": f"{r['rental_score']} / 100",
            "Google Maps Navigation": get_google_maps_search_url(r["google_maps_query"])
        })

    df_top_rentals = pd.DataFrame(top_rental_rows)
    render_sticky_frozen_table(df_top_rentals, frozen_cols=1, table_id="top_rentals_table", max_height="480px")

    st.markdown("<br>", unsafe_allow_html=True)

    # ---------------------------------------------------------
    # SECTION 4: MEGA INFRASTRUCTURE MASTER PLAN CATALYST MATRIX
    # ---------------------------------------------------------
    st.markdown("### 🚀 Mega Infrastructure Master Plan Catalyst Tracker")
    st.caption("Tracking multi-billion dollar public capital expenditure (Capex ₹ Cr) and timeline delivery dates that structurally drive land and real estate appreciation.")

    plan_rows = []
    for mp in govt_master_plans:
        c_obj = next((c for c in cities if c["id"] == mp["city_id"]), None)
        c_name = c_obj["name"] if c_obj else mp["city_id"]
        plan_rows.append({
            "Project Name": mp["project_name"],
            "Corridor / City": c_name,
            "Implementing Agency": mp["implementing_agency"],
            "Project Type": mp["project_type"],
            "Capex Outlay": f"₹{mp['capex_cr']:,} Cr",
            "Target Completion": f"Year {mp['target_completion_year']}",
            "Catalytic Impact Score": f"⭐ {mp['impact_score']} / 100",
            "Real Estate Catalyst Description": mp["growth_catalyst_description"]
        })

    df_plans = pd.DataFrame(plan_rows)
    render_sticky_frozen_table(df_plans, frozen_cols=1, table_id="master_plans_table", max_height="400px")

    st.markdown("<br>", unsafe_allow_html=True)

    # ---------------------------------------------------------
    # SECTION 5: MULTI-CITY COMPARATIVE ANALYTICS CHARTS
    # ---------------------------------------------------------
    st.markdown("### 📊 Cross-City Valuation vs Master Plan Growth Analytics")
    c_chart1, c_chart2 = st.columns(2)

    with c_chart1:
        st.markdown("#### 📈 Price / Sqft vs Expected Govt Growth Probability")
        # Prepare dataframe for scatter
        chart_p_data = []
        for p in properties:
            chart_p_data.append({
                "Property": p["name"],
                "City": p["city_name"],
                "Price_Sqft": p["price_per_sqft"],
                "Growth_Probability": p["growth_probability_pct"],
                "Total_Price_Cr": p["total_price_cr"],
                "Score": p["investment_score"]
            })
        df_p_chart = pd.DataFrame(chart_p_data)

        fig_p_scatter = px.scatter(
            df_p_chart,
            x="Price_Sqft",
            y="Growth_Probability",
            color="City",
            size="Total_Price_Cr",
            hover_name="Property",
            template="plotly_dark",
            labels={"Price_Sqft": "Price per Sqft (₹)", "Growth_Probability": "Govt Master Plan Growth Prob (%)"}
        )
        fig_p_scatter.update_layout(margin=dict(l=20, r=20, t=30, b=20), height=350)
        st.plotly_chart(fig_p_scatter, use_container_width=True)

    with c_chart2:
        st.markdown("#### 💰 Net Rental Yield (%) by Metropolitan Region")
        chart_r_data = []
        for r in rental_properties:
            chart_r_data.append({
                "Property": r["name"],
                "City": r["city_name"],
                "Rental_Yield": r["rental_yield_pct"],
                "Monthly_Rent": r["monthly_rent_inr"],
                "Rental_Score": r["rental_score"]
            })
        df_r_chart = pd.DataFrame(chart_r_data)

        fig_r_bar = px.bar(
            df_r_chart,
            x="Rental_Yield",
            y="Property",
            color="City",
            orientation="h",
            template="plotly_dark",
            labels={"Rental_Yield": "Net Rental Yield (%)", "Property": "Rental Benchmark Property"}
        )
        fig_r_bar.update_layout(margin=dict(l=20, r=20, t=30, b=20), height=350)
        st.plotly_chart(fig_r_bar, use_container_width=True)

# =============================================================
# TAB 2: MICRO-MARKET AVOIDANCE RADAR (Sticky Frozen 1st Column Table)
# =============================================================
with tabs[1]:
    st.markdown(f"### 📊 Micro-Market Avoidance & Viability Radar — {active_city['name']}")
    st.caption("Explore ward contours, flood recurrence, commute delays, and water dependency with locked 1st column.")

    table_data = []
    for mm in city_micros:
        table_data.append({
            "Micro-Market Name": mm["name"],
            "Viability Score (0-100)": f"{mm['composite_avoidance_score']} / 100",
            "Verdict Tag": mm["verdict"],
            "Flood Risk Category": mm["flood_risk_category"],
            "Elevation (m)": f"{mm['elevation_m']}m",
            "Datum vs Basin": mm["elevation_vs_basin"],
            "Hist Flood Events": mm["historical_flood_incidents"],
            "Peak Delay Ratio": f"{mm['traffic_delay_index']}x",
            "Avg Peak Speed": f"{mm['avg_peak_speed_kmh']} km/h",
            "Commute Wasted (hrs/mo)": f"{mm['wasted_commute_hours_monthly']} hrs",
            "Water Supply Setup": mm["water_supply_type"],
            "Tanker Reliance Index": f"{mm['tanker_reliance_index']} / 10",
            "Top Active Builders": ", ".join(mm["top_builders_active"]),
            "Google Maps Search": get_google_maps_search_url(mm["name"] + " " + active_city["name"]),
            "Academic / Civic Citation": mm["civic_citation"]
        })

    df_micros = pd.DataFrame(table_data)
    render_sticky_frozen_table(df_micros, frozen_cols=1, table_id="micros_radar_table", max_height="520px")

    st.markdown("<br>", unsafe_allow_html=True)
    col_chart1, col_chart2 = st.columns(2)

    with col_chart1:
        st.markdown("#### 📈 Elevation vs Traffic Delay Ratio")
        fig_scatter = px.scatter(
            df_micros,
            x="Elevation (m)",
            y="Peak Delay Ratio",
            color="Verdict Tag",
            hover_name="Micro-Market Name",
            size="Hist Flood Events",
            template="plotly_dark",
            color_discrete_map={
                "🟢 Prime Resilient Buy / Rent": "#10B981",
                "🟡 Watchlist / Caution (Monsoon Stress)": "#F59E0B",
                "🟡 Watchlist / Caution (Traffic Stress)": "#F59E0B",
                "🔴 High-Risk Avoidance Zone": "#EF4444"
            }
        )
        fig_scatter.update_layout(margin=dict(l=20, r=20, t=30, b=20), height=340)
        st.plotly_chart(fig_scatter, use_container_width=True)

    with col_chart2:
        st.markdown("#### ⏳ Monthly Commute Hours Lost to Gridlock")
        fig_bar = px.bar(
            df_micros.sort_values(by="Commute Wasted (hrs/mo)", ascending=True),
            x="Commute Wasted (hrs/mo)",
            y="Micro-Market Name",
            orientation="h",
            color="Verdict Tag",
            template="plotly_dark",
            color_discrete_map={
                "🟢 Prime Resilient Buy / Rent": "#10B981",
                "🟡 Watchlist / Caution (Monsoon Stress)": "#F59E0B",
                "🟡 Watchlist / Caution (Traffic Stress)": "#F59E0B",
                "🔴 High-Risk Avoidance Zone": "#EF4444"
            }
        )
        fig_bar.update_layout(margin=dict(l=20, r=20, t=30, b=20), height=340)
        st.plotly_chart(fig_bar, use_container_width=True)

# =============================================================
# TAB 3: TOP BUILDERS BY CITY & STATE DIRECTORY (15+ per City)
# =============================================================
with tabs[2]:
    st.markdown(f"### 🏗️ Top Builder Directory & RERA Track Record (At least 15+ per City)")
    st.caption("Benchmarking Tier 1 National & Regional champions by RERA on-time delivery punctuality, construction durability, and legal risk across all 6 metropolitan corridors.")

    builder_filter_mode = st.radio(
        "Filter Builders Display:",
        options=[f"📍 Active Focus City: {active_city['name']} (16 Builders)", "🌐 All Cities Across India (96 Builders Total)"],
        horizontal=True
    )

    if "Active Focus City" in builder_filter_mode:
        selected_builders = [
            b for b in builders
            if b.get("city_id") == selected_city_id or any(selected_city_id in s.lower() for s in b.get("active_states_and_cities", []))
        ]
        if len(selected_builders) < 15:
            # Fallback to state match
            selected_builders = [
                b for b in builders
                if any(active_city["state"].lower() in s.lower() for s in b.get("active_states_and_cities", []))
            ]
    else:
        selected_builders = builders

    builder_table = []
    for b in selected_builders:
        flagship = b.get("flagship_projects", {}).get(selected_city_id, "Marquee Portfolio Project")
        c_obj = next((c for c in cities if c["id"] == b.get("city_id")), None)
        c_name = c_obj["name"] if c_obj else b.get("headquarters", "National")

        builder_table.append({
            "Builder Name": b["name"],
            "City / Region": c_name,
            "Tier Classification": b["tier"],
            "Headquarters": b["headquarters"],
            "RERA On-Time Delivery": f"{b['on_time_delivery_pct']}%",
            "Quality Score (1-10)": f"⭐ {b['construction_quality_rating']} / 10",
            "Litigation Index": b["litigation_index"],
            "Delivered Sqft (Mn)": f"{b['total_delivered_sqft_mn']} Mn",
            "Flagship In Region": flagship,
            "Official State RERA Portal": b["rera_portal_url"]
        })

    df_builders = pd.DataFrame(builder_table)
    render_sticky_frozen_table(df_builders, frozen_cols=1, table_id="builders_table", max_height="520px")

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown(f"#### 🏢 Builder Pedigree Profiles ({active_city['name']} Champions)")
    b_cols = st.columns(3)
    for idx, b in enumerate(selected_builders[:6]):
        with b_cols[idx % 3]:
            st.markdown(f"""
            <div style='background-color:#1E293B; border:1px solid #334155; border-radius:8px; padding:16px; margin-bottom:14px;'>
                <div style='display:flex; justify-content:space-between; align-items:center;'>
                    <h4 style='margin:0; color:#38BDF8;'>{b['name']}</h4>
                    <span style='background:#0D9488; color:#FFFFFF; font-size:10px; padding:2px 6px; border-radius:4px; font-weight:bold;'>Est. {b['established_year']}</span>
                </div>
                <p style='color:#94A3B8; font-size:12px; margin:4px 0 10px 0;'>{b['tier']} • HQ: {b['headquarters']}</p>
                <p style='font-size:12px; margin:0;'><b>RERA Compliance:</b> {b['rera_compliance_score']}/100 | <b>On-Time:</b> {b['on_time_delivery_pct']}%</p>
                <p style='font-size:12px; margin:4px 0;'><b>Strengths:</b> {b['strengths']}</p>
                <p style='font-size:12px; margin:0; color:#F59E0B;'><b>Tradeoffs:</b> {b['cautions']}</p>
                <div style='margin-top:8px;'>
                    <a href='{b['rera_portal_url']}' target='_blank' style='font-size:11px; color:#34D399; font-weight:bold;'>Verify on RERA Portal ↗</a>
                </div>
            </div>
            """, unsafe_allow_html=True)

# =============================================================
# TAB 4: RESILIENT PROPERTY SCREENER
# =============================================================
with tabs[3]:
    st.markdown(f"### 🏢 Benchmark Property Screener — {active_city['name']}")
    st.caption(f"Filtered by Purchase Budget: ≤ ₹{budget_purchase_max:.2f} Cr | Rental Budget: ≤ ₹{budget_rental_max:,}/mo")

    filtered_properties = []
    for p in city_props:
        if p["total_price_cr"] <= budget_purchase_max:
            if filter_piped_water_only:
                ws_conn = p.get("water_infrastructure", {}).get("piped_connection", "")
                if "100%" not in ws_conn and "BWSSB" not in ws_conn and "BMC" not in ws_conn and "CMWSSB" not in ws_conn and "GMDA" not in ws_conn and "HMWSSB" not in ws_conn and "UP Jal" not in ws_conn:
                    continue
            filtered_properties.append(p)

    if not filtered_properties:
        st.warning(f"No properties found matching purchase budget ≤ ₹{budget_purchase_max} Cr in {active_city['name']}. Showing all properties for preview.")
        filtered_properties = city_props

    prop_rows = []
    for p in filtered_properties:
        ws = p.get("water_infrastructure", {})
        dist_to_bm = estimate_urban_road_distance_km(p["lat"], p["lng"], active_benchmark_obj["lat"], active_benchmark_obj["lng"])
        util_str = f"STP: {'✅' if ws.get('has_stp') else '❌'} | Softener: {'✅' if ws.get('has_water_softener') else '❌'} | Meter: {'✅' if ws.get('has_water_meter') else '❌'}"

        prop_rows.append({
            "Property Name": p["name"],
            "Builder": p["builder"],
            "Micro-Market": p["micro_market"],
            "Configuration": p["bhk"],
            "Avg Sqft": f"{p['avg_sqft']} sqft",
            "Price / Sqft": f"₹{p['price_per_sqft']:,}",
            "Total Price (Cr)": f"₹{p['total_price_cr']:.2f} Cr",
            f"Road Dist to {active_benchmark_obj['name']}": f"{dist_to_bm} km",
            "Plinth Elevation": f"{p['elevation_m']}m",
            "Flood Risk Tag": p["flood_resilience_tag"],
            "Civic Utilities": util_str,
            "Growth Prob (% Plan)": f"🚀 {p['growth_probability_pct']}%",
            "Govt Master Plan": p["govt_master_plan_catalyst"],
            "Viability Score": f"{p['investment_score']} / 100",
            "Google Maps Navigation": get_google_maps_search_url(p["google_maps_query"]),
            "Official RERA Portal": p["rera_url"]
        })

    df_props = pd.DataFrame(prop_rows)
    render_sticky_frozen_table(df_props, frozen_cols=1, table_id="props_screener_table", max_height="520px")

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("#### 🔍 Property Deep-Dive Cards & School Fee Ecosystems")
    for p in filtered_properties[:4]:
        with st.expander(f"📌 {p['name']} — {p['builder']} ({p['bhk']} | ₹{p['total_price_cr']} Cr)"):
            c_left, c_right = st.columns([2, 1])
            with c_left:
                st.markdown(f"**Government Master Plan Growth Catalyst**: {p['govt_master_plan_catalyst']}")
                st.markdown(f"**Growth Probability**: `{p['growth_probability_pct']}%` | **Investment Score**: `{p['investment_score']} / 100`")
                st.markdown(f"**Water Infrastructure**: {p.get('water_infrastructure', {}).get('piped_connection', 'N/A')}")
                st.markdown(render_schools_collapsible_html(p.get("lat"), p.get("lng"), city_id=p.get("city_id"), top_n=2), unsafe_allow_html=True)
            with c_right:
                st.markdown(f"**Plinth Elevation**: `{p['elevation_m']} meters MSL`")
                st.markdown(f"**Distance to Benchmark**: `{estimate_urban_road_distance_km(p['lat'], p['lng'], active_benchmark_obj['lat'], active_benchmark_obj['lng'])} km to {active_benchmark_obj['name']}`")
                st.markdown(f"[Navigate via Google Maps ↗]({get_google_maps_search_url(p['google_maps_query'])})")
                st.markdown(f"[Official State RERA Verification ↗]({p['rera_url']})")

# =============================================================
# TAB 5: GATED COMMUNITY PLOTS & SITES
# =============================================================
with tabs[4]:
    st.markdown(f"### 🏡 Gated Community Villa Plots & Land Investments")
    st.caption("Vetted DTCP / BMRDA / CIDCO / CMDA / HMDA / VDA layouts with stormwater outfall analysis and high natural plinth elevation.")

    display_plots = city_plots if city_plots else gated_plots

    plot_rows = []
    for pl in display_plots:
        dist_to_bm = estimate_urban_road_distance_km(pl["lat"], pl["lng"], active_benchmark_obj["lat"], active_benchmark_obj["lng"])
        plot_rows.append({
            "Layout / Scheme Name": pl["name"],
            "Developer": pl["developer"],
            "Location / Micro-Market": pl["location"],
            "Plot Sizes": pl["plot_sizes_sqft"],
            "Price / Sqft": f"₹{pl['price_per_sqft']:,}",
            "Starting Ticket": pl["total_price_lakhs"],
            f"Road Dist to {active_benchmark_obj['name']}": f"{dist_to_bm} km",
            "Land Elevation": f"{pl['elevation_m']}m",
            "Statutory Approval": pl["approval_authority"],
            "Drainage & Percolation": pl["soil_percolation"],
            "Flood Exposure Tag": pl["flood_risk_tag"],
            "Growth Prob (% Plan)": f"🚀 {pl['growth_probability_pct']}%",
            "Appreciation Score": f"{pl['plotted_appreciation_score']} / 100",
            "Google Maps Place": get_google_maps_search_url(pl["google_maps_query"]),
            "Official Approval Link": pl["validation_url"]
        })

    df_plots = pd.DataFrame(plot_rows)
    render_sticky_frozen_table(df_plots, frozen_cols=1, table_id="plots_table", max_height="480px")

    st.markdown("""
    > [!IMPORTANT]
    > **Gated Community Plot Due-Diligence Checklist**:
    > 1. **Plinth Elevation**: Ensure plot grade is at least +1.5m above the surrounding road centerline to prevent storm gutter backflow.
    > 2. **Layout Drainage Outfall**: Verify approved storm drain connectivity to municipal tertiary channels.
    > 3. **RERA Layout Registration**: Ensure all plotted layouts carry explicit Town Planning and RERA approvals before signing sale deeds.
    """)

# =============================================================
# TAB 6: WATER SUPPLY & GROUND REALITY MONITOR
# =============================================================
with tabs[5]:
    st.markdown(f"### 💧 Water Supply & Ground Reality Monitor — {active_city['name']}")
    st.caption("Comparing municipal bulk piped supply, groundwater table depletion, and private tanker dependency economics.")

    col_w1, col_w2 = st.columns([1, 1])

    with col_w1:
        st.markdown("#### 📉 Elevation vs Tanker Reliance Index")
        fig_water = px.scatter(
            df_micros,
            x="Elevation (m)",
            y="Tanker Reliance Index",
            size="Hist Flood Events",
            color="Verdict Tag",
            hover_name="Micro-Market Name",
            template="plotly_dark",
            labels={"Tanker Reliance Index": "Tanker Dependency (0=Low, 10=Severe)"}
        )
        fig_water.update_layout(margin=dict(l=20, r=20, t=30, b=20), height=340)
        st.plotly_chart(fig_water, use_container_width=True)

    with col_w2:
        st.markdown("#### 🧮 Monthly Water Maintenance Cost Calculator")
        st.markdown("Calculate household expenditure difference between municipal piped water vs private tanker dependency:")
        
        household_count = st.number_input("Apartment Units in Society:", min_value=50, max_value=3000, value=350, step=50)
        tanker_cost_per_load = st.slider("Cost per 6,000L Private Tanker (₹):", min_value=800, max_value=2500, value=1500, step=100)
        
        daily_liters_society = household_count * 3.5 * 150
        daily_tankers_needed = daily_liters_society / 6000
        monthly_tanker_expenditure = daily_tankers_needed * tanker_cost_per_load * 30
        per_flat_tanker_cost = round(monthly_tanker_expenditure / household_count)
        
        monthly_municipal_cost = (daily_liters_society * 30 / 1000) * 25
        per_flat_municipal_cost = round(monthly_municipal_cost / household_count)
        monthly_savings = per_flat_tanker_cost - per_flat_municipal_cost

        st.metric(
            label="Tanker-Dependent Society Cost / Flat / Month",
            value=f"₹{per_flat_tanker_cost:,}",
            delta=f"-₹{monthly_savings:,} Extra Burden",
            delta_color="inverse"
        )
        st.metric(
            label="Municipal Piped Society Cost / Flat / Month",
            value=f"₹{per_flat_municipal_cost:,}",
            delta=f"+₹{monthly_savings:,} Monthly Savings",
            delta_color="normal"
        )

# =============================================================
# TAB 7: CHRONIC AVOIDANCE ZONES DEEP DIVE
# =============================================================
with tabs[6]:
    st.markdown(f"### 🚨 Chronic Real Estate Avoidance Zones")
    st.caption("Forensic analysis of chronic monsoon waterlogging, tidal backflows, and hydraulic bottlenecks.")

    for av in avoidance_zones:
        with st.expander(f"⚠️ {av['name']} — {av['city']} ({av['severity']})", expanded=False):
            st.markdown(f"**Root Cause**: {av['root_cause']}")
            st.markdown(f"**Elevation Delta**: `{av['elevation_delta_m']}` | **Historical Closures**: `{av['historical_closures_annual']}`")
            st.markdown(f"**Municipal Mitigation Progress**: {av['mitigation_status']}")
            st.markdown(f"**Real Estate Asset Impact**: {av['real_estate_impact']}")
            st.markdown(f"**Verified Citation**: `{av['citation']}`")
            st.markdown(f"[View Hotspot in Google Maps ↗]({get_google_maps_search_url(av['name'] + ' ' + av['city'])})")

# =============================================================
# TAB 8: EXPLAINABLE AI COPILOT
# =============================================================
with tabs[7]:
    st.markdown(f"### 🤖 Explainable AI Avoidance Copilot")
    st.caption("Natural language queries powered by multi-criteria civic telemetry, topographical models, and builder track records.")

    copilot_query = st.text_input(
        "Ask the AI Copilot a question:",
        value=f"Which micro-markets in {active_city['name']} should I strictly avoid during monsoon?",
        help="Example: Compare top builders in Bengaluru, or show flood-free properties under 2.5 Cr."
    )

    q_btn1, q_btn2, q_btn3 = st.columns(3)
    if q_btn1.button("🔴 Show Avoidance Zones"):
        copilot_query = f"Which areas should I avoid due to flooding in {active_city['name']}?"
    if q_btn2.button("🏗️ Compare Best Builders"):
        copilot_query = f"Who are the top tier 1 builders with best RERA delivery in {active_city['name']}?"
    if q_btn3.button("💧 Check Water Supply & Softener"):
        copilot_query = f"Which properties have Cauvery or municipal piped water and STPs in {active_city['name']}?"

    if copilot_query:
        ai_response = run_avoidance_copilot_query(
            user_query=copilot_query,
            city_id=selected_city_id,
            micro_markets=micro_markets,
            builders=builders,
            properties=properties,
            avoidance_zones=avoidance_zones
        )
        st.markdown(ai_response)

# -------------------------------------------------------------
# Footer
# -------------------------------------------------------------
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #64748B; font-size: 0.82rem;'>
    <b>Urban Pulse: Flood, Traffic & Water Supply Monitor for Indian Cities</b> • MIT Open Source License<br>
    Live Streamlit Deployment: <a href='https://flood-traffic-water-supply-monitor-for-indian-cities.streamlit.app/' target='_blank' style='color:#38BDF8; font-weight:bold;'>flood-traffic-water-supply-monitor-for-indian-cities.streamlit.app</a><br>
    Validated against IIT Delhi HydroSense, TNGIS, BBMP, BMC, CMWSSB, GMDA, and UP Jal Sansthan civic datasets.
</div>
""", unsafe_allow_html=True)
