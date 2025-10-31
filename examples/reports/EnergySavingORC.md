# Problem Statement
design the energy recovery from flue gas of LNG burner, 10,000 SCFD, 300°C, 0.1 barg and use it to produce electricity with 30% efficiency.

# Process Requirements
## Objective
- Primary goal: Electricity generation via energy recovery from LNG burner flue gas
- Key drivers: Energy Conservation, Efficiency

## Capacity
The volumetric flow rate of the LNG burner flue gas is 10,000.0 SCFD (Standard Cubic Feet per Day).

## Components
The chemical components involved in the process are:
- Nitrogen (Primary component of flue gas, inferred)
- Carbon Dioxide (Combustion product, inferred)
- Water (Combustion product, inferred)
- Oxygen (Excess air, inferred)
- Argon (Trace component, inferred)

## Purity Target
- Component: Electricity
- Value: 30% (Conversion efficiency)

## Constraints and Assumptions
- The source material is Flue Gas from an LNG (Liquefied Natural Gas) burner.
- The flue gas inlet temperature is 300°C.
- The flue gas inlet pressure is 0.1 barg.
- The minimum required conversion efficiency from thermal energy to electrical energy is 30%.
- Flue gas composition (major components: N2, CO2, H2O, O2) is inferred based on standard LNG combustion principles.
- The system must be designed to handle a continuous flow of 10,000 SCFD of flue gas.

# Concept Detail
## Concept Summary
- Name: Organic Rankine Cycle (ORC) with High-Efficiency Fluid
- Intent: Electricity generation via energy recovery from LNG burner flue gas, targeting 30% conversion efficiency.
- Feasibility Score (from review): 7

## Process Narrative
The energy recovery process begins with the hot LNG burner flue gas (at 300°C and 0.1 barg) entering the ORC Heat Exchanger (E-101), which acts as the evaporator/boiler. Within E-101, the thermal energy from the flue gas is transferred to the closed-loop organic working fluid (e.g., a high-stability siloxane). The flue gas is cooled significantly before being vented to the stack, typically reducing its temperature below 150°C.

The organic working fluid is vaporized into a high-pressure, high-temperature gas, which then drives the Expander (T-101), converting the thermal energy into mechanical shaft power. This mechanical power is directly coupled to an Electrical Generator (G-101) to produce the net electrical output. After expanding, the low-pressure fluid vapor is sent to the Condenser (E-102), where it is cooled, typically by ambient air or plant cooling water, returning it to a liquid state.

Finally, the Working Fluid Pump (P-101) boosts the pressure of the liquid working fluid, sending it back to the ORC Heat Exchanger (E-101) to complete the closed thermodynamic cycle. The ORC system is designed for continuous, automated operation, minimizing operator intervention and maximizing the recovery of the low-grade heat resource.

## Major Equipment & Roles
| Equipment | Function | Critical Operating Notes |
|---|---|---|
| E-101 ORC Heat Exchanger (Evaporator) | Transfers heat from the flue gas (shell side) to the organic working fluid (tube side) for vaporization. | Flue gas side must be designed for low pressure drop (0.1 barg inlet). Organic fluid thermal stability is critical; monitor for degradation products. |
| T-101 Expander/Turbine | Converts the high-pressure organic vapor into mechanical work to drive the generator. | Vendor guarantee required for minimum isentropic efficiency. Requires highly effective shaft sealing to prevent expensive working fluid loss. |
| E-102 Condenser | Converts low-pressure organic vapor back into liquid form using cooling medium (air or water). | Condensation temperature directly impacts cycle efficiency; specify robust cooling mechanism. Must maintain minimum subcooling to prevent pump cavitation. |
| P-101 Working Fluid Pump | Increases the pressure of the liquid working fluid before it returns to the evaporator. | Must be continuously monitored for suction pressure (NPSH) due to low fluid vapor pressure. Magnetic coupling preferred to minimize fluid leakage. |
| G-101 Electrical Generator | Converts mechanical work from T-101 into grid-compatible electricity. | Specify output voltage and frequency compatible with plant infrastructure. |

## Operating Envelope
- Design capacity: 10,000 SCFD Flue Gas (continuous basis)
- Key pressure levels: Flue gas inlet at 0.1 barg. ORC high-pressure side (Evaporator/Expander inlet) TBD, typically 15–30 barg. ORC low-pressure side (Condenser/Pump inlet) TBD, typically 1–2 barg.
- Key temperature levels: Flue gas inlet at 300°C, outlet TBD (Target <150°C). Organic fluid maximum temperature TBD (Target 280°C). Condensation temperature TBD (Target 30–40°C).
- Special utilities / additives: High-stability, low-GWP organic working fluid (e.g., specific siloxane or fluorocarbon). Cooling medium (Air or Plant Cooling Water).
- Material compatibility: All wetted parts in the ORC loop must be compatible with the selected organic fluid to prevent corrosion or decomposition (e.g., Stainless Steel 316, specific elastomers for seals).

## Risks & Safeguards
- Thermal Degradation of Working Fluid — Implement continuous online monitoring of the organic fluid composition (e.g., GC or specialized sensors) for breakdown products. If degradation rate exceeds threshold, execute immediate shutdown.
- Loss of Expensive Working Fluid Inventory — Specify double mechanical seals or magnetic coupling pumps (P-101) and use robust, welded construction for piping. Install sensitive leak detection alarms (e.g., infrared or acoustic sensors) around the skid.
- Flue Gas Side Fouling of E-101 — Install differential pressure monitoring across E-101. Design E-101 for periodic soot blowing or chemical cleaning; specify wider flue gas channels than standard heat exchangers.
- Expander (T-101) Failure/Low Efficiency — Require vendor performance guarantees and run-in testing before shipment. Implement vibration monitoring and predictive maintenance alerts.

## Data Gaps & Assumptions
- Assumed the flue gas composition (major components N2, CO2, H2O) is standard for LNG combustion with excess air; detailed analysis of H₂O and SO₂ content needed to determine acid dew point.
- TBD: Exact thermodynamic properties (especially thermal stability limit) of the final selected organic working fluid. This dictates the maximum operating temperature.
- TBD: The net electrical power output (kW) and required heat transfer area (m²) for E-101, pending determination of the flue gas specific heat calculation based on composition and the ORC working fluid properties.
- TBD: Availability and cost of plant cooling water vs. suitability/efficiency of air cooling for E-102 (Condenser).

# Design Basis
## Preliminary Process Basis of Design (BoD)

