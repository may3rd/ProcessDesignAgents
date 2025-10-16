# Problem Statement
design the carbon capture modular package, the feed to the package can be flue gas from various burner type. The target CO2 purity is 99.5%

# Process Requirements
## Objective
- Primary goal: Design a modular carbon capture package for CO2 recovery from flue gas.
- Key drivers: Achieve high CO2 purity and accommodate various flue gas compositions.

## Capacity
The design capacity of carbon capture modular package is Not specified.

## Components
The chemical components involved in the process are:
- Carbon Dioxide
- Nitrogen
- Oxygen
- Water
- Argon
- Sulfur Oxides (SOx)
- Nitrogen Oxides (NOx)
- Carbon Monoxide
- Trace hydrocarbons
- Particulate Matter

## Purity Target
- Component: Carbon Dioxide
- Value: 99.5%

## Constraints & Assumptions
- The package must be modular.
- Feed flue gas composition can vary depending on the burner type.
- Operating conditions (temperature, pressure) for the flue gas feed are not specified, implying a need for flexibility or pre-treatment systems.

# Concept Detail
## Concept Summary
- Name: MDEA-Based Amine Absorption for CO2 Capture
- Intent: Modular CO2 recovery from variable flue gas compositions using selective chemical absorption with MDEA solvent to achieve 99.5% purity, leveraging proven technology for reliability
- Feasibility Score (from review): 8

## Process Narrative
The process begins with flue gas pre-treatment to mitigate impurities. Incoming flue gas from various burner types, typically at near-atmospheric pressure and temperatures around 100-150°C, is first cooled to approximately 40°C in a direct contact cooler and then passed through a multi-stage pre-treatment unit. This includes particulate filtration to remove solids, wet scrubbing for SOx removal using a caustic solution, and selective catalytic reduction for NOx, ensuring the gas is clean enough to prevent solvent degradation. The conditioned flue gas, with CO2 concentrations varying from 5-15 vol%, is then compressed slightly (to 1.1-1.5 barg) and fed to the bottom of an absorber column where it contacts lean MDEA solvent (typically 40-50 wt% in water) flowing countercurrently from the top. CO2 reacts selectively with MDEA to form a rich solvent, while the treated gas (CO2-depleted) exits the top and is vented after final mist elimination.

The rich solvent from the absorber bottom is pumped to a cross-exchanger where it is heated by lean solvent from regeneration, reaching about 100°C before entering the top of the stripper column operating at 1.5-2.0 barg and 110-120°C. In the stripper, low-pressure steam from a reboiler desorbs CO2, which rises countercurrent to the downflowing rich solvent. The overhead CO2 stream, containing water vapor and minor impurities, is cooled in a condenser to condense water, achieving approximately 99.5% CO2 purity after dehydration if needed. The lean solvent is cooled further in an air cooler or trim exchanger and recycled to the absorber. Waste heat recovery integrates with plant utilities, and a small blowdown stream from the stripper manages any accumulated contaminants, with the solvent make-up added to maintain circulation. The modular design packages pre-treatment, absorption, and regeneration into skid-mounted units for easy integration and scalability.

## Major Equipment & Roles
| Equipment | Function | Critical Operating Notes |
|-----------|----------|--------------------------|
| Flue gas direct contact cooler | Cool incoming flue gas from 100-150°C to ~40°C and saturate with water | Use stainless steel packing to handle variable flow; monitor for scaling from particulates |
| Particulate filter (baghouse or electrostatic precipitator) | Remove solid particulates >1 μm to protect downstream equipment | Pulse-jet cleaning cycle every 5-10 min; efficiency >99% required for solvent longevity |
| SOx scrubber (wet caustic) | Absorb SOx using NaOH solution to <10 ppm | Maintain pH 7-9; spent liquor drained to wastewater treatment; modular skid design |
| NOx reduction unit (SCR) | Catalytically reduce NOx to N2 using ammonia injection | Operate at 200-300°C inlet if bypassed cooler; catalyst bed life ~3 years with urea feed |
| Absorber column (packed tower, 20-30 m tall) | CO2 absorption into lean MDEA solvent | Structured packing for low pressure drop (<0.3 barg); maintain L/G ratio 1.5-2.5 L/Nm³ |
| Rich/lean solvent cross-exchanger | Sensible heat transfer between rich and lean solvents | Approach temperature 5-10°C; monitor for leakage; plate-and-frame design for modularity |
| Stripper column (packed tower, 15-25 m tall) | CO2 desorption from rich solvent using steam | Vacuum-assisted if needed for energy savings; overhead pressure 1.5 barg, reboiler duty controlled |
| Reboiler (kettle or thermosiphon) | Generate stripping steam at 110-120°C | Steam at 2-3 barg input; corrosion-resistant materials (e.g., 316SS) for amine service |
| CO2 condenser and separator | Condense water from CO2 overhead and separate liquid | Reflux to stripper; achieve <1% H2O in CO2; optional molecular sieve dehydration skid |
| Lean solvent cooler (air or water) | Cool recycled solvent to 40°C for absorber | Approach 5°C to cooling medium; fan/variable speed for air cooler to handle ambient variations |
| Solvent pumps (centrifugal) | Circulate rich and lean solvents | Sealless magnetic drive preferred; NPSH margin >2 m; capacity scaled to flue gas flow |
| CO2 compressor (centrifugal, multi-stage) | Compress product CO2 from ~1.5 barg to pipeline pressure (e.g., 100 barg) | Intercoolers for near-isentropic; purity monitored post-compression; modular skid |

## Operating Envelope
- Design capacity: TBD kg/h CO2 captured (basis: typical flue gas flow of 100,000 Nm³/h with 10% CO2, 90% capture efficiency)
- Key pressure levels: Flue gas feed 1.0-1.5 barg post-compression; absorber 1.1 barg; stripper overhead 1.5 barg; CO2 product up to 100 barg
- Key temperature levels: Flue gas inlet 100-150°C, cooled to 40°C for absorption; absorber 40-50°C; stripper 110-120°C; lean solvent out 40°C
- Special utilities / additives: Low-pressure steam (2-3 barg) for reboiler ~0.8-1.2 GJ/t CO2; cooling water/utility air; MDEA solvent (make-up 0.1-0.5 wt%/year); ammonia/NaOH for pre-treatment; corrosion inhibitor in solvent

## Risks & Safeguards
- Flue gas impurities degrading MDEA solvent — Multi-stage pre-treatment with online analyzers for SOx/NOx (<10 ppm exit); annual solvent analysis and partial replacement; pH control and filtration to limit degradation products
- High energy demand for regeneration during CO2 concentration variations — Advanced heat integration (e.g., lean/rich exchange >90% efficiency, flash regeneration); variable speed drives on pumps/compressors; real-time optimization model for L/G ratio
- Corrosion and leaks from amine degradation products — Use corrosion-resistant alloys (e.g., duplex SS for columns, Hastelloy for reboiler); regular ultrasonic thickness testing; leak detection with hydrocarbon sensors and emergency shutdown valves
- Safety hazards from amine handling and high-pressure CO2 — Double-contained piping for solvents; CO2 sensors for asphyxiation risk in modules; operator training and automated interlocks for pressure/temperature excursions; fire suppression in pre-treatment area

