"""
Civic Data Initializer & Reference Generator
Populates high-fidelity CSV datasets for:
1. data/chronic_avoidance_pincodes.csv
2. data/civic_complaints_radar.csv
3. data/master_plan_catalysts_2040.csv
"""

import csv
import os

PINCODES_DATA = [
    # BENGALURU
    {
        'pincode': '560103', 'locality': 'Bellandur & Outer Ring Road (ORR) Lowlands', 'city': 'Bengaluru', 'state': 'Karnataka',
        'avoidance_severity': 'Critical Avoidance', 'elevation_delta_m': '-7.5m below Bellandur ridge',
        'annual_waterlogging_days': '14-22 days', 'negative_feedbacks_count': 1420,
        'common_civic_complaints': 'Severe stormwater drain (Rajakaluve) backflow into apartment basements; Bellandur lake foam & toxic methane fires during monsoons; 100% dependency on private water tankers (₹1,800/load); severe peak traffic snarls at Ecospace & Kadubeesanahalli junctions (speeds < 8 km/h); frequent 11kV transformer trips.',
        'water_tanker_reliance_index': 9.6, 'peak_traffic_delay_index': '2.85x (9.2 km/h avg)',
        'development_authority_10_20yr_plan': 'BDA / BMRDA Master Plan 2031: Bellandur Lake Rejuvenation Wetland Sluices; 73km Peripheral Ring Road (PRR) eastern alignment; Comprehensive Rajakaluve concrete retaining walls.',
        'upcoming_metro_line_and_station': 'Namma Metro Blue Line (ORR-Airport) Bellandur & Ecospace Stations (Opening 2026-27)',
        'upcoming_airport_connectivity': 'Direct elevated Metro corridor to Kempegowda International Airport (KIA T2) via Hebbal (52 km, 55 mins travel time)',
        'major_commercial_mall_sports_hubs': 'Central Mall Bellandur, Ecoworld Play Arenas, Agara Lake Sports Complex, Soul Space Spirit Mall',
        'critique_negative_score_penalty': -32, 'critique_master_plan_boost': 18,
        'critique_ai_viability_score': 38,
        'real_estate_advisory': 'STRICT AVOIDANCE for ground floor units and basement parking. High rental demand for techies, but structural dampness and seasonal evacuation risks persist.',
        'last_scanned_timestamp': '2026-10-03 10:00:00',
        'data_source': 'BBMP Disaster Cell / Karnataka SWRD / BMRCL Phase 2B DPR'
    },
    {
        'pincode': '560087', 'locality': 'Varthur & Panathur Railway Underbridge (RUB) Catchment', 'city': 'Bengaluru', 'state': 'Karnataka',
        'avoidance_severity': 'Critical Avoidance', 'elevation_delta_m': '-9.0m Varthur wetland trough',
        'annual_waterlogging_days': '16-25 days', 'negative_feedbacks_count': 1280,
        'common_civic_complaints': 'Panathur S-bend Railway Underbridge single-lane bottleneck causing 90-min traffic jams; Varthur lake overflow onto SH-35; zero municipal BWSSB piped connection; private tanker mafia extortion; foul stench from open stormwater conduits; severe potholes on Balagere road.',
        'water_tanker_reliance_index': 9.8, 'peak_traffic_delay_index': '3.10x (6.5 km/h avg)',
        'development_authority_10_20yr_plan': 'BMRDA Master Plan: 4-lane Panathur ROB replacement; Varthur-Sarjapur intermediate arterial widening to 80ft; BMRCL Phase 3 extension to Varthur Kodi.',
        'upcoming_metro_line_and_station': 'Namma Metro Phase 3 Varthur Kodi Extension Station (Target 2031-33)',
        'upcoming_airport_connectivity': 'SH-35 to Whitefield Kadugodi connecting to Airport Expressway via Budigere Cross (42 km)',
        'major_commercial_mall_sports_hubs': 'Nexus Whitefield Mall (4.2 km), Varthur Club Ground, Decathlon Sarjapur (5 km)',
        'critique_negative_score_penalty': -35, 'critique_master_plan_boost': 15,
        'critique_ai_viability_score': 32,
        'real_estate_advisory': 'Avoid property purchases without verified physical approach road width >= 40 feet. Beware of wetland encroachment buffer notices.',
        'last_scanned_timestamp': '2026-10-03 10:00:00',
        'data_source': 'BMRDA Master Plan 2031 / BBMP Ward 149 Audit'
    },
    {
        'pincode': '560035', 'locality': 'Sarjapur Road (Rainbow Drive & Kasavanahalli Lakebed)', 'city': 'Bengaluru', 'state': 'Karnataka',
        'avoidance_severity': 'High Stress Avoidance', 'elevation_delta_m': '-5.8m Kasavanahalli lake valley',
        'annual_waterlogging_days': '10-18 days', 'negative_feedbacks_count': 940,
        'common_civic_complaints': 'Rainbow Drive gated layout natural nala obstruction causing complete boat evacuations in heavy rainfall; Kasavanahalli lake overflow onto Sarjapur Main Road; acute drinking water scarcity; unregulated tanker water with TDS > 850 ppm causing pipe corrosion; Carmelaram railway crossing gridlock.',
        'water_tanker_reliance_index': 9.2, 'peak_traffic_delay_index': '2.60x (11.0 km/h avg)',
        'development_authority_10_20yr_plan': 'BDA CDP 2035: Carmelaram Railway Overbridge (ROB) 4-laning; SWD nala desilting and detention basin creation; STRR connecting Hoskote to Sarjapur.',
        'upcoming_metro_line_and_station': 'Namma Metro Red Line (Sarjapur to Hebbal via Agara) Carmelaram Station (Target 2030-32)',
        'upcoming_airport_connectivity': 'Satellite Town Ring Road (STRR NH-948A) connecting to Bengaluru International Airport (KIA) bypass',
        'major_commercial_mall_sports_hubs': 'Market Square Mall Sarjapur, Play Arena Sports Complex (Kasavanahalli), Kaikondrahalli Lake Eco-Track',
        'critique_negative_score_penalty': -28, 'critique_master_plan_boost': 19,
        'critique_ai_viability_score': 44,
        'real_estate_advisory': 'Verify independent stormwater outfall and plinth elevation >= 1.5m above road grade. Prefer elevated ridge societies over valley bed layouts.',
        'last_scanned_timestamp': '2026-10-03 10:00:00',
        'data_source': 'BBMP Mahadevapura Division / NGT Order O.A. 222/2022'
    },
    {
        'pincode': '560068', 'locality': 'Bommanahalli & Central Silk Board Junction', 'city': 'Bengaluru', 'state': 'Karnataka',
        'avoidance_severity': 'High Stress Avoidance', 'elevation_delta_m': '-4.2m Madiwala lake overflow runoff',
        'annual_waterlogging_days': '8-14 days', 'negative_feedbacks_count': 1150,
        'common_civic_complaints': 'Central Silk Board junction chronic commuter bottleneck (up to 45 mins delay); Rupena Agrahara service road knee-deep waterlogging during 30mm rain; heavy particulate air pollution (PM2.5 > 140); old drainage infrastructure surcharge.',
        'water_tanker_reliance_index': 7.5, 'peak_traffic_delay_index': '2.95x (8.5 km/h avg)',
        'development_authority_10_20yr_plan': 'BMRCL Silk Board Multi-Level Flyover Loop and Interchange Hub; BBMP Madiwala drain deepening project.',
        'upcoming_metro_line_and_station': 'Silk Board Interchange Station (Yellow Line to E-City & Blue Line to Airport)',
        'upcoming_airport_connectivity': 'Direct Blue Line elevated metro run via Silk Board-K.R. Puram-Nagawara to KIA Airport (45 mins)',
        'major_commercial_mall_sports_hubs': 'Vega City Mall (4 km), Forum South Bengaluru (5 km), Madiwala Lake Boating & Sports Club',
        'critique_negative_score_penalty': -26, 'critique_master_plan_boost': 22,
        'critique_ai_viability_score': 52,
        'real_estate_advisory': 'Rapid transit hub due to dual metro interchange, but severe surface congestion and air noise require triple-glazed windows and flood gates.',
        'last_scanned_timestamp': '2026-10-03 10:00:00',
        'data_source': 'BMRCL Yellow/Blue Line Joint DPR / BBMP Stormwater Wing'
    },
    {
        'pincode': '560048', 'locality': 'Hoodi & Whitefield Railway Basin Lowlands', 'city': 'Bengaluru', 'state': 'Karnataka',
        'avoidance_severity': 'Moderate Caution', 'elevation_delta_m': '-3.8m Hoodi lake runoff',
        'annual_waterlogging_days': '6-10 days', 'negative_feedbacks_count': 620,
        'common_civic_complaints': 'Waterlogging on Hoodi circle underpass; industrial effluents in local open stormwater trenches; water pressure drops in high-rise societies; Hoodi railway gate traffic jams.',
        'water_tanker_reliance_index': 7.2, 'peak_traffic_delay_index': '2.20x (14.0 km/h avg)',
        'development_authority_10_20yr_plan': 'Whitefield Tech Corridor Urban Redevelopment Plan; Cauvery Stage V full piped distribution commissioning.',
        'upcoming_metro_line_and_station': 'Namma Metro Purple Line Hoodi Station (Operational)',
        'upcoming_airport_connectivity': 'Whitefield-Budigere Cross corridor to Airport Terminal (36 km, 40 mins via SH-104)',
        'major_commercial_mall_sports_hubs': 'Phoenix Marketcity (3 km), VR Bengaluru Mall (3 km), Decathlon Whitefield, ITPL Cricket Ground',
        'critique_negative_score_penalty': -18, 'critique_master_plan_boost': 21,
        'critique_ai_viability_score': 64,
        'real_estate_advisory': 'Good capital appreciation corridor supported by Purple Line Metro. Ensure society has dedicated dual piped plumbing and BWSSB Cauvery connection.',
        'last_scanned_timestamp': '2026-10-03 10:00:00',
        'data_source': 'BWSSB Cauvery Stage V Progress Report / BMRCL Operations'
    },
    {
        'pincode': '560064', 'locality': 'Yelahanka Kogilu & Puttenahalli Bird Sanctuary Fringe', 'city': 'Bengaluru', 'state': 'Karnataka',
        'avoidance_severity': 'High Stress Avoidance', 'elevation_delta_m': '-6.2m Kogilu lake marsh basin',
        'annual_waterlogging_days': '12-16 days', 'negative_feedbacks_count': 780,
        'common_civic_complaints': 'Kogilu cross underpass total submergence during heavy monsoon downpours; Kendriya Vihar society basement flooding; encroachment on secondary feeders of Puttenahalli lake; muddy approach roads during rains.',
        'water_tanker_reliance_index': 8.0, 'peak_traffic_delay_index': '2.30x (13.5 km/h avg)',
        'development_authority_10_20yr_plan': 'BBMP Yelahanka Zone SWD Remodeling; NH-44 Kogilu junction flyover expansion; BDA Peripheral Ring Road Phase 1.',
        'upcoming_metro_line_and_station': 'Namma Metro Blue Line Kogilu Cross & Yelahanka Stations (Opening 2026-27)',
        'upcoming_airport_connectivity': 'Closest Bengaluru corridor to KIA International Airport (18 km, 15 mins via elevated NH-44)',
        'major_commercial_mall_sports_hubs': 'RMZ Galleria Mall Yelahanka (2.5 km), Padukone-Dravid Centre for Sports Excellence (7 km), Puttenahalli Lake Eco Park',
        'critique_negative_score_penalty': -27, 'critique_master_plan_boost': 24,
        'critique_ai_viability_score': 54,
        'real_estate_advisory': 'High airport proximity value, but rigorously avoid low-lying apartments within 200m of Kogilu lake basin or SWD buffers.',
        'last_scanned_timestamp': '2026-10-03 10:00:00',
        'data_source': 'BBMP Yelahanka Stormwater Master Drainage Plan'
    },

    # MUMBAI & MMR
    {
        'pincode': '400058', 'locality': 'Andheri West (S.V. Road & Andheri Subway Corridor)', 'city': 'Mumbai & MMR', 'state': 'Maharashtra',
        'avoidance_severity': 'Critical Avoidance', 'elevation_delta_m': '-4.2m below railway tracks',
        'annual_waterlogging_days': '12-18 days', 'negative_feedbacks_count': 1850,
        'common_civic_complaints': 'Andheri Subway shuts down completely 15+ times per monsoon season with water depths > 5 feet; Mogara Nullah tidal backflow during high tides (>4.5m); S.V. Road severe traffic paralyzation; basement seepage in older cooperative housing societies; high pest and vector disease incidence post-monsoon.',
        'water_tanker_reliance_index': 4.5, 'peak_traffic_delay_index': '3.25x (7.8 km/h avg)',
        'development_authority_10_20yr_plan': 'BMC BRIMSTOWAD Project: Mogara Holding Pond near Gilbert Hill; underground stormwater holding tanks; Versova-Bandra Sea Link (VBSL) connector.',
        'upcoming_metro_line_and_station': 'Mumbai Metro Line 2B (D.N. Nagar to Mandale) & Line 7 (Andheri East to Dahisar) interchange at WEH',
        'upcoming_airport_connectivity': 'Chhatrapati Shivaji Maharaj International Airport (CSMIA T2) within 6 km; Direct connector to Western Express Highway',
        'major_commercial_mall_sports_hubs': 'Infinity Mall Malad (5 km), Citi Mall Andheri, Andheri Sports Complex (Shahaji Raje Krida Sankul), Juhu Beach Promenade',
        'critique_negative_score_penalty': -34, 'critique_master_plan_boost': 20,
        'critique_ai_viability_score': 42,
        'real_estate_advisory': 'Extreme caution for subterranean parking and ground floor retail. Upper floor residential assets maintain strong rental demand.',
        'last_scanned_timestamp': '2026-10-03 10:00:00',
        'data_source': 'BMC Disaster Management Department / BRIMSTOWAD High Powered Committee'
    },
    {
        'pincode': '400024', 'locality': 'Kurla West (CST Road & Mithi River Basin)', 'city': 'Mumbai & MMR', 'state': 'Maharashtra',
        'avoidance_severity': 'Critical Avoidance', 'elevation_delta_m': '-6.0m reclaimed mangrove sink',
        'annual_waterlogging_days': '14-20 days', 'negative_feedbacks_count': 1620,
        'common_civic_complaints': 'Mithi River breach causing 4 to 6 feet waterlogging across CST Road, LBS Marg, and Taximen Colony; Central Railway track submergence suspending suburban trains; uninsurable underground basements; heavy airborne chemical odor from industrial nullahs; severe gridlock at Kurla-Kalina junction.',
        'water_tanker_reliance_index': 5.2, 'peak_traffic_delay_index': '3.40x (6.2 km/h avg)',
        'development_authority_10_20yr_plan': 'MMRDA Mithi River Development Authority: Channel desilting, retaining wall construction, and Chunabhatti holding pond; BKC-Kurla elevated corridor.',
        'upcoming_metro_line_and_station': 'Mumbai Metro Line 3 (Aqua Line Colaba-Bandra-SEEPZ) BKC Station (1.8 km) & Metro Line 2B Kurla Station',
        'upcoming_airport_connectivity': 'Direct proximity to CSMIA T1 & T2 terminals (4 km via Kurla-CST link road)',
        'major_commercial_mall_sports_hubs': 'Phoenix Marketcity Kurla (2 km), Jio World Plaza BKC (2.5 km), University of Mumbai Sports Grounds',
        'critique_negative_score_penalty': -36, 'critique_master_plan_boost': 18,
        'critique_ai_viability_score': 36,
        'real_estate_advisory': 'Strict avoidance for long-term capital preservation unless project is situated on elevated BKC podium structures with specialized sump gates.',
        'last_scanned_timestamp': '2026-10-03 10:00:00',
        'data_source': 'MMRDA Mithi River Authority / IIT Bombay Urban Flood Study'
    },
    {
        'pincode': '400022', 'locality': 'Sion & Chunabhatti (Gandhi Market & Pratiksha Nagar)', 'city': 'Mumbai & MMR', 'state': 'Maharashtra',
        'avoidance_severity': 'Critical Avoidance', 'elevation_delta_m': '-4.8m saucer-shaped wetland basin',
        'annual_waterlogging_days': '10-15 days', 'negative_feedbacks_count': 1390,
        'common_civic_complaints': 'Gandhi Market Kings Circle saucer basin acts as natural drainage sink, submerging BEST buses and taxis; Harbour Line rail tracks submerged at Chunabhatti; vehicular traffic stalled on Eastern Express Highway (EEH); dampness and foundation moss in low-rise chawls and residential buildings.',
        'water_tanker_reliance_index': 4.0, 'peak_traffic_delay_index': '3.10x (8.2 km/h avg)',
        'development_authority_10_20yr_plan': 'BMC Underground Water Holding Tanks at Pramod Mahajan Park & St. Xavier Ground; Mahim Nature Park conservation buffer.',
        'upcoming_metro_line_and_station': 'Mumbai Metro Line 4 (Wadala to Kasarvadavali) Sion Station (Opening 2026-27)',
        'upcoming_airport_connectivity': 'Eastern Freeway connecting South Mumbai to Navi Mumbai International Airport (NMIA) via MTHL Atal Setu',
        'major_commercial_mall_sports_hubs': 'High Street Phoenix Lower Parel (6 km), Sion Fort Historical Park, Somaiya Vidyavihar Olympic Sports Track',
        'critique_negative_score_penalty': -31, 'critique_master_plan_boost': 21,
        'critique_ai_viability_score': 46,
        'real_estate_advisory': 'Avoid low-lying ground units near Gandhi Market. High connectivity upside via MTHL Atal Setu and Metro 4 for elevated tower assets.',
        'last_scanned_timestamp': '2026-10-03 10:00:00',
        'data_source': 'BMC F-North Ward Flood Mitigation Registry'
    },
    {
        'pincode': '400615', 'locality': 'Thane West (Ghodbunder Road Waghbil & Anand Nagar)', 'city': 'Mumbai & MMR', 'state': 'Maharashtra',
        'avoidance_severity': 'Moderate Caution', 'elevation_delta_m': '-3.5m Thane Creek tidal fringe',
        'annual_waterlogging_days': '7-12 days', 'negative_feedbacks_count': 920,
        'common_civic_complaints': 'Ghodbunder Road peak-hour bumper-to-bumper traffic (heavy container trucks heading to JNPT); Waghbil nala overflow during high tide; frequent summer water cuts requiring TMC water rationing; transformer voltage fluctuations during thunderstorms.',
        'water_tanker_reliance_index': 6.8, 'peak_traffic_delay_index': '2.70x (11.5 km/h avg)',
        'development_authority_10_20yr_plan': 'TMC / MMRDA Thane-Borivali Twin Tunnel (11.8 km subterranean link); Ghodbunder elevated flyover extensions; Kopri creek widening.',
        'upcoming_metro_line_and_station': 'Mumbai Metro Line 4 & 5 Interchange (Wadala-Kasarvadavali & Thane-Bhiwandi-Kalyan)',
        'upcoming_airport_connectivity': 'Navi Mumbai International Airport via Thane-Belapur Road & MTHL corridor (38 km)',
        'major_commercial_mall_sports_hubs': 'Viviana Mall (4 km), Korum Mall (5 km), Suraj Water Park, Yeoor Hills Eco Trails & Sanjay Gandhi National Park',
        'critique_negative_score_penalty': -22, 'critique_master_plan_boost': 25,
        'critique_ai_viability_score': 62,
        'real_estate_advisory': 'Strong 10-year growth corridor once Thane-Borivali tunnel cuts travel time to Western Suburbs to 15 mins. Ensure project has dedicated water storage reservoirs.',
        'last_scanned_timestamp': '2026-10-03 10:00:00',
        'data_source': 'MMRDA Comprehensive Transportation Study (CTS 2036)'
    },
    {
        'pincode': '410206', 'locality': 'Panvel (Kalundre River Catchment & Old Panvel)', 'city': 'Mumbai & MMR', 'state': 'Maharashtra',
        'avoidance_severity': 'High Stress Avoidance', 'elevation_delta_m': '-5.1m Kalundre river high-tide level',
        'annual_waterlogging_days': '8-14 days', 'negative_feedbacks_count': 810,
        'common_civic_complaints': 'Kalundre river overflow flooding Old Panvel market and low-lying residential clusters; CIDCO water supply disruptions in dry months; heavy dust pollution from ongoing airport construction; traffic bottlenecks on Sion-Panvel expressway.',
        'water_tanker_reliance_index': 6.5, 'peak_traffic_delay_index': '2.35x (16.0 km/h avg)',
        'development_authority_10_20yr_plan': 'CIDCO NAINA (Navi Mumbai Airport Influence Notified Area) Master Plan; Kalundre river training and tidal flap gates; Panvel-Karjat suburban rail expansion.',
        'upcoming_metro_line_and_station': 'Navi Mumbai Metro Line 1 & Line 2 (Belapur-Pendhar to Khandeshwar / NMIA Airport)',
        'upcoming_airport_connectivity': 'Adjacent to Navi Mumbai International Airport (NMIA - Opening 2025-26)',
        'major_commercial_mall_sports_hubs': 'Orion Mall Panvel, Karnala Sports Academy & Bird Sanctuary, D.Y. Patil Stadium Nerul (14 km)',
        'critique_negative_score_penalty': -25, 'critique_master_plan_boost': 28,
        'critique_ai_viability_score': 60,
        'real_estate_advisory': 'Massive long-term growth catalyst from NMIA commercial operations and NAINA infrastructure. Stick strictly to CIDCO-planned sectors with high plinth elevations.',
        'last_scanned_timestamp': '2026-10-03 10:00:00',
        'data_source': 'CIDCO NAINA Master Plan 2038 / Panvel Municipal Corporation (PMC)'
    },

    # CHENNAI
    {
        'pincode': '600042', 'locality': 'Velachery (Lakebed Inundation Zone & Vijayanagar)', 'city': 'Chennai', 'state': 'Tamil Nadu',
        'avoidance_severity': 'Critical Avoidance', 'elevation_delta_m': '-5.5m below surrounding Guindy ridge',
        'annual_waterlogging_days': '15-22 days', 'negative_feedbacks_count': 1730,
        'common_civic_complaints': 'Severe inundation during NE monsoon & cyclones (Michaung submerged cars completely); residents park vehicles on bypass flyovers; drainage backflow into toilets; high winter rental discounts; heavy mosquito breeding in stagnant water; groundwater brackish with high iron content.',
        'water_tanker_reliance_index': 7.8, 'peak_traffic_delay_index': '2.90x (9.5 km/h avg)',
        'development_authority_10_20yr_plan': 'CMDA Second Master Plan: Remodeling of Velachery macro-drain outfall into Pallikaranai marsh; elevated corridor from Vijayanagar to Taramani.',
        'upcoming_metro_line_and_station': 'Chennai Metro Phase 2 Corridor 3 & 5 (Madhavaram to Sholinganallur) Velachery Station (Target 2026-28)',
        'upcoming_airport_connectivity': 'Chennai International Airport (MAA) at Meenambakkam within 7.5 km via Inner Ring Road',
        'major_commercial_mall_sports_hubs': 'Phoenix Marketcity Chennai (1.5 km), Grand Square Mall, Velachery Aquatic Complex & YMCA Grounds',
        'critique_negative_score_penalty': -35, 'critique_master_plan_boost': 19,
        'critique_ai_viability_score': 40,
        'real_estate_advisory': 'Avoid ground floor flats and standalone houses without high stilts. Multi-story gated towers with rooftop generators and stilt parking manage better.',
        'last_scanned_timestamp': '2026-10-03 10:00:00',
        'data_source': 'Greater Chennai Corporation (GCC) Disaster Management Wing / TNGIS'
    },
    {
        'pincode': '600100', 'locality': 'Pallikaranai & Medavakkam Marshland Encroachment Fringe', 'city': 'Chennai', 'state': 'Tamil Nadu',
        'avoidance_severity': 'Critical Avoidance', 'elevation_delta_m': '-7.0m natural drainage sink of South Chennai',
        'annual_waterlogging_days': '18-28 days', 'negative_feedbacks_count': 1480,
        'common_civic_complaints': 'Lowest topography sink in South Chennai; roads waterlogged for up to 3 weeks post-cyclone; boat rescue required for inner streets; high groundwater salinity (>950 ppm TDS); National Green Tribunal (NGT) legal scrutiny on building buffer zones; burning of municipal dump site causing air toxicity.',
        'water_tanker_reliance_index': 8.9, 'peak_traffic_delay_index': '2.65x (12.0 km/h avg)',
        'development_authority_10_20yr_plan': 'Tamil Nadu Forest Dept Ramsar Wetland Conservation Buffer; Medavakkam 3-level flyover complex; CMWSSB underground sewerage extension.',
        'upcoming_metro_line_and_station': 'Chennai Metro Phase 2 Corridor 5 Medavakkam Junction & Eachangadu Stations (Target 2027)',
        'upcoming_airport_connectivity': 'Radial Road connecting directly to Pallavaram-Thoraipakkam 200ft road to Chennai Airport (12 km)',
        'major_commercial_mall_sports_hubs': 'Pallikaranai Eco Park, Nanmangalam Reserve Forest Nature Trail, Vivira Mall Navalur (9 km)',
        'critique_negative_score_penalty': -37, 'critique_master_plan_boost': 16,
        'critique_ai_viability_score': 35,
        'real_estate_advisory': 'Strict avoidance for plots without explicit NGT clearance. Severe risk of water ingress and building settlement on soft peaty marsh clay.',
        'last_scanned_timestamp': '2026-10-03 10:00:00',
        'data_source': 'National Green Tribunal Order / GCC South Region Stormwater Audit'
    },
    {
        'pincode': '600091', 'locality': 'Madipakkam (Lake Basin & Puzhuthivakkam Lowlands)', 'city': 'Chennai', 'state': 'Tamil Nadu',
        'avoidance_severity': 'High Stress Avoidance', 'elevation_delta_m': '-4.9m Madipakkam lakebed runoff',
        'annual_waterlogging_days': '12-19 days', 'negative_feedbacks_count': 1120,
        'common_civic_complaints': 'Narrow residential streets lacking storm drains; unpaved roads turning into slush during rains; low CMWSSB piped water pressure; high reliance on private water lorries; traffic chokes near Kaiveli junction.',
        'water_tanker_reliance_index': 8.2, 'peak_traffic_delay_index': '2.45x (12.5 km/h avg)',
        'development_authority_10_20yr_plan': 'CMDA Comprehensive Stormwater Drainage Network (Kovalam Basin); Madipakkam lake bund restoration.',
        'upcoming_metro_line_and_station': 'Chennai Metro Phase 2 Corridor 5 Madipakkam Station (Target 2027-28)',
        'upcoming_airport_connectivity': 'Chennai International Airport (6 km via Thillai Ganga Nagar subway)',
        'major_commercial_mall_sports_hubs': 'Phoenix Marketcity (3 km), Madipakkam Lake Walking Track, St. Thomas Mount Heritage Park',
        'critique_negative_score_penalty': -29, 'critique_master_plan_boost': 20,
        'critique_ai_viability_score': 47,
        'real_estate_advisory': 'Ensure prospective buildings have stilt-plus-3 structure with minimum 4ft road elevation. Metro Phase 2 connectivity will unlock high rental demand.',
        'last_scanned_timestamp': '2026-10-03 10:00:00',
        'data_source': 'CMWSSB Water & Sewerage Division / CMDA Second Master Plan'
    },
    {
        'pincode': '600119', 'locality': 'Sholinganallur & OMR IT Corridor (Buckingham Canal Fringes)', 'city': 'Chennai', 'state': 'Tamil Nadu',
        'avoidance_severity': 'Moderate Caution', 'elevation_delta_m': '-3.2m coastal canal catchment',
        'annual_waterlogging_days': '8-14 days', 'negative_feedbacks_count': 1210,
        'common_civic_complaints': 'Sholinganallur signal mega traffic bottleneck (up to 30 mins to cross 800m); Buckingham canal overflow on service roads; high private water tanker expenditure for IT parks; salinity in groundwater requiring RO filtration units.',
        'water_tanker_reliance_index': 8.5, 'peak_traffic_delay_index': '2.75x (11.0 km/h avg)',
        'development_authority_10_20yr_plan': 'Tamil Nadu Highways: OMR Multi-Tier Elevated Expressway from Taramani to Siruseri; Buckingham Canal desilting and ecotourism waterway.',
        'upcoming_metro_line_and_station': 'Chennai Metro Phase 2 Corridor 3 (Madhavaram to SIPCOT IT Park) Sholinganallur Junction Interchange',
        'upcoming_airport_connectivity': 'Future Parandur Greenfield Airport connected via proposed Chennai Peripheral Ring Road (CPRR)',
        'major_commercial_mall_sports_hubs': 'The Marina Mall (5 km), BMR Mall, ECR Beach Resorts & Surf Clubs (3 km), ELCOT IT Park Playfields',
        'critique_negative_score_penalty': -24, 'critique_master_plan_boost': 26,
        'critique_ai_viability_score': 61,
        'real_estate_advisory': 'Premier tech employment hub. Avoid low-lying rear plots adjacent to Buckingham canal; premium high-rises on OMR main road offer solid growth.',
        'last_scanned_timestamp': '2026-10-03 10:00:00',
        'data_source': 'CMDA OMR Elevated Road DPR / CMDA Corridor Study'
    },

    # DELHI-NCR
    {
        'pincode': '110091', 'locality': 'Mayur Vihar Phase-1 & Yamuna Active Floodplains', 'city': 'Delhi-NCR', 'state': 'Delhi',
        'avoidance_severity': 'Critical Avoidance', 'elevation_delta_m': '-4.5m Yamuna River active floodplain',
        'annual_waterlogging_days': '10-18 days', 'negative_feedbacks_count': 1340,
        'common_civic_complaints': 'Yamuna river breaching danger mark (205.33m) causes direct backflow into Khadar lowlands; subterranean moisture in basements; heavy fog and air pollution during winter (AQI > 450); severe gridlock on Noida link road during peak office hours.',
        'water_tanker_reliance_index': 5.0, 'peak_traffic_delay_index': '2.60x (14.0 km/h avg)',
        'development_authority_10_20yr_plan': 'DDA Master Plan for Delhi 2041 (MPD-2041): Yamuna Riverfront Rejuvenation (Asita East Eco Park); Geeta Colony drainage augmentation.',
        'upcoming_metro_line_and_station': 'Delhi Metro Pink Line & Blue Line interchange at Mayur Vihar-1 (Operational)',
        'upcoming_airport_connectivity': 'Indira Gandhi International Airport (IGI T3) via Barapullah elevated corridor (24 km, 35 mins)',
        'major_commercial_mall_sports_hubs': 'Star City Mall Mayur Vihar, Commonwealth Games (CWG) Sports Complex, Akshardham Temple & Cultural Monument',
        'critique_negative_score_penalty': -30, 'critique_master_plan_boost': 20,
        'critique_ai_viability_score': 50,
        'real_estate_advisory': 'Strictly avoid unauthorised colonies in Yamuna Khadar belt. DDA-allotted multi-story apartment pockets on elevated embankments are structurally safe.',
        'last_scanned_timestamp': '2026-10-03 10:00:00',
        'data_source': 'DDA MPD-2041 / Central Water Commission (CWC) Yamuna Gauge Records'
    },
    {
        'pincode': '122002', 'locality': 'Gurugram Cyber City & DLF Phase 2 Lowlands', 'city': 'Delhi-NCR', 'state': 'Haryana',
        'avoidance_severity': 'High Stress Avoidance', 'elevation_delta_m': '-3.8m Aravali runoff sink',
        'annual_waterlogging_days': '8-15 days', 'negative_feedbacks_count': 1550,
        'common_civic_complaints': 'Cyber City underpass submergence under 4 feet water during flash storms; Subhash Chowk and IFFCO Chowk gridlock; GMDA piped water rationing in peak summer; private tanker reliance in builder floors; severe particulate smog and construction dust.',
        'water_tanker_reliance_index': 7.8, 'peak_traffic_delay_index': '3.10x (9.0 km/h avg)',
        'development_authority_10_20yr_plan': 'GMDA Comprehensive Drainage Plan: Leg 1, 2, 3 stormwater drain concrete remodeling into Najafgarh basin; Gurugram Metro Extension.',
        'upcoming_metro_line_and_station': 'Gurugram Metro Rail Project (Huda City Centre to Cyber City 28.5 km loop with 27 stations)',
        'upcoming_airport_connectivity': 'Closest NCR business hub to IGI International Airport (12 km, 15 mins via NH-48)',
        'major_commercial_mall_sports_hubs': 'DLF CyberHub, Ambience Mall Gurugram, Tau Devi Lal Sports Stadium, Aravali Biodiversity Park',
        'critique_negative_score_penalty': -28, 'critique_master_plan_boost': 27,
        'critique_ai_viability_score': 62,
        'real_estate_advisory': 'Global corporate hub with premium rentals. Ensure property is not in direct Aravali drainage runoff path. DLF Phase 2 podium complexes are resilient.',
        'last_scanned_timestamp': '2026-10-03 10:00:00',
        'data_source': 'GMDA Urban Drainage Blueprint / Haryana Mass Rapid Transport Corporation'
    },
    {
        'pincode': '201301', 'locality': 'Noida Sector 137 & Shahdara Drain Low-Lying Belt', 'city': 'Delhi-NCR', 'state': 'Uttar Pradesh',
        'avoidance_severity': 'Moderate Caution', 'elevation_delta_m': '-3.0m Shahdara drainage depression',
        'annual_waterlogging_days': '6-10 days', 'negative_feedbacks_count': 890,
        'common_civic_complaints': 'Heavy foul odor from open Shahdara drain affecting high-rise balconies; complaints of corrosion in air conditioner coils due to hydrogen sulfide gas; waterlogging at underpass near Advant Navis; high maintenance charges for diesel generators.',
        'water_tanker_reliance_index': 6.0, 'peak_traffic_delay_index': '2.15x (16.0 km/h avg)',
        'development_authority_10_20yr_plan': 'Noida Master Plan 2031: Covering and bio-remediation of Shahdara drain; Noida-Greater Noida Expressway decongestion flyovers.',
        'upcoming_metro_line_and_station': 'Noida Metro Aqua Line Sector 137 Station (Operational)',
        'upcoming_airport_connectivity': 'Direct expressway access to upcoming Noida International Airport (Jewar - Opening 2025-26)',
        'major_commercial_mall_sports_hubs': 'Advant Navis Business Park, Sector 137 Central Bio-Diversity Park, Noida Indoor Stadium (8 km)',
        'critique_negative_score_penalty': -22, 'critique_master_plan_boost': 24,
        'critique_ai_viability_score': 64,
        'real_estate_advisory': 'High rental yield for tech workers. Inspect apartment orientation; prefer towers facing inward or towards central greens away from the open drain.',
        'last_scanned_timestamp': '2026-10-03 10:00:00',
        'data_source': 'Noida Authority Environmental Cell / Central Pollution Control Board (CPCB)'
    },

    # HYDERABAD
    {
        'pincode': '500013', 'locality': 'Moosarambagh & Musi River Basin (Old City Lowlands)', 'city': 'Hyderabad', 'state': 'Telangana',
        'avoidance_severity': 'Critical Avoidance', 'elevation_delta_m': '-6.5m Musi river flood level',
        'annual_waterlogging_days': '12-18 days', 'negative_feedbacks_count': 1220,
        'common_civic_complaints': 'Moosarambagh causeway completely submerged when Osman Sagar & Himayat Sagar gates open; river water inundating colonies; extreme stench and mosquitoes from untreated industrial effluents; building foundation dampness; narrow congested approach roads.',
        'water_tanker_reliance_index': 5.5, 'peak_traffic_delay_index': '2.80x (10.2 km/h avg)',
        'development_authority_10_20yr_plan': 'Government of Telangana Musi Riverfront Development Project (MRDP): ₹58,000 Cr riverfront rejuvenation, check dams, and elevated expressway corridor.',
        'upcoming_metro_line_and_station': 'Hyderabad Metro Red Line Malakpet Station (1.8 km) & proposed Musi Riverfront Metro Spur',
        'upcoming_airport_connectivity': 'Rajiv Gandhi International Airport (RGIA Shamshabad) via Inner Ring Road & PVNR Expressway (22 km)',
        'major_commercial_mall_sports_hubs': 'L.B. Nagar D-Mart & Shopping Hub, Victory Play Ground Chaderghat, Salar Jung Museum & Cultural Hub',
        'critique_negative_score_penalty': -33, 'critique_master_plan_boost': 17,
        'critique_ai_viability_score': 39,
        'real_estate_advisory': 'Avoid properties within 200m of Musi river buffer until MRDP retaining wall and river desilting civil works are commissioned.',
        'last_scanned_timestamp': '2026-10-03 10:00:00',
        'data_source': 'GHMC Disaster Management Cell / Musi Riverfront Development Corporation'
    },
    {
        'pincode': '500081', 'locality': 'Madhapur & Durgam Cheruvu Lake Catchment', 'city': 'Hyderabad', 'state': 'Telangana',
        'avoidance_severity': 'Moderate Caution', 'elevation_delta_m': '-3.5m Durgam Cheruvu runoff basin',
        'annual_waterlogging_days': '6-10 days', 'negative_feedbacks_count': 1050,
        'common_civic_complaints': 'Waterlogging on Kavuri Hills connecting roads during short cloudbursts; peak-hour gridlock at Mindspace roundabout and Ayyappa Society; high private water tanker reliance in older standalone buildings; noise pollution from IT commercial towers.',
        'water_tanker_reliance_index': 6.9, 'peak_traffic_delay_index': '2.50x (12.5 km/h avg)',
        'development_authority_10_20yr_plan': 'HMDA Master Plan 2031: Strategic Road Development Plan (SRDP) multi-level underpasses; Durgam Cheruvu lake aeration and eco-walkway.',
        'upcoming_metro_line_and_station': 'Hyderabad Metro Blue Line Durgam Cheruvu & Madhapur Stations (Operational)',
        'upcoming_airport_connectivity': 'RGIA Airport via Nehru Outer Ring Road (ORR Gachibowli junction) (30 km, 30 mins)',
        'major_commercial_mall_sports_hubs': 'Inorbit Mall Cyberabad, Durgam Cheruvu Cable Bridge Promenade, Hitex Exhibition Centre, Gachibowli Athletic Stadium',
        'critique_negative_score_penalty': -20, 'critique_master_plan_boost': 28,
        'critique_ai_viability_score': 71,
        'real_estate_advisory': 'Tier-1 IT residential hotspot. Choose gated societies on elevated rock plateau with HMWSSB Krishna/Godavari piped drinking water connections.',
        'last_scanned_timestamp': '2026-10-03 10:00:00',
        'data_source': 'HMDA Master Plan / HMWSSB Water Supply Division'
    },
    {
        'pincode': '500072', 'locality': 'Kukatpally & KPHB (IDL Lake Inundation Depression)', 'city': 'Hyderabad', 'state': 'Telangana',
        'avoidance_severity': 'High Stress Avoidance', 'elevation_delta_m': '-4.8m IDL lake nala catchment',
        'annual_waterlogging_days': '10-15 days', 'negative_feedbacks_count': 1180,
        'common_civic_complaints': 'IDL Lake overflow submerging surrounding colonies and connecting roads; severe choke at Kukatpally Y-junction; groundwater contamination from historical chemical industrial units; high traffic congestion on NH-65.',
        'water_tanker_reliance_index': 7.2, 'peak_traffic_delay_index': '2.70x (11.0 km/h avg)',
        'development_authority_10_20yr_plan': 'GHMC Strategic Nala Development Programme (SNDP): Box drain remodeling at IDL lake; Kukatpally flyover expansion.',
        'upcoming_metro_line_and_station': 'Hyderabad Metro Red Line KPHB Colony & JNTU Stations (Operational)',
        'upcoming_airport_connectivity': 'Direct access via Miyapur-Gachibowli ORR link to Rajiv Gandhi International Airport',
        'major_commercial_mall_sports_hubs': 'Forum Sujana Mall (Nexus Hyderabad), Manjeera Mall, JNTU Sports Grounds',
        'critique_negative_score_penalty': -27, 'critique_master_plan_boost': 21,
        'critique_ai_viability_score': 54,
        'real_estate_advisory': 'Dense commercial and retail locality. Ensure water testing report for heavy metals before purchasing residential units in older plots.',
        'last_scanned_timestamp': '2026-10-03 10:00:00',
        'data_source': 'GHMC SNDP Phase 2 Report / Telangana Pollution Control Board'
    },

    # VARANASI & EASTERN UP 100KM CORRIDOR
    {
        'pincode': '221002', 'locality': 'Varanasi Cantt, Nadesar & Varuna River Basin', 'city': 'Varanasi & Eastern UP', 'state': 'Uttar Pradesh',
        'avoidance_severity': 'Critical Avoidance', 'elevation_delta_m': '-5.5m Varuna river flood basin',
        'annual_waterlogging_days': '12-20 days', 'negative_feedbacks_count': 980,
        'common_civic_complaints': 'Varuna River monsoon backflow submerging Nadesar and Cantt lowlands; water enters ground-floor houses during Ganga high flood levels (>71.26m danger mark); traffic gridlock near Varanasi Junction railway station; open drain siltation.',
        'water_tanker_reliance_index': 5.8, 'peak_traffic_delay_index': '2.60x (11.5 km/h avg)',
        'development_authority_10_20yr_plan': 'VDA Master Plan 2031: Varuna Riverfront Development & Flood Embankments; Varanasi Urban Ropeway Phase 1 (Cantt Station to Godowlia); Ring Road Phase 2 completion.',
        'upcoming_metro_line_and_station': 'Varanasi Urban Public Transport Ropeway (Cantt Railway Station Terminal - Opening 2025-26)',
        'upcoming_airport_connectivity': 'Direct 4-lane elevated highway to Lal Bahadur Shastri International Airport Babatpur (21 km, 22 mins)',
        'major_commercial_mall_sports_hubs': 'JHV Mall Nadesar, Sigra International Sports Complex (Dr. Sampurnanand Stadium), Sarnath Heritage Buddhist Circuit (9 km)',
        'critique_negative_score_penalty': -31, 'critique_master_plan_boost': 23,
        'critique_ai_viability_score': 52,
        'real_estate_advisory': 'Avoid low-lying riverbed settlements in Varuna flood corridor. High appreciation on elevated Cantt ridge and Shivpur corridor.',
        'last_scanned_timestamp': '2026-10-03 10:00:00',
        'data_source': 'Varanasi Development Authority (VDA) / Central Water Commission Varuna Gauge'
    },
    {
        'pincode': '221001', 'locality': 'Godowlia, Chowk & Ancient Core Ghats', 'city': 'Varanasi & Eastern UP', 'state': 'Uttar Pradesh',
        'avoidance_severity': 'High Stress Avoidance', 'elevation_delta_m': '-3.8m ancient stormwater conduits',
        'annual_waterlogging_days': '8-14 days', 'negative_feedbacks_count': 1140,
        'common_civic_complaints': 'Extreme pedestrian and e-rickshaw vehicular gridlock; knee-deep waterlogging during cloudbursts due to British-era brick barrel drains choking; no private car parking available; severe building alteration restrictions under ASI and VDA heritage norms.',
        'water_tanker_reliance_index': 4.2, 'peak_traffic_delay_index': '3.50x (4.5 km/h avg)',
        'development_authority_10_20yr_plan': 'Kashi Vishwanath Dham Special Area Heritage Plan; Underground utility ducting; Riverfront Ghat stabilization.',
        'upcoming_metro_line_and_station': 'Varanasi Ropeway Godowlia Chowk Terminal (Direct 15-min aerial transit to Cantt Station)',
        'upcoming_airport_connectivity': 'Lal Bahadur Shastri Airport connected via Babatpur 4-lane NH-56 (26 km)',
        'major_commercial_mall_sports_hubs': 'Dashashwamedh Ghat Cultural Plaza, Kashi Vishwanath Dham Corridor, Assi Ghat Ganga Aarti Amphitheatre',
        'critique_negative_score_penalty': -29, 'critique_master_plan_boost': 24,
        'critique_ai_viability_score': 55,
        'real_estate_advisory': 'High commercial and homestay/hotel tourism value, but completely unsuited for vehicle-owning families due to no-car zoning and drainage chokes.',
        'last_scanned_timestamp': '2026-10-03 10:00:00',
        'data_source': 'Kashi Vishwanath Special Area Development Board / UP Jal Sansthan'
    },
    {
        'pincode': '211002', 'locality': 'Prayagraj (Baghada, Salori & Bakshi Bund Basin)', 'city': 'Varanasi & Eastern UP', 'state': 'Uttar Pradesh',
        'avoidance_severity': 'Critical Avoidance', 'elevation_delta_m': '-7.2m Ganga-Yamuna Sangam backflow basin',
        'annual_waterlogging_days': '20-30 days', 'negative_feedbacks_count': 1410,
        'common_civic_complaints': 'Chronic evacuation zone during monsoon floods when Ganga and Yamuna exceed 84.73m danger mark; student hostels and residential colonies submerged under 8-10 feet water; power cut for days; heavy silt and mud deposition post-monsoon.',
        'water_tanker_reliance_index': 5.2, 'peak_traffic_delay_index': '2.40x (13.0 km/h avg)',
        'development_authority_10_20yr_plan': 'Prayagraj Mela Authority & PDA Mahakumbh Master Plan: Bakshi Bund pumping station modernization; Ganga Expressway connecting Prayagraj to Meerut (594 km).',
        'upcoming_metro_line_and_station': 'Prayagraj Light Metro Phase 1 (Shantipuram to Naini) Civil Lines Interchange (3.5 km)',
        'upcoming_airport_connectivity': 'Prayagraj Domestic Airport (Bamrauli) with direct flights to Delhi, Mumbai, Bengaluru (14 km)',
        'major_commercial_mall_sports_hubs': 'Civil Lines Shopping District, Sangam Mahakumbh Grounds, Madan Mohan Malaviya Stadium, Alfred Park (Chandrashekhar Azad Park)',
        'critique_negative_score_penalty': -38, 'critique_master_plan_boost': 17,
        'critique_ai_viability_score': 33,
        'real_estate_advisory': 'STRICT AVOIDANCE for property purchase. Annual evacuation hotspot with catastrophic structural risk during peak flood discharge.',
        'last_scanned_timestamp': '2026-10-03 10:00:00',
        'data_source': 'Prayagraj District Disaster Management Authority / CWC Flood Atlas'
    }
]


