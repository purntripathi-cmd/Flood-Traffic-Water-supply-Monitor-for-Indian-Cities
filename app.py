"""
🌊 Urban Pulse: Flood, Traffic & Water Supply Monitor for Indian Cities
Comprehensive Civic Intelligence & Real Estate Avoidance Screener across 6 Metropolitan Corridors:
1. Bengaluru (Karnataka)
2. Mumbai & MMR (Maharashtra)
3. Chennai (Tamil Nadu)
4. Delhi-NCR (Delhi / Haryana / UP)
5. Hyderabad (Telangana)
6. Varanasi & Eastern UP 100km Corridor (Varanasi, Prayagraj, Mirzapur, Jaunpur, Chandauli)

Integrates:
- Topographical flood vulnerability & historical flood event inventories (IIT Delhi HydroSense / SRTM DEM / TNGIS)
- Traffic delay ratios & commuter wasted hours (TomTom / Google Routes / Open-Source traffic models)
- Municipal water supply coverage, groundwater table depth, and tanker dependency index
- Top Tier-1 builders by city and state with verified RERA compliance and on-time delivery track records
- Sticky 1st-column frozen tables for 100% responsive cross-platform exploration
- Explainable AI Avoidance Copilot with citation backing
"""

import json
import os
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
        font-size: 2.2rem;
        font-weight: 800;
        background: linear-gradient(90deg, #38BDF8 0%, #0D9488 50%, #34D399 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.2rem;
    }
    .sub-title {
        color: #94A3B8;
        font-size: 0.95rem;
        margin-bottom: 1.2rem;
    }
    .kpi-card {
        background-color: #1E293B;
        border: 1px solid #334155;
        border-radius: 8px;
        padding: 14px 18px;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.2);
    }
    .kpi-title {
        font-size: 0.78rem;
        text-transform: uppercase;
        color: #94A3B8;
        font-weight: 700;
        letter-spacing: 0.05em;
    }
    .kpi-value {
        font-size: 1.45rem;
        font-weight: 800;
        color: #F8FAFC;
        margin-top: 4px;
    }
    .kpi-sub {
        font-size: 0.78rem;
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
    with open(os.path.join(DATA_DIR, "gated_plots.json"), "r", encoding="utf-8") as f:
        gated_plots = json.load(f)
    with open(os.path.join(DATA_DIR, "avoidance_zones.json"), "r", encoding="utf-8") as f:
        avoidance_zones = json.load(f)
    with open(os.path.join(DATA_DIR, "user_preferences.json"), "r", encoding="utf-8") as f:
        user_preferences = json.load(f)
    return cities, micro_markets, builders, properties, gated_plots, avoidance_zones, user_preferences


cities, micro_markets, builders, properties, gated_plots, avoidance_zones, user_preferences = load_all_datasets()

# -------------------------------------------------------------
# Sidebar Controls & Configurable Filters
# -------------------------------------------------------------
st.sidebar.image("https://images.unsplash.com/photo-1542314831-068cd1dbfeeb?w=500&auto=format&fit=crop&q=60", use_column_width=True)
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

st.sidebar.markdown("---")
st.sidebar.markdown("### 📚 Open-Source Citation Standards")
st.sidebar.caption("""
- **Urban Flood Mapping**: RushilGargash08 (MLP / Topography)
- **IIT Delhi HydroSense**: India Flood Inventory GeoJSON
- **Bengaluru Waterlog**: diagram-chasing/blr-water-log
- **Traffic Wasted Time**: parthtiwari-dev Congestion Engine
- **India Geodata**: yashveeeeeeer GIS ward contours
- **IIT Gandhinagar**: India Flood Atlas (1901-2020)
""")

# -------------------------------------------------------------
# Main Header & Executive KPI Metrics
# -------------------------------------------------------------
st.markdown("<div class='main-title'>🌊 Urban Pulse: Flood, Traffic & Water Supply Monitor</div>", unsafe_allow_html=True)
st.markdown(
    f"<div class='sub-title'>Civic Resilience Screener & Real Estate Avoidance Radar for <b>{active_city['name']} ({active_city['state']})</b></div>",
    unsafe_allow_html=True
)

# Filter Data for Active City
city_micros = [m for m in micro_markets if m["city_id"] == selected_city_id]
city_props = [p for p in properties if p["city_id"] == selected_city_id]
city_plots = [pl for pl in gated_plots if pl["city_id"] == selected_city_id]
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
    "🗺️ Geospatial Risk & Avoidance Map",
    "📊 Micro-Market Avoidance Radar",
    "🏗️ Top Builders by City & State",
    "🏢 Resilient Property Screener",
    "🏡 Gated Community Plots & Sites",
    "💧 Water Supply & Ground Reality",
    "🚨 Chronic Avoidance Zones Deep Dive",
    "🤖 Explainable AI Copilot"
])

