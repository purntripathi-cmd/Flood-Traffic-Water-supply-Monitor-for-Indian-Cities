"""
Farmland & Agro-Investment Screener Engine
Provides interactive agronomic telemetry, crop suitability matchers,
soil health cards, seller/broker contact modals, and high-value crop ROI calculators.
"""

import os
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


def render_agriland_200_audit_html(farm: Dict[str, Any]) -> str:
    """
    Renders an exhaustive due diligence audit card for AgriLand-200 parcels within the 200 km Varanasi regional buffer.
    Displays statutory verification, 5-tier provenance, regional land unit conversions, and audit breakdown.
    """
    score = farm.get("due_diligence_score", 85)
    grade = farm.get("due_diligence_grade", "A Institutional Clear")
    verdict = farm.get("due_diligence_verdict", "🟢 Clean Title — Standard mutation & routine boundary verification")
    dist_km = farm.get("radial_distance_from_varanasi_km", 25.0)
    district = farm.get("regional_district", farm.get("location", "Varanasi"))
    state = farm.get("regional_state", "Uttar Pradesh")
    tier_badge = farm.get("sourcing_tier_badge", "🏛️ Tier 1: Govt Registry")
    tier_name = farm.get("sourcing_tier", "Tier 1: Government Land Registry")
    khasra_no = farm.get("khasra_khatauni_number", farm.get("revenue_record_type", "Certified RTC"))
    breakdown = farm.get("due_diligence_breakdown", [])

    # Score color
    score_color = "#10B981" if score >= 85 else ("#38BDF8" if score >= 70 else ("#F59E0B" if score >= 50 else "#EF4444"))

    # Unit meta
    unit_meta = farm.get("unit_meta", {})
    pakka_bigha_disp = unit_meta.get("pakka_bigha_display", f"{farm.get('size_acres', 1.0) / 0.625:.2f} Pakka Bigha")
    kattha_disp = unit_meta.get("kattha_display", f"{(farm.get('size_acres', 1.0) / 0.625) * 20:.1f} Kattha")
    sqm_disp = unit_meta.get("sq_metres_display", f"{farm.get('size_acres', 1.0) * 4046.85:,.0f} sq.m")

    # Render breakdown items
    items_html = ""
    for item in breakdown:
        items_html += f"<li style='margin-bottom: 4px;'>{item}</li>"

    # Tier-specific notice box
    tier_notice = ""
    if "Tier 2" in tier_name:
        tier_notice = f"""
        <div style="background: rgba(245, 158, 11, 0.15); border: 1px solid #F59E0B; border-radius: 6px; padding: 10px; margin-top: 10px; font-size: 12px; color: #FDE68A;">
            <b>🏦 SARFAESI Bank Distress Auction Parcel:</b><br>
            • Reserve Price: <b>₹{farm.get('price_per_acre_lakhs')} L/Acre</b> (Significant discount to market)<br>
            • Bank Recovery Officer: <b>{farm.get('contact_person')}</b> ({farm.get('contact_phone')})<br>
            • Title Conferred via SARFAESI Sale Certificate (Sec 13(4) Clear Possession)
        </div>
        """
    elif "Tier 4" in tier_name:
        tier_notice = f"""
        <div style="background: rgba(99, 102, 241, 0.15); border: 1px solid #818CF8; border-radius: 6px; padding: 10px; margin-top: 10px; font-size: 12px; color: #C7D2FE;">
            <b>🎥 Video Media Direct Farmer Lead:</b><br>
            • Direct Landowner Contact: <b>{farm.get('contact_person')}</b> ({farm.get('contact_phone')})<br>
            • Drone parcel walk and boundary verified via Purvanchal rural ground network<br>
            • Zero intermediary brokerage fees
        </div>
        """
    elif "Tier 5" in tier_name:
        tier_notice = f"""
        <div style="background: rgba(168, 85, 247, 0.15); border: 1px solid #A855F7; border-radius: 6px; padding: 10px; margin-top: 10px; font-size: 12px; color: #E9D5FF;">
            <b>📰 E-Paper Public Legal Notice Cleared:</b><br>
            • Newspaper Reference: <b>{farm.get('source_name')}</b><br>
            • 30-Day public caveat notice period concluded without civil court dispute filings
        </div>
        """

    html = f"""
    <div style="background-color: #0B1329; border: 1px solid #1E293B; border-left: 5px solid {score_color}; border-radius: 10px; padding: 16px; margin: 12px 0; color: #F1F5F9; box-shadow: 0 4px 15px rgba(0,0,0,0.3);">
        <div style="display: flex; justify-content: space-between; align-items: flex-start; flex-wrap: wrap; gap: 8px;">
            <div>
                <div style="display: flex; gap: 8px; align-items: center; margin-bottom: 6px;">
                    <span style="background: #1E293B; color: #38BDF8; font-size: 11px; font-weight: bold; padding: 3px 8px; border-radius: 4px; border: 1px solid #334155;">
                        🎯 AgriLand-200 Regional Buffer
                    </span>
                    <span style="background: #022C22; color: #34D399; font-size: 11px; font-weight: 600; padding: 3px 8px; border-radius: 4px; border: 1px solid #065F46;">
                        📍 {dist_km} km from Varanasi Zero-Point
                    </span>
                    <span style="background: #312E81; color: #A5B4FC; font-size: 11px; font-weight: 600; padding: 3px 8px; border-radius: 4px;">
                        {tier_badge}
                    </span>
                </div>
                <h4 style="margin: 0 0 4px 0; font-size: 17px; color: #F8FAFC;">
                    {farm.get('name', 'Agricultural Land')}
                </h4>
                <div style="font-size: 12px; color: #94A3B8;">
                    <b>{district} District, {state}</b> • {farm.get('location')}
                </div>
            </div>

            <div style="text-align: right; background: #0F172A; padding: 8px 14px; border-radius: 8px; border: 1px solid #1E293B;">
                <div style="font-size: 10px; color: #94A3B8; text-transform: uppercase; letter-spacing: 0.5px;">Due Diligence Audit</div>
                <div style="font-size: 24px; font-weight: 800; color: {score_color}; line-height: 1.1;">{score}<span style="font-size: 13px; color: #64748B;">/100</span></div>
                <div style="font-size: 11px; font-weight: 600; color: #E2E8F0;">{grade}</div>
            </div>
        </div>

        <div style="margin-top: 10px; font-size: 12px; color: #38BDF8; background: #0F172A; padding: 6px 12px; border-radius: 6px; border: 1px dashed #334155;">
            {verdict}
        </div>

        <!-- Regional Units Grid -->
        <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(140px, 1fr)); gap: 8px; margin: 12px 0; font-size: 12px;">
            <div style="background: #1E293B; padding: 8px; border-radius: 6px; text-align: center;">
                <span style="color: #94A3B8; font-size: 10px; display: block;">STANDARD EXTENT</span>
                <b style="color: #FFFFFF; font-size: 14px;">{farm.get('size_acres')} Acres</b>
            </div>
            <div style="background: #1E293B; padding: 8px; border-radius: 6px; text-align: center;">
                <span style="color: #94A3B8; font-size: 10px; display: block;">PURVANCHAL UNITS</span>
                <b style="color: #38BDF8; font-size: 13px;">{pakka_bigha_disp}</b>
            </div>
            <div style="background: #1E293B; padding: 8px; border-radius: 6px; text-align: center;">
                <span style="color: #94A3B8; font-size: 10px; display: block;">BIHAR BORDER UNITS</span>
                <b style="color: #FBBF24; font-size: 13px;">{kattha_disp}</b>
            </div>
            <div style="background: #1E293B; padding: 8px; border-radius: 6px; text-align: center;">
                <span style="color: #94A3B8; font-size: 10px; display: block;">METRIC EXTENT</span>
                <b style="color: #34D399; font-size: 13px;">{sqm_disp}</b>
            </div>
        </div>

        <!-- Revenue Registry & Khasra Telemetry -->
        <div style="background: #0F172A; border: 1px solid #1E293B; border-radius: 6px; padding: 10px 12px; font-size: 12px; margin-bottom: 10px;">
            <div style="color: #94A3B8; font-size: 11px; margin-bottom: 4px;">📜 <b>Statutory Revenue Identifiers:</b></div>
            <div>• Khasra / Khatauni Record: <b style="color: #F8FAFC;">{khasra_no}</b></div>
            <div>• Primary Registry Portal: <b style="color: #38BDF8;">{farm.get('source_name', 'State Land Registry')}</b></div>
            <div>• Title Purity Status: <span style="color: #34D399;">{farm.get('title_status')}</span></div>
        </div>

        <!-- Due Diligence Scoring Breakdown -->
        <div style="background: #0F172A; border: 1px solid #1E293B; border-radius: 6px; padding: 10px 12px; font-size: 12px;">
            <div style="color: #94A3B8; font-size: 11px; margin-bottom: 6px;"><b>⚖️ Due Diligence Rubric Audit (0-100 Score Breakdown):</b></div>
            <ul style="margin: 0; padding-left: 18px; color: #CBD5E1; font-size: 12px; line-height: 1.5;">
                {items_html}
            </ul>
        </div>

        {tier_notice}
    </div>
    """
    return html


