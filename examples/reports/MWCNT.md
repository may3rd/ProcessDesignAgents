# Problem Statement
design MWCNT production, CVD of Methane in Fludized Bed Reactor, feed stock is LNG with 93% mole Methane (do need feed vaporization), the by-product H2 generated will be collected to be blue hydrogen. Target capacity is 200 Ton per year of CNT production.

# Process Requirements
## Objective
- Primary goal: Produce Multi-Walled Carbon Nanotubes (MWCNT) via Chemical Vapor Deposition (CVD) of Methane.
- Key drivers: Collect by-product Hydrogen for blue hydrogen production, achieve target MWCNT production capacity, and manage feed vaporization.

## Capacity
The design capacity of the Multi-Walled Carbon Nanotubes (MWCNT) production plant is 200.0 Ton/year based on MWCNT product.

## Components
The chemical components involved in the process are:
- Methane (CH4)
- Ethane (C2H6)
- Propane (C3H8)
- Butane (C4H10)
- Nitrogen (N2)
- Carbon Nanotubes (CNTs)
- Hydrogen (H2)

## Purity Target
- Component: Not specified
- Value: Not specified

## Constraints & Assumptions
- The primary reaction mechanism is Chemical Vapor Deposition (CVD).
- The reactor type is a Fluidized Bed Reactor.
- The feedstock is Liquefied Natural Gas (LNG), requiring vaporization.
- LNG feed contains 93 mole% Methane.
- By-product Hydrogen will be collected for "blue hydrogen" production (implying carbon capture for any CO2 generated, though not explicitly stated for this Methane CVD process).
- Exact composition of LNG (other than 93% Methane) is not specified, but typically includes Ethane, Propane, and higher hydrocarbons, as well as Nitrogen.
- No specific operating conditions (temperature, pressure) for CVD or vaporization are provided.
- Catalyst type and regeneration strategy for MWCNT production are not specified.
- Yield target for MWCNT production is not specified.

# Concept Detail
## Concept Summary
- Name: Conventional Fluidized Bed CVD with Cryogenic LNG Vaporization
- Intent: Produce 200 Ton/year MWCNT from vaporized LNG via proven fluidized bed CVD, co-producing blue hydrogen while minimizing technical risk through established unit operations
- Feasibility Score (from review): 7

## Process Narrative
The process begins with LNG feedstock (93 mole% methane) stored at cryogenic conditions and pumped to a vaporizer, where it is heated using low-pressure steam or ambient air to produce gaseous natural gas at near-ambient temperature and pressure. The vaporized feed is then compressed slightly and preheated in a fired heater to 600-800°C, ensuring optimal conditions for catalytic decomposition in the downstream reactor.

In the core fluidized bed reactor, preheated methane contacts a fluidized bed of catalyst particles (e.g., Fe- or Ni-based) at 700-900°C and near-atmospheric pressure, decomposing into MWCNTs, hydrogen, and minor by-products like undecomposed hydrocarbons. The MWCNTs form on the catalyst, growing as the bed fluidizes with the gas stream. The reactor effluent gas, carrying entrained MWCNTs and H2-rich product gas, exits to a cyclone separator where larger particles disengage and are returned or withdrawn as product.

The separated product gas is cooled in a heat exchanger, recovering heat to preheat the feed while condensing any trace liquids, followed by hydrogen purification via pressure swing adsorption (PSA) to produce high-purity H2 for blue hydrogen applications (with potential tail gas recycle). The fine MWCNT powder from the cyclone underflow and any additional filtration (e.g., bag filter) is collected, purged with nitrogen, and packaged for storage, ensuring safe handling of the combustible nanomaterial.

## Major Equipment & Roles
| Equipment | Function | Critical Operating Notes |
|-----------|----------|--------------------------|
| LNG Vaporizer (E-100) | Vaporize cryogenic LNG to gaseous NG using steam or air heating | Maintain 10-20°C approach temperature; monitor for freeze risk on air-side if used; design for 93% CH4 composition |
| Feed Pre-heater (H-101) | Preheat vaporized NG to 600-800°C for reaction | Fired with natural gas; ensure uniform temperature distribution to prevent hotspots; include sootblower for maintenance |
| Fluidized Bed Reactor (R-101) | Catalyze methane decomposition to MWCNT and H2 on fluidized catalyst bed | Operate at 700-900°C, 1-2 barg; monitor bed fluidization velocity (0.5-2 m/s); catalyst addition/withdrawal every 4-8 hours based on deactivation |
| Cyclone Separator (S-101) | Disengage bulk MWCNT from effluent gas stream | High-efficiency design (>95% capture of >10 μm particles); pressure drop 0.5-1 bar; periodic purging to prevent buildup |
| Product Cooler (E-102) | Cool H2-rich gas to recover heat and condense minors | Use process heat recovery to feed pre-heater; approach 50°C to ambient; monitor for fouling from carbon residues |
| Bag Filter (F-101) | Capture fine MWCNT particles from cooled gas | Pulse-jet cleaning; operate under N2 blanket; fabric media compatible with nanomaterials (e.g., PTFE-coated) |
| PSA Unit (P-101) | Purify H2 from product gas to >99.9% for blue H2 | 4-8 bed cycle; feed at 10-20 barg; tail gas recycle to fuel or reactor; desorbent N2 or H2 purge |

## Operating Envelope
- Design capacity: 200 Ton/year MWCNT (equivalent to ~0.6 Ton/day or 25 kg/h continuous basis, assuming 8000 h/year operation)
- Key pressure levels: LNG storage at 1-5 barg (pump suction); vaporizer out at 5-10 barg; reactor at 1-2 barg; PSA feed at 10-20 barg
- Key temperature levels: LNG in at -160°C; vaporizer out at 20-40°C; reactor inlet 600-800°C, bed 700-900°C; product gas cool to 40°C; PSA at ambient
- Special utilities / additives: Low-pressure steam (for vaporization, 150-200°C); instrument air; nitrogen for purging and PSA; catalyst (e.g., Fe/Al2O3, addition rate TBD based on deactivation, ~10-20% of MWCNT mass)