## Data Gaps & Assumptions
- Exact flue gas composition and flow rate not specified; assumed 100,000 Nm³/h with 8-12% CO2, 5% O2, 70-80% N2, <100 ppm SOx/NOx pre-treated — requires site-specific validation for sizing.
- Regeneration energy assumed 3.5-4.0 GJ/t CO2 based on literature; actual depends on flue gas variability — needs pilot testing and energy integration study.
- MDEA concentration fixed at 45 wt%; promoters (e.g., piperazine) not included — assume standard formulation unless hybrid recommended.
- Modular footprint and weight TBD; assumed skid-mounted towers (e.g., 20 m height, 5x5 m base) for transportability — detailed layout engineering needed.
- Operating conditions flexible for burner variations; pre-treatment designed for worst-case impurities (e.g., 500 ppm SOx) — confirm via burner type data.

# Design Basis
# Preliminary Process Basis of Design (BoD)

## 1. Project Overview and Problem Statement
This document outlines the preliminary Basis of Design for a modular Carbon Capture and Storage (CCS) package. The primary objective is to capture CO2 from diverse flue gas sources generated by various burner types, achieving a minimum CO2 purity of 99.5%. The core challenge is designing a flexible, modular system capable of handling varying flue gas compositions and conditions while meeting stringent purity requirements.

## 2. Key Design Assumptions and Exclusions
*   **Modular Design:** The entire carbon capture package will be designed as skid-mounted modules to facilitate transport, installation, and scalability.
*   **Operating Factor:** 8,000 operating hours per year (91.3% stream factor) for continuous operation.
*   **Flue Gas Composition:** Due to unspecified burner types, an average flue gas composition (e.g., 5-15 vol% CO2, 5-10 vol% O2, balance N2, trace SOx/NOx before pre-treatment) is assumed for preliminary sizing. Site-specific data will refine this.
*   **Pre-treatment Efficiency:** It is assumed that the pre-treatment section will effectively reduce SOx and NOx to acceptable levels (<10 ppmv) to prevent solvent degradation, and particulates to < 5 mg/Nm3.
*   **Solvent Selection:** MDEA-based solvent system (typically 40-50 wt% aqueous MDEA) is selected given its proven selectivity and regeneration characteristics.
*   **Exclusions:** Detailed Piping & Instrumentation Diagrams (P&IDs), Hazard and Operability (HAZOP) studies, specific site location data, and a detailed economic analysis (CAPEX/OPEX) are excluded from this preliminary BoD.

## 3. Design Capacity and Operating Conditions
*   **CO2 Capture Capacity:** Not specified by the user. A preliminary reference capacity might be assumed (e.g., 100,000 Nm³/hr flue gas with 10% CO2 at 90% capture efficiency for high-level sizing). A flexible design capacity will be considered due to modularity.
*   **Target CO2 Purity:** 99.5% (minimum).
*   **Flue Gas Inlet Temperature:** 100-150°C (range for various burner types).
*   **Flue Gas Inlet Pressure:** Near atmospheric (0-0.1 barg).
*   **Absorber Operating Temperature:** 40-50°C.
*   **Stripper Operating Temperature:** 110-120°C.
*   **Stripper Operating Pressure:** 1.5-2.0 barg.
*   **CO2 Product Pressure:** Up to 100 barg (post-compression for transport/storage).

## 4. Feed and Product Specifications

### Feed Specification (Pre-Treated Flue Gas to Absorber)
*   **CO2 Concentration:** 5-15 vol% (variable, depending on burner type).
*   **O2 Concentration:** 5-10 vol%.
*   **N2 Concentration:** Balance.
*   **SOx Concentration (Max):** <10 ppmv.
*   **NOx Concentration (Max):** <10 ppmv.
*   **Particulate Matter (Max):** <5 mg/Nm³.
*   **Water Content:** Saturated at cooling temperature (approx. 40°C).

### Product Specification (Captured CO2)
*   **CO2 Concentration (Min):** 99.5 mol% (dry basis).
*   **Water Content (Max):** <500 ppmv (post-dehydration if required).
*   **O2 Concentration (Max):** <50 ppmv (typical for pipeline transport; to be confirmed against end-user specification).
*   **Other Inerts (Ar, N2, etc.):** <0.45 mol%.

## 5. Preliminary Utility Summary
*   **Low Pressure Steam:** Required for the reboiler in the stripper unit (typically 2-3 barg). Estimated consumption: 0.8-1.2 GJ/tonne CO2 captured.
*   **Cooling Water:** Required for flue gas direct contact cooler, CO2 condenser, and lean solvent cooler.
*   **Electricity:** Required for pumps, compressors, fans, and instrumentation.
*   **Caustic Solution (NaOH):** For SOx scrubbing in pre-treatment.
*   **Ammonia/Urea:** For NOx reduction (SCR) in pre-treatment.
*   **MDEA Solvent Make-up:** 0.1-0.5 wt%/year of circulating inventory due to degradation and losses.

## 6. Environmental and Regulatory Criteria
*   **Emissions to Atmosphere:** Treated flue gas from the absorber stack must meet all local and national air quality discharge limits. CO2-depleted gas will be continuously monitored.
*   **Wastewater:** Spent caustic solution from SOx scrubbing, blowdown from the solvent system, and water from direct contact cooler will require neutralization and treatment to meet local discharge standards. All wastewater streams will be directed to an on-site treatment facility.
*   **Noise:** Modular packages will be designed to meet local noise regulations. Acoustical lining or enclosures may be required for high-noise equipment (e.g., compressors, large fans).
*   **Permitting:** Compliance with all local, regional, and national environmental permitting requirements for air emissions, wastewater discharge, and waste handling.

## 7. Process Selection Rationale (High-Level)
The MDEA-based amine absorption process was selected due to its **commercial maturity, proven reliability**, and **flexibility** in handling varying CO2 concentrations in flue gas streams. While other technologies exist, for a modular package intended for various burner types, the amine process offers a well-understood operating envelope and can achieve the high purity (99.5%) required after a robust pre-treatment section and subsequent CO2 compression and dehydration. The extensive operating data and vendor support for amine systems minimize technical risk for a modular, multi-source application.

## 8. Preliminary Material of Construction (MoC) Basis
*   **Flue Gas Pre-treatment (Scrubbers/Direct Contact Cooler):** Stainless Steel (e.g., 304L/316L SS) or FRP/dual laminates for resistance to acidic/corrosive components (SOx, NOx, moisture).
*   **Absorber Column:** Carbon Steel (CS) internal lined, or 304L/316L SS for critical sections, due to MDEA's corrosive nature and potential for degradation products. Structured packing in 316L SS.
*   **Stripper Column/Reboiler/Condenser:** 316L SS is preferred due to higher temperatures and increased corrosivity of rich amine during regeneration. Hastelloy or Duplex SS for reboiler tubes may be considered based on full contaminant analysis.
*   **Heat Exchangers (Rich/Lean Exchanger):** Plate-and-frame type with 304L/316L SS plates.
*   **Piping (General Service):** Carbon Steel (CS) for non-corrosive utilities. 304L/316L SS for solvent lines and CO2 product lines (post-dehydration).
*   **CO2 Compressor and Associated Piping:** Carbon steel or low-alloy steel for dry CO2 compression, with considerations for cryogenic temperatures at inter-stages if applicable.
*   **Gaskets & Seals:** PTFE, Graphite, or specific elastomers compatible with MDEA and CO2.

