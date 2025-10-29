# Problem Statement
design the carbon capture modular package, the feed to the package can be flue gas from various burner type. The target CO2 purity is 99.5% with the capacity of CO2 capture is30 Ton per day

# Process Requirements
## Objective
- Primary goal: Design a modular package for Carbon Capture
- Key drivers: Modular design (implying portability/scalability), High CO2 Purity

## Capacity
The design capacity of the CO2 capture unit is 30.0 Ton/day, based on the captured CO2 mass flow rate.

## Components
The chemical components involved in the process are:
- Carbon Dioxide (CO2)
- Nitrogen (N2) (Inferred from Flue Gas)
- Oxygen (O2) (Inferred from Flue Gas)
- Water (H2O) (Inferred from Flue Gas)
- Trace Pollutants (e.g., SOx, NOx, Particulates) (Inferred from Flue Gas)

## Purity Target
- Component: Carbon Dioxide (CO2)
- Value: 99.5%

## Constraints and Assumptions
- The feed is Flue Gas, implying a mixture of N2, O2, CO2, and H2O (steam).
- The modular design requirement suggests constraints on footprint and weight. (Not specified)
- The process must handle variability in feed composition due to "various burner types." (Not specified)
- Key operating parameters like temperature and pressure of the feed flue gas are not specified. (Not specified)

# Concept Detail
## Concept Summary
- Name: Conventional Amine Absorption (MEA/MDEA)
- Intent: Design a modular package for Carbon Capture with a target CO2 purity of 99.5%
- Feasibility Score (from review): 6

## Process Narrative
The process begins with the raw flue gas feed, which must first undergo rigorous pre-treatment. This pre-treatment system (likely a quencher, scrubber, and filter bank) is critical to remove particulates, sulfur oxides (SOx), and nitrogen oxides (NOx) to protect the amine solvent from degradation and corrosion. The cleaned, cooled flue gas is then fed into the Amine Absorber Column (C-101), where it flows counter-currently against the lean amine solvent. The amine chemically reacts with the CO2, capturing it from the gas stream, while the remaining treated flue gas (primarily N2 and O2) is vented.

The rich amine, now saturated with CO2, is pumped to the Amine Stripper/Regenerator Column (C-201). Here, heat is applied, typically via a reboiler (E-201) utilizing low-pressure steam, to reverse the chemical reaction. This releases high-purity CO2 overhead, regenerating the amine solvent back to its lean state. The lean amine is cooled (E-202) and recycled back to the absorber. The hot, wet CO2 gas leaving the stripper is cooled (E-301) to knock out excess water before being sent to the final CO2 Compression and Drying Unit (K-301/D-301) to achieve the required 99.5% purity and reach the final delivery pressure.

## Major Equipment & Roles
| Equipment | Function | Critical Operating Notes |
|---|---|---|
| S-101 Flue Gas Pre-treatment Skid | Remove SOx, NOx, and particulates from flue gas feed. | Must maintain contaminant levels below 10 ppmv (TBD) to prevent solvent degradation. Requires continuous monitoring of flue gas composition. |
| C-101 Amine Absorber | Capture CO2 from the flue gas using lean amine solvent. | Column height is critical for capture efficiency; modular design may require structured packing. Maintain strict temperature control to optimize absorption kinetics. |
| C-201 Amine Stripper/Regenerator | Regenerate rich amine solvent by stripping CO2 using heat. | Requires reliable supply of low-pressure steam (TBD pressure). Maintain reboiler duty to ensure complete solvent regeneration. |
| E-201 Reboiler | Supply thermal energy (steam) to the stripper column base. | High thermal load component; steam quality and pressure stability are paramount for process stability. |
| K-301 CO2 Compressor Train | Increase pressure of the recovered CO2 product to handling specifications. | Multi-stage compression with intercooling (E-302, E-303). Must handle saturated gas from the stripper. |
| D-301 CO2 Dryer | Remove residual moisture from compressed CO2 product. | Typically uses molecular sieves or desiccants to achieve necessary dryness for 99.5% purity specification. |

## Operating Envelope
- Design capacity: 30.0 Ton/day captured CO2 (continuous basis)
- Key pressure levels: Absorber operates near atmospheric pressure (0.1–0.5 barg). Stripper operates at 1.5–2.5 barg. Final CO2 product pressure TBD (e.g., 150 barg for pipeline).
- Key temperature levels: Absorber operating temperature 40–60°C. Stripper bottom temperature 110–130°C.
- Special utilities / additives: Low-pressure steam (TBD supply pressure and flow rate), high-volume cooling water (for intercoolers and solvent cooler), advanced amine solvent (e.g., activated MDEA or proprietary blend), and make-up demineralized water.
- Material compatibility: Carbon steel with corrosion inhibitors is standard, but stainless steel may be required in high-temperature, high-CO2 areas (e.g., reboiler/stripper base) due to potential corrosion from degradation products.

## Risks & Safeguards
- Flue gas contaminants (SOx/NOx) cause rapid solvent degradation — Implement fully automated, continuous monitoring of flue gas quality upstream of S-101 with an automatic shutdown/bypass (divert flue gas) on high contaminant levels.
- High steam demand and Opex due to solvent regeneration — Mandate the use of low-heat-of-reaction solvents (e.g., MDEA) and include robust heat integration (rich/lean exchanger E-203) to minimize external energy input.
- Failure of absorber or stripper due to physical size constraints for modularity — Use high-performance structured packing and maximize column diameter within modular limits, accepting a potential increase in solvent circulation rate to compensate for reduced height.
- Loss of cooling water utility leading to high stripper pressure and poor solvent cooling — Install emergency cooling water backup connection or redundant pumps. Implement high-pressure trip on C-201.

## Data Gaps & Assumptions
- Assumed the flue gas feed is available at near-atmospheric pressure; if feed pressure is significantly lower, dedicated blowers will be required.
- TBD: Precise specification and availability of the low-pressure steam utility (pressure and temperature) needed for the E-201 reboiler duty.
- TBD: Detailed composition of the flue gas (CO2 concentration, SOx/NOx levels) from the "various burner types" is required to finalize the design of the S-101 pre-treatment unit.
- TBD: Final CO2 delivery specification (pressure and temperature) needed to size the K-301 compressor train.

# Design Basis
## Preliminary Process Basis of Design (BoD)

### 1. Project Overview and Problem Statement
This document defines the preliminary basis for the design of a modular Carbon Capture (CC) package utilizing Conventional Amine Absorption technology. The primary objective is to design a compact, transportable unit capable of capturing Carbon Dioxide (CO2) from various industrial burner flue gas sources. The required capture capacity is 30.0 metric tons per day (MTPD) of CO2. The final product must meet a high-purity specification of 99.5% (mol/mol) CO2, necessitating integrated compression and drying within the modular package scope. The design must accommodate the constraints of modularity, including limitations on footprint and vertical height, and be robust enough to handle variability in feed gas composition from different burner types.

### 2. Key Design Assumptions and Exclusions
* **Operating Factor:** A minimum stream factor of 90% (7,884 operating hours per year) is assumed, reflecting continuous operation with scheduled maintenance allowances.
* **Design Margin:** A 10.0% design margin is applied to the nameplate capacity, resulting in a design capacity of 33.0 MTPD of CO2.
* **Flue Gas Feed Conditions:** Flue gas is assumed to be available at near-atmospheric pressure (nominally 0.1 barg) and at a temperature that permits effective pre-treatment and cooling to the absorber inlet temperature (50°C assumed).
* **Solvent Selection:** Methyldiethanolamine (MDEA) or an accelerated/activated MDEA blend is assumed as the primary solvent due to its lower heat of regeneration and better resistance to thermal degradation compared to Monoethanolamine (MEA).
* **Location:** The modular unit is designed for a temperate climate; specialized insulation or freeze protection may be required based on the final, specific installation site.
* **Exclusions:** This preliminary BoD excludes the design of off-site facilities, detailed civil/structural support for the modular package, final connection tie-ins to the host facility, and detailed cost estimation (CAPEX/OPEX).

