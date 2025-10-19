# Benchmark Test Case Selection Guide

**Purpose**: Select 3-5 representative test cases from PyROPS to serve as validation benchmarks

**Critical**: These benchmarks establish the validation baseline. All RocketPy results must match PyROPS results within 0.1% for key metrics.

---

## Criteria for Benchmark Selection

### Must-Have Characteristics

1. **Well-Validated**
   - Simulation has been reviewed and approved by physics team
   - Results are known to be physically reasonable
   - Preferably compared against actual flight data or theoretical calculations

2. **Representative**
   - Covers different flight regimes (subsonic, transonic, supersonic)
   - Exercises major features of the simulator

3. **Complete**
   - All input files available
   - Simulation runs successfully in current PyROPS
   - No missing data or dependencies

4. **Documented**
   - Parameters are known and recorded
   - Purpose/context is understood

### Coverage Requirements

Select test cases that collectively cover:

**Flight Regimes**:
- [ ] Subsonic flight (Mach < 0.8)
- [ ] Transonic flight (0.8 ≤ Mach ≤ 1.2)
- [ ] Supersonic flight (Mach > 1.2)

**Propulsion**:
- [ ] Hybrid motor (primary focus based on PyROPS)
- [ ] Liquid motor (if used)
- [ ] Solid motor (if available for comparison)

**Flight Phases**:
- [ ] Launch rail departure
- [ ] Powered ascent (motor burning)
- [ ] Coasting ascent (motor burnout to apogee)
- [ ] Descent with parachute
- [ ] Landing

**Features**:
- [ ] Aerodynamics (fin effects, angle of attack)
- [ ] Variable mass properties (propellant consumption)
- [ ] Wind effects
- [ ] Parachute deployment (main and/or drogue)
- [ ] Staging (if applicable)

---

## Recommended Test Cases

Based on PyROPS analysis, here are recommended test cases:

### BM-001: Baseline Nominal Flight ⭐ PRIORITY 1

**Why**: This should be your most-validated, "golden" test case

**Description**: Standard hybrid rocket flight with nominal conditions

**Characteristics**:
- Hybrid motor (solid fuel + liquid oxidizer)
- Single stage
- Main parachute recovery
- Moderate wind
- Well-validated physics

**Input Files Required**:
- `thrust_curve_hybrid.xlsx`
- `mass_properties.xlsx`
- `RASAeroII.xlsx` (0° fin cant)
- `atmosphere_data.xlsx`
- `wind.xlsx`

**Expected Coverage**:
- Hybrid motor operation ✓
- Variable mass properties ✓
- Aerodynamic lookup tables ✓
- Launch rail dynamics ✓
- Parachute deployment ✓
- Wind effects ✓

---

### BM-002: High Wind Scenario ⭐ PRIORITY 2

**Why**: Tests wind/aerodynamic interaction

**Description**: Same rocket as BM-001 but with high wind conditions

**Characteristics**:
- Same rocket configuration as BM-001
- Modified wind profile (higher magnitude)
- Tests lateral drift and angle of attack response

**Input Files Required**:
- Same as BM-001, except:
- `wind.xlsx` (modified with higher wind speeds)

**Expected Coverage**:
- Wind sensitivity ✓
- Aerodynamic forces at angle ✓
- Landing dispersion ✓

---

### BM-003: Drogue + Main Parachute (if applicable)

**Why**: Tests recovery system complexity

**Description**: Rocket with two-stage recovery (drogue at apogee, main at lower altitude)

**Characteristics**:
- Drogue parachute at apogee
- Main parachute at lower altitude (e.g., 1000m)
- Different descent rates

**Input Files Required**:
- Same base configuration
- Modified recovery settings

**Expected Coverage**:
- Multi-parachute system ✓
- Altitude-based triggers ✓

---

### BM-004: Multi-Stage (if applicable)

**Why**: Tests staging and separation

**Description**: Two-stage rocket with separation event

**Characteristics**:
- Stage separation during ascent
- Different aerodynamics post-separation
- Booster and nose cone separate trajectories

**Input Files Required**:
- `thrust_curve_staging.xlsx`
- `RASAeroIINose.xlsx`, `RASAeroIIBooster.xlsx`
- Staging parameters

**Expected Coverage**:
- Staging events ✓
- Mass discontinuities ✓
- Aerodynamic configuration changes ✓

---

### BM-005: Monte Carlo (100 runs) - OPTIONAL

**Why**: Tests statistical analysis

**Description**: Monte Carlo with uncertainties

**Characteristics**:
- Same base as BM-001
- Add parameter uncertainties
- 100 simulations minimum

**Expected Coverage**:
- Monte Carlo framework ✓
- Landing dispersion ✓
- Statistical outputs ✓