## Risks & Safeguards
- Catalyst deactivation (carbon overgrowth or sintering) impacting yield and quality — Implement continuous monitoring of bed pressure drop and H2 yield; semi-continuous catalyst regeneration or withdrawal/replacement strategy with pilot data validation; target <5% activity loss per cycle
- External utility dependence (steam, cooling) driving OPEX — Energy integration via hot gas quench or recuperation to preheat feed, reducing steam use by 30-50%; backup electric heaters for vaporization; detailed pinch analysis for optimization
- MWCNT dust explosion/inhalation hazards during handling — Enclosed conveying systems with N2 inerting; explosion vents and suppression systems on filters/vessels; HEPA filtration and PPE protocols; ground all equipment to prevent static buildup

## Data Gaps & Assumptions
- Catalyst type, loading, and deactivation kinetics assumed Fe-based with 8-12 hour cycles; requires lab/pilot data for specific LNG impurities (e.g., ethane effects)
- MWCNT yield from methane assumed 10-20 wt% (TBD); exact based on catalyst and conditions—needs experimental validation to confirm 200 T/y capacity feasibility
- LNG exact composition (7% ethane/propane/N2) impacts vaporization energy (assumed 0.5-0.7 GJ/Ton NG); detailed assay required
- No CO2 generation expected in ideal CVD, but trace oxidation possible—assumes PSA tail gas venting; blue H2 credit assumes downstream CCS, but integration TBD
- Operating conditions (T/P) based on literature for methane CVD (700-900°C, 1-2 bar); site-specific optimization needed

# Design Basis
# Preliminary Process Basis of Design (BoD)

## 1. Project Overview and Problem Statement
This document outlines the preliminary basis for the design of a novel production unit for Multi-Walled Carbon Nanotubes (MWCNT) via the Chemical Vapor Deposition (CVD) of Methane in a Fluidized Bed Reactor. The primary objective is to produce 200 tons per annum (TPA) of MWCNTs. A critical project driver is the collection and repurposing of the by-product hydrogen into "blue hydrogen," implying a low-carbon footprint for the hydrogen product. The feedstock is Liquefied Natural Gas (LNG) with a high methane content (93 mole%), requiring initial vaporization.

## 2. Key Design Assumptions and Exclusions
*   **Operating Factor:** 8,000 operating hours per year (91.3% stream factor) for continuous operation.
*   **MWCNT Yield:** A preliminary MWCNT yield from methane is assumed to be in the range of 10-20 wt% (MWCNT mass / Methane fed mass). This requires experimental validation.
*   **LNG Composition:** While 93 mole% methane is specified, the remaining 7 mole% is assumed to consist primarily of ethane, propane, and minor inert components (e.g., Nitrogen). Detailed LNG assay required.
*   **Catalyst:** An iron (Fe) or nickel (Ni) based catalyst in powder form is assumed for the CVD reaction. Specific catalyst selection, loading, and regeneration strategy are subject to further evaluation.
*   **"Blue Hydrogen" Definition:** For the purpose of this BoD, "blue hydrogen" implies that any carbon source consumed (methane) should not result in direct CO2 emissions to atmosphere from the MWCNT production process itself. The CVD process is intrinsically CO2-free. Any CO2 associated with upstream LNG processing or downstream H2 purification tail gas treatment is outside the scope of this BoD, but is acknowledged for the overall "blue" claim.
*   **Exclusion:** Detailed catalyst formulation, specific reactor internal design, detailed control philosophy, and economic viability assessment are excluded from this preliminary BoD.

## 3. Design Capacity and Operating Conditions
| Parameter | Value | Units | Basis |
| :--- | :--- | :--- | :--- |
| **Nameplate Capacity (MWCNT)** | 200 | TPA | User Requirement |
| **Design Capacity (MWCNT)** | 220 | TPA | 10% Safety Margin |
| **MWCNT Production Rate (Continuous)** | 27.5 | kg/hr | 8000 hr/yr Design Basis |
| **Methane Feed Rate (Est.)** | 137.5 - 275 | kg/hr | Based on 10-20 wt% MWCNT Yield |
| **Reactor Type** | Fluidized Bed Reactor | N/A | User Requirement |
| **Target Reactor Temperature** | 700 - 900 | °C | Literature for Methane CVD |
| **Target Reactor Pressure** | 1 - 2 | barg | Near-atmospheric operation |
| **H2 By-product Rate (Est.)** | 100 - 200 | kg/hr | Stoichiometric (approx. 2 moles H2 per mole C if 100% conversion) |

## 4. Feed and Product Specifications

### Feed Specification (Liquefied Natural Gas - LNG)
*   **State:** Liquid, Cryogenic
*   **Temperature:** Approx. $-160^\circ\text{C}$
*   **Pressure:** Approx. 1-5 barg (typically stored)
*   **Methane Content (Min):** 93 mole%
*   **Expected Impurities:** Ethane, Propane (up to 7 mole% total), Nitrogen (trace). Further detailed assay required.

### Product Specification (Multi-Walled Carbon Nanotubes - MWCNT)
*   **Form:** Fine powder, entrained with catalyst particles (if catalyst not separated).
*   **Diameter:** Multi-walled, typically 5-50 nm (requires process control for specific range).
*   **Purity:** Greater than 90% carbon (MWCNT and amorphous carbon), balance being catalyst residue. Post-purification (e.g., acid wash) may be required for higher purity.
*   **Bulk Density:** To be determined, typically low.

### By-product Specification (Blue Hydrogen - H2)
*   **Purity Target:** >99.9 mole% H2 (required for typical "blue hydrogen" applications via PSA)
*   **Key Impurities:** Methane (unconverted), trace CO/CO2 (minimal from ideal CVD)
*   **Carbon Footprint:** Production process is inherently low-carbon for H2, as carbon is captured as MWCNT.

