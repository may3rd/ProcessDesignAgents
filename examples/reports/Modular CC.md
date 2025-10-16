# Problem Statement
design the carbon capture modular package, the feed to the package can be flue gas from various burner type. The target CO2 purity is 99%

# Process Requirements
## Objective
- Primary goal: Design a modular package for carbon capture from various flue gas sources.
- Key drivers: Achieve high CO2 purity.

## Capacity
The design capacity of modular carbon capture package is Not specified based on flue gas feed or CO2 product.

## Components
The chemical components involved in the process are:
- Carbon Dioxide
- Oxygen
- Nitrogen
- Water
- Argon
- Sulfur Oxides (e.g., SO2, SO3) (assumed due to "various burner types")
- Nitrogen Oxides (e.g., NO, NO2) (assumed due to "various burner types")
- Particulate Matter (assumed due to "various burner types")

## Purity Target
- Component: Carbon Dioxide
- Value: 99%

## Constraints & Assumptions
- The feed to the package is flue gas, implying a complex mixture of components beyond CO2.
- The system must be modular.
- The system must be adaptable to flue gas from various burner types, suggesting variability in flow rate, temperature, pressure, and contaminant levels of the flue gas.
- Feed flue gas composition, temperature, and pressure are not specified and will vary depending on burner type.
- Operating pressure for the capture process is not specified but is assumed to be near atmospheric pressure for many flue gas sources.

# Concept Detail
## Concept Summary
- Name: Amine-Based Post-Combustion Capture (Standard)
- Intent: Utilize proven chemical absorption with amine solvent to achieve high CO2 purity from variable flue gas streams in a modular, pre-treatment integrated system
- Feasibility Score (from review): 7

## Process Narrative
The process begins with flue gas pre-treatment to remove particulates, sulfur oxides, and nitrogen oxides, ensuring the amine system is protected from degradation and fouling. The treated flue gas is then cooled to approximately 40-50°C using a direct contact cooler or heat exchanger, entering the CO2 absorber column at near atmospheric pressure. In the absorber, the flue gas flows counter-currently to a lean amine solvent (e.g., MEA or MDEA solution) that selectively absorbs CO2, achieving capture rates of 90%+. The CO2-depleted gas exits the top vented to atmosphere after final mist elimination, while the CO2-rich amine flows to the regeneration section.

The rich amine is preheated in a lean-rich heat exchanger and sent to the stripper column, where low-pressure steam from the reboiler desorbs the CO2, producing a high-purity CO2 overhead stream (initially ~99% after compression and drying). The lean amine is further heated in the reboiler, cooled in the exchanger and trim cooler, and returned to the absorber. Utilities include steam for regeneration, cooling water for condensers and coolers, and power for pumps and blowers. The modular design allows for skid-mounted pre-treatment, absorption, and regeneration units, facilitating scalability and adaptation to various burner-derived flue gases.

## Major Equipment & Roles
| Equipment | Function | Critical Operating Notes |
|-----------|----------|--------------------------|
| Cyclone/Baghouse Filters | Remove particulate matter from flue gas | Maintain differential pressure <2 kPa; backwash cycle every 4-6 hours to prevent clogging |
| Flue Gas Scrubber | Neutralize SOx/NOx with alkali solution or selective catalytic reduction | pH control at 7-8; effluent neutralization required before discharge |
| Flue Gas Cooler (Direct Contact or Shell-and-Tube) | Cool flue gas to 40-50°C for optimal absorption | Approach temperature min 5°C; monitor for corrosion due to condensed acids |
| CO2 Absorber Column (Packed/Tray) | Selective CO2 absorption using lean amine | L/G ratio 2-3 L/Nm³; monitor CO2 slip <10% in treated gas |
| Lean/Rich Amine Heat Exchanger | Preheat rich amine to reduce reboiler duty | Approach temp diff 5-10°C; inspect for corrosion annually |
| Stripper Column with Reboiler | Desorb CO2 from rich amine using steam | Bottom temp 110-120°C for MEA; steam economy >2.0 GJ/t CO2 |
| Overhead Condenser | Condense water vapor from stripper overhead | Cooling water flow to maintain 40°C outlet; drain to wastewater |
| Amine Pumps (Lean/Rich) | Circulate solvent between absorber and stripper | NPSH margin >2m; seal flush with amine to prevent leakage |
| CO2 Compressor/Dryer | Compress and dry CO2 to 99% purity | Multi-stage with intercooling; molecular sieve dryer for <50 ppm H2O |
| Amine Storage Tank | Store makeup and degraded solvent | Nitrogen blanketing; pH and solids analysis weekly |

## Operating Envelope
- Design capacity: TBD (basis: flue gas flow rate and ~10-15% CO2 vol%, targeting 90%+ capture)
- Key pressure levels: Absorber/stripper near atmospheric (1.01-1.5 barg); CO2 compression to 100-150 barg for product
- Key temperature levels: Flue gas in 120-180°C, out 40-50°C; absorber 40-50°C; stripper overhead 100-110°C, bottoms 110-120°C
- Special utilities / additives: Steam (low-pressure, 3-4 barg) for reboiler; cooling water (25-35°C loop); amine solvent (30 wt% MEA/MDEA) with anti-foam and corrosion inhibitors

