# Migration Roadmap: PyROPS to RocketPy

## Document Purpose

This document provides a detailed, step-by-step plan for migrating from PyROPS v2.3.12 to RocketPy. It is designed to be:
- **Actionable**: Clear steps that can be executed immediately
- **Comprehensive**: Covers all aspects of migration
- **Resumable**: Can pause and resume at any checkpoint
- **Validated**: Ensures physics accuracy is preserved

**CRITICAL**: This migration must preserve all validated physics. Validation tests are mandatory.

---

## Table of Contents

1. [Prerequisites](#1-prerequisites)
2. [Phase 1: Environment Setup](#2-phase-1-environment-setup-days-1-2)
3. [Phase 2: Benchmark Extraction](#3-phase-2-benchmark-extraction-days-3-4)
4. [Phase 3: Data Conversion](#4-phase-3-data-conversion-days-5-6)
5. [Phase 4: Core Implementation](#5-phase-4-core-implementation-days-7-9)
6. [Phase 5: Validation](#6-phase-5-validation-days-10-11)
7. [Phase 6: Extensions & Optimization](#7-phase-6-extensions--optimization-days-12-14)
8. [Phase 7: Documentation & Handoff](#8-phase-7-documentation--handoff-day-15)
9. [Checkpoints & Recovery](#9-checkpoints--recovery)
10. [Troubleshooting](#10-troubleshooting)

---

## 1. Prerequisites

### 1.1 Required Knowledge
- [ ] Basic Python programming
- [ ] Understanding of PyROPS workflow (how to run simulations)
- [ ] Access to PyROPS validated test cases
- [ ] Familiarity with command line / terminal

### 1.2 Required Software
- [ ] Python 3.8 or higher
- [ ] Git (for version control)
- [ ] Text editor or IDE (VS Code, PyCharm, etc.)
- [ ] Excel or LibreOffice (for viewing data files)

### 1.3 Required Access
- [ ] PyROPS installation and all input files
- [ ] Historical simulation results (for validation)
- [ ] Engineering team for physics validation support

### 1.4 Preparation Checklist
- [ ] Git repository initialized ✓
- [ ] Folder structure created ✓
- [ ] PyROPS is currently functional
- [ ] Identify 3-5 "golden" test cases (well-validated simulations)
- [ ] Back up all current PyROPS data

---

## 2. Phase 1: Environment Setup (Days 1-2)

### Day 1 Morning: Python Environment

**Objective**: Set up Python environment with RocketPy

**Steps**:

1. **Verify Python version**
   ```bash
   python --version  # Should be 3.8 or higher
   ```
   If not installed, download from python.org

2. **Create virtual environment** (recommended)
   ```bash
   cd /Users/anban/opt/share/engineering-projects/pyrops-v0.1
   python -m venv venv_rocketpy

   # Activate (macOS/Linux)
   source venv_rocketpy/bin/activate

   # Activate (Windows)
   # venv_rocketpy\Scripts\activate
   ```

3. **Install RocketPy and dependencies**
   ```bash
   pip install --upgrade pip
   pip install rocketpy
   pip install pandas numpy scipy matplotlib
   pip install pytest  # For testing
   pip install jupyter  # Optional, for notebooks
   ```

4. **Verify installation**
   ```bash
   python -c "import rocketpy; print(rocketpy.__version__)"
   ```
   Expected output: Version number (e.g., 1.10.0)

**Checkpoint 1.1**: RocketPy installed successfully
- [ ] Virtual environment created
- [ ] RocketPy imported without errors
- [ ] Version number displayed

**Deliverable**: `rocketpy_migration/docs/environment_setup.log` with installation details

---

### Day 1 Afternoon: RocketPy Familiarization

**Objective**: Run example RocketPy simulations to understand API

**Steps**:

1. **Run first example**

   Create file: `rocketpy_migration/src/example_01_basic.py`

   ```python
   """Example 1: Basic RocketPy simulation"""
   from rocketpy import Environment, SolidMotor, Rocket, Flight

   # Create environment
   env = Environment(latitude=32.990254, longitude=-106.974998, elevation=1400)

   # Create motor
   motor = SolidMotor(
       thrust_source="data/motors/Cesaroni_M1670.eng",
       burn_out_time=3.9,
       dry_mass=1.815,
       dry_inertia=(0.125, 0.125, 0.002),
       center_of_dry_mass=0.317,
       grains_center_of_mass_position=0.397,
       grain_number=5,
       grain_separation=0.005,
       grain_density=1815,
       grain_outer_radius=0.033,
       grain_initial_inner_radius=0.015,
       grain_initial_height=0.120,
       nozzle_radius=0.033,
       throat_radius=0.011,
       nozzle_position=0.001,
       interpolation_method="linear",
   )

   # Create rocket
   rocket = Rocket(
       radius=0.0635,
       mass=14.426,
       inertia=(6.321, 6.321, 0.034),
       power_off_drag="data/calisto/powerOffDragCurve.csv",
       power_on_drag="data/calisto/powerOnDragCurve.csv",
       center_of_mass_without_motor=0,
       coordinate_system_orientation="tail_to_nose",
   )

   rocket.add_motor(motor, position=-1.373)

   # Add fins
   rocket.add_trapezoidal_fins(
       n=4,
       span=0.100,
       root_chord=0.120,
       tip_chord=0.040,
       position=-1.168,
   )

   # Add parachute
   rocket.add_parachute(
       name="Main",
       cd_s=10.0,
       trigger="apogee",
       sampling_rate=105,
       lag=1.5,
       noise=(0, 8.3, 0.5),
   )

   # Simulate flight
   flight = Flight(
       rocket=rocket,
       environment=env,
       rail_length=5.2,
       inclination=85,
       heading=0,
   )

   # Display results
   print(f"Apogee: {flight.apogee:.2f} m")
   print(f"Max velocity: {flight.max_velocity:.2f} m/s")
   print(f"Impact: ({flight.latitude_impact:.6f}, {flight.longitude_impact:.6f})")
   ```

   Run: `python example_01_basic.py`

2. **Explore RocketPy classes**
   - Read documentation: https://docs.rocketpy.org/
   - Study Environment, Motor, Rocket, Flight classes
   - Note differences from PyROPS structure

3. **Run Jupyter notebook examples**
   ```bash
   jupyter notebook
   ```
   - Navigate to RocketPy examples (if downloaded repository)
   - Run basic trajectory example
   - Run Monte Carlo example

**Checkpoint 1.2**: RocketPy basics understood
- [ ] Example simulation runs successfully
- [ ] Understand Environment, Motor, Rocket, Flight classes
- [ ] Can modify parameters and see results change

**Deliverable**: Notes on RocketPy API patterns in `rocketpy_migration/docs/rocketpy_notes.md`

---

### Day 2: Git Version Control Setup

**Objective**: Commit initial state and establish workflow

**Steps**:

1. **Create initial commit**
   ```bash
   cd /Users/anban/opt/share/engineering-projects/pyrops-v0.1

   # Stage documentation
   git add README.md
   git add .gitignore
   git add REQUIREMENTS_AND_SPECIFICATIONS.md
   git add EXISTING_SOLUTIONS_RESEARCH.md
   git add FINAL_RECOMMENDATION.md
   git add MIGRATION_ROADMAP.md

   # Stage folder structure
   git add rocketpy_migration/

   # Commit
   git commit -m "Initial commit: Project analysis and migration setup

   - Add comprehensive requirements and specifications documentation
   - Add research on existing solutions (RocketPy, OpenRocket, MAPLEAF)
   - Add final recommendation to adopt RocketPy
   - Add migration roadmap
   - Initialize rocketpy_migration folder structure
   - Add .gitignore for Python projects"
   ```

2. **Create development branch**
   ```bash
   git checkout -b feature/rocketpy-migration
   ```

3. **Create branch strategy document**

   File: `.github/branching-strategy.md` (or `docs/branching-strategy.md`)

   ```markdown
   # Git Branching Strategy

   ## Branches

   - `main`: Stable, production-ready code
   - `develop`: Integration branch for features
   - `feature/*`: Individual feature branches
   - `bugfix/*`: Bug fixes
   - `hotfix/*`: Emergency fixes for production

   ## Workflow

   1. Create feature branch from `develop`
   2. Work on feature, commit regularly
   3. Test thoroughly
   4. Merge back to `develop` when complete
   5. Merge `develop` to `main` for releases

   ## Commit Message Format

   ```
   <type>: <subject>

   <body>

   <footer>
   ```

   Types: feat, fix, docs, test, refactor, chore
   ```

4. **Commit regularly**
   - Commit after each major step
   - Use descriptive commit messages
   - Push to remote repository (if using GitHub/GitLab)

**Checkpoint 1.3**: Version control established
- [ ] Initial commit created
- [ ] Feature branch created
- [ ] Branching strategy documented
- [ ] Understand Git workflow

**Deliverable**: Git repository with documented commit history

---

## 3. Phase 2: Benchmark Extraction (Days 3-4)

**CRITICAL PHASE**: This establishes validation criteria

### Day 3: Identify and Document Test Cases

**Objective**: Select representative test cases that cover all physics

**Steps**:

1. **Select "Golden" Test Cases**

   Choose 3-5 simulations that:
   - Have been validated against real flight data (if available)
   - Cover different flight regimes
   - Exercise all major features

   **Recommended test cases**:

   | Test ID | Description | Why Selected |
   |---------|-------------|--------------|
   | BM-001 | Baseline nominal flight | Standard configuration, well-validated |
   | BM-002 | High wind scenario | Tests wind/aerodynamic interaction |
   | BM-003 | Multi-stage separation | Tests staging events |
   | BM-004 | Drogue + main parachute | Tests recovery system |
   | BM-005 | Monte Carlo (100 runs) | Tests statistical analysis |

2. **Document test case parameters**

   Create: `rocketpy_migration/benchmarks/test_cases.md`

   ```markdown
   # Benchmark Test Cases

   ## BM-001: Baseline Nominal Flight

   **Description**: Standard Phoenix 1BIIr hybrid rocket simulation

   **Input Parameters**:
   - Launch Site:
     - Latitude: -34.600°
     - Longitude: 20.300°
     - Altitude: 0 m
   - Launch Conditions:
     - Elevation: 80.0°
     - Azimuth: -100.0°
     - Rail length: 7.0 m
   - Rocket Configuration:
     - Body radius: 0.087 m
     - Body length: 4.920 m
     - Dry mass: 49.35224149 kg
     - COM (dry): 1.386632 m
     - MOI (dry): Ixx=0.04023116, Iyy=180.8297, Izz=180.8297 kg⋅m²
   - Propulsion:
     - Motor type: Hybrid
     - Burn time: 17.1 s
     - Fuel density: 1065 kg/m³
     - Oxidizer density: 880 kg/m³
     - [Additional parameters...]
   - Aerodynamics:
     - Data source: RASAeroII.xlsx
   - Environment:
     - Atmosphere: atmosphere_data.xlsx
     - Wind: wind.xlsx
   - Recovery:
     - Main parachute CD: 2.2
     - Main parachute diameter: 1.22 m
     - Deployment altitude: 13500 m (or time: 5 s after apogee)

   **Input Files** (archived in benchmarks/BM-001/):
   - thrust_curve.xlsx
   - mass_properties.xlsx
   - RASAeroII.xlsx
   - atmosphere_data.xlsx
   - wind.xlsx

   **Expected Outputs** (from PyROPS validation run):
   - Apogee altitude: [TBD - run PyROPS]
   - Max velocity: [TBD]
   - Max Mach: [TBD]
   - Max acceleration: [TBD]
   - Burnout altitude: [TBD]
   - Landing position: [TBD]
   - Landing velocity: [TBD]
   - Flight time: [TBD]

   **Acceptance Criteria**:
   - Apogee: Within 0.1% of PyROPS
   - Max velocity: Within 0.1%
   - Landing position: Within 10 m
   ```

   Repeat for BM-002 through BM-005.

3. **Archive input files for each test case**
   ```bash
   mkdir -p rocketpy_migration/benchmarks/BM-001
   mkdir -p rocketpy_migration/benchmarks/BM-002
   # etc.

   # Copy input files for BM-001
   cp Inputs/thrust_curve_hybrid.xlsx rocketpy_migration/benchmarks/BM-001/
   cp Inputs/mass_properties.xlsx rocketpy_migration/benchmarks/BM-001/
   cp Inputs/RASAeroII.xlsx rocketpy_migration/benchmarks/BM-001/
   cp Inputs/atmosphere_data.xlsx rocketpy_migration/benchmarks/BM-001/
   cp Inputs/wind.xlsx rocketpy_migration/benchmarks/BM-001/
   ```

**Checkpoint 2.1**: Test cases selected and documented
- [ ] 3-5 test cases identified
- [ ] Parameters documented
- [ ] Input files archived
- [ ] Expected outputs defined (will be filled in Day 4)

---

### Day 4: Run PyROPS Benchmarks

**Objective**: Generate reference outputs from PyROPS

**Steps**:

1. **Run PyROPS for each test case**

   **IMPORTANT**: Run PyROPS with EXACT parameters as documented

   For BM-001:
   - Launch PyROPS UI
   - Load parameters from `benchmarks/BM-001/test_cases.md`
   - Run simulation
   - Record ALL outputs

2. **Extract and record outputs**

   Create: `rocketpy_migration/benchmarks/BM-001/pyrops_reference.json`

   ```json
   {
     "test_id": "BM-001",
     "test_name": "Baseline Nominal Flight",
     "pyrops_version": "v2.3.12",
     "run_date": "2025-10-19",
     "solver": "RK45 adaptive",
     "time_step": 0.02,
     "run_time_seconds": 245.3,

     "key_events": {
       "rail_departure": {
         "time": 0.83,
         "velocity": 24.5,
         "altitude": 7.0
       },
       "burnout": {
         "time": 17.1,
         "velocity": 325.4,
         "altitude": 2456.7
       },
       "apogee": {
         "time": 42.8,
         "altitude": 12543.2,
         "latitude": -34.5989,
         "longitude": 20.3012
       },
       "parachute_deployment": {
         "time": 47.8,
         "altitude": 11234.5
       },
       "landing": {
         "time": 487.2,
         "altitude": 0.0,
         "latitude": -34.5945,
         "longitude": 20.3034,
         "velocity": 6.5
       }
     },

     "maximum_values": {
       "max_velocity": 325.4,
       "max_acceleration": 45.2,
       "max_mach": 0.95,
       "max_dynamic_pressure": 15234.5,
       "max_angle_of_attack": 2.3
     },

     "landing": {
       "latitude": -34.5945,
       "longitude": 20.3034,
       "range_from_launch": 1234.5,
       "bearing_from_launch": 185.3,
       "impact_velocity": 6.5
     },

     "validation_data": {
       "minimum_stability_margin": 1.85,
       "rail_stability": "stable",
       "flight_regime": "subsonic",
       "warnings": []
     }
   }
   ```

3. **Export full trajectory data**

   From PyROPS, export CSV with time-series data:
   `rocketpy_migration/benchmarks/BM-001/pyrops_trajectory.csv`

   Columns should include:
   - time
   - altitude
   - latitude, longitude
   - velocity (N, E, D)
   - velocity magnitude
   - acceleration magnitude
   - Mach number
   - angle of attack
   - etc.

4. **Generate reference plots**

   Save plots from PyROPS:
   - Altitude vs. time
   - Velocity vs. time
   - Trajectory (Lat/Lon)

   Save in: `rocketpy_migration/benchmarks/BM-001/plots/`

5. **Repeat for all test cases**

**Checkpoint 2.2**: PyROPS benchmarks complete
- [ ] All test cases run in PyROPS
- [ ] Key outputs recorded in JSON files
- [ ] Full trajectory CSV files exported
- [ ] Reference plots saved
- [ ] No warnings or errors in PyROPS runs

**Deliverable**: Complete benchmark dataset in `rocketpy_migration/benchmarks/`

---

## 4. Phase 3: Data Conversion (Days 5-6)

**Objective**: Convert PyROPS data formats to RocketPy-compatible formats

### Day 5: Aerodynamic Data Conversion

**Steps**:

1. **Create conversion script for RASAero data**

   File: `rocketpy_migration/src/convert_rasaero.py`

   ```python
   """Convert RASAero Excel files to RocketPy CSV format"""
   import pandas as pd
   import numpy as np

   def convert_rasaero_to_csv(input_excel, output_csv):
       """
       Convert RASAero Excel format to RocketPy CSV format

       RASAero columns (PyROPS):
       0: Mach
       1: Alpha (deg)
       5: CD (axial coefficient)
       8: CN (normal coefficient)
       12: COP (inches)

       RocketPy CSV format:
       mach, alpha, CD, CL, COP (meters)
       """
       print(f"Reading {input_excel}...")
       df = pd.read_excel(input_excel, header=0, engine='openpyxl')

       # Extract columns
       mach = df.iloc[:, 0].values
       alpha_deg = df.iloc[:, 1].values
       CA = df.iloc[:, 5].values  # Axial coefficient
       CN = df.iloc[:, 8].values  # Normal coefficient
       cop_inches = df.iloc[:, 12].values

       # Convert units
       cop_meters = cop_inches * 0.0254  # inches to meters

       # Create output dataframe
       output = pd.DataFrame({
           'Mach': mach,
           'Alpha': alpha_deg,
           'CA': CA,
           'CN': CN,
           'COP': cop_meters
       })

       # Remove duplicates (if any)
       output = output.drop_duplicates()

       # Save to CSV
       output.to_csv(output_csv, index=False)
       print(f"Converted {len(output)} rows to {output_csv}")

       # Summary
       print(f"  Mach range: {mach.min():.2f} to {mach.max():.2f}")
       print(f"  Alpha range: {alpha_deg.min():.1f}° to {alpha_deg.max():.1f}°")
       print(f"  COP range: {cop_meters.min():.3f} to {cop_meters.max():.3f} m")

       return output

   if __name__ == "__main__":
       # Convert standard RASAero files
       convert_rasaero_to_csv(
           '../../Inputs/RASAeroII.xlsx',
           '../data/aerodynamics/rasaero_0deg.csv'
       )

       convert_rasaero_to_csv(
           '../../Inputs/RASAeroII15.xlsx',
           '../data/aerodynamics/rasaero_15deg.csv'
       )

       # Convert nose and booster (if used)
       convert_rasaero_to_csv(
           '../../Inputs/RASAeroIINose.xlsx',
           '../data/aerodynamics/rasaero_nose.csv'
       )

       convert_rasaero_to_csv(
           '../../Inputs/RASAeroIIBooster.xlsx',
           '../data/aerodynamics/rasaero_booster.csv'
       )

       print("\nAerodynamic data conversion complete!")
   ```

   Run: `python convert_rasaero.py`

2. **Validate converted aerodynamic data**

   Create: `rocketpy_migration/tests/test_aero_conversion.py`

   ```python
   """Test that aerodynamic data conversion is correct"""
   import pandas as pd
   import numpy as np

   def test_rasaero_conversion():
       # Load original
       df_orig = pd.read_excel('../../Inputs/RASAeroII.xlsx', header=0)

       # Load converted
       df_conv = pd.read_csv('../data/aerodynamics/rasaero_0deg.csv')

       # Check lengths match
       assert len(df_orig) == len(df_conv), "Row count mismatch"

       # Check Mach values match
       mach_orig = df_orig.iloc[:, 0].values
       mach_conv = df_conv['Mach'].values
       np.testing.assert_array_almost_equal(mach_orig, mach_conv, decimal=5)

       # Check COP conversion (inches to meters)
       cop_orig_inches = df_orig.iloc[:, 12].values
       cop_conv_meters = df_conv['COP'].values
       cop_orig_meters = cop_orig_inches * 0.0254
       np.testing.assert_array_almost_equal(cop_orig_meters, cop_conv_meters, decimal=6)

       print("✓ Aerodynamic data conversion validated")

   if __name__ == "__main__":
       test_rasaero_conversion()
   ```

   Run: `python test_aero_conversion.py`

**Checkpoint 3.1**: Aerodynamic data converted
- [ ] Conversion script created and tested
- [ ] CSV files generated
- [ ] Validation test passes
- [ ] Data spot-checked manually

---

### Day 6: Other Data Conversions

**Steps**:

1. **Convert thrust curves**

   ```python
   """Convert thrust curve data to RocketPy format"""
   import pandas as pd

   # Hybrid motor thrust curve
   df_thrust = pd.read_excel('../../Inputs/thrust_curve_hybrid.xlsx', header=0)

   # RocketPy expects: time (s), thrust (N), chamber_pressure (Pa)
   output = pd.DataFrame({
       'time': df_thrust['Time (s)'],
       'thrust': df_thrust['Thrust (N)'],
       'chamber_pressure': df_thrust['Chamber Pressure (Pa)']
   })

   output.to_csv('../data/propulsion/thrust_curve.csv', index=False)
   ```

2. **Convert atmospheric data**

   ```python
   """Convert atmosphere data to RocketPy format"""
   import pandas as pd

   df_atm = pd.read_excel('../../Inputs/atmosphere_data.xlsx', header=None)

   # RocketPy Environment can use custom atmosphere
   output = pd.DataFrame({
       'altitude': df_atm.iloc[:, 0],
       'temperature': df_atm.iloc[:, 1],
       'pressure': df_atm.iloc[:, 2],
       'density': df_atm.iloc[:, 3]
   })

   output.to_csv('../data/environment/atmosphere.csv', index=False)
   ```

3. **Convert wind profile**

   ```python
   """Convert wind data to RocketPy format"""
   import pandas as pd
   import numpy as np

   df_wind = pd.read_excel('../../Inputs/wind.xlsx', header=0)

   # PyROPS uses bearing (degrees), RocketPy uses direction
   # Convert magnitude and bearing to u (east) and v (north) components

   altitude = df_wind['altitude (m)'].values
   magnitude = df_wind['magnitude (m/s)'].values
   bearing = df_wind['bearing (degrees)'].values

   # Convert bearing to direction (meteorological convention)
   # PyROPS: counter-clockwise from North
   # RocketPy: standard meteorological (direction wind is FROM)

   u = magnitude * np.sin(np.radians(bearing))  # East component
   v = magnitude * np.cos(np.radians(bearing))  # North component

   output = pd.DataFrame({
       'altitude': altitude,
       'wind_u': u,
       'wind_v': v
   })

   output.to_csv('../data/environment/wind_profile.csv', index=False)
   ```

4. **Convert mass properties** (if needed)

   RocketPy calculates this automatically, but we can pre-compute if needed:

   ```python
   """Convert mass properties data"""
   import pandas as pd

   df_mass = pd.read_excel('../../Inputs/mass_properties.xlsx', header=0)

   # RocketPy uses this during motor burn
   output = pd.DataFrame({
       'time': df_mass['time'],
       'mass': df_mass['mass'],
       'Ixx': df_mass['MOIx'],
       'Iyy': df_mass['MOIy'],
       'Izz': df_mass['MOIz'],
       'center_of_mass': df_mass['centre-of-mass']
   })

   output.to_csv('../data/propulsion/mass_properties.csv', index=False)
   ```

**Checkpoint 3.2**: All data converted
- [ ] Thrust curve CSV created
- [ ] Atmosphere CSV created
- [ ] Wind profile CSV created
- [ ] Mass properties CSV created (if needed)
- [ ] All CSVs validated (spot-check values)

**Deliverable**: Complete dataset in `rocketpy_migration/data/` folder

---

## 5. Phase 4: Core Implementation (Days 7-9)

**Objective**: Implement standard simulation workflow in RocketPy

### Day 7: Implement Baseline Simulation

**Steps**:

1. **Create main simulation script**

   File: `rocketpy_migration/src/simulate_rocket.py`

   ```python
   """
   RocketPy simulation matching PyROPS BM-001 baseline
   """
   from rocketpy import Environment, HybridMotor, Rocket, Flight
   import json

   def create_environment():
       """Create environment matching PyROPS setup"""
       env = Environment(
           latitude=-34.600,
           longitude=20.300,
           elevation=0,
           date=(2025, 10, 19, 12)  # Adjust as needed
       )

       # Load custom atmosphere
       env.set_atmospheric_model(
           type='custom_atmosphere',
           pressure='../data/environment/atmosphere.csv',
           temperature='../data/environment/atmosphere.csv',
       )

       # Load wind profile
       env.set_wind_velocity_model(
           file='../data/environment/wind_profile.csv'
       )

       return env

   def create_motor():
       """Create hybrid motor matching PyROPS setup"""
       motor = HybridMotor(
           thrust_source='../data/propulsion/thrust_curve.csv',
           burn_time=17.1,
           dry_mass=49.35224149,  # Dry rocket mass
           dry_inertia=(180.8297, 180.8297, 0.04023116),  # (I_yy, I_zz, I_xx)
           center_of_dry_mass_position=1.386632,
           grain_number=1,
           grain_density=1065,  # Fuel density
           grain_outer_radius=0.0735,
           grain_initial_inner_radius=0.0735 - 0.0375,  # R - thickness
           grain_initial_height=0.510,
           grain_separation=0,
           grains_center_of_mass_position=0.5395,
           nozzle_radius=0.0475,  # Derived from exit area
           throat_radius=0.03,  # Estimate
           oxidizer_tank_position=2.20745,
           # Additional parameters...
       )

       return motor

   def create_rocket(motor):
       """Create rocket matching PyROPS geometry"""
       rocket = Rocket(
           radius=0.087,
           mass=49.35224149 + 15.0,  # Dry + propellant (estimate)
           inertia=(180.8297, 180.8297, 0.04023116),
           power_off_drag='../data/aerodynamics/rasaero_0deg.csv',
           power_on_drag='../data/aerodynamics/rasaero_0deg.csv',
           center_of_mass_without_motor=1.386632,
           coordinate_system_orientation="nose_to_tail",
       )

       # Add motor
       rocket.add_motor(motor, position=0)  # Adjust position

       # Add fins (matching PyROPS geometry)
       rocket.add_trapezoidal_fins(
           n=4,
           span=0.12,  # FinSpan from PyROPS
           root_chord=0.25,  # FinRootChord
           tip_chord=0.10,  # FinTipChord
           sweep_length=0.05,  # FinSweep
           position=-3.5,  # FinLocation
           cant_angle=0.0,  # FinCantAngle (degrees)
       )

       # Add parachutes
       rocket.add_parachute(
           name='Main',
           cd_s=2.2 * (1.22/2)**2 * 3.14159,  # CD * area
           trigger='apogee',
           sampling_rate=105,
           lag=5.0,  # Delay after apogee
           noise=(0, 0, 0),
       )

       return rocket

   def run_simulation():
       """Run complete simulation"""
       print("Creating environment...")
       env = create_environment()

       print("Creating motor...")
       motor = create_motor()

       print("Creating rocket...")
       rocket = create_rocket(motor)

       print("Running flight simulation...")
       flight = Flight(
           rocket=rocket,
           environment=env,
           rail_length=7.0,
           inclination=80.0,  # Launch elevation
           heading=-100.0,  # Launch azimuth (PyROPS convention)
           max_time=1200,  # 20 minutes
       )

       # Extract results
       results = {
           'apogee': flight.apogee,
           'apogee_time': flight.apogee_time,
           'max_velocity': flight.max_velocity,
           'max_acceleration': flight.max_acceleration,
           'latitude_impact': flight.latitude_impact,
           'longitude_impact': flight.longitude_impact,
           'impact_velocity': flight.impact_velocity,
       }

       print("\n" + "="*50)
       print("SIMULATION RESULTS")
       print("="*50)
       for key, value in results.items():
           print(f"{key}: {value}")

       # Export data
       flight.export_data('../outputs/flight_data.csv')

       # Save results
       with open('../outputs/results.json', 'w') as f:
           json.dump(results, f, indent=2)

       return flight, results

   if __name__ == "__main__":
       flight, results = run_simulation()
   ```

   Run: `python simulate_rocket.py`

2. **Debug and iterate**
   - Fix import errors
   - Adjust parameters as needed
   - Verify simulation completes without errors

**Checkpoint 4.1**: Baseline simulation runs
- [ ] Script executes without errors
- [ ] Simulation completes
- [ ] Results file generated
- [ ] Results seem physically reasonable (apogee > 0, etc.)

---

### Day 8: Validation Against Benchmark

**Steps**:

1. **Compare with PyROPS benchmark BM-001**

   Create: `rocketpy_migration/tests/validate_bm001.py`

   ```python
   """Validate RocketPy results against PyROPS benchmark BM-001"""
   import json
   import pandas as pd

   # Load PyROPS reference
   with open('../benchmarks/BM-001/pyrops_reference.json') as f:
       pyrops = json.load(f)

   # Load RocketPy results
   with open('../outputs/results.json') as f:
       rocketpy = json.load(f)

   def compare_value(name, pyrops_val, rocketpy_val, tolerance_pct=0.1):
       """Compare two values and report difference"""
       diff = abs(pyrops_val - rocketpy_val)
       diff_pct = (diff / pyrops_val) * 100 if pyrops_val != 0 else 0

       status = "✓ PASS" if diff_pct <= tolerance_pct else "✗ FAIL"

       print(f"{name:30s} | PyROPS: {pyrops_val:12.2f} | RocketPy: {rocketpy_val:12.2f} | Diff: {diff_pct:6.3f}% | {status}")

       return diff_pct <= tolerance_pct

   print("="*100)
   print("VALIDATION: RocketPy vs PyROPS Benchmark BM-001")
   print("="*100)
   print(f"{'Parameter':<30s} | {'PyROPS':<12s} | {'RocketPy':<12s} | {'Diff %':<6s} | Status")
   print("-"*100)

   tests = [
       ("Apogee (m)", pyrops['key_events']['apogee']['altitude'], rocketpy['apogee']),
       ("Max Velocity (m/s)", pyrops['maximum_values']['max_velocity'], rocketpy['max_velocity']),
       ("Max Acceleration (m/s²)", pyrops['maximum_values']['max_acceleration'], rocketpy['max_acceleration']),
       ("Landing Latitude (deg)", pyrops['landing']['latitude'], rocketpy['latitude_impact']),
       ("Landing Longitude (deg)", pyrops['landing']['longitude'], rocketpy['longitude_impact']),
       ("Impact Velocity (m/s)", pyrops['landing']['impact_velocity'], rocketpy['impact_velocity']),
   ]

   results = [compare_value(name, pval, rval) for name, pval, rval in tests]

   print("="*100)
   if all(results):
       print("✓✓✓ ALL TESTS PASSED ✓✓✓")
       print("RocketPy validation successful! Physics preserved.")
   else:
       print("✗✗✗ SOME TESTS FAILED ✗✗✗")
       print("Investigate differences. May need parameter tuning.")
   print("="*100)
   ```

   Run: `python validate_bm001.py`

2. **Iterate until validation passes**

   If tests fail:
   - Review parameter mapping (PyROPS → RocketPy)
   - Check unit conversions
   - Verify data file conversions
   - Consult RocketPy documentation
   - Ask RocketPy community if needed

   **DO NOT PROCEED** until validation passes (or differences are explained and accepted)

**Checkpoint 4.2**: Validation passes
- [ ] All key metrics within 0.1% of PyROPS
- [ ] Differences documented and explained
- [ ] Physics team approves results

**CRITICAL GATE**: Do not proceed to Day 9 until validation passes

---

### Day 9: Implement Monte Carlo

**Steps**:

1. **Create Monte Carlo simulation script**

   File: `rocketpy_migration/src/monte_carlo_sim.py`

   ```python
   """Monte Carlo simulation matching PyROPS setup"""
   from rocketpy import Environment, HybridMotor, Rocket, Flight, MonteCarlo
   import json

   # Import environment, motor, rocket from simulate_rocket.py
   from simulate_rocket import create_environment, create_motor, create_rocket

   def run_monte_carlo(n_simulations=100):
       """Run Monte Carlo with uncertainties matching PyROPS"""

       # Base environment, motor, rocket
       env = create_environment()
       motor = create_motor()
       rocket = create_rocket(motor)

       # Create Monte Carlo
       mc = MonteCarlo(
           filename='../outputs/monte_carlo',
           environment=env,
           rocket=rocket,
           rail_length=(7.0, 0.1),  # (mean, std)
           inclination=(80.0, 2.0),  # Launch elevation uncertainty
           heading=(-100.0, 5.0),  # Launch azimuth uncertainty
       )

       # Add parameter uncertainties (match PyROPS MC parameters)
       # Example: motor thrust variation
       mc.set_motor_thrust_variation(variation=0.05)  # 5% variation

       # Run simulations
       print(f"Running {n_simulations} Monte Carlo simulations...")
       mc.simulate(number_of_simulations=n_simulations)

       # Generate plots
       mc.plots.ellipses()  # Landing dispersion
       mc.plots.apogee()  # Apogee distribution

       # Export results
       mc.export_data('../outputs/monte_carlo_results.csv')

       print(f"Monte Carlo complete! Results saved.")

       return mc

   if __name__ == "__main__":
       mc = run_monte_carlo(n_simulations=100)
   ```

   Run: `python monte_carlo_sim.py`

2. **Validate Monte Carlo results**
   - Compare landing dispersion with PyROPS
   - Compare apogee distribution
   - Verify statistics (mean, std dev)

**Checkpoint 4.3**: Monte Carlo implemented
- [ ] Monte Carlo simulation runs
- [ ] Results statistically similar to PyROPS
- [ ] Landing dispersion plot generated
- [ ] Performance acceptable (should be much faster than PyROPS)

---

## 6. Phase 5: Validation (Days 10-11)

**Objective**: Complete validation across all benchmark test cases

### Day 10: Run All Benchmarks

**Steps**:

1. **Create validation test suite**

   File: `rocketpy_migration/tests/run_all_validations.py`

   ```python
   """Run all benchmark validations"""
   import os
   import json

   # Test cases
   test_cases = ['BM-001', 'BM-002', 'BM-003', 'BM-004', 'BM-005']

   results = {}

   for test_id in test_cases:
       print(f"\n{'='*80}")
       print(f"Running validation for {test_id}")
       print('='*80)

       # Load test configuration
       # Run simulation
       # Compare with benchmark
       # Record results

       # Placeholder (implement actual validation)
       results[test_id] = {
           'passed': True,  # or False
           'differences': {}
       }

   # Summary report
   print(f"\n{'='*80}")
   print("VALIDATION SUMMARY")
   print('='*80)

   for test_id, result in results.items():
       status = "✓ PASS" if result['passed'] else "✗ FAIL"
       print(f"{test_id}: {status}")

   # Save report
   with open('../outputs/validation_report.json', 'w') as f:
       json.dump(results, f, indent=2)
   ```

2. **Run validation suite**
   ```bash
   cd rocketpy_migration/tests
   python run_all_validations.py
   ```

3. **Document results**
   - Create validation report
   - Note any discrepancies
   - Get physics team approval

**Checkpoint 5.1**: All benchmarks validated
- [ ] All test cases run successfully
- [ ] Results within acceptance criteria
- [ ] Validation report generated
- [ ] Physics team sign-off obtained

---

### Day 11: Performance Testing

**Steps**:

1. **Measure performance improvements**

   ```python
   """Performance comparison: RocketPy vs PyROPS"""
   import time

   # Time single simulation
   start = time.time()
   flight = run_simulation()
   single_time = time.time() - start
   print(f"Single simulation: {single_time:.2f} seconds")

   # Time Monte Carlo (100 runs)
   start = time.time()
   mc = run_monte_carlo(100)
   mc_time = time.time() - start
   print(f"Monte Carlo (100 runs): {mc_time:.2f} seconds")
   print(f"  Per simulation: {mc_time/100:.2f} seconds")
   ```

2. **Compare with PyROPS**
   - PyROPS: ~1-5 minutes per simulation
   - RocketPy: Expected <10 seconds
   - Speedup: 10-30x

**Checkpoint 5.2**: Performance validated
- [ ] RocketPy is faster than PyROPS
- [ ] Monte Carlo runs in reasonable time
- [ ] Performance meets expectations

---

## 7. Phase 6: Extensions & Optimization (Days 12-14)

### Day 12: Custom Features (Optional)

**If needed**: Implement RCS thruster control or other PyROPS-specific features

File: `rocketpy_migration/src/rcs_controller.py`

```python
"""Custom RCS thruster roll control for RocketPy"""
# Implementation of RCS control matching PyROPS behavior
# (Only if needed - may not be required for initial deployment)
```

### Day 13-14: Utilities and Optimization

**Steps**:

1. **Create plotting utilities matching PyROPS style**
2. **Optimize data loading and caching**
3. **Create batch simulation scripts**
4. **Performance tuning if needed**

---

## 8. Phase 7: Documentation & Handoff (Day 15)

### Day 15: Final Documentation

**Steps**:

1. **Create user guide**

   File: `rocketpy_migration/docs/USER_GUIDE.md`

   ```markdown
   # RocketPy User Guide for [Team Name]

   ## Quick Start

   ### Running a Standard Simulation

   ```bash
   cd rocketpy_migration/src
   python simulate_rocket.py
   ```

   ### Running Monte Carlo

   ```bash
   python monte_carlo_sim.py
   ```

   ## Configuration

   [How to modify parameters...]

   ## Troubleshooting

   [Common issues and solutions...]
   ```

2. **Conduct team training**
   - Hands-on session
   - Q&A
   - Distribute documentation

3. **Final Git commit**
   ```bash
   git add .
   git commit -m "feat: Complete RocketPy migration

   - Implement all benchmark test cases
   - Validate against PyROPS (all tests pass)
   - Achieve 10-30x performance improvement
   - Complete documentation and training

   Ready for production use."

   git checkout main
   git merge feature/rocketpy-migration
   git tag v1.0.0 -m "RocketPy migration complete"
   ```

---

## 9. Checkpoints & Recovery

### Major Checkpoints

| Checkpoint | Description | Recovery Action if Failed |
|------------|-------------|---------------------------|
| 1.3 | Git setup complete | Review Git tutorial, get help |
| 2.2 | PyROPS benchmarks complete | Cannot proceed - must have reference data |
| 3.2 | Data conversion complete | Fix conversion scripts, re-run |
| 4.2 | **CRITICAL: Validation passes** | **STOP. Debug until passing. Do not proceed.** |
| 5.1 | All benchmarks validated | Investigate failures, adjust parameters |
| 5.2 | Performance validated | Acceptable - proceed even if not optimal |

### Recovery Procedures

**If validation fails (Checkpoint 4.2)**:

1. Check parameter mapping (PyROPS → RocketPy)
2. Verify unit conversions (inches → meters, etc.)
3. Review data file conversions (re-run conversion scripts)
4. Compare coordinate systems and sign conventions
5. Consult RocketPy documentation
6. Post question to RocketPy GitHub issues
7. Consult with physics team
8. **DO NOT SKIP VALIDATION**

**If stuck on any phase**:

1. Review this roadmap section
2. Check RocketPy documentation: https://docs.rocketpy.org/
3. Search RocketPy GitHub issues: https://github.com/RocketPy-Team/RocketPy/issues
4. Ask RocketPy community (very responsive)
5. Document issue for team discussion

---

## 10. Troubleshooting

### Common Issues

**Issue**: RocketPy simulation crashes
- **Solution**: Check for NaN or Inf values in data files, verify units

**Issue**: Results don't match PyROPS
- **Solution**: Verify parameter mapping, check coordinate system conventions

**Issue**: Monte Carlo takes too long
- **Solution**: Reduce number of simulations for testing, optimize later

**Issue**: Aerodynamic data import error
- **Solution**: Verify CSV format, check for missing values

---

## Success Criteria

### Mandatory (Must Pass)
- [ ] All benchmark tests pass validation (within 0.1%)
- [ ] Physics team approves results
- [ ] Performance improvement demonstrated (faster than PyROPS)
- [ ] Documentation complete
- [ ] Version control established

### Recommended (Should Pass)
- [ ] Monte Carlo results match PyROPS statistics
- [ ] User guide created
- [ ] Team trained
- [ ] All code committed to Git

### Optional (Nice to Have)
- [ ] RCS control implemented
- [ ] Custom plotting utilities
- [ ] Optimization for maximum performance

---

## Timeline Summary

| Phase | Days | Critical Path | Can Skip if Time-Limited? |
|-------|------|---------------|---------------------------|
| 1. Setup | 1-2 | Yes | No |
| 2. Benchmarking | 3-4 | **Yes** | **No - Critical** |
| 3. Data Conversion | 5-6 | Yes | No |
| 4. Implementation | 7-9 | **Yes** | **No - Critical** |
| 5. Validation | 10-11 | **Yes** | **No - Critical** |
| 6. Extensions | 12-14 | No | Yes (defer to later) |
| 7. Documentation | 15 | No | No (but can be brief) |

**Minimum Viable Migration**: Phases 1-5 (11 days)
**Full Migration**: Phases 1-7 (15 days)

---

## Next Steps

**Immediate Actions** (right now):

1. [ ] Review this roadmap with team
2. [ ] Assign roles (who does what)
3. [ ] Schedule kickoff meeting
4. [ ] Begin Day 1: Install RocketPy

**Before Starting**:

- [ ] Team has read and understood this roadmap
- [ ] Calendar time blocked (2-3 weeks)
- [ ] Stakeholders informed
- [ ] PyROPS is currently functional (for benchmarking)
- [ ] Commitment obtained to complete validation rigorously

---

**Let's begin! Start with Phase 1, Day 1 Morning. Good luck!**

---

**Document Version**: 1.0
**Created**: 2025-10-19
**Status**: Active Migration Plan