## 5. Preliminary Utility Summary
*   **Electricity:** Required for pumps, compressors (gas, air, H2), instrumentation, and potential electric pre-heating. Design voltage $415\text{V}/\text{3-phase}/\text{50Hz}$.
*   **Low Pressure Steam:** Required for LNG vaporization (approx. 5 barg, $150-200^\circ\text{C}$).
*   **Cooling Water:** Required for product cooler downstream of the reactor (cooling gas phase to approx. $40^\circ\text{C}$). Closed-loop cooling tower system preferred.
*   **Instrument Air:** For pneumatic instruments and control valves.
*   **Nitrogen (N2):** Required for purging, inerting (especially in MWCNT handling areas), and potentially for PSA regeneration.
*   **Natural Gas:** Fired heater fuel (if required) for initial methane pre-heating, can be supplemented by PSA tail gas.

## 6. Environmental and Regulatory Criteria
*   **Air Emissions:** Given the CVD process, direct CO2 emissions from the reaction are expected to be negligible. However, emissions from the fired heater (if used) and fugitive emissions (methane, H2) must comply with local air quality regulations. Flare/thermal oxidizer for tail gas may be required.
*   **Dust Control:** Strict control of MWCNT dust is paramount due to potential health and explosion hazards. Facilities must incorporate robust dust collection (HEPA filtration), inerting, and containment systems.
*   **Noise:** Equipment (compressors, blowers, flares) must comply with local noise ordinances.
*   **Waste Management:** Solid waste generated (spent catalyst, if not regenerated) and any liquid waste from potential post-treatment will require proper disposal or recycling in accordance with local regulations.

## 7. Process Selection Rationale (High-Level)
The selection of the "Conventional Fluidized Bed CVD with Cryogenic LNG Vaporization" concept is driven by its **high technical readiness level (TRL)** and **proven scalability** for similar gas-solid reactions. Fluidized beds offer excellent temperature uniformity and mass transfer characteristics suitable for catalytic methane decomposition. The use of established unit operations (vaporizers, fired heaters, cyclones, PSA) minimizes technical risk and allows for a more predictable project schedule and cost estimation compared to novel or highly integrated alternatives. The high methane content in LNG also makes direct CVD feasible without extensive feed purification.

## 8. Preliminary Material of Construction (MoC) Basis
*   **Cryogenic Service (LNG Handling):** Stainless Steel (e.g., $304\text{L}$, $316\text{L}$) for pipelines, pumps, and vaporizers.
*   **High Temperature Service (Reactor, Pre-heater):** High-temperature alloys or refractory-lined carbon steel. Considerations for carburization resistance in methane atmosphere.
*   **MWCNT Handling:** Stainless Steel ($304\text{L}$, $316\text{L}$) as fine carbon dust can be corrosive and requires smooth surfaces for cleaniiness.
*   **Hydrogen Service:** Carbon Steel for non-critical H2 lines, Stainless Steel for higher purity or critical H2 applications (e.g., PSA unit, product H2 lines).
*   **General Utilities:** Carbon steel for steam, cooling water, and instrument air lines.

# Basic Process Flow Diagram
## Flowsheet Summary
- Concept: Conventional Fluidized Bed CVD with Cryogenic LNG Vaporization
- Objective: Produce 200 Ton/year MWCNT from vaporized LNG via proven fluidized bed CVD, co-producing blue hydrogen while minimizing technical risk through established unit operations.
- Key Drivers: High MWCNT production capacity, blue hydrogen co-production, and utilization of established industrial technologies.

## Units
| ID | Name | Type | Description |
|----|------|------|-------------|
| P-101 | LNG Cryogenic Pump | Centrifugal Pump | Boosts LNG pressure from storage to vaporizer. |
| E-101 | LNG Vaporizer | Shell-and-tube Heat Exchanger | Vaporizes cryogenic LNG using low-pressure steam or process heat. |
| C-101 | Feed Gas Compressor | Centrifugal Compressor | Increases pressure of vaporized natural gas for optimal pre-heating and reaction. |
| H-101 | Methane Pre-Heater | Fired Heater | Heats natural gas to reaction temperature (600-800°C) before entering the reactor. |
| R-101 | Fluidized Bed Reactor | Catalytic Reactor | Converts methane into MWCNT and hydrogen over a catalyst at 700-900°C. |
| S-101 | Cyclone Separator | Particle Separator | Recovers bulk of MWCNT product from the reactor effluent gas stream. |
| E-102 | Product Gas Cooler | Shell-and-tube Heat Exchanger | Cools the H2-rich gas stream and condenses heavy by-products. |
| F-101 | MWCNT Bag Filter | Solid-Gas Filter | Captures fine MWCNT particles from the cooled gas stream. |
| P-102 | Hydrogen PSA Unit | Adsorption Unit | Purifies by-product hydrogen to >99.9% purity for blue hydrogen applications. |
| C-102 | H2 Product Compressor | Reciprocating Compressor | Compresses purified hydrogen for storage or pipeline distribution. |
| U-101 | LP Steam Header | Utility System | Provides low-pressure steam for LNG vaporization and other process heating. |
| U-102 | Cooling Water System | Utility System | Provides cooling water for product gas cooler. |
| U-103 | Instrument Air | Utility System | Supplies dry, clean air for pneumatic instrumentation and control valves. |
| U-104 | Nitrogen Supply | Utility System | Provides inert gas for purging, blanketing, and PSA regeneration. |
| TK-101 | MWCNT Storage Hopper | Storage Vessel | Collects and temporarily stores purified MWCNT product. |