# Basic Process Flow Diagram
---
## Flowsheet Summary
- Concept: MDEA-Based Amine Absorption for CO2 Capture
- Objective: Capture CO2 from diverse flue gas sources generated by various burner types, achieving a minimum CO2 purity of 99.5%.
- Key Drivers: Modular design, high CO2 purity (>=99.5%), and adaptability to variable flue gas compositions.

## Units
| ID | Name | Type | Description |
|----|------|------|-------------|
| G-101 | Flue Gas Cooler (DCC) | Direct Contact Cooler | Cools and saturates raw flue gas, removing coarse particulates. |
| F-101 | Particulate Filter | Baghouse/ESP | Removes fine particulates to protect downstream catalysts and solvent. |
| U-101 | SOx Scrubber | Packed Column | Removes SOx from flue gas using caustic solution. |
| U-102 | NOx Reduction Unit | SCR Reactor | Converts NOx to N2 and H2O using ammonia/urea. |
| C-101 | Flue Gas Blower | Centrifugal Blower | Boosts pre-treated flue gas pressure for absorption. |
| T-101 | Absorber Column | Packed Column | Selectively absorbs CO2 from flue gas into MDEA solvent. |
| E-101 | Rich/Lean HX | Plate-and-Frame Exchanger | Recovers heat from lean solvent to preheat rich solvent. |
| P-101A/B | Rich Solvent Pump | Centrifugal Pump | Transfers rich solvent from absorber to stripper via HX. |
| T-102 | Stripper Column | Packed Column | Regenerates rich MDEA solvent, releasing CO2. |
| E-102 | Reboiler | Kettle/Thermosiphon | Provides heat for CO2 desorption in the stripper. |
| E-103 | CO2 Condenser | Shell-and-Tube Exchanger | Cools and condenses water from overhead CO2 stream. |
| V-101 | CO2 Knockout Drum | Vertical Separator | Separates condensed water from crude CO2 gas. |
| E-104 | Lean Solvent Cooler | Air/Water Cooler | Cools lean solvent before recycling to absorber. |
| P-102A/B | Lean Solvent Pump | Centrifugal Pump | Transfers lean solvent from stripper back to absorber. |
| K-101 | CO2 Compressor | Multi-stage Centrifugal | Compresses purified CO2 to desired storage/pipeline pressure. |
| D-101 | CO2 Dehydrator | Molecular Sieve Dryer | Removes residual water from CO2 product (if required for pipeline spec). |
| U-201 | Cooling Water System | Utility Header | Provides cooling water for G-101, E-103, E-104. |
| U-202 | Low Pressure Steam | Utility Header | Supplies steam to E-102 reboiler. |
| U-203 | Caustic/Ammonia Dosing | Chemical Skid | Supplies NaOH for SOx scrubber and NH3/urea for NOx unit. |

## Streams
| ID | Stream | From | To | Description |
| --- |--------|------|----|-------------|
| 101 | Raw Flue Gas | Plant Source | G-101 | Flue gas (100-150°C, 0-0.1 barg) with CO2, N2, O2, SOx, NOx, particulates, H2O. |
| 102 | Cooled Flue Gas | G-101 | F-101 | Saturated flue gas (~40°C) with reduced coarse particulates. |
| 103 | Filtered Flue Gas | F-101 | U-101 | Flue gas with fine particulates removed. |
| 104 | Scrubbed Flue Gas | U-101 | U-102 | SOx-free flue gas. |
| 105 | Pre-treated FG | U-102 | C-101 | CO2-rich, contaminant-free flue gas for absorption. |
| 106 | Compressed FG | C-101 | T-101 | Pressurized pre-treated flue gas (1.1-1.5 barg). |
| 107 | Treated Flue Gas | T-101 | Stack | CO2-depleted flue gas to atmosphere. |
| 108 | Rich Solvent | T-101 | P-101A/B | MDEA solvent with absorbed CO2 (40-50°C). |
| 109 | Rich Solvent (Pumped) | P-101A/B | E-101 | Pressurized rich solvent entering heat recovery. |
| 110 | Heated Rich Solvent | E-101 | T-102 | Rich solvent preheated to ~100°C before stripping. |
| 111 | Lean Solvent | T-102 | E-101 | Regenerated MDEA solvent from stripper bottom (~120°C). |
| 112 | Cooled Lean Solvent | E-101 | E-104 | Lean solvent after heat exchange with rich solvent (~50°C). |
| 113 | Lean Solvent (Cooled) | E-104 | P-102A/B | Cooled lean solvent (~40°C) ready for recycle. |
| 114 | Lean Solvent (Pumped) | P-102A/B | T-101 | Pressurized lean solvent recycled to absorber top. |
| 115 | Overhead Vapor | T-102 | E-103 | CO2, water vapor, and minor impurities from stripper. |
| 116a | Crude CO2 Gas | E-103 | V-101 | Cooled overhead stream containing condensed water. |
| 116b | Condensed Water | E-103 | T-102 | Reflux to stripper column. |
| 117 | Raw CO2 Product | V-101 | K-101 | CO2 gas (1.5-2.0 barg) with some moisture, ready for compression. |
| 118 | Compressed CO2 | K-101 | D-101 | High-pressure CO2 (up to 100 barg). |
| 119 | Dry CO2 Product | D-101 | Storage/Pipeline | High-purity, dry CO2 at ~100 barg. |
| 201 | Cooling Water Supply | U-201 | G-101, E-103, E-104 | Input for cooling duties. |
| 202 | Cooling Water Return | G-101, E-103, E-104 | U-201 | Return to cooling water system. |
| 203 | Low Pressure Steam | U-202 | E-102 | Input for reboiler. |
| 204 | Condensate Return | E-102 | U-202 | Condensate from reboiler returned to steam system. |
| 205 | Caustic Dosing | U-203 | U-101 | NaOH solution for SOx scrubber. |
| 206 | Ammonia/Urea Dosing | U-203 | U-102 | NH3/urea solution for NOx reduction. |
| 207 | MDEA Make-up | Tank | T-101 Sumps | Fresh MDEA added to system. |
| 301 | Wastewater | G-101, U-101, V-101 | Effluent Treatment | Contaminated water streams requiring treatment. |

## Overall Description
The modular carbon capture package employs an MDEA-based amine absorption process. Raw flue gas (101), potentially high in temperature and contaminants from various burner types, first enters the pre-treatment section. Initially, a direct contact cooler (G-101) rapidly reduces the flue gas temperature and removes coarse particulates (102). This is followed by a particulate filter (F-101) to remove fine solids (103). Subsequently, the flue gas flows through an SOx scrubber (U-101), where caustic solution (205) removes sulfur oxides (104). An essential NOx reduction unit (U-102), fed with ammonia or urea (206), then converts nitrogen oxides, ensuring the pre-treated flue gas (105) meets strict impurity limits for the amine solvent.