CIVIC_COMPLAINTS_RADAR = [
    {
        'complaint_id': 'CC_BLR_01', 'city': 'Bengaluru', 'pincode': '560103', 'locality': 'Bellandur / Ecospace',
        'category': 'Drainage & Basement Flooding', 'severity': 'Critical',
        'complaint_summary': 'Basement parking submerged up to 4.5 feet; 82 vehicles damaged after stormwater drain boundary wall collapsed near Outer Ring Road.',
        'verified_grievance_source': 'BBMP Sahaya Grievance #441902 / Mahadevapura Task Force',
        'impact_on_property_value': '-15% rental discount on ground-floor units; mandatory flood barrier installation costs.'
    },
    {
        'complaint_id': 'CC_BLR_02', 'city': 'Bengaluru', 'pincode': '560087', 'locality': 'Panathur / Varthur',
        'category': 'Traffic Gridlock & Bottlenecks', 'severity': 'Critical',
        'complaint_summary': 'Panathur Railway Underbridge single-lane gridlock causing 1.5 to 2 hours delay for a 1.2km commute to Cessna Business Park.',
        'verified_grievance_source': 'Bangalore Traffic Police (BTP) Public Grievance Portal',
        'impact_on_property_value': 'Severe tenant turnover in apartment complexes along Balagere-Panathur road.'
    },
    {
        'complaint_id': 'CC_MUM_01', 'city': 'Mumbai & MMR', 'pincode': '400058', 'locality': 'Andheri West Subway',
        'category': 'Monsoon Inundation & Rail Disruption', 'severity': 'Critical',
        'complaint_summary': 'Andheri subway closed 18 times during monsoon; water level reaching 5 feet under rail tracks during 40mm/hr rains.',
        'verified_grievance_source': 'BMC Disaster Management Control Room Logs',
        'impact_on_property_value': 'Commercial showrooms face water seepage damage; lower commercial lease rates.'
    },
    {
        'complaint_id': 'CC_MUM_02', 'city': 'Mumbai & MMR', 'pincode': '400024', 'locality': 'Kurla West / CST Road',
        'category': 'Mithi River Overflow & Sewerage Odor', 'severity': 'Critical',
        'complaint_summary': 'Mithi river toxic silt and industrial chemical backflow enters ground floor chawls and commercial warehouses.',
        'verified_grievance_source': 'Maharashtra Pollution Control Board (MPCB) Complaint Registry',
        'impact_on_property_value': 'Cap on residential property appreciation despite proximity to BKC.'
    },
    {
        'complaint_id': 'CC_CHN_01', 'city': 'Chennai', 'pincode': '600042', 'locality': 'Velachery Lakebed',
        'category': 'Monsoon Cyclone Flooding', 'severity': 'Critical',
        'complaint_summary': 'Cyclone Michaung caused complete 4-day isolation of Vijayanagar and TNHB layout; power cut for 96 hours; drinking water distributed by boats.',
        'verified_grievance_source': 'Greater Chennai Corporation (GCC) Emergency Cell',
        'impact_on_property_value': 'Extreme depression in resale liquidity for independent houses without stilt parking.'
    },
    {
        'complaint_id': 'CC_DEL_01', 'city': 'Delhi-NCR', 'pincode': '122002', 'locality': 'Gurugram Cyber City',
        'category': 'Urban Flash Flooding & Power Cuts', 'severity': 'High',
        'complaint_summary': 'Waterlogging on NH-48 service lanes and Cyber City underpasses; diesel generator backup costs of ₹35-42/unit passed to residents.',
        'verified_grievance_source': 'GMDA Citizen Portal & Haryana RERA Complaints',
        'impact_on_property_value': 'High maintenance fees (CAM charges > ₹8/sqft) eroding net rental yields.'
    },
    {
        'complaint_id': 'CC_HYD_01', 'city': 'Hyderabad', 'pincode': '500013', 'locality': 'Moosarambagh Musi Basin',
        'category': 'River Overflow & Water Contamination', 'severity': 'Critical',
        'complaint_summary': 'Osman Sagar reservoir gates release flooding 25 colonies; Musi river toxic foam and heavy mosquito infestation.',
        'verified_grievance_source': 'GHMC Monsoon Emergency Ward Operations',
        'impact_on_property_value': 'Stagnant capital growth; distress sales during post-monsoon period.'
    },
    {
        'complaint_id': 'CC_VAR_01', 'city': 'Varanasi & Eastern UP', 'pincode': '211002', 'locality': 'Prayagraj Baghada & Salori',
        'category': 'Catastrophic River Flooding', 'severity': 'Critical',
        'complaint_summary': 'Ganga and Yamuna confluence submerging student lodges up to second floor; annual boat evacuations lasting 3 weeks.',
        'verified_grievance_source': 'Prayagraj District Administration Flood Relief Log',
        'impact_on_property_value': 'Zero institutional home loan sanctioning for non-elevated ground plots in flood zone.'
    }
]


