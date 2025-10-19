# PyROPS v2.3.12 - Requirements and Specifications Document

## Executive Summary

This document provides a comprehensive analysis of the Python Rocket Performance Simulator (PyROPS) developed by the Aerospace Systems Research Institute. This analysis focuses on functional requirements, specifications, inputs, processing, and outputs to serve as a foundation for future development decisions.

**System Name:** PyROPS (Python Rocket Performance Simulator)
**Version:** 2.3.12
**Developer:** Aerospace Systems Research Institute, 2023
**Current Status:** Operational but requires optimization and modernization

---

## 1. System Overview

### 1.1 Purpose
PyROPS is a high-fidelity 6-Degree-of-Freedom (6-DOF) rocket trajectory simulation system designed to model the complete flight envelope of sounding rockets and experimental launch vehicles. The system simulates from launch rail departure through apogee, descent, and recovery phases.

### 1.2 Core Capabilities
- **6-DOF Rigid Body Dynamics**: Full translational and rotational motion simulation
- **High-Fidelity Aerodynamics**: Integration with external aerodynamic prediction tools (RASAero II, MissileDATCOM)
- **Variable Mass Properties**: Time-dependent mass, center of gravity, and moments of inertia modeling for propellant consumption
- **Atmospheric Modeling**: Altitude-dependent atmospheric properties
- **Wind Modeling**: Altitude-varying wind profiles with turbulence
- **Monte Carlo Analysis**: Statistical analysis of trajectory dispersions
- **Multi-Stage Support**: Staging and separation events
- **Recovery Systems**: Parachute and drogue deployment modeling
- **Launch Rail Dynamics**: Constrained motion modeling during rail-guided phase
- **Hybrid and Liquid Propulsion**: Support for various propulsion system types

### 1.3 Use Cases
1. **Mission Planning**: Predicting landing zones and trajectory envelopes
2. **Performance Optimization**: Evaluating design changes on flight performance
3. **Safety Analysis**: Determining impact dispersion zones
4. **Uncertainty Quantification**: Monte Carlo analysis of manufacturing tolerances and environmental conditions
5. **Control System Design**: Fin cant angle and roll control system design
6. **Aerodynamic Validation**: Cross-checking aerodynamic prediction tools

---

## 2. Functional Requirements

### 2.1 Physics Modeling Requirements

#### FR-2.1.1 Equations of Motion
- **Requirement**: Simulate 6-DOF rigid body dynamics
- **State Variables** (12 states):
  1. Velocity kinematic, North (m/s)
  2. Velocity kinematic, East (m/s)
  3. Velocity kinematic, Downward (m/s)
  4. Angular velocity, roll (rad/s)
  5. Angular velocity, pitch (rad/s)
  6. Angular velocity, yaw (rad/s)
  7. Latitude (degrees)
  8. Longitude (degrees)
  9-12. Quaternion orientation (w, x, y, z components)

#### FR-2.1.2 Coordinate Systems
- **Earth-Centered Inertial (ECI)**: For initial conditions
- **North-East-Down (NED)**: For kinematic velocities
- **Body-Fixed**: For forces, moments, and angular velocities
- **Geodetic**: For position (latitude, longitude, altitude)

#### FR-2.1.3 Gravitation Model
- **Standard**: Spherical Earth gravity model (g = GM/r²)
- **Advanced**: WGS84 ellipsoidal Earth model with latitude-dependent gravity
- **Formula**: g₀ = -9.7803 × (1 + 0.0053×sin²(lat) - 0.0000058×sin²(2×lat))

#### FR-2.1.4 Atmospheric Model
- **Input**: Tabulated atmosphere data (altitude vs. temperature, pressure, density)
- **Properties Computed**:
  - Density (kg/m³)
  - Pressure (Pa)
  - Temperature (K)
  - Speed of sound (m/s)
  - Dynamic pressure (Pa)
  - Mach number

#### FR-2.1.5 Aerodynamics
- **Lookup Tables**: 2D interpolation (Mach, angle of attack) for:
  - Axial force coefficient (CA)
  - Normal force coefficient (CN)
  - Center of pressure location (m)
- **Data Sources**:
  - RASAero II output files (primary aerodynamic database)
  - MissileDATCOM output files (backup/validation)
- **Mach Regimes**:
  - Subsonic (M < 0.8)
  - Transonic (0.8 ≤ M ≤ 1.5) - interpolated
  - Supersonic (M > 1.5)
- **Configuration Support**:
  - Complete vehicle
  - Nose section (post-separation)
  - Booster section (post-separation)

#### FR-2.1.6 Fin Aerodynamics
- **Analytical Models**: Barrowman method for subsonic/supersonic regimes
- **Effects Modeled**:
  - Normal force generation
  - Roll moment from fin cant angle
  - Roll damping
  - Induced drag
- **Configuration**:
  - Root chord, tip chord, sweep, span
  - Fin location from nose
  - Cant angle (for roll control)
  - Number of fins (default: 4)

#### FR-2.1.7 Damping Moments
- **Pitch Damping**: Function of pitch rate, geometry, altitude
- **Yaw Damping**: Function of yaw rate, geometry, altitude
- **Roll Damping**: Fin-induced roll damping

#### FR-2.1.8 Propulsion System
- **Thrust Curve Input**: Time-based thrust and chamber pressure data
- **Curve Fitting**: Polynomial fitting (Chebyshev, Hermite, Laguerre, Legendre, Polynomial)
- **Thrust Models**:
  - Momentum thrust
  - Pressure thrust from nozzle exit area and ambient pressure
- **Misalignment**: Pitch and yaw thrust misalignment modeling
- **Propellant Types**: Hybrid (solid fuel + liquid oxidizer) and liquid