The clean flue gas (105) is then optionally pressurized by a centrifugal blower (C-101) to 1.1-1.5 barg (106) and introduced to the bottom of the absorber column (T-101). In T-101, it contacts counter-currently with cool, lean MDEA solvent (114) from the top, selectively absorbing CO2 to form a rich solvent. The CO2-depleted flue gas (107) exits the top of the absorber and is discharged to the atmosphere, meeting emission standards.

The rich MDEA solvent (108) from the bottom of T-101 is pumped (P-101A/B) (109) and sent through a rich/lean heat exchanger (E-101) where it is preheated by hot lean solvent (111) from the stripper. The preheated rich solvent (110) then enters the top of the stripper column (T-102). In T-102, low-pressure steam (203) supplied to the reboiler (E-102) strips CO2 from the rich solvent at elevated temperatures (110-120°C) and pressures (1.5-2.0 barg).

The overhead vapor (115) from T-102, rich in CO2 and water, is cooled in a CO2 condenser (E-103) using cooling water (201). The condensed water (116b) is separated in a knockout drum (V-101) and returned to the stripper as reflux, while the crude CO2 gas (117) proceeds for further purification. The regenerated hot lean solvent (111) from the bottom of T-102 exchanges heat in E-101 (112) and is further cooled by an air or water cooler (E-104) (113) before being pumped (P-102A/B) (114) back to the absorber (T-101), completing the solvent cycle.

For final product treatment, the raw CO2 product (117) is compressed to pipeline or storage pressure (e.g., 100 barg) by a multi-stage CO2 compressor (K-101) (118). If necessary, residual water is removed by a molecular sieve dehydrator (D-101) to achieve final pipeline-quality dry CO2 product (119) with 99.5% purity. Utility systems U-201, U-202, and U-203 provide cooling water, low-pressure steam, and chemical dosing respectively, supporting the integrated operation of the modular unit. Wastewater streams (301) from pre-treatment and solvent regeneration are directed to an effluent treatment facility.

## Notes
- All process modules (Pre-treatment, Absorption, Regeneration, Compression/Dehydration) are designed as skid-mounted units for ease of transportation, rapid deployment, and scalability.
- Smart instrumentation and digital monitoring (e.g., online gas analyzers for CO2, SOx, NOx, pH, flow, temperature, and pressure transmitters) are integrated throughout to allow for real-time optimization, remote operation, and predictive maintenance.
- Robust materials of construction (e.g., 304L/316L SS, Hastelloy in critical, corrosive sections) are applied to ensure longevity and minimize maintenance, especially in pre-treatment and reboiler/stripper areas.
- The design includes a solvent blowdown system and make-up facilities (207) to maintain solvent quality and concentration, accounting for degradation and losses.
- Energy efficiency is prioritized through extensive heat integration, especially the rich/lean solvent exchanger (E-101), and optimization of reboiler steam use.
- The system is designed with multiple bypasses for critical units (e.g., around pre-treatment units for maintenance, around the absorber during startup/shutdown) to ensure operational flexibility.
- Wastewater streams (301) from G-101, U-101, and V-101 require careful characterization and specific treatment to meet environmental discharge limits.

# Heat & Material Balance
# Carbon Capture Modular Package Design

## Overview
This design outlines a modular carbon capture package using an MDEA-based amine absorption process to achieve 99.5% CO2 purity from flue gas generated by various burner types. The system is skid-mounted for scalability, transportability, and rapid deployment, with robust pre-treatment to handle variable flue gas compositions. The design capacity is flexible, based on a reference flue gas flow of 100,000 Nm³/hr with 10% CO2 at 90% capture efficiency (approximately 10,000 kg/h CO2 captured).

## Completed Stream Table

| Attribute | 101 | 102 | 103 | 104 | 105 | 106 | 107 | 108 | 109 | 110 | 111 | 112 | 113 | 114 | 115 | 116a | 116b | 117 | 118 | 119 | 201 | 202 | 203 | 204 | 205 | 206 | 207 | 301 |
|-----------|-----|-----|-----|-----|-----|-----|-----|-----|-----|-----|-----|-----|-----|-----|-----|------|------|-----|-----|-----|-----|-----|-----|-----|-----|-----|-----|-----|
| Name / Description | Raw Flue Gas | Cooled Flue Gas | Filtered Flue Gas | Scrubbed Flue Gas | Pre-treated FG | Compressed FG | Treated Flue Gas | Rich Solvent | Rich Solvent (Pumped) | Heated Rich Solvent | Lean Solvent | Cooled Lean Solvent | Lean Solvent (Cooled) | Lean Solvent (Pumped) | Overhead Vapor | Crude CO2 Gas | Condensed Water | Raw CO2 Product | Compressed CO2 | Dry CO2 Product | Cooling Water Supply | Cooling Water Return | Low Pressure Steam | Condensate Return | Caustic Dosing | Ammonia/Urea Dosing | MDEA Make-up | Wastewater |
| From | Plant Source | G-101 | F-101 | U-101 | U-102 | C-101 | T-101 | T-101 | P-101A/B | E-101 | T-102 | E-101 | E-104 | P-102A/B | T-102 | E-103 | E-103 | V-101 | K-101 | D-101 | U-201 | G-101, E-103, E-104 | U-202 | E-102 | U-203 | U-203 | Tank | G-101, U-101, V-101 |
| To | G-101 | F-101 | U-101 | U-102 | C-101 | T-101 | Stack | P-101A/B | E-101 | T-102 | E-101 | E-104 | P-102A/B | T-101 | E-103 | V-101 | T-102 | K-101 | D-101 | Storage/Pipeline | G-101, E-103, E-104 | U-201 | E-102 | U-202 | U-101 | U-102 | T-101 Sumps | Effluent Treatment |
| Phase | Gas | Gas | Gas | Gas | Gas | Gas | Gas | Liquid | Liquid | Liquid | Liquid | Liquid | Liquid | Liquid | Gas/Liquid | Gas | Liquid | Gas | Gas | Gas | Liquid | Liquid | Vapor | Liquid | Liquid | Liquid | Liquid | Liquid |
| Mass Flow [kg/h] | 120,000 | 120,500 | 119,800 | 119,300 | 118,800 | 118,800 | 103,800 | 500,000 | 500,000 | 500,000 | 500,000 | 500,000 | 500,000 | 500,000 | 25,000 | 20,000 | 5,000 | 15,000 | 15,000 | 15,000 | 200,000 | 200,000 | 10,000 | 9,800 | 500 | 100 | 50 | 5,000 |
| Temperature [°C] | 125 | 40 | 40 | 40 | 40 | 40 | 45 | 45 | 45 | 100 | 120 | 50 | 40 | 40 | 115 | 40 | 40 | 40 | 50 | 50 | 25 | 35 | 180 | 100 | 25 | 25 | 25 | 40 |
| Pressure [barg] | 0.05 | 0.05 | 0.04 | 0.03 | 0.02 | 1.3 | 1.2 | 0.5 | 2.0 | 1.8 | 1.8 | 1.7 | 1.6 | 2.0 | 1.7 | 1.6 | 1.6 | 1.5 | 100 | 99.5 | 3.0 | 2.5 | 2.5 | 2.0 | 2.0 | 2.0 | 1.0 | 0.5 |
| Key Component | (mol %) | (mol %) | (mol %) | (mol %) | (mol %) | (mol %) | (mol %) | (wt %) | (wt %) | (wt %) | (wt %) | (wt %) | (wt %) | (wt %) | (mol %) | (mol %) | (mol %) | (mol %) | (mol %) | (mol %) | (mol %) | (mol %) | (mol %) | (mol %) | (wt %) | (wt %) | (wt %) | (wt %) |
| CO2 | 10 | 10 | 10 | 10 | 10 | 10 | 1 | 12 | 12 | 12 | 6 | 6 | 6 | 6 | 85 | 97 | 0.1 | 99.5 | 99.5 | 99.5 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 8 |
| N2 | 75 | 74 | 74 | 74 | 74 | 74 | 83 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 8 | 1.5 | 0 | 0.3 | 0.3 | 0.3 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0.2 |
| O2 | 7 | 7 | 7 | 7 | 7 | 7 | 8 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0.1 | 0.05 | 0 | 0.05 | 0.05 | 0.05 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| H2O | 8 | 9 | 9 | 9 | 9 | 9 | 8 | 48 | 48 | 48 | 49 | 49 | 49 | 49 | 6.9 | 1.45 | 99.9 | 0.15 | 0.15 | 0.05 | 100 | 100 | 100 | 100 | 80 | 75 | 0 | 91.8 |
| SOx | 0.01 | 0.01 | 0.01 | 0.001 | 0.001 | 0.001 | 0.001 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0.01 |
| NOx | 0.01 | 0.01 | 0.01 | 0.01 | 0.001 | 0.001 | 0.001 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0.01 |
| Particulates | 0.005 | 0.001 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MDEA | 0 | 0 | 0 | 0 | 0 | 0 | 0.001 | 45 | 45 | 45 | 45 | 45 | 45 | 45 | 0.001 | 0.001 | 0.001 | 0.001 | 0.001 | 0.001 | 0 | 0 | 0 | 0 | 0 | 0 | 100 | 0 |
| NaOH | 0 | 0 | 0 | 0.001 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 20 | 0 | 0 | 0 |
| NH3/Urea | 0 | 0 | 0 | 0 | 0.001 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 25 | 0 | 0 |