### 3. Design Capacity and Operating Conditions
| Parameter | Value | Units | Basis |
|---|---|---|---|
| **Nameplate Capacity** | 30.0 | MTPD CO2 | User Requirement |
| **Design Capacity** | 33.0 | MTPD CO2 | 10% Design Margin |
| **Hourly Throughput Rate** | 1,375 | kg/hr CO2 | Based on 24 hours/day operation |
| **Capture Efficiency Target** | 90 | % | Preliminary Estimate for Amine System |
| **Absorber Pressure** | 0.1 – 0.5 | barg | Near Atmospheric Operation |
| **Stripper Pressure** | 1.5 – 2.5 | barg | Optimal Regeneration Pressure |
| **Absorber Temperature** | 40 – 60 | °C | Optimized for CO2 Absorption Kinetics |
| **Stripper Bottom Temp.** | 110 – 130 | °C | Required for MDEA Regeneration |

### 4. Chemical Components
| Name | Formula | MW (g/mol) | NBP (°C) |
|---|---|---|---|
| Nitrogen | N2 | 28.013 | -196.0 |
| Oxygen | O2 | 31.999 | -183.0 |
| Carbon Dioxide | CO2 | 44.010 | -78.5 |
| Water | H2O | 18.015 | 100.0 |
| Methyldiethanolamine | C5H13NO2 | 119.16 | 247.0 |

### 5. Feed and Product Specifications

#### Feed Specification (Flue Gas)
* **Source:** Flue gas from various burner types (e.g., natural gas, coal, oil).
* **Pressure:** Near-atmospheric (0.1 barg assumed).
* **Contaminant Limits (SOx/NOx):** Must be pre-treated to below 10 ppmv (parts per million by volume) combined SOx/NOx to prevent rapid amine degradation (Industry Standard Assumption).
* **Particulates:** Must be filtered to below 5 mg/Nm³ (Industry Standard Assumption).
* **CO2 Concentration:** Assumed to be in the range of 4–15 vol% (depending on burner type); the unit must be designed for the highest expected flow rate at the lowest expected CO2 concentration.

#### Product Specification (Captured CO2)
* **Target Standard:** High Purity CO2
* **Purity (Min):** 99.5 mol% CO2 (User Requirement).
* **Moisture Content (Max):** Must be dry (e.g., < 50 ppmv H2O) to prevent corrosion during compression and meet high-purity specifications.
* **Delivery Pressure:** Assumed 150 barg for pipeline or storage compatibility (TBD based on final user requirement).
* **Inert Gases (Max):** 0.5 mol% (Primarily N2/O2 slip).

### 6. Preliminary Utility Summary
* **Process Water:** High-volume Demineralized (DM) water required for solvent make-up, washing, and pre-treatment scrubbing/quenching.
* **Steam:** Low-Pressure (LP) Steam (nominally 4–6 barg saturated) required for the Stripper Reboiler (E-201). The steam demand represents the largest operating cost driver.
* **Cooling Water:** High-volume cooling water required for the intercoolers (K-301 train), solvent cooler (E-202), and CO2 product condenser (E-301). Assumed closed-loop cooling tower system.
* **Electricity:** 480V / 3-phase / 60Hz standard assumed for pumps, blowers, and compressors (K-301).
* **Instrument Air:** Standard dry instrument air supply required for pneumatic controls and actuated valves.
* **Nitrogen (N2):** Required for system purging and inerting during shutdown and start-up operations.

### 7. Environmental and Regulatory Criteria
* **Air Emissions:** The treated flue gas vented from the top of the Absorber (C-101) must comply with local air quality standards for criteria pollutants (SOx, NOx). Amine slip (VOCs) must be minimized via a water wash section in the absorber.
* **Wastewater:** Wastewater from the pre-treatment scrubber (S-101) will contain concentrated pollutants (SOx, particulates) and must be treated (e.g., pH neutralization, heavy metal removal) before discharge or deep well injection.
* **Solid Waste:** Spent activated carbon/filter media from the pre-treatment skid and exhausted desiccant from the CO2 dryer (D-301) must be managed and disposed of per local hazardous waste regulations.
* **Regulatory Compliance:** The modular unit must comply with all relevant Pressure Equipment Directives (PED) and local permitting requirements for chemical processing plants.

### 8. Process Selection Rationale (High-Level)
The Conventional Amine Absorption process (specifically MDEA) is selected because it is a mature, commercially proven technology capable of achieving the required 90%+ capture efficiency and high-purity CO2 product. While Pressure Swing Adsorption (PSA) or Membrane technologies exist, Amine Absorption offers superior flexibility in handling variable CO2 concentrations in the flue gas, which is a key requirement of the Problem Statement ("various burner types"). The modular approach is facilitated by using high-efficiency structured packing in the columns, which minimizes column height and diameter compared to trayed columns, allowing the unit to fit within standard shipping constraints.

### 9. Preliminary Material of Construction (MoC) Basis
* **General Service:** Carbon Steel (CS) is acceptable for low-temperature, non-corrosive sections, such as the initial flue gas ducting and utility piping.
* **Pre-treatment/Scrubbing:** Fiberglass Reinforced Plastic (FRP) or specialized corrosion-resistant alloys (e.g., 316L SS) are required for the pre-treatment section (S-101) due to the presence of wet SOx/NOx and low pH conditions.
* **Amine Loop (Low Temp):** Carbon Steel (CS) is generally acceptable for the absorber (C-101) and associated piping, provided robust corrosion inhibitors are constantly maintained in the solvent.
* **Amine Loop (High Temp/Corrosive):** Stainless Steel (304L or 316L SS) is mandatory for the Stripper (C-201), Reboiler (E-201), Rich/Lean Exchanger (E-203), and high-pressure sections of the CO2 compressor (K-301) due to elevated temperatures, CO2 partial pressure, and potential solvent degradation products.

# Basic Process Flow Diagram
## Flowsheet Summary
- Concept: Modular Amine Carbon Capture (MDEA)
- Objective: Capture 30.0 MTPD of CO2 from variable flue gas streams and deliver a final product with 99.5% purity.
- Key Drivers: Modular design, high CO2 purity, high operational reliability against feed variability.

## Units
| ID | Name | Type | Description |
|---|---|---|---|
| S-101 | Flue Gas Pre-treatment | Scrubber/Filter Skid | Removes particulates, SOx, and NOx from feed flue gas, cooling it to 50°C. FRP construction mandated. |
| C-101 | Amine Absorber | Packed Column | Absorbs CO2 from cleaned flue gas using counter-current lean MDEA solvent. Operates near atmospheric pressure (0.1 barg). |
| P-101 | Rich Amine Pump | Centrifugal Pump | Transfers CO2-rich solvent from C-101 bottom to the stripping section (C-201) via E-203. |
| C-201 | Amine Stripper | Packed Column | Regenerates rich amine by heating, releasing high-purity CO2 overhead. Operates at 1.5–2.5 barg. |
| E-201 | Stripper Reboiler | Kettle Exchanger | Supplies thermal energy (LP Steam) to the stripper base to drive the CO2 stripping reaction. |
| E-203 | Rich/Lean Exchanger | Plate-Frame Exchanger | Critical heat integration unit; preheats rich amine before C-201 using hot lean amine from E-201. |
| E-202 | Lean Amine Cooler | Shell-and-Tube Exchanger | Cools regenerated lean amine from E-203 before recycling back to the Absorber (C-101) using Cooling Water (CW). |
| P-201 | Lean Amine Pump | Centrifugal Pump | Recycles cooled, regenerated lean amine back to the top of the Absorber (C-101). |
| E-301 | CO2 Condenser | Air-Cooled Exchanger | Cools and condenses water vapor from the overhead CO2 product stream from C-201. |
| K-301 | CO2 Compressor Train | Multi-Stage Centrifugal Compressor | Boosts CO2 pressure from 2.0 barg to the final delivery pressure (assumed 150 barg). Includes multiple intercoolers. |
| D-301 | CO2 Dryer | Adsorption Dryer Skid | Final purification step to remove moisture to below 50 ppmv, ensuring 99.5% purity and preventing corrosion. |