#### FR-2.1.9 Mass Properties (Time-Varying)
- **Inputs**:
  - Dry mass, COM, MOI (from CAD)
  - Fuel grain properties (density, geometry, burn characteristics)
  - Oxidizer properties (density, volume, consumption rate)
- **Computed Properties** (as function of time):
  - Total mass (kg)
  - Center of gravity location (m from datum)
  - Moments of inertia: Ixx, Iyy, Izz (kg·m²)

#### FR-2.1.10 Wind and Turbulence
- **Wind Profile**: Altitude-dependent wind magnitude and bearing
- **Turbulence Model**: Dryden turbulence spectrum
  - Turbulence length scale
  - Turbulence intensity (σ)
- **Jetstream**: Optional high-altitude wind layer (10-15 km)

### 2.2 Simulation Control Requirements

#### FR-2.2.1 Numerical Integration
- **Methods Supported**:
  - Fixed time-step (Euler, RK2, RK4, RK8)
  - Adaptive time-step (RK45, DOP853)
- **Time Step Control**:
  - User-specified time step
  - Adaptive step size with tolerance control
- **Integration Domain**: Time-based (0 to Tmax)

#### FR-2.2.2 Event Detection
- **Rail Departure**: Detect when rocket clears launch rail
- **Burnout**: Detect propellant exhaustion
- **Apogee**: Detect maximum altitude
- **Parachute Deployment**: Time-based or altitude-based
- **Drogue Deployment**: Altitude-based
- **Staging**: Time-based separation events
- **Ground Impact**: Altitude = 0
- **Angle of Attack Limit**: Monitor aerodynamic validity

#### FR-2.2.3 Flight Phases
1. **Launch Rail Phase**: Constrained 1-DOF motion along rail
2. **Powered Ascent**: Thrust + aerodynamics + gravity
3. **Coasting Ascent**: Aerodynamics + gravity (post-burnout)
4. **Apogee**: Velocity ≈ 0
5. **Descent** (multiple modes):
   - Free fall
   - Drogue descent
   - Main parachute descent
6. **Ground Impact**: Simulation termination

### 2.3 Monte Carlo Requirements

#### FR-2.3.1 Uncertainty Parameters
- Launch conditions: Elevation angle, azimuth angle, altitude
- Thrust: Magnitude (%), misalignment (pitch/yaw), burn time
- Aerodynamics: Drag coefficient (%), lift coefficient (%), moment coefficient (%), center of pressure (%)
- Fin cant angle
- Wind: Magnitude (%), direction
- Roll control parameters

#### FR-2.3.2 Statistical Sampling
- **Distribution**: Truncated normal distribution
- **Population Size**: User-specified number of runs
- **Output**: Statistical ensemble of trajectories

### 2.4 Recovery System Requirements

#### FR-2.4.1 Parachute Modeling
- **Parameters**:
  - Drag coefficient
  - Diameter
  - Deployment time/altitude
- **Configurations**:
  - Main parachute
  - Drogue parachute
  - Nose section parachute
  - Booster section parachute
  - Combined parachute

#### FR-2.4.2 Descent Dynamics
- **Drag Force**: F = 0.5 × ρ × V² × CD × A
- **Terminal Velocity**: Computed from force balance
- **Deployment Shock**: Not modeled (instantaneous deployment)

### 2.5 Control System Requirements

#### FR-2.5.1 Roll Control
- **Method**: Pulsed thrusters or aerodynamic (fin cant)
- **Control Law**: Bang-bang control with deadband
- **Parameters**:
  - Roll rate thresholds (upper/lower)
  - Thruster force
  - Pulse frequency
  - Active time window

---

## 3. Input Requirements and Formats

### 3.1 Configuration Inputs (UI-Based)

#### 3.1.1 Simulation Parameters
- **Maximum Simulation Time** (s): Total simulation duration
- **Time Step Size** (s): Integration time step
- **Number of Runs**: For Monte Carlo analysis

#### 3.1.2 Launch Site
- **Latitude** (deg): -90 to +90
- **Longitude** (deg): -180 to +180
- **Altitude** (m): Above sea level
- **Elevation Angle** (deg): Launch rail angle from horizontal
- **Azimuth** (deg): Launch direction (counter-clockwise from North)
- **Rail Length** (m): Length of launch rail

#### 3.1.3 Vehicle Geometry
- **Body Radius** (m): Rocket fuselage radius
- **Body Length** (m): Total rocket length
- **Nose Radius** (m): Nose cone base radius
- **Nose Length** (m): Nose cone length
- **Nozzle Exit Area** (m²): For pressure thrust calculation

#### 3.1.4 Fin Geometry
- **Root Chord** (m): Fin root chord length
- **Tip Chord** (m): Fin tip chord length
- **Sweep** (m): Leading edge sweep distance
- **Span** (m): Fin semi-span
- **Location** (m): Distance from nose to fin leading edge
- **Span Root** (m): Distance from body centerline to fin root
- **Cant Angle** (deg): Fin cant for roll control

#### 3.1.5 Mass Properties (Dry)
- **CAD Mass** (kg): Dry mass from CAD
- **CAD COM** (m): Center of mass (x, y, z from origin)
- **CAD MOI** (kg·m²): Moments of inertia (Ixx, Iyy, Izz)

#### 3.1.6 Propulsion - Fuel
- **Density** (kg/m³): Solid fuel density
- **Radius** (m): Fuel grain outer radius
- **Thickness** (m): Fuel grain wall thickness (initial and current)
- **Length** (m): Fuel grain length
- **COM** (m): Fuel grain center of mass location

#### 3.1.7 Propulsion - Oxidizer
- **Density** (kg/m³): Liquid oxidizer density
- **Radius** (m): Oxidizer tank radius
- **Length** (m): Oxidizer column length (initial and current)
- **COM** (m): Oxidizer center of mass location

