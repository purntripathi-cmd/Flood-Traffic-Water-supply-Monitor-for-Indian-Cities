# 🌊 Flood, Traffic & Water Supply Monitor for Indian Cities

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

## ⚡ Key Capabilities & Features

### 1. Live System Resource Telemetry (CPU & RAM Load)
- Real-time diagnostic telemetry bar visible at the top header and in the sidebar.
- Monitors **Streamlit Process Memory (MB)**, **System RAM Used / Total (GB, %)**, and **CPU Utilization (%)** with active health badges (`Optimal 🟢`, `Moderate 🟡`, `High Load 🔴`).

### 2. Multi-Layer Google Maps & Property Focus Zoom
- Seamless tile layer switching between **Google Maps (Roadmap)**, **Google Maps (Satellite Hybrid)**, **Google Maps (Terrain)**, **CartoDB Dark Matter**, and **OpenStreetMap**.
- **Interactive Focus Selector**: Choose any property to immediately zoom in, render a prominent glowing focus halo, and draw a dynamic driving route polyline to the configured benchmark landmark.

### 3. Cross-City Top 10 Comparison Tables (National Radar)
Permanent Tab 1 feature comparing inventories across all 6 metropolitan regions, sorted High to Low by score:
- **Top 10 Properties to Purchase / Invest**: Sorted by composite Investment Score, featuring Government Master Plan growth probabilities (%), plinth elevations, flood resilience tags, and utility infrastructure breakdowns.
- **Top 10 Best Gated Community Plots & Land**: Sorted by Plotted Appreciation Score, featuring statutory approvals (BMRDA, CIDCO, CMDA, DTCP, HMDA, VDA), soil percolation, and elevation.
- **Top 10 Best Rental Properties**: Sorted by Rental Viability Score, featuring net rental yields (%), commute distances, and maintenance costs.

### 4. Configurable 4th Column Benchmark Distance
- Interactive benchmark selector in the sidebar configurable to key landmarks or schools.
- Defaults to **🏫 New Horizon Gurukul** for Bengaluru, and regional benchmark institutions (DAIS for Mumbai, Sishya for Chennai, TSRS for Delhi-NCR, CHIREC for Hyderabad, Sunbeam for Varanasi).

### 5. CBSE / ICSE School Proximity & Fee Structures (Classes 1st to 12th)
- Collapsible interactive cards embedded in property profiles detailing nearby CBSE/ICSE schools, driving distances, verified ratings, review counts, and complete tuition fee brackets from Class 1 to Class 12.

### 6. Full Civic Utility Tracking
- Granular infrastructure breakdown for every property:
  - **STP**: Advanced MBBR / SBR sewage treatment plants.
  - **Water Softeners**: Centralized ion-exchange plants for high-TDS groundwater.
  - **Individual IoT Water Meters**: Sub-metered consumption preventing billing disputes.
  - **Dual Plumbing / Double Piping**: Recycled greywater for flush & landscaping.
  - **Piped Gas**: IGL / GAIL / Adani piped gas connections.
  - **Municipal Supply**: Authorized bulk piped municipal water (BWSSB / BMC / CMWSSB / DJB / HMWSSB / UP Jal Sansthan).

### 7. Top Builders by City & State (At Least 15+ per City, 96 Total)
- Benchmarks 16 Tier-1 National Leaders and Regional Champions per city (96 builders across India).
- Tracks verified RERA on-time delivery percentages, construction quality ratings (1-10), litigation risk indices, delivered square footage, and direct state RERA registry links.

### 8. Sticky 1st-Column Frozen Table Engine
- Pure CSS sticky iframe renderer (`utils/table_view.py`) locking the first column on the left with `#0D9488` teal divider and shadow, guaranteeing responsive scrolling across desktop, tablet, and mobile browsers.

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
│   └── user_preferences.json        # Configurable budget and risk defaults
├── utils/
│   ├── __init__.py
│   ├── table_view.py                # Pure CSS sticky 1st-column frozen table renderer
│   ├── geo.py                       # Haversine distance, urban detour factors, maps URLs
│   ├── scoring.py                   # 0-100 composite avoidance viability index algorithm
│   ├── schools.py                   # Multi-city CBSE/ICSE school proximity & fee structure renderer
│   └── ai_copilot.py                # Explainable AI recommendation engine with citations
├── scripts/
│   ├── generate_cities_and_builders.py # Generator for 6 cities and 96 builders
│   └── generate_all_property_inventories.py # Generator for purchase, plots, rentals, and master plans
├── app.py                           # Master multi-city Streamlit application with live telemetry & Google Maps
├── requirements.txt                 # Python dependencies
├── .gitignore                       # Git ignore rules (protects .github/ and .venv/)
└── README.md                        # Documentation and architecture guide
```

---

## ⚖️ License & Citations
- **License**: Released under the [MIT License](LICENSE).
- **Citations**: Please cite the respective civic and academic research repositories when utilizing the underlying flood and traffic data indices (*IIT Delhi HydroSense, RushilGargash08, diagram-chasing, parthtiwari-dev, yashveeeeeeer, IIT Gandhinagar*).