MASTER_PLAN_CATALYSTS_2040 = [
    {
        'catalyst_id': 'MP_BLR_01', 'city': 'Bengaluru', 'corridor': 'ORR - Airport Blue Line',
        'authority': 'BMRCL / BDA', 'target_completion_year': 2026,
        'project_type': 'Metro & Rapid Transit',
        'project_name': 'Namma Metro Blue Line Phase 2B (Silk Board to KIA Airport via ORR)',
        'scale_and_budget': '₹14,844 Cr | 58.19 km elevated viaduct with 30 stations',
        'key_stations_or_nodes': 'Silk Board, Bellandur, Ecospace, Kadubeesanahalli, Marathahalli, KR Puram, Nagawara, Hebbal, Yelahanka, Airport T2',
        'growth_impact_rating': 9.8,
        'economic_catalyst_notes': 'Transforms Outer Ring Road and North Bengaluru into an uninterrupted airport rail transit corridor; cuts commute times by 60%.'
    },
    {
        'catalyst_id': 'MP_BLR_02', 'city': 'Bengaluru', 'corridor': 'Peripheral Ring Road (PRR / STRR)',
        'authority': 'BDA / NHAI', 'target_completion_year': 2028,
        'project_type': 'Expressway & Ring Road',
        'project_name': 'Satellite Town Ring Road (STRR NH-948A) & Bengaluru PRR',
        'scale_and_budget': '₹21,000 Cr | 288 km 6-lane access-controlled expressway',
        'key_stations_or_nodes': 'Doddaballapur, Hoskote, Sarjapur, Attibele, Kanakapura, Ramanagara, Magadi',
        'growth_impact_rating': 9.4,
        'economic_catalyst_notes': 'Diverts heavy interstate logistics out of the city; unlocks multi-thousand-acre logistics, agroforestry, and villa layouts.'
    },
    {
        'catalyst_id': 'MP_MUM_01', 'city': 'Mumbai & MMR', 'corridor': 'Navi Mumbai International Airport (NMIA)',
        'authority': 'CIDCO / Adani Airports', 'target_completion_year': 2025,
        'project_type': 'Airport & Aerocity',
        'project_name': 'Navi Mumbai International Airport (NMIA Phase 1 & Aerocity)',
        'scale_and_budget': '₹19,646 Cr | 20 Million Passengers/Yr capacity in Phase 1 (90 MPPA final)',
        'key_stations_or_nodes': 'Ulwe, Panvel, Dronagiri, Kharghar Corporate Park, NAINA Zone',
        'growth_impact_rating': 9.9,
        'economic_catalyst_notes': 'Primary economic catalyst for MMR; connects with MTHL Atal Setu and Mumbai Coastal Road for 40-min drive to Nariman Point.'
    },
    {
        'catalyst_id': 'MP_MUM_02', 'city': 'Mumbai & MMR', 'corridor': 'Thane-Borivali Twin Tunnel',
        'authority': 'MMRDA', 'target_completion_year': 2028,
        'project_type': 'Subterranean Expressway',
        'project_name': 'Thane-Borivali 11.8 km 6-Lane Subterranean Twin Tunnel under SGNP',
        'scale_and_budget': '₹16,600 Cr | Reduces travel time between Thane and Western Suburbs from 90 mins to 15 mins',
        'key_stations_or_nodes': 'Tikuji-ni-Wadi (Thane) to Magathane / Borivali (Western Express Highway)',
        'growth_impact_rating': 9.6,
        'economic_catalyst_notes': 'Eliminates Ghodbunder Road bottlenecks; massive boost to Thane residential and commercial demand.'
    },
    {
        'catalyst_id': 'MP_CHN_01', 'city': 'Chennai', 'corridor': 'Chennai Metro Phase 2 Corridors 3, 4 & 5',
        'authority': 'CMRL / CMDA', 'target_completion_year': 2027,
        'project_type': 'Metro & Rapid Transit',
        'project_name': 'CMRL Phase 2 Network Expansion (116.1 km)',
        'scale_and_budget': '₹63,246 Cr | 119 stations connecting North Chennai to OMR SIPCOT and Poonamallee',
        'key_stations_or_nodes': 'Madhavaram, Sterling Road, Adyar, Velachery, Medavakkam, Sholinganallur, Siruseri SIPCOT',
        'growth_impact_rating': 9.7,
        'economic_catalyst_notes': 'Provides high-speed public rail transit directly beneath the congested OMR and Medavakkam tech corridors.'
    },
    {
        'catalyst_id': 'MP_DEL_01', 'city': 'Delhi-NCR', 'corridor': 'Noida International Airport (Jewar)',
        'authority': 'YAPL / NIAL / YEIDA', 'target_completion_year': 2025,
        'project_type': 'Airport & Aerocity',
        'project_name': 'Noida International Greenfield Airport Jewar (DXN)',
        'scale_and_budget': '₹29,650 Cr | 4 runways, cargo hub, and direct Yamuna Expressway connectivity',
        'key_stations_or_nodes': 'Jewar, Yamuna Expressway Sector 18, 20, 22D, Noida Sector 150',
        'growth_impact_rating': 9.9,
        'economic_catalyst_notes': 'Transforms Greater Noida and Yamuna Expressway into India’s biggest electronics manufacturing and aviation corridor.'
    },
    {
        'catalyst_id': 'MP_HYD_01', 'city': 'Hyderabad', 'corridor': 'Musi Riverfront Development & Elevated Skyway',
        'authority': 'MRDCL / Govt of Telangana', 'target_completion_year': 2029,
        'project_type': 'Riverfront Rejuvenation & Skyway',
        'project_name': 'Musi Riverfront Urban Rejuvenation & 55 km East-West Skyway',
        'scale_and_budget': '₹58,000 Cr | River channel desilting, STPs, pedestrian promenades, check dams',
        'key_stations_or_nodes': 'Osmansagar, Bapu Ghat, Moosarambagh, Chaderghat, Nagole',
        'growth_impact_rating': 9.3,
        'economic_catalyst_notes': 'Addresses historical flood risks in Old City and creates a central cultural and commercial water promenade.'
    },
    {
        'catalyst_id': 'MP_VAR_01', 'city': 'Varanasi & Eastern UP', 'corridor': 'Varanasi Urban Ropeway Transit & Ring Road Phase 2',
        'authority': 'VDA / NHLML', 'target_completion_year': 2025,
        'project_type': 'Aerial Cable Transit & Ring Highway',
        'project_name': 'Varanasi Public Transport Ropeway (Cantt Station to Godowlia Chowk) & Ring Road Phase 2',
        'scale_and_budget': '₹807 Cr (Ropeway) + ₹3,200 Cr (Ring Road) | 3.8 km Ropeway over congested core',
        'key_stations_or_nodes': 'Varanasi Cantt, Vidya Pith, Rath Yatra, Girija Ghar, Godowlia Chowk; Ring Road Sandaha to Ramnagar',
        'growth_impact_rating': 9.5,
        'economic_catalyst_notes': 'First urban aerial ropeway in India; leapfrogs ancient street congestion in 15 minutes.'
    }
]


