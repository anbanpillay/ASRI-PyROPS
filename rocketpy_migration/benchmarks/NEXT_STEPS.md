# Benchmark Extraction - Next Steps

**Current Status**: BM-001 (baseline) prepared, ready for PyROPS execution

---

## ✅ Completed

1. Benchmark selection guide created
2. BM-001 folder structure created
3. BM-001 documentation prepared (README.md)
4. All input files archived in BM-001 folder:
   - ✓ thrust_curve_hybrid.xlsx (233 KB)
   - ✓ mass_properties.xlsx (1.3 MB)
   - ✓ RASAeroII.xlsx (124 KB)
   - ✓ atmosphere_data.xlsx (44 KB)
   - ✓ wind.xlsx (5.3 KB)
   - ✓ Settings.xlsx (11 KB)
   - ✓ side_damping.xlsx (10 KB)

---

## ⏳ CRITICAL: Next Action Required

### YOU NEED TO RUN PYROPS

To complete benchmark extraction, you must:

**1. Launch PyROPS**
```bash
cd ASRI_Simulator
python launcher.pyw
# or on Windows: launcher.pyw
```

**2. Configure Simulation**

Use these parameters (from BM-001/README.md):

**Launch Site**:
- Latitude: -34.600°
- Longitude: 20.300°
- Altitude: 0 m

**Launch Conditions**:
- Elevation: 80.0°
- Azimuth: -100.0°
- Rail Length: 7.0 m

**Rocket** (should match PyROPS defaults):
- Body Radius: 0.087 m
- Body Length: 4.920 m
- Dry Mass: 49.35224149 kg
- COM: 1.386632 m
- MOI: Ixx=0.04023116, Iyy=180.8297, Izz=180.8297

**Propulsion**:
- Motor: Hybrid
- Burn Time: 17.1 s
- [See BM-001/README.md for full parameters]

**Recovery**:
- Main Parachute CD: 2.2
- Main Parachute Diameter: 1.22 m
- Deployment Altitude: 13500 m (or time-based)

**3. Run Simulation**

- Click "Start" or "Run" in PyROPS
- Wait for completion
- Note any warnings or errors

**4. Export Results**

If PyROPS has export functionality:
- Export trajectory CSV
- Export plots (altitude, velocity, trajectory)
- Save simulation results

**5. Record Key Metrics**

Fill in the following in `BM-001/pyrops_reference/pyrops_reference.json`:

```json
{
  "test_id": "BM-001",
  "pyrops_version": "v2.3.12",
  "run_date": "YYYY-MM-DD",

  "key_events": {
    "rail_departure": {
      "time": ___,
      "velocity": ___,
      "altitude": ___
    },
    "burnout": {
      "time": ___,
      "velocity": ___,
      "altitude": ___
    },
    "apogee": {
      "time": ___,
      "altitude": ___,  ← MOST IMPORTANT
      "latitude": ___,
      "longitude": ___
    },
    "parachute_deployment": {
      "time": ___,
      "altitude": ___
    },
    "landing": {
      "time": ___,
      "latitude": ___,
      "longitude": ___,
      "velocity": ___
    }
  },

  "maximum_values": {
    "max_velocity": ___,
    "max_acceleration": ___,
    "max_mach": ___,
    "max_dynamic_pressure": ___,
    "max_angle_of_attack": ___
  },

  "landing": {
    "latitude": ___,
    "longitude": ___,
    "range_from_launch": ___,
    "impact_velocity": ___
  }
}
```

**6. Save Data**

Copy/move files to:
- `rocketpy_migration/benchmarks/BM-001/pyrops_reference/pyrops_reference.json`
- `rocketpy_migration/benchmarks/BM-001/pyrops_reference/pyrops_trajectory.csv`
- `rocketpy_migration/benchmarks/BM-001/pyrops_reference/plots/` (any plots)

---

## Alternative: If PyROPS Doesn't Run

If you encounter issues running PyROPS:

**Option A**: Use historical data
- Do you have results from a previous PyROPS run?
- Can you use that as the reference?

**Option B**: Simplified validation
- Skip detailed benchmarking for now
- Proceed with data conversion (Phase 3)
- Do qualitative comparison (does RocketPy produce reasonable results?)
- Come back to detailed validation later

**Option C**: Ask your colleagues
- Do they have validated PyROPS results?
- Can they run PyROPS and provide outputs?

---

## Recommended: Additional Benchmarks (Optional)

After BM-001, consider creating:

**BM-002: High Wind Scenario**
- Same rocket as BM-001
- Modify wind.xlsx with higher wind speeds
- Run and document

**BM-003: Different Configuration**
- Different parachute settings
- OR staging scenario
- OR different thrust curve

**Target**: 3-5 total benchmarks

---

## When PyROPS Run is Complete

Update files:
1. `BM-001/README.md` - Fill in "Expected Results" section
2. Create `pyrops_reference.json` with results
3. Archive trajectory CSV and plots
4. Git commit:
   ```bash
   git add rocketpy_migration/benchmarks/BM-001/
   git commit -m "feat: Complete BM-001 PyROPS reference run"
   ```

Then proceed to:
- **Phase 3**: Data Conversion (convert Excel → CSV for RocketPy)
- **Phase 4**: Implementation (create RocketPy simulation)
- **Phase 5**: Validation (compare RocketPy vs PyROPS)

---

## Time Estimate

**If PyROPS works smoothly**: 1-2 hours for BM-001
**If PyROPS has issues**: Could take several hours to debug

**Total for 3 benchmarks**: 3-6 hours

---

## Questions?

See:
- `BENCHMARK_SELECTION_GUIDE.md` - How to select test cases
- `BM-001/README.md` - Full parameters for BM-001
- `MIGRATION_ROADMAP.md` Phase 2, Day 4 - Detailed instructions

---

## Summary

**What you need to do NOW**:
1. 🚀 Run PyROPS with BM-001 parameters
2. 📊 Record the results (apogee, velocity, landing, etc.)
3. 💾 Save to `pyrops_reference/pyrops_reference.json`
4. ✅ Commit to Git

**This is CRITICAL** - you cannot validate RocketPy without this reference data!

---

**Status**: ⏳ Waiting for PyROPS execution
**Blocker**: Need to run PyROPS simulation
**Priority**: HIGH - Required for validation
