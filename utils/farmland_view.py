"""
Farmland & Agro-Investment Screener Engine
Provides interactive agronomic telemetry, crop suitability matchers,
soil health cards, seller/broker contact modals, and high-value crop ROI calculators.
"""

from typing import List, Dict, Any
import pandas as pd


# High-value crop benchmark economics for the ROI calculator
HIGH_VALUE_CROP_BENCHMARKS = {
    "Hass Avocado": {
        "trees_per_acre": 160,
        "gestation_years": 3.5,
        "annual_yield_per_tree_kg": 75,
        "farmgate_price_per_kg": 180,
        "est_annual_gross_lakhs": 21.6,
        "description": "High export demand, requires well-drained sandy loam soil (pH 6.0-7.0), zero waterlogging."
    },
    "Dragon Fruit (Pitaya)": {
        "trees_per_acre": 450,  # RCC poles with 4 vines each = 1800 vines
        "gestation_years": 1.5,
        "annual_yield_per_tree_kg": 20,
        "farmgate_price_per_kg": 120,
        "est_annual_gross_lakhs": 10.8,
        "description": "Cactus family, drought-resilient, rapid harvest within 18 months, thrives in gravelly red loam."
    },
    "Certified Sandalwood (Chandan)": {
        "trees_per_acre": 300,
        "gestation_years": 15.0,
        "annual_yield_per_tree_kg": 25,  # Heartwood yield at harvest
        "farmgate_price_per_kg": 8500,
        "est_annual_gross_lakhs": 42.5,  # Amortized over 15 years (~6 Cr total harvest)
        "description": "Premium commercial timber, state-permitted harvesting with transit passes, host plants required."
    },
    "High-Density Guava (Taiwan Pink)": {
        "trees_per_acre": 700,
        "gestation_years": 2.0,
        "annual_yield_per_tree_kg": 25,
        "farmgate_price_per_kg": 45,
        "est_annual_gross_lakhs": 7.8,
        "description": "Year-round fruit bearing, high domestic demand, responds excellently to drip fertigation."
    },
    "Alphonso / Banganapalli Mango Orchard": {
        "trees_per_acre": 80,
        "gestation_years": 4.0,
        "annual_yield_per_tree_kg": 90,
        "farmgate_price_per_kg": 80,
        "est_annual_gross_lakhs": 5.7,
        "description": "Classic evergreen orchard, generational appreciation, intercropping possible with pulses & spices."
    },
    "Protected Greenhouse (Exotic Mushrooms & English Greens)": {
        "trees_per_acre": 1,  # Polyhouse structure
        "gestation_years": 0.5,
        "annual_yield_per_tree_kg": 1,
        "farmgate_price_per_kg": 1,
        "est_annual_gross_lakhs": 14.5,
        "description": "Controlled climate polyhouse with climate automation; high initial capex, fastest turnaround."
    }
}


def render_seller_contact_card_html(farm: Dict[str, Any]) -> str:
    """Renders a styled seller/broker contact card with WhatsApp and direct call triggers."""
    is_owner = "Owner" in farm.get("seller_category", "")
    badge_bg = "#059669" if is_owner else ("#2563EB" if "Broker" in farm.get("seller_category", "") else "#7C3AED")
    badge_label = "🧑‍🌾 DIRECT LANDOWNER" if is_owner else ("🏢 VERIFIED AGRO BROKER" if "Broker" in farm.get("seller_category", "") else "🏡 MANAGED FARMLAND OPERATOR")

    clean_phone = farm.get("contact_phone", "").replace(" ", "").replace("-", "")
    wa_url = farm.get("contact_whatsapp", f"https://wa.me/{clean_phone}")

    html = f"""
    <div style="background-color: #1E293B; border: 1px solid #334155; border-radius: 10px; padding: 16px; margin: 10px 0; color: #F8FAFC;">
        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px;">
            <span style="background-color: {badge_bg}; color: #FFFFFF; font-size: 11px; font-weight: bold; padding: 3px 8px; border-radius: 4px; letter-spacing: 0.5px;">
                {badge_label}
            </span>
            <span style="font-size: 12px; color: #34D399; font-weight: 600;">
                {farm.get('verified_listing_badge', '✅ Verified Listing')}
            </span>
        </div>
        <h4 style="margin: 4px 0 2px 0; font-size: 16px; color: #38BDF8;">{farm.get('contact_person', 'Land Contact')}</h4>
        <p style="margin: 0 0 10px 0; font-size: 12px; color: #94A3B8;">{farm.get('agency_or_firm', 'Agricultural Representative')}</p>
        
        <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 8px; margin-bottom: 12px; font-size: 12px;">
            <div style="background: #0F172A; padding: 6px 10px; border-radius: 6px;">
                <span style="color: #64748B;">Parcel Extent:</span> <b>{farm.get('size_local_units', f"{farm.get('size_acres')} Acres")}</b>
            </div>
            <div style="background: #0F172A; padding: 6px 10px; border-radius: 6px;">
                <span style="color: #64748B;">Rate/Acre:</span> <b style="color: #34D399;">₹{farm.get('price_per_acre_lakhs')} L/Acre</b>
            </div>
        </div>

        <div style="display: flex; gap: 8px;">
            <a href="tel:{clean_phone}" style="flex: 1; text-align: center; background: #0D9488; color: white; padding: 8px 12px; border-radius: 6px; text-decoration: none; font-size: 12px; font-weight: 600;">
                📞 Call {farm.get('contact_phone')}
            </a>
            <a href="{wa_url}" target="_blank" style="flex: 1; text-align: center; background: #16A34A; color: white; padding: 8px 12px; border-radius: 6px; text-decoration: none; font-size: 12px; font-weight: 600;">
                💬 WhatsApp Chat ↗
            </a>
        </div>
    </div>
    """
    return html