#### 3.1.8 Propulsion - Performance
- **Burn Time** (s): Total burn duration
- **Fuel Burn Time** (s): Fuel grain burn duration
- **Thrust Polynomial Degree**: Curve fit polynomial order
- **Thrust Hybrid**: Flag for hybrid motor mode

#### 3.1.9 Recovery Systems
- **Main Parachute**:
  - CD (drag coefficient)
  - Diameter (m)
  - Deployment delay (s) or altitude (m)
- **Drogue Chute**: Same parameters
- **Nose/Booster Chutes**: Individual parameters for separated sections

#### 3.1.10 Staging (if applicable)
- **Number of Stages**: Integer
- **Stage Time** (s): Separation event time
- **Stage Delay** (s): Delay between events
- **Stage Mass, COM, MOI**: Properties of separated stage

#### 3.1.11 Uncertainty Bounds (Monte Carlo)
For each parameter:
- **Lower Limit**: Minimum variation
- **Upper Limit**: Maximum variation

Parameters include:
- Launch elevation, azimuth, altitude
- Thrust misalignment (pitch, yaw), magnitude (%), burn time
- Wind magnitude (%), direction
- Aerodynamic coefficients (%)
- Center of pressure (%)
- Fin cant angle

#### 3.1.12 Solver Settings
- **Solver Type**: Fixed-step (Order 2/4/8) or Adaptive (RK45/DOP853)
- **Relative Tolerance**: For adaptive solvers
- **Absolute Tolerance**: For adaptive solvers
- **First Time Step** (s): Initial step size
- **Maximum Time Step** (s): Step size limit

#### 3.1.13 Options/Flags
- **Earth Model**: Spherical or WGS84 ellipsoid
- **Turbulence**: Enable/disable atmospheric turbulence
- **Staging**: Enable multi-stage simulation
- **Thrust Model**: Select thrust curve source
- **Roll Control**: Enable active roll control
- **Monte Carlo Mode**: Enable uncertainty analysis
- **4-in-1 Mode**: Generate combined plots
- **Detailed MC Output**: Full Monte Carlo dataset export

### 3.2 File-Based Inputs

#### 3.2.1 Atmosphere Data
- **File**: `Inputs/atmosphere_data.xlsx`
- **Format**: Excel spreadsheet, no header
- **Columns**:
  1. Altitude (m)
  2. Temperature (K)
  3. Pressure (Pa)
  4. Density (kg/m³)
- **Requirements**: Monotonically increasing altitude, sufficient range (0 to expected apogee + margin)

#### 3.2.2 Mass Properties (Time-Series)
- **File**: `Inputs/mass_properties.xlsx`
- **Format**: Excel spreadsheet, header row
- **Columns**:
  - time (s)
  - mass (kg)
  - MOIx (kg·m²)
  - MOIy (kg·m²)
  - MOIz (kg·m²)
  - centre-of-mass (m from origin)
- **Generation**: Computed by `calculator.pyw` from fuel/oxidizer geometry and consumption rates
- **Requirements**: Time array from 0 to burnout + margin, constant values post-burnout

#### 3.2.3 Thrust Curve - Hybrid Rocket
- **File**: `Inputs/thrust_curve_hybrid.xlsx`
- **Format**: Excel spreadsheet, header row
- **Columns**:
  - Time (s)
  - Thrust (N) - momentum thrust
  - Chamber Pressure (Pa)
- **Requirements**: Time from 0 to burnout, smooth data for polynomial fitting

#### 3.2.4 Thrust Curve - Liquid Rocket
- **File**: `Inputs/thrust_curve_liquid.xlsx`
- **Format**: Excel spreadsheet, header row
- **Columns**:
  - Pressure (Pa) - reversed order (high to low)
  - Thrust (N) - reversed order
- **Note**: Data is flipped during import
- **Requirements**: Covers expected chamber pressure range

#### 3.2.5 Thrust Curve - Staging
- **File**: `Inputs/thrust_curve_staging.xlsx`
- **Format**: Similar to hybrid, for multi-stage vehicles
- **Use**: Upper stage or booster thrust profiles

#### 3.2.6 Thrust Curve - Raw Data
- **File**: `Inputs/thrust_curve_RAW.csv`
- **Format**: CSV file
- **Use**: Original test data before processing

#### 3.2.7 Aerodynamic Database - Main Vehicle
- **Files**:
  - `Inputs/RASAeroII.xlsx` (0° fin cant)
  - `Inputs/RASAeroII15.xlsx` (15° fin cant)
  - `Inputs/RASAeroII Detailed.xlsx` (extended data)
  - `Inputs/RASAeroII15 Detailed.xlsx`
- **Format**: Excel spreadsheet, header row
- **Columns**:
  1. Mach number
  2. Alpha (angle of attack, degrees)
  3. [Other columns...]
  4. CD (column 5)
  5. [Other columns...]
  6. CN (column 8)
  7. [Other columns...]
  8. COP (column 12, inches - converted to meters)
- **Requirements**:
  - Mach range: 0 to expected max Mach + margin
  - Alpha range: 0° to expected max angle of attack
  - Structured grid (all Mach × Alpha combinations)

#### 3.2.8 Aerodynamic Database - Nose Section
- **Files**:
  - `Inputs/RASAeroIINose.xlsx`
  - `Inputs/RASAeroIINose15.xlsx`
- **Format**: Same as main vehicle
- **Use**: Post-separation nose cone aerodynamics

#### 3.2.9 Aerodynamic Database - Booster Section
- **Files**:
  - `Inputs/RASAeroIIBooster.xlsx`
  - `Inputs/RASAeroIIBooster15.xlsx`