---

## Benchmark Selection Worksheet

Fill this out for each proposed test case:

### Test Case: BM-XXX

**Name**: _______________________________

**Priority**: [ ] Critical [ ] High [ ] Medium [ ] Low

**Validation Status**:
- [ ] Physics team has reviewed
- [ ] Results are reasonable
- [ ] Compared against flight data: Yes / No / N/A

**Availability**:
- [ ] All input files present
- [ ] Simulation runs in current PyROPS
- [ ] No missing dependencies

**Coverage** (check all that apply):
- [ ] Subsonic
- [ ] Transonic
- [ ] Supersonic
- [ ] Hybrid motor
- [ ] Liquid motor
- [ ] Parachute recovery
- [ ] Wind effects
- [ ] Staging
- [ ] Monte Carlo

**Estimated Runtime** (PyROPS):
- Single run: ________ minutes
- Monte Carlo (if applicable): ________ hours

**Notes**:
_____________________________________________________________
_____________________________________________________________

---

## Selection Process

### Step 1: Inventory (30 minutes)

1. List all PyROPS simulations you've run
2. Identify which are most validated/trusted
3. Check which input files currently exist in `Inputs/` folder

### Step 2: Select Minimum Set (30 minutes)

**Minimum**: 3 test cases
- BM-001: Baseline nominal ⭐ MANDATORY
- BM-002: One variant (wind, parachute, etc.)
- BM-003: Additional coverage

**Recommended**: 5 test cases
- All of the above
- BM-004: Multi-stage or other advanced feature
- BM-005: Monte Carlo

**Do not exceed 7 test cases** (diminishing returns)

### Step 3: Document (1 hour per test case)

For each selected test case:
1. Copy `BENCHMARK_TEMPLATE.md` → `BM-XXX/README.md`
2. Fill in all parameters
3. List all input files
4. Create folder: `rocketpy_migration/benchmarks/BM-XXX/`

### Step 4: Archive Input Files (30 minutes per test case)

Copy input files to benchmark folder:
```bash
mkdir -p rocketpy_migration/benchmarks/BM-001
cp Inputs/thrust_curve_hybrid.xlsx rocketpy_migration/benchmarks/BM-001/
cp Inputs/mass_properties.xlsx rocketpy_migration/benchmarks/BM-001/
cp Inputs/RASAeroII.xlsx rocketpy_migration/benchmarks/BM-001/
cp Inputs/atmosphere_data.xlsx rocketpy_migration/benchmarks/BM-001/
cp Inputs/wind.xlsx rocketpy_migration/benchmarks/BM-001/
```

---

## Next Steps After Selection

Once test cases are selected and documented:

1. **Day 4: Run PyROPS Benchmarks**
   - Launch PyROPS
   - Load each benchmark configuration
   - Run simulation
   - Export results (CSV, plots)
   - Record key metrics in `pyrops_reference.json`

2. **Validation Preparation**
   - Define acceptance criteria (typically 0.1% for key metrics)
   - Get physics team buy-in on selected cases
   - Ensure all data archived in Git

---

## Quality Checklist

Before proceeding to Phase 3 (Data Conversion), verify:

- [ ] Minimum 3 test cases selected (recommend 5)
- [ ] BM-001 (baseline nominal) is included
- [ ] All test cases cover different scenarios (not redundant)
- [ ] Each test case has folder: `benchmarks/BM-XXX/`
- [ ] Each test case has documentation: `BM-XXX/README.md`
- [ ] All input files archived in benchmark folders
- [ ] Physics team approves selected test cases
- [ ] Ready to run PyROPS benchmarks (Day 4)

---

## Common Pitfalls to Avoid

❌ **Don't select too many test cases**
- More than 7 cases = excessive work, diminishing returns
- Focus on quality over quantity

❌ **Don't select redundant cases**
- Don't create 3 variations of the same scenario
- Each case should test something different

❌ **Don't select unvalidated cases**
- If you're not confident in PyROPS results, don't use as benchmark
- Only use well-validated simulations

❌ **Don't skip documentation**
- Future-you will need to remember what each case tests
- Document now while fresh in mind

❌ **Don't proceed without physics team approval**
- Get sign-off on selected test cases
- Ensure acceptance criteria agreed upon

---

## Success Criteria

You've successfully completed benchmark selection when:

✅ 3-5 test cases selected
✅ Each test case documented in `BM-XXX/README.md`
✅ All input files archived
✅ Physics team approves selection
✅ Ready to run PyROPS Day 4

**Estimated Time**: 4-6 hours for 3 test cases, 8-10 hours for 5 test cases

---

**Next Document**: After selection, proceed to running PyROPS benchmarks (see `MIGRATION_ROADMAP.md` Phase 2, Day 4)
