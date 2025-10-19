# Rocket Simulation Migration Project

## Project Status

This project is migrating from the legacy PyROPS v2.3.12 system to RocketPy, a modern, validated, open-source rocket trajectory simulation library.

**Current Phase**: Migration Planning and Setup
**Target Completion**: 2 weeks from start date
**Version Control**: Git initialized

## Repository Structure

```
pyrops-v0.1/
├── ASRI_Simulator/          # Legacy PyROPS system (PRESERVED FOR VALIDATION)
│   ├── body/                # Core simulation modules
│   ├── launcher.pyw         # Main UI launcher
│   └── Path.txt             # Hardcoded path (legacy)
│
├── Inputs/                  # PyROPS input data files (REFERENCE)
│   ├── atmosphere_data.xlsx
│   ├── mass_properties.xlsx
│   ├── RASAeroII*.xlsx      # Aerodynamic databases
│   ├── thrust_curve*.xlsx
│   ├── wind.xlsx
│   └── ...
│
├── rocketpy_migration/      # NEW: RocketPy implementation
│   ├── src/                 # RocketPy simulation code
│   ├── tests/               # Validation and unit tests
│   ├── data/                # Converted data files (CSV format)
│   ├── docs/                # Migration documentation
│   ├── outputs/             # Simulation results
│   └── benchmarks/          # Benchmark test cases
│
├── docs/                    # Project documentation
│   ├── REQUIREMENTS_AND_SPECIFICATIONS.md
│   ├── EXISTING_SOLUTIONS_RESEARCH.md
│   ├── FINAL_RECOMMENDATION.md
│   └── MIGRATION_ROADMAP.md (to be created)
│
├── .git/                    # Version control
├── .gitignore
└── README.md                # This file
```

## Quick Start (After Migration)

```bash
# Install RocketPy
pip install rocketpy

# Run a simulation
cd rocketpy_migration/src
python simulate_rocket.py

# Run validation tests
cd ../tests
python test_validation.py
```

## Documentation

### Analysis Documents (Completed)
- **REQUIREMENTS_AND_SPECIFICATIONS.md**: Complete PyROPS technical specification
- **EXISTING_SOLUTIONS_RESEARCH.md**: Survey of 5 open-source simulators
- **FINAL_RECOMMENDATION.md**: Decision analysis recommending RocketPy

### Migration Documents (In Progress)
- **MIGRATION_ROADMAP.md**: Detailed step-by-step migration plan
- **VALIDATION_PLAN.md**: Benchmark tests and acceptance criteria
- **CONVERSION_GUIDE.md**: Data format conversion procedures

## Key Decisions

### Why RocketPy?
- 97% requirements coverage
- 10-30x performance improvement
- Peer-reviewed validation (~1% apogee accuracy)
- 1-2 week migration vs. 5-12 months for alternatives
- Active development and community support
- Cross-platform (vs. PyROPS Windows-only)

### Folder Structure Rationale
- **Keep PyROPS intact**: Preserve for validation and reference
- **Separate migration folder**: Clean separation of old/new
- **Version control**: Track all changes systematically
- **Benchmark preservation**: Ensure validated physics maintained

## Validation Strategy

**Critical Requirement**: All PyROPS validated physics MUST be preserved

1. **Extract benchmark test cases** from PyROPS
2. **Run benchmarks in PyROPS** and record outputs (apogee, velocity, position, etc.)
3. **Implement same scenarios in RocketPy**
4. **Compare results**: Must match within 0.1% (numerical precision)
5. **Document any differences**: Investigate and explain all discrepancies

## Migration Phases

### Phase 1: Setup (Days 1-2) ✓
- [x] Initialize Git repository
- [x] Create folder structure
- [ ] Install RocketPy
- [ ] Create migration plan document

### Phase 2: Benchmarking (Days 3-4)
- [ ] Extract test cases from PyROPS
- [ ] Run PyROPS benchmarks
- [ ] Document expected outputs
- [ ] Create validation test suite

### Phase 3: Data Conversion (Days 5-6)
- [ ] Convert RASAero Excel → CSV
- [ ] Convert thrust curves → CSV
- [ ] Convert atmosphere data → CSV
- [ ] Convert mass properties → CSV

### Phase 4: Implementation (Days 7-9)
- [ ] Implement standard simulation workflow
- [ ] Implement Monte Carlo workflow
- [ ] Validate against benchmarks

### Phase 5: Extensions (Days 10-12)
- [ ] Implement custom features (RCS control, etc.)
- [ ] Create plotting utilities
- [ ] Documentation

### Phase 6: Validation & Handoff (Days 13-15)
- [ ] Full validation test suite
- [ ] Team training
- [ ] Production sign-off

## Team Members

- **Project Lead**: [Name]
- **Physics/Validation**: [Name]
- **Software Development**: [Name]
- **Testing**: [Name]

## Version History

- **v0.1** (Current): Legacy PyROPS system
- **v1.0** (Target): RocketPy-based system

## License

[To be determined - RocketPy is MIT licensed]

## Contact

[Team contact information]

---

**Last Updated**: 2025-10-19
**Status**: Migration in progress