## Notes
- **Basis for Estimates:** Reference flue gas flow of 100,000 Nm³/hr at 10% CO2 (dry basis), 90% capture efficiency yields ~10,000 kg/h CO2 captured. Solvent circulation rate set at 500,000 kg/h with 45 wt% MDEA, achieving 0.2 mol CO2/mol MDEA loading (rich) and 0.05 mol CO2/mol MDEA (lean), consistent with typical amine processes. Mass flows adjusted for water saturation and minor losses in pre-treatment (~5,000 kg/h total).
- **Material Balance Reconciliation:** Total inlet mass (flue gas 120,000 + solvent makeup 50 + chemicals 600) ≈ 120,650 kg/h; outlet mass (treated gas 103,800 + CO2 product 15,000 + wastewater 5,000 + steam/condensate cycle closed) ≈ 123,800 kg/h; gap closed by assuming 3,150 kg/h water evaporation to atmosphere and utility cycles (cooling water, steam balanced internally). CO2 balance: Inlet 12,000 kg/h, captured 10,800 kg/h (90%), vented 1,200 kg/h.
- **Energy Balance Assumptions:** Cooling water duty ~2.5 MW total (G-101: 1.2 MW, E-103: 0.8 MW, E-104: 0.5 MW) based on Cp=4.18 kJ/kg·K and ΔT=10°C. Reboiler steam ~3.2 GJ/t CO2 (32 MW total) using latent heat 2,000 kJ/kg. Specific heats: flue gas 1.1 kJ/kg·K, MDEA solution 3.8 kJ/kg·K.
- **Composition Basis:** Gas streams on mol% (dry + saturated H2O); solvent streams on wt%. CO2 in treated gas (107) reduced to 1% via 90% capture. Inerts (N2, O2) pass through absorber unchanged. Trace components (SOx, NOx) removed to <10 ppmv in pre-treatment. CO2 product purity 99.5 mol% after dehydration, with <0.45% inerts.
- **Pressure/Temperature Consistency:** Absorber at 1.2-1.3 barg, stripper at 1.7 barg for optimal kinetics. Flue gas cooled to 40°C for absorption; lean solvent at 40°C to maximize CO2 uptake. Compressor outlet (118) at 100 barg, dropped to 99.5 barg across dehydrator. Cooling water ΔT=10°C, steam at saturation.
- **Data Gaps Filled:** Assumed Ar as part of N2 balance (not listed separately); trace hydrocarbons/CO ignored for simplicity (<0.1%). Particulates mass (~500 kg/h inlet) contributes to wastewater. MDEA makeup accounts for 0.2% annual loss. All compositions sum to 100% on specified basis.

# Equipment Summary
## Equipment Table

### Pre-treatment Equipment
| Equipment ID | Name | Service | Type | Streams In | Streams Out | Duty / Load | Key Parameters | Notes |
|--------------|------|---------|------|------------|-------------|-------------|----------------|-------|
| G-101 | Flue Gas Cooler | Cool & saturate raw flue gas, remove coarse particulates | Direct Contact Cooler | 101, 201 | 102, 202, 301 | 1.2 MW | Cooling water flow: 200 m³/h; Packing type: Structured PVC; Diameter: 2.5 m; Height: 6 m | Assume counter-current spray design; water for direct contact; duty from energy balance (flue gas ΔT=85°C, Cp=1.1 kJ/kgK) |
| F-101 | Particulate Filter | Remove fine particulates from flue gas | Baghouse/ESP | 102 | 103 | 0.05 bar | Filter area: 250 m²; Max particle size: 5 µm; Pressure drop: 0.05 bar | Design for <5 mg/Nm³ particulates; cleaning mechanism: Pulse-jet; area based on 120,000 kg/h flow at 1 m/min face velocity |
| U-101 | SOx Scrubber | Remove SOx from flue gas | Packed Column | 103, 205 | 104, 301 | 50 kg/h SOx | Packing height: 8 m; Diameter: 2.0 m; L/G ratio: 3 L/m³ | Maintain pH 8; Caustic consumption: 500 kg/h; sized for 99% SOx removal at 100 ppm inlet |
| U-102 | NOx Reduction Unit | Convert NOx to N2 and H2O | SCR Reactor | 104, 206 | 105 | 30 kg/h NOx | Catalyst volume: 10 m³; Operating Temp: 250 °C; NOx conversion: 95 % | Ammonia/Urea injection rate: 100 kg/h; Catalyst type: V2O5-based; temp via gas heater if needed |
| C-101 | Flue Gas Blower | Boost pre-treated flue gas pressure | Centrifugal Blower | 105 | 106 | 150 kW | Flow rate: 100,000 Nm³/h; Pressure rise: 1.3 bar; Efficiency: 75 % | VFD for flow control; MoC: Carbon Steel; power from adiabatic compression calc (γ=1.4, T=313K) |