- **Format**: Same as main vehicle
- **Use**: Post-separation booster aerodynamics

#### 3.2.10 MissileDATCOM Data
- **File**: `Inputs/MissileDATCOM.txt`
- **Format**: DATCOM output file (text)
- **Processing**: Parsed by `missile_datcom.pyw` to extract CN, CD, COP
- **Output**: `Inputs/MissileDATCOM.xlsx` (converted format)
- **Cards**: User-specifies number of Mach cards to parse

#### 3.2.11 Wind Profile
- **File**: `Inputs/wind.xlsx`
- **Format**: Excel spreadsheet, header row
- **Columns**:
  - altitude (m)
  - magnitude (m/s)
  - bearing (degrees, HYROPS convention: counter-clockwise from North)
- **Transformation**: Converted to North-East components internally
- **Requirements**: Altitude from 0 to apogee + margin

#### 3.2.12 Side Damping Parameters
- **File**: `Inputs/side_damping.xlsx`
- **Format**: Excel spreadsheet
- **Content**: Rocket geometry parameters for pitch/yaw damping calculations
- **Parameters**:
  - Segment radii (r1-r8)
  - Segment lengths (s1-s8)
  - Nose geometry

#### 3.2.13 Settings File
- **File**: `Inputs/Settings.xlsx`
- **Format**: Excel spreadsheet
- **Content**: Simulation configuration options
- **Parameters**: Various flags and parameters not in the UI

#### 3.2.14 Limitations File
- **File**: `ASRI_Simulator/body/Limitations.xlsx`
- **Format**: Excel spreadsheet
- **Content**:
  - Range limit (m) - maximum allowable range
  - Stability margin limit - minimum required static stability
- **Use**: Simulation validity checks

### 3.3 Path Configuration
- **File**: `ASRI_Simulator/Path.txt`
- **Content**: Single line with working directory path
- **Current Value**: `C:\Users\user\desktop`
- **Issue**: HARDCODED Windows path, major portability problem

---

## 4. Processing and Algorithms

### 4.1 Initialization Phase

#### 4.1.1 Data Loading
1. Read `Path.txt` to get working directory
2. Load atmosphere data from Excel
3. Load mass properties from Excel (pre-computed by calculator)
4. Load thrust curve data (hybrid or liquid)
5. Load aerodynamic databases (RASAero or DATCOM)
6. Load wind profile
7. Parse UI inputs

#### 4.1.2 Pre-Processing
1. **Mass Properties Calculator** (`calculator.pyw`):
   - Compute fuel grain mass, COM, MOI as function of time
   - Compute oxidizer mass, COM, MOI as function of time
   - Combine with dry mass properties
   - Export time series to `mass_properties.xlsx`

2. **Thrust Curve Fitting** (`thrust_curve_fit.pyw`):
   - Load raw thrust data
   - Fit polynomial (user-specified degree)
   - Support multiple basis functions: Polynomial, Chebyshev, Hermite, Laguerre, Legendre
   - Selected: Chebyshev (best balance of accuracy and smoothness)

3. **Aerodynamic Table Preparation** (`aerodynamics.pyw`):
   - Load RASAero or DATCOM Excel files
   - Reshape into 2D lookup matrices: CA(Mach, Alpha), CN(Mach, Alpha), COP(Mach, Alpha)
   - Convert units (inches to meters for COP)
   - Create interpolation functions (scipy.interpolate.interp2d)
   - Separate tables for 0° and 15° fin configurations

4. **Wind Coordinate Transformation** (`wind.pyw`):
   - Convert (magnitude, bearing) to (North component, East component)
   - Formula:
     - Magnitude1 = magnitude × cos(bearing)
     - Magnitude2 = -magnitude × sin(bearing)

5. **Monte Carlo Setup** (`monte_carlo.pyw`):
   - Generate random samples from truncated normal distribution
   - Create variation arrays for all uncertainty parameters
   - Population size: user-specified

#### 4.1.3 Initial State Vector
1. **Position** (Geodetic):
   - Latitude = User input
   - Longitude = User input
   - Altitude = User input + rail offset

2. **Velocity** (NED frame):
   - Vn = V₀ × sin(elevation) × cos(azimuth)
   - Ve = V₀ × sin(elevation) × sin(azimuth)
   - Vd = -V₀ × cos(elevation)
   - V₀ ≈ 0 (stationary on rail)

3. **Orientation** (Quaternion):
   - Aligned with launch rail (elevation, azimuth)
   - Computed from Euler angles

4. **Angular Velocity**:
   - ω = [0, 0, 0] (stationary on rail)

### 4.2 Integration Loop

The simulator uses either fixed-step or adaptive ODE solvers to integrate the state equations.

#### 4.2.1 State Derivative Function (Core Physics)

For each time step, compute derivatives of 12 state variables:

**Inputs to derivative function**:
- Current time t
- Current state vector y[12]

**Processing**:

1. **Read Time-Varying Properties**:
   - Interpolate mass(t) from mass properties table
   - Interpolate COM(t), Ixx(t), Iyy(t), Izz(t)
   - Evaluate thrust(t) from fitted curve

2. **Geometric Calculations**:
   - Reference area: Sref = π × R_body²
   - Compute current altitude from geodetic position
   - Earth radius (function of latitude for WGS84)

3. **Atmospheric Properties**:
   - Interpolate ρ(altitude), P(altitude), T(altitude)
   - Speed of sound: a = √(γ × R × T), γ=1.4, R=287 J/(kg·K)

4. **Kinematics**:
   - Extract quaternion [w,x,y,z] = y[8:12]
   - Construct rotation matrix from quaternion
   - Transform velocity from NED to body frame:
     - V_body = R^T × V_NED