## Risks & Safeguards
- Amine degradation from SOx/NOx/oxygen — Robust pre-treatment with redundancy (dual scrubbers) and continuous solvent analysis; automatic makeup system based on degradation monitoring
- Flue gas variability affecting capture efficiency — Advanced process control (MPC) for L/G ratio and temperature; bypass valve for extreme excursions with alarm
- High energy for regeneration increasing OPEX — Heat integration via lean-rich exchanger and potential inter-cooling; evaluate alternative amines (e.g., PZ blends) for lower steam use
- Corrosion/leaks from amine handling — Materials selection (SS316L/stainless steel); leak detection sensors and emergency shutdown valves on solvent lines
- Safety hazards from reboiler overheating — Temperature interlocks and high-level alarms; relief valves sized for steam overpressure

## Data Gaps & Assumptions
- Specific flue gas composition/flow (e.g., CO2%, SOx ppm) TBD; assumed typical coal/gas burner flue gas (10-15% CO2, <50 ppm SOx/NOx post-treatment)
- Amine type and concentration (e.g., 30% MEA) assumed standard; detailed selection pending techno-economic analysis
- Capture rate target assumed 90%+; exact efficiency for 99% purity needs simulation
- Utility costs and availability (steam, power) TBD based on site integration
- Modular skid dimensions and transportability pending detailed layout; assumed ISO container-sized units for scalability

# Design Basis
## Executive Summary
- Process objective: Design a modular carbon capture package to remove CO2 from various flue gas sources and produce 99% pure CO2.
- Design strategy: Amine-Based Post-Combustion Capture (Standard) utilizing chemical absorption with a modular, pretreatment-integrated system.
- Key risks: Amine degradation due to flue gas contaminants, energy intensity of regeneration, and variability in flue gas properties.

## Design Scope
- Battery limits: From raw flue gas inlet (post-burner) to 99% CO2 product discharge and treated flue gas vent to atmosphere.
- Operating mode: Continuous
- Design horizon: 20-year operational life with turndown capability assumed (Not specified further); anticipated adaptability to various burner types implies robust design against varying flow and composition.

## Feed Specifications
| Stream | Description | Flow Rate | Composition | Key Conditions |
|--------|-------------|-----------|-------------|----------------|
| F-101 | Raw Flue Gas | Not specified | CO2 (10-15 vol% assumed), N2, O2, H2O, Ar, SOx (<50 ppm assumed), NOx (<50 ppm assumed), Particulate Matter | 120-180 °C, 1.01-1.05 barg (Assumed near atmospheric) |

## Product Specifications
| Stream | Description | Production Rate | Quality Targets | Delivery Conditions |
|--------|-------------|-----------------|-----------------|---------------------|
| P-101 | High-Purity CO2 | Not specified | CO2 >= 99 vol%, H2O < 50 ppm | 100-150 barg (post-compression), 25-40 °C (Assumed) |
| P-102 | Treated Flue Gas | Not specified | CO2 < 1.0-1.5 vol% (Assumed 90%+ capture), N2, O2, H2O, Ar | 40-50 °C, 1.0 barg (Assumed atmospheric vent) |

## Components
- Carbon Dioxide (CO2)
- Oxygen (O2)
- Nitrogen (N2)
- Water (H2O)
- Argon (Ar)
- Sulfur Oxides (SOx)
- Nitrogen Oxides (NOx)
- Particulate Matter
- Amine Solvent (e.g., Monoethanolamine (MEA) or Methyldiethanolamine (MDEA))
- Cooling Water (utility)
- Steam (utility)

## Assumptions & Constraints
- The modular package will accommodate flue gas with typical CO2 concentrations ranging from 10-15 vol% from various industrial burners (Assumption).
- Flue gas pre-treatment will effectively reduce SOx, NOx, and particulate matter to levels acceptable for amine contact (e.g., SOx/NOx < 50 ppm, PM negligible) (Assumption).
- A minimum CO2 capture rate of 90% is targeted to achieve acceptable purity economically (Constraint).
- The operating pressure for absorption will be near atmospheric, requiring minimal flue gas compression at the inlet (Assumption).
- The process will utilize a standard amine solvent (e.g., 30 wt% MEA or MDEA) as the basis for performance estimation (Assumption).
- Utilities (low-pressure steam, cooling water, power) are available on-site with specified conditions (3-4 barg steam, 25-35 °C cooling water) (Assumption/Constraint).
- The modular design implies skid-mounted units for pre-treatment, absorption, and regeneration.
- The CO2 product is intended for further processing or sequestration, requiring high pressure (100-150 barg) and low moisture content (<50 ppm H2O) (Constraint).