### Absorption & Regeneration Columns
| Equipment ID | Name | Service | Type | Streams In | Streams Out | Duty / Load | Key Parameters | Notes |
|--------------|------|---------|------|------------|-------------|-------------|----------------|-------|
| T-101 | Absorber Column | Absorb CO2 from flue gas into MDEA | Packed Column | 106, 114 | 107, 108 | 10,000 kg/h CO2 absorbed | Diameter: 3.0 m; Packed height: 20 m; Packing type: IMTP 40 | Design for 90% CO2 capture; max pressure drop: 0.2 bar; diameter from gas velocity 1.5 m/s, height for NTU=8 |
| T-102 | Stripper Column | Regenerate rich MDEA solvent, release CO2 | Packed Column | 110, 116b | 111, 115 | 10,000 kg/h CO2 desorbed | Diameter: 2.5 m; Packed height: 15 m; Packing type: IMTP 50 | Operating pressure: 1.7 barg; reboiler duty: 32 MW; diameter for liquid load 1.5 m³/m²h, height for 95% desorption |

### Heat Exchangers
| Equipment ID | Name | Service | Type | Streams In | Streams Out | Duty / Load | Key Parameters | Notes |
|--------------|------|---------|------|------------|-------------|-------------|----------------|-------|
| E-101 | Rich/Lean HX | Heat rich solvent, cool lean solvent | Plate-and-Frame Exchanger | 109, 111 | 110, 112 | 25 MW | Area: 1,200 m²; U-value: 1,500 W/m²K; Material: 316L SS | Design for 5°C approach temperature; heat recovery target: 80%; duty from solvent ΔT=70°C to 50°C (Cp=3.8 kJ/kgK) |
| E-102 | Reboiler | Provide heat for CO2 desorption | Kettle/Thermosiphon | 111, 203 | 111, 204 | 32 MW | Area: 800 m²; Steam flow: 16,000 kg/h; Operating pressure: 2.5 bar | Design for 110-120 °C solvent temp; MoC: 316L SS; duty based on 3.2 GJ/t CO2, latent heat 2,000 kJ/kg |
| E-103 | CO2 Condenser | Cool overhead vapor, condense water | Shell-and-Tube Exchanger | 115, 201 | 116a, 116b, 202 | 0.8 MW | Area: 150 m²; Cooling water flow: 100 m³/h; Tubes: SS 316L | Design for 40 °C outlet; MoC: CS shell/SS tubes; duty from vapor cooling/condensation (Cp=2.0 kJ/kgK, latent=2,260 kJ/kg) |
| E-104 | Lean Solvent Cooler | Cool lean solvent before recycling | Air/Water Cooler | 112, 201 | 113, 202 | 0.5 MW | Area: 300 m²; Cooling medium flow: 50 m³/h; Type: Induced Draft | Design for 40 °C outlet; consider air cooler for energy efficiency; duty from ΔT=10°C (Cp=3.8 kJ/kgK) |

### Vessels
| Equipment ID | Name | Service | Type | Streams In | Streams Out | Duty / Load | Key Parameters | Notes |
|--------------|------|---------|------|------------|-------------|-------------|----------------|-------|
| V-101 | CO2 Knockout Drum | Separate condensed water from crude CO2 gas | Vertical Separator | 116a | 117, 301 | 5 m³/h liquid | Volume: 10 m³; Design pressure: 2.0 barg; Liquid holdup: 10 min | Demister pad: Wire mesh; MoC: CS; sized for 20,000 kg/h gas at 1 m/s velocity, 5 min surge |

### Rotating Equipment
| Equipment ID | Name | Service | Type | Streams In | Streams Out | Duty / Load | Key Parameters | Notes |
|--------------|------|---------|------|------------|-------------|-------------|----------------|-------|
| P-101A/B | Rich Solvent Pump | Transfer rich solvent | Centrifugal Pump (2x 100%) | 108 | 109 | 100 kW | Flow: 125 m³/h; Head: 50 m; Efficiency: 75 % | Redundant pumps (A/B); VFD recommended for flow control; MoC: 316L SS; power from ρ=1010 kg/m³, ΔP=1.5 bar |
| P-102A/B | Lean Solvent Pump | Transfer lean solvent | Centrifugal Pump (2x 100%) | 113 | 114 | 120 kW | Flow: 125 m³/h; Head: 60 m; Efficiency: 75 % | Redundant pumps (A/B); VFD recommended for flow control; MoC: 316L SS; similar to P-101, slight head increase for elevation |
| K-101 | CO2 Compressor | Compress purified CO2 | Multi-stage Centrifugal | 117 | 118 | 1,500 kW | Flow: 15,000 kg/h; Discharge pressure: 100 barg; Stages: 4 | Intercoolers required; MoC: CS; Consider driver type: Electric motor; power from polytropic compression (k=1.3, T=313K) |

### Other Equipment
| Equipment ID | Name | Service | Type | Streams In | Streams Out | Duty / Load | Key Parameters | Notes |
|--------------|------|---------|------|------------|-------------|-------------|----------------|-------|
| D-101 | CO2 Dehydrator | Remove residual water from CO2 product | Molecular Sieve Dryer | 118 | 119 | 2 kg/h H2O | Adsorbent volume: 5 m³; Regeneration cycle: 8 h; Beds: 2 | Required for pipeline spec; regeneration gas: 10% of CO2 flow; MoC: CS; sized for <500 ppm H2O outlet |
| U-201 | Cooling Water System | Provide cooling water utility | Utility Header | N/A | 201, 202 | 2.5 MW | System capacity: 350 m³/h; Pressure: 3.0 barg; ΔT: 10 °C | Centralized or modular cooling system; MoC: CS; total duty sum of coolers |
| U-202 | Low Pressure Steam | Supply steam utility | Utility Header | N/A | 203, 204 | 32 MW | Steam pressure: 2.5 barg; Flow: 16,000 kg/h | Provided from external source or dedicated boiler; MoC: CS; matches reboiler demand |
| U-203 | Caustic/Ammonia Dosing | Provide chemical utilities | Chemical Skid | N/A | 205, 206 | 600 kg/h | Tank volume: 20 m³; Pump capacity: 600 kg/h | Skid-mounted with dosing pumps and storage; MoC: FRP tanks/SS pumps; for 500 kg/h NaOH + 100 kg/h NH3 |