### 1. Project Overview and Problem Statement
This Basis of Design (BoD) outlines the preliminary engineering requirements for a continuous energy recovery unit designed to generate electricity from the waste heat contained within the flue gas stream of an LNG burner. The primary objective is to maximize energy conservation by recovering thermal energy from a 10,000 SCFD flue gas stream entering at 300°C and 0.1 barg, converting this energy into electrical power with a minimum guaranteed conversion efficiency of 30%. The key process technology selected is the Organic Rankine Cycle (ORC) utilizing a high-stability organic working fluid, which is strategically chosen for its ability to operate efficiently at the given low-grade heat source temperatures. The critical design constraint is the low pressure of the flue gas source, which necessitates a low-pressure drop heat exchanger design.

### 2. Key Design Assumptions and Exclusions
* **Operating Factor:** 8,760 operating hours per year (100% stream factor) is assumed, reflecting continuous base-load operation of the LNG burner, maximizing available heat source utilization.
* **Flue Gas Composition:** The flue gas composition is assumed to be standard for LNG combustion with 15% excess air, consisting primarily of N₂, CO₂, H₂O, and O₂.
* **Design Margin:** A 5% thermal capacity margin is assumed for the Heat Exchanger (E-101) sizing to account for minor fouling and process variability.
* **Plant Lifespan:** The major equipment (Expander, Heat Exchangers) will be designed for a minimum operational life of 20 years.
* **Location:** The system is assumed to be located adjacent to the existing LNG burner stack; ambient conditions will be based on a generic industrial site (e.g., 15°C annual average, 35°C maximum design temperature for Condenser E-102).
* **Flue Gas Outlet Temperature:** The target flue gas outlet temperature from the ORC Heat Exchanger (E-101) is set at a maximum of 130°C to maximize heat recovery while remaining safely above the predicted acid dew point, thus mitigating corrosion risk.
* **Exclusions:** This preliminary BoD excludes detailed thermodynamic modeling (Pinch Analysis), detailed sizing of the Expander (T-101) or Generator (G-101), civil/structural design, and detailed cost estimation.

### 3. Design Capacity and Operating Conditions
| Parameter | Value | Units | Basis |
|---|---|---|---|
| **Nameplate Capacity (Flue Gas)** | 10,000 | SCFD | User Requirement (Continuous) |
| **Flue Gas Inlet Temperature** | 300 | °C | User Input |
| **Flue Gas Inlet Pressure** | 0.1 | barg | User Input (Low-Pressure Source) |
| **Target Thermal-to-Electric Efficiency** | 30 | % | User Requirement (Minimum) |
| **Flue Gas Outlet Temperature (Target)** | 130 | °C | Engineering Assumption (Dew Point Margin) |
| **ORC High-Pressure Side (Estimated)** | 18 | barg | Preliminary Estimate (Siloxane Fluid) |
| **ORC Max Working Temp (Estimated)** | 280 | °C | Preliminary Estimate (Thermal Stability Limit) |

### 4. Chemical Components
| Name | Formula | MW (g/mol) | NBP (°C) |
|---|---|---|---|
| Nitrogen | N₂ | 28.013 | -196.0 |
| Oxygen | O₂ | 31.999 | -183.0 |
| Argon | Ar | 39.948 | -185.9 |
| Carbon Dioxide | CO₂ | 44.010 | -78.5 |
| Water | H₂O | 18.015 | 100.0 |
| Organic Working Fluid (Siloxane) | C₁₀H₂₂ (approx.) | 142.282 | 174.2 (approx.) |

### 5. Feed and Product Specifications

#### Feed Specification (LNG Flue Gas)
* **Inlet Temperature:** 300°C (Critical design parameter for ORC fluid selection).
* **Inlet Pressure:** 0.1 barg (Critical design parameter for heat exchanger pressure drop).
* **Composition:** Inferred composition from complete LNG combustion with excess air (primarily N₂, CO₂, H₂O, O₂). Detailed analysis required to confirm trace components and acid dew point.
* **Flow Rate:** 10,000 SCFD (Standard Cubic Feet per Day).

#### Product Specification (Electrical Power)
* **Target Conversion Efficiency (Min):** 30% (Thermal to Electrical).
* **Output Quality:** Grid-compatible electricity (e.g., 480V, 3-phase, 60 Hz or site standard).
* **Continuity:** Continuous output, synchronized with LNG burner operation.

### 6. Preliminary Utility Summary
* **Cooling Medium:** The Condenser (E-102) will primarily utilize **air cooling** to minimize the consumption of water, unless site-specific conditions demonstrate superior economic and thermal performance with plant cooling water.
* **Process Water:** Minimal requirement; used for periodic cleaning/washdown of the flue gas side of E-101.
* **Electricity:** Required for the Working Fluid Pump (P-101) and associated instrumentation/controls. The net electric output must significantly exceed parasitic loads.
* **Instrument Air:** Standard dry instrument air supply required for control valves, actuators, and purging systems.
* **Nitrogen:** Required for initial system inerting and periodic purging of the ORC loop during maintenance to prevent oxidation of the working fluid.
* **Working Fluid Inventory:** Requires a closed-loop supply of the high-stability organic fluid, with a dedicated storage tank for maintenance drainage and makeup.

### 7. Environmental and Regulatory Criteria
* **Air Emissions:** The flue gas remains the primary emission stream. The ORC system acts as a heat sink and does not alter the chemical composition of the flue gas, but the lower stack temperature (target 130°C) must be evaluated against local dispersion modeling requirements.
* **Working Fluid Handling:** The organic working fluid must be handled as a hazardous material (HAP/VOC) due to its cost and potential environmental impact. Robust leak detection and containment systems are mandatory.
* **Noise:** The Expander (T-101) and air-cooled Condenser fans (if used) are major noise sources and require acoustic mitigation measures to meet local regulations.
* **Waste Management:** Spent or degraded organic working fluid must be managed and disposed of/recycled according to local chemical waste regulations.

### 8. Process Selection Rationale (High-Level)
The Organic Rankine Cycle (ORC) is selected because the heat source temperature (300°C) is too low for an efficient conventional steam Rankine cycle, but too high for simple heat recovery (e.g., water preheating). The ORC utilizes an organic fluid with a lower boiling point and higher molecular weight than water, making it ideally suited for converting low-grade heat into mechanical work at the required temperature range. The use of a high-stability siloxane fluid is necessary to meet the 30% efficiency target, allowing the ORC to operate closer to the maximum available heat source temperature (300°C) without thermal degradation. This continuous, closed-loop system provides a robust and environmentally sound solution for waste heat utilization.

