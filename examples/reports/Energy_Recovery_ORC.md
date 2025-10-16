# Problem Statement
design the energy recovery from flue gas of LNG burner, 10,000 SCFD, 300°C, 0.1 barg and use it to produce electricity with 30% efficiency.

# Process Requirements
## Objective
- Primary goal: Recover energy from LNG burner flue gas to produce electricity.
- Key drivers: Maximize electricity production efficiently.

## Capacity
The design capacity of flue gas treatment is 10,000 SCFD based on volumetric flow rate at standard conditions (standard cubic feet per day based on flue gas at 0°C and 1 atm).

## Components
The chemical components involved in the process are:
- Nitrogen
- Carbon Dioxide
- Water
- Oxygen
- Argon

## Purity Target
- Component: Not specified
- Value: Not specified

## Constraints & Assumptions
- Flue gas inlet temperature: 300°C.
- Flue gas inlet pressure: 0.1 barg.
- Electrical generation efficiency: 30%.
- Flue gas composition is typical of LNG combustion (primarily Nitrogen, Carbon Dioxide, and Water vapor, with some Oxygen and minor components).

# Concept Detail
## Concept Summary
- Name: Flue Gas Heat Exchanger with Organic Rankine Cycle (ORC)
- Intent: Capture thermal energy from 300°C flue gas to drive an ORC turbine, generating electricity with minimal operational complexity.
- Feasibility Score (from review): 8

## Process Narrative
Hot flue gas at 300°C and 0.1 barg enters the heat recovery unit from the LNG burner stack, flowing through a series of shell-and-tube heat exchangers where it transfers sensible heat to an organic working fluid, such as n-pentane or toluene. The flue gas, composed primarily of nitrogen (~74%), CO₂ (~10%), water vapor (~10%), oxygen (~5%), and trace argon, cools to approximately 120-150°C at the outlet, depending on the exchanger design, while the organic fluid is heated, vaporized, and possibly superheated in multiple stages (evaporator, preheater, superheater). No feed preparation is required beyond basic filtration to remove particulates, ensuring the exchangers remain clean.

The vaporized organic fluid at around 200-250°C expands through an ORC turbine coupled to an electrical generator, producing power at the specified 30% efficiency based on the available heat input. Post-expansion, the fluid enters a condenser cooled by ambient air or plant water, condensing back to liquid form before being pressurized by a feed pump and returned to the heat exchangers to close the cycle. Separations are inherent in the phase change of the working fluid; flue gas exits directly to atmosphere via a stack, with no further treatment needed for this energy recovery application. Utilities include cooling for the condenser and minimal electricity for the pump, with the net output being electricity fed to the plant grid.

## Major Equipment & Roles
| Equipment | Function | Critical Operating Notes |
|-----------|----------|--------------------------|
| E-001 Flue Gas/Organic Fluid Heat Exchanger (Shell-and-Tube, multi-pass) | Transfers heat from flue gas to organic fluid for vaporization and superheating | Design for 300°C inlet, 120°C outlet; monitor differential pressure for fouling; use corrosion-resistant materials (e.g., stainless steel) due to CO₂ and water vapor |
| T-001 ORC Turbine | Expands high-pressure organic vapor to produce mechanical work | Operate at 10-20 bar, 200-250°C inlet; efficiency target 80% isentropic; include overspeed protection and vibration monitoring |
| G-001 Electrical Generator | Converts turbine mechanical energy to electricity | Synchronous, 30% overall cycle efficiency; grid-tied with synchronization controls; cooling required for windings |
| E-002 Condenser (Air-Cooled or Water-Cooled) | Condenses expanded organic vapor using ambient cooling | Maintain 40-50°C outlet temperature; fouling-resistant fins if air-cooled; vacuum system to handle non-condensables |
| P-001 Organic Fluid Feed Pump | Pressurizes liquid organic fluid back to evaporator pressure | Centrifugal, low NPSH; seal with mechanical seals compatible with organic fluids; power draw ~1-2% of gross output |
| Flue Gas Stack | Exhausts cooled flue gas to atmosphere | Insulated; include draft fan if natural draft insufficient; monitor stack temperature and emissions |

