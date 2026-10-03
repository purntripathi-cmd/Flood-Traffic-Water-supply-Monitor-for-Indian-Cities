# 🌊 Flood, Traffic & Water Supply Monitor for Indian Cities

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://github.com/purntripathi-cmd/Flood-Traffic-Water-supply-Monitor-for-Indian-Cities)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-teal.svg)](https://opensource.org/licenses/MIT)
[![Civic Intelligence](https://img.shields.io/badge/Civic-Intelligence%20Radar-emerald.svg)](#)

> **High-Fidelity Civic Infrastructure & Real Estate Avoidance Screener** across 6 major Indian metropolitan corridors: **Bengaluru**, **Mumbai & MMR**, **Chennai**, **Delhi-NCR**, **Hyderabad**, and **Varanasi & Eastern UP 100km Corridor** (Varanasi, Prayagraj, Mirzapur, Jaunpur, Chandauli).

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

1. **Bengaluru (Karnataka)**: Mahadevapura, Outer Ring Road (ORR), Bellandur, Whitefield, Sarjapur Road, Hebbal, Electronic City, and HSR Layout.
2. **Mumbai & MMR (Maharashtra)**: Andheri West (Subway & Lokhandwala), Kurla & Sion Chunabhatti (Mithi River Basin), Bandra Kurla Complex (BKC), Powai & Hiranandani Gardens, Western Express Highway (WEH), Thane West (Ghodbunder Road), and Navi Mumbai (Vashi & Seawoods).
3. **Chennai (Tamil Nadu)**: Velachery & Madipakkam, Perungudi & OMR IT Corridor, Sholinganallur, Pallikaranai Marshland, Porur & Ramapuram, Guindy & Alandur, and East Coast Road (ECR).
4. **Delhi-NCR (Delhi / Haryana / UP)**: Yamuna Floodplains & Mayur Vihar, Barapullah Phase-III / Sarai Kale Khan, South Delhi (Defence Colony & Greater Kailash), Gurugram (Cyber City & DLF Phase 2), Gurugram (Golf Course Extension Road), Noida Expressway (Sector 150 & 137), and Dwarka Expressway.
5. **Hyderabad (Telangana)**: Gachibowli & Financial District, HITECH City & Madhapur, Kondapur & Hafeezpet, Kukatpally & KPHB, Tellapur & Kollur, Musi River Basin (Moosarambagh), and Nallagandla.
6. **Varanasi & Eastern UP 100km Corridor (Uttar Pradesh)**:
   - **Varanasi**: Ancient Core (Godowlia - Chowk), Ganga-Varuna Confluence (Sarai Mohana), Cantt & Shivpur (Elevated Alluvial Ridge), Ramnagar Sandstone Bluff.
   - **Prayagraj (Allahabad)**: Sangam Lowlands (Baghada & Salori chronic evacuation basin) vs. Civil Lines & Ashok Nagar (Elevated British Grid Plateau).
   - **Mirzapur**: Vindhyan Runoff & Ganga Ghats.
   - **Jaunpur**: Gomti River Meander & Shahi Bridge Hydraulic Bottleneck.
   - **Chandauli**: Mughalsarai / Pt. Deen Dayal Upadhyaya Nagar.

---

## ⚡ Key Capabilities & Features

### 1. 0 to 100 Composite Avoidance & Viability Index
A quantitative multi-criteria decision algorithm combining:
$$\text{Viability Score} = 100 - (0.30 \times \text{Flood Risk}) - (0.25 \times \text{Traffic Penalty}) - (0.20 \times \text{Water Insecurity}) + (0.15 \times \text{Drainage Infrastructure}) + (0.10 \times \text{Builder Pedigree})$$
- 🟢 **Score $\ge 75$**: Prime Resilient Buy / Rent (High plinth, low flood recurrence, low tanker reliance).
- 🟡 **Score $55 - 74$**: Watchlist / Caution (Monsoon stress, localized road puddling, or traffic bottlenecks).
- 🔴 **Score $< 55$**: High-Risk Avoidance Zone (Low-lying lakebed, subway depression, river backflow inundation).

### 2. Sticky 1st-Column Frozen Table Engine
- Built with a pure CSS sticky iframe renderer (`utils/table_view.py`) guaranteeing responsive scrolling across desktop, tablet, and mobile browsers.
- Permanently locks Column 1 (Property Name, Micro-Market, Layout, or Builder) on the left with `#0D9488` teal divider and shadow, while all other columns scroll smoothly horizontally.

### 3. Top Builders Directory & RERA Audit
- Vetted repository of Tier 1 National Leaders (*Godrej, Prestige, Sobha, Brigade, Lodha, Oberoi, DLF, Tata Housing, Hiranandani, Puravankara, Mahindra*) and Regional Champions (*Casagrand, Aparna, My Home, Eldeco, Omaxe*).
- Displays verified RERA on-time delivery percentages, construction quality ratings (1-10), litigation risk indices, and direct portal links.

### 4. Configurable Real Estate Screener
- Interactive sidebar budget controls:
  - **Purchase Budget**: Default ₹3.50 Crores (configurable up to ₹12 Cr).
  - **Rental Budget**: Default ₹80,000 / month (configurable).
  - **Authorized Municipal Piped Water Filter**: BWSSB / BMC / CMWSSB / DJB / HMWSSB / Jal Sansthan.
  - **Direct Map Navigation**: Named Google Maps search queries and official RERA registry links.

### 5. Gated Community Villa Plots & Land Recommendations
- Curated directory of plotted developments (*Prestige Great Acres, Brigade Oasis, Hiranandani Fortune City Plots, DLF Alameda, My Home Ankura, Eldeco Shaurya, etc.*).
- Evaluates land elevation, soil percolation, layout storm drain outfalls, and town planning approvals (BDA, DTCP, HMDA, CIDCO, VDA, PDA).

### 6. Water Supply & Tanker Burden Calculator
- Models per-flat monthly savings of municipal piped connections and dual-piping STPs vs private tanker dependency (calculating up to ₹4,500/month in household savings).
- Tracks groundwater table depth and total dissolved solids (TDS ppm).

### 7. Chronic Avoidance Zones Deep Dive
- Forensic breakdowns of notorious avoidance hotspots:
  - *Andheri Subway & Milan Subway (Mumbai)*
  - *Kurla & Sion Chunabhatti Mithi River Basin (Mumbai)*
  - *Velachery Lakebed & Pallikaranai Marsh Encroachments (Chennai)*
  - *Rainbow Drive Layout & Bellandur EcoSpace Underpass (Bengaluru)*
  - *Yamuna Floodplains & Barapullah Phase-III Choke (Delhi-NCR)*
  - *Musi River Moosarambagh Lowlands (Hyderabad)*
  - *Prayagraj Baghada & Salori Sangam Backwater Zone (Eastern UP)*
  - *Varanasi Ganga-Varuna Confluence (Sarai Mohana)*
  - *Jaunpur Gomti River Shahi Bridge Bottleneck*

### 8. Explainable AI Avoidance Copilot
- Natural language query assistant evaluating user constraints and outputting structured markdown briefs with direct academic citations.

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
Open your browser at `http://localhost:8501`.

---

## 📁 Repository Structure

```
Flood-Traffic-Water-supply-Monitor-for-Indian-Cities/
├── .streamlit/
│   └── config.toml                  # Dark theme styling (#0D9488, #0F172A)
├── data/
│   ├── cities.json                  # 6 target metropolitan hubs and baseline stats
│   ├── micro_markets.json           # 42 detailed micro-markets with elevation & delay indices
│   ├── builders.json                # 22 top builders with RERA on-time delivery & quality ratings
│   ├── properties.json              # 36 benchmark residential purchase/rental properties
│   ├── gated_plots.json             # 18 vetted gated villa plotted communities
│   ├── avoidance_zones.json         # 12 notorious chronic avoidance hotspots
│   └── user_preferences.json        # Configurable budget and risk defaults
├── utils/
│   ├── __init__.py
│   ├── table_view.py                # Pure CSS sticky 1st-column frozen table renderer
│   ├── geo.py                       # Haversine distance, urban detour factors, maps URLs
│   ├── scoring.py                   # 0-100 composite avoidance viability index algorithm
│   └── ai_copilot.py                # Explainable AI recommendation engine with citations
├── scripts/
│   ├── generate_datasets.py         # Primary dataset generator
│   └── generate_properties_plots_avoidance.py # Property & plot data generator
├── app.py                           # Master multi-city Streamlit application
├── requirements.txt                 # Python dependencies
├── .gitignore                       # Git ignore rules (protects .github/ and .venv/)
└── README.md                        # Documentation and architecture guide
```

---

## ⚖️ License & Citations
- **License**: Released under the [MIT License](LICENSE).
- **Citations**: Please cite the respective civic and academic research repositories when utilizing the underlying flood and traffic data indices (*IIT Delhi HydroSense, RushilGargash08, diagram-chasing, parthtiwari-dev, yashveeeeeeer, IIT Gandhinagar*).