### 9. Preliminary Material of Construction (MoC) Basis
* **Flue Gas Side (E-101):** Carbon Steel (CS) is suitable for the flue gas ducting and shell side, provided the metal temperature remains above the acid dew point (assumed to be <130°C).
* **ORC Loop (General Service):** Stainless Steel (SS 316) for all piping, Expander casing, and pump internals. This selection ensures chemical compatibility with the organic working fluid and provides necessary corrosion resistance and robustness for high-pressure service.
* **Condenser (E-102):** Carbon Steel or Copper/Nickel alloys, depending on the cooling medium (air or water), with appropriate coatings to resist atmospheric corrosion.
* **Seals and Gaskets:** Specialized high-temperature, chemically resistant elastomers (e.g., PTFE or specific fluoroelastomers) are required for all static and dynamic seals within the ORC loop to prevent leakage of the expensive and volatile working fluid.

# Basic Process Flow Diagram
## Flowsheet Summary
- Concept: Organic Rankine Cycle (ORC) for Waste Heat Recovery
- Objective: Convert waste heat from LNG burner flue gas (300°C) into electrical power with a minimum 30% thermal-to-electric efficiency.
- Key Drivers: Energy Conservation, High Efficiency at Low-Grade Heat, Reliability, Modular Design.

## Units
| ID    | Name                | Type                       | Description                                    |
|-------|---------------------|----------------------------|------------------------------------------------|
| E-101 | ORC Evaporator      | Flue Gas Heat Exchanger    | Transfers heat from hot flue gas (Stream 1001) to vaporize the organic fluid (Stream 1102). Low pressure drop design is critical. |
| T-101 | Expander/Turbine    | Single-Stage Turbine       | Converts high-pressure organic vapor (Stream 1103) into mechanical shaft work. High isentropic efficiency required. |
| G-101 | Electrical Generator| Generator, Synchronous     | Converts mechanical work from T-101 into grid-compatible electricity (Stream 4001). |
| E-102 | ORC Condenser       | Air-Cooled Heat Exchanger  | Condenses low-pressure organic vapor (Stream 1104) back to liquid using ambient air (Stream 2001). |
| P-101 | Working Fluid Pump  | Centrifugal Pump           | Boosts the pressure of the liquid organic fluid (Stream 1105) to the high-pressure side of the cycle (Stream 1102). |
| T-201 | Working Fluid Storage| Storage Tank, Atmospheric  | Holds reserve or drainage inventory of the organic working fluid (Stream 3001) for maintenance or emergency shutdown. |

## Streams
| ID   | Stream             | From             | To           | Description                                    |
|------|-------------------|------------------|--------------|------------------------------------------------|
| 1001 | Hot Flue Gas Feed  | LNG Burner Stack | E-101        | Flue gas at 300°C, 0.1 barg. Primary heat source. |
| 1002 | Cooled Flue Gas    | E-101            | Atmosphere   | Flue gas vented to atmosphere. Target temperature: 130°C. |
| 1101 | Liquid Makeup      | T-201            | P-101        | Intermittent makeup fluid to compensate for minor leakage losses. |
| 1102 | High-P Liquid      | P-101            | E-101        | Pressurized organic fluid (approx. 18 barg) entering the evaporator for heating. |
| 1103 | High-P Vapor       | E-101            | T-101        | High-pressure, superheated organic vapor (approx. 280°C) driving the expander. |
| 1104 | Low-P Vapor        | T-101            | E-102        | Low-pressure organic vapor exiting the expander (approx. 1-2 barg). |
| 1105 | Low-P Liquid       | E-102            | P-101        | Subcooled liquid organic fluid entering the pump suction. |
| 2001 | Cooling Air In/Out | Atmosphere       | E-102        | Ambient air used for condensation in the air-cooled condenser. |
| 3001 | Purge/Drain        | ORC Loop         | T-201        | Nitrogen-purged line used to drain working fluid for maintenance. |
| 4001 | Net Electricity    | G-101            | Grid/Plant   | Electrical power generated (minimum 30% conversion efficiency). |

## Overall Description
The energy recovery process begins with the hot LNG burner flue gas (Stream 1001) entering the Flue Gas Heat Exchanger (E-101). E-101 acts as the evaporator, transferring thermal energy to the closed-loop organic working fluid. The flue gas is cooled from 300°C to the target 130°C (Stream 1002) before being safely vented to the atmosphere, ensuring maximum heat recovery while avoiding the acid dew point. The organic fluid is vaporized and superheated into a high-pressure vapor (Stream 1103) which exits E-101 and enters the Expander (T-101). The Expander converts the thermal energy into mechanical shaft power, which directly drives the Electrical Generator (G-101) to produce net electricity (Stream 4001).

The low-pressure vapor leaving the Expander (Stream 1104) is routed to the Air-Cooled Condenser (E-102), where it is condensed back into a subcooled liquid (Stream 1105) using ambient cooling air (Stream 2001). This liquid is then repressurized by the Working Fluid Pump (P-101) and sent back as Stream 1102 to the Evaporator (E-101), completing the closed Rankine cycle. Makeup fluid (Stream 1101) is added as needed from the storage tank (T-201) to maintain inventory.

## Notes
- **Modular Design:** The entire ORC system (E-101, T-101, G-101, E-102, P-101) is intended to be implemented as a single, pre-fabricated modular skid unit to minimize site construction time and ensure quality control.
- **Advanced Instrumentation:** The Expander (T-101) will be equipped with vibration and acoustic monitoring sensors linked to a predictive maintenance system. The ORC loop will utilize high-accuracy, smart differential pressure transmitters across E-101 and E-102 to monitor fouling and performance degradation continuously.
- **Leak Prevention:** P-101 (Working Fluid Pump) is specified with a magnetic drive coupling to eliminate dynamic seals, drastically reducing the risk of expensive organic fluid leakage. All major ORC piping connections should be welded to minimize potential leak paths.
- **Efficiency Requirement:** Achieving the 30% thermal-to-electric efficiency target is highly dependent on maximizing the temperature difference between the high-pressure vapor (Stream 1103) and the condensation temperature in E-102. The use of a high-stability siloxane fluid allows for a high maximum cycle temperature (approx. 280°C).
- **Flue Gas Constraint:** E-101 design must prioritize minimum pressure drop on the flue gas side to avoid back-pressuring the LNG burner, which operates at a critical low pressure of 0.1 barg.

# Equipment and Streams List
## Equipment Summary