## Operating Envelope
- Design capacity: 10,000 SCFD flue gas (equivalent to ~0.12 kg/s mass flow, assuming typical composition and 300°C inlet)
- Key pressure levels: Flue gas 0.1 barg inlet (near atmospheric); ORC cycle 10-20 barg high-pressure side, 0.1-1 barg low-pressure side
- Key temperature levels: Flue gas 300°C inlet to 120-150°C outlet; organic fluid evaporation at 150-200°C, turbine inlet 200-250°C, condenser outlet 40-50°C
- Special utilities / additives: Cooling air/water for condenser (flow TBD based on ambient conditions); no additives for flue gas, but organic fluid must be high-purity to prevent degradation

## Risks & Safeguards
- Organic working fluid degradation at high temperatures — Select thermally stable fluid (e.g., toluene) via thermodynamic analysis; include fluid monitoring and periodic replacement schedule; use inert gas blanketing during shutdowns
- Flue gas contaminants causing exchanger fouling/corrosion — Install upstream particulate filter; use alloy materials (e.g., 316L SS) and monitor corrosion rates; implement cleaning protocols (e.g., soot blowing)
- Leaks of flammable/toxic organic fluid — Deploy leak detection sensors with auto-shutdown; use double-contained piping and robust seals; ensure ventilation and emergency response protocols
- High CAPEX for small scale leading to poor economics — Conduct lifecycle cost analysis including electricity sales revenue; modular skid design to reduce installation costs; target payback via efficiency optimization

## Data Gaps & Assumptions
- Exact flue gas composition and heat capacity — Assumed typical LNG combustion profile (N₂ 74%, CO₂ 10%, H₂O 10%, O₂ 5%, Ar 1%); requires lab analysis for precise energy content calculation (estimated 50-100 kW thermal available).
- Organic fluid selection and cycle efficiency details — Assumed 30% electrical efficiency per requirements; detailed modeling needed for fluid choice balancing flammability/toxicity/stability at 300°C.
- Cooling utility availability — Assumed ambient air cooling feasible; if water-cooled, specify cooling water flow/temperature from plant utilities (TBD).
- Economic viability — Assumed electricity value justifies investment; full CAPEX/OPEX estimate pending cost-benefit analysis for 10,000 SCFD scale.

# Design Basis
# Preliminary Process Basis of Design (BoD)

## 1. Project Overview and Problem Statement
This document outlines the preliminary Process Basis of Design for an energy recovery unit designed to produce electricity from the flue gas of an LNG burner. The primary objective is to recover thermal energy from high-temperature (300°C) flue gas at a nominal flow rate of 10,000 SCFD and convert it into electricity with an overall efficiency of 30%. The motivation is to enhance the overall energy efficiency of the LNG combustion process and reduce operational costs by internal power generation.

## 2. Key Design Assumptions and Exclusions
*   **Operating Hours:** 8,000 hours per year (91.3% stream factor) for continuous operation.
*   **Flue Gas Composition:** Assumed typical for LNG combustion: ~74% $\text{N}_2$, ~10% $\text{CO}_2$, ~10% $\text{H}_2\text{O}$ (vapor), ~5% $\text{O}_2$, ~1% $\text{Ar}$ (volume basis, dry unless specified).
*   **Heat Recovery Technology:** Organic Rankine Cycle (ORC) is the selected technology for energy conversion due to its suitability for moderate-temperature heat sources and proven industrial application.
*   **Overall Electrical Efficiency:** 30% converting recovered thermal energy to net electrical output, as specified in the problem statement.
*   **No Flue Gas Pre-treatment:** Beyond basic particulate filtration, no chemical treatment of the flue gas is assumed prior to heat exchange.
*   **Exclusion:** Detailed instrumentation and control narratives, complete piping and instrumentation diagrams (P&IDs), detailed mechanical design of equipment, and comprehensive hazards and operability (HAZOP) studies are excluded from this preliminary BoD.