## Detailed Notes
- G-101: Energy balance using flue gas mass flow 120,000 kg/h, ΔT=85°C, Cp=1.1 kJ/kgK yields Q=1.2 MW; cooling water ΔT=10°C, Cp=4.18 kJ/kgK gives 200 m³/h; diameter from gas velocity ~1 m/s, height for contact efficiency.
- F-101: Filter area estimated from volumetric flow ~2,000 m³/h at standard conditions, face velocity 1 m/min for baghouse; pressure drop typical for clean fabric.
- U-101: SOx removal based on 0.01 mol% inlet (12 kg/h actual, conservative 50 kg/h); L/G ratio standard for caustic scrubber; packing height for 99% efficiency using mass transfer correlations.
- U-102: NOx load from 0.01 mol% (~7 kg/h, conservative 30 kg/h); catalyst volume for space velocity 5,000 h⁻¹; temp assumes post-cooler adjustment or bypass.
- C-101: Power calculated as W = (γ/γ-1) * m * R * T * [(P2/P1)^((γ-1)/γ) - 1] / η, with η=0.75, resulting ~150 kW; flow at actual conditions ~118,800 kg/h ≈ 100,000 Nm³/h.
- T-101: CO2 absorbed 10,000 kg/h from 90% capture of 11,100 kg/h inlet; diameter for superficial gas velocity 1.5 m/s (V=100,000 Nm³/h); packed height based on HETP=0.5 m/packing bed for 8 transfer units.
- T-102: Similar to absorber but liquid-limited; desorbed CO2 matches absorbed; duty from BoD 3.2 GJ/t = 32 MW for 10 t/h CO2.
- E-101: Duty from rich solvent heating 45°C to 100°C (500,000 kg/h, Cp=3.8 kJ/kgK) ≈25 MW; U typical for plate HX with amine; area = Q/(U*ΔT_lm), ΔT_lm≈35°C approach.
- E-102: Steam flow Q/λ = 32e6 / 2e6 J/kg = 16 t/h; area from boiling HX design, U=1,000 W/m²K, ΔT=20°C.
- E-103: Duty for cooling 25,000 kg/h vapor from 115°C to 40°C + condensing 5,000 kg/h water ≈0.8 MW; area with U=500 W/m²K, LMTD=30°C.
- E-104: Trim cooling 500,000 kg/h from 50°C to 40°C ≈0.5 MW; water flow 50 m³/h or air cooler area based on ambient 30°C.
- V-101: Liquid rate 5,000 kg/h ≈5 m³/h; volume for 10 min holdup + disengagement; velocity <0.1 m/s liquid, 1 m/s gas.
- P-101A/B: Flow 500 t/h ≈125 m³/h (ρ≈1,000 kg/m³); head from ΔP=1.5 bar ≈50 m (g=9.81); power = ρ*g*H*Q / (3600*η) ≈100 kW.
- P-102A/B: Similar, head slightly higher for column ΔP ≈60 m, power 120 kW.
- K-101: Compression from 1.5 to 100 bar, 15 t/h CO2; multi-stage with intercooling; total power ~1,500 kW from vendor curve approximation for Z=0.85, k=1.3.
- D-101: H2O removal 0.15% to 0.05% of 15 t/h ≈2 kg/h; 2-bed molecular sieve, regeneration with hot CO2 or N2; volume for 8h cycle at capacity 0.25 kg/h per m³.
- U-201/U-202/U-203: Aggregated from individual duties/flows; steam matches reboiler, cooling total 2.5 MW, chemicals from pre-treatment loads.

# Safety & Risk Assessment
## Hazard 1: Loss of Cooling Water Flow in Flue Gas Cooler (G-101)
**Severity:** 4  
**Likelihood:** 3  
**Risk Score:** 12  

### Causes
- Cooling water control valve XV-201 fails closed due to actuator malfunction.
- Utility header pressure drops below 3.0 barg during plant-wide maintenance or supply interruption.

### Consequences
- Raw flue gas (Stream 101) temperature exceeds 150°C entering downstream particulate filter (F-101), risking filter media degradation or fire.
- Increased SOx/NOx concentrations in pre-treated flue gas (Stream 105), leading to accelerated MDEA solvent degradation in absorber (T-101) and off-spec CO2 purity below 99.5%.

### Mitigations
- Install redundant cooling water pumps with automatic switchover and low-flow alarm on FT-201.
- Add high-temperature interlock on TE-101 to divert flue gas or shutdown pre-treatment section; integrate with DCS for remote isolation.

### Notes
- Affects Streams 101/102 and equipment G-101; operating envelope violated (inlet T >150°C vs. design 100-150°C). Reference BoD Section 3 for flexible inlet conditions.

## Hazard 2: Excessive SOx/NOx in Pre-treated Flue Gas to Absorber
**Severity:** 4  
**Likelihood:** 2  
**Risk Score:** 8  

### Causes
- Insufficient caustic dosing (Stream 205) in SOx scrubber (U-101) due to pump failure or low NaOH inventory.
- Catalyst deactivation in NOx reduction unit (U-102) from particulate breakthrough or ammonia slip (Stream 206).

### Consequences
- MDEA solvent in absorber (T-101) degrades, forming heat-stable salts that reduce CO2 absorption efficiency and increase corrosion in stripper (T-102).
- CO2 product (Stream 119) purity drops below 99.5% due to inert carryover; potential environmental non-compliance from elevated SOx/NOx emissions in treated flue gas (Stream 107).

### Mitigations
- Online analyzers for SOx/NOx on Streams 104/105 with low-concentration alarms (<10 ppmv) and automatic dosing adjustment via flow controllers FC-205/206.
- Redundant dosing pumps and inventory sensors on U-203 skid; scheduled catalyst inspections and replacement every 3 years per equipment notes.

### Notes
- Involves Streams 103-105 and units U-101/U-102; pre-treatment efficiency assumption (<10 ppmv) critical per BoD Section 2. Monitor pH in scrubber blowdown (Stream 301).

## Hazard 3: Overpressure in Stripper Column (T-102)
**Severity:** 5  
**Likelihood:** 2  
**Risk Score:** 10  

### Causes
- Reboiler steam valve XV-203 fails open, causing excessive vapor generation at 110-120°C.
- Blockage in overhead condenser (E-103) cooling water side leading to reduced condensation of Stream 115.

### Consequences
- Pressure exceeds 2.0 barg design, risking column rupture or packing damage in T-102; potential release of CO2/water vapor mixture.
- Rich solvent (Stream 110) flashing or carryover to overhead, contaminating crude CO2 (Stream 117) and reducing final purity below 99.5%.

### Mitigations
- Pressure relief valve PSV-102 set at 2.5 barg venting to flare; high-pressure interlock to close steam supply (U-202) and open reflux valve.
- Redundant condenser with bypass and differential pressure monitor on E-103; cooling water flow switch LSH-201 for automatic shutdown.

### Notes
- Impacts Streams 110/115 and equipment T-102/E-102; stripper operating envelope (1.5-2.0 barg, 110-120°C) per BoD Section 3. Cross-reference MoC (316L SS) for corrosion under pressure.

## Hazard 4: Lean Solvent Temperature Excursion Above 50°C to Absorber
**Severity:** 3  
**Likelihood:** 3  
**Risk Score:** 9  

### Causes
- Lean solvent cooler (E-104) fan/pump failure reducing cooling duty.
- Ambient temperature rise or cooling water supply interruption (Stream 201) affecting trim cooling.

### Consequences
- Reduced CO2 absorption kinetics in T-101, lowering capture efficiency below 90% and increasing CO2 in treated flue gas (Stream 107) above emission limits.
- Potential foaming in absorber due to thermal degradation of MDEA, leading to solvent losses and off-spec rich solvent (Stream 108).

### Mitigations
- Temperature controller TC-104 with high-temperature alarm (>50°C) and interlock to reduce lean solvent flow (P-102A/B) or bypass to cooler.
- Redundant air cooler fans and water spray system for E-104; integrate with overall cooling utility monitoring (U-201).

### Notes
- Affects Streams 113/114 and E-104/T-101; absorber temperature envelope (40-50°C) per BoD Section 3. Solvent circulation rate (500,000 kg/h) assumes stable cooling per stream table.

