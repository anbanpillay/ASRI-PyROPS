# Benchmark Test Case: BM-001

## Test Case ID: BM-001

**Test Name**: Baseline Nominal Hybrid Rocket Flight

**Purpose**: Primary validation test case for standard hybrid rocket configuration

**Priority**: ⭐ CRITICAL - This is the "golden" reference test

**Created By**: Migration Team
**Date**: 2025-10-19
**Last Updated**: 2025-10-19

---

## Test Configuration

### Launch Site
- **Latitude**: -34.600° (South Africa region based on PyROPS default)
- **Longitude**: 20.300°
- **Altitude**: 0 m MSL

### Launch Conditions
- **Elevation Angle**: 80.0° (from horizontal)
- **Azimuth**: -100.0° (counter-clockwise from North, PyROPS convention)
- **Rail Length**: 7.0 m
- **Launch Date/Time**: Standard atmosphere (no specific date required)

### Rocket Configuration

**Geometry**:
- Body Radius: 0.087 m
- Body Length: 4.920 m
- Nose Type: Ogive (from RASAero data)
- Nose Length: TBD (from RASAero)

**Mass Properties (Dry)** - From PyROPS calculator.pyw:
- Mass: 49.35224149 kg
- Center of Mass: (1.386632, 0, 0) m from nose tip
- Moments of Inertia:
  - Ixx: 0.04023116 kg·m²
  - Iyy: 180.8297 kg·m²
  - Izz: 180.8297 kg·m²

**Fins** (from PyROPS launcher defaults):
- Number of Fins: 4
- Root Chord: TBD (check PyROPS UI or Settings.xlsx)
- Tip Chord: TBD
- Span: TBD
- Sweep: TBD
- Location: TBD m from nose
- Cant Angle: 0° (standard configuration)

### Propulsion System

**Motor Type**: Hybrid (Solid fuel + Liquid oxidizer)

**Hybrid Motor** (Phoenix 1BIIr from HYROPS model):
- **Burn Time**: 17.1 s
- **Fuel Grain**:
  - Density: 1065 kg/m³
  - Outer Radius: 0.0735 m
  - Initial Inner Radius: 0.0735 - 0.0375 = 0.0360 m
  - Thickness: 0.0375 m (initial)
  - Length: 0.51 m
  - Center of Mass: 0.5395 m from origin
- **Oxidizer**:
  - Type: Liquid (likely N2O or similar)
  - Density: 880 kg/m³
  - Outer Radius: 0.07633 m
  - Initial Length: 1.9869 m
  - Center of Mass: 2.20745 m from origin
- **Nozzle**:
  - Exit Area: 0.007056 m²
  - Exit Radius: √(0.007056/π) ≈ 0.0474 m
  - Throat Area: TBD

**Thrust Curve**:
- Source File: `thrust_curve_hybrid.xlsx`
- Peak Thrust: TBD (run PyROPS to determine)
- Total Impulse: TBD
- Average Thrust: TBD

**Mass Properties (Time-Varying)**:
- Source File: `mass_properties.xlsx`
- Initial Wet Mass: TBD (dry + propellant)
- Final Dry Mass: 49.35224149 kg
- Propellant Mass: TBD

### Aerodynamics

**Data Source**: RASAero II

**Files**:
- Standard (0° cant): `RASAeroII.xlsx`

**Mach Range**: 0.0 - TBD (check RASAero file)
**Alpha Range**: 0° - TBD°
**Reference Area**: π × (0.087)² ≈ 0.0238 m²

### Environment

**Atmosphere**:
- Model: Custom
- Source File: `atmosphere_data.xlsx`
- Surface Temperature: TBD (from file)
- Surface Pressure: TBD (from file)

**Wind**:
- Model: Altitude-varying
- Source File: `wind.xlsx`
- Surface Wind Speed: TBD (from file)
- Surface Wind Direction: TBD

**Turbulence**:
- Enabled: TBD (check PyROPS settings)
- Model: Dryden (if enabled)
- Intensity: TBD
- Length Scale: TBD

### Recovery System

**Main Parachute** (from PyROPS launcher defaults):
- Drag Coefficient: 2.2
- Diameter: 1.22052868353847 m
- Deployment Trigger: Altitude or Apogee
- Deployment Altitude: 13500 m (or possibly time-based)
- Deployment Delay: 5 s

**Drogue Parachute** (if applicable):
- Drag Coefficient: 1.6
- Diameter: 0.304871262610412 m
- Deployment: TBD

### Simulation Settings

**Numerical Integration**:
- Solver: RK45 adaptive (PyROPS default)
- Time Step: 0.02 s (initial)
- Max Time: 1200 s (20 minutes)
- Relative Tolerance: TBD
- Absolute Tolerance: TBD

**Physics Options**:
- Gravity Model: WGS84 or Spherical (check Settings.xlsx)
- Coordinate System: NED (North-East-Down)
- Atmosphere Model: Custom (from atmosphere_data.xlsx)

---

## Expected Results (PyROPS Reference)

**STATUS**: ⏳ PENDING - Need to run PyROPS

**To Complete**:
1. Launch PyROPS with parameters above
2. Run simulation
3. Export results
4. Fill in sections below

### Key Events

**Rail Departure**:
- Time: ___ s
- Velocity: ___ m/s
- Altitude: ___ m (should be ~7.0 m)

