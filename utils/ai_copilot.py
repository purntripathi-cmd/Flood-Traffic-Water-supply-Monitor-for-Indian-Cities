"""
Explainable AI Avoidance Copilot & Multi-Criteria Screener
Synthesizes topographical flood data, traffic congestion telemetry, and water supply metrics
to answer user queries and generate executive screening briefs.
"""

from typing import List, Dict, Any


def run_avoidance_copilot_query(
    user_query: str,
    city_id: str,
    micro_markets: List[Dict[str, Any]],
    builders: List[Dict[str, Any]],
    properties: List[Dict[str, Any]],
    avoidance_zones: List[Dict[str, Any]]
) -> str:
    """
    Analyzes user queries using deterministic multi-parameter pattern matching and dataset synthesis.
    Returns clear, explainable, evidence-backed advice with citations.
    """
    q = user_query.lower().strip()

    # Query 1: Avoidance zones / Chronic flood areas
    if any(k in q for k in ["avoid", "flood", "waterlog", "submerge", "danger", "safe", "risk"]):
        resilient = [m for m in micro_markets if m["city_id"] == city_id and m["composite_avoidance_score"] >= 75]
        avoid_list = [m for m in micro_markets if m["city_id"] == city_id and m["composite_avoidance_score"] < 55]
        
        response = f"### 🛡️ AI Risk Screening & Avoidance Synthesis for **{city_id.replace('_', ' ').title()}**\n\n"
        
        if avoid_list:
            response += "#### 🔴 High-Risk Avoidance Zones (Flagged by Topography & Historic Flood Logs):\n"
            for m in avoid_list:
                response += f"- **{m['name']}** (Avoidance Score: `{m['composite_avoidance_score']}/100`)\n"
                response += f"  - *Flood Risk Category*: {m['flood_risk_category']}\n"
                response += f"  - *Elevation Datum*: {m['elevation_vs_basin']} (Elevation: {m['elevation_m']}m)\n"
                response += f"  - *Primary Constraint*: {m['swd_drainage_status']}\n"
                response += f"  - *Citations*: `{m['civic_citation']}`\n\n"
        
        if resilient:
            response += "#### 🟢 Recommended Resilient Havens (High Plinth & Superior Drainage):\n"
            for m in resilient[:3]:
                response += f"- **{m['name']}** (Viability Score: `{m['composite_avoidance_score']}/100` | Delay: `{m['traffic_delay_index']}x` | Water Score: `{m['water_supply_score']}/100`)\n"
                response += f"  - *Top Active Builders*: {', '.join(m['top_builders_active'])}\n"
        
        return response

    # Query 2: Builder comparison / Best builder
    elif any(k in q for k in ["builder", "developer", "reputation", "delivery", "quality", "rera"]):
        city_builders = [b for b in builders if any(city_id.lower() in s.lower() for s in b["active_states_and_cities"])]
        if not city_builders:
            city_builders = builders[:5]

        # Sort by RERA compliance and on-time delivery
        sorted_b = sorted(city_builders, key=lambda x: (x["on_time_delivery_pct"], x["construction_quality_rating"]), reverse=True)
        
        response = f"### 🏗️ AI Builder Pedigree & RERA Delivery Radar\n\n"
        response += "| Builder Name | Tier | RERA On-Time % | Quality (1-10) | Litigation Risk | Official Portal |\n"
        response += "| :--- | :--- | :--- | :--- | :--- | :--- |\n"
        for b in sorted_b[:6]:
            response += f"| **{b['name']}** | {b['tier']} | `{b['on_time_delivery_pct']}%` | `{b['construction_quality_rating']}/10` | `{b['litigation_index']}` | [Official RERA ↗]({b['rera_portal_url']}) |\n"
        
        response += "\n> [!TIP]\n> **AI Recommendation**: Tier 1 National and Regional leaders like Sobha, Prestige, Godrej, Oberoi, and Eldeco maintain in-house batching plants, German precast lines, and institutional escrow accounts that safeguard handover schedules.\n"
        return response

    # Query 3: Water supply & Tanker reliance
    elif any(k in q for k in ["water", "cauvery", "bmc", "djb", "tanker", "borewell", "piped", "tds"]):
        city_props = [p for p in properties if p["city_id"] == city_id]
        
        response = f"### 💧 Water Security & Ground Reality Report\n\n"
        response += "Evaluating municipal piped connections, water softener presence, STP treatment, and private tanker dependency:\n\n"
        for p in city_props[:4]:
            ws = p["water_supply"]
            response += f"- **{p['name']}** ({p['builder_name']})\n"
            response += f"  - *Piped Connection*: `{ws.get('piped_connection', 'N/A')}`\n"
            response += f"  - *Water Softener*: `{ws.get('water_softener', 'N/A')}`\n"
            response += f"  - *STP & Dual Piping*: `{ws.get('stp_treatment', 'N/A')}`\n"
            response += f"  - *Summer Tanker Reliance*: `{ws.get('tanker_reliance', 'N/A')}`\n\n"
        
        response += "> [!NOTE]\n> Properties connected to dual-piping STPs and municipal piped bulk supply (BWSSB / BMC / CMWSSB / DJB / HMWSSB / Jal Sansthan) reduce monthly maintenance exposure by ₹3,000 to ₹7,000 per household compared to private tanker dependency.\n"
        return response

    # Default overview
    else:
        return f"""### 🤖 AI Civic Intelligence Summary for **{city_id.replace('_', ' ').title()}**

1. **Topographical Risk**: Consult Tab 1 (Geospatial Risk Map) to verify elevation contours and proximity to historical water overflow basins.
2. **Commute Friction**: Check Tab 2 (Micro-Market Radar) for Peak-to-Free-Flow delay indices (`1.0x` is ideal; `>2.2x` indicates severe peak gridlock).
3. **Piped Water & Sewage Treatment**: Inspect Tab 5 (Water Supply Monitor) to confirm municipal supply authorization and on-site STP dual-piping.
4. **Developer Pedigree**: Filter Tab 3 (Top Builders) for verified RERA compliance and structural durability track records.
5. **Pre-Filtered Screening**: Use Tab 4 (Property Screener) with configurable budget limits (Default: ₹80,000/mo rent and ₹3.50 Cr purchase).
"""