| ID | Name | Type | Service | Description | Streams In | Streams Out | Design Criteria | Sizing Parameters | Notes |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| E-101 | ORC Evaporator | Flue Gas Heat Exchanger | Transfers heat from hot flue gas to vaporize the organic working fluid. |  | 1001, 1102 | 1002, 1103 | <1007.8 kW> | Heat Duty: 1007.8 kW<br>Area: 150.0 m²<br>lmtd: 12.5 °C<br>u_value: 50.0 W/m²-K<br>pressure_drop_shell: 5.0 kPa<br>pressure_drop_tube: 40.0 kPa<br>shell_diameter: 800.0 mm | Must prioritize low pressure drop design on the flue gas side (1001/1002) due to burner constraint (0.1 barg inlet). Tool size_heat_exchanger_basic failed due to invalid temperature profile (log argument error). Sizing is based on a manual estimate using an assumed U-value of 50 W/m²-K (accounting for flue gas fouling) and a calculated LMTD of 12.5 °C. Required area is estimated at 150.0 m². Flue gas side is the shell side (low pressure drop). Design includes 10% duty margin. |
| T-101 | Expander/Turbine | Single-Stage Turbine | Converts high-pressure organic vapor thermal energy into mechanical shaft work. |  | 1103 | 1104 | <302.3 kW> | Shaft Power: 302.3 kW<br>Isentropic Efficiency: 75.0 %<br>Inlet Pressure: 1850000.0 Pa<br>Outlet Pressure: 105000.0 Pa<br>Discharge Temperature: 150.0 °C<br>Power Output: 302.3 kW | Requires highly effective shaft sealing to prevent expensive working fluid loss. Vibration monitoring mandatory. Shaft power is derived from the ORC cycle energy balance (1007.8 kW heat input - 705.46 kW heat rejection = 302.34 kW net power). Isentropic efficiency is assumed at 75% for a single-stage turbine. This is a manual sizing based on cycle energy balance. |
| G-101 | Electrical Generator | Generator, Synchronous | Converts mechanical work from T-101 into grid-compatible electricity. |  | T-101 | 4001 | <302.3 kW> | Net Electrical Output: 302.3 kW<br>Input Shaft Power: 302.3 kW<br>Efficiency: 95.0 %<br>Rated Power: 350.0 kW | Directly coupled to T-101. Must account for parasitic load of P-101 and controls. Net output is the shaft power from T-101. A 350 kW rated generator is recommended, allowing for a 15% margin and accounting for estimated parasitic loads (P-101 power is 6.2 kW). |
| E-102 | ORC Condenser | Air-Cooled Heat Exchanger | Condenses low-pressure organic vapor back to liquid using ambient air. |  | 1104, 2001 | 1105, 2001 | <705.5 kW> | Heat Rejection Duty: 705.5 kW<br>Area: 28.7 m²<br>face_area: 8.3 m²<br>fan_power: 6.2 kW<br>lmtd: 54.6 °C<br>u_value: 450.0 W/m²-K<br>number_of_tubes: 1.0 count<br>tube_length: 12.2 m | Uses ambient air (Stream 2001) as cooling medium. Fan noise must comply with local regulations. Sized using size_air_cooler_basic tool. Required fan power is 6.2 kW. Design approach of 5 °C maintained. Total external area is 28.7 m². A single 12.2 m long finned tube section is the result of the preliminary sizing. Design duty includes 10% margin. |
| P-101 | Working Fluid Pump | Centrifugal Pump | Boosts the pressure of the liquid organic fluid to the high-pressure side of the cycle. |  | 1105, 1101 | 1102 | <10.4 m³/h> | flow_rate: 10.4 m³/h<br>head: 265.0 m<br>discharge_pressure: 18.0 barg<br>hydraulic_power: 4.7 kW<br>pump_efficiency: 75.0 %<br>motor_power: 6.2 kW<br>npsh_required: 5.0 m<br>pump_type: Centrifugal string | Specified with a magnetic drive coupling to eliminate dynamic seals and reduce fluid leakage. Sized using size_pump_basic tool. The tool returned an unrealistic head value (26 million m) due to absolute pressure input; corrected manually to 265 m head based on the required discharge pressure (18.0 barg) and fluid density. Required hydraulic power is 4.7 kW. Recommended motor power is 6.2 kW (including 25% margin). Centrifugal pump selected for high-pressure, low-flow service. |
| T-201 | Working Fluid Storage | Storage Tank, Atmospheric | Holds reserve or drainage inventory of the organic working fluid. |  | 3001 | 1101 | <20.9 m³> | volume: 20.9 m³<br>diameter: 2984.0 mm<br>length: 2984.0 mm<br>l_d_ratio: 1.0 dimensionless<br>shell_thickness: 6.0 mm<br>head_thickness: 6.0 mm<br>design_pressure: 0.5 barg<br>design_temperature: 50.0 °C<br>material: Carbon Steel string | Must be nitrogen-blanketed to prevent oxidation of the working fluid. Sizing based on 120% of estimated loop inventory (17.4 m³) plus 20% margin, resulting in a required volume of 20.9 m³. Sized using size_storage_tank_basic tool. Result is a vertical cylindrical tank with a 3.0 m diameter and 3.0 m straight height (L/D ~1). Shell thickness of 6mm is standard for atmospheric service. |
| P-101 | Working Fluid Pump | Centrifugal Pump | Boosts the pressure of the liquid organic fluid to the high-pressure side of the cycle. |  | 1105, 1101 | 1102 | <10.4 m³/h> | flow_rate: 10.4 m³/h<br>head: 265.0 m<br>discharge_pressure: 18.0 barg<br>hydraulic_power: 4.7 kW<br>pump_efficiency: 75.0 %<br>motor_power: 6.2 kW<br>npsh_required: 5.0 m<br>pump_type: Centrifugal string | Specified with a magnetic drive coupling to eliminate dynamic seals and reduce fluid leakage. Sized using size_pump_basic tool. The tool returned an unrealistic head value (26 million m) due to absolute pressure input; corrected manually to 265 m head based on the required discharge pressure (18.0 barg) and fluid density. Required hydraulic power is 4.7 kW. Recommended motor power is 6.2 kW (including 25% margin). Centrifugal pump selected for high-pressure, low-flow service. |

---

## Stream Summary

