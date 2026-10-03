"""
Custom Sticky / Frozen Column Table Renderer for Streamlit
Freezes 1st column (configurable) and sticky header with horizontal and vertical scroll.
Renders via Streamlit Components HTML iframe for 100% guaranteed visibility across all browsers.
Includes intuitive parameter definitions that appear as tooltips on mouse hover.
Features universal wrap text across all cells and headers with responsive row height.
Features native client-side interactive sorting on every column header (click to sort asc/desc).
"""

import html as html_lib
import pandas as pd
import streamlit as st
import streamlit.components.v1 as components

# Dictionary of parameter definitions explaining every metric in simple words on mouse hover
PARAMETER_DEFINITIONS = {
    "Rank": "Current ranking position within the selected scope (All India or focused Corridor).",
    "Property Name": "Registered legal project name under RERA and local municipal corporation.",
    "Layout / Scheme Name": "Name of the approved plotted community layout.",
    "City & Micro-Market": "Metropolitan jurisdiction and specific urban ward / neighbourhood cluster.",
    "City & Location": "City and locality where the plotted layout is situated.",
    "Builder & Tier": "Developer brand pedigree classified as Tier 1 National Leader or Regional Champion based on track record.",
    "Developer": "Promoter or real estate firm executing the project / layout.",
    "Growth Prob (% Plan)": "Statistical likelihood (0-100%) of superior capital appreciation directly driven by state-funded mega infrastructure projects.",
    "Govt Master Plan Catalyst": "Key government public infrastructure project (e.g. Metro Line, Coastal Road, Aerotropolis) boosting connectivity.",
    "Projected 5-Yr Appreciation": "Forecasted capital appreciation percentage over a 5-year investment horizon based on historical CAGR and planned infrastructure.",
    "Expected Completion": "Quarter and year of project handover, occupancy certificate issuance, or construction completion.",
    "Upcoming Phase Details": "Specific tower, wing, or pre-launch phase currently under development.",
    "Property Age vs Completion Timeline": "Distinguishes ready-to-move projects by actual society age (years since occupancy certificate) versus under-construction or upcoming pre-launch phases by targeted completion quarters and remaining months.",
    "Age / Handover Status": "Current execution phase indicating ready possession with active occupancy vs upcoming handover milestones.",
    "Road Dist to City Center": "Direct driving road distance in km to the administrative / historical City Center (e.g. Vidhana Soudha, CSMT, Chennai Central, Connaught Place, Secretariat, Cantt/Godowlia, Hazratganj).",
    "Critic AI Status": "Automated validation status by Critic AI testing price realism, hydrological risk, and municipal sanction validity.",
    "Road Dist": "Realistic driving road network distance in km, accounting for street curvature, flyovers, and arterial detours.",
    "Config & Area": "Unit configuration (e.g. 2, 3, or 4 BHK) and average super built-up / carpet area in square feet.",
    "Plot Sizes (sqft)": "Available standard plot dimensions in square feet (e.g. 1200, 1500, 2400 sqft).",
    "Price / Sqft": "Unit purchase rate per square foot in Indian Rupees (₹).",
    "Total Price (Cr)": "All-inclusive base purchase cost of the residential apartment in ₹ Crores.",
    "Starting Ticket": "Entry-level purchase cost for land/plot in ₹ Lakhs.",
    "Upfront Cash (L)": "Estimated initial down payment and statutory stamp duty / registration cash required in ₹ Lakhs.",
    "Total Ownership (Cr)": "Comprehensive 5-year total cost of ownership including base price, stamp duty, GST, and maintenance.",
    "Plinth Elevation": "Elevation of the building ground slab in meters above Mean Sea Level (MSL). Higher elevation prevents flood runoff from entering basements.",
    "Land Elevation": "Natural topographical ground elevation in meters above Mean Sea Level (MSL).",
    "Flood Risk Category": "Topographical vulnerability to monsoon inundation based on lake overflow, river backflow, or low-lying basin depressions.",
    "Flood Exposure": "Vulnerability tag based on contour depressions, storm nala proximity, and historical monsoon logs.",
    "Statutory Authority": "Town planning and developmental authority (e.g., BMRDA, CIDCO, CMDA, DTCP, HMDA, VDA, LDA, PDA) that sanctioned the layout plan.",
    "Soil Percolation": "Natural soil absorption rate and rainwater runoff infiltration efficiency.",
    "STP & Water Infra": "On-site Sewage Treatment Plant (MBBR/SBR), Water Softener, Individual IoT Meter, Dual Plumbing, and Gas Pipeline status.",
    "Civic Utilities": "Availability of Sewage Treatment Plant (STP), Water Softener, IoT Meter, and Dual Plumbing.",
    "Investment Score": "Composite 0-100 viability ranking blending structural elevation, builder pedigree, flood safety, and transit growth catalysts.",
    "Appreciation Score": "0-100 score measuring long-term plotted land capital growth potential.",
    "Rental Score": "0-100 rental suitability score balancing yield, walking transit access, and municipal water reliability.",
    "Monthly Rent": "Base monthly rental outflow in Indian Rupees (₹).",
    "Maintenance / Mo": "Monthly society maintenance charges paid towards common facilities, security, and amenities.",
    "Security Deposit": "Upfront refundable deposit paid to landlord (typically 2 to 6 months of rent).",
    "Net Rental Yield": "Annual rental income expressed as a percentage of total property capital value, factoring in maintenance.",
    "Commute Hub Dist": "Road driving distance to the nearest major tech corridor or employment business district.",
    "School Dist": "Driving distance to the nearest premier CBSE / ICSE academic campus.",
    "Google Maps Navigation": "Direct navigation deep-link to the exact verified geographic pin on Google Maps.",
    "Google Maps Place": "Direct place link to view terrain, photos, and access roads on Google Maps.",
    "State RERA Registry": "Direct URL to official State Real Estate Regulatory Authority registry verifying developer approvals.",
    "Sanction Verification": "Direct URL to official town planning approval and RERA sanction registry.",
    "Data Sources & Links": "Verifiable primary references including State RERA Registries, Municipal Master Plans, and TomTom Congestion feeds.",
    "Farmland Estate Name": "Name of the agricultural estate, managed agroforestry plantation, or private family orchard.",
    "Parcel Extent (Acres)": "Total contiguous land acreage in standard acres and local units (Guntas, Bighas, Cents).",
    "Price / Acre (Lakhs)": "Agricultural land cost per acre in Indian Rupees (₹ Lakhs per acre).",
    "Total Outlay (Cr)": "Total purchase ticket price for the entire farmland parcel in ₹ Crores.",
    "Soil Type & Texture": "Soil classification (e.g. Red Sandy Loam, Gangetic Alluvium, Black Regur) indicating nutrient holding and drainage.",
    "Soil pH & Organic Carbon": "Soil chemical fertility: pH (optimal 6.5-7.5) and Organic Carbon (OC % > 0.75% indicates rich living soil).",
    "Water Security & Borewells": "Operational irrigation infrastructure: operational borewells (inch flow), canal water shares, and sweet water TDS.",
    "Water Salinity TDS": "Total Dissolved Solids in ppm; sweet potable water (< 400 ppm) ensures healthy crop root nutrient uptake.",
    "Supported Crops & Horticulture": "Agricultural crops validated by agro-climatic conditions, soil chemistry, and temperature ranges.",
    "High-Value Crops": "High-margin commercial agroforestry and exotic crops (e.g. Hass Avocado, Sandalwood, Dragon Fruit, Cordyceps Mushroom, Medjool Dates).",
    "Annual Harvest Estimate": "Estimated annual gross revenue from commercial crop harvest per acre once plantation reaches maturity.",
    "Title & Legal Verification": "Revenue ownership clarity: verified 30-year RTC / Pahani, Saat Bara (7/12), Patta Chitta, or Jamabandi without encumbrances.",
    "Farmhouse Allowance": "Permissible built-up area (typically up to 10% or 10,000 sqft) for agricultural cottage, workers quarters, and storage.",
    "Seller Category (Owner / Broker)": "Identifies direct farmer/landowner versus verified RERA-accredited agro broker or managed farmland community operator.",
    "Contact Person & Phone": "Direct mobile phone contact and instant WhatsApp communication link for land viewing and title document inspection.",
    "Pincode": "6-digit postal index code identifying the specific urban ward and micro-market.",
    "Ward / Locality": "Municipal administrative ward or prominent residential/commercial neighborhood cluster.",
    "Avoidance Severity": "Risk classification: Critical Avoidance (severe life/asset danger), High Stress Avoidance (chronic seasonal breakdown), or Moderate Caution.",
    "Elevation Delta": "Topographical difference in meters between the lowest contour of this locality and surrounding natural drainage ridges.",
    "Waterlogging Days / Season": "Historical average number of days per monsoon season with submerged streets, basements, or disabled vehicular traffic.",
    "Negative Feedbacks Count": "Aggregated resident grievances filed across municipal portals, RWAs, social media, and consumer litigation.",
    "Common Civic Complaints (-ve Feedback)": "Unfiltered resident complaints regarding drainage overflow, dry borewells, tanker mafia extortion, road craters, transformer trips, and foul odors.",
    "Water Tanker Reliance Index": "Scale of 1 to 10 measuring dependency on private water tankers due to absent or inadequate municipal piped supply.",
    "Peak Traffic Delay Index": "Ratio of peak-hour commute travel time to free-flow travel time, including average vehicle speed (km/h).",
    "10-20 Yr Development Authority Master Plan": "Long-term planned public infrastructure schemes (2026-2045) sanctioned by statutory urban planning authorities.",
    "Upcoming Metro Line & Station": "Specific mass rapid transit rail corridor, upcoming station name, and scheduled year of commercial operation.",
    "Upcoming Airport Connectivity": "Driving distance, dedicated elevated expressway, or high-speed rail access to the international airport or upcoming greenfield airport.",
    "Major Malls, Sports & Tourist Hubs": "Proximity to regional grade-A shopping malls, Olympic stadiums, public sports complexes, lake promenades, and cultural tourist circuits.",
    "Critique Negative Penalty": "Points deducted from the area's viability score based on the severity and frequency of civic complaints and infrastructure breakdowns.",
    "Critique Master Plan Boost": "Points awarded to the area based on transformative upcoming 10-20 year public transit, highway, and civic projects.",
    "Critique AI Viability Score": "Composite 0-100 score balancing negative civic distress against long-term development authority master plan catalysts.",
    "Real Estate Advisory": "Unbiased actionable recommendation for prospective property buyers, tenants, and commercial investors."
}