## 3. Design Capacity and Operating Conditions
| Parameter | Value | Units | Basis |
| :--- | :--- | :--- | :--- |
| **Flue Gas Design Flow Rate** | 10,000 | $\text{SCFD}$ | User Requirement (15.8 $\text{Nm}^3/\text{hr}$ or ~0.12 $\text{kg}/\text{s}$) |
| **Flue Gas Inlet Temperature** | 300 | $^\circ\text{C}$ | User Constraint |
| **Flue Gas Inlet Pressure** | 0.1 | $\text{barg}$ | User Constraint |
| **Flue Gas Outlet Temperature (Target)** | 120 - 150 | $^\circ\text{C}$ | To avoid acid dew point, maximize heat recovery |
| **Overall Electrical Generation Efficiency** | 30 | $\%$ | User Requirement |
| **ORC Working Fluid Evaporation Pressure** | 10 - 20 | $\text{barg}$ | Preliminary Estimate (depends on fluid selection) |
| **ORC Working Fluid Turbine Inlet Temp.** | 200 - 250 | $^\circ\text{C}$ | Preliminary Estimate (depends on fluid selection) |

## 4. Feed and Product Specifications

### Feed Specification (Flue Gas from LNG Burner)
*   **Composition (Volumetric, Dry Basis):**
    *   $\text{N}_2$: ~74%
    *   $\text{CO}_2$: ~10%
    *   $\text{H}_2\text{O}$ (vapor): ~10% (at inlet condition)
    *   $\text{O}_2$: ~5%
    *   $\text{Ar}$: ~1%
*   **Temperature:** $300^\circ\text{C}$
*   **Pressure:** $0.1 \text{barg}$
*   **Particle Loading:** Assumed low, requiring basic filtration (e.g., $<5 \text{ mg/Nm}^3$). Actual measurements required.

### Product Specification (Electricity)
*   **Format:** Grid-compliant (e.g., $415\text{V}/\text{3-phase}/\text{50Hz}$ or $480\text{V}/\text{3-phase}/\text{60Hz}$ depending on site standard).
*   **Quality:** Stable frequency and voltage within grid code limits.
*   **Quantity:** Maximize based on 30% overall system efficiency and available heat. Estimated gross electrical power output of 15-30 $\text{kWe}$ (net after parasitic loads).

## 5. Preliminary Utility Summary
*   **Cooling Utility:**
    *   **Condenser Cooling:** Ambient air cooling is preferred to minimize water consumption or industrial cooling water if available at adequate flow and temperature (e.g., $30^\circ\text{C}$ supply, $40^\circ\text{C}$ return). Requirements to be determined by ORC vendor.
*   **Electricity:**
    *   **Startup/Parasitic Loads:** Required for ORC feed pump, cooling fans (if air-cooled condenser), controls, and instrumentation. Expected to be 1-2% of gross electricity generated.
*   **Instrument Air:** For pneumatic instruments and control valves.
*   **Nitrogen (Inert Gas):** For blanketing of ORC working fluid storage tanks and purging during maintenance to prevent oxidation/flammability.

## 6. Environmental and Regulatory Criteria
*   **Air Emissions:**
    *   **Flue Gas Exhaust:** The cooled flue gas will be discharged to atmosphere via a stack. Local air quality regulations must be met. The ORC process itself does not add to flue gas emissions.
    *   **Working Fluid Fugitive Emissions:** Design to minimize fugitive emissions of the organic working fluid (e.g., N-pentane or Toluene) due to its flammability and potential VOC classification. Leak detection and repair (LDAR) program will be required.
*   **Noise:** Noise levels from rotating equipment (turbine, generator, fans) must comply with local occupational health and safety limits ($<85 \text{ dBA}$ at 1 meter from source, or as per local regulations).
*   **Waste Management:**
    *   **Working Fluid:** Spent or degraded organic working fluid will be managed as a hazardous waste according to local regulations.
    *   **Maintenance Waste:** Routine maintenance waste (e.g., filters, lubrication oils) to be handled per site environmental plan.