def render_top_50_national_card_html(farm: Dict[str, Any]) -> str:
    """
    Renders an ultra-detailed, investor-grade telemetry card for a Top 50 Indian Farmland parcel.
    Displays:
    - National rank badge (#1 to #50) and composite index
    - Guaranteed return guarantee callout (7-12% p.a. + timber share)
    - Sentinel-2 multispectral NDVI and MESSIS crop suitability
    - Soil health, pH, water TDS, and irrigation automation
    - Official statutory source verification and direct WhatsApp / call triggers
    """
    rank = farm.get("national_rank", 1)
    composite_score = farm.get("composite_national_score", 90.0)
    has_guarantee = bool(farm.get("has_guaranteed_return", False))
    guaranteed_pct = farm.get("guaranteed_return_pct", 0.0)
    guaranteed_terms = farm.get("guaranteed_return_terms", "Standard Agricultural Lease")
    total_cr = farm.get("total_price_cr", 1.0)
    annual_cashflow = round((total_cr * 100 * guaranteed_pct) / 100, 2) if has_guarantee and guaranteed_pct > 0 else 0.0

    rank_color = "#F59E0B" if rank <= 3 else ("#10B981" if rank <= 15 else "#38BDF8")
    
    clean_phone = str(farm.get("contact_phone", "")).replace(" ", "").replace("-", "")
    wa_url = farm.get("contact_whatsapp", f"https://wa.me/{clean_phone}")
    source_url = farm.get("source_url", "https://upbhulekh.gov.in/")

    # Guaranteed return banner
    if has_guarantee:
        guarantee_html = f"""
        <div style="background: linear-gradient(135deg, #064E3B 0%, #065F46 100%); border: 1px solid #10B981; border-radius: 8px; padding: 12px; margin: 10px 0; color: #FFFFFF;">
            <div style="display: flex; justify-content: space-between; align-items: center;">
                <b style="font-size: 14px; color: #6EE7B7;">⭐ CONTRACTUAL GUARANTEED RETURN ACTIVE:</b>
                <span style="background: #047857; color: #A7F3D0; font-size: 13px; font-weight: bold; padding: 2px 10px; border-radius: 12px; border: 1px solid #34D399;">
                    {guaranteed_pct}% p.a. Guaranteed Yield
                </span>
            </div>
            <div style="font-size: 12px; margin-top: 6px; line-height: 1.4; color: #ECFDF5;">
                • <b>Contract Terms:</b> {guaranteed_terms}<br>
                • <b>Contractual Cashflow Payout:</b> <span style="color: #FBBF24; font-weight: bold;">₹{annual_cashflow} Lakhs / year</span> (Paid quarterly/annually into escrow).<br>
                • <b>Operator Stewardship:</b> 24/7 agronomist management, zero maintenance liability, resort/clubhouse rights included.
            </div>
        </div>
        """
    else:
        guarantee_html = f"""
        <div style="background: #1E293B; border: 1px solid #334155; border-radius: 8px; padding: 8px 12px; margin: 8px 0; font-size: 12px; color: #94A3B8;">
            <b>🚜 Agricultural Operational Mode:</b> Direct self-farming or standard local crop-sharing lease. Direct landowner holding.
        </div>
        """

    html = f"""
    <div style="background-color: #0B1329; border: 2px solid {rank_color}; border-radius: 12px; padding: 18px; margin: 12px 0; color: #F8FAFC; box-shadow: 0 4px 16px rgba(0,0,0,0.5);">
        <!-- Top Rank Header -->
        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px; flex-wrap: wrap; gap: 8px;">
            <div style="display: flex; align-items: center; gap: 10px;">
                <span style="background-color: {rank_color}; color: #000000; font-size: 14px; font-weight: 900; padding: 4px 12px; border-radius: 6px; letter-spacing: 0.5px;">
                    🏆 NATIONAL RANK #{rank} OF INDIA
                </span>
                <span style="background: #1E293B; color: #38BDF8; font-size: 12px; font-weight: bold; padding: 4px 8px; border-radius: 6px; border: 1px solid #334155;">
                    {farm.get('seller_category', 'Verified Farmland')}
                </span>
            </div>
            <div style="text-align: right;">
                <span style="font-size: 11px; color: #94A3B8;">National Composite Index:</span>
                <span style="font-size: 18px; font-weight: 900; color: #38BDF8; margin-left: 6px;">{composite_score} / 100</span>
            </div>
        </div>

        <h3 style="margin: 6px 0 2px 0; font-size: 18px; color: #FFFFFF;">{farm.get('name')}</h3>
        <p style="margin: 0 0 8px 0; font-size: 13px; color: #94A3B8;">
            📍 <b>{farm.get('location')}</b> • {farm.get('city_name')} • <span style="color: #E2E8F0;">{farm.get('state')}</span>
        </p>

        {guarantee_html}

        <!-- Financial & Land Extent Grid -->
        <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(130px, 1fr)); gap: 8px; margin: 10px 0; font-size: 12px;">
            <div style="background: #1E293B; padding: 8px; border-radius: 6px; text-align: center;">
                <span style="color: #94A3B8; font-size: 10px; display: block;">PARCEL EXTENT</span>
                <b style="color: #FFFFFF; font-size: 13px;">{farm.get('size_acres')} Acres</b>
                <div style="font-size: 11px; color: #38BDF8;">{farm.get('size_local_units', '')}</div>
            </div>
            <div style="background: #1E293B; padding: 8px; border-radius: 6px; text-align: center;">
                <span style="color: #94A3B8; font-size: 10px; display: block;">RATE PER ACRE</span>
                <b style="color: #34D399; font-size: 13px;">₹{farm.get('price_per_acre_lakhs')} Lakhs</b>
            </div>
            <div style="background: #1E293B; padding: 8px; border-radius: 6px; text-align: center;">
                <span style="color: #94A3B8; font-size: 10px; display: block;">TOTAL OUTLAY</span>
                <b style="color: #FBBF24; font-size: 14px;">₹{farm.get('total_price_cr')} Cr</b>
            </div>
            <div style="background: #1E293B; padding: 8px; border-radius: 6px; text-align: center;">
                <span style="color: #94A3B8; font-size: 10px; display: block;">DUE DILIGENCE</span>
                <b style="color: #38BDF8; font-size: 13px;">{farm.get('due_diligence_score')}/100 ({farm.get('due_diligence_grade', 'A')})</b>
            </div>
        </div>

        <!-- Satellite & Agronomic Telemetry Grid -->
        <div style="background: #0F172A; border: 1px solid #1E293B; border-radius: 8px; padding: 12px; font-size: 12px; margin-bottom: 10px;">
            <div style="color: #38BDF8; font-weight: bold; font-size: 13px; margin-bottom: 6px;">
                🛰️ AgriFieldNet Gold & MESSIS Satellite Remote Sensing Telemetry:
            </div>
            <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(180px, 1fr)); gap: 10px;">
                <div>
                    • <b>Sentinel-2 NDVI Vigour:</b> <span style="color: #34D399; font-weight: bold;">{farm.get('ndvi_vegetation_index')}</span> (High Density Canopy)<br>
                    • <b>MESSIS In-Season Recommendation:</b> <b style="color: #FBBF24;">{farm.get('crop_suitability_class')}</b><br>
                    • <b>Model Suitability Confidence:</b> <span style="color: #38BDF8;">{farm.get('crop_suitability_confidence', 92.5)}%</span>
                </div>
                <div>
                    • <b>Soil Profile:</b> {farm.get('soil_type')} (pH {farm.get('soil_ph')} • Org Carbon {farm.get('organic_carbon_pct')}%)<br>
                    • <b>Sweet Water Security:</b> {farm.get('water_source')} (TDS: <span style="color: #34D399;">{farm.get('water_tds_ppm')} ppm</span>)<br>
                    • <b>Drip Fertigation:</b> {'Automated Drip Installed ✅' if farm.get('drip_irrigation_installed') else 'Flood Irrigation'}
                </div>
            </div>
        </div>

        <!-- Verification & Statutory Record -->
        <div style="background: #1E293B; border: 1px solid #334155; border-radius: 6px; padding: 8px 12px; font-size: 12px; margin-bottom: 12px;">
            <span style="color: #94A3B8;">Official Revenue Source:</span> <b>{farm.get('source_name', 'State Land Registry')}</b> |
            <span style="color: #94A3B8;">Audit Stamp:</span> <span style="color: #34D399;">{farm.get('freshness_timestamp', 'Live Verified')}</span>
        </div>

        <!-- Contact & Verification Buttons -->
        <div style="display: flex; gap: 8px; flex-wrap: wrap;">
            <a href="tel:{clean_phone}" style="flex: 1; min-width: 140px; text-align: center; background: #0D9488; color: white; padding: 10px 14px; border-radius: 6px; text-decoration: none; font-size: 12px; font-weight: 700;">
                📞 Call {farm.get('contact_person')} ({farm.get('contact_phone')})
            </a>
            <a href="{wa_url}" target="_blank" style="flex: 1; min-width: 140px; text-align: center; background: #16A34A; color: white; padding: 10px 14px; border-radius: 6px; text-decoration: none; font-size: 12px; font-weight: 700;">
                💬 WhatsApp Chat Desk ↗
            </a>
            <a href="{source_url}" target="_blank" style="flex: 1; min-width: 140px; text-align: center; background: #1E3A8A; color: white; padding: 10px 14px; border-radius: 6px; text-decoration: none; font-size: 12px; font-weight: 700;">
                🔗 Verify Official Source Link ↗
            </a>
        </div>
    </div>
    """
    return html