def render_agronomic_telemetry_html(farm: Dict[str, Any]) -> str:
    """Renders soil, water, and crop suitability scorecard."""
    supp = farm.get("supported_crops", {})
    html = f"""
    <div style="background-color: #0F172A; border: 1px solid #1E293B; border-radius: 8px; padding: 14px; font-size: 13px; color: #E2E8F0; line-height: 1.5;">
        <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(180px, 1fr)); gap: 10px; margin-bottom: 12px;">
            <div style="border-left: 3px solid #38BDF8; padding-left: 8px;">
                <div style="color: #94A3B8; font-size: 11px;">Soil Type & pH</div>
                <b>{farm.get('soil_type', 'Red Loam')}</b>
                <div style="font-size: 11px; color: #38BDF8;">pH: {farm.get('soil_ph')} • Org Carbon: {farm.get('organic_carbon_pct')}%</div>
            </div>
            <div style="border-left: 3px solid #34D399; padding-left: 8px;">
                <div style="color: #94A3B8; font-size: 11px;">Water Security & Yield</div>
                <b>{farm.get('water_source', 'Borewell')}</b>
                <div style="font-size: 11px; color: #34D399;">Water Table: {farm.get('groundwater_depth_ft')}ft • TDS: {farm.get('water_tds_ppm')} ppm (Sweet)</div>
            </div>
            <div style="border-left: 3px solid #F59E0B; padding-left: 8px;">
                <div style="color: #94A3B8; font-size: 11px;">Irrigation & Electricity</div>
                <b>{'Drip Installed ✅' if farm.get('drip_irrigation_installed') else 'Flood/Furrow ⚠️'}</b>
                <div style="font-size: 11px; color: #F59E0B;">{farm.get('power_supply')}</div>
            </div>
        </div>

        <div style="background: #1E293B; padding: 10px 12px; border-radius: 6px; margin-top: 8px;">
            <div style="color: #38BDF8; font-weight: 600; margin-bottom: 4px;">🌟 Supported High-Value Crops & Horticulture:</div>
            <div><b style="color: #34D399;">High-Value / Exotic:</b> {supp.get('high_value_crops', 'N/A')}</div>
            <div style="margin-top: 3px;"><b style="color: #FBBF24;">Horticulture & Fruits:</b> {supp.get('horticulture_fruits', 'N/A')}</div>
            <div style="margin-top: 3px;"><b style="color: #94A3B8;">Cash Crops / Staples:</b> {supp.get('cash_crops_staples', 'N/A')}</div>
            <div style="margin-top: 6px; font-size: 12px; color: #A7F3D0;">
                <b>📈 Projected Annual Harvest Revenue:</b> ~₹{farm.get('annual_agro_yield_estimate_lakhs', 4.5)} Lakhs / year
            </div>
        </div>

        <div style="margin-top: 10px; font-size: 12px; color: #CBD5E1;">
            <b>📜 Title & Legal Status:</b> {farm.get('title_status')} ({farm.get('revenue_record_type')})<br>
            <b>🏡 Farmhouse Allowance:</b> {farm.get('farmhouse_permission')}<br>
            <b>🛣️ Approach Road:</b> {farm.get('road_approach')} | <b>🛡️ Boundary:</b> {farm.get('fencing')}
        </div>
    </div>
    """
    return html