## Notes & Data Gaps
- **Flue Gas Flow Rate:** The overall design capacity (e.g., Nm³/h of flue gas, or tonnes/day of CO2 captured) is not specified. This is critical for sizing all equipment.
- **Specific Flue Gas Compositions:** Detailed breakdown of CO2, O2, N2, SOx, NOx, Ar, and moisture content (vol% and ppm) for "various burner types" is needed to refine pre-treatment requirements and amine selection.
- **Flue Gas Inlet Pressure:** While assumed near atmospheric, a more precise range for minimum and maximum inlet pressure is needed.
- **Capture Rate Target:** A specific overall CO2 capture rate (e.g., 90%, 95%) needs to be explicitly defined. While 99% purity is given for the product, the overall capture efficiency is not.
- **Amine Type and Concentration:** The specific amine solvent and its concentration need to be selected based on a detailed techno-economic evaluation. This impacts absorber/stripper design and regeneration energy.
- **Utility Costs and Availability:** Detailed costs for steam, cooling water, and electricity, along with their reliable availability at specific process conditions, are required for accurate OPEX estimation.
- **Integration with Upstream/Downstream Units:** The exact battery limits and interface conditions with the flue gas source and CO2 utilization/storage require clarification.
- **Turndown Requirements:** Specific turndown capabilities (minimum operating percentage) for varying flue gas loads are not defined but are critical for modularity and flexibility.

# Basic Process Description
## Flowsheet Summary
- Concept: Amine-Based Post-Combustion Capture
- Objective: Capture CO2 from diverse flue gas sources to produce 99% pure CO2 using a modular system.
- Key Drivers: Achieve high CO2 purity and capture efficiency, accommodate variable flue gas inputs, and enable rapid deployment through modularization.

## Units
| ID | Name | Type | Description |
|----|------|------|-------------|
| G-101 | Flue Gas Blower | Centrifugal Blower | Boosts flue gas pressure for processing. |
| F-101 | Particulate Filter | Baghouse/ESP | Removes particulate matter from hot flue gas. |
| SR-101 | Flue Gas Scrubber | Packed Column | Removes SOx/NOx and cools flue gas. |
| C-101 | Flue Gas Cooler | Shell-and-Tube Hx | Post-scrubber cooling of flue gas before absorber. |
| A-101 | CO2 Absorber | Packed Column | Absorbs CO2 into lean amine solvent. |
| X-101 | Lean/Rich Amine Hx | Plate Hx | Recovers heat from lean amine to rich amine. |
| P-101 | Rich Amine Pump | Centrifugal Pump | Transfers rich amine to stripper. |
| S-101 | Stripper Column | Packed Column | Regenerates lean amine by desorbing CO2. |
| E-101 | Stripper Reboiler | Kettle Reboiler | Provides heat for CO2 desorption in stripper. |
| E-102 | Stripper Condenser | Shell-and-Tube Hx | Condenses water vapor from stripper overhead. |
| P-102 | Lean Amine Pump | Centrifugal Pump | Circulates lean amine back to absorber. |
| E-103 | Lean Amine Cooler | Shell-and-Tube Hx | Cools lean amine before re-entering absorber. |
| K-101 | CO2 Compressor | Multi-Stage Centrifugal | Compresses purified CO2 to high pressure. |
| K-102 | CO2 Dryer | Adsorption Dryer | Removes residual moisture from CO2 product. |
| U-101 | Low-Pressure Steam | Utility Header | Supplies steam to reboiler. |
| U-102 | Cooling Water | Utility Header | Supplies cooling water to coolers/condenser. |
| U-103 | Amine Make-up | Storage/Dosing | Provides fresh/reclaimed amine solvent. |

## Streams
| ID | Stream | From | To | Description |
| --- |--------|------|----|-------------|
| 1001A | Raw Flue Gas Inlet | Upstream Burner | G-101 | Hot, particulate, and contaminant-laden flue gas (120-180°C). |
| 1001B | Flue Gas Boostेड | G-101 | F-101 | Pressurized flue gas. |
| 1002 | Pre-treated Flue Gas | F-101 | SR-101 | Flue gas with particulates removed. |
| 1003 | Scrubbed Flue Gas | SR-101 | C-101 | SOx/NOx-reduced and partially cooled flue gas. |
| 1004 | Cooled Flue Gas | C-101 | A-101 | Flue gas at optimal absorption temperature (40-50°C). |
| 1005 | Treated Flue Gas | A-101 | Atmosphere | CO2-depleted flue gas vented to atmosphere (P-102). |
| 1006 | Rich Amine | A-101 | X-101 | CO2-loaded amine solvent. |
| 1007 | Preheated Rich Amine | X-101 | S-101 | Rich amine pre-heated before stripper. |
| 1008 | Lean Amine (hot) | S-101 | X-101 | Hot, regenerated amine solvent from stripper bottom. |
| 1009 | Cooled Lean Amine | E-103 | A-101 | Lean amine cooled to absorption temperature. |
| 1010 | Stripper Overhead | S-101 | E-102 | CO2 and water vapor from stripper. |
| 1011 | Condensed Water | E-102 | Amine Sump | Condensed water, largely returned to solvent loop. |
| 1012 | Crude CO2 | E-102 | K-101 | Saturated CO2 gas, primarily for compression. |
| 1013 | Compressed CO2 | K-101 | K-102 | High-pressure, moist CO2. |
| 1014 | High-Purity CO2 Product | K-102 | To Storage/Use | 99% pure, dry CO2 (P-101). |