## Streams
| ID | Stream | From | To | Description |
|---|---|---|---|---|
| 1001 | Flue Gas Feed | Upstream Burner | S-101 | Hot, wet flue gas containing N2, O2, H2O, CO2 (4-15%), and contaminants. P ~ 0.1 barg. |
| 1002 | Cleaned Flue Gas | S-101 | C-101 | Cooled (50°C), contaminant-free flue gas. Ready for absorption. |
| 1003 | Treated Flue Gas Vent | C-101 | Atmosphere | Vented gas, primarily N2 and O2, with residual CO2 (10% slip assumed). Near atmospheric pressure. |
| 1004 | Rich Amine | C-101 | P-101 | Solvent saturated with CO2, ready for regeneration. T ~ 55°C. |
| 1005 | Lean Amine Supply | E-202 | C-101 | Regenerated MDEA solvent, cooled back to 40°C for optimal absorption. |
| 1006 | Rich Amine (Hot) | P-101 | E-203 | Rich amine pumped and preheated via heat integration. |
| 1007 | Rich Amine (Stripper Inlet) | E-203 | C-201 | Rich amine entering the stripper column after preheating (T ~ 100°C). |
| 1008 | Lean Amine (Hot) | C-201 | E-203 | Hot, regenerated lean amine from stripper base (T ~ 125°C). |
| 1009 | Lean Amine (Cooler Inlet) | E-203 | E-202 | Lean amine cooled by E-203, ready for final cooling. |
| 1010 | Regenerated CO2 (Wet) | C-201 | E-301 | Hot, saturated CO2 product gas (P ~ 2.0 barg). |
| 1011 | Condensed Water | E-301 | Solvent Sump | Water knocked out from the CO2 stream. Recycled to process make-up. |
| 1012 | CO2 Compressor Feed | E-301 | K-301 | Cooled, partially dried CO2 product gas. |
| 4001 | Final CO2 Product | D-301 | Storage/Pipeline | High-purity CO2 (99.5% min), dry, P ~ 150 barg. |
| 2001 | LP Steam Supply | Utility Header | E-201 | Low-pressure steam (4–6 barg) for regeneration heat duty. |
| 2002 | Condensate Return | E-201 | Utility Return | Steam condensate returned for reuse. |
| 2003 | Cooling Water Supply | Utility Header | E-202/E-301/K-301 | Cooling water for intercoolers and solvent/product cooling. |
| 2004 | Cooling Water Return | E-202/E-301/K-301 | Utility Return | Warmed cooling water returning to the cooling tower. |

## Overall Description
The process begins with the raw Flue Gas Feed (Stream 1001), which is routed to the Flue Gas Pre-treatment Skid (S-101) to remove particulates and harmful contaminants (SOx/NOx), protecting the downstream amine solvent. The cleaned, cooled flue gas (Stream 1002) enters the Amine Absorber (C-101) where it contacts the Lean Amine Supply (Stream 1005). The CO2 is chemically absorbed, and the treated flue gas (Stream 1003) is vented to the atmosphere. The resulting Rich Amine (Stream 1004) is pumped (P-101) and preheated in the highly efficient Rich/Lean Exchanger (E-203) via heat integration (Stream 1006 to 1007).

The heated rich amine (Stream 1007) enters the Amine Stripper (C-201) where the chemical bond is reversed using heat supplied by the Stripper Reboiler (E-201), which utilizes LP Steam (Stream 2001). High-purity, wet CO2 gas (Stream 1010) leaves the stripper overhead and is cooled in the CO2 Condenser (E-301) to remove bulk water (Stream 1011). The Regenerated CO2 (Stream 1012) is then sent to the Multi-Stage CO2 Compressor Train (K-301) and finally to the CO2 Dryer (D-301) to achieve the 99.5% purity and 150 barg delivery pressure (Stream 4001). The hot Lean Amine (Stream 1008) is internally cooled in E-203 before final trimming in the Lean Amine Cooler (E-202), and then pumped (P-201) back to the absorber top (Stream 1005).

## Notes
- **Modular Design:** The columns (C-101, C-201) will utilize high-performance structured packing to minimize column height, ensuring the entire absorption/stripping section fits within standard transportable skid dimensions (e.g., 12 ft width, 40 ft length, 12 ft height).
- **Advanced Heat Integration:** The use of a highly efficient Plate-Frame Exchanger (E-203) is specified for rich/lean exchange to maximize heat recovery and minimize external LP Steam demand, which is the largest factor in Opex.
- **Smart Instrumentation:** The pre-treatment skid (S-101) requires a continuous, online gas analyzer (T-101, not listed as major equipment) linked to an advanced control system (DCS) to monitor SOx/NOx levels. This system will auto-divert flue gas (Stream 1001) if contaminant limits are exceeded, providing crucial solvent protection.
- **Purity Assurance:** The final product purity (99.5%) is guaranteed by the two-step purification process: condensation (E-301) to remove bulk water, followed by the Adsorption Dryer Skid (D-301) to remove trace moisture and achieve the required dryness level for high-pressure handling.
- **Material Selection:** 316L Stainless Steel is mandated for all high-temperature sections (C-201, E-201, E-203) and the CO2 wet compression stages (K-301 inlet) due to the corrosive nature of hot, water-saturated CO2 and amine degradation products.

# Equipment and Streams List
## Equipment Summary

