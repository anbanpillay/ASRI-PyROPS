# Benchmark Test Case Template

## Test Case ID: BM-XXX

**Test Name**: [Descriptive name]

**Purpose**: [What aspect of physics/functionality this test validates]

**Priority**: [Critical / High / Medium / Low]

**Created By**: [Name]
**Date**: [YYYY-MM-DD]
**Last Updated**: [YYYY-MM-DD]

---

## Test Configuration

### Launch Site
- **Latitude**: [degrees]
- **Longitude**: [degrees]
- **Altitude**: [meters MSL]

### Launch Conditions
- **Elevation Angle**: [degrees from horizontal]
- **Azimuth**: [degrees, counter-clockwise from North]
- **Rail Length**: [meters]
- **Launch Date/Time**: [if specific atmosphere needed]

### Rocket Configuration

**Geometry**:
- Body Radius: [m]
- Body Length: [m]
- Nose Type: [ogive/conical/etc]
- Nose Length: [m]

**Mass Properties (Dry)**:
- Mass: [kg]
- Center of Mass (x,y,z): [m from nose tip or other reference]
- Moments of Inertia (Ixx, Iyy, Izz): [kg⋅m²]

**Fins**:
- Number of Fins: [typically 4]
- Root Chord: [m]
- Tip Chord: [m]
- Span: [m]
- Sweep: [m]
- Location: [m from nose]
- Cant Angle: [degrees]

### Propulsion System

**Motor Type**: [Solid / Hybrid / Liquid]

**Hybrid Motor** (if applicable):
- Burn Time: [s]
- Fuel Grain:
  - Density: [kg/m³]
  - Outer Radius: [m]
  - Initial Inner Radius: [m]
  - Length: [m]
  - Center of Mass: [m]
- Oxidizer:
  - Type: [N2O, LOX, etc.]
  - Density: [kg/m³]
  - Initial Volume/Length: [m³ or m]
  - Center of Mass: [m]
- Nozzle:
  - Exit Area: [m²]
  - Throat Area: [m²]
  - Exit Radius: [m]

**Thrust Curve**:
- Source File: `BM-XXX/thrust_curve.csv` or `.xlsx`
- Peak Thrust: [N]
- Total Impulse: [N⋅s]
- Average Thrust: [N]

**Mass Properties (Propellant)**:
- Source File: `BM-XXX/mass_properties.csv`
- Initial Wet Mass: [kg]
- Final Dry Mass: [kg]
- Propellant Mass: [kg]

### Aerodynamics

**Data Source**: [RASAero II / MissileDATCOM / Custom]

**Files**:
- Standard (0° cant): `BM-XXX/aerodynamics_0deg.csv`
- 15° cant (if applicable): `BM-XXX/aerodynamics_15deg.csv`
- Nose (if separated): `BM-XXX/aerodynamics_nose.csv`
- Booster (if separated): `BM-XXX/aerodynamics_booster.csv`

**Mach Range**: [min - max]
**Alpha Range**: [min° - max°]
**Reference Area**: [m²]

### Environment

**Atmosphere**:
- Model: [Standard / Custom]
- Source File (if custom): `BM-XXX/atmosphere.csv`
- Surface Temperature: [K]
- Surface Pressure: [Pa]

**Wind**:
- Model: [Constant / Altitude-varying / None]
- Source File (if varying): `BM-XXX/wind_profile.csv`
- Surface Wind Speed: [m/s]
- Surface Wind Direction: [degrees]

**Turbulence**:
- Enabled: [Yes / No]
- Model: [Dryden / None]
- Intensity: [m/s]
- Length Scale: [m]

### Recovery System

**Main Parachute**:
- Drag Coefficient: [dimensionless]
- Diameter: [m]
- Deployment Trigger: [Apogee / Altitude / Time]
- Deployment Delay: [s]
- Deployment Altitude: [m] (if altitude trigger)