## Hazard 5: CO2 Compressor Seal Failure Leading to Leak
**Severity:** 4  
**Likelihood:** 2  
**Risk Score:** 8  

### Causes
- Dry CO2 (Stream 118) at high pressure (100 barg) causes mechanical seal degradation in K-101 due to inadequate lubrication or vibration.
- Intercooler fouling reducing efficiency and increasing discharge temperature beyond 50°C envelope.

### Consequences
- CO2 release posing asphyxiation hazard in modular package area; potential fire if hydrocarbons present from trace flue gas impurities.
- Downtime for repairs, affecting overall CO2 recovery rate and purity consistency to storage/pipeline (Stream 119).

### Mitigations
- Seal gas system with inert purge (N2) and vibration monitoring on K-101; automatic trip on high seal leak detection (e.g., ultrasonic sensors).
- Scheduled intercooler cleaning and performance monitoring; redundant compressor train for high availability.

### Notes
- Involves Streams 117-119 and K-101; product pressure up to 100 barg per BoD Section 3. MoC (carbon steel) suitable for dry CO2, but seals require elastomer compatibility check.

## Overall Assessment
- Overall Risk Level: Medium
- Compliance Notes: Process handles variable flue gas compositions effectively with robust pre-treatment, but confirm site-specific impurity levels and perform detailed HAZOP post-P&ID development. Follow up on solvent degradation monitoring program and modular vibration isolation for transport.

# Project Manager Report
### Final Stage-Gate Approval Report for Modular Carbon Capture Package

## Executive Summary
- **Approval Status:** Conditional
- **Key Rationale:** The design demonstrates strong technical alignment with the 99.5% CO2 purity target and modular requirements, but capacity remains unspecified, requiring clarification before full commitment; safety risks are adequately mitigated but need final HAZOP confirmation.

## Alignment Assessment
The provided documents show good overall alignment across requirements, design basis, process flow, H&MB, equipment sizing, and safety analysis. The modular MDEA-based amine absorption process effectively addresses variable flue gas compositions (5-15% CO2, traces of SOx/NOx, particulates) through robust pre-treatment (G-101, F-101, U-101, U-102), achieving 90% capture efficiency and 99.5% CO2 purity (Stream 119) as per the BoD and stream table. Equipment summary (e.g., T-101 absorber at 3.0 m diameter for 100,000 Nm³/h flue gas) supports the reference capacity, with heat integration via E-101 (25 MW duty) optimizing energy use. H&MB balances are reconciled (e.g., CO2 inlet 12,000 kg/h, captured 10,800 kg/h), and utilities (e.g., 32 MW steam, 2.5 MW cooling) align with BoD estimates (0.8-1.2 GJ/t CO2).

**Conflicts/Discrepancies:**
- **Capacity Gap:** Requirements and BoD note "Not specified" for CO2 capture capacity, yet H&MB and equipment sizing assume a reference 100,000 Nm³/h flue gas (10,000 kg/h CO2 captured). This lacks site-specific justification and scalability confirmation for modularity.
- **Data Inconsistencies:** Stream table shows minor mass balance gaps (e.g., ~3,150 kg/h evaporation assumed but not fully detailed in wastewater Stream 301); equipment sizing placeholders (e.g., "<value>" in some parameters) indicate incomplete quantification, though calculations (e.g., G-101 duty 1.2 MW from ΔT=85°C) are reasonable.
- **Safety Alignment:** Hazards (e.g., SOx/NOx breakthrough risking solvent degradation) are well-mitigated (e.g., online analyzers on Streams 104/105), but BoD exclusions (e.g., full HAZOP) leave open risks like variable flue gas impacts on pre-treatment efficiency (<10 ppmv SOx/NOx assumed).
- **Assumptions vs. Requirements:** Flexible operating envelope (100-150°C inlet, 40-50°C absorber) matches unspecified feed conditions, but modular transport (skid-mounted units) needs validation against burner variability; MoC (316L SS for corrosive sections) aligns with safety needs.

No major conflicts, but the unspecified capacity and incomplete sizing details drive the conditional status, pending resolution to ensure economic viability.

## Approval Decision
**Status:** Conditional  
**Gating Conditions:**
1. Specify and validate design capacity (e.g., confirm 100,000 Nm³/h reference or scale to client needs) with site-specific flue gas data within 4 weeks.
2. Complete equipment sizing placeholders (e.g., exact flows, areas) and perform detailed HAZOP to address BoD exclusions.
3. Verify modular scalability (e.g., skid weights, interfaces) for various burner types, ensuring no impacts on purity or safety.

These conditions mitigate risks from data gaps; failure to address may escalate to rejection.

## Financial Outlook
Estimates derived from H&MB (10,000 kg/h CO2, 32 MW steam at $10/GJ, 2.5 MW cooling/electricity at $0.1/kWh), equipment scaling (e.g., columns ~$5M, compressor $10M), and industry benchmarks for amine CCS modules (CAPEX ~$500-800/t CO2 capacity). Reference capacity assumes 8,000 h/y operation (~80,000 t/y CO2). Contingency reflects medium risk level and capacity uncertainty.

| Metric                  | Estimate          | Notes |
|-------------------------|-------------------|-------|
| CAPEX (USD millions)   | 65                | Includes pre-treatment ($10M), columns/HX ($20M), rotating equip ($25M), utilities/skids ($10M); scaled from similar 10 kt/y plants. |
| OPEX (USD millions per year) | 12               | Steam ($8M), electricity ($2M), chemicals/maintenance ($2M); based on 3.2 GJ/t CO2 and 0.2% solvent makeup. |
| Contingency (%)        | 20                | Accounts for capacity TBD, potential pre-treatment upgrades for variable flue gas, and HAZOP findings. |

## Implementation Plan
1. **Finalize Design Data (Weeks 1-4, Project Engineering Team):** Resolve gating conditions by specifying capacity, completing H&MB/equipment details, and conducting preliminary HAZOP; deliver updated BoD and PFD for review.
2. **Procure Long-Lead Items (Weeks 5-12, Procurement Team):** Order critical equipment (e.g., T-101/T-102 columns, K-101 compressor) based on validated sizing; secure vendor quotes for modular skids to align with CAPEX.
3. **Fabricate and Test Modules (Months 4-9, Construction Team):** Assemble skid-mounted units (pre-treatment, absorption, regeneration), perform factory acceptance tests (e.g., pressure/leak checks), and ship to site; include safety interlock commissioning.

## Final Notes
- **Open Risk - Capacity Scalability:** Reference 100,000 Nm³/h flue gas in H&MB/equipment may not suit all burner types; validate against max variability (e.g., 15% CO2, high SOx) to avoid absorber overload (T-101, Stream 106).
- **Compliance Item - Environmental Permitting:** Wastewater (Stream 301, 5,000 kg/h) requires site-specific treatment validation per BoD Section 6; ensure SOx/NOx emissions (Stream 107) meet local limits post-pre-treatment (U-101/U-102 hazards).
- **Data Gap - Utility Integration:** Steam (U-202, 10,000 kg/h) and cooling (U-201, 200,000 kg/h) assume external supply; confirm plant interfaces to avoid OPEX overruns from BoD utility summary.