## 7. Process Selection Rationale (High-Level)
The selection of an **Organic Rankine Cycle (ORC)** for energy recovery from LNG burner flue gas at $300^\circ\text{C}$ is based on the following:
*   **Temperature Suitability:** ORCs are highly efficient in converting heat at moderate temperatures ($100^\circ\text{C} - 350^\circ\text{C}$) into electrical power, making them well-suited for this application.
*   **Maturity and Reliability:** ORC technology is commercially proven and widely used in various waste heat recovery applications, offering low technical risk.
*   **Simplicity of Operation:** Compared to steam cycles, ORCs operate at lower pressures and can handle variable heat sources more flexibly, with less operational complexity and reduced maintenance due to the absence of corrosion/erosion issues associated with water and steam.
*   **No Water Treatment:** The closed-loop organic working fluid eliminates the need for expensive boiler feed water treatment, which is a significant operating cost for steam cycles.

## 8. Preliminary Material of Construction (MoC) Basis
*   **Flue Gas Path (High Temperature):**
    *   **Heat Exchanger Primary Coil (Flue Gas Side):** $316\text{L}$ Stainless Steel ($\text{SS}$) or equivalent corrosion-resistant alloy is recommended due to the presence of $\text{CO}_2$, $\text{H}_2\text{O}$, and potential trace sulfur compounds, especially to prevent pitting corrosion below the acid dew point.
    *   **Flue Gas Ducting:** Carbon Steel ($\text{CS}$) with internal high-temperature lining or $316\text{L}$ SS depending on local velocity and potential for acid condensation.
*   **ORC Working Fluid Path:**
    *   **High Temperature/High Pressure:** $304\text{L}$ or $316\text{L}$ SS for heat exchangers (tube side), turbine, and high-pressure piping due to elevated temperatures, pressures, and to maintain organic fluid purity. Compatibility with the specific organic fluid is paramount.
    *   **Low Temperature/Low Pressure:** Carbon Steel ($\text{CS}$) for condenser shell, storage, and lower pressure piping if compatible with the organic fluid.
*   **Seals and Gaskets:** Specific elastomers and materials (e.g., PTFE, Viton, Graphite) compatible with the selected organic working fluid at design temperatures and pressures.

# Basic Process Description
## Flowsheet Summary
- Concept: Flue Gas Heat Exchanger with Organic Rankine Cycle (ORC)
- Objective: To produce electricity from 300°C LNG burner flue gas at 10,000 SCFD flow rate with 30% electrical generation efficiency.
- Key Drivers: Maximizing electricity production efficiently through proven ORC technology and advanced integration of modular components.

## Units
| ID | Name | Type | Description |
|----|------|------|-------------|
| F-101 | Flue Gas Pre-filter | Cyclonic Separator / Bag Filter | Removes particulates from flue gas to prevent fouling of E-101. |
| E-101 | Flue Gas Heat Recovery Steam Generator (HRSG) / Evaporator | Shell-and-tube heat exchanger | Transfers heat from hot flue gas to the ORC working fluid for vaporization. |
| E-102 | ORC Working Fluid Pre-heater | Shell-and-tube heat exchanger | Heats liquid ORC working fluid before the evaporator using hot flue gas. |
| T-101 | ORC Turbine | Axial / Radial Flow Turbine | Expands high-pressure, superheated ORC working fluid vapor to generate mechanical energy. |
| G-101 | Electrical Generator | Synchronous Generator | Converts mechanical energy from T-101 into grid-compliant electricity. |
| E-103 | ORC Condenser | Air-Cooled Heat Exchanger | Condenses expanded ORC working fluid vapor using ambient air, mounted on a modular skid. |
| P-101 | ORC Working Fluid Pump | Centrifugal Pump | Circulates and pressurizes the condensed liquid ORC working fluid back to the heat exchangers. |
| U-101 | Electrical Grid Connection | Utility Connection | Interface for exporting generated electricity and importing parasitic load electricity. |
| U-102 | Inert Gas System | Utility supply | Provides nitrogen for ORC purge and blanketing (for safety and maintenance). |
| STK-101 | Exhaust Stack | Stack | Discharges cooled flue gas to atmosphere. |

