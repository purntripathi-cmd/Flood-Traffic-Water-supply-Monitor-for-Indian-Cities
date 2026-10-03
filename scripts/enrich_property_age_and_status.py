"""
Enriches properties.json and gated_plots.json with:
- property_status (Ready to Move vs Under Construction vs Upcoming Pre-Launch)
- property_age (Years since delivery / Occupancy certificate date / Months to completion)
- age_vs_completion (Human-readable summary comparing property age vs upcoming handover timeline)
"""

import json
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "data")

props_file = os.path.join(DATA_DIR, "properties.json")
with open(props_file, "r", encoding="utf-8") as f:
    properties = json.load(f)

# Property status, age & completion details
prop_age_mapping = {
    "prop_blr_1": {
        "status": "Under Construction",
        "age": "Under Construction (Handover in ~14 months)",
        "summary": "🏗️ Under Construction (Dec 2026 • 14 mos)",
        "possession_year": 2026
    },
    "prop_blr_2": {
        "status": "Ready to Move",
        "age": "4 years old (OC delivered in 2022)",
        "summary": "🟢 Ready to Move (4 yrs old • Active Community)",
        "possession_year": 2022
    },
    "prop_blr_3": {
        "status": "Upcoming Pre-Launch",
        "age": "Upcoming Phase 2 (Foundation & Raft stage)",
        "summary": "🚀 Upcoming Pre-Launch (March 2027 • ~2 yrs)",
        "possession_year": 2027
    },
    "prop_mum_1": {
        "status": "Under Construction",
        "age": "Under Construction (Finishing & Snagging stage)",
        "summary": "🏗️ Under Construction (June 2026 • 8 mos)",
        "possession_year": 2026
    },
    "prop_mum_2": {
        "status": "Under Construction",
        "age": "Near Completion (OC inspection in progress)",
        "summary": "🏗️ Near Completion (Dec 2025 • ~2 mos)",
        "possession_year": 2025
    },
    "prop_mum_3": {
        "status": "Under Construction",
        "age": "Under Construction (18th floor slab cast)",
        "summary": "🏗️ Under Construction (March 2027 • 17 mos)",
        "possession_year": 2027
    },
    "prop_chn_1": {
        "status": "Ready to Move",
        "age": "2 years old (Delivered in 2024)",
        "summary": "🟢 Ready to Move (2 yrs old • Instant Handover)",
        "possession_year": 2024
    },
    "prop_chn_2": {
        "status": "Under Construction",
        "age": "Under Construction (Structure complete)",
        "summary": "🏗️ Under Construction (Q3 2026 • 11 mos)",
        "possession_year": 2026
    },
    "prop_chn_3": {
        "status": "Under Construction",
        "age": "Under Construction (Tower A MEP works)",
        "summary": "🏗️ Under Construction (Dec 2026 • 14 mos)",
        "possession_year": 2026
    },
    "prop_del_1": {
        "status": "Near Completion",
        "age": "Near Completion (Internal fitouts ongoing)",
        "summary": "🏗️ Near Completion (Q1 2026 • 5 mos)",
        "possession_year": 2026
    },
    "prop_del_2": {
        "status": "Under Construction",
        "age": "Under Construction (Structure 12th floor)",
        "summary": "🏗️ Under Construction (Dec 2026 • 14 mos)",
        "possession_year": 2026
    },
    "prop_del_3": {
        "status": "Upcoming Pre-Launch",
        "age": "Upcoming Phase 2 (Earthwork & Piling)",
        "summary": "🚀 Upcoming Pre-Launch (March 2027 • ~2 yrs)",
        "possession_year": 2027
    },
    "prop_hyd_1": {
        "status": "Ready to Move",
        "age": "3 years old (Delivered in 2023)",
        "summary": "🟢 Ready to Move (3 yrs old • Luxury OC)",
        "possession_year": 2023
    },
    "prop_hyd_2": {
        "status": "Ready to Move",
        "age": "5 years old (Established society 2021)",
        "summary": "🟢 Ready to Move (5 yrs old • 100% Occupied)",
        "possession_year": 2021
    },
    "prop_hyd_3": {
        "status": "Under Construction",
        "age": "Under Construction (10th floor slab)",
        "summary": "🏗️ Under Construction (March 2027 • 17 mos)",
        "possession_year": 2027
    },
    "prop_vns_1": {
        "status": "Under Construction",
        "age": "Under Construction (Brickwork & Glazing)",
        "summary": "🏗️ Under Construction (Dec 2026 • 14 mos)",
        "possession_year": 2026
    },
    "prop_vns_2": {
        "status": "Ready to Move",
        "age": "2 years old (Delivered in 2024)",
        "summary": "🟢 Ready to Move (2 yrs old • Registry Ready)",
        "possession_year": 2024
    },
    "prop_vns_3": {
        "status": "Upcoming Pre-Launch",
        "age": "Upcoming Launch (RERA Sanctioned layout)",
        "summary": "🚀 Upcoming Pre-Launch (Q2 2027 • ~20 mos)",
        "possession_year": 2027
    }
}

for p in properties:
    info = prop_age_mapping.get(p["id"], {
        "status": "Under Construction",
        "age": "Under Construction (Handover in ~14 months)",
        "summary": "🏗️ Under Construction (Dec 2026)",
        "possession_year": 2026
    })
    p["property_status"] = info["status"]
    p["property_age"] = info["age"]
    p["age_vs_completion"] = info["summary"]
    p["possession_year"] = info["possession_year"]

with open(props_file, "w", encoding="utf-8") as f:
    json.dump(properties, f, indent=2)

print(f"Enriched {len(properties)} properties with age and completion timelines.")

# Enrich Gated Plots
plots_file = os.path.join(DATA_DIR, "gated_plots.json")
with open(plots_file, "r", encoding="utf-8") as f:
    gated_plots = json.load(f)

for pl in gated_plots:
    exp_c = pl.get("expected_completion", "Ready for Construction")
    if "Ready" in exp_c or "Immediate" in exp_c:
        pl["property_status"] = "Ready for Registration"
        pl["property_age"] = "Immediate Registry (All statutory approvals in place)"
        pl["age_vs_completion"] = "🟢 Ready for Immediate Registry & Villa Construction"
    else:
        pl["property_status"] = "Under Development"
        pl["property_age"] = "Phased Infrastructure Development (~12 months to handover)"
        pl["age_vs_completion"] = f"🏗️ Under Development ({exp_c})"

with open(plots_file, "w", encoding="utf-8") as f:
    json.dump(gated_plots, f, indent=2)

print(f"Enriched {len(gated_plots)} gated plots with age and handover status.")