# =============================================================
# TAB 1: GEOSPATIAL RISK & AVOIDANCE MAP
# =============================================================
with tabs[0]:
    st.markdown(f"### 🗺️ Multi-Layer Geospatial Avoidance Map — {active_city['name']}")
    st.caption("Visualizing elevation contours, lakebed floodplains, traffic bottlenecks, and curated residential projects.")

    m = folium.Map(
        location=[active_city["center_lat"], active_city["center_lng"]],
        zoom_start=active_city["default_zoom"],
        tiles="CartoDB dark_matter",
        control_scale=True
    )

    # Feature Groups
    fg_avoid = folium.FeatureGroup(name="🔴 High-Risk Avoidance Zones", show=True)
    fg_caution = folium.FeatureGroup(name="🟡 Caution / Monsoon Stress", show=True)
    fg_resilient = folium.FeatureGroup(name="🟢 Prime Resilient Hubs", show=True)
    fg_properties = folium.FeatureGroup(name="🏢 Curated Benchmark Properties", show=True)

    # Plot Micro-Markets
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
            <a href='{get_google_maps_search_url(mm['name'] + ' ' + active_city['name'])}' target='_blank' style='font-size:11px; color:#0284C7; font-weight:bold;'>Open in Google Maps ↗</a>
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

    # Plot Properties
    for p in city_props:
        prop_popup = f"""
        <div style='font-family:sans-serif; width:250px;'>
            <h4 style='margin:0 0 2px 0; color:#0F172A;'>{p['name']}</h4>
            <p style='margin:0; color:#475569; font-size:11px;'>By {p['builder_name']} • {p['bhk']}</p>
            <p style='margin:4px 0 0 0; font-size:12px;'><b>Price:</b> ₹{p['total_price_cr']} Cr (₹{p['price_per_sqft']}/sqft)</p>
            <p style='margin:0; font-size:12px;'><b>Rent:</b> ₹{p['monthly_rent_inr']:,}/mo</p>
            <p style='margin:0; font-size:12px;'><b>Water:</b> {p['water_supply']['piped_connection']}</p>
            <hr style='margin:6px 0;'>
            <a href='{get_google_maps_search_url(p['google_maps_query'])}' target='_blank' style='font-size:11px; color:#0284C7; font-weight:bold;'>Google Maps Navigation ↗</a> | 
            <a href='{p['validation_url']}' target='_blank' style='font-size:11px; color:#059669; font-weight:bold;'>Official RERA ↗</a>
        </div>
        """
        folium.Marker(
            location=[p["lat"], p["lng"]],
            popup=folium.Popup(prop_popup, max_width=300),
            tooltip=f"🏢 {p['name']} ({p['builder_name']})",
            icon=folium.Icon(color="blue", icon="home", prefix="fa")
        ).add_to(fg_properties)

    fg_avoid.add_to(m)
    fg_caution.add_to(m)
    fg_resilient.add_to(m)
    fg_properties.add_to(m)
    folium.LayerControl().add_to(m)

    st_folium(m, width="100%", height=520)

    st.markdown("""
    > [!TIP]
    > **Legend**:
    > - 🟢 **Green Circles**: Prime Resilient Micro-Markets (High plinth, low flood recurrence, resilient infrastructure).
    > - 🟡 **Yellow Circles**: Caution / Watchlist (Traffic bottlenecks or seasonal monsoon surface stagnation).
    > - 🔴 **Red Circles**: Chronic Avoidance Zones (Low-lying lakebed, subway depression, river backwater inundation).
    > - 🏢 **Blue Pins**: Curated benchmark properties from top-tier builders with verified RERA documentation.
    """)

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
    
    # Render sticky table with 1st column permanently frozen
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
# TAB 3: TOP BUILDERS BY CITY & STATE DIRECTORY
# =============================================================
with tabs[2]:
    st.markdown(f"### 🏗️ Top Builder Directory & RERA Track Record")
    st.caption("Benchmark Tier 1 National & Regional builders by RERA delivery punctuality, construction durability, and legal risk.")

    # Filter builders present in this region/state
    relevant_builders = [
        b for b in builders
        if any(active_city["state"].lower() in s.lower() or active_city["id"].lower() in s.lower() for s in b["active_states_and_cities"])
    ]
    if not relevant_builders:
        relevant_builders = builders

    builder_table = []
    for b in relevant_builders:
        flagship = b["flagship_projects"].get(selected_city_id, "National Marquee Portfolio")
        builder_table.append({
            "Builder Name": b["name"],
            "Tier Classification": b["tier"],
            "Headquarters": b["headquarters"],
            "RERA On-Time Delivery": f"{b['on_time_delivery_pct']}%",
            "Quality Score (1-10)": f"⭐ {b['construction_quality_rating']} / 10",
            "Litigation Index": b["litigation_index"],
            "Delivered Sqft (Mn)": f"{b['total_delivered_sqft_mn']} Mn",
            "Flagship In Region": flagship,
            "Official RERA Registry": b["rera_portal_url"]
        })

    df_builders = pd.DataFrame(builder_table)
    render_sticky_frozen_table(df_builders, frozen_cols=1, table_id="builders_table", max_height="480px")

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("#### 🏢 Builder Pedigree Comparison Cards")
    b_cols = st.columns(3)
    for idx, b in enumerate(relevant_builders[:6]):
        with b_cols[idx % 3]:
            st.markdown(f"""
            <div style='background-color:#1E293B; border:1px solid #334155; border-radius:8px; padding:16px; margin-bottom:14px;'>
                <div style='display:flex; justify-content:space-between; align-items:center;'>
                    <h4 style='margin:0; color:#38BDF8;'>{b['name']}</h4>
                    <span style='background:#0D9488; color:#FFFFFF; font-size:10px; padding:2px 6px; border-radius:4px; font-weight:bold;'>{b['established_year']}</span>
                </div>
                <p style='color:#94A3B8; font-size:12px; margin:4px 0 10px 0;'>{b['tier']} • HQ: {b['headquarters']}</p>
                <p style='font-size:12px; margin:0;'><b>RERA Compliance:</b> {b['rera_compliance_score']}/100 | <b>On-Time:</b> {b['on_time_delivery_pct']}%</p>
                <p style='font-size:12px; margin:4px 0;'><b>Strengths:</b> {b['strengths']}</p>
                <p style='font-size:12px; margin:0; color:#F59E0B;'><b>Tradeoffs:</b> {b['cautions']}</p>
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
        if p["total_price_cr"] <= budget_purchase_max and p["monthly_rent_inr"] <= budget_rental_max:
            if filter_piped_water_only:
                if "100%" not in p["water_supply"]["piped_connection"] and "BWSSB" not in p["water_supply"]["piped_connection"] and "BMC" not in p["water_supply"]["piped_connection"]:
                    continue
            filtered_properties.append(p)

    if not filtered_properties:
        st.warning(f"No properties found matching purchase budget ≤ ₹{budget_purchase_max} Cr and rent ≤ ₹{budget_rental_max:,}/mo in {active_city['name']}. Try adjusting the sidebar filters.")
        filtered_properties = city_props  # fallback preview

    prop_rows = []
    for p in filtered_properties:
        ws = p["water_supply"]
        prop_rows.append({
            "Property Name": p["name"],
            "Builder": p["builder_name"],
            "Micro-Market": p["micro_market_name"],
            "Configuration": p["bhk"],
            "Avg Sqft": f"{p['avg_sqft']} sqft",
            "Price / Sqft": f"₹{p['price_per_sqft']:,}",
            "Total Price (Cr)": f"₹{p['total_price_cr']:.2f} Cr",
            "Monthly Rent": f"₹{p['monthly_rent_inr']:,}",
            "Maintenance / Mo": f"₹{p['monthly_maintenance_inr']:,}",
            "Elevation Datum": f"{p['elevation_m']}m",
            "Flood Risk Tag": p["flood_risk_tag"],
            "Piped Water Source": ws.get("piped_connection", "N/A"),
            "STP & Dual Piping": ws.get("stp_treatment", "N/A"),
            "Water Softener": ws.get("water_softener", "N/A"),
            "Viability Index": f"{p['avoidance_index']} / 100",
            "Google Maps Navigation": get_google_maps_search_url(p["google_maps_query"]),
            "Official RERA Portal": p["validation_url"]
        })

    df_props = pd.DataFrame(prop_rows)
    render_sticky_frozen_table(df_props, frozen_cols=1, table_id="props_screener_table", max_height="520px")

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("#### 🔍 Property Deep-Dive Cards")
    for p in filtered_properties[:4]:
        with st.expander(f"📌 {p['name']} — {p['builder_name']} ({p['bhk']} | ₹{p['total_price_cr']} Cr)"):
            c_left, c_right = st.columns([2, 1])
            with c_left:
                st.markdown(f"**Key Highlights**: {p['key_highlights']}")
                st.markdown(f"**Tradeoffs & Constraints**: {p['tradeoffs']}")
                st.markdown(f"**Water Infrastructure**: {p['water_supply']['piped_connection']} • {p['water_supply']['stp_treatment']} • Softener: {p['water_supply']['water_softener']}")
            with c_right:
                st.markdown(f"**Plinth Elevation**: `{p['elevation_m']} meters`")
                st.markdown(f"**Peak Commute Delay to Hub**: `{p['traffic_delay_to_hub_mins']} mins`")
                st.markdown(f"[Navigate via Google Maps ↗]({get_google_maps_search_url(p['google_maps_query'])})")
                st.markdown(f"[Official State RERA Verification ↗]({p['validation_url']})")

# =============================================================
# TAB 5: GATED COMMUNITY PLOTS & SITES
# =============================================================
with tabs[4]:
    st.markdown(f"### 🏡 Gated Community Villa Plots & Land Investments")
    st.caption("Addressing demand for gated community land: vetted DTCP / BDA / HMDA / VDA / PDA / MahaRERA layouts with stormwater outfall analysis.")

    if not city_plots:
        st.info(f"Displaying national benchmark plotted developments from top builders across India.")
        display_plots = gated_plots
    else:
        display_plots = city_plots

    plot_rows = []
    for pl in display_plots:
        plot_rows.append({
            "Layout / Scheme Name": pl["name"],
            "Developer": pl["builder_name"],
            "Location / Micro-Market": pl["location"],
            "Plot Sizes": pl["plot_sizes_sqft"],
            "Price / Sqft": f"₹{pl['price_per_sqft']:,}",
            "Starting Ticket": f"₹{pl['total_price_lakhs']} Lakhs",
            "Land Elevation": f"{pl['elevation_m']}m",
            "Statutory Approval": pl["approval_authority"],
            "Drainage & Percolation": pl["drainage_percolation"],
            "Flood Exposure Tag": pl["flood_risk_tag"],
            "Resilience Score": f"{pl['avoidance_score']} / 100",
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
        st.markdown("#### 📉 Groundwater Depth vs Water Hardness (TDS)")
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
        
        # Calculations: 150 liters per capita per day, 3.5 persons per flat
        daily_liters_society = household_count * 3.5 * 150
        daily_tankers_needed = daily_liters_society / 6000
        monthly_tanker_expenditure = daily_tankers_needed * tanker_cost_per_load * 30
        per_flat_tanker_cost = round(monthly_tanker_expenditure / household_count)
        
        # Municipal piped water cost is approx ₹25 per 1,000L
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
    st.caption("Deep-dive forensic analysis of chronic monsoon waterlogging, tidal backflows, and hydraulic bottlenecks.")

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
    Validated against IIT Delhi HydroSense, TNGIS, BBMP, BMC, CMWSSB, GMDA, and UP Jal Sansthan civic datasets.
</div>
""", unsafe_allow_html=True)
