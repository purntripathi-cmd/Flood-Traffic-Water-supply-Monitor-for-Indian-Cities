"""
Multi-Criteria Real Estate Viability & Avoidance Scoring Engine
Implements weighted composite scoring combining Flood Risk, Traffic Congestion,
Water Security, Drainage Quality, and Builder Pedigree.
"""

from typing import Dict, Any


def compute_composite_avoidance_score(
    flood_risk_score: float,       # 0 - 100 (100 = severe flooding)
    traffic_delay_index: float,    # 1.0 - 3.5 (peak time / free flow time)
    water_supply_score: float,     # 0 - 100 (100 = 24x7 municipal piped)
    drainage_score: float = 70.0,  # 0 - 100 (100 = Dutch holding pond / master SWD)
    builder_rating: float = 9.0    # 1.0 - 10.0
) -> Dict[str, Any]:
    """
    Computes a 0 to 100 Composite Avoidance & Viability Index.
    Higher score (75-100) = Prime Resilient Real Estate
    Medium score (55-74) = Moderate Caution / Monsoon Stress
    Low score (<55) = Avoidance Zone
    """
    # Normalize traffic delay penalty: (delay_index - 1.0) / 2.0 * 100
    traffic_penalty = min(100.0, max(0.0, (traffic_delay_index - 1.0) / 2.0 * 100.0))
    
    # Invert water supply score to insecurity
    water_insecurity = 100.0 - water_supply_score

    # Weights
    # Flood: 30%, Traffic: 25%, Water Insecurity: 20%, Drainage: 15%, Builder: 10%
    base_deductions = (
        0.30 * flood_risk_score +
        0.25 * traffic_penalty +
        0.20 * water_insecurity
    )
    
    bonuses = (
        0.15 * drainage_score +
        0.10 * (builder_rating * 10.0)
    )

    final_score = round(max(5.0, min(98.0, 100.0 - base_deductions + (bonuses * 0.25))), 1)

    if final_score >= 75.0:
        verdict = "🟢 Prime Resilient Buy / Rent"
        color = "#10B981"
        category = "PRIME_RESILIENT"
    elif final_score >= 55.0:
        verdict = "🟡 Watchlist / Caution (Monsoon Stress)"
        color = "#F59E0B"
        category = "CAUTION_WATCHLIST"
    else:
        verdict = "🔴 High-Risk Avoidance Zone"
        color = "#EF4444"
        category = "AVOIDANCE_ZONE"

    return {
        "composite_score": final_score,
        "verdict": verdict,
        "category": category,
        "color": color,
        "traffic_penalty": round(traffic_penalty, 1),
        "water_insecurity": round(water_insecurity, 1)
    }


def calculate_monthly_wasted_commute_hours(delay_index: float, daily_one_way_km: float = 14.0) -> int:
    """
    Calculates wasted hours spent sitting in traffic per commuter per month (22 working days).
    Based on standard free-flow speed of 35 km/h vs peak congested speed.
    """
    free_flow_speed_kmh = 35.0
    free_flow_hours_daily = (daily_one_way_km * 2) / free_flow_speed_kmh
    peak_hours_daily = free_flow_hours_daily * delay_index
    wasted_hours_daily = peak_hours_daily - free_flow_hours_daily
    monthly_wasted = round(wasted_hours_daily * 22)
    return max(8, min(65, monthly_wasted))