def get_column_definition(col_name: str) -> str:
    """Finds the most matching explanation for a column name."""
    col_clean = str(col_name).strip()
    if col_clean in PARAMETER_DEFINITIONS:
        return PARAMETER_DEFINITIONS[col_clean]
    for key, val in PARAMETER_DEFINITIONS.items():
        if key.lower() in col_clean.lower() or col_clean.lower() in key.lower():
            return val
    return f"Parameter metric: {col_clean}. Hover to inspect values."


def render_sticky_frozen_table(df: pd.DataFrame, frozen_cols: int = 1, table_id: str = "custom_table", max_height: str = "580px"):
    """
    Renders an HTML/CSS table where the first `frozen_cols` columns are permanently frozen / sticky on the left,
    and the table header is sticky on top, while the remaining columns scroll horizontally.
    Includes mouse hover tooltip definitions on every column header.
    Fully implements text wrapping in all cells and interactive client-side column header sorting.
    """
    if df.empty:
        st.info("No records to display matching active filters.")
        return

    cols = list(df.columns)
    frozen_col_count = min(frozen_cols, len(cols))

    # Calculate optimal pixel height (accounting for multi-line wrapped cells)
    try:
        max_h_int = int(str(max_height).replace("px", "").strip())
    except Exception:
        max_h_int = 580
    calc_height = min(max_h_int, max(380, (len(df) + 1) * 75 + 70))

    # Column widths for frozen columns - 280px for generous fit with clean multi-line wrapping
    col_widths = [280, 210, 190, 170]
    offsets = [0]
    for i in range(1, frozen_col_count):
        w = col_widths[i-1] if i-1 < len(col_widths) else 170
        offsets.append(offsets[i-1] + w)

    # Build pure CSS with strict text-wrapping across all headers and cells
    css_rules = [f"""
    * {{
        box-sizing: border-box;
    }}
    body {{
        margin: 0;
        padding: 0;
        background-color: #0B1120;
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
        color: #F8FAFC;
    }}
    .table-container {{
        position: relative;
        overflow-x: auto;
        overflow-y: auto;
        max-height: {calc_height - 10}px;
        width: 100%;
        border: 1px solid #334155;
        border-radius: 8px;
        background-color: #0B1120;
        -webkit-overflow-scrolling: touch;
    }}
    table {{
        border-collapse: separate;
        border-spacing: 0;
        width: 100%;
        font-size: 0.84rem;
        table-layout: auto;
    }}
    th {{
        position: sticky;
        top: 0;
        background-color: #1E293B;
        color: #38BDF8;
        font-weight: 700;
        padding: 12px 14px;
        border-bottom: 2px solid #334155;
        border-right: 1px solid #334155;
        white-space: normal !important;
        word-wrap: break-word !important;
        overflow-wrap: break-word !important;
        line-height: 1.35 !important;
        min-width: 140px;
        z-index: 25;
        text-align: left;
        cursor: pointer;
        user-select: none;
    }}
    th:hover {{
        background-color: #334155;
        color: #7DD3FC;
    }}
    td {{
        padding: 11px 14px;
        border-bottom: 1px solid #1E293B;
        border-right: 1px solid #1E293B;
        white-space: normal !important;
        word-wrap: break-word !important;
        overflow-wrap: break-word !important;
        word-break: break-word !important;
        vertical-align: middle;
        background-color: #0B1120;
        color: #E2E8F0;
        line-height: 1.45 !important;
        min-width: 130px;
    }}
    tr:nth-child(even) td {{
        background-color: #0F172A;
    }}
    tr:hover td {{
        background-color: #1E293B !important;
    }}
    .sort-icon {{
        display: inline-block;
        margin-left: 5px;
        font-size: 0.72rem;
        color: #94A3B8;
        vertical-align: middle;
    }}
    th:hover .sort-icon {{
        color: #38BDF8;
    }}
    """]

    # Frozen column rules
    for idx in range(frozen_col_count):
        nth = idx + 1
        left_px = offsets[idx]
        width_px = col_widths[idx] if idx < len(col_widths) else 170
        is_last_frozen = (idx == frozen_col_count - 1)
        
        if is_last_frozen:
            border_r = "border-right: 3px solid #0D9488 !important; box-shadow: 4px 0 10px rgba(0,0,0,0.6);"
        else:
            border_r = "border-right: 1px solid #334155;"

        if nth == 1:
            font_color = "#38BDF8"
            font_weight = "700"
        elif nth == 2:
            font_color = "#F8FAFC"
            font_weight = "600"
        else:
            font_color = "#E2E8F0"
            font_weight = "500"

        css_rules.append(f"""
        th.fcol-{nth} {{
            position: sticky;
            left: {left_px}px;
            top: 0;
            z-index: 45 !important;
            background-color: #1E293B !important;
            min-width: {width_px}px !important;
            max-width: {width_px + 80}px !important;
            width: {width_px}px !important;
            white-space: normal !important;
            word-wrap: break-word !important;
            overflow-wrap: break-word !important;
            word-break: break-word !important;
            line-height: 1.35 !important;
            {border_r}
        }}
        td.fcol-{nth} {{
            position: sticky;
            left: {left_px}px;
            z-index: 20;
            background-color: #0B1120 !important;
            min-width: {width_px}px !important;
            max-width: {width_px + 80}px !important;
            width: {width_px}px !important;
            font-weight: {font_weight};
            color: {font_color};
            white-space: normal !important;
            word-wrap: break-word !important;
            overflow-wrap: break-word !important;
            word-break: break-word !important;
            line-height: 1.45 !important;
            vertical-align: middle;
            {border_r}
        }}
        tr:nth-child(even) td.fcol-{nth} {{
            background-color: #0F172A !important;
        }}
        tr:hover td.fcol-{nth} {{
            background-color: #1E293B !important;
        }}
        """)

    full_css = "\n".join(css_rules)

    # Build Table HTML
    html_parts = [
        "<!DOCTYPE html>",
        "<html>",
        "<head>",
        "<meta charset='utf-8'>",
        f"<style>{full_css}</style>",
        "</head>",
        "<body>",
        f"<div class='table-container' id='{table_id}_container'>",
        f"<table id='{table_id}'>",
        "<thead>",
        "<tr>"
    ]

    for idx, c in enumerate(cols):
        col_class = f" class='fcol-{idx+1}'" if idx < frozen_col_count else ""
        col_def = get_column_definition(str(c))
        # Add title attribute, info symbol, and interactive sort indicator
        html_parts.append(
            f"<th{col_class} title='{html_lib.escape(col_def)}' data-col='{idx}'>"
            f"{html_lib.escape(str(c))} "
            f"<span style='font-size:0.68rem; color:#94A3B8;'>ℹ️</span>"
            f"<span class='sort-icon'>⇅</span>"
            f"</th>"
        )
    html_parts.append("</tr></thead><tbody>")

    for _, row in df.iterrows():
        html_parts.append("<tr>")
        for idx, c in enumerate(cols):
            col_class = f" class='fcol-{idx+1}'" if idx < frozen_col_count else ""
            raw_val = str(row[c]) if row[c] is not None else ""
            
            # Format cell content with badges
            if "🟢" in raw_val:
                cell_content = f"<span style='background:rgba(16,185,129,0.15); color:#34D399; padding:3px 8px; border-radius:4px; font-weight:700; border:1px solid rgba(16,185,129,0.3); display:inline-block;'>{html_lib.escape(raw_val)}</span>"
            elif "🟡" in raw_val:
                cell_content = f"<span style='background:rgba(245,158,11,0.15); color:#FBBF24; padding:3px 8px; border-radius:4px; font-weight:700; border:1px solid rgba(245,158,11,0.3); display:inline-block;'>{html_lib.escape(raw_val)}</span>"
            elif "🔴" in raw_val or "CRITICAL" in raw_val:
                cell_content = f"<span style='background:rgba(239,68,68,0.15); color:#F87171; padding:3px 8px; border-radius:4px; font-weight:700; border:1px solid rgba(239,68,68,0.3); display:inline-block;'>{html_lib.escape(raw_val)}</span>"
            elif "⭐" in raw_val:
                cell_content = f"<span style='color:#FBBF24; font-weight:600;'>{html_lib.escape(raw_val)}</span>"
            elif "✅" in raw_val and "STP" not in raw_val:
                cell_content = f"<span style='background:rgba(16,185,129,0.12); color:#10B981; padding:2px 6px; border-radius:4px; font-weight:600; display:inline-block;'>{html_lib.escape(raw_val)}</span>"
            elif "⚠️" in raw_val and "STP" not in raw_val:
                cell_content = f"<span style='background:rgba(245,158,11,0.12); color:#F59E0B; padding:2px 6px; border-radius:4px; font-weight:600; display:inline-block;'>{html_lib.escape(raw_val)}</span>"
            elif raw_val.startswith("₹"):
                cell_content = f"<span style='color:#38BDF8; font-weight:600;'>{html_lib.escape(raw_val)}</span>"
            elif raw_val.startswith("http://") or raw_val.startswith("https://"):
                url_lower = raw_val.lower()
                if "google.com/maps" in url_lower:
                    link_label = "Google Maps ↗"
                    btn_bg = "#1D4ED8"
                elif "rera.karnataka.gov.in" in url_lower:
                    link_label = "K-RERA Portal ↗"
                    btn_bg = "#0F766E"
                elif "maharera.mahaonline.gov.in" in url_lower:
                    link_label = "MahaRERA ↗"
                    btn_bg = "#B45309"
                elif "rera.tn.gov.in" in url_lower:
                    link_label = "TN-RERA ↗"
                    btn_bg = "#047857"
                elif "up-rera.in" in url_lower:
                    link_label = "UP-RERA ↗"
                    btn_bg = "#7C3AED"
                elif "rera.telangana.gov.in" in url_lower:
                    link_label = "TS-RERA ↗"
                    btn_bg = "#C2410C"
                elif "haryanarera.gov.in" in url_lower or "punjab.gov.in" in url_lower:
                    link_label = "RERA Portal ↗"
                    btn_bg = "#0284C7"
                elif "rera.goa.gov.in" in url_lower:
                    link_label = "Goa-RERA ↗"
                    btn_bg = "#0D9488"
                elif "github.com" in url_lower:
                    link_label = "GitHub Reference ↗"
                    btn_bg = "#24292F"
                else:
                    link_label = "Official Link ↗"
                    btn_bg = "#334155"

                cell_content = f"<a href='{html_lib.escape(raw_val)}' target='_blank' rel='noreferrer noopener' style='background:{btn_bg}; color:#FFFFFF; padding:4px 10px; border-radius:4px; text-decoration:none; font-weight:700; font-size:0.76rem; display:inline-block; border:1px solid rgba(255,255,255,0.2);'>{link_label}</a>"
            else:
                cell_content = html_lib.escape(raw_val)

            html_parts.append(f"<td{col_class}>{cell_content}</td>")
        html_parts.append("</tr>")

    # Native Client-side JS Sorter for table headers
    js_sorter = f"""
    <script>
    (function() {{
        const tbl = document.getElementById('{table_id}');
        if (!tbl) return;
        const ths = tbl.querySelectorAll('thead th');
        let currentSortIdx = -1;
        let isAsc = true;

        ths.forEach((th, idx) => {{
            th.addEventListener('click', function() {{
                const tbody = tbl.querySelector('tbody');
                const rows = Array.from(tbody.querySelectorAll('tr'));
                if (rows.length === 0) return;

                if (currentSortIdx === idx) {{
                    isAsc = !isAsc;
                }} else {{
                    currentSortIdx = idx;
                    isAsc = true;
                }}

                // Reset all icon spans
                ths.forEach((otherTh, oIdx) => {{
                    const icon = otherTh.querySelector('.sort-icon');
                    if (icon) {{
                        if (oIdx === idx) {{
                            icon.innerHTML = isAsc ? '▲' : '▼';
                            icon.style.color = '#38BDF8';
                        }} else {{
                            icon.innerHTML = '⇅';
                            icon.style.color = '#94A3B8';
                        }}
                    }}
                }});

                rows.sort((rowA, rowB) => {{
                    const tdA = rowA.children[idx];
                    const tdB = rowB.children[idx];
                    const valA = tdA ? tdA.innerText.trim() : '';
                    const valB = tdB ? tdB.innerText.trim() : '';

                    // Clean numerical strings
                    const cleanA = valA.replace(/[₹,$,L,Cr,%,⭐,/,km,Mn,L\\/Acre,Acres,yrs,yr,old,mos,mo]/gi, '').trim();
                    const cleanB = valB.replace(/[₹,$,L,Cr,%,⭐,/,km,Mn,L\\/Acre,Acres,yrs,yr,old,mos,mo]/gi, '').trim();

                    const numA = parseFloat(cleanA);
                    const numB = parseFloat(cleanB);

                    if (!isNaN(numA) && !isNaN(numB) && cleanA !== '' && cleanB !== '') {{
                        return isAsc ? (numA - numB) : (numB - numA);
                    }}
                    return isAsc ? valA.localeCompare(valB, undefined, {{numeric: true}}) : valB.localeCompare(valA, undefined, {{numeric: true}});
                }});

                rows.forEach(r => tbody.appendChild(r));
            }});
        }});
    }})();
    </script>
    """

    html_parts.extend([
        "</tbody>",
        "</table>",
        "</div>",
        js_sorter,
        "</body>",
        "</html>"
    ])

    full_html = "\n".join(html_parts)
    components.html(full_html, height=calc_height, scrolling=True)