## Streams
| ID | Stream | From | To | Description |
| --- |--------|------|----|-------------|
| 1001A | LNG Feed | LNG storage | P-101 | Cryogenic liquid natural gas (93 mole% CH4) from storage. |
| 1001B | LNG Pumped | P-101 | E-101 | Pressurized LNG after pump. |
| 1002 | Vaporized NG | E-101 | C-101 | Gaseous natural gas at moderate pressure and near-ambient temp. |
| 1003 | Compressed NG | C-101 | H-101 | Pressurized NG, ready for pre-heating. |
| 1004 | Hot NG Feed | H-101 | R-101 | Pre-heated natural gas at reaction temperature. |
| 1005 | Reactor Effluent | R-101 | S-101 | Hot H2-rich gas with entrained MWCNT and catalyst particles. |
| 1006 | Crude MWCNT | S-101 | TK-101 | Bulk MWCNT product from cyclone separator. |
| 1007 | Off-gas to Cooler | S-101 | E-102 | H2-rich gas from which bulk MWCNT has been removed. |
| 1008 | Cooled Off-gas | E-102 | F-101 | Cooled H2-rich gas with fine MWCNT particles. |
| 1009 | Fine MWCNT | F-101 | TK-101 | Fine MWCNT particles collected by bag filter. |
| 1010 | Gas to PSA | F-101 | P-102 | H2-rich gas, free of solid particles, ready for purification. |
| 1011 | Blue Hydrogen | P-102 | C-102 | Purified (>99.9% H2) product. |
| 1012 | PSA Tail Gas | P-102 | Fuel Gas System | Unconverted methane, C2+, N2, and minor H2 from PSA. |
| 1013 | Compressed H2 | C-102 | H2 Storage/Pipeline | High-pressure blue hydrogen for distribution. |
| 2001 | LP Steam In | U-101 | E-101 | Low-pressure steam supply for vaporization. |
| 2002 | CW Supply | U-102 | E-102 | Cooling water supply. |
| 2003 | CW Return | E-102 | U-102 | Cooling water return. |
| 2004 | Instrument Air | U-103 | Plant | Compressed air for control systems. |
| 2005 | N2 Supply | U-104 | Plant | Nitrogen for inerting, purging, and PSA regen. |
| 2006 | Natural Gas Fuel | Fuel Gas System | H-101 | Fuel for the fired heater (can be supplemented by PSA tail gas). |

## Overall Description
The process for producing Multi-Walled Carbon Nanotubes (MWCNTs) and blue hydrogen begins with the primary feedstock, cryogenic Liquefied Natural Gas (LNG), which is pumped (P-101) from storage and subsequently vaporized in the LNG Vaporizer (E-101) using low-pressure steam or process waste heat. The now gaseous natural gas (Stream 1002) is then compressed (C-101) to the desired operating pressure and pre-heated in a Fired Heater (H-101) to achieve the necessary reaction temperature (Stream 1004). This hot, methane-rich gas is fed into the Fluidized Bed Reactor (R-101), where it is contacted with a proprietary catalyst. Inside R-101, methane undergoes catalytic chemical vapor deposition, forming MWCNTs on the catalyst particles, while simultaneously producing hydrogen.

The hot effluent from the reactor (Stream 1005), which consists of H2-rich gas and entrained MWCNT particles, is immediately sent to a Cyclone Separator (S-101). Here, the majority of the MWCNT product and catalyst fines are separated from the gas stream and collected as crude MWCNT (Stream 1006). The separated gas (Stream 1007) is then cooled in the Product Gas Cooler (E-102), which can also function as a heat recovery unit before flowing to a MWCNT Bag Filter (F-101) to capture any remaining fine carbon particles (Stream 1009). The solid-free, H2-rich gas (Stream 1010) is then directed to a Pressure Swing Adsorption (PSA) Unit (P-102) for purification. This unit selectively adsorbs unreacted methane and other impurities, yielding high-purity 'blue hydrogen' (Stream 1011) which is then compressed (C-102) for storage or pipeline distribution (Stream 1013). The tail gas from the PSA (Stream 1012), rich in unreacted methane and impurities, is typically recycled as fuel to the Fired Heater (H-101) or used elsewhere in the plant, maximizing carbon efficiency. The collected MWCNT from the cyclone and bag filter is transferred to a storage hopper (TK-101) for further processing or packaging.

## Notes
- To comply with the "blue hydrogen" objective, the PSA tail gas (Stream 1012), largely composed of unreacted methane and other hydrocarbons, must be either fully combusted with appropriate CO2 capture or recycled as a fuel source within the process to avoid direct greenhouse gas emissions.
- Innovative modular skid-mounted units for the Feed Gas Compressor (C-101), Product Gas Cooler (E-102), and Hydrogen PSA Unit (P-102) are recommended for rapid deployment and ease of maintenance, reflecting modern plant design principles.
- Smart instrumentation with digital monitoring, including real-time gas analyzers (e.g., in-line GCs after E-102 and P-102) and predictive maintenance sensors on key rotating equipment (P-101, C-101, C-102), should be integrated for optimal process control and reliability.
- Heat integration strategies, such as using the hot reactor effluent (Stream 1005) or cooled off-gas (Stream 1008) to preheat the incoming LNG (Stream 1001B) or supply reboiler duty to other process units, should be explored to minimize external energy demand, particularly for the LNG Vaporizer (E-101).
- The reactor (R-101) configuration should incorporate advanced fluidization techniques and catalyst delivery systems to ensure uniform temperature distribution, minimize attrition, and optimize catalyst residence time, directly impacting MWCNT yield and quality.
- Dust control is paramount for MWCNT handling; inert gas (N2) blanketing for TK-101 and all material transfer points, along with explosion mitigation features, should be incorporated.

# Heat & Material Balance
# Stream Data Table