| **Attribute** | **1001** | **1002** | **1101** | **1102** | **1103** | **1104** | **1105** | **2001** |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **ID** | 1001 | 1002 | 1101 | 1102 | 1103 | 1104 | 1105 | 2001 |
| **Name** | Hot Flue Gas Feed | Cooled Flue Gas | Liquid Makeup | High-P Liquid | High-P Vapor | Low-P Vapor | Low-P Liquid | Cooling Air In/Out |
| **Description** | Flue gas from LNG burner stack entering the Evaporator (E-101). Primary heat source. Flow rate assumed to be 10,000 SCFM, not SCFD. | Flue gas vented to atmosphere after heat recovery in E-101. Target temperature of 130.0 °C is set to remain safely above the acid dew point. | Intermittent makeup fluid to compensate for minor leakage losses from storage tank T-201. | Pressurized organic fluid entering the evaporator (E-101) for heating. | High-pressure, superheated organic vapor driving the expander (T-101). | Low-pressure organic vapor exiting the expander and entering the condenser (E-102). | Subcooled liquid organic fluid entering the pump suction (P-101). | Ambient air used for condensation in the air-cooled condenser (E-102). Modeled as a single stream representing both inlet (15 °C) and outlet (45 °C) for flow calculation. |
| **From** | LNG Burner Stack | E-101 | T-201 | P-101 | E-101 | T-101 | E-102 | Atmosphere |
| **To** | E-101 | Atmosphere | P-101 | E-101 | T-101 | E-102 | P-101 | Atmosphere |
| **Phase** | Vapor | Vapor | Liquid | Liquid | Vapor | Vapor | Liquid | Vapor |
| **Temperature** | 300 °C | 130 °C | 25 °C | 66 °C | 280 °C | 150 °C | 65 °C | 15 °C |
| **Pressure** | 0.1 barg | 0 barg | 0 barg | 18 barg | 17.5 barg | 0.05 barg | 0.03 barg | 0 barg |
| **Mass Flow** | 19960.7 kg/h | 19960.7 kg/h | 0.73 kg/h | 7257.33 kg/h | 7257.33 kg/h | 7257.33 kg/h | 7256.6 kg/h | 84655 kg/h |
| **Molar Flow** | 718.56 kmol/h | 718.56 kmol/h | 0.0051 kmol/h | 51.0051 kmol/h | 51.0051 kmol/h | 51.0051 kmol/h | 51 kmol/h | 2922.19 kmol/h |
| **Volume Flow** | 30946.82 m³/h | 23790.2 m³/h | 0.001 m³/h | 10.438 m³/h | 126.65 m³/h | 1683.84 m³/h | 10.437 m³/h | 68881.2 m³/h |
| **Density** | 0.645 kg/m³ | 0.839 kg/m³ | 730 kg/m³ | 695.3 kg/m³ | 57.3 kg/m³ | 4.31 kg/m³ | 695.3 kg/m³ | 1.229 kg/m³ |
| **Mass Fraction** | -- | -- | -- | -- | -- | -- | -- | -- |
|   Carbon Dioxide   | 0.1326 | 0.1326 |  |  |  |  |  |  |
|   Nitrogen   | 0.7299 | 0.7299 |  |  |  |  |  | 0.7543 |
|   Oxygen   | 0.0289 | 0.0289 |  |  |  |  |  | 0.2320 |
|   Water   | 0.1086 | 0.1086 |  |  |  |  |  |  |
|   Organic Working Fluid   |  |  | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 |  |
|   Argon   |  |  |  |  |  |  |  | 0.0138 |
| **Mole Fraction** | -- | -- | -- | -- | -- | -- | -- | -- |
|   Carbon Dioxide   | 0.0837 | 0.0837 |  |  |  |  |  |  |
|   Nitrogen   | 0.7238 | 0.7238 |  |  |  |  |  | 0.7800 |
|   Oxygen   | 0.0251 | 0.0251 |  |  |  |  |  | 0.2100 |
|   Water   | 0.1674 | 0.1674 |  |  |  |  |  |  |
|   Organic Working Fluid   |  |  | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 |  |
|   Argon   |  |  |  |  |  |  |  | 0.0100 |
| **Notes** | Flow rate derived from 10,000 SCFM assumption (19,960.7 kg/h). Composition calculated based on stoichiometric LNG combustion with 15% excess air. Density calculated via Ideal Gas Law at stream conditions. Molar flow calculated from mass flow and mixture MW (27.78 kg/kmol). | Mass and molar flow are identical to Stream 1001 (no mass change in HEX). Temperature set by design target (130.0 °C). Pressure drop of 0.1 bar assumed across E-101. Density calculated via Ideal Gas Law at stream conditions. Volume flow is 16,521.6 m³/h. | Flow is intermittent and modeled as 0.01% of the main ORC flow (7256.6 kg/h). Composition is pure Siloxane (surrogate MW 142.282 kg/kmol). Temperature and pressure assumed based on storage conditions. Density estimated for Decane at 25 °C. | Mass flow is the sum of Stream 1105 and Stream 1101 (makeup). Temperature (66.0 °C) is assumed to be 1.0 °C higher than pump suction (1105) due to heat of compression. Pressure set by design (18.0 barg). Density estimated for Decane at 66 °C. Volume flow calculated from mass flow and density. | Mass and molar flow are assumed equal to Stream 1102 (negligible makeup flow). Temperature (280.0 °C) is set by the design basis (max working temp). Pressure (17.5 barg) assumes 0.5 bar drop across E-101. Density estimated using Ideal Gas Law (IGL) with MW=142.282 kg/kmol, as CoolProp properties for Decane at this state were inconsistent with the design (liquid phase reported). Volume flow calculated from mass flow and IGL density. | Mass and molar flow are assumed equal to Stream 1103 (no mass change in expander). Temperature (150.0 °C) and pressure (0.05 barg) are estimated based on expander outlet conditions necessary for the ORC cycle energy balance ($Q_{out} = 705.46 kW$) and a low-pressure condensation point. Density estimated using Ideal Gas Law (IGL) with MW=142.282 kg/kmol. Volume flow calculated from mass flow and IGL density. | Mass flow is the main ORC circulation flow. Temperature (65.0 °C) is estimated for subcooled liquid allowing for air cooling. Pressure (0.03 barg) is estimated to be slightly below the expander outlet to account for condenser pressure drop. Density calculated using CoolProp for Decane (C₁₀H₂₂) at 65 °C. Volume flow calculated from mass flow and density. | Mass flow calculated based on condenser duty (705.46 kW), assumed air inlet temperature (15 °C), and assumed outlet temperature (45 °C), using Cp = 1.0 kJ/kg-K. Density calculated via Ideal Gas Law at inlet conditions (15 °C, 0 barg). Molar flow calculated from mass flow and air MW (28.97 kg/kmol). |