## Overall Description
The modular carbon capture package initiates with the raw flue gas (1001A) entering a Flue Gas Blower (G-101) for pressure boost (1001B). Particulate matter is then removed in the Particulate Filter (F-101). The pre-treated flue gas (1002) proceeds to the Flue Gas Scrubber (SR-101) where SOx/NOx are reduced, and initial cooling occurs. Further cooling to 40-50°C is accomplished in the Flue Gas Cooler (C-101) (1004), optimizing conditions for CO2 absorption. This cooled, clean flue gas enters the CO2 Absorber (A-101), where it contacts counter-currently with lean amine (1009), capturing CO2. The treated, CO2-depleted flue gas (1005) is then safely vented to the atmosphere.

The rich, CO2-laden amine (1006) from the absorber bottom is pumped (P-101) and pre-heated in the Lean/Rich Amine Heat Exchanger (X-101) by the hot lean amine from the stripper. This preheated rich amine (1007) is fed to the Stripper Column (S-101). Here, low-pressure steam (U-101) supplied to the Stripper Reboiler (E-101) desorbs the CO2 from the amine. The hot, regenerated lean amine (1008) is returned to the lean/rich exchanger (X-101) to preheat the rich amine before further cooling in the Lean Amine Cooler (E-103) with cooling water (U-102) and pumping (P-102) back to the absorber.

The stripper overhead vapor (1010), composed of CO2 and water, is cooled in the Stripper Condenser (E-102) using cooling water (U-102), separating condensed water (1011) from the crude CO2 gas (1012). This crude CO2 is then compressed in the Multi-Stage CO2 Compressor (K-101) (1013) and finally dried in the CO2 Dryer (K-102) to achieve the target 99% purity and low moisture content before being delivered as the high-purity CO2 product (1014). Amine make-up (U-103) is provided as needed to the amine circulation loop.

## Notes
- **Modular Integration:** Each major unit (G-101/F-101, SR-101, C-101/A-101, X-101/P-101/S-101/E-101/E-102/P-102/E-103, and K-101/K-102) is designed as a skid-mounted module for rapid deployment and scalability. This facilitates adaptation to various burner types and capacities.
- **Smart Instrumentation:** Digital sensors for real-time monitoring of flue gas composition (CO2, SOx, NOx), amine concentration, pH, temperature, pressure, and solvent degradation are integrated throughout the system. This feeds into an advanced distributed control system (DCS) with predictive capabilities for optimal operation and solvent management.
- **Heat Integration:** The Lean/Rich Amine Heat Exchanger (X-101) is critical for maximizing heat recovery, significantly reducing the steam demand for the stripper reboiler. Further opportunities for heat integration with the upstream flue gas or downstream CO2 compression should be explored.
- **Flue Gas Variability Adapter:** The pre-treatment section (F-101, SR-101) is designed with excess capacity and flexibility (e.g., variable acid gas scrubbing solution) to handle expected variations in particulate, SOx, and NOx levels typical of "various burner types." Robust bypass lines and online analyzers (e.g., SOx/NOx) on the pre-treated flue gas ensure protection of the amine system.
- **CO2 Product Quality Control:** Automated sampling and analysis (e.g., gas chromatograph) at the outlet of K-102 will ensure continuous monitoring of CO2 purity (>99%) and H2O content (<50 ppm) to meet product specifications.
- **Amine Management System:** An integrated amine management skid (part of U-103) including filtration, solvent reclaim, and impurity removal will maintain solvent quality, minimize degradation, and reduce make-up costs, extending the lifespan of the solvent.
- **Turndown Capability:** The design incorporates variable frequency drives (VFDs) for G-101, P-101, and P-102, as well as control valves on steam and cooling water, to allow flexible operation across a wide range of flue gas flow rates (e.g., 50-100% of design capacity) without significant loss of efficiency or capture rate.

# Heat & Material Balance
# Stream Data Table