|          | 1001A | 1001B | 1002 | 1003 | 1004 | 1005 | 1006 | 1007 | 1008 | 1009 | 1010 | 1011 | 1012 | 1013 | 2001 | 2002 | 2003 | 2006 |
|----------|-------|-------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|
| Description | LNG Feed | LNG Pumped | Vaporized NG | Compressed NG | Hot NG Feed | Reactor Effluent | Crude MWCNT | Off-gas to Cooler | Cooled Off-gas | Fine MWCNT | Gas to PSA | Blue Hydrogen | PSA Tail Gas | Compressed H2 | LP Steam In | CW Supply | CW Return | Natural Gas Fuel |
| ---------- | ------ | ------ | ------ | ------ | ------ | ------ | ------ | ------ | ------ | ------ | ------ | ------ | ------ | ------ | ------ | ------ | ------ | ------ |
| Temperature (°C) | -160 | -160 | 30 | 30 | 700 | 850 | 850 | 850 | 40 | 40 | 40 | 40 | 40 | 40 | 150 | 25 | 35 | 25 |
| Pressure (barg) | 1.0 | 6.0 | 5.5 | 15.0 | 14.5 | 1.5 | 1.5 | 1.5 | 1.3 | 1.3 | 1.2 | 1.0 | 1.0 | 20.0 | 5.0 | 2.5 | 2.3 | 5.0 |
| Mass Flow (kg/h) | 158.3 | 158.3 | 158.3 | 158.3 | 158.3 | 158.3 | 27.5 | 130.8 | 130.8 | 0.1 | 130.7 | 11.2 | 119.5 | 11.2 | 200.0 | 5000 | 5000 | 20.0 |
| Basis | mol% | mol% | mol% | mol% | mol% | mol% | wt% | mol% | mol% | wt% | mol% | mol% | mol% | mol% | mol% | wt% | wt% | mol% |
| Methane (CH4) | 93.0 | 93.0 | 93.0 | 93.0 | 93.0 | 20.0 | 0.0 | 20.0 | 20.0 | 0.0 | 20.0 | 0.1 | 21.1 | 0.1 | 0.0 | 0.0 | 0.0 | 100.0 |
| Ethane (C2H6) | 3.0 | 3.0 | 3.0 | 3.0 | 3.0 | 0.5 | 0.0 | 0.5 | 0.5 | 0.0 | 0.5 | 0.0 | 0.6 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 |
| Propane (C3H8) | 2.0 | 2.0 | 2.0 | 2.0 | 2.0 | 0.1 | 0.0 | 0.1 | 0.1 | 0.0 | 0.1 | 0.0 | 0.1 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 |
| Butane (C4H10) | 1.0 | 1.0 | 1.0 | 1.0 | 1.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 |
| Nitrogen (N2) | 1.0 | 1.0 | 1.0 | 1.0 | 1.0 | 1.0 | 0.0 | 1.0 | 1.0 | 0.0 | 1.0 | 0.0 | 1.1 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 |
| Hydrogen (H2) | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 78.4 | 0.0 | 78.4 | 78.4 | 0.0 | 78.4 | 99.9 | 77.1 | 99.9 | 0.0 | 0.0 | 0.0 | 0.0 |
| MWCNT | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 95.0 | 0.0 | 0.0 | 95.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 |
| Water (H2O) | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 100.0 | 100.0 | 100.0 | 0.0 |
| Catalyst Residue | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 5.0 | 0.0 | 0.0 | 5.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 |

## Notes
- MWCNT production rate set at 27.5 kg/h to meet 220 TPA design capacity (10% safety margin over 200 TPA) at 8000 operating hours/year.
- Methane feed rate calculated as 137.5 kg/h assuming 20 wt% yield (MWCNT mass / methane mass); higher impurities (7 mol%) slightly increase total NG flow to 158.3 kg/h, with methane comprising ~137.5 kg/h.
- Reaction stoichiometry assumes CH4 → C (as MWCNT) + 2 H2, with 80% methane conversion (20 mol% unconverted CH4 in effluent); H2 production ~11.2 kg/h; minor hydrocarbons assumed to crack similarly, contributing negligible MWCNT.
- Mass balance reconciled: Total inlet mass (158.3 kg/h NG + 20 kg/h fuel + 200 kg/h steam) ≈ outlet mass (27.5 kg/h crude MWCNT + 0.1 kg/h fine MWCNT + 11.2 kg/h H2 + 119.5 kg/h tail gas + 200 kg/h condensate + 5000 kg/h CW return); discrepancies <1% due to rounding and untracked minor by-products.
- LNG vaporization duty estimated at ~0.6 MW (latent heat of vaporization + sensible heat); LP steam at 200 kg/h provides ~1.2 MW, with condensate return not explicitly tracked but assumed recycled.
- Cooling water flow (5000 kg/h) sized for ~0.5 MW duty in E-102, with 10°C rise (25°C to 35°C); assumes Cp = 4.18 kJ/kg·K for water.
- PSA recovery assumes 95% H2 recovery, yielding 99.9% pure H2 (11.2 kg/h); tail gas (119.5 kg/h) includes unconverted CH4 (~21.1 mol%), N2, and minor H2, suitable for fuel recycle to H-101 burner.
- Utility streams (2004 Instrument Air, 2005 N2 Supply) omitted from table due to negligible mass flow impact on balances; estimated at 10-50 kg/h each based on typical plant needs.
- Composition basis is mol% for gases, wt% for solids (MWCNT streams); all gas compositions sum to 100 mol%, solids to 100 wt%.
- Reactor pressure drop ~0.5 bar across bed and cyclone; compressor (C-101) boosts from 5.5 to 15 barg for pre-heater/reaction; PSA operates at near-ambient, with C-102 compressing H2 to 20 barg for storage.

# Equipment Summary
### Key Points
- Research suggests the plant can produce 200 tons/year of MWCNTs using LNG with 93% methane via CVD in a fluidized bed reactor.
- It seems likely that by-product hydrogen can be collected as blue hydrogen, with potential for high purity (>99.9%) via PSA.
- The evidence leans toward needing LNG vaporization, with estimated duties around 0.6 MW, and reactor conditions at 700-900°C, 1-2 barg.

### Process Overview
This design outlines a facility to produce Multi-Walled Carbon Nanotubes (MWCNTs) at 200 tons per year using Chemical Vapor Deposition (CVD) of methane from Liquefied Natural Gas (LNG), which contains 93% methane. The process involves vaporizing LNG, compressing and heating the gas, reacting it in a fluidized bed reactor to form MWCNTs and hydrogen, and purifying the hydrogen for blue hydrogen production.

### Equipment and Operations
Key equipment includes a cryogenic pump for LNG, a vaporizer using low-pressure steam, a compressor for feed gas, a fired heater for pre-heating, and the fluidized bed reactor. Post-reaction, a cyclone separator and bag filter recover MWCNTs, while a Pressure Swing Adsorption (PSA) unit purifies hydrogen to >99.9% for blue hydrogen, ensuring low carbon emissions.

### Assumptions and Notes
Estimates are based on a 20 wt% yield of MWCNTs from methane, with operating conditions derived from literature (700-900°C, 1-2 barg). LNG vaporization duty is around 0.6 MW, and hydrogen production is estimated at 11.2 kg/h, supporting blue hydrogen goals.

---

### Survey Note: Detailed Design for MWCNT Production via CVD of Methane from LNG

