# RocketPy Migration Folder

This folder contains the new RocketPy-based rocket simulation system, migrated from PyROPS v2.3.12.

## Folder Structure

```
rocketpy_migration/
├── src/                    # RocketPy simulation code
│   ├── simulate_rocket.py        # Main simulation script
│   ├── monte_carlo_sim.py        # Monte Carlo simulations
│   ├── convert_rasaero.py        # Data conversion utilities
│   └── ...
│
├── tests/                  # Validation and unit tests
│   ├── test_aero_conversion.py   # Test data conversions
│   ├── validate_bm001.py         # Validate benchmark BM-001
│   ├── run_all_validations.py   # Run full test suite
│   └── ...
│
├── data/                   # Converted data files (CSV format)
│   ├── aerodynamics/       # Aerodynamic coefficient tables
│   │   ├── rasaero_0deg.csv
│   │   ├── rasaero_15deg.csv
│   │   ├── rasaero_nose.csv
│   │   └── rasaero_booster.csv
│   ├── propulsion/         # Thrust curves, motor data
│   │   ├── thrust_curve.csv
│   │   └── mass_properties.csv
│   └── environment/        # Atmosphere, wind profiles
│       ├── atmosphere.csv
│       └── wind_profile.csv
│
├── docs/                   # Documentation
│   ├── USER_GUIDE.md       # How to use RocketPy system
│   ├── CONVERSION_GUIDE.md # Data format conversions
│   └── environment_setup.log
│
├── outputs/                # Simulation results (gitignored)
│   ├── flight_data.csv
│   ├── results.json
│   ├── monte_carlo_results.csv
│   └── plots/
│
├── benchmarks/             # Benchmark test cases for validation
│   ├── BENCHMARK_TEMPLATE.md   # Template for new tests
│   ├── BM-001/             # Baseline nominal flight
│   │   ├── test_cases.md   # Test specification
│   │   ├── pyrops_reference/
│   │   │   ├── pyrops_reference.json
│   │   │   └── pyrops_trajectory.csv
│   │   ├── rocketpy_results/
│   │   │   ├── simulate_bm_001.py
│   │   │   └── rocketpy_results.json
│   │   └── validation_report.md
│   ├── BM-002/             # High wind scenario
│   ├── BM-003/             # Multi-stage
│   ├── BM-004/             # Recovery system
│   └── BM-005/             # Monte Carlo
│
└── README.md               # This file
```

## Quick Start

### Prerequisites

```bash
# Install RocketPy
pip install rocketpy pandas numpy scipy matplotlib pytest
```

### Running a Simulation

```bash
cd src
python simulate_rocket.py
```

Output will be saved to `../outputs/`

### Running Monte Carlo

```bash
cd src
python monte_carlo_sim.py
```

### Running Validation Tests

```bash
cd tests
python run_all_validations.py
```

## Data Conversion

If you need to convert new data files from PyROPS format:

```bash
cd src
python convert_rasaero.py  # Convert aerodynamic data
# Add other conversion scripts as needed
```

## Validation Status

| Test ID | Description | Status | Last Run | Approved By |
|---------|-------------|--------|----------|-------------|
| BM-001 | Baseline Nominal | ⏳ Pending | - | - |
| BM-002 | High Wind | ⏳ Pending | - | - |
| BM-003 | Multi-Stage | ⏳ Pending | - | - |
| BM-004 | Recovery System | ⏳ Pending | - | - |
| BM-005 | Monte Carlo | ⏳ Pending | - | - |

Legend:
- ✅ Validated and approved
- ⚠️ Validation complete, minor issues
- ❌ Validation failed
- ⏳ Pending

## Development Status

**Current Phase**: Setup and Planning
**Target Completion**: 2 weeks from start
**Next Milestone**: Complete Phase 2 (Benchmark Extraction)

See `../MIGRATION_ROADMAP.md` for detailed plan.

## Important Notes

### Validation is CRITICAL

Do NOT skip validation. All PyROPS validated physics MUST be preserved. Every test case must pass before production use.

### Data File Formats

- **Aerodynamics**: CSV format, columns: Mach, Alpha, CA, CN, COP (meters)
- **Thrust**: CSV format, columns: time (s), thrust (N), chamber_pressure (Pa)
- **Atmosphere**: CSV format, columns: altitude, temperature, pressure, density
- **Wind**: CSV format, columns: altitude, wind_u (east), wind_v (north)

### Coordinate Systems

- **RocketPy**: Typically nose-to-tail, but configurable
- **PyROPS**: Check original system (likely tail-to-nose)
- **IMPORTANT**: Verify coordinate system matches during validation

## Support

- **RocketPy Documentation**: https://docs.rocketpy.org/
- **RocketPy GitHub**: https://github.com/RocketPy-Team/RocketPy
- **Migration Roadmap**: `../MIGRATION_ROADMAP.md`
- **Team Contact**: [To be filled in]

## Version History

- **v0.1**: Initial folder structure and planning (2025-10-19)
- **v1.0**: Target completion (TBD)

---

**Status**: Under Development
**Last Updated**: 2025-10-19