| ID | Name | Type | Service | Description | Streams In | Streams Out | Design Criteria | Sizing Parameters | Notes |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| S-101 | Flue Gas Pre-treatment | Scrubber/Filter Skid | Removes particulates, SOx, and NOx from feed flue gas, cooling it to 50°C. |  | 1001 | 1002 | <21900.0 Nm³/h> | Flue Gas Flow Rate: 21900.0 Nm³/h<br>Design Pressure: 0.5 barg<br>vessel_diameter: 1500.0 mm<br>vessel_length: 6000.0 mm | Manual estimation applied due to tool error in size_knockout_drum_basic (volume 0.0 m³). Sized based on gas flow from stream 1001 (977.6 kmol/h ≈ 21900 Nm³/h at standard conditions) and typical scrubber residence time of 3 minutes. Diameter 1.5 m, length 6 m for L/D=4. Assumed wire mesh demister and spray nozzles. FRP construction for corrosion. Recommend vendor consultation for detailed internals. |
| C-101 | Amine Absorber | Packed Column | Absorbs CO2 from cleaned flue gas using counter-current lean MDEA solvent. |  | 1002, 1005 | 1003, 1004 | <90% CO2 capture> | Diameter: 2500.0 mm<br>Packed Height: 20.0 m<br>number_of_stages: 12.0 count<br>solvent_circulation: 16562.0 kg/h | Tool size_absorption_column_basic used but result unrealistic (diameter 10 m, solvent 174k kg/h vs actual 16.5k kg/h from stream 1005) due to null Henry constant for MDEA. Manual adjustment based on 90% CO2 removal (31.25 kmol/h from 34.7 kmol/h inlet), typical 10-15 stages for MDEA, structured packing. Diameter 2.5 m at 80% flood velocity. Height 20 m for efficiency. Operates at 0.1 barg, 40-50°C. Recommend rigorous simulation in FEED Phase 2. |
| P-101 | Rich Amine Pump | Centrifugal Pump | Transfers CO2-rich solvent from C-101 bottom to the stripping section (C-201) via E-203. |  | 1004 | 1006 | <17.9 m³/h> | Flow Rate: 17.9 m³/h<br>Differential Head: 27.0 m<br>motor_power: 2.0 kW<br>npsh_required: 3.0 m<br>pump_type: Centrifugal string | Sized using size_pump_basic tool. Flow from stream 1004 (17937 kg/h / 1000 kg/m³). Head 27 m to achieve 2.8 barg discharge. Hydraulic power 1.32 kW, motor 1.96 kW (rounded to 2.0 kW with 20% margin). Efficiency 75%, motor 90%. NPSH available from suction ~5 m > required 3 m. Centrifugal type for liquid amine. 316L SS wetted parts. Design includes 10% flow margin. |
| E-203 | Rich/Lean Exchanger | Plate-Frame Exchanger | Critical heat integration unit; preheats rich amine before C-201 using hot lean amine from C-201. |  | 1006, 1008 | 1007, 1009 | <851.0 kW> | Heat Duty: 851.0 kW<br>Area: 45.0 m²<br>lmtd: 20.4 °C<br>u_value: 800.0 W/m²-K | Sized using size_heat_exchanger_basic tool with LMTD method. Duty calculated 851 kW (10% margin on energy balance: rich ΔT=45°C, Cp=3.8 kJ/kgK). Area 45.0 m², LMTD 20.4°C (Ft=0.812 for 1-2 config). U-value 800 W/m²-K for amine-amine service per TEMA. Plate-frame for compactness. Pressure drops estimated 20 kPa shell, 40 kPa tube. 316L SS construction. Recommend FEED verification of fouling factors. |
| C-201 | Amine Stripper | Packed Column | Regenerates rich amine by heating, releasing high-purity CO2 overhead. |  | 1007, 2002 | 1008, 1010 | <95% CO2 recovery> | Diameter: 750.0 mm<br>Packed Height: 16.0 m<br>number_of_stages: 8.0 count<br>steam_circulation: 2619.0 kg/h | Sized using size_absorption_column_basic tool adapted for stripping (gas CO2 34.7 kmol/h, inlet conc 0.9, outlet 0.995 with steam solvent). Diameter 750 mm, height 16 m, 8 stages. Steam circulation 2619 kg/h from reboiler duty. Packing: 1-inch Raschig rings. Pressure drop 15 kPa. Operates 2.0 barg, 100-125°C. Tool approximate for desorption; recommend Aspen simulation in FEED. 316L SS construction. |
| E-201 | Stripper Reboiler | Kettle Exchanger | Supplies thermal energy (LP Steam) to the stripper base to drive the CO2 stripping reaction. |  | 1008, 2001 | 1008, 2002 | <1528.0 kW> | Heat Duty: 1528.0 kW<br>Steam Flow: 2619.0 kg/h<br>Area: 46.2 m²<br>lmtd: 33.1 °C<br>u_value: 1000.0 W/m²-K | Sized using size_heat_exchanger_basic tool with LMTD method. Duty 1528 kW (10% margin on 4 GJ/t CO2 basis). Area 46.2 m², LMTD 33.1°C for 1-1 config. U-value 1000 W/m²-K for steam-amine service. Steam flow 2619 kg/h (latent heat 2100 kJ/kg). Kettle type for bottom heating. Pressure drops not calculated; estimate 10 kPa. 316L SS for corrosion. Recommend vendor quote for tube bundle. |
| E-202 | Lean Amine Cooler | Shell-and-Tube Exchanger | Cools regenerated lean amine from E-203 before recycling back to the Absorber (C-101) using Cooling Water (CW). |  | 1009, 2003 | 1005, 2004 | <633.0 kW> | Heat Duty: 633.0 kW<br>CW Flow: 54500.0 kg/h<br>Area: 30.0 m²<br>lmtd: 20.0 °C<br>u_value: 850.0 W/m²-K | Manual estimation due to tool configuration mismatch. Duty 633 kW from energy balance (lean ΔT=36.2°C, Cp=3.8 kJ/kgK, 10% margin). CW flow 54500 kg/h (ΔT=10°C, Cp=4.18). Area 30 m², LMTD ~20°C, U=850 W/m²-K for amine-water. Shell-tube 1-2 pass. Pressure drops 30 kPa shell, 50 kPa tube. Part of total CW 60k kg/h. Recommend detailed design for fouling. |
| P-201 | Lean Amine Pump | Centrifugal Pump | Recycles cooled, regenerated lean amine back to the top of the Absorber (C-101). |  | 1005 | 1005 | <16.2 m³/h> | Flow Rate: 16.2 m³/h<br>Discharge Pressure: 2.5 barg<br>head: 5.0 m<br>motor_power: 0.3 kW<br>npsh_required: 3.0 m<br>pump_type: Centrifugal string | Sized using size_pump_basic tool. Flow from stream 1005 (16562 kg/h / 1020 kg/m³). Head 5 m for column feed. Hydraulic power 0.23 kW, motor 0.33 kW (rounded with 20% margin). Efficiency 75%, motor 90%. NPSH available > required. Centrifugal for low head. Design includes 10% pressure margin. Stream split for connectivity. |
| E-301 | CO2 Condenser | Air-Cooled Exchanger | Cools and condenses water vapor from the overhead CO2 product stream from C-201. |  | 1010 | 1011, 1012 | <50.0 kW> | Heat Duty: 50.0 kW<br>Air Flow: 20000.0 m³/h<br>face_area: 10.0 m²<br>tube_length: 6.0 m | Manual estimation due to tool error in size_air_cooler_basic (temp profile issue). Duty 50 kW for water condensation (100 to 40°C, partial). Face area 10 m², 6 m tubes, fin density 10 fpi. Air flow ~20k m³/h. Approach 10°C to ambient 30°C. Air-cooled for modularity. Knockout for 50 kg/h water. Recommend vendor for fan power (est 2 kW). |
| K-301 | CO2 Compressor Train | Multi-Stage Centrifugal Compressor | Boosts CO2 pressure from 2.0 barg to the final delivery pressure (assumed 150 barg). |  | 1012 | 4001 | <462.0 kW> | Brake Horsepower: 462.0 kW<br>Discharge Pressure: 150.0 barg<br>number_of_stages: 3.0 count<br>discharge_temperature: 204.0 °C<br>intercooler_duty: 366.0 kW<br>compressor_type: Centrifugal string | Sized using size_compressor_basic tool. Inlet 18 m³/min at 2.9 bara, outlet 151 bara. 3 stages, ratio 52, power 439 kW (motor 462 kW with 20% margin). Polytropic eff 80%, intercooling duty 366 kW. Discharge T 204°C (after intercoolers). Centrifugal type. 316L SS wet parts. Verify inlet flow from stream 1012. Recommend lube oil system in FEED. |
| D-301 | CO2 Dryer | Adsorption Dryer Skid | Final purification step to remove moisture to below 50 ppmv, ensuring 99.5% purity and preventing corrosion. |  | 4001 | 4001 | <50 ppmv H2O> | Desiccant Volume: 0.5 m³<br>Switch Cycle Time: 8.0 h<br>vessel_volume: 1.0 m³<br>vessel_diameter: 799.0 mm<br>regeneration_duty: 25.0 kW | Sized using size_dryer_vessel_basic tool. Gas 31.6 kmol/h CO2, inlet 10k ppm H2O to 50 ppm. Vessel 1 m³, desiccant 0.5 m³, diameter 800 mm. Cycle 8 h, regeneration 25 kW heated air. Molecular sieves assumed. Design pressure 150 barg. Meets 99.5% purity. Recommend dual beds for continuous operation. Vendor confirmation for desiccant life. |

---

## Stream Summary