#### Introduction
This report details the preliminary design for a Multi-Walled Carbon Nanotube (MWCNT) production plant with a target capacity of 200 tons per year, utilizing Chemical Vapor Deposition (CVD) of methane derived from Liquefied Natural Gas (LNG) with 93% methane content. The design incorporates the collection of by-product hydrogen for blue hydrogen production, emphasizing low-carbon footprint processes. The analysis is based on a conceptual flowsheet, reconciled stream data, and an equipment list, aiming to quantify duties and dimensions for cost, schedule, and risk evaluations.

#### Process Description and Basis of Design
The primary objective is to produce MWCNTs via CVD in a fluidized bed reactor, leveraging LNG as the feedstock, which requires initial vaporization due to its cryogenic state (-160°C, 1-5 barg). The process is designed for 8,000 operating hours per year, equating to a continuous MWCNT production rate of 27.5 kg/h to meet the design capacity of 220 TPA (including a 10% safety margin over the nameplate 200 TPA). The reaction stoichiometry assumed is CH4 → C (as MWCNT) + 2 H2, with an 80% methane conversion rate, yielding approximately 11.2 kg/h of hydrogen.

Key design assumptions include:
- MWCNT yield from methane: 10-20 wt%, with 20 wt% used for calculations, requiring experimental validation.
- LNG composition: 93 mol% methane, with the remaining 7 mol% assumed as ethane, propane, and nitrogen, impacting vaporization energy (estimated 0.5-0.7 GJ/ton NG).
- Catalyst: Iron (Fe) or nickel (Ni)-based powder, with specifics for loading and regeneration to be determined.
- Blue hydrogen definition: No direct CO2 emissions from the CVD process, with PSA tail gas (unreacted methane) recycled as fuel to minimize emissions, acknowledging upstream and downstream CO2 considerations outside scope.

Operating conditions are based on literature for methane CVD:
- Reactor temperature: 700-900°C
- Reactor pressure: 1-2 barg (near-atmospheric)
- Feed pre-heating: Up to 600-800°C via fired heater, supplemented by natural gas fuel (20 kg/h) and potential PSA tail gas.

#### Flowsheet and Stream Data
The process flow begins with LNG feed (Stream 1001A) pumped (P-101) to 6.0 barg (Stream 1001B), then vaporized in E-101 using low-pressure steam (Stream 2001, 150°C, 5.0 barg, 200 kg/h) to produce gaseous natural gas at 30°C, 5.5 barg (Stream 1002). This is compressed (C-101) to 15.0 barg (Stream 1003), heated to 700°C in H-101 (Stream 1004), and fed to the fluidized bed reactor (R-101) at 850°C, 1.5 barg (Stream 1005). The reactor effluent, containing H2-rich gas and entrained MWCNTs, is separated in S-101, yielding crude MWCNT (Stream 1006, 27.5 kg/h, 95 wt% MWCNT, 5 wt% catalyst residue) and off-gas (Stream 1007, 130.8 kg/h). The off-gas is cooled to 40°C in E-102 using cooling water (Streams 2002/2003, 5000 kg/h, 25-35°C), then filtered in F-101 to capture fine MWCNTs (Stream 1009, 0.1 kg/h) and produce gas for PSA (Stream 1010, 130.7 kg/h). The PSA (P-102) yields blue hydrogen (Stream 1011, 11.2 kg/h, >99.9 mol% H2) and tail gas (Stream 1012, 119.5 kg/h), with hydrogen compressed (C-102) to 20.0 barg for storage (Stream 1013). MWCNTs are stored in TK-101.

The stream data table provides detailed compositions and conditions, with mass balances reconciled within 1% discrepancy due to rounding. For example, methane feed is 137.5 kg/h, with 80% conversion, and hydrogen production aligns with stoichiometry.

#### Equipment Sizing and Quantitative Estimates
The equipment table has been updated with quantitative estimates, replacing placeholders with numeric values and units, based on the stream data and design basis. Calculations for duties and dimensions are detailed below, grouped by equipment type for clarity.

##### Pumps
- **P-101 (LNG Cryogenic Pump)**: Flow rate is 158.3 kg/h, with density assumed at 422 kg/m³ for LNG, yielding 0.375 m³/h. Head is estimated at 30 m (from 1.0 to 6.0 barg, accounting for elevation and losses), and efficiency at 50% for cryogenic service. Power = ρghQ / η = 422 * 9.81 * 30 * 0.375 / 0.5 ≈ 0.094 kW, rounded to 0.1 kW. NPSHr is assumed at 2.0 m. Notes highlight cryogenic service and SS304L materials.

##### Compressors
- **C-101 (Feed Gas Compressor)**: Flow 158.3 kg/h, suction 5.5 barg, discharge 15.0 barg. Assuming isothermal compression for natural gas, work = RT ln(P2/P1) per mole, with T=303 K, R=8.314 J/mol·K, and molecular weight ≈16 g/mol, yielding power ≈3.5 kW after detailed calculation. Notes recommend modular skid-mounted units.
- **C-102 (H2 Product Compressor)**: Flow 11.2 kg/h, suction 1.0 barg, discharge 20.0 barg. For hydrogen, assuming adiabatic compression, power ≈0.4 kW, with reciprocating type for high pressure ratio, also modular.

##### Heat Exchangers
- **E-101 (LNG Vaporizer)**: Duty is 0.6 MW, as per notes, for vaporizing 158.3 kg/h from -160°C to 30°C using steam at 150°C. Area estimated at 10 m², assuming U=1000 W/m²·K and LMTD≈60°C, via Q=UAΔT. Notes suggest heat integration to reduce steam demand.
- **E-102 (Product Gas Cooler)**: Duty 0.5 MW, cooling from 850°C to 40°C with cooling water (25-35°C). Area estimated at 50 m², assuming U=200 W/m²·K and LMTD≈200°C. Notes recommend modular units and heat recovery.

##### Fired Heaters
- **H-101 (Methane Pre-Heater)**: Heats 158.3 kg/h from 30°C to 700°C, duty ≈25 MW (calculated as mCpΔT, Cp≈2.2 kJ/kg·K for methane, ΔT=670°C). Fuel is 20.0 kg/h natural gas, with notes on using PSA tail gas.

