# 🏢 Property Screener with Flood, Traffic & Water Supply Details

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://flood-traffic-water-supply-monitor-for-indian-cities.streamlit.app/)
[![Live App URL](https://img.shields.io/badge/Live%20App-flood--traffic--water--supply--monitor--for--indian--cities.streamlit.app-38BDF8.svg)](https://flood-traffic-water-supply-monitor-for-indian-cities.streamlit.app/)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-teal.svg)](https://opensource.org/licenses/MIT)
[![Civic Intelligence](https://img.shields.io/badge/Civic-Intelligence%20Radar-emerald.svg)](#)

> **Live Streamlit App**: [https://flood-traffic-water-supply-monitor-for-indian-cities.streamlit.app/](https://flood-traffic-water-supply-monitor-for-indian-cities.streamlit.app/)

A **High-Fidelity Civic Infrastructure & Real Estate Avoidance Screener** across 6 major Indian metropolitan corridors: **Bengaluru**, **Mumbai & MMR**, **Chennai**, **Delhi-NCR**, **Hyderabad**, and **Varanasi & Eastern UP 100km Corridor** (Varanasi, Prayagraj, Mirzapur, Jaunpur, Chandauli).

Synthesizes open-source civic flood-mapping models, traffic congestion predictors, water table telemetry, and municipal GIS datasets to identify **resilient havens** and steer home buyers, renters, and developers away from **chronic infrastructure avoidance zones**.

---

## 📌 Architecture & Reference Models

This platform brings together civic research datasets, remote sensing imagery, and predictive machine learning architectures:

| Domain | Open-Source Reference & Dataset | Purpose |
| :--- | :--- | :--- |
| **Urban Flood Risk & Vulnerability** | [Urban-Flood-Risk-Mapping-and-Detection](https://github.com/RushilGargash08/Urban-Flood-Risk-Mapping-and-Detection) | Random Forest & Multi-Layer Perceptron (MLP) topographical models calibrated for Indian metro basins (Velachery & Greater Bengaluru). |
| **Historical Inundation Logs** | [India Flood Inventory](https://github.com/hydrosenselab/India-Flood-Inventory) (IIT Delhi HydroSense Lab) | Multi-source geospatial GeoJSON inventory of Indian urban flood events. |
| **Hyperlocal Drainage Modeling** | [Chennai Flood Risk Model](https://www.linkedin.com/posts/samueljebakumar_github-shmuel07chennai-flood-risk-zone-level-activity-7471501228355538944-_mPG) | SRTM 30m Digital Elevation Models (DEM) and TNGIS drainage susceptibility datasets. |
| **Road Surface Water Accumulation** | [blr-water-log](https://github.com/diagram-chasing/blr-water-log) | Stormwater accumulation and ward-level road submergence patterns across Bengaluru. |
| **River Basin Gauging & Floodplains** | [Predict River Disaster - Ganga River](https://github.com/Devesh-Singh-Gouni) & [India Flood Atlas](https://github.com/wcl-iitgn/india-flood-atlas-data) | Ganga, Yamuna, Varuna, and Gomti danger marks, gauge stations, and historical inundation series (1901-2020) for Eastern UP. |
| **Traffic Delay & Commute Loss** | [Bangalore Traffic Wasted Time Prediction](https://github.com/parthtiwari-dev/bangalore-traffic-wasted-time-prediction) | Peak commute delay ratios ($\text{Peak Travel Time} \div \text{Free-Flow Time}$) and monthly hours lost to traffic bottlenecks. |
| **Multi-City Traffic Time-Series** | [Real-Time Traffic Analysis](https://github.com/Shashwat-19/Real-Time-Traffic-Analysis) & [Bengaluru Traffic Optimization](https://github.com/Bhupendra-DS/bengaluru-traffic-optimization) | Bottleneck classification across arterial corridors (WEH, EEH, ORR, OMR, Ring Road). |
| **SAR Remote Sensing & Elevation** | [Hugging Face Datasets: harshinde/sen1floods](https://huggingface.co/datasets/harshinde/sen1floods) | Sentinel-1 SAR and Sentinel-2 optical imagery for low-lying water accumulation during monsoons. |
| **Municipal GIS Boundaries** | [India Geodata](https://github.com/yashveeeeeeer/india-geodata) | Ready-to-use GeoJSON boundaries covering municipal wards, water bodies, and road footprints across 28+ Indian cities. |

---

## 🏙️ Target Metropolitan Hubs & Corridors

1. **Bengaluru (Karnataka)**: Mahadevapura, Outer Ring Road (ORR), Bellandur, Kadubeesanahalli, Whitefield, Sarjapur Road, Hebbal, Electronic City, and HSR Layout.
2. **Mumbai & MMR (Maharashtra)**: Andheri West (Subway & Lokhandwala), Kurla & Sion Chunabhatti (Mithi River Basin), Bandra Kurla Complex (BKC), Powai & Hiranandani Gardens, Western Express Highway (WEH), Thane West (Ghodbunder Road), and Navi Mumbai (Panvel, Kharghar, Ulwe).
3. **Chennai (Tamil Nadu)**: Velachery & Madipakkam, Perungudi & OMR IT Corridor, Sholinganallur, Siruseri, Pallikaranai Marshland, Porur & Ramapuram, Guindy & Alandur, and East Coast Road (ECR).
4. **Delhi-NCR (Delhi / Haryana / UP)**: Yamuna Floodplains & Mayur Vihar, Barapullah Phase-III / Sarai Kale Khan, South Delhi (Defence Colony & Greater Kailash), Gurugram (Cyber City, DLF Phase 2 & Golf Course Ext), Noida Expressway (Sector 150 & 137), and Dwarka Expressway.
5. **Hyderabad (Telangana)**: Gachibowli & Financial District, HITECH City & Madhapur, Kondapur & Hafeezpet, Kukatpally & KPHB, Tellapur & Kollur, Musi River Basin (Moosarambagh), and Nallagandla.
6. **Varanasi & Eastern UP 100km Corridor (Uttar Pradesh)**:
   - **Varanasi**: Ancient Core (Godowlia - Chowk), Ganga-Varuna Confluence (Sarai Mohana), Cantt & Shivpur (Elevated Alluvial Ridge), Ramnagar Sandstone Bluff.
   - **Prayagraj (Allahabad)**: Sangam Lowlands (Baghada & Salori chronic evacuation basin) vs. Civil Lines & Ashok Nagar (Elevated British Grid Plateau).
   - **Mirzapur**: Vindhyan Runoff & Ganga Ghats.
   - **Jaunpur**: Gomti River Meander & Shahi Bridge Hydraulic Bottleneck.
   - **Chandauli**: Mughalsarai / Pt. Deen Dayal Upadhyaya Nagar.

---

## ⚡ Key Capabilities & New Features

### 1. Multi-Select Area / Locality Restriction Filter
- Configurable multi-select filter allowing users to restrict all screener tables, maps, and comparative analyses to specific micro-markets (e.g. `['Bellandur', 'Kadubeesanahalli']` or `['Andheri West']`).
- When activated, all maps, purchase tables, gated plots, and rental benchmarks dynamically isolate inventories within the chosen areas.

### 2. AI/ML Project Search & Onboarding Engine
- Empowers users to search and onboard any new project across India using an autonomous extraction engine.
- Pulls multi-source civic telemetry (RERA registries, municipal GIS flood contours, TomTom traffic indices, and developer filings).
- **Deduplication Engine**: Enforces strict deduplication using cryptographic content hashing; existing entries are skipped unless key pricing, phase, or completion specifications have changed.
- Automatically calculates:
  - Ranked composite Investment Score
  - Date of publish and verifiable source citation links
  - Projected 5-Year Capital Appreciation (%) and planned development catalysts
  - Expected completion timelines & upcoming phase details

### 3. Critic AI Validation & Autonomous Self-Correction
- Dedicated Critic AI testing engine audits every property against hydrological and civic heuristics:
  - **Basin Elevation Check**: Evaluates claimed plinth elevations against Digital Elevation Models (DEM); penalizes projects in known depression basins claiming zero flood risk.
  - **Water Pipeline Ground Reality**: Verifies whether municipal bulk supply (e.g., BWSSB Cauvery Stage V, BMC, CMWSSB) has officially been commissioned in the specific sector.
  - **Price Sanity Bounds**: Audits rates against municipal guideline values and registration data.
- Enforces corrections and displays transparent status badges (`✅ Critic AI Validated` or `⚠️ Auto-Corrected by Critic AI`).

### 4. Daily AI/ML Scan & Local Multi-Sheet Excel Storage (`.xlsx`)
- Automatically generates and synchronizes Tab 1 screener data locally to `data/daily_property_screener_dump.xlsx`.
- Multi-sheet workbook covering:
  - `Top 10 Purchase Properties`
  - `Top 10 Gated Plots`
  - `Top 10 Rental Properties`
  - `Mega Master Plans`
  - `Critic AI & Onboarded Log`
- Includes in-app **Download Daily Excel (.xlsx)** button.

### 5. Parameter Definitions on Mouse Hover (Interactive Tooltips)
- Every column header in table views contains a native tooltip (`title="..."`) explaining the parameter in simple, non-technical terms when hovering with a mouse.
- Supported by a dedicated **Parameter Dictionary** expander in the UI.

### 6. Distance Calculation Logic (Tiered Detour Routing)
- Matches the South East Bengaluru app routing logic (`utils/geo.py`):
  - Local road grid ($h \le 1.0\text{ km}$): $1.25\times$
  - Arterial / tech corridors ($1.0 < h \le 8.0\text{ km}$): $1.32\times$
  - Highway / expressway bypass ($h > 8.0\text{ km}$): $1.22\times$

### 7. Live System Resource Telemetry (CPU & RAM Load)
- Real-time diagnostic telemetry bar visible at the top header and in the sidebar.
- Monitors **Streamlit Process Memory (MB)**, **System RAM Used / Total (GB, %)**, and **CPU Utilization (%)** with active health badges (`Optimal 🟢`, `Moderate 🟡`, `High Load 🔴`).

### 8. Multi-Layer Google Maps & Property Focus Zoom
- Seamless tile layer switching between **Google Maps (Roadmap)**, **Google Maps (Satellite Hybrid)**, **Google Maps (Terrain)**, **CartoDB Dark Matter**, and **OpenStreetMap**.
- **Interactive Focus Selector**: Choose any property to immediately zoom in, render a prominent glowing focus halo, and draw a dynamic driving route polyline to the configured benchmark landmark.
### 9. Unified Radar & Top 15+ Builders Directory (Clubbed Architecture)
- Merges the Panoramic Geospatial Radar, Top 10 Multi-City Comparative Tables, and the Top 15+ Builders Directory into a single seamless flagship tab (`🗺️ Panoramic Radar, Top Properties & Builder Directory`).
- Benchmarks Tier-1 National Leaders and Regional Champions per city (96 builders across India) with verified RERA on-time delivery percentages, construction quality ratings (1-10), litigation risk indices, delivered square footage, and direct state RERA registry links.
- Interactive cross-filtering allows searching by developer brand, project name, or neighborhood simultaneously across properties and builder registries.

### 10. City Center 4th-Column Distance Benchmark (Configurable)
- Default 4th-column distance calculation across all screener tables computes exact tiered road distance to each metropolitan region's **City Center**:
  - **Bengaluru**: Vidhana Soudha / MG Road (`12.9778° N, 77.5713° E`)
  - **Mumbai & MMR**: CSMT / Fort (`18.9401° N, 72.8354° E`)
  - **Chennai**: Chennai Central (`13.0823° N, 80.2754° E`)
  - **Delhi-NCR**: Connaught Place (`28.6304° N, 77.2177° E`)
  - **Hyderabad**: Secretariat / Abids (`17.4062° N, 78.4691° E`)
  - **Varanasi Corridor**: Varanasi Cantt / Godowlia (`25.3268° N, 82.9866° E`)
- Fully configurable in the sidebar to switch between City Center, premier schools, primary IT hubs, or custom GPS coordinates.

### 11. Property Age vs Upcoming Handover Timeline & Appreciation Matrix
- Displays **Property Age vs Completion Timeline** as the 5th column across all purchase and plotted inventories:
  - **Ready-to-Move Properties**: Categorized by society age (e.g., `🟢 Ready to Move (4 yrs old • Active Community)`).
  - **Under-Construction / Upcoming Projects**: Categorized by target completion quarter and remaining delivery buffer (e.g., `🏗️ Under Construction (Dec 2026 • 14 mos)` or `🚀 Upcoming Pre-Launch (March 2027 • ~2 yrs)`).
- Includes an interactive Plotly timeline scatter chart analyzing **Completion Target vs 5-Year Capital Appreciation (%)**.

### 12. Dynamic Table Refresh on Corridor, Locality & Budget Filter
- By default, displays top properties and plots across India (National Top 10).
- When a user selects a specific corridor, adds preferred localities, adjusts the purchase budget (e.g., ₹3.50 Cr) or rental budget (e.g., ₹80,000/mo), or types a search keyword, all screener tables dynamically refresh in real time.

### 13. Sticky 1st-Column Frozen Table Engine
- Pure CSS sticky iframe renderer (`utils/table_view.py`) locking the first column on the left with `#0D9488` teal divider and shadow, guaranteeing responsive scrolling across desktop, tablet, and mobile browsers.

### 14. Verified Farmlands & High-Yield Agro-Investments Engine
- Curated catalog of 24 verified agricultural land parcels and managed agroforestry estates across India (`data/farmlands.json`).
- **Comprehensive Agronomic Telemetry**: Soil classification, pH, organic carbon %, groundwater table depth, sweet water TDS (ppm), and drip irrigation status.
- **High-Value Exotic & Commercial Crop Modeling**: Benchmark economics, tree density, gestation timelines, and annual harvest yields for Hass Avocado, Certified Sandalwood (Chandan), Dragon Fruit (Pitaya), Taiwan Pink Guava, Alphonso Mango, and Protected Greenhouses.
- **Verified Seller Contacts & Categorization**: Distinguishes between `Direct Landowner / Farmer`, `Verified Agricultural Broker`, and `Managed Farmland Operator` with instant Click-to-Call (`tel:`) and Direct WhatsApp Inquiry (`wa.me`) buttons.
- **State-Wise Land Purchase Legal Guide**: Comprehensive due diligence frameworks for Karnataka (Sections 79A/B repealed), Maharashtra (Section 63 MTAL), Tamil Nadu (unrestricted Patta/Chitta transfers), Telangana (Dharani instant registry), and Uttar Pradesh (Section 80 conversion).
- **Multi-Sheet Daily Excel Export**: Farmland inventory with all 28 agronomic, financial, and legal attributes automatically exported to the `"Verified Farmlands"` worksheet in `daily_property_screener_dump.xlsx`.

---

## 🚀 Quickstart & Local Installation

### Prerequisites
- Python 3.10 or higher installed.
- Git installed.

### 1. Clone the Repository
```bash
git clone https://github.com/purntripathi-cmd/Flood-Traffic-Water-supply-Monitor-for-Indian-Cities.git
cd Flood-Traffic-Water-supply-Monitor-for-Indian-Cities
```

### 2. Create and Activate Virtual Environment
```bash
# Windows (PowerShell)
python -m venv .venv
.venv\Scripts\Activate.ps1

# Linux / macOS
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Launch the Streamlit Monitor
```bash
streamlit run app.py
```
Open your browser at `http://localhost:8501` or access the cloud deployment at [flood-traffic-water-supply-monitor-for-indian-cities.streamlit.app](https://flood-traffic-water-supply-monitor-for-indian-cities.streamlit.app/).

---

## 📁 Repository Structure

```
Flood-Traffic-Water-supply-Monitor-for-Indian-Cities/
├── .streamlit/
│   └── config.toml                  # Dark theme styling (#0D9488, #0F172A)
├── data/
│   ├── cities.json                  # 6 target metropolitan hubs and baseline stats
│   ├── micro_markets.json           # 42 detailed micro-markets with elevation & delay indices
│   ├── builders.json                # 96 top builders (16 per city) with RERA on-time delivery & quality
│   ├── properties.json              # 18 benchmark residential purchase properties with master plans & utilities
│   ├── rental_properties.json       # 18 rental benchmark properties with yields & commute hubs
│   ├── gated_plots.json             # 18 vetted gated villa plotted communities with statutory approvals
│   ├── govt_master_plans.json       # Government infrastructure master plans (Metro, Aerotropolis, Expressways)
│   ├── cbse_schools.json            # 15 premier CBSE/ICSE schools with Class 1-12 fee structures
│   ├── avoidance_zones.json         # 12 notorious chronic avoidance hotspots
│   ├── onboarded_projects.json      # Dynamic AI/ML onboarded custom projects
│   ├── daily_property_screener_dump.xlsx # Deduplicated multi-sheet Excel scan
│   └── user_preferences.json        # Configurable budget and risk defaults
├── utils/
│   ├── __init__.py
│   ├── table_view.py                # Pure CSS sticky 1st-column frozen table renderer with mouse hover tooltips
│   ├── geo.py                       # Tiered urban detour distance calculation, maps URLs
│   ├── scoring.py                   # 0-100 composite avoidance viability index algorithm
│   ├── schools.py                   # Multi-city CBSE/ICSE school proximity & fee structure renderer
│   ├── critic_ai.py                 # Autonomous data validation, anomaly detection & self-correction
│   ├── ai_onboarder.py              # Multi-source AI/ML search, extraction, and deduplication
│   ├── excel_exporter.py            # Multi-sheet Excel workbook export & daily synchronization
│   └── ai_copilot.py                # Explainable AI recommendation engine with citations
├── scripts/
│   ├── generate_cities_and_builders.py # Generator for 6 cities and 96 builders
│   ├── generate_all_property_inventories.py # Generator for purchase, plots, rentals, and master plans
│   └── enrich_inventories_with_critic_and_sources.py # Enriches data with Critic AI status and 5-yr growth
├── app.py                           # Master Property Screener application with live telemetry & Google Maps
├── requirements.txt                 # Python dependencies (including openpyxl)
├── .gitignore                       # Git ignore rules (protects .github/ and .venv/)
└── README.md                        # Documentation and architecture guide
```

---

## ⚖️ License & Citations
- **License**: Released under the [MIT License](LICENSE).
- **Citations**: Please cite the respective civic and academic research repositories when utilizing the underlying flood and traffic data indices (*IIT Delhi HydroSense, RushilGargash08, diagram-chasing, parthtiwari-dev, yashveeeeeeer, IIT Gandhinagar*).