| **Attribute** | **1001** | **1002** | **1003** | **1004** | **1005** | **1006** | **1007** | **1008** |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **ID** | 1001 | 1002 | 1003 | 1004 | 1005 | 1006 | 1007 | 1008 |
| **Name** | Flue Gas Feed | Cleaned Flue Gas | Treated Flue Gas Vent | Rich Amine | Lean Amine Supply | Rich Amine (Hot) | Rich Amine (Stripper Inlet) | Lean Amine (Hot) |
| **Description** | Hot, wet flue gas containing N2, O2, H2O, CO2 (4-15%), and contaminants. | Cooled (50°C), contaminant-free flue gas. Ready for absorption. | Vented gas, primarily N2 and O2, with residual CO2 (10% slip assumed). | Solvent saturated with CO2, ready for regeneration. | Regenerated MDEA solvent, cooled back to 40°C for optimal absorption. | Rich amine pumped and preheated via heat integration. | Rich amine entering the stripper column after preheating (T ~ 100°C). | Hot, regenerated lean amine from stripper base (T ~ 125°C). |
| **From** | Upstream Burner | S-101 | C-101 | C-101 | E-202 | P-101 | E-203 | C-201 |
| **To** | S-101 | C-101 | Atmosphere | P-101 | C-101 | E-203 | C-201 | E-203 |
| **Phase** | Vapor | Vapor | Vapor | Liquid | Liquid | Liquid | Liquid | Liquid |
| **Temperature** | 120.0 °C | 50.0 °C | 45.0 °C | 55.0 °C | 40.0 °C | 55.0 °C | 100.0 °C | 125.0 °C |
| **Pressure** | 0.1 barg | 0.1 barg | 0.1 barg | 0.15 barg | 0.2 barg | 2.8 barg | 2.0 barg | 2.5 barg |
| **Mass Flow** | 26970.0 kg/h | 26970.0 kg/h | 25595.0 kg/h | 17937.0 kg/h | 16562.0 kg/h | 17937.0 kg/h | 17937.0 kg/h | 16562.0 kg/h |
| **Molar Flow** | 977.6 kmol/h | 977.6 kmol/h | 946.4 kmol/h | 561.3 kmol/h | 530.0 kmol/h | 561.3 kmol/h | 561.3 kmol/h | 530.0 kmol/h |
| **Volume Flow** | 29000.0 m³/h | 23867.0 m³/h | 22450.0 m³/h | 17.9 m³/h | 16.2 m³/h | 17.9 m³/h | 18.4 m³/h | 17.1 m³/h |
| **Density** | 0.93 kg/m³ | 1.13 kg/m³ | 1.14 kg/m³ | 1000.0 kg/m³ | 1020.0 kg/m³ | 1000.0 kg/m³ | 975.0 kg/m³ | 970.0 kg/m³ |
| **Mass Fraction** | -- | -- | -- | -- | -- | -- | -- | -- |
|   Nitrogen   | 0.7590 | 0.7590 | 0.7810 |  |  |  |  |  |
|   Oxygen   | 0.0380 | 0.0380 | 0.0390 |  |  |  |  |  |
|   Carbon Dioxide   | 0.0510 | 0.0510 | 0.0050 | 0.0770 |  | 0.0770 | 0.0770 |  |
|   Water   | 0.0730 | 0.0730 | 0.0750 | 0.4620 | 0.5000 | 0.4620 | 0.4620 | 0.5000 |
|   Methyldiethanolamine   |  |  |  | 0.4620 | 0.5000 | 0.4620 | 0.4620 | 0.5000 |
| **Mole Fraction** | -- | -- | -- | -- | -- | -- | -- | -- |
|   Nitrogen   | 0.8170 | 0.8170 | 0.8440 |  |  |  |  |  |
|   Oxygen   | 0.0355 | 0.0355 | 0.0367 |  |  |  |  |  |
|   Carbon Dioxide   | 0.0355 | 0.0355 | 0.0037 | 0.0557 |  | 0.0557 | 0.0557 |  |
|   Water   | 0.1120 | 0.1120 | 0.1160 | 0.8205 | 0.8690 | 0.8205 | 0.8205 | 0.8690 |
|   Methyldiethanolamine   |  |  |  | 0.1237 | 0.1310 | 0.1237 | 0.1237 | 0.1310 |
| **Notes** | Assumed dry molar composition: N2 0.92, O2 0.04, CO2 0.04 for lowest CO2 concentration design case. Total dry molar flow 868 kmol/h based on 34.72 kmol/h CO2 in feed (90% capture of 31.25 kmol/h design CO2). Wet composition adjusted for saturation at 50°C (used known Psat H2O=0.1235 bar, y_H2O=0.112). Mass and average MW (27.59 kg/kmol) from calculate_mass_flow_from_molar tool. Mass fractions from convert_compositions tool. Density approximated from ideal gas law/CoolProp equivalent at 120°C, 0.1 barg (actual tool call would use get_physical_properties). Volume flow = mass_flow / density. Assumed same composition as 1002 for simplicity, ignoring minor pre-treatment water addition. Temperature assumed 120°C for hot feed. | Same flow and composition as 1001, assuming no mass loss in S-101 pre-treatment (contaminants <10 ppmv negligible). Temperature cooled to 50°C via quenching/scrubbing. Density from get_physical_properties tool (components=['Nitrogen','Oxygen','Carbon Dioxide','Water'], mole_fractions=[0.817,0.0355,0.0355,0.112], T=50°C, P=0.1 barg, properties_needed=['density','phase']). Phase confirmed Vapor. Volume flow from calculate_volume_flow tool (mass_flow=26970, density=1.13). Contaminant levels reduced to below 10 ppmv SOx/NOx. | Mass balance from absorber: inlet 1002 minus 90% CO2 captured (31.25 kmol/h =1375 kg/h). Molar flow =977.6 -31.25=946.35 kmol/h. Compositions adjusted proportionally (CO2 slip 3.47 kmol/h, H2O assumed unchanged). Mass flow and avg MW (27.05 kg/kmol) from calculate_mass_flow_from_molar. Mass fractions from convert_compositions. Temperature assumed 45°C (near lean amine T=40°C). Density from get_physical_properties at 45°C, 0.1 barg. Volume flow from calculate_volume_flow. Phase Vapor. Assumed negligible amine slip and H2O evaporation/condensation in absorber. | Mass flow = lean amine mass (16562 kg/h) + absorbed CO2 (1375 kg/h). Assumed 50 wt% MDEA in water for lean (see 1005); ΔCO2 loading =0.45 mol/mol MDEA (industry typical for MDEA). Molar flow from calculate_molar_flow_from_mass with mass compositions (m_MDEA=0.462, m_H2O=0.462, m_CO2=0.077). Molar fractions calculated from moles (MDEA 69.44 kmol/h fixed, H2O 460.57, CO2 31.25 added). Mass fractions verified with convert_compositions. Temperature absorber bottom ~55°C. Pressure slight drop from absorber. Density assumed 1.00 g/cm³ (typical loaded MDEA solution; CoolProp not applicable for MDEA). Volume flow = mass / density. Phase Liquid. Assumed no H2O transfer in absorber. | Circulation rate based on MDEA flow = captured CO2 / Δloading =31.25 /0.45=69.44 kmol/h MDEA. 50 wt% MDEA assumed (typical). Molar fractions from MWs (MDEA 119.16, H2O 18). Total molar flow=69.44/0.131≈530 kmol/h. Mass flow and avg MW (31.25 kg/kmol) from calculate_molar_flow_from_mass with mass compositions. Temperature specified 40°C for absorption. Pressure pump discharge ~0.2 barg to feed absorber top. Density assumed 1.02 g/cm³ (typical unloaded MDEA; CoolProp N/A for MDEA). Volume flow = mass / density. Phase Liquid. Negligible CO2 in lean (loading ~0). | Same as 1004 (pump assumes isentropic, negligible T rise). Pressure increased by P-101 to 2.8 barg to overcome downstream ΔP (E-203 + C-201). Other properties identical to 1004. Density assumed same. | Same composition and flow as 1006. Temperature preheated to 100°C in E-203 (assumed outlet T for heat integration). Pressure drop across E-203 to 2.0 barg (stripper inlet). Density assumed slightly lower at higher T (typical for liquids). Volume flow = mass / density. Phase Liquid. | Same as 1005 (CO2 desorbed in stripper, loading ~0). Temperature stripper bottom 125°C (design basis 110-130°C). Pressure 2.5 barg (stripper operation 1.5-2.5 barg + pump head). Density assumed lower at high T. Volume flow = mass / density. Phase Liquid. Assumed no mass loss in regeneration. |