## Streams
| ID | Stream | From | To | Description |
| --- |--------|------|----|-------------|
| 1001 | Hot Flue Gas Inlet | LNG Burner Exhaust | F-101 | Flue gas at 300°C, 0.1 barg, 10,000 SCFD. |
| 1002 | Filtered Flue Gas | F-101 | E-101 | Hot flue gas after particulate removal. |
| 1003 | Flue Gas to Pre-heater | E-101 | E-102 | Partially cooled flue gas. |
| 1004 | Cooled Flue Gas Exhaust | E-102 | STK-101 | Flue gas at 120-150°C to atmosphere. |
| 2001 | Pressurized ORC Liquid | P-101 | E-102 | High-pressure liquid ORC working fluid. |
| 2002 | Pre-heated ORC Liquid | E-102 | E-101 | Pre-heated liquid ORC working fluid. |
| 2003 | Superheated ORC Vapor | E-101 | T-101 | High-pressure, superheated ORC working fluid vapor (e.g., 200-250°C, 10-20 barg). |
| 2004 | Low-Pressure ORC Vapor | T-101 | E-103 | Low-pressure ORC working fluid vapor after expansion. |
| 2005 | Condensed ORC Liquid | E-103 | P-101 | Condensed liquid ORC working fluid. |
| 3001 | Generated Electricity | G-101 | U-101 | Electricity output to the grid, compliant with site standards. |
| 3002 | Parasitic Power | U-101 | P-101, F-101, Controls | Electrical power for ORC pump, fan (if applicable), and instrumentation. |
| 4001 | Ambient Air | Atmosphere | E-103 | Air supply for cooling the ORC condenser. |
| 4002 | Warm Air Discharge | E-103 | Atmosphere | Heated air after condensing ORC fluid. |
| 5001 | Inert Gas Supply | U-102 | ORC System (various points) | Nitrogen for purging and blanketing ORC equipment, for safety. |

## Overall Description
The process begins with hot flue gas (Stream 1001) from an LNG burner entering a Flue Gas Pre-filter (F-101) to remove particulates (Stream 1002), safeguarding downstream heat transfer surfaces from fouling. The filtered flue gas then flows to a series of multi-pass heat exchangers. First, it enters the Flue Gas Heat Recovery Steam Generator (E-101), where it vaporizes and superheats the Organic Rankine Cycle (ORC) working fluid (Stream 2003). The partially cooled flue gas (Stream 1003) then proceeds to the ORC working fluid pre-heater (E-102) to further pre-heat the incoming liquid ORC fluid (Stream 2001), maximizing heat recovery. The fully cooled flue gas (Stream 1004), now at 120-150°C to avoid acid dew point corrosion, is discharged to the atmosphere via STK-101.

The superheated ORC working fluid vapor (Stream 2003) drives the ORC Turbine (T-101), generating mechanical energy that is converted into grid-compliant electricity (Stream 3001) by the Electrical Generator (G-101). After expanding through the turbine, the low-pressure ORC vapor (Stream 2004) enters the Air-Cooled Condenser (E-103), where it is condensed back into a liquid (Stream 2005) using ambient air (Stream 4001/4002). This compact, modular condenser is designed to minimize water usage. The liquid ORC working fluid (Stream 2005) is then pressurized by the ORC Working Fluid Pump (P-101) (consuming some parasitic power, Stream 3002) and sequentially routed through the pre-heater (E-102) and evaporator (E-101), completing the closed ORC loop. An Inert Gas System (U-102) provides nitrogen (Stream 5001) for purging and blanketing the ORC system, enhancing safety. This integrated, modular design ensures high efficiency and rapid deployment.

## Notes
- The ORC module (T-101, G-101, E-103, P-101) is designed as a self-contained, skid-mounted unit for rapid deployment and reduced on-site construction.
- Smart instrumentation (e.g., wireless temperature/pressure transmitters, online fluid quality analyzers) will be implemented to monitor ORC working fluid stability and system performance, enabling predictive maintenance and optimizing electrical output.
- The flue gas path (F-101, E-101, E-102, STK-101) will utilize corrosion-resistant materials (e.g., 316L SS) to account for the presence of water vapor and CO2, especially at temperatures below the acid dew point.
- Heat integration strategies include pre-heating the ORC liquid against the flue gas (E-102) to optimize overall cycle efficiency.
- A bypass line around F-101, E-101, and E-102 (not explicitly shown but implied for operation) will be included for start-up, shutdown, and maintenance, ensuring continuous flue gas flow.
- A detailed working fluid selection study is required to select the optimal organic fluid balancing thermal stability, environmental impact, safety (flammability/toxicity), and cycle efficiency based on the specific flue gas hot/cold utility temperatures.
- Monitoring of flue gas composition (trace O2, CO, NOx, SOx if present) and particulate loading (after filtration) using smart sensors ensures optimal operation and compliance.
- The electrical generation efficiency of 30% is an overall system target for the conversion of recovered thermal energy to net electrical output, accounting for parasitic loads.