**Drogue Parachute** (if applicable):
- Drag Coefficient: [dimensionless]
- Diameter: [m]
- Deployment Trigger: [Apogee / Altitude / Time]
- Deployment Delay: [s]

### Staging (if applicable)

**Number of Stages**: [1 / 2 / 3]

**Stage Separation**:
- Separation Time: [s]
- Separation Delay: [s]
- Jettisoned Mass: [kg]

### Simulation Settings

**Numerical Integration**:
- Solver: [RK45 / DOP853 / RK4 fixed]
- Time Step: [s] (if fixed)
- Max Time: [s]
- Relative Tolerance: [if adaptive]
- Absolute Tolerance: [if adaptive]

**Physics Options**:
- Gravity Model: [Spherical / WGS84]
- Coordinate System: [NED / ECI / Other]
- Atmosphere Model: [as above]

---

## Expected Results (PyROPS Reference)

**Simulation Run Info**:
- PyROPS Version: v2.3.12
- Run Date: [YYYY-MM-DD]
- Run Time: [seconds]
- Solver: [RK45 / RK4 / etc.]

### Key Events

**Rail Departure**:
- Time: [s]
- Velocity: [m/s]
- Altitude: [m]

**Burnout**:
- Time: [s]
- Velocity: [m/s]
- Altitude: [m]
- Mach Number: [dimensionless]

**Apogee**:
- Time: [s]
- Altitude: [m]
- Latitude: [degrees]
- Longitude: [degrees]

**Parachute Deployment**:
- Time: [s]
- Altitude: [m]
- Velocity: [m/s]

**Landing**:
- Time: [s]
- Latitude: [degrees]
- Longitude: [degrees]
- Impact Velocity: [m/s]
- Range from Launch: [m]
- Bearing from Launch: [degrees]

### Maximum Values

- **Max Velocity**: [m/s]
- **Max Acceleration**: [m/s²]
- **Max Mach Number**: [dimensionless]
- **Max Dynamic Pressure**: [Pa]
- **Max Angle of Attack**: [degrees]
- **Max Altitude**: [m] (should equal apogee)

### Trajectory Characteristics

- **Total Flight Time**: [s]
- **Minimum Stability Margin**: [calibers]
- **Flight Regime**: [Subsonic / Transonic / Supersonic]
- **Peak Stability Margin**: [calibers]

### Data Files

**Reference Files** (from PyROPS):
- Full Trajectory CSV: `BM-XXX/pyrops_trajectory.csv`
- Results JSON: `BM-XXX/pyrops_reference.json`
- Plots: `BM-XXX/plots/` (altitude, velocity, trajectory, etc.)

---

## Validation Criteria

### Pass/Fail Thresholds

| Parameter | Tolerance | Rationale |
|-----------|-----------|-----------|
| Apogee Altitude | ±0.1% or ±10m | Most critical metric |
| Max Velocity | ±0.1% | High sensitivity to thrust |
| Max Mach | ±0.1% | Affects aerodynamics |
| Burnout Altitude | ±1% | Less critical |
| Landing Latitude | ±0.001° (~100m) | Acceptable GPS-level |
| Landing Longitude | ±0.001° (~100m) | Acceptable GPS-level |
| Impact Velocity | ±5% | Recovery critical |
| Flight Time | ±1% | Overall trajectory |

### Additional Checks

- [ ] No simulation crashes or errors
- [ ] All state variables remain physical (no NaN, Inf, negative altitude, etc.)
- [ ] Trajectory is smooth (no discontinuities)
- [ ] Energy conservation approximately holds (KE + PE + work ≈ constant accounting for drag)
- [ ] Stability margin > 1.0 throughout flight (if required)

---

## Test Execution

### PyROPS Execution

**Date Run**: [YYYY-MM-DD]
**Run By**: [Name]

**Steps**:
1. Open PyROPS launcher
2. Load parameters from this specification
3. Verify all input files in correct location
4. Run simulation
5. Export results to CSV
6. Save plots
7. Record key metrics in `pyrops_reference.json`