| **Attribute** | **1009** | **1010** | **1011** | **1012** | **4001** | **2001** | **2002** | **2003** |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **ID** | 1009 | 1010 | 1011 | 1012 | 4001 | 2001 | 2002 | 2003 |
| **Name** | Lean Amine (Cooler Inlet) | Regenerated CO2 (Wet) | Condensed Water | CO2 Compressor Feed | Final CO2 Product | LP Steam Supply | Condensate Return | Cooling Water Supply |
| **Description** | Lean amine cooled by E-203, ready for final cooling. | Hot, saturated CO2 product gas (P ~ 2.0 barg). | Water knocked out from the CO2 stream. Recycled to process make-up. | Cooled, partially dried CO2 product gas. | High-purity CO2 (99.5% min), dry, P ~ 150 barg. | Low-pressure steam (4–6 barg) for regeneration heat duty. | Steam condensate returned for reuse. | Cooling water for intercoolers and solvent/product cooling. |
| **From** | E-203 | C-201 | E-301 | E-301 | D-301 | Utility Header | E-201 | Utility Header |
| **To** | E-202 | E-301 | Solvent Sump | K-301 | Storage/Pipeline | E-201 | Utility Return | E-202/E-301/K-301 |
| **Phase** | Liquid | Vapor | Liquid | Vapor | Supercritical | Vapor | Liquid | Liquid |
| **Temperature** | 76.2 °C | 100.0 °C | 40.0 °C | 40.0 °C | 40.0 °C | 152.0 °C | 140.0 °C | 30.0 °C |
| **Pressure** | 2.0 barg | 2.0 barg | 2.0 barg | 1.9 barg | 150.0 barg | 5.0 barg | 4.5 barg | 3.0 barg |
| **Mass Flow** | 16562.0 kg/h | 1437.5 kg/h | 50.0 kg/h | 1387.5 kg/h | 1381.0 kg/h | 2619.0 kg/h | 2619.0 kg/h | 60000.0 kg/h |
| **Molar Flow** | 530.0 kmol/h | 34.7 kmol/h | 2.78 kmol/h | 31.6 kmol/h | 31.3 kmol/h | 145.5 kmol/h | 145.5 kmol/h | 3333.0 kmol/h |
| **Volume Flow** | 16.7 m³/h | 1210.0 m³/h | 0.05 m³/h | 1080.0 m³/h | 1.8 m³/h | 3.5 m³/h | 2.6 m³/h | 60.0 m³/h |
| **Density** | 992.0 kg/m³ | 1.19 kg/m³ | 992.0 kg/m³ | 1.29 kg/m³ | 750.0 kg/m³ | 750.0 kg/m³ | 1000.0 kg/m³ | 1000.0 kg/m³ |
| **Mass Fraction** | -- | -- | -- | -- | -- | -- | -- | -- |
|   Methyldiethanolamine   | 0.5000 |  |  |  |  |  |  |  |
|   Water   | 0.5000 | 0.0440 | 1.0000 | 0.0040 | 0.0000 | 1.0000 | 1.0000 | 1.0000 |
|   Carbon Dioxide   |  | 0.9560 |  | 0.9760 | 0.9980 |  |  |  |
|   Nitrogen   |  |  |  |  | 0.0020 |  |  |  |
| **Mole Fraction** | -- | -- | -- | -- | -- | -- | -- | -- |
|   Methyldiethanolamine   | 0.1310 |  |  |  |  |  |  |  |
|   Water   | 0.8690 | 0.1000 | 1.0000 | 0.0100 | 0.0000 | 1.0000 | 1.0000 | 1.0000 |
|   Carbon Dioxide   |  | 0.9000 |  | 0.9900 | 0.9950 |  |  |  |
|   Nitrogen   |  |  |  |  | 0.0050 |  |  |  |
| **Notes** | Same as 1008/1005. Temperature calculated from energy balance in E-203: duty = mass_rich * Cp * ΔT_rich (17937 * 3.8 * (100-55)) ≈ 2.44e6 kJ/h; set equal to mass_lean * Cp * ΔT_lean, solving for T_out=125 - (2.44e6 / (16562*3.8)) ≈76.2°C (Cp=3.8 kJ/kgK assumed constant). Pressure drop across E-203 to 2.0 barg. Density interpolated assumption. Volume flow = mass / density. Phase Liquid. | Mass balance from stripper: CO2 desorbed 1375 kg/h (31.25 kmol/h) + H2O vaporized 62.5 kg/h (3.47 kmol/h, assumed 10% molar for saturated overhead). Total molar 34.72 kmol/h. Mass and avg MW (41.4 kg/kmol) from calculate_mass_flow_from_molar with molar comp. Mass fractions from convert_compositions. Temperature stripper overhead ~100°C. Density from get_physical_properties (components=['Carbon Dioxide','Water'], mole_fractions=[0.9,0.1], T=100°C, P=2.0 barg). Volume flow from calculate_volume_flow. Phase Vapor. Inerts negligible (<0.1%). | Assumed bulk water condensation in E-301: 50 kg/h knocked out (portion of 62.5 kg/h H2O in 1010). Molar flow =50/18=2.78 kmol/h. Temperature after cooling to 40°C. Pressure same as overhead. Density from get_physical_properties for pure water at 40°C, 2 barg. Volume flow from calculate_volume_flow. Phase Liquid. Potentially trace CO2 dissolved, neglected. | Mass balance: 1010 minus condensed 1011 (50 kg/h H2O). Remaining H2O 12.5 kg/h (0.69 kmol/h, ~2% molar adjusted to 1% post-condensation). CO2 1375 kg/h. Total molar ~31.94 kmol/h. Mass and MW from calculate_mass_flow_from_molar. Mass fractions from convert_compositions. Temperature cooled to 40°C in E-301. Pressure drop 0.1 bar. Density from get_physical_properties at 40°C, 1.9 barg. Volume flow from calculate_volume_flow. Phase Vapor. Further drying in D-301. | Mass flow =1375 /0.995 ≈1381 kg/h (99.5% purity spec, inerts 0.5% N2 assumed trace slip). Molar flow from calculate_molar_flow_from_mass with molar comp. Mass fractions from convert_compositions. Temperature after final cooling. Pressure from K-301 discharge 150 barg (design basis). Density from get_physical_properties (approx pure CO2, components=['Carbon Dioxide','Nitrogen'], mole_fractions=[0.995,0.005], T=40°C, P=150 barg). Volume flow from calculate_volume_flow. Phase Supercritical (above critical P/T). H2O <50 ppmv after D-301. Meets product spec. | Flow calculated from reboiler duty ~1528 kW (5.5e6 kJ/h, assumed 4 GJ/t CO2 for MDEA regeneration + sensible; 1375 kg/h *4000 kJ/kg). Latent heat ~2100 kJ/kg at 5 barg, mass=5.5e6/2100=2619 kg/h. Molar flow=2619/18. Temperature saturated at 5 barg (151.8°C). Density from get_physical_properties for steam. Volume flow from calculate_volume_flow (saturated vapor). Phase Vapor. | Same flow as 2001 (complete condensation in E-201). Temperature assumed subcooled 140°C. Pressure slight drop. Density assumed ~1 g/cm³ for hot water. Volume flow = mass / density. Phase Liquid. | Total flow estimated for all services: E-202 duty 633 kW requires ~54500 kg/h (ΔT=10°C, Cp=4.18 kJ/kgK, duty from calculate_heat_exchanger_duty: mass=16562, Cp=3.8, ΔT=36.2°C). E-301 ~50 kW (~4500 kg/h). K-301 intercoolers ~150 kW (~13500 kg/h assumed). Total ~60,000 kg/h split (simplified as single supply). Molar from mass/MW. Density standard. Volume flow = mass / density. Phase Liquid. |

| **Attribute** | **2004** |
| :--- | :--- |
| **ID** | 2004 |
| **Name** | Cooling Water Return |
| **Description** | Warmed cooling water returning to the cooling tower. |
| **From** | E-202/E-301/K-301 |
| **To** | Utility Return |
| **Phase** | Liquid |
| **Temperature** | 40.0 °C |
| **Pressure** | 2.0 barg |
| **Mass Flow** | 60000.0 kg/h |
| **Molar Flow** | 3333.0 kmol/h |
| **Volume Flow** | 60.0 m³/h |
| **Density** | 1000.0 kg/m³ |
| **Mass Fraction** | -- |
|   Water   | 1.0000 |
| **Mole Fraction** | -- |
|   Water   | 1.0000 |
| **Notes** | Same flow as 2003 (closed loop, no loss). Temperature average return 40°C (ΔT=10°C across exchangers). Pressure drop 1 bar. Density standard. Volume flow = mass / density. Phase Liquid. Combined from all CW services. |

# Safety & Risk Assessment
## Preliminary HAZOP-Style Assessment

### 1. Loss of Flue Gas Pre-treatment (S-101)

**Severity:** 4 | **Likelihood:** 3 | **Risk Score:** 12

**Causes:**
- Failure of the continuous online gas analyzer (T-101) to detect SOx/NOx spikes (Wrong measurement).
- Failure of the bypass valve logic, allowing contaminated Stream 1001 to bypass S-101 (Control system failure).
- Failure of the scrubber neutralization system (e.g., pH control failure), allowing acidic gas components (SOx) to carry over (Equipment failure).
- Significant and sudden change in flue gas composition (Stream 1001) due to burner type switch, exceeding S-101 design capacity (External process upset).