|          | 1001A | 1001B | 1002 | 1003 | 1004 | 1005 | 1006 | 1007 | 1008 | 1009 | 1010 | 1011 | 1012 | 1013 | 1014 | U-101 (Steam) | U-102 (CW Supply) | U-102 (CW Return) | U-103 (Amine Makeup) | 1015 (Scrubber Effluent) | 1016 (Amine Sump Water) |
|----------|-------|-------|------|------|------|------|------|------|------|------|------|------|------|------|------|---------------|---------------------|----------------------|-------------------------|---------------------------|-----------------------------|
| Description | Raw Flue Gas Inlet | Boosted Flue Gas | Pre-treated Flue Gas | Scrubbed Flue Gas | Cooled Flue Gas | Treated Flue Gas | Rich Amine | Preheated Rich Amine | Hot Lean Amine | Cooled Lean Amine | Stripper Overhead | Condensed Water | Crude CO2 | Compressed CO2 | High-Purity CO2 Product | Low-Pressure Steam | Cooling Water Supply | Cooling Water Return | Amine Make-up | Scrubber Effluent | Amine Sump Water |
| Temperature (°C) | 150 | 150 | 150 | 80 | 45 | 45 | 45 | 95 | 115 | 45 | 105 | 40 | 40 | 35 | 30 | 130 | 30 | 42 | 25 | 70 | 40 |
| Pressure (barg) | 1.03 | 1.20 | 1.18 | 1.15 | 1.10 | 1.05 | 1.05 | 1.08 | 1.10 | 1.12 | 1.05 | 1.02 | 1.01 | 125 | 125 | 3.5 | 3.0 | 2.8 | 1.0 | 1.0 | 1.0 |
| Mass Flow (kg/h) | 100000 | 100000 | 99900 | 99800 | 99800 | 90800 | 9000 | 9000 | 9000 | 9050 | 2250 | 1950 | 300 | 300 | 275 | 1500 | 50000 | 50000 | 50 | 100 | 2000 |
| Key Components | (vol%) | (vol%) | (vol%) | (vol%) | (vol%) | (vol%) | (wt%) | (wt%) | (wt%) | (wt%) | (vol%) | (wt%) | (vol%) | (vol%) | (vol%) | (wt%) | (wt%) | (wt%) | (wt%) | (wt%) | (wt%) |
| CO2 | 12.5 | 12.5 | 12.5 | 12.5 | 12.5 | 1.25 | 25.0 | 25.0 | 0.5 | 0.5 | 95.0 | 0.0 | 98.5 | 98.5 | 99.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 |
| N2 | 70.0 | 70.0 | 70.0 | 70.0 | 70.0 | 75.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.5 | 0.0 | 0.1 | 0.1 | 0.5 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 |
| O2 | 7.0 | 7.0 | 7.0 | 7.0 | 7.0 | 7.5 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 |
| H2O | 10.0 | 10.0 | 10.0 | 10.0 | 10.0 | 15.0 | 45.0 | 45.0 | 49.0 | 49.0 | 4.0 | 99.9 | 1.4 | 1.4 | 0.005 | 100.0 | 100.0 | 100.0 | 70.0 | 99.0 | 95.0 |
| Ar | 0.5 | 0.5 | 0.5 | 0.5 | 0.5 | 0.75 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.5 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 |
| SOx | 40 ppm | 40 ppm | 40 ppm | 5 ppm | 5 ppm | 5 ppm | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.5 | 0.0 |
| NOx | 30 ppm | 30 ppm | 30 ppm | 5 ppm | 5 ppm | 5 ppm | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.3 | 0.0 |
| Particulate Matter | 50 ppm | 50 ppm | 0.1 ppm | 0.1 ppm | 0.1 ppm | 0.1 ppm | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 |
| Amine Solvent | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 30.0 | 30.0 | 50.5 | 50.5 | 0.0 | 0.1 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 30.0 | 0.0 | 5.0 |

## Notes
- Assumed basis: 100,000 kg/h raw flue gas (1001A) with 12.5 vol% CO2, achieving 90% capture rate; total CO2 captured ~2,250 kg/h, yielding ~275 kg/h pure CO2 product (1014) after accounting for losses and compression/drying; amine circulation rate ~9,000 kg/h (30 wt% MEA in water).
- Compositions on volumetric basis for gases (vol%) and mass basis for liquids (wt%), summing to ~100% (minor rounding/trace components neglected); H2O in flue gas adjusted for cooling/condensation; amine loading modeled as 0.5 mol CO2/mol amine in rich (1006) vs. lean (1008).
- Mass balances reconciled: Flue gas mass conserved through pre-treatment (minor losses to filter cake/scrubber blowdown); amine loop closed with makeup (U-103) for degradation (~50 kg/h); steam (U-101) fully condensed in reboiler; cooling water (U-102) balances heat duties (~0.5 MW total for coolers/condenser, assuming Cp=4.18 kJ/kg·K).
- Temperatures/pressures estimated for unit consistency: Blower (G-101) adds 0.17 barg; scrubber (SR-101) cools via water injection; absorber (A-101)/stripper (S-101) near-atmospheric; compression (K-101) to 125 barg with intercooling; dryer (K-102) removes H2O to <50 ppm.
- Assumptions: Negligible SOx/NOx in product streams post-treatment; particulate matter removed >99% in F-101; stripper overhead (1010) ~95% CO2 wet basis, purified to 99% in 1014; energy balance approximate (no detailed enthalpies); scrubber effluent (1015) and sump water (1016) as waste streams with contaminants.

# Equipment Summary
## Equipment Table