5. **Wind Velocity**:
   - Interpolate wind(altitude) → [wind_N, wind_E, 0]
   - If turbulence enabled: Add Dryden turbulence
   - If jetstream enabled: Add jetstream component

6. **Relative Velocity**:
   - V_rel = V_body - R^T × V_wind
   - Magnitude: V_a = |V_rel|
   - Mach number: M = V_a / a

7. **Angle of Attack and Sideslip**:
   - Total angle of attack: α_total = atan(√(V_rel_y² + V_rel_z²) / V_rel_x)
   - Roll angle of attack: φ = atan2(V_rel_z, V_rel_y)

8. **Aerodynamic Coefficient Lookup**:
   - If α_total < 15°:
     - [CA, CN, COP] = Interpolate(M, α_total) from standard table
   - Else:
     - [CA, CN, COP] = Interpolate(M, α_total) from 15° table
   - Apply Monte Carlo variations (if enabled):
     - CA *= (1 + Variation_drag)
     - CN *= (1 + Variation_lift)
     - COP *= (1 + Variation_COP)

9. **Dynamic Pressure**:
   - q = 0.5 × ρ × V_a²

10. **Aerodynamic Forces** (Body Frame):
    - Axial force: F_axial = -q × Sref × CA
    - Normal force magnitude: F_normal = q × Sref × CN
    - Normal force direction: perpendicular to V_rel in body frame
    - Components:
      - F_x = F_axial
      - F_y = F_normal × sin(φ)
      - F_z = -F_normal × cos(φ)

11. **Fin Forces and Moments** (`fins.pyw`):
    - Compute fin normal force coefficient (function of M, α, fin geometry)
    - Fin induced drag: Cdp_fin
    - Roll moment from cant angle: L_fin
    - Roll damping: L_damp
    - Add to total aerodynamic forces and moments

12. **Pitch/Yaw Damping** (`sidedamping.pyw`):
    - Equivalent diameter from rocket geometry
    - Pitch damping coefficient: C_mq
    - Yaw damping coefficient: C_nr
    - Pitch damping moment: M_damp = C_mq × q_pitch
    - Yaw damping moment: N_damp = C_nr × r_yaw

13. **Thrust**:
    - If t < burnout_time:
      - Thrust magnitude: T = thrust_curve(t) × (1 + Variation_thrust_mag)
      - Thrust vector (body frame):
        - Nominal: [T, 0, 0]
        - With misalignment: Apply rotation by (pitch_misalign, yaw_misalign)
      - Pressure thrust: T_pressure = (P_chamber - P_ambient) × A_exit
      - Total thrust: T_total = T_momentum + T_pressure
    - Else:
      - T = 0

14. **Gravity**:
    - If WGS84: g = EllipseGravity(altitude, latitude)
    - Else: g = -GM / (R + altitude)²
    - Gravity vector (NED frame): [0, 0, g]
    - Transform to body frame: g_body = R^T × g_NED

15. **Total Forces** (Body Frame):
    - F = F_aero + F_thrust + m × g_body

16. **Acceleration** (Body Frame):
    - a_body = F / m

17. **Transform Acceleration to NED**:
    - a_NED = R × a_body

18. **Position Derivatives**:
    - dLat/dt = V_N / (R_Earth + altitude)
    - dLon/dt = V_E / ((R_Earth + altitude) × cos(latitude))
    - dAlt/dt = -V_D

19. **Aerodynamic Moments** (Body Frame):
    - Moment arm: r_CP = COP - COM
    - M_aero = r_CP × F_aero
    - Add pitch/yaw damping moments
    - Add fin roll moment

20. **Roll Control Moments** (if enabled):
    - If roll_rate < lower_threshold OR roll_rate > upper_threshold:
      - Fire thruster → M_x = ±F_thruster × arm
    - Pulse width modulation at specified frequency

21. **Total Moments**:
    - M = M_aero + M_control + M_damping

22. **Angular Acceleration**:
    - Euler's equations:
      - Ixx × dω_x/dt = M_x + (Iyy - Izz) × ω_y × ω_z
      - Iyy × dω_y/dt = M_y + (Izz - Ixx) × ω_z × ω_x
      - Izz × dω_z/dt = M_z + (Ixx - Iyy) × ω_x × ω_y

23. **Quaternion Derivative**:
    - dq/dt = 0.5 × q ⊗ ω
    - Where ⊗ is quaternion multiplication

24. **Launch Rail Constraint**:
    - If on rail (distance traveled < rail_length):
      - Force all motion along rail axis
      - Constrain rotations
      - Check rail departure condition: V > V_min AND distance > L_rail

25. **Parachute Deployment**:
    - If conditions met (altitude < threshold OR time > delay):
      - Replace aerodynamic model with parachute drag:
        - F_drag = 0.5 × ρ × V² × CD_chute × A_chute
      - Lock attitude (quaternion frozen)
      - Disable thrust

26. **Staging Events**:
    - If t = stage_time:
      - Subtract stage mass
      - Update COM, MOI
      - Switch to separated aerodynamic tables (nose or booster)
      - Optionally deploy staging parachute

27. **Turbulence Model** (`wind.pyw`):
    - Dryden spectral model:
      - Turbulence state equation (2nd order filter)
      - Driven by Gaussian white noise
      - Length scale: L_t (default 150 m)
      - Intensity: σ_t (default 10 m/s)
      - Output: turbulence velocity components

28. **Output State Derivatives**:
    - Return dy/dt[12]:
      - [dV_N/dt, dV_E/dt, dV_D/dt, dω_x/dt, dω_y/dt, dω_z/dt, dLat/dt, dLon/dt, dq_w/dt, dq_x/dt, dq_y/dt, dq_z/dt]