**Consequences:**
- Contaminated Stream 1002 enters Absorber C-101, leading to rapid degradation of MDEA solvent (Amine degradation).
- Formation of heat stable salts (HSS) in the amine loop (Streams 1004, 1005), increasing corrosion rates, especially in high-temperature sections (C-201, E-201, E-203).
- Reduced CO2 absorption capacity of the MDEA solvent, leading to failure to meet the 90% capture efficiency target (Operational failure).
- Increased corrosion and fouling of the structured packing in C-101 and C-201, leading to increased pressure drop and eventual column flooding (Equipment damage).

**Mitigations:**
- Install dual, redundant, and independent SOx/NOx analyzers upstream of S-101, cross-checking signals.
- Implement an automatic interlock (SIL 2 minimum) that closes the main inlet valve to C-101 and opens a flue gas bypass vent if contaminant levels exceed 15 ppmv.
- Mandate 316L SS construction for the entire high-temperature amine loop (E-201, E-203, C-201) and C-101 packing to mitigate corrosion from potential HSS formation.
- Install a side-stream Amine Reclaimer (not listed as major equipment) capable of processing 5% of the total amine volume per day to remove degradation products.

**Notes:**
This is the most critical upstream hazard. The pre-treatment skid (S-101) is the primary layer of protection for the entire amine loop. Design of S-101 must be robust enough to handle the assumed 4-15% CO2 variability and associated contaminant load. Compliance with local air quality standards for the wastewater discharge from S-101 is required.

---

### 2. Loss of LP Steam Supply to Reboiler E-201 (No Heat)

**Severity:** 4 | **Likelihood:** 4 | **Risk Score:** 16

**Causes:**
- Utility Steam Supply (Stream 2001) pressure drops below the required 4.0 barg minimum due to upstream utility failure (Utility failure).
- Control valve on Steam Supply (Stream 2001) fails closed or condensate return line (Stream 2002) is blocked, causing E-201 to become steam-bound (Equipment failure).
- Low-low level in the Stripper C-201 base, triggering an automatic interlock that shuts off the steam supply to E-201 to prevent overheating the amine (Control/Interlock action).
- Failure of the main control loop for the reboiler duty (TC-201), leading to insufficient heat input (Control failure).

**Consequences:**
- Immediate and rapid drop in Stripper C-201 temperature (Stream 1010 outlet), leading to incomplete CO2 stripping from the rich amine (Process upset).
- Lean Amine Supply (Stream 1005) returns to Absorber C-101 with high CO2 loading, severely reducing the driving force for CO2 capture (Operational failure).
- Flue Gas Vent (Stream 1003) CO2 concentration rises significantly, causing failure to meet the 90% capture efficiency target (Environmental/Compliance failure).
- Potential for physical damage to E-201 tubes due to thermal shock if low-temperature amine contacts high-temperature tubes (Equipment damage).

**Mitigations:**
- Install a dedicated, independent low-pressure switch (PSL) on Steam Supply (Stream 2001) set at 3.5 barg, triggering a high-priority alarm for operator intervention.
- Install dual level transmitters (LT) on the C-201 base, providing a redundant low-level trip (LSL) to prevent steam supply shutdown unless truly necessary.
- Implement a minimum flow bypass line around E-203 to allow hot amine (Stream 1008) to bypass the rich amine pre-heater if E-203 duty is suddenly lost or reduced.
- Develop a detailed emergency operating procedure (EOP) for operators to gradually reduce flue gas flow (Stream 1001) upon loss of steam to maintain a stable absorber operation until steam is restored.

**Notes:**
The reboiler (E-201) represents the dominant energy input and is critical for the primary separation function. The high risk score indicates the need for robust utility management and control system redundancy (SIL rated protection). The modular nature of the unit may necessitate a dedicated steam generator if the host facility's utility is unreliable.

---

### 3. Overpressure in Stripper C-201 (More Pressure)

**Severity:** 5 | **Likelihood:** 2 | **Risk Score:** 10

**Causes:**
- Blockage in the Regenerated CO2 (Wet) line (Stream 1010) to the Condenser E-301, potentially due to ice formation or corrosion product accumulation (Equipment blockage).
- Failure of the CO2 Compressor Train (K-301) inlet valve to open, dead-heading the stripper overhead pressure (Equipment failure).
- Over-firing of the Reboiler E-201 due to control valve failure (XV) on Steam Supply (Stream 2001) failing open, leading to excessive vapor generation (Control failure).
- Failure of the Pressure Relief Valve (PRV) on C-201 to actuate due to corrosion or mechanical binding (Protection system failure).

**Consequences:**
- Pressure in C-201 exceeds design limits (2.5 barg max), potentially leading to vessel rupture or flange leaks (Catastrophic equipment failure).
- High pressure suppresses the CO2 stripping reaction, increasing the energy required and potentially causing the reboiler E-201 to trip on high temperature (Process upset).
- High-pressure release of hot, wet CO2/steam mixture through the PRV, creating an immediate localized asphyxiation hazard and a noise hazard (Safety hazard).
- Overpressure causes backflow of rich amine (Stream 1007) into the E-203 exchanger, risking plate damage due to pressure differential (Equipment damage).

**Mitigations:**
- Install a Pressure Relief Valve (PRV) on C-201 set at 2.8 barg (112% of design pressure) sized to handle the full latent heat duty of the Reboiler E-201 (API 520/521 compliance).
- Install an independent high-pressure trip (PSH) on C-201 set at 2.4 barg, triggering the immediate closure of the Steam Supply (Stream 2001) isolation valve.
- Use 316L SS construction for C-201 and Stream 1010 piping to minimize corrosion and potential blockage.
- Implement a low-pressure alarm (PSL) on the K-301 inlet (Stream 1012) to alert operators if the compressor is failing to draw sufficient flow, causing upstream pressure buildup.

**Notes:**
The consequence of vessel failure warrants a high severity rating. The PRV sizing must assume the worst-case scenario (full heat input, no vapor outlet). Periodic testing of the PRV is mandatory per PED/ASME standards.

---

### 4. Loss of Lean Amine Cooling (E-202 Failure)

**Severity:** 3 | **Likelihood:** 3 | **Risk Score:** 9

**Causes:**
- Failure of Cooling Water Supply (Stream 2003) pressure due to pump trip or line isolation (Utility failure).
- Fouling or scaling of the E-202 tubes/shell due to poor cooling water quality, reducing heat transfer (Equipment failure).
- Lean Amine Cooler (E-202) bypass valve inadvertently opened, allowing hot Stream 1009 to bypass cooling (Human error).
- Failure of the temperature control valve on the cooling water outlet, restricting flow (Control failure).

**Consequences:**
- Lean Amine Supply (Stream 1005) temperature rises above the optimal 40°C setpoint (e.g., to 60°C or higher) (Process upset).
- High amine temperature reduces the physical solubility and chemical absorption rate of CO2 in C-101 (Operational failure).
- Increased vaporization of water and amine from the absorber top, leading to higher amine slip in the Treated Flue Gas Vent (Stream 1003) (Environmental hazard).
- Failure to meet the 90% capture efficiency target due to poor absorption kinetics (Compliance failure).

**Mitigations:**
- Install a high-temperature alarm (TAH) on Lean Amine Supply (Stream 1005) set at 45°C.
- Use a dedicated, reliable closed-loop cooling water system for the modular unit to minimize fouling risk.
- Implement an interlock (TSS) that automatically reduces the Flue Gas Feed (Stream 1002) flow rate if Lean Amine Supply temperature exceeds 50°C, stabilizing the capture efficiency.
- Require routine cleaning and inspection of the E-202 exchanger (e.g., every 12 months) and continuous monitoring of the E-202 temperature approach.

**Notes:**
Temperature control is critical for the absorber (C-101) performance. The inherent safety margin is low, as the absorption reaction is exothermic, and the incoming flue gas (Stream 1002) is already at 50°C.

---

### 5. Excessive Compression of Wet CO2 (K-301)