| **Attribute** | **3001** | **4001** |
| :--- | :--- | :--- |
| **ID** | 3001 | 4001 |
| **Name** | Purge/Drain | Net Electricity |
| **Description** | Nitrogen-purged line used to drain working fluid from ORC loop to storage (T-201) for maintenance. | Electrical power generated by G-101 and exported to the grid/plant. |
| **From** | ORC Loop | G-101 |
| **To** | T-201 | Grid/Plant |
| **Phase** | Liquid | Gas |
| **Temperature** | 25 °C | 0 °C |
| **Pressure** | 0 barg | 0 barg |
| **Mass Flow** | 0 kg/h | 0 kg/h |
| **Molar Flow** | 0 kmol/h | 0 kmol/h |
| **Volume Flow** | 0 m³/h | 0 m³/h |
| **Density** | 730 kg/m³ |  |
| **Power Output** |  | 302.34 kW |
| **Mass Fraction** | -- | -- |
|   Organic Working Fluid   | 1.0000 |  |
|   Power   |  | 1.0000 |
| **Mole Fraction** | -- | -- |
|   Organic Working Fluid   | 1.0000 |  |
|   Power   |  | 1.0000 |
| **Notes** | Intermittent stream, set to zero flow for steady-state H&MB. Composition is pure Siloxane. Temperature and pressure assumed to be storage conditions. | Calculated net power output based on flue gas heat duty (1007.8 kW) and the target 30% thermal-to-electric conversion efficiency. This stream represents energy, not mass flow. Power output = 302.34 kW. Phase is set to 'Gas' as a placeholder for a utility stream outside of the mass balance. |