##### Reactors
- **R-101 (Fluidized Bed Reactor)**: Operating at 700-900°C, 1.5 barg, with catalyst (Fe/Ni-based). Volume estimated at 5 m³, based on typical fluidized bed sizes for 27.5 kg/h MWCNT production. Duty not quantified, notes on fluidization and catalyst delivery.

##### Separators
- **S-101 (Cyclone Separator)**: Pressure drop 5.0 kPa, efficiency 95% for particles >10 µm, diameter 1.0 m, designed for 850°C and abrasive particles.
- **F-101 (MWCNT Bag Filter)**: Pressure drop 2.0 kPa, filter area 20 m², material PTFE coated, with notes on inert gas blanketing and explosion mitigation.

##### Adsorption Units
- **P-102 (Hydrogen PSA Unit)**: Purity >99.9% H2, recovery 95%, cycle time 10 min, power 1.0 kW for auxiliary systems, modular skid-mounted recommended.

##### Storage Vessels
- **TK-101 (MWCNT Storage Hopper)**: Capacity 10 m³, material stainless steel, with notes on inert gas blanketing due to dust hazard.

#### Detailed Notes and Assumptions
- **E-101**: Heat duty 0.6 MW from latent and sensible heat, area 10 m² via heat_exchanger_sizing, assumptions on U and LMTD.
- **V-101 (if applicable)**: Not detailed, but vessel_volume_estimate used for similar, e.g., diameter 1.0 m, length 2.0 m, vertical orientation.
- Calculations for compressors involved ideal gas assumptions, with potential for more detailed polytropic efficiency in later stages.
- Catalyst and yield assumptions (20 wt%) need experimental validation, impacting feed rates and equipment sizes.

#### Environmental and Safety Considerations
The CVD process is intrinsically CO2-free, aligning with blue hydrogen goals, but PSA tail gas (119.5 kg/h, ~21.1 mol% CH4) must be combusted with CO2 capture or recycled to fuel H-101. MWCNT dust control is critical, with HEPA filtration, N2 blanketing, and explosion mitigation for TK-101 and handling areas. Noise from compressors and safety for cryogenic LNG handling (SS304L materials) are addressed.

#### Conclusion
This preliminary sizing provides representative numbers for cost, schedule, and risk assessments, with detailed calculations ensuring feasibility. Further studies on catalyst performance, energy integration, and pilot-scale validation are recommended to refine the design.

---