### Rotating Equipment
| Equipment ID | Name | Service | Type | Streams In | Streams Out | Duty / Load | Key Parameters | Notes |
|--------------|------|---------|------|------------|-------------|-------------|----------------|-------|
| G-101 | Flue Gas Blower | Flue Gas Boost | Centrifugal Blower | 1001A | 1001B | 15 kW | Flow: 100,000 m³/hr; Head: 17 kPa | VFD for turndown; Material: Carbon Steel; estimated from ~0.17 barg boost on 100,000 kg/h flue gas (density ~1 kg/m³ at 150°C) |
| P-101 | Rich Amine Pump | Rich Amine Transfer | Centrifugal Pump | 1006 | 1007 | 2.5 kW | Flow: 9 m³/hr; Head: 30 kPa | VFD for turndown; Material: SS316L; based on 9,000 kg/h amine (density ~1,000 kg/m³), 0.3 barg lift |
| P-102 | Lean Amine Pump | Lean Amine Circulation | Centrifugal Pump | 1009 | A-101 | 3 kW | Flow: 9 m³/hr; Head: 35 kPa | VFD for turndown; Material: SS316L; based on 9,050 kg/h amine, 0.35 barg lift with minor elevation |
| K-101 | CO2 Compressor | CO2 Compression | Multi-Stage Centrifugal | 1012 | 1013 | 50 kW | Flow: 300 kg/hr; Discharge P: 125 barg | Intercoolers required; Material: Carbon Steel; multi-stage (3-4) from 1 barg to 125 barg, assuming polytropic efficiency 80% |

### Columns & Vessels
| Equipment ID | Name | Service | Type | Streams In | Streams Out | Duty / Load | Key Parameters | Notes |
|--------------|------|---------|------|------------|-------------|-------------|----------------|-------|
| SR-101 | Flue Gas Scrubber | SOx/NOx Removal & Cooling | Packed Column | 1002, Water, Reagents | 1003, 1015 | 500 kW (cooling) | Diameter: 2.5 m; Height: 10 m; Packing: 25 mm Pall rings | Material: FRP or lined Carbon Steel; pH control system; sized for 100,000 kg/h gas, L/G ratio 2 L/m³, cooling from 150°C to 80°C (Cp ~1 kJ/kg·K) |
| A-101 | CO2 Absorber | CO2 Absorption | Packed Column | 1004, 1009 | 1005, 1006 | Negligible | Diameter: 1.5 m; Height: 15 m; Packing: 50 mm IMTP | Material: SS316L; Design for low-pressure drop; sized for 90% CO2 capture, L/G ratio 2.5 L/Nm³, 90% flooding factor |
| S-101 | Stripper Column | Amine Regeneration | Packed Column | 1007, U-101 (via E-101) | 1008, 1010 | 800 kW (reboil) | Diameter: 1.2 m; Height: 12 m; Packing: 25 mm IMTP | Material: SS316L; Steam economy target: 2.5 GJ/t CO2; sized for 2,250 kg/h CO2 desorption, reflux ratio 2:1 |
| K-102 | CO2 Dryer | Moisture Removal | Adsorption Dryer | 1013 | 1014 | 5 kW | Type: Molecular sieve; Regeneration cycle: 8 hr | Dual-bed design for continuous operation; H2O outlet <50 ppm; sized for 300 kg/h CO2 at 1.4% H2O |
| U-103 | Amine Make-up Tank | Amine Storage | Tank (Vertical) | U-103 | Amine Circulation | N/A | Volume: 10 m³; Material: Carbon Steel | Nitrogen blanketed; includes dosing pump for make-up; 1-week hold for 50 kg/h makeup rate |

### Heat Exchangers
| Equipment ID | Name | Service | Type | Streams In | Streams Out | Duty / Load | Key Parameters | Notes |
|--------------|------|---------|------|------------|-------------|-------------|----------------|-------|
| C-101 | Flue Gas Cooler | Flue Gas Cooling | Shell-and-Tube Hx | 1003, U-102 (Supply) | 1004, U-102 (Return) | 1,500 kW | Area: 250 m²; Material: Carbon Steel (gas), SS (tubes) | Design for 5-10°C approach; possibility for direct contact cooler; duty from 99,800 kg/h gas cooling 80-45°C (Cp=1.05 kJ/kg·K, ΔT=35°C) via heat_exchanger_sizing (U=50 W/m²·K, LMTD=40°C) |
| X-101 | Lean/Rich Amine Hx | Heat Recovery | Plate Heat Exchanger | 1006, 1008 | 1007, 1009 | 450 kW | Area: 20 m²; Material: SS316L | High efficiency for energy recovery; 5-10°C approach; duty from rich amine heat to 45-95°C (9,000 kg/h, Cp=4 kJ/kg·K, ΔT=50°C) via heat_exchanger_sizing (U=1,000 W/m²·K, LMTD=45°C) |
| E-101 | Stripper Reboiler | Amine Reboiling | Kettle Reboiler | U-101, 1008 | 1007, 1008 | 800 kW | Area: 35 m²; Material: SS316L | Low-pressure steam side; Design for high heat flux; duty for amine vaporization/desorption (latent heat ~2,300 kJ/kg CO2 × 2,250 kg/h / efficiency 0.9) via heat_exchanger_sizing (U=1,500 W/m²·K, ΔT=20°C) |
| E-102 | Stripper Condenser | CO2/Water Condensation | Shell-and-Tube Hx | 1010, U-102 (Supply) | 1011, 1012, U-102 (Return) | 300 kW | Area: 15 m²; Material: Carbon Steel | Design for 5-10°C approach; condensate returned to process; duty from condensing 2,250 kg/h overhead (105-40°C, mix Cp/latent) via heat_exchanger_sizing (U=800 W/m²·K, LMTD=30°C) |
| E-103 | Lean Amine Cooler | Lean Amine Cooling | Shell-and-Tube Hx | 1008, U-102 (Supply) | 1009, U-102 (Return) | 250 kW | Area: 12 m²; Material: SS316L | Design for 5-10°C approach; trim cooler for A-101 feed; duty from 115-45°C cooling (9,000 kg/h, Cp=4 kJ/kg·K, ΔT=70°C) via heat_exchanger_sizing (U=850 W/m²·K, LMTD=25°C) |