**Status**: [ ] Not Run [ ] In Progress [X] Complete

**Notes**: [Any observations, warnings, issues]

---

### RocketPy Execution

**Date Run**: [YYYY-MM-DD]
**Run By**: [Name]

**Steps**:
1. Convert data files to RocketPy format (if not already done)
2. Create RocketPy simulation script: `BM-XXX/simulate_bm_xxx.py`
3. Run: `python simulate_bm_xxx.py`
4. Export results to CSV
5. Generate plots
6. Record key metrics in `rocketpy_results.json`

**Status**: [ ] Not Run [ ] In Progress [X] Complete

**Notes**: [Any observations, parameter tuning needed]

---

### Validation Results

**Date Validated**: [YYYY-MM-DD]
**Validated By**: [Name]

**Comparison**:

| Parameter | PyROPS | RocketPy | Difference | % Diff | Pass/Fail |
|-----------|--------|----------|------------|--------|-----------|
| Apogee (m) | | | | | |
| Max Velocity (m/s) | | | | | |
| Max Mach | | | | | |
| Landing Lat (°) | | | | | |
| Landing Lon (°) | | | | | |
| Impact Velocity (m/s) | | | | | |
| Flight Time (s) | | | | | |

**Overall Result**: [ ] PASS [ ] FAIL [ ] CONDITIONAL PASS

**Physics Team Sign-Off**:
- Name: [_________________]
- Date: [_________________]
- Signature: [_________________]

---

## Discrepancy Analysis

### Identified Differences

**Difference 1**: [Description]
- **Magnitude**: [value]
- **Likely Cause**: [hypothesis]
- **Action Taken**: [what was done]
- **Resolution**: [outcome]

**Difference 2**: [Description]
- [...]

### Accepted Deviations

If any parameters fail validation but are accepted by physics team:

- **Parameter**: [name]
- **Deviation**: [amount]
- **Justification**: [why accepted]
- **Risk Assessment**: [impact]
- **Approved By**: [name, date]

---

## Lessons Learned

- [Lesson 1]
- [Lesson 2]
- [...]

---

## Files Checklist

**Input Files** (in `rocketpy_migration/benchmarks/BM-XXX/`):
- [ ] `README.md` (this file)
- [ ] `thrust_curve.csv` or `.xlsx`
- [ ] `mass_properties.csv` or `.xlsx`
- [ ] `aerodynamics_0deg.csv`
- [ ] `aerodynamics_15deg.csv` (if applicable)
- [ ] `atmosphere.csv` (if custom)
- [ ] `wind_profile.csv` (if not constant)

**PyROPS Reference** (in `BM-XXX/pyrops_reference/`):
- [ ] `pyrops_reference.json` (key metrics)
- [ ] `pyrops_trajectory.csv` (full time-series)
- [ ] `plots/altitude_vs_time.png`
- [ ] `plots/velocity_vs_time.png`
- [ ] `plots/trajectory_map.png`

**RocketPy Results** (in `BM-XXX/rocketpy_results/`):
- [ ] `simulate_bm_xxx.py` (simulation script)
- [ ] `rocketpy_results.json` (key metrics)
- [ ] `rocketpy_trajectory.csv` (full time-series)
- [ ] `plots/altitude_vs_time.png`
- [ ] `plots/velocity_vs_time.png`
- [ ] `plots/trajectory_map.png`

**Validation** (in `BM-XXX/`):
- [ ] `validation_report.md` (comparison analysis)
- [ ] `validation_plots/` (overlay plots showing PyROPS vs RocketPy)

---

## Notes

[Any additional notes, special considerations, references to related tests, etc.]

---

**Test Status**: [ ] Not Started [ ] In Progress [ ] Complete [ ] Validated [ ] Approved

**Last Updated By**: [Name]
**Last Updated Date**: [YYYY-MM-DD]