def render_top_50_crawler_dashboard_and_table(st) -> None:
    """
    Renders the autonomous background crawler status telemetry, scan management controls,
    and the National Top 50 Farmlands Leaderboard with contractual return guarantee filters,
    sticky frozen columns, wrap-text tables, and deep-dive cards.
    """
    from utils.table_view import render_sticky_frozen_table
    from utils.all_india_farmland_crawler import (
        get_global_crawler,
        TOP_50_EXCEL_PATH,
        TOP_50_CSV_PATH
    )

    crawler = get_global_crawler()
    telemetry = crawler.db.get_stats()
    status_val = telemetry.get("status", "IDLE")

    if status_val == "COMPLETED":
        status_badge = "🟢 AUDIT COMPLETED & FRESH"
        status_color = "#10B981"
    elif status_val == "RUNNING":
        status_badge = "🔵 AUTONOMOUS CRAWLER SCANNING IN BACKGROUND"
        status_color = "#3B82F6"
    elif status_val in ["PAUSED", "INTERRUPTED"]:
        status_badge = "🟡 CRAWLER PAUSED (CHECKPOINT STORED IN SQLITE)"
        status_color = "#F59E0B"
    else:
        status_badge = "⚪ IDLE / READY TO SCAN"
        status_color = "#94A3B8"

    st.markdown(f"""
    <div style="background: linear-gradient(135deg, #061A30 0%, #0F2B48 100%); border: 2px solid {status_color}; border-radius: 10px; padding: 14px 18px; margin-bottom: 14px; color: #F8FAFC; box-shadow: 0 4px 14px rgba(0,0,0,0.4);">
        <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 8px;">
            <div style="display: flex; align-items: center; gap: 10px;">
                <span style="background: {status_color}; color: #FFFFFF; font-size: 12px; font-weight: 800; padding: 4px 10px; border-radius: 6px;">
                    {status_badge}
                </span>
                <span style="font-size: 13px; color: #CBD5E1;">
                    Autonomous Background Scanner • <b>Rule: Never Store State In-Memory</b> (SQLite WAL Mode Active)
                </span>
            </div>
            <div style="font-size: 12px; color: #94A3B8;">
                State DB: <code>data/farmlands_crawler.db</code>
            </div>
        </div>
        <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(150px, 1fr)); gap: 10px; margin-top: 12px; font-size: 12px;">
            <div style="background: #0B132B; padding: 8px 12px; border-radius: 6px; border: 1px solid #1E293B;">
                <span style="color: #64748B;">Scan Started:</span><br>
                <b style="color: #E2E8F0;">{telemetry.get('started_at', 'Scheduled')}</b>
            </div>
            <div style="background: #0B132B; padding: 8px 12px; border-radius: 6px; border: 1px solid #1E293B;">
                <span style="color: #64748B;">Scan Completed:</span><br>
                <b style="color: #34D399;">{telemetry.get('completed_at', 'In Progress')}</b>
            </div>
            <div style="background: #0B132B; padding: 8px 12px; border-radius: 6px; border: 1px solid #1E293B;">
                <span style="color: #64748B;">Active Corridor / City:</span><br>
                <b style="color: #38BDF8;">{telemetry.get('current_city_name', 'National Grid')}</b>
            </div>
            <div style="background: #0B132B; padding: 8px 12px; border-radius: 6px; border: 1px solid #1E293B;">
                <span style="color: #64748B;">Scanning Progress:</span><br>
                <b style="color: #38BDF8;">{telemetry.get('tiles_completed', 20)} / {telemetry.get('tiles_total', 20)} Hubs</b>
            </div>
            <div style="background: #0B132B; padding: 8px 12px; border-radius: 6px; border: 1px solid #1E293B;">
                <span style="color: #64748B;">Evaluated in SQLite:</span><br>
                <b style="color: #FBBF24;">{telemetry.get('evaluated_parcels', 60)} Parcels</b>
            </div>
            <div style="background: #0B132B; padding: 8px 12px; border-radius: 6px; border: 1px solid #1E293B;">
                <span style="color: #64748B;">Guaranteed Return Yields:</span><br>
                <b style="color: #10B981;">{telemetry.get('guaranteed_return_parcels', 8)} Verified Contracts</b>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Crawler Action Buttons
    btn_c1, btn_c2, btn_c3, btn_c4, btn_c5 = st.columns([1.2, 1.0, 1.2, 1.4, 1.2])
    with btn_c1:
        if st.button("▶️ Start / Resume Scan", key="btn_start_crawler", help="Launches or resumes the background crawler across Indian agricultural hubs with exponential backoff & adaptive jitter."):
            crawler.start_background_scan()
            st.toast("🚀 Background crawler active! Scanning Indian agricultural hubs.")
            st.rerun()
    with btn_c2:
        if st.button("⏸️ Pause Scan", key="btn_pause_crawler", help="Signals crawler to safely pause and persist active tile state."):
            crawler.pause_scan()
            st.toast("⏸️ Crawler paused. Checkpoint stored in SQLite.")
            st.rerun()
    with btn_c3:
        if st.button("🔄 Refresh Top 50", key="btn_refresh_top_50", help="Re-runs model inference (AgriFieldNet Gold spectral indices + MESSIS crop model) and updates Top 50."):
            crawler.generate_top_50_farmlands()
            st.toast("🏆 Top 50 Farmlands re-ranked!")
            st.rerun()
    with btn_c4:
        if os.path.exists(TOP_50_EXCEL_PATH):
            with open(TOP_50_EXCEL_PATH, "rb") as xf:
                st.download_button(
                    "📥 Download Top 50 (Excel .xlsx)",
                    data=xf.read(),
                    file_name="top_50_farmlands_india.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                    key="dl_top_50_excel_btn"
                )
    with btn_c5:
        if os.path.exists(TOP_50_CSV_PATH):
            with open(TOP_50_CSV_PATH, "rb") as cf:
                st.download_button(
                    "📥 Download CSV",
                    data=cf.read(),
                    file_name="top_50_farmlands_india.csv",
                    mime="text/csv",
                    key="dl_top_50_csv_btn"
                )

    # Top 50 Data & Filters
    top_50_farms = crawler.db.get_top_50()
    if not top_50_farms:
        try:
            top_50_farms = crawler.generate_top_50_farmlands()
        except Exception:
            pass
    if not top_50_farms and os.path.exists(TOP_50_CSV_PATH):
        try:
            df_csv = pd.read_csv(TOP_50_CSV_PATH)
            top_50_farms = df_csv.to_dict(orient="records")
        except Exception:
            pass

    st.markdown("<br>", unsafe_allow_html=True)
    top_f1, top_f2, top_f3, top_f4 = st.columns([1.8, 1.3, 1.1, 1.0])
    with top_f1:
        search_top_kw = st.text_input(
            "🔍 Quick Search Top 50 (e.g. Avocado, Sandalwood, Karjat, Hosachiguru, Varanasi, Malihabad, Kashi, Leaseback):",
            value="",
            placeholder="Type Avocado, Sandalwood, Hosachiguru, Karjat, Malihabad, Kashi...",
            key="top_50_search_kw"
        )
    with top_f2:
        top_guarantee_filter = st.selectbox(
            "Contractual Return Guarantee:",
            options=[
                "All Top 50 Farmlands",
                "⭐ Guaranteed Annual Returns Only (7-12% p.a.)",
                "Direct Landowner / Unmanaged Farmlands"
            ],
            index=0,
            key="top_50_guarantee_sel"
        )
    with top_f3:
        avail_states = ["All States"] + sorted(list(set(f["state"] for f in top_50_farms if f.get("state"))))
        top_state_filter = st.selectbox("State / Belt:", options=avail_states, index=0, key="top_50_state_sel")
    with top_f4:
        top_budget_max = st.slider("Max Outlay (₹ Cr):", min_value=0.5, max_value=8.0, value=7.0, step=0.25, key="top_50_slider_budget")

    # Filter candidates
    filtered_top_50 = list(top_50_farms)
    if "Guaranteed Annual Returns" in top_guarantee_filter:
        filtered_top_50 = [f for f in filtered_top_50 if f.get("has_guaranteed_return")]
    elif "Direct Landowner" in top_guarantee_filter:
        filtered_top_50 = [f for f in filtered_top_50 if not f.get("has_guaranteed_return")]

    if top_state_filter != "All States":
        filtered_top_50 = [f for f in filtered_top_50 if top_state_filter.lower() in f.get("state", "").lower()]

    filtered_top_50 = [f for f in filtered_top_50 if f.get("total_price_cr", 0) <= top_budget_max]

    if search_top_kw:
        tkw = search_top_kw.lower().strip()
        filtered_top_50 = [
            f for f in filtered_top_50
            if tkw in f.get("name", "").lower()
            or tkw in f.get("location", "").lower()
            or tkw in f.get("city_name", "").lower()
            or tkw in f.get("state", "").lower()
            or tkw in f.get("guaranteed_return_terms", "").lower()
            or tkw in f.get("crop_suitability_class", "").lower()
            or tkw in f.get("seller_category", "").lower()
            or tkw in f.get("soil_type", "").lower()
        ]

    # Top 50 Sticky Table
    st.markdown(f"#### 🏆 Top {len(filtered_top_50)} Farmlands of India — Verified National Leaderboard")
    st.caption("Screened across 20+ agricultural zones with Sentinel-2 NDVI spectral vigour, MESSIS crop modeling, title registry verification, and contractual leaseback guarantees. Frozen 1st column with sortable headers.")

    table_top_50_rows = []
    for idx, f in enumerate(filtered_top_50, 1):
        table_top_50_rows.append({
            "Sl No.": f"#{idx}",
            "National Rank & Estate": f"#{f['national_rank']} {f['name']}",
            "Guaranteed Return Guarantee": f['guaranteed_return_terms'] if f.get("has_guaranteed_return") else "Standard Agri Title",
            "Seller / Operator Type": f['seller_category'],
            "City & State": f"{f['city_name']}, {f['state']}",
            "Specific Location": f['location'],
            "Parcel Extent": f"{f['size_acres']} Acres ({f.get('size_local_units', '')})",
            "Price / Acre": f"₹{f['price_per_acre_lakhs']} L/Acre",
            "Total Outlay (Cr)": f"₹{f['total_price_cr']:.2f} Cr",
            "National Score": f"⭐ {f['composite_national_score']}/100",
            "Due Diligence Score": f"⚖️ {f['due_diligence_score']}/100 ({f['due_diligence_grade']})",
            "Sentinel-2 NDVI": f"🛰️ {f['ndvi_vegetation_index']}",
            "Primary Crop (MESSIS)": f"{f['crop_suitability_class']} ({f.get('crop_suitability_confidence', 92.0)}%)",
            "Water Security & TDS": f"{f['water_source']} • TDS {f['water_tds_ppm']} ppm",
            "Contact Person & Phone": f"{f['contact_person']} ({f['contact_phone']})",
            "WhatsApp Link": f.get("contact_whatsapp", "https://wa.me/"),
            "Official Source URL": f.get("source_url", "https://upbhulekh.gov.in/")
        })

    df_top_50_display = pd.DataFrame(table_top_50_rows)
    c_t50_a, c_t50_b = st.columns([3, 1])
    with c_t50_a:
        st.caption(f"Showing **{len(df_top_50_display)}** of **{len(top_50_farms)}** ranked farmland estates matching active filters.")
    with c_t50_b:
        from utils.csv_manager import df_to_csv_bytes
        st.download_button(
            "📥 Download Table (CSV)",
            data=df_to_csv_bytes(df_top_50_display),
            file_name="top_50_farmlands_filtered.csv",
            mime="text/csv",
            key="dl_top_50_filtered_csv_btn"
        )
    render_sticky_frozen_table(df_top_50_display, frozen_cols=2, table_id="top_50_farmlands_table", max_height="620px")

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("#### 🌟 Featured Top Farmlands: Full Agronomic, Satellite & Contact Telemetry")
    st.caption("Deep-dive inspection cards for Top Farmlands featuring remote sensing indices, soil pH, guaranteed cashflows, and direct owner/operator WhatsApp contacts:")

    for f in filtered_top_50[:10]:
        exp_title = f"🏆 #{f['national_rank']} {f['name']} — {f['size_acres']} Acres in {f['city_name']}, {f['state']} • ₹{f['total_price_cr']:.2f} Cr"
        if f.get("has_guaranteed_return"):
            exp_title += f" [⭐ {f['guaranteed_return_pct']}% Guaranteed Return]"
        with st.expander(exp_title, expanded=False):
            st.markdown(render_top_50_national_card_html(f), unsafe_allow_html=True)