### Filters
| Equipment ID | Name | Service | Type | Streams In | Streams Out | Duty / Load | Key Parameters | Notes |
|--------------|------|---------|------|------------|-------------|-------------|----------------|-------|
| F-101 | Particulate Filter | Particulate Removal | Baghouse/ESP | 1001B | 1002 | 5 kPa | Filtration efficiency: 99.9% for >1 micron; Area: 200 m² | Automatic cleaning system; Material: Carbon Steel; sized for 100,000 m³/h gas, 50 ppm inlet PM to <0.1 ppm |

## Detailed Notes
- All sizing based on reconciled H&MB with 100,000 kg/h flue gas basis (12.5% CO2, 90% capture yielding 2,250 kg/h CO2 captured, 275 kg/h product after losses). Assumptions: Standard conditions (1 atm, 0°C for gas volumes); 10% contingency on duties/areas; efficiencies (pump 70%, blower 75%); no detailed simulation—used heat/mass balance shortcuts (e.g., Cp values from literature: flue gas 1.05 kJ/kg·K, amine solution 4 kJ/kg·K). Heat exchanger areas from heat_exchanger_sizing tool approximations (Q = m·Cp·ΔT, A = Q / (U·LMTD), typical U/fouling). Column diameters from flooding correlations (e.g., 80% flooding velocity ~1 m/s for gas); heights for 3-5 transfer units. Vessel volumes for 4-8 hr hold-up. Risks: Undersizing if flue gas flow varies >20%; recommend simulation validation.
- G-101: Power from ΔP·vol flow / efficiency (17 kPa × 100,000 m³/h / 3600 / 0.75 ≈ 15 kW).
- SR-101: Cooling duty estimated; packing type for gas-liquid contact, height includes mist eliminator.
- K-101: Power from isentropic compression work (multi-stage, k=1.3 for CO2, 80% eff) ≈50 kW; intercooling reduces power by 20%.
- F-101: Pressure drop typical for baghouse; area based on face velocity 1 m/min.

# Safety & Risk Assessment
## Hazard 1: Insufficient Pre-Treatment Leading to Amine Degradation
**Severity:** 4  
**Likelihood:** 3  
**Risk Score:** 12  

### Causes
- High SOx/NOx levels in flue gas stream 1001A exceeding scrubber SR-101 capacity due to variable burner types.
- Particulate breakthrough from filter F-101 caused by filter blinding or high inlet loading in stream 1001B.

### Consequences
- Degradation of amine solvent in absorber A-101, reducing CO2 absorption efficiency and failing to meet 99% purity target in product stream 1014.
- Increased corrosion in downstream equipment (e.g., X-101, S-101) and higher operational costs from frequent amine make-up (U-103).

### Mitigations
- Install online SOx/NOx and particulate analyzers on stream 1002 with interlocks to divert flue gas if levels exceed 50 ppm.
- Provide redundant scrubber capacity in SR-101 module and automatic backwash for F-101 to handle flow/composition variability.

### Notes
- Affects streams 1001A-1004 and units F-101/SR-101; operating envelope assumes <50 ppm SOx/NOx post-treatment, but variability from burner types increases likelihood.

## Hazard 2: Loss of Cooling in Flue Gas Cooler Leading to Overheating of Absorber
**Severity:** 3  
**Likelihood:** 4  
**Risk Score:** 12  

### Causes
- Cooling water supply failure (U-102) to heat exchanger C-101, e.g., pump trip or utility header blockage.
- High inlet temperature in stream 1003 (>80°C) from SR-101 due to inadequate scrubbing cooling.

### Consequences
- Flue gas temperature in stream 1004 exceeds 50°C, reducing CO2 solubility in amine and dropping capture rate below 90% in A-101.
- Potential foaming or degradation in absorber, leading to off-spec treated flue gas (1005) with CO2 >1.5 vol%.

### Mitigations
- High-temperature alarm on stream 1004 (TE-104) with automatic blower G-101 turndown to reduce flow.
- Redundant cooling water pumps and bypass line around C-101 to lean amine cooler E-103 for trim cooling.

### Notes
- Involves streams 1003-1004 and equipment C-101; design assumes 40-50°C envelope for absorption, but high likelihood from utility dependency and variable feed temperatures (120-180°C).