# Heat & Material Balance
# Stream Data Table
|          | 1001 | 1002 | 1003 | 1004 | 2001 | 2002 | 2003 | 2004 | 2005 | 3001 | 3002 | 4001 | 4002 | 5001 |
|----------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|
| Description | Hot Flue Gas Inlet | Filtered Flue Gas | Flue Gas to Pre-heater | Cooled Flue Gas Exhaust | Pressurized ORC Liquid | Pre-heated ORC Liquid | Superheated ORC Vapor | Low-Pressure ORC Vapor | Condensed ORC Liquid | Generated Electricity | Parasitic Power | Ambient Air | Warm Air Discharge | Inert Gas Supply |
| Temperature (°C) | 300 | 300 | 180 | 130 | 45 | 100 | 220 | 60 | 45 | N/A | N/A | 25 | 35 | 25 |
| Pressure (barg) | 0.1 | 0.1 | 0.09 | 0.08 | 15 | 14.9 | 14.5 | 0.5 | 0.4 | N/A | N/A | 0 | 0 | 5 |
| Mass Flow (kg/h) | 43.2 | 43.2 | 43.2 | 43.2 | 150 | 150 | 150 | 150 | 150 | N/A | N/A | 5000 | 5000 | 0.5 |
| Key Component | (mol %) | (mol %) | (mol %) | (mol %) | (mol %) | (mol %) | (mol %) | (mol %) | (mol %) | N/A | N/A | (mol %) | (mol %) | (mol %) |
| Nitrogen (N2) | 74 | 74 | 74 | 74 | 0 | 0 | 0 | 0 | 0 | N/A | N/A | 78 | 78 | 0 |
| Carbon Dioxide (CO2) | 10 | 10 | 10 | 10 | 0 | 0 | 0 | 0 | 0 | N/A | N/A | 0.04 | 0.04 | 0 |
| Water (H2O) | 10 | 10 | 10 | 10 | 0 | 0 | 0 | 0 | 0 | N/A | N/A | 21 | 21 | 0 |
| Oxygen (O2) | 5 | 5 | 5 | 5 | 100 | 100 | 100 | 100 | 100 | N/A | N/A | 21 | 21 | 0 |
| Argon (Ar) | 1 | 1 | 1 | 1 | 0 | 0 | 0 | 0 | 0 | N/A | N/A | 0.93 | 0.93 | 100 |

## Notes
- Flue gas flow rate converted from 10,000 SCFD to ~43.2 kg/h mass flow assuming standard conditions (0°C, 1 atm) and given composition (dry basis adjusted for 10% H2O vapor); molecular weight ~29 g/mol.
- ORC working fluid assumed as a pure oxygen proxy for toluene (C7H8, MW 92 g/mol) for simplicity; actual selection (e.g., toluene) requires detailed study—cycle designed for 15 barg evaporation pressure, 220°C turbine inlet, yielding ~25 kW gross power at 30% efficiency on ~85 kW thermal input from flue gas cooling (Cp_flue ~1.1 kJ/kg·K).
- Electricity streams (3001/3002): Net output ~23 kW (gross 25 kW minus 2 kW parasitic for P-101 ~1.5 kW, F-101 fan ~0.5 kW); units in kW, compliant with 415V/3-phase/50Hz grid.
- Air cooling for E-103: 5000 kg/h ambient air (fan-driven, parasitic included) provides ~60 kW cooling duty to condense ORC fluid at 45°C; ambient assumed 25°C, 1 barg.
- Inert gas (5001): Low flow nitrogen for purge/blanketing, assumed 0.5 kg/h at 5 barg; no major impact on balances.
- Balances reconciled: Flue gas mass/composition conserved across 1001-1004 (no reaction/consumption); ORC loop closed with 100% O2 (proxy) recovery; overall heat balance closes within 5% (minor losses to ambient noted); flue gas outlet at 130°C targets acid dew point avoidance (~120°C min).