**Burnout**:
- Time: ~17.1 s (burn time)
- Velocity: ___ m/s
- Altitude: ___ m
- Mach Number: ___

**Apogee**:
- Time: ___ s
- Altitude: ___ m ⭐ PRIMARY METRIC
- Latitude: ___°
- Longitude: ___°

**Parachute Deployment**:
- Time: ___ s
- Altitude: ___ m
- Velocity: ___ m/s

**Landing**:
- Time: ___ s
- Latitude: ___°
- Longitude: ___°
- Impact Velocity: ___ m/s
- Range from Launch: ___ m
- Bearing from Launch: ___°

### Maximum Values

- **Max Velocity**: ___ m/s
- **Max Acceleration**: ___ m/s²
- **Max Mach Number**: ___
- **Max Dynamic Pressure**: ___ Pa
- **Max Angle of Attack**: ___°
- **Max Altitude**: ___ m (should equal apogee)

### Trajectory Characteristics

- **Total Flight Time**: ___ s
- **Minimum Stability Margin**: ___ calibers
- **Flight Regime**: Subsonic / Transonic / Supersonic
- **Peak Stability Margin**: ___ calibers

### Data Files

**Reference Files** (to be created after PyROPS run):
- [ ] Full Trajectory CSV: `pyrops_reference/pyrops_trajectory.csv`
- [ ] Results JSON: `pyrops_reference/pyrops_reference.json`
- [ ] Plots: `pyrops_reference/plots/`
  - [ ] altitude_vs_time.png
  - [ ] velocity_vs_time.png
  - [ ] trajectory_map.png

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
- [ ] All state variables remain physical (no NaN, Inf, negative altitude)
- [ ] Trajectory is smooth (no discontinuities)
- [ ] Energy conservation approximately holds
- [ ] Stability margin > 1.0 throughout flight

---

## Test Execution

### PyROPS Execution

**Date Run**: _____________
**Run By**: _____________

**Steps**:
1. [ ] Open PyROPS launcher (`ASRI_Simulator/launcher.pyw`)
2. [ ] Load parameters from this specification
3. [ ] Verify all input files in Inputs/ folder
4. [ ] Run simulation
5. [ ] Export results to CSV
6. [ ] Save plots
7. [ ] Record key metrics in `pyrops_reference.json`

**Status**: [ ] Not Run [ ] In Progress [ ] Complete

**Notes**:
_____________________________________________________________

---

### RocketPy Execution

**Date Run**: _____________
**Run By**: _____________

**Status**: [ ] Not Run [ ] In Progress [ ] Complete

**Notes**:
_____________________________________________________________

---

### Validation Results

**Date Validated**: _____________
**Validated By**: _____________

**Comparison Table**:

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
- Name: _________________
- Date: _________________
- Signature: _________________

---

## Files Checklist

**Input Files** (archived in `BM-001/`):
- [ ] `thrust_curve_hybrid.xlsx`
- [ ] `mass_properties.xlsx`
- [ ] `RASAeroII.xlsx`
- [ ] `atmosphere_data.xlsx`
- [ ] `wind.xlsx`
- [ ] `Settings.xlsx` (if needed)
- [ ] `side_damping.xlsx` (if needed)

**PyROPS Reference** (in `pyrops_reference/`):
- [ ] `pyrops_reference.json` (key metrics)
- [ ] `pyrops_trajectory.csv` (full time-series)
- [ ] `plots/altitude_vs_time.png`
- [ ] `plots/velocity_vs_time.png`
- [ ] `plots/trajectory_map.png`

**RocketPy Results** (in `rocketpy_results/`):
- [ ] `simulate_bm_001.py` (simulation script)
- [ ] `rocketpy_results.json` (key metrics)
- [ ] `rocketpy_trajectory.csv` (full time-series)

**Validation** (in `validation/`):
- [ ] `validation_report.md` (comparison analysis)
- [ ] `validation_plots/` (overlay plots)

---

## Action Items

**Immediate** (Phase 2, Day 3-4):
1. [ ] Copy input files to this folder
2. [ ] Review and confirm all parameters above
3. [ ] Run PyROPS simulation
4. [ ] Export and archive results
5. [ ] Document any deviations or issues

**Later** (Phase 4-5):
1. [ ] Convert data to RocketPy format
2. [ ] Implement in RocketPy
3. [ ] Run validation comparison
4. [ ] Get physics team approval

---

## Notes

### Parameters to Verify

Before running PyROPS, need to confirm:
- [ ] Fin dimensions (check PyROPS UI or Settings.xlsx)
- [ ] Actual thrust curve values (check thrust_curve_hybrid.xlsx)
- [ ] Nozzle throat radius
- [ ] Turbulence settings
- [ ] Exact parachute deployment logic

### Known from PyROPS Code Analysis

- Rocket model: Phoenix 1BIIr (from HYROPS)
- Motor type: Hybrid (solid fuel + liquid oxidizer)
- Propellant masses calculated by calculator.pyw
- Uses RK45 adaptive integrator (from fixed_step_solver.pyw and main.pyw)

---

**Test Status**: ⏳ PENDING PyROPS RUN

**Next Step**: Archive input files, then run PyROPS benchmark

**Last Updated By**: Migration Team
**Last Updated Date**: 2025-10-19