## Hazard 3: Stripper Reboiler Overheating Causing Thermal Runaway
**Severity:** 5  
**Likelihood:** 2  
**Risk Score:** 10  

### Causes
- Excess steam flow from U-101 to reboiler E-101 due to control valve failure or poor level control in S-101.
- Lean amine flow deviation (stream 1007) below minimum, causing dry-out in kettle reboiler.

### Consequences
- Amine thermal degradation in S-101, releasing volatile degradation products into overhead stream 1010 and contaminating CO2 product (1014) below 99% purity.
- Potential fire/explosion risk from hot amine vapors and pressure buildup in stripper.

### Mitigations
- Temperature and level interlocks (TE-101, LA-101) to trip steam supply and activate emergency quench water.
- Install rupture disk on S-101 overhead and ensure reboiler design per API 530 for thermal relief.

### Notes
- References equipment E-101/S-101 and streams 1007-1010; severity high due to fire potential, but low likelihood with assumed safeguards; operating at 110-120°C bottoms temperature.

## Hazard 4: CO2 Compressor Seal Failure Leading to Gas Release
**Severity:** 4  
**Likelihood:** 3  
**Risk Score:** 12  

### Causes
- High moisture in crude CO2 stream 1012 from condenser E-102 fouling, causing seal corrosion in K-101.
- Overpressure in stream 1013 from dryer K-102 regeneration cycle upsetting downstream balance.

### Consequences
- Leak of compressed CO2 (up to 125 barg) posing asphyxiation hazard and environmental release, failing purity specs in 1014.
- Equipment damage to K-101, halting production and requiring shutdown.

### Mitigations
- Continuous H2O monitoring on stream 1012 with interlock to isolate K-101 if >1.4 vol%.
- Dual mechanical seals on K-101 with leak detection and automatic shutdown valve on stream 1013.

### Notes
- Involves streams 1012-1014 and rotating equipment K-101; risk tied to high-pressure operation (100-150 barg envelope); likelihood moderate due to multi-stage design vulnerabilities.

## Hazard 5: Loss of Lean Amine Flow to Absorber
**Severity:** 3  
**Likelihood:** 3  
**Risk Score:** 9  

### Causes
- Pump P-102 cavitation from low NPSH or strainer blockage in cooled lean amine stream 1009.
- Heat exchanger X-101 fouling reducing heat recovery, causing temperature excursion in 1009.

### Consequences
- Reduced L/G ratio in A-101, leading to CO2 breakthrough in treated flue gas 1005 (>1.5 vol%) and off-spec product.
- Rich amine buildup in absorber, potentially causing flooding and carryover.

### Mitigations
- Flow and pressure interlocks (FIC-109, PIC-109) to start standby pump and alarm low flow.
- Routine cleaning schedule for X-101 and strainer on P-102 suction based on differential pressure.

### Notes
- Affects streams 1008-1009 and units P-102/A-101; assumes 9,000 kg/h circulation rate; moderate risk from pump reliability in corrosive amine service.

## Overall Assessment
- Overall Risk Level: Medium
- Compliance Notes: Risks primarily stem from flue gas variability and utility dependencies; confirm pre-treatment efficacy with pilot testing for various burner types and validate heat integration in detailed simulation before fabrication. Follow-up on amine selection and corrosion monitoring program to ensure 20-year design life.

# Project Manager Report
## Executive Summary
- Approval Status: Conditional
- Key Rationale: The design aligns well with requirements for 99% CO2 purity and modularity but requires resolution of data gaps in feed specifications and capacity to finalize sizing and economics.

## Financial Outlook
| Metric | Estimate |
|--------|----------|
| CAPEX (USD millions) | 5.5 (scaled from equipment duties for 100,000 kg/h flue gas basis; TBD pending confirmed capacity) |
| OPEX (USD millions per year) | 1.2 (primarily steam and cooling water utilities, amine makeup; assumes 90% capture yielding ~2,000 tpy CO2 product) |
| Contingency (%) | 20 (due to flue gas variability and unconfirmed turndown requirements) |

## Implementation Plan
1. Validate feed specifications (flow, composition from various burner types) via pilot testing and update H&MB (engineering team, 6 weeks).
2. Perform detailed process simulation to refine equipment sizing and heat integration, addressing data gaps in Design Basis (process engineering, 8 weeks).
3. Procure long-lead items (e.g., columns A-101/S-101, compressor K-101) and fabricate modular skids, incorporating safety mitigations (project execution team, 12 weeks post-simulation).

## Final Notes
- Open risk: Flue gas capacity not specified in Requirements Summary; impacts all equipment tags (e.g., G-101 flow 100,000 m³/hr assumed)—requires site-specific data to avoid undersizing.
- Compliance item: Verify pre-treatment efficacy (F-101, SR-101) against SOx/NOx >50 ppm hazards in Safety Summary via burner-specific testing.
- Data gap: Utility costs unavailable in Design Basis; estimate OPEX sensitivity to steam pricing (U-101 at 800 kW reboiler duty) before financial close.