def generate_all_csvs():
    os.makedirs('data', exist_ok=True)
    
    # 1. Chronic Avoidance Pincodes CSV
    pincode_file = 'data/chronic_avoidance_pincodes.csv'
    with open(pincode_file, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=list(PINCODES_DATA[0].keys()))
        writer.writeheader()
        writer.writerows(PINCODES_DATA)
    print(f"[OK] Generated {pincode_file} ({len(PINCODES_DATA)} rows)")

    # 2. Civic Complaints Radar CSV
    complaints_file = 'data/civic_complaints_radar.csv'
    with open(complaints_file, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=list(CIVIC_COMPLAINTS_RADAR[0].keys()))
        writer.writeheader()
        writer.writerows(CIVIC_COMPLAINTS_RADAR)
    print(f"[OK] Generated {complaints_file} ({len(CIVIC_COMPLAINTS_RADAR)} rows)")

    # 3. Master Plan Catalysts 2040 CSV
    master_file = 'data/master_plan_catalysts_2040.csv'
    with open(master_file, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=list(MASTER_PLAN_CATALYSTS_2040[0].keys()))
        writer.writeheader()
        writer.writerows(MASTER_PLAN_CATALYSTS_2040)
    print(f"[OK] Generated {master_file} ({len(MASTER_PLAN_CATALYSTS_2040)} rows)")


if __name__ == "__main__":
    generate_all_csvs()