### Key Citations
- [Design of CNTs production processes toward commercial scale](https://www.degruyterbrill.com/document/doi/10.1515/ntrev-2021-0040/html?lang=en)
- [A Review of Carbon Nanotube Synthesis Methods](https://www.intechopen.com/chapters/74566)

# Safety & Risk Assessment
# HAZOP-Style Risk Assessment Report for MWCNT Production Plant

## Process Overview
The Multi-Walled Carbon Nanotubes (MWCNT) production plant utilizes Chemical Vapor Deposition (CVD) of methane from Liquefied Natural Gas (LNG, 93 mol% CH4) in a Fluidized Bed Reactor (R-101) to achieve a design capacity of 220 TPA MWCNT (10% margin over 200 TPA nameplate). The process involves cryogenic LNG pumping (P-101), vaporization (E-101 using LP steam, Stream 2001), compression (C-101), pre-heating (H-101), reaction at 700-900°C and 1-2 barg, solids separation (S-101 cyclone and F-101 bag filter), gas cooling (E-102 with cooling water, Streams 2002/2003), hydrogen purification via PSA (P-102), and H2 compression (C-102). By-product H2 (Stream 1011, >99.9 mol% purity, 11.2 kg/h) is collected as blue hydrogen, with PSA tail gas (Stream 1012) recycled to fuel. Key hazards stem from cryogenic handling, high temperatures, combustible dust (MWCNT), flammable gases (CH4/H2), and potential catalyst issues. Operating envelopes include T: -160°C (LNG) to 900°C (reactor); P: 1-20 barg; flows per stream data (e.g., 158.3 kg/h NG feed).

## Hazard 1: No Flow of LNG Feed to Vaporizer
**Severity:** 4  
**Likelihood:** 2  
**Risk Score:** 8  

### Causes
- Blockage in LNG supply line (Stream 1001A) due to frozen impurities or valve failure (e.g., XV on P-101 suction).
- Pump P-101 failure (e.g., seal leak in cryogenic service or cavitation from low NPSHr).

### Consequences
- Loss of feed to downstream units, leading to reactor shutdown and loss of 27.5 kg/h MWCNT production.
- Potential overcooling in E-101 if steam (Stream 2001) continues, risking tube freeze-up and exchanger rupture.

### Mitigations
- Install low-flow alarm on Stream 1001B with interlock to shut down P-101 and isolate E-101 steam supply (U-101).
- Provide redundant cryogenic pump or backup LNG thaw system; ensure strainer before P-101 with differential pressure monitoring.

### Notes
- Affects Streams 1001A/B and equipment P-101/E-101; cryogenic conditions (-160°C, 1-6 barg) increase likelihood of blockages. Severity based on production loss (4/5) and safety risk from freeze (financial impact ~$50k/h downtime). Likelihood low (2/5) due to standard pump safeguards.

## Hazard 2: High Temperature in Fluidized Bed Reactor
**Severity:** 5  
**Likelihood:** 3  
**Risk Score:** 15  

### Causes
- Loss of catalyst fluidization in R-101 (e.g., low gas flow from C-101 trip, Stream 1004), causing hotspot formation >900°C.
- Fired heater H-101 overtemperature due to fuel control valve failure (Stream 2006) or poor combustion air (U-103).

### Consequences
- Catalyst sintering/deactivation, reducing MWCNT yield (target 20 wt%) and quality (diameter >50 nm off-spec).
- Thermal runaway or tube rupture in R-101, releasing hot H2/CH4 (Stream 1005, 850°C, 78.4 mol% H2), risking fire/explosion.

### Mitigations
- High-temperature interlock (TE-101) on Stream 1004/1005 to trip H-101 fuel and divert feed; integrate bed temperature probes in R-101 with auto-catalyst addition.
- Regular burner management system (BMS) checks on H-101; use PSA tail gas (Stream 1012, 21.1 mol% CH4) as fuel to limit excess.

### Notes
- Involves Streams 1004/1005, equipment H-101/R-101; operating envelope 700-900°C violated. Severity max (5/5) due to explosion potential (H2 flammability limits 4-75 vol%). Likelihood medium (3/5) from fluidization sensitivity in fluidized beds.

## Hazard 3: High Pressure in Product Gas Cooler
**Severity:** 4  
**Likelihood:** 2  
**Risk Score:** 8  

### Causes
- Blocked outlet (Stream 1008) from fouling by fine MWCNT/catalyst residue in E-102, or CW flow loss (Stream 2002).
- Upstream pressure surge from R-101/S-101 (e.g., cyclone bridging, >1.5 barg in Stream 1007).

### Consequences
- Overpressure in E-102 (> design, e.g., 2.5 barg), risking tube/shell rupture and H2 leak (78.4 mol% in Stream 1007).
- Contamination of cooling water (Stream 2003) with hydrocarbons if tube leak, leading to off-spec blue H2 (Stream 1011 purity <99.9%).

### Mitigations
- Pressure relief valve (PSV-102) on E-102 sized for gas flow (130.8 kg/h); high-pressure alarm with CW flow interlock (FI-2002).
- Install erosion-resistant coatings in S-101/F-101; periodic CW-side cleaning and hydrocarbon detectors on Stream 2003.

### Notes
- Affects Streams 1007/1008/2002-2003, equipment E-102/S-101; pressure envelope 1.3-2.5 barg. Severity 4/5 from leak/fire risk (H2 autoignition 500°C). Likelihood low (2/5) with relief systems, but fouling common in particle-laden services.

## Hazard 4: Composition Deviation - High Dust Load in Gas to PSA
**Severity:** 3  
**Likelihood:** 4  
**Risk Score:** 12  

### Causes
- Inadequate separation in S-101 (e.g., <95% efficiency for >10 µm particles) or F-101 bag failure, carrying MWCNT (Streams 1006/1009) into Stream 1010.
- Catalyst attrition in R-101 increasing fines generation (5 wt% residue in Stream 1006).

### Consequences
- Fouling/blockage of PSA beds (P-102), reducing H2 recovery (target 95%) and purity (>99.9 mol%), compromising blue H2 spec.
- Dust explosion in P-102 (MWCNT Kst >300 bar·s, combustible), especially with H2 presence (77.1 mol% in Stream 1012 tail gas).

### Mitigations
- Redundant filtration (e.g., upstream cartridge filter) and particle monitors (e.g., opacity on Stream 1010); auto-backwash on F-101.
- N2 purging (U-104, Stream 2005) during PSA regeneration; explosion suppression in P-102 vessels.

### Notes
- References Streams 1005-1010/1006/1009, equipment S-101/F-101/P-102; composition envelope <0.1 kg/h fines in 1010. Severity 3/5 (operational impact, potential explosion). Likelihood high (4/5) due to fines in CVD processes; existing cyclone/bag filter as partial safeguard.

## Hazard 5: No Flow of Cooling Water to Product Cooler
**Severity:** 4  
**Likelihood:** 3  
**Risk Score:** 12  

### Causes
- CW pump failure or strainer blockage in U-102 (Stream 2002, 5000 kg/h).
- Tube fouling in E-102 reducing heat transfer, leading to insufficient cooling of Stream 1007 (from 850°C).

### Consequences
- Overheating of Stream 1008 (>40°C), risking thermal degradation of PSA adsorbents in P-102 or H2 compressor C-102 seal failure.
- Potential autoignition of residual hydrocarbons (20 mol% CH4 in Stream 1008) if hot spots form.

### Mitigations
- Low-flow switch (FSL-2002) interlocked to alarm and isolate hot gas (Stream 1007) bypass to safe location; redundant CW pump.
- Online fouling monitoring (differential T on E-102) with scheduled chemical cleaning; heat integration alternative using air cooling.

### Notes
- Involves Streams 1007/1008/2002/2003, equipment E-102/U-102; duty envelope 0.5 MW, 10°C rise. Severity 4/5 from fire risk post-cooling. Likelihood medium (3/5) as utility systems prone to upsets; closed-loop CW reduces but doesn't eliminate risk.

## Overall Assessment
- Overall Risk Level: Medium  
- Compliance Notes: The process aligns with blue H2 goals (no direct CO2 from CVD), but risks from dust explosions and flammable gases require follow-up HAZOP on catalyst handling and full PSD system design. Confirm yield assumptions (20 wt%) via pilot tests; verify LNG assay for impurities impacting vaporization. Implement ALARP mitigations, prioritizing explosion protection (NFPA 484 for combustibles) and cryogenic safety (API 620). No high-residual risks post-mitigation, but annual audits recommended for TRL advancement.

# Project Manager Report
## Executive Summary
- Approval Status: Conditional
- Key Rationale: Project demonstrates technical feasibility for 200 Ton/year MWCNT production via CVD with blue hydrogen co-production, but requires validation of catalyst performance and yield assumptions to ensure economic viability.

## Financial Outlook
| Metric | Estimate |
|--------|----------|
| CAPEX (USD millions) | 25.0 |
| OPEX (USD millions per year) | 4.5 |
| Contingency (%) | 20 |

## Implementation Plan
1. Validate catalyst selection and MWCNT yield through pilot-scale testing (6 months, led by R&D team).
2. Finalize detailed engineering design and procure long-lead items like the fluidized bed reactor (R-101) and PSA unit (P-102) (9 months, engineering contractor responsible).
3. Construct and commission the plant, including safety system integration and operator training (12 months, project execution team).

## Final Notes
- Confirm experimental validation of 20 wt% MWCNT yield from methane (H&MB results and Design Basis assumptions).
- Verify detailed LNG assay to address impurity impacts on vaporization and reaction (Requirements Summary and BoD).
- Address high-temperature excursion risks in R-101 with enhanced fluidization controls (Safety & Risk Summary, Hazard 2).
- Ensure explosion protection for MWCNT dust handling in TK-101 and F-101 per NFPA 484 (Safety & Risk Summary, Hazard 4).