#### 4.2.2 Event Handling

**Rail Departure**:
- Monitor: Distance traveled = ∫V dt
- Condition: Distance ≥ rail_length
- Action: Switch from 1-DOF to 6-DOF dynamics, print message

**Burnout**:
- Condition: t ≥ burnout_time
- Action: Set thrust = 0, print message

**Apogee**:
- Monitor: Vertical velocity V_D
- Condition: V_D changes sign (negative to positive)
- Action: Record apogee altitude, print message, optionally deploy drogue

**Parachute Deployment**:
- Condition: (altitude < deploy_altitude) OR (time > deploy_time)
- Action: Switch drag model, print message

**Angle of Attack Limit**:
- Monitor: α_total
- Condition: α_total > max_allowed (e.g., 20°)
- Action: Print warning (aerodynamic data may be invalid)

**Stability Warning**:
- Compute: Static margin = (COP - COM) / diameter
- Condition: Margin < minimum_stable
- Action: Print warning

**Ground Impact**:
- Condition: altitude ≤ 0
- Action: Terminate integration

#### 4.2.3 Integration Methods

**Fixed-Step Solvers** (`fixed_step_solver.pyw`):
- **RK2**: 2nd-order Runge-Kutta
- **RK4**: 4th-order Runge-Kutta
- **RK8**: 8th-order Runge-Kutta
- Time step: Constant, user-specified
- Pros: Predictable runtime, simple
- Cons: Must use small step for accuracy, inefficient

**Adaptive Solvers** (`main.pyw`):
- **RK45**: Runge-Kutta-Fehlberg (4th/5th order)
- **DOP853**: Dormand-Prince 8th order
- Time step: Variable, automatically adjusted
- Error control: User-specified relative and absolute tolerances
- Pros: Efficient, accurate
- Cons: Unpredictable runtime

**Solver Selection**:
- Fixed-step: Better for Monte Carlo (consistent timing)
- Adaptive: Better for high-fidelity single runs

### 4.3 Monte Carlo Processing

**Algorithm** (`monte_carlo.pyw`):

1. Generate random samples:
   - N = number of runs (user input)
   - For each uncertainty parameter:
     - Generate N samples from truncated normal distribution
     - Range: [lower_limit, upper_limit]
     - Distribution: μ=0, σ=1.1, truncated at ±0.5σ

2. For each run i = 1 to N:
   - Apply variations to nominal values:
     - Elevation = Elevation_nom + variation[i] × Δ_elevation
     - Thrust_mag = Thrust_nom × (1 + variation[i] × Δ_thrust_percent)
     - ... (all 14 uncertainty parameters)

   - Run simulation with perturbed inputs

   - Record outputs:
     - Apogee altitude
     - Max Mach number
     - Max acceleration
     - Max angle of attack
     - Landing position (Lat, Lon)
     - Range from launch site
     - Flight time
     - etc.

3. Statistical Analysis:
   - Compute mean, std dev, min, max for each output
   - Generate scatter plots (landing positions)
   - Generate probability ellipses (e.g., 99% confidence)
   - Export full dataset to CSV

### 4.4 Post-Processing and Output Generation

**Data Collection**:
- During integration, append state data to lists at specified intervals
- Full state vector + derived quantities
- Interval: Every N steps or every Δt seconds

**Derived Quantities**:
- Altitude above ground
- Velocity magnitude
- Flight path angle
- Heading
- Acceleration magnitude
- Mach number
- Dynamic pressure
- Angle of attack
- Stability margin
- Thrust magnitude
- Drag force
- Lift force
- etc.

**Output Formatting**:
- Create Pandas DataFrame
- Columns: time, position (Lat/Lon/Alt), velocity, orientation, derived quantities
- Export to Excel or CSV

**Plotting** (`graphics_library.pyw`):
- 3D trajectory visualization
- Altitude vs. time
- Velocity vs. time
- Mach vs. time
- Angle of attack vs. time
- Stability margin vs. time
- Acceleration vs. time
- etc.

**Monte Carlo Plots** (`monte_carlo_plot.pyw`):
- Landing scatter plot (Lat vs. Lon)
- Apogee histogram
- Range histogram
- Probability contours
- Statistical summary table

---

## 5. Output Specifications

### 5.1 Simulation Outputs

#### 5.1.1 Time-Series Data
**File Format**: Excel (.xlsx) or CSV
**Structure**: Rows = time steps, Columns = variables

**Primary State Variables**:
- time (s)
- Latitude (deg)
- Longitude (deg)
- Altitude (m)
- Velocity North (m/s)
- Velocity East (m/s)
- Velocity Down (m/s)
- Angular velocity roll (rad/s)
- Angular velocity pitch (rad/s)
- Angular velocity yaw (rad/s)
- Quaternion w, x, y, z

**Derived Quantities**:
- Velocity magnitude (m/s)
- Flight path angle (deg)
- Heading (deg)
- Acceleration North, East, Down (m/s²)
- Acceleration magnitude (m/s²)
- Mach number
- Dynamic pressure (Pa)
- Angle of attack (deg)
- Sideslip angle (deg)
- Roll angle (deg)
- Pitch angle (deg)
- Yaw angle (deg)
- Thrust (N)
- Drag force (N)
- Normal force (N)
- Center of pressure (m)
- Center of gravity (m)
- Static margin (calibers)
- Mass (kg)
- Moments of inertia (kg·m²)

**Optional Outputs** (can be enabled):
- Individual force components
- Individual moment components
- Aerodynamic coefficients
- Wind velocity components
- Turbulence contributions
- Control system states

#### 5.1.2 Summary Outputs
Printed to console and optionally to file:

- **Launch Conditions**:
  - Launch site (Lat, Lon, Alt)
  - Launch azimuth, elevation
  - Rail length

- **Key Events**:
  - Rail departure time, velocity
  - Burnout time, altitude, velocity
  - Apogee time, altitude
  - Parachute deployment time, altitude
  - Landing time, position, velocity

- **Maximum Values**:
  - Max altitude (apogee)
  - Max velocity
  - Max Mach number
  - Max acceleration
  - Max dynamic pressure
  - Max angle of attack
  - Max range

- **Landing**:
  - Landing position (Lat, Lon)
  - Range from launch site (m)
  - Bearing to landing site (deg)
  - Impact velocity (m/s)

- **Stability**:
  - Minimum static margin (during flight)
  - Time of minimum margin

#### 5.1.3 Graphical Outputs
**3D Trajectory Plot**:
- X-axis: East (m)
- Y-axis: North (m)
- Z-axis: Altitude (m)
- Includes launch rail, launch site marker

**Time-History Plots** (multiple subplots):
- Altitude vs. time
- Velocity magnitude vs. time
- Mach number vs. time
- Acceleration magnitude vs. time
- Angle of attack vs. time
- etc.

**File Format**: PNG, PDF, or interactive (matplotlib)

### 5.2 Monte Carlo Outputs

#### 5.2.1 Landing Dispersion
**Plot**: Scatter plot of landing positions
- X-axis: East offset from launch (m)
- Y-axis: North offset from launch (m)
- Each point = one Monte Carlo run
- Overlays:
  - Mean landing position
  - 1σ, 2σ, 3σ ellipses
  - Convex hull (maximum dispersion)

**Data File**: CSV with columns:
- Run number
- Landing Lat, Lon
- East offset, North offset
- Range, bearing

#### 5.2.2 Statistical Distributions
**Histograms** for key metrics:
- Apogee altitude
- Max Mach
- Max acceleration
- Range
- Flight time

**Statistics** (for each metric):
- Mean
- Standard deviation
- Minimum
- Maximum
- 1st, 25th, 50th, 75th, 99th percentiles

#### 5.2.3 Detailed Monte Carlo Output
If "MC Detailed" enabled:
- **Full dataset**: All time-series data for all runs
- **File size**: Can be very large (GB for large N)
- **Format**: Multi-sheet Excel or HDF5

### 5.3 Intermediate Outputs

**Mass Properties File**:
- Generated by: `calculator.pyw`
- File: `Inputs/mass_properties.xlsx`
- Used as input for main simulation

**Aerodynamic Conversion**:
- MissileDATCOM.txt → MissileDATCOM.xlsx
- Parsed and reformatted for easier import

---

## 6. Current System Issues and Limitations

### 6.1 Performance Issues
1. **Very slow execution**: ~minutes for single run, hours for Monte Carlo
2. **Inefficient data structures**: Global variables, excessive list appends
3. **Repeated file I/O**: Reading JSON files every integration step
4. **Inefficient aerodynamic interpolation**: Creating interpolators every call
5. **Unoptimized numerical methods**: Fixed-step with very small time steps

### 6.2 Code Quality Issues
1. **Hardcoded paths**: Windows-specific absolute paths (e.g., `C:\Users\user\desktop`)
2. **Non-modular design**: Monolithic files (2500+ lines), deeply nested functions
3. **Excessive global variables**: 200+ globals, making debugging difficult
4. **Poor naming**: Single-letter variables, inconsistent conventions
5. **No documentation**: Minimal comments, no docstrings
6. **No testing**: No unit tests, validation tests, or regression tests
7. **Dead code**: Commented-out sections, unused functions

### 6.3 Portability Issues
1. **Windows-only**: .pyw files, Windows path conventions
2. **Hardcoded directory**: `Path.txt` contains `C:\Users\user\desktop`
3. **OS-specific assumptions**: File path separators, line endings
4. **Excel dependency**: All data files in .xlsx format (requires openpyxl)

### 6.4 Maintainability Issues
1. **Monolithic structure**: All physics in single ODE function
2. **Tight coupling**: Hard to replace components (e.g., aerodynamics model)
3. **No separation of concerns**: UI, simulation logic, I/O all mixed
4. **Inconsistent state management**: Some state in files, some in globals
5. **No version control indicators**: No Git history, branching unclear

### 6.5 Numerical Issues
1. **Quaternion normalization**: May drift over long integration times
2. **Coordinate singularities**: Gimbal lock potential if using Euler angles incorrectly
3. **Integration tolerances**: Fixed-step may accumulate errors
4. **Interpolation extrapolation**: No bounds checking on table lookups

### 6.6 Physical Model Limitations
1. **Rigid body assumption**: No structural dynamics, sloshing
2. **Instantaneous parachute deployment**: No deployment dynamics, shock loads
3. **Point mass aerodynamics**: No distributed loads
4. **No atmospheric variability**: Single atmosphere profile
5. **Simplified turbulence**: Dryden model is basic

### 6.7 User Experience Issues
1. **Complex UI**: 100+ input fields, overwhelming
2. **No input validation**: Can enter physically invalid values
3. **Cryptic error messages**: Hard to diagnose failures
4. **No undo/redo**: Manual re-entry of inputs
5. **No configuration save/load**: Must re-enter all parameters

### 6.8 Data Management Issues
1. **Excel for everything**: Not suitable for large datasets
2. **No data provenance**: Hard to track which inputs generated which outputs
3. **Overwriting outputs**: No automatic versioning or timestamping
4. **No metadata**: Output files lack information about simulation setup

---

## 7. System Requirements Summary