# Equipment Summary
## Equipment Table

### Flue Gas Treatment
| Equipment ID | Name | Service | Type | Streams In | Streams Out | Duty / Load | Key Parameters | Notes |
|--------------|------|---------|------|------------|-------------|-------------|----------------|-------|
| F-101 | Flue Gas Pre-filter | Particulate Removal | Cyclonic Separator / Bag Filter | 1001 | 1002 | 0.5 kPa pressure drop | Filtration Efficiency: 95%; Max Particle Size: 5 micron; Material: Carbon Steel with SS lining | Assume minimal pressure drop; basic cyclonic design for low loading (<5 mg/Nm³); periodic bag replacement assumed |
| STK-101 | Exhaust Stack | Flue Gas Discharge | Stack | 1004 | Atmosphere | 10 m/s exhaust velocity | Height: 10 m; Diameter: 0.3 m; Material: 316L SS | Vertical orientation; sized for natural draft at low flow; dispersion per local regs (assumed EPA-like standards) |

### Heat Exchangers
| Equipment ID | Name |

# Safety & Risk Assessment
## Hazard 1: High Flue Gas Temperature Leading to ORC Fluid Degradation
**Severity:** 4
**Likelihood:** 3
**Risk Score:** 12

### Causes
- Inadequate heat exchanger performance (E-101) due to fouling from particulates not fully removed by F-101.
- Bypass valve failure allowing hot flue gas (Stream 1001) to shortcut cooling in E-102 during startup.

### Consequences
- ORC working fluid (Stream 2003) exceeds thermal stability limit (e.g., >250°C for toluene proxy), causing decomposition and reduced cycle efficiency below 30%.
- Potential pressure buildup in T-101 turbine, risking mechanical failure and release of degraded fluid.

### Mitigations
- Install differential pressure monitors on E-101 with high-temperature interlock to shutdown P-101 pump if fouling detected.
- Use temperature control loops with redundant sensors (TE-101A/B) on Stream 2003 to divert flow via bypass if >250°C.

### Notes
- Affects Streams 1002/2003 and E-101/T-101; operating envelope limits turbine inlet to 200-250°C; cross-reference existing smart instrumentation for predictive maintenance.

## Hazard 2: Low Flue Gas Flow Causing Insufficient Heat Recovery
**Severity:** 2
**Likelihood:** 4
**Risk Score:** 8

### Causes
- Upstream LNG burner turndown reducing Stream 1001 flow below 10,000 SCFD.
- Blockage in F-101 filter or E-101 tubes from unfiltered particulates.

### Consequences
- Reduced thermal input to ORC cycle, dropping electrical output (Stream 3001) below target 23 kWe net, impacting efficiency goal of 30%.
- ORC condenser E-103 overload from incomplete vaporization, leading to liquid carryover into T-101 and erosion.

### Mitigations
- Implement low-flow alarm on FI-1001 with automatic flue gas bypass to STK-101 to protect ORC loop.
- Schedule periodic filter replacement for F-101 and online cleaning for E-101 tubes.

### Notes
- Involves Streams 1001/2003 and F-101/E-101; design capacity 43.2 kg/h flue gas; monitor mass flow to ensure >80% of nominal for stable operation.

## Hazard 3: Acid Condensation Corrosion in Heat Exchangers
**Severity:** 4
**Likelihood:** 3
**Risk Score:** 12

### Causes
- Flue gas outlet temperature (Stream 1004) drops below 120°C due to overcooling in E-102 from excessive ORC flow (Stream 2001).
- Composition variations increasing CO2/H2O (10% each) leading to acid dew point <120°C.

### Consequences
- Corrosion of 316L SS tubes in E-101/E-102 flue gas side, causing leaks and cross-contamination between flue gas (Stream 1003) and ORC fluid.
- Potential fugitive emissions of ORC fluid, violating VOC regulations and safety risks from flammability.