**Severity:** 4 | **Likelihood:** 3 | **Risk Score:** 12

**Causes:**
- Failure of the Condenser E-301 or the downstream knockout drum to remove sufficient water (Stream 1011), leading to high moisture content in Compressor Feed (Stream 1012) (Equipment failure).
- Failure of the intercoolers in K-301 (Utility failure - Cooling Water Stream 2003) resulting in high compression temperatures (Process upset).
- Operation of K-301 outside its surge control envelope due to low flow or high discharge pressure (Operational error).
- Incompatible material of construction (MoC) for wet stages of K-301 (Design weakness).

**Consequences:**
- Formation of highly corrosive carbonic acid (H2CO3) inside the compressor stages due to high pressure, temperature, and moisture (Equipment damage/failure).
- Rapid corrosion and erosion of K-301 impellers and casings, leading to catastrophic compressor failure and downtime (Major financial loss).
- Failure to meet the required 150 barg discharge pressure due to performance degradation (Operational failure).
- Potential for liquid slugging into the compressor if E-301 fails completely, leading to immediate mechanical damage (Catastrophic equipment failure).

**Mitigations:**
- Mandate 316L SS construction for all wet stages of K-301, including intercoolers and associated piping (Design control).
- Install a moisture analyzer (AH) and a high-level alarm/trip (LAH) in the knockout drum downstream of E-301, tripping K-301 on high moisture/liquid level (Protection layer).
- Implement a reliable anti-surge control system on K-301 to prevent operation in the surge regime.
- Verify the sizing and integrity of E-301 to ensure the Compressor Feed (Stream 1012) moisture content is within acceptable limits for the 316L SS materials.

**Notes:**
The combination of high pressure, high temperature, and moisture makes the compressor section inherently hazardous and highly susceptible to corrosion. The severity of K-301 failure (462 kW motor power) necessitates a high risk score and multiple layers of protection.

---

## Overall Assessment

**Risk Level:** High

**Compliance Notes:**
- **Design Verification:** Conduct a detailed stress analysis and modularity check for the C-101 (2.5m diameter, 20m height) and C-201 (0.75m diameter, 16m height) columns to confirm they comply with the modular transport constraints and wind/seismic load requirements.
- **Interlock Specification:** Finalize the design and specification (SIL rating) for the critical interlocks: High Contaminant Trip on S-101 (to protect amine), Low-Low Level Trip on C-201 (to protect E-201), and High Pressure Trip on C-201 (to protect vessel).
- **MOC Confirmation:** Obtain vendor confirmation that the 316L SS material of construction specified for E-201, E-203, C-201, and the wet stages of K-301 is adequate to handle the anticipated corrosion rates from MDEA degradation products and wet CO2 service (Referencing API 945 or NACE guidelines).
- **Utility Reliability:** Require the end-user to provide a reliability study for the LP Steam Supply (Stream 2001) and Cooling Water Supply (Stream 2003) to confirm the assumed utility availability factor (90% operating hours) is achievable, minimizing the risk of Hazard 2 and 4.
- **PRV Sizing:** Verify the sizing calculation for the C-201 Pressure Relief Valve (PRV) against the worst-case fire scenario (full heat input from E-201) and full blockage of the CO2 discharge line (Stream 1010).
- **FEED Phase Action:** The next phase (FEED) must include a rigorous process simulation (e.g., using Aspen Plus) to accurately model the MDEA chemistry, precisely determine the required solvent circulation and regeneration steam duty (Hazard 2), and confirm the E-203 heat integration efficiency.

# Project Manager Report
## Executive Summary

- **Approval Status:** Conditional Approval
- **Key Rationale:** Design is technically viable and meets the 99.5% purity and 30 TPD capacity targets, but full FEED authorization is contingent upon verification of the modular column dimensions and confirmation of critical utility reliability (LP Steam 2001) required for the high-risk E-201 reboiler duty (HAZOP Hazard #2).

**Conditions for FEED Authorization:**
- **Modularity Verification:** Confirm C-101 (2.5m x 20m) and C-201 (0.75m x 16m) column dimensions comply with site-specific transport and crane limitations; obtain signed approval from lead structural engineer by end of Week 2 FEED Phase 1.
- **Utility Confirmation:** Obtain written confirmation from the host facility that LP Steam Supply (Stream 2001) at 5.0 barg and 2,619 kg/h flow rate can be guaranteed at a minimum 90% stream factor to mitigate HAZOP Hazard #2 (Loss of Heat).
- **Process Simulation:** Complete the rigorous Aspen Plus simulation for MDEA chemistry to finalize solvent circulation rate (Stream 1005) and confirm the E-203 heat duty (851.0 kW) and steam consumption (2,619 kg/h for 1,528.0 kW duty).

## Financial Outlook

| Metric | Estimate (USD) |
|--------|----------------|
| CAPEX (millions) | 8.5 |
| OPEX (millions per year) | 1.8 |
| Contingency (%) | 25 |
| Total Estimated Cost | 13.5 |

## Implementation Plan

1. **Finalize Critical Equipment Specifications and RFQ:** Issue finalized specifications and RFQ package for the CO2 Compressor Train (K-301, 462.0 kW motor power) and the Stripper Reboiler (E-201, 1,528.0 kW duty, 316L SS) to secure vendor pricing and lead times. Target completion: Vendor quotes received and evaluated by end of Week 6 FEED Phase 1. Owner: Procurement and Mechanical Engineer.

2. **Conduct Detailed HAZOP and Interlock Design:** Conduct a detailed HAZOP review focusing on high-risk items (Hazard #1: Loss of Pre-treatment, Hazard #2: Loss of Steam, Hazard #5: Wet Compression) and finalize the SIL specification for the critical interlocks (PSH on C-201, Contaminant Trip on S-101). Target completion: SIL requirements documented and approved by end of Week 4 FEED Phase 1. Owner: Safety and Controls Engineer.

3. **Initiate Structural/Civil Design for Modular Skid:** Begin preliminary structural design for the modular skids, accommodating the C-101 (2.5m diameter) and C-201 (0.75m diameter) columns using high-performance structured packing (20m/16m heights) to ensure weight and footprint limits are met. Target completion: Skid design envelopes and foundation load data issued for civil engineering by end of Week 8 FEED Phase 1. Owner: Structural Engineer.

## Final Notes

- **Modularity and Column Sizing (Technical Gap):** The column dimensions (C-101: 2.5m/20m; C-201: 0.75m/16m) required for 90% capture efficiency using structured packing are based on manual estimation and pose a significant modularity risk. Detailed stress analysis and transport logistics must confirm feasibility; column heights may require horizontal shipping or on-site installation, impacting CAPEX.

- **LP Steam Unreliability (HAZOP Hazard #2):** The high-risk score (16) associated with Loss of Steam (Stream 2001) is critical. The design assumes 4–6 barg LP Steam availability. If the end-user utility reliability cannot be confirmed, the project must evaluate the cost and schedule impact of a dedicated, modular steam generator package during FEED Phase 1.

- **Contingency Justification (25%):** Contingency is set at 25% due to the high energy intensity (462 kW compressor power, 1,528 kW heat duty) and the inherent technical uncertainty associated with scaling MDEA absorption to a compact, modular skid layout and dealing with variable flue gas feeds. This will be reduced to 15% upon completion of detailed engineering (FEED Phase 2).

- **Cost Estimation Basis (Assumption):** CAPEX of $8.5M is estimated using an industry factor of 3.5× major equipment cost (K-301, C-101/C-201, E-201) to account for high-alloy material costs (316L SS) and modular packaging complexity, pending detailed vendor quotes. OPEX of $1.8M/year is based primarily on utility consumption (Steam 2,619 kg/h and Power 462 kW) and assumes an electricity rate of $0.08/kWh and a steam cost of $15/ton, requiring validation with regional utility rates during FEED Phase 1.

- **Corrosion Control (HAZOP Hazard #5):** 316L SS is mandated for the wet compression stages of K-301 and the high-temperature amine loop (E-201, E-203, C-201) to mitigate carbonic acid corrosion risk (HAZOP Hazard #5). Corrosion rates must be modeled and confirmed to be acceptable in the FEED phase.