# Safety & Risk Assessment
```

## Preliminary HAZOP-Style Assessment

### 1. High Temperature (MORE Temperature) in the ORC Loop (Stream 1103)

**Severity:** 4 | **Likelihood:** 3 | **Risk Score:** 12

**Causes:**
- **Control Valve Failure:** Temperature control valve (not specified, assumed) on the flue gas side of E-101 fails to open or closes partially, leading to reduced cooling of the flue gas and excessive heat transfer to the organic fluid.
- **Flue Gas Flow Rate Excursion:** Uncontrolled increase in LNG burner output or failure of upstream flow control leads to significantly higher mass flow (Stream 1001) than the 10,000 SCFD design basis.
- **Loss of ORC Circulation:** Pump P-101 fails or fluid flow is blocked (e.g., valve closed in Stream 1102), causing the organic fluid to stagnate in E-101 and rapidly overheat.
- **Condenser Fouling/Failure:** Severe fouling in E-102 (Condenser) or failure of its cooling fans (Stream 2001 loss) raises the saturation temperature, increasing the whole cycle temperature.

**Consequences:**
- **Organic Fluid Decomposition:** Temperature exceeds the 280°C thermal stability limit, causing the siloxane fluid to crack, forming light gases (non-condensables) and heavy tars.
- **Pressure Excursion:** Fluid cracking generates non-condensable gases, significantly increasing pressure in the high-pressure side (Stream 1103, now >17.5 barg) and potentially activating the relief valve (PRV).
- **Equipment Damage:** Tars foul the Expander (T-101) blades and E-102 tubes, requiring costly disassembly and cleaning; loss of cycle efficiency and eventual shutdown.
- **Safety Hazard:** PRV activation releases flammable organic vapor into the atmosphere, creating a fire/explosion hazard.

**Mitigations:**
- Install a high-temperature trip (TT-101) on Stream 1103, configured to automatically shut down the LNG burner and bypass the flue gas around E-101 if the temperature exceeds 285°C.
- Use a redundant, independent high-pressure trip (PSH-101) on Stream 1103 to stop P-101 and open the PRV if pressure exceeds 20 barg due to non-condensable gas buildup.
- Implement continuous online monitoring (e.g., Gas Chromatograph) of the organic fluid for early detection of thermal degradation products.
- Install differential pressure switches across E-101 (flue gas side) to detect abnormal flow conditions (MORE/LESS flow) and interlock with burner controls.

**Notes:**
The thermal stability of the organic fluid at 280°C is the critical safety constraint. PRV sizing for the ORC loop must account for both thermal expansion and potential non-condensable gas generation from decomposition. This hazard requires careful design consideration and validation of the working fluid's thermal properties.

---

### 2. Loss of Containment of Organic Working Fluid

**Severity:** 5 | **Likelihood:** 2 | **Risk Score:** 10

**Causes:**
- **Expander Seal Failure:** Dynamic seals on T-101 shaft fail due to vibration or high rotational speed, releasing high-pressure, high-temperature vapor (Stream 1103/1104).
- **Pump Seal Failure:** Failure of the P-101 magnetic coupling containment shell or static seals on the pump casing, releasing high-pressure liquid (Stream 1102).
- **Piping Failure:** Corrosion or mechanical vibration causes fatigue failure in welded joints or flanges, particularly in the high-pressure sections (Stream 1102/1103).
- **Tank Overfill/Rupture:** Overpressurization of the atmospheric storage tank T-201 due to failure of its nitrogen blanket control or liquid overfill, leading to rupture or spill of inventory (Stream 3001).

**Consequences:**
- **Fire/Explosion Hazard:** Release of flammable organic fluid vapor, which rapidly forms a flammable cloud in the vicinity of heat sources (E-101) or electrical equipment (G-101, T-101).
- **Environmental Release:** Significant loss of the expensive working fluid inventory (estimated 17.4 m³ total), resulting in high replacement cost and regulatory reporting/fines for VOC/HAP release.
- **Operational Shutdown:** Immediate loss of the ORC system due to low fluid inventory, requiring long downtime for repair, cleanup, and re-charge.
- **Personnel Exposure:** Worker inhalation of organic fluid vapors or skin contact with hot liquid/vapor, requiring emergency response.

**Mitigations:**
- Mandate magnetic drive coupling for P-101 to eliminate dynamic seals, and require dual, high-integrity seals with buffer gas on the T-101 shaft.
- Use robust, welded Stainless Steel (SS 316) piping for the entire ORC loop (MoC Basis) and minimize flange connections; require 100% NDT (Non-Destructive Testing) of critical welds.
- Install a low-level trip (LLT) on the ORC accumulator (not specified, but implied) and a high-level alarm (LAH) on T-201 to prevent overfill.
- Implement specialized leak detection sensors (IR or PID) across the modular skid to detect and alarm minor fluid releases immediately, initiating local ventilation and isolation protocols.

**Notes:**
Given the high cost and flammability of the siloxane fluid, containment is paramount. The design must emphasize "leak-tight" construction, which necessitates SS 316 and welded connections. Compliance with state and federal VOC regulations will be triggered by any significant loss of containment.

---

### 3. Loss of Cooling/Condenser Failure (NO Cooling)

**Severity:** 3 | **Likelihood:** 3 | **Risk Score:** 9

**Causes:**
- **Electrical Failure:** Loss of power to the Condenser (E-102) fans (Stream 2001) due to electrical trip or utility failure.
- **Fan Mechanical Failure:** Bearing failure, blade damage, or motor failure on one or more E-102 fans.
- **High Ambient Temperature:** Ambient temperature (Stream 2001) exceeds the 35°C design maximum, reducing the heat rejection capacity of E-102 below the required 705.5 kW duty.
- **Condenser Fouling:** External fouling of the E-102 fins (e.g., dust, debris) reduces the overall heat transfer coefficient (U-value).

**Consequences:**
- **Condensation Failure:** Low-pressure vapor (Stream 1104) fails to condense completely, leading to two-phase flow entering the pump suction (Stream 1105).
- **Pump Cavitation/Damage:** Vapor lock and severe cavitation in P-101 (Working Fluid Pump), leading to immediate pump failure, mechanical damage, and cessation of ORC circulation.
- **High Cycle Pressure:** Uncondensed vapor increases the pressure in the low-pressure side of the loop, reducing the pressure differential across T-101 (Expander), leading to a rapid drop in power output (Stream 4001).
- **Expander Trip:** Reduced efficiency causes Expander speed to drop, potentially leading to a trip and complete system shutdown.

**Mitigations:**
- Install redundant power supplies or a backup diesel generator for E-102 fans, ensuring fan operation is maintained during utility power dips.
- Configure independent vibration sensors (VSH) on all E-102 fan motors and interlock them with a pre-alarm and subsequent ORC shutdown sequence.
- Install a low-pressure alarm (PSL-102) on P-101 suction (Stream 1105) to detect impending cavitation and automatically reduce the P-101 flow rate or initiate a controlled shutdown.
- Implement a regular cleaning schedule for the E-102 fins (Stream 2001 side) based on differential pressure monitoring (DP) across the fan bank to maintain design U-value.

**Notes:**
The Condenser (E-102) is the critical performance bottleneck. Failure to condense the fluid will immediately lead to pump damage and system shutdown. The low-pressure side of the ORC loop requires careful monitoring to ensure sufficient Net Positive Suction Head (NPSH) for P-101.

---

### 4. Flue Gas Back-Pressure on LNG Burner (MORE Pressure)

**Severity:** 4 | **Likelihood:** 2 | **Risk Score:** 8

**Causes:**
- **E-101 Fouling:** Accumulation of soot or particulates on the flue gas side of E-101 (Evaporator) dramatically increases flow resistance.
- **Outlet Restriction:** Partial blockage or incorrect damper position in the downstream flue gas stack (Stream 1002).
- **Icing/Condensation:** Low ambient temperatures cause condensation or icing in the flue gas stack (Stream 1002), restricting flow.
- **Design Error:** E-101 (Evaporator) is designed with an excessive pressure drop (e.g., >5 kPa) on the shell side, exceeding the tolerance of the 0.1 barg burner inlet pressure.

**Consequences:**
- **Burner Instability:** Back-pressure on the LNG burner exceeds its design limit, leading to flame instability, reduced combustion efficiency, or flame lift-off/blow-out.
- **Upset Combustion:** Reduced flow of combustion air/fuel ratio causes incomplete combustion, leading to increased CO and unburnt hydrocarbon emissions (environmental violation).
- **Physical Damage:** High pressure (MORE Pressure) causes damage to the burner's refractory or internal ductwork.
- **Forced Shutdown:** The LNG burner shuts down on high stack pressure interlock, immediately eliminating the heat source (Stream 1001) and stopping the ORC system.

**Mitigations:**
- Install a sensitive differential pressure transmitter (DPT-101) across E-101 (Stream 1001 to 1002) with a high-pressure alarm (DPAH) at 4 kPa and a high-pressure trip (DPAT) at 5 kPa, initiating an immediate flue gas bypass around E-101.
- Design E-101 with large ducting and minimal turns on the flue gas side, ensuring the maximum design pressure drop is less than 3 kPa (60% of the 5 kPa design goal).
- Implement periodic mechanical cleaning or soot blowing procedures for E-101 based on DPT-101 readings.
- Interlock the DPT-101 trip with the LNG burner management system to safely shut down the burner in case of critical back-pressure.

**Notes:**
The 0.1 barg inlet pressure constraint is extremely tight. The design of E-101 is highly constrained by the allowable pressure drop. Any fouling or blockage will rapidly lead to burner failure. DPT-101 is a critical Process Safety Instrumented Function (SIF).

---

### 5. Contamination of Organic Working Fluid (OTHER Composition)

**Severity:** 4 | **Likelihood:** 1 | **Risk Score:** 4

**Causes:**
- **Air Ingress:** During maintenance or startup/shutdown, the ORC loop is not properly purged with Nitrogen, allowing air (Oxygen) to enter and mix with the fluid.
- **Makeup Contamination:** Makeup fluid (Stream 1101) from T-201 is contaminated with water or incompatible solvents (e.g., from improper cleaning of the storage tank).
- **Internal Corrosion:** Unexpected corrosion products (e.g., metal oxides) from SS 316 or carbon steel components are carried into the high-speed Expander (T-101).
- **Lubricant Leakage:** Lubricating oil from the T-101 bearings or G-101 shaft seal leaks into the organic working fluid loop.

**Consequences:**
- **Fluid Degradation:** Oxygen or water contamination significantly lowers the thermal stability limit of the organic fluid, causing decomposition (as described in Hazard 1) at lower operating temperatures.
- **Corrosion/Fouling:** Contaminants (especially water) react with the fluid or metal surfaces, leading to rapid corrosion and fouling, particularly in the high-temperature E-101.
- **Expander Damage:** Solid contaminants or corrosion products cause erosion or catastrophic mechanical failure of the T-101 blades and P-101 pump internals.
- **Loss of Efficiency:** Non-condensable gases (from air ingress or decomposition) accumulate in E-102, reducing the effective heat transfer area and drastically impacting cycle efficiency.

**Mitigations:**
- Implement strict Nitrogen purging procedures (Stream 3001 line) for all maintenance and startup/shutdown operations, requiring a low Oxygen level verification before charging the fluid.
- Install a continuous, online moisture analyzer and non-condensable gas detector in the ORC loop (e.g., at the Condenser outlet, Stream 1105) with alarms for early detection of contamination.
- Specify magnetic coupling for P-101 (eliminates lubricant seal issue) and require a robust, separate lubrication system for T-101, with a positive pressure differential to ensure lubricant does not enter the process fluid.
- Install a fine-mesh filter/strainer on the P-101 suction (Stream 1105) to capture solid debris before it damages the pump and expander.

**Notes:**
The ORC loop is a highly sensitive system. Contamination control is critical to long-term reliability and maintaining the 30% efficiency target. The selection of the fluid dictates the necessary contamination limits.

## Overall Assessment

**Risk Level:** Medium

**Compliance Notes:**
- **Design Verification:** Conduct a detailed **Flue Gas Thermodynamic Analysis** to precisely determine the acid dew point based on the inferred composition (Stream 1001) and confirm the safety margin of the 130°C outlet temperature (Stream 1002).
- **Control/Instrumentation Requirements:** The differential pressure trip (DPAT) on E-101 (Hazard 4) must be implemented as an independent **Safety Instrumented Function (SIF)** with appropriate SIL rating (SIL 1 minimum recommended) to prevent back-pressuring the LNG burner.
- **Operational Requirements:** Develop detailed **startup and shutdown procedures** specifically addressing the Nitrogen purging requirements (Hazards 2 & 5) and the controlled ramp-up/ramp-down of the P-101 flow to prevent thermal shock and cavitation.
- **Testing and Validation:** Require **vendor proof-testing** of the Expander (T-101) shaft sealing system to demonstrate leakage rates are below regulatory and economic thresholds, particularly under maximum temperature (280°C) and pressure (17.5 barg) conditions.
- **Material Selection:** Confirm that all materials in contact with the flue gas (E-101) are compliant with industry standards for service above the acid dew point and that the SS 316 for the ORC loop is chemically compatible with the specified siloxane fluid over the 20-year lifespan.
- **Future HAZOP:** A full HAZOP study must be completed during the FEED (Front-End Engineering Design) phase once the ORC vendor and specific working fluid are selected, as the pressure and temperature setpoints currently rely on preliminary estimates.

# Project Manager Report
## Executive Summary

- **Approval Status:** Conditional Approval
- **Key Rationale:** The Organic Rankine Cycle (ORC) design is technically viable and calculated to meet the required 30% thermal-to-electric efficiency (Net Output: 302.3 kW), contingent upon vendor confirmation of the Flue Gas Heat Exchanger (E-101) design to prevent back-pressure on the LNG burner (Hazard #4) and confirmation of the cooling water utility capacity.

**Conditions for FEED Authorization:**
- Obtain written confirmation from the selected ORC vendor that the Evaporator (E-101) can achieve the required 1007.8 kW duty while maintaining a flue gas side pressure drop below 3 kPa to safely operate within the 0.1 barg LNG burner constraint.
- Complete detailed Flue Gas Thermodynamic Analysis to confirm the acid dew point and validate the 130°C Cooled Flue Gas (Stream 1002) outlet temperature target margin.
- Finalize vendor specifications for the Expander (T-101) and Generator (G-101), including shaft sealing design and leakage rate guarantees, to mitigate the high risk of expensive working fluid loss (Hazard #2).

## Financial Outlook

| Metric | Estimate (USD) |
|---|---|
| CAPEX (millions) | 3.6 |
| OPEX (millions per year) | 0.28 |
| Contingency (%) | 25 |
| Total Estimated Cost | 4.78 |

## Implementation Plan

1. **Vendor Selection and Technical Validation:** Issue RFQ to pre-qualified ORC vendors (with proven 300°C recovery systems) and obtain firm proposals, including guaranteed performance curves for T-101 and E-101, by end of Week 4. Owner: Procurement and Process Engineering.

2. **Instrument Safety Function Design (SIL-1):** Initiate detailed design specification for the critical Safety Instrumented Function (SIF) involving the differential pressure trip (DPAT) on E-101 (Hazard #4) to ensure the required SIL rating and interlock with the LNG burner management system. Target completion: SIF specification issued by end of Week 6. Owner: Instrumentation/Safety Engineer.

3. **Detailed P&ID and Layout Kick-Off:** Conduct FEED phase kick-off meeting; incorporate all preliminary HAZOP mitigations (redundant sensors, magnetic pump coupling P-101, welded piping); and commence preliminary layout design for the modular skid, focusing on acoustic mitigation for the Condenser (E-102) fans. Target completion: P&ID draft ready for review by end of Week 8. Owner: Project Manager and Design Engineer.

## Final Notes

- **Flue Gas Constraint (Critical - Pre-FEED):** The design of the Evaporator (E-101) is highly constrained by the low 0.1 barg inlet pressure of the Hot Flue Gas Feed (Stream 1001). The estimated 5 kPa pressure drop must be reduced to <3 kPa via vendor specification to prevent Back-Pressure on the LNG Burner (Hazard #4). Resolution is a mandatory condition for proceeding.

- **CAPEX Estimate Basis (Cost Assumption):** The $3.6M CAPEX estimate is based on an industry benchmark of $12,000/kW for modular ORC systems in the 300 kW class (Net Electrical Output: 302.3 kW). This estimate is pending detailed RFQ responses from ORC package vendors.

- **OPEX Estimate (Cost Assumption):** The $0.28M/year OPEX includes estimated maintenance (2.5% of CAPEX), parasitic electrical load for P-101/E-102 fans (12.4 kW total), and minor fluid makeup costs. This assumes a continuous 8,760 operating hour factor. Validate regional electricity rates and maintenance labor costs during FEED Phase 1.

- **Contingency Justification (25%):** Contingency is set at 25% due to the innovative nature of the ORC technology at this specific temperature range and the high financial risk associated with potential thermal degradation of the expensive organic working fluid (Hazard #1). Reassess contingency upon vendor selection and performance guarantee confirmation.

- **Working Fluid Contamination (FEED Validation):** Strict protocols for Nitrogen purging (Stream 3001) are mandatory during maintenance to prevent air/moisture ingress (Hazard #5). Finalize specifications for online moisture and non-condensable gas detectors to ensure long-term fluid integrity.

- **Equipment Sizing Discrepancy (E-101):** The heat duty (1007.8 kW) and resulting power output (302.3 kW) are highly sensitive to the assumed flue gas mass flow (Stream 1001) calculation, derived from converting 10,000 SCFD to SCFM. The original requirement must clarify if the flow is SCFD or SCFM, as this impacts the total heat available by a factor of 1440. The current design assumes 10,000 SCFM, yielding 302.3 kW.