### 7.1 Functional Requirements (High-Level)
1. **FR-1**: Simulate 6-DOF rocket trajectory from launch to landing
2. **FR-2**: Support hybrid and liquid rocket propulsion systems
3. **FR-3**: Model time-varying mass properties during propellant consumption
4. **FR-4**: Integrate external aerodynamic prediction tools (RASAero, DATCOM)
5. **FR-5**: Support multi-stage vehicles with separation events
6. **FR-6**: Model parachute recovery systems (main, drogue)
7. **FR-7**: Perform Monte Carlo uncertainty analysis
8. **FR-8**: Model active roll control systems
9. **FR-9**: Support altitude-varying atmospheric and wind profiles
10. **FR-10**: Provide 3D trajectory visualization and statistical analysis

### 7.2 Non-Functional Requirements
1. **NFR-1 Performance**: Single run should complete in <10 seconds
2. **NFR-2 Scalability**: 1000-run Monte Carlo should complete in <2 hours
3. **NFR-3 Portability**: Cross-platform (Windows, macOS, Linux)
4. **NFR-4 Maintainability**: Modular design, documented, tested
5. **NFR-5 Usability**: Intuitive UI, input validation, helpful error messages
6. **NFR-6 Reliability**: Numerically stable, validated against test data
7. **NFR-7 Extensibility**: Easy to add new models (e.g., different aerodynamics)

### 7.3 Data Requirements
1. **DR-1**: Support standard atmosphere models (US Standard, custom tables)
2. **DR-2**: Support RASAero II and MissileDATCOM aerodynamic databases
3. **DR-3**: Support various thrust curve formats (time-series, pressure-thrust)
4. **DR-4**: Import/export in common formats (CSV, JSON, HDF5, Excel)
5. **DR-5**: Provide data validation and range checking

### 7.4 Interface Requirements
1. **IR-1**: Graphical user interface for configuration
2. **IR-2**: Command-line interface for batch/Monte Carlo runs
3. **IR-3**: Python API for programmatic access
4. **IR-4**: Export data in formats compatible with analysis tools (MATLAB, Python)

---

## 8. Validation and Verification Needs

### 8.1 Verification (Are we building the system right?)
1. **Unit Tests**: Test individual functions (e.g., coordinate transformations, aerodynamics lookups)
2. **Integration Tests**: Test subsystems (e.g., mass properties calculator)
3. **Regression Tests**: Ensure changes don't break existing functionality
4. **Code Coverage**: Aim for >80% test coverage

### 8.2 Validation (Are we building the right system?)
1. **Test Cases**: Compare against known analytical solutions (e.g., ballistic trajectory)
2. **Benchmark Data**: Validate against other simulators (OpenRocket, RocketPy, HYROPS)
3. **Flight Data**: Compare predictions with actual flight test results
4. **Sensitivity Analysis**: Verify physical reasonableness of parameter sensitivities

### 8.3 Acceptance Criteria
1. Trajectory predictions within 5% of flight test data (for validated rockets)
2. Monte Carlo landing dispersion within 10% of observed dispersion
3. Apogee prediction within 3% or 100m (whichever is greater)
4. All test cases pass with numerical error < 0.1%

---

## 9. Technical Specifications Summary

### 9.1 State Vector (12 DOF)
- 3 translational velocities (NED frame)
- 3 angular velocities (body frame)
- 2 position coordinates (geodetic)
- 4 orientation parameters (quaternion)

### 9.2 Reference Frames
- NED (North-East-Down): Kinematic velocities, position rates
- Body-Fixed: Forces, moments, angular velocities
- Geodetic: Position (lat/lon/alt)

### 9.3 Key Physical Models
- **Gravity**: Spherical or WGS84 ellipsoid
- **Atmosphere**: Tabulated (altitude-dependent)
- **Aerodynamics**: 2D lookup tables (Mach, AOA) from external tools
- **Propulsion**: Polynomial-fitted thrust curves
- **Mass Properties**: Tabulated time-series
- **Wind**: Altitude profile + turbulence + jetstream
- **Fins**: Barrowman analytical model
- **Damping**: Empirical formulas based on geometry

### 9.4 Numerical Methods
- **Integration**: RK2/4/8 (fixed), RK45/DOP853 (adaptive)
- **Interpolation**: Linear (1D), bilinear (2D)
- **Curve Fitting**: Orthogonal polynomials (Chebyshev, etc.)
- **Monte Carlo**: Truncated normal sampling

### 9.5 Typical Performance
- **Single Run**: 1-5 minutes (current system, slow!)
- **Monte Carlo (1000 runs)**: 24-48 hours (current system, very slow!)
- **Apogee**: Typically 10-50 km
- **Max Mach**: Typically 2-5
- **Flight Duration**: 200-600 seconds

---

## 10. Glossary

**6-DOF**: Six Degrees of Freedom (3 translational + 3 rotational)
**AOA**: Angle of Attack
**CAD**: Computer-Aided Design
**COM**: Center of Mass
**COP**: Center of Pressure
**DATCOM**: Data Compendium (USAF aerodynamic prediction tool)
**DOP853**: Dormand-Prince 8th-order ODE solver
**ECI**: Earth-Centered Inertial frame
**MOI**: Moment of Inertia
**NED**: North-East-Down reference frame
**ODE**: Ordinary Differential Equation
**RASAero**: Rocket Aero Software (aerodynamic prediction tool)
**RK45**: Runge-Kutta-Fehlberg 4th/5th order
**WGS84**: World Geodetic System 1984 (Earth ellipsoid model)

---

## End of Document

This requirements and specifications document provides a comprehensive description of the PyROPS v2.3.12 rocket simulation system. It serves as the foundation for evaluating alternative solutions and making informed decisions about future development directions.

**Document Version**: 1.0
**Date**: 2025-10-19
**Prepared by**: Technical Analysis - Claude Code