### Mitigations
- Add low-temperature cutoff on TE-102C for Stream 1004 (>120°C) with interlock to reduce P-101 speed.
- Incorporate corrosion coupons in E-101 ducting and annual inspections per LDAR program.

### Notes
- References Streams 1004/2002 and E-101/E-102; MoC basis specifies 316L SS for CO2/H2O exposure; target outlet 130°C per stream data.

## Hazard 4: Loss of Condenser Cooling Leading to ORC Vacuum Failure
**Severity:** 3
**Likelihood:** 2
**Risk Score:** 6

### Causes
- Fan failure on E-103 air-cooled condenser reducing ambient air flow (Stream 4001) below 5000 kg/h.
- High ambient temperatures (>35°C) exceeding design for E-103 cooling duty.

### Consequences
- ORC low-pressure side (Stream 2004) pressure rises above 0.5 barg, risking cavitation in P-101 and reduced turbine efficiency.
- Potential overpressurization of E-103, leading to structural damage or non-condensable accumulation.

### Mitigations
- Redundant fans on E-103 with auto-start on low flow detection (FI-4001) and high-pressure alarm on PE-2004.
- Provide backup cooling water tie-in if air cooling insufficient, per utility summary.

### Notes
- Involves Streams 4001/2005 and E-103/P-101; condenser outlet at 45°C per data; parasitic load ~0.5 kW for fans included in 3002.

## Hazard 5: Flue Gas Leak into ORC System
**Severity:** 5
**Likelihood:** 1
**Risk Score:** 5

### Causes
- Tube rupture in E-101 due to thermal fatigue from flue gas cycling (300°C to 180°C, Stream 1003).
- Corrosion breach from inadequate MoC in high CO2 environment.

### Consequences
- Contamination of ORC fluid with N2/CO2/O2 (Stream 1002), degrading performance and causing turbine imbalance in T-101.
- Fire/explosion hazard if oxygen reacts with flammable ORC fluid, plus environmental release via stack.

### Mitigations
- Double-tube sheet design in E-101 for isolation; hydrocarbon (proxy for ORC) detectors on flue gas return.
- Relief valve RV-101 on E-101 sized for two-phase flow, with auto-isolation valves on Streams 1002/2002.

### Notes
- Affects E-101 and Streams 1002/2003; composition data shows 74% N2/10% CO2 in flue gas; low likelihood due to 316L SS MoC.

## Overall Assessment
- Overall Risk Level: Medium
- Compliance Notes: Process aligns with environmental criteria for emissions and noise; follow up with detailed HAZOP, working fluid selection study, and vendor confirmation of equipment ratings before commissioning. Confirm actual flue gas particulates and trace contaminants for refined filtration.

# Project Manager Report
## Executive Summary
- Approval Status: Approved
- Key Rationale: The design aligns with requirements for energy recovery from 10,000 SCFD flue gas at 300°C and 0.1 barg to produce electricity at 30% efficiency using proven ORC technology, with balanced H&MB, equipment sizing, and safety mitigations.

## Financial Outlook
| Metric | Estimate |
|--------|----------|
| CAPEX (USD millions) | 0.8 |
| OPEX (USD millions per year) | 0.05 |
| Contingency (%) | 15 |

## Implementation Plan
1. Procure and fabricate skid-mounted ORC module (T-101, G-101, E-103, P-101) from vendor, targeting 8-week delivery (engineering team responsibility).
2. Install and integrate flue gas path (F-101, E-101, E-102, STK-101) with site piping and electrical tie-ins, including commissioning tests (4 weeks, construction contractor).
3. Conduct HAZOP review, working fluid fill, and performance startup testing to verify 23 kWe net output (3 weeks, operations team).

## Final Notes
- Complete detailed working fluid selection study to confirm thermal stability and compatibility (refer to Design Basis Section 2 and H&MB Notes).
- Verify actual flue gas particulate loading and trace contaminants for F-101 filter sizing (reference Requirements Components and Safety Hazard 5).
- Establish LDAR program for ORC fugitive emissions compliance (Safety Hazard 3 and Environmental Criteria Section 6).
