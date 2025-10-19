#!/usr/bin/env python3
"""
Data Conversion Script
Converts PyROPS Excel files to RocketPy-compatible formats
"""

import pandas as pd
import numpy as np
from pathlib import Path
import json

# Define paths
bm001_dir = Path(__file__).parent.parent / "benchmarks" / "BM-001"
output_dir = Path(__file__).parent.parent / "data"
output_dir.mkdir(exist_ok=True)

# Create subdirectories
(output_dir / "motors").mkdir(exist_ok=True)
(output_dir / "aerodynamics").mkdir(exist_ok=True)
(output_dir / "environment").mkdir(exist_ok=True)
(output_dir / "mass_properties").mkdir(exist_ok=True)

print("=" * 80)
print("DATA CONVERSION: PyROPS -> RocketPy")
print("=" * 80)

# =============================================================================
# 1. THRUST CURVE CONVERSION
# =============================================================================
print("\n1. Converting thrust curve...")
thrust_file = bm001_dir / "thrust_curve_hybrid.xlsx"

# Read the Excel file - note that headers are actually the first row of data
df_thrust_raw = pd.read_excel(thrust_file, sheet_name='thrust_curve', header=None)

# The first row contains what looks like initial values, but actually the data starts there
# Let's read without headers and then properly name columns
df_thrust = pd.read_excel(thrust_file, sheet_name='thrust_curve', header=None)

# Rename columns: time (s), thrust (N), chamber_pressure (Pa)
df_thrust.columns = ['time', 'thrust', 'chamber_pressure']

# RocketPy needs: time and thrust
df_thrust_rocketpy = df_thrust[['time', 'thrust']].copy()

# Save in multiple formats
thrust_csv = output_dir / "motors" / "hybrid_thrust_curve.csv"
df_thrust_rocketpy.to_csv(thrust_csv, index=False, float_format='%.6f')
print(f"   ✓ Saved: {thrust_csv}")
print(f"   - Duration: {df_thrust['time'].max():.2f} s")
print(f"   - Peak Thrust: {df_thrust['thrust'].max():.2f} N")
print(f"   - Total Impulse: {np.trapz(df_thrust['thrust'], df_thrust['time']):.2f} N·s")

# Also save the full data (with chamber pressure) for reference
df_thrust.to_csv(output_dir / "motors" / "hybrid_thrust_curve_full.csv",
                 index=False, float_format='%.6f')

# =============================================================================
# 2. AERODYNAMICS CONVERSION
# =============================================================================
print("\n2. Converting aerodynamics data...")
aero_file = bm001_dir / "RASAeroII.xlsx"
df_aero = pd.read_excel(aero_file, sheet_name='RASAeroII')

# Save complete aerodynamics data
aero_csv = output_dir / "aerodynamics" / "rasaero_data.csv"
df_aero.to_csv(aero_csv, index=False, float_format='%.6f')
print(f"   ✓ Saved: {aero_csv}")
print(f"   - Mach range: {df_aero['Mach'].min():.3f} to {df_aero['Mach'].max():.3f}")
print(f"   - Alpha range: {df_aero['Alpha'].min():.1f}° to {df_aero['Alpha'].max():.1f}°")
print(f"   - Data points: {len(df_aero)}")

# Extract key coefficients for quick reference
# RocketPy primarily uses CD (drag coefficient)
df_cd = df_aero[['Mach', 'Alpha', 'CD']].copy()
df_cd.to_csv(output_dir / "aerodynamics" / "drag_coefficient.csv",
             index=False, float_format='%.6f')

# Extract power-off drag for coasting phase
df_cd_poweroff = df_aero[['Mach', 'Alpha', 'CD Power-Off']].copy()
df_cd_poweroff.to_csv(output_dir / "aerodynamics" / "drag_coefficient_poweroff.csv",
                      index=False, float_format='%.6f')

# =============================================================================
# 3. ATMOSPHERE CONVERSION
# =============================================================================
print("\n3. Converting atmosphere data...")
atm_file = bm001_dir / "atmosphere_data.xlsx"

# The headers are actually the surface conditions
# Read without headers first
df_atm_raw = pd.read_excel(atm_file, sheet_name='atmosphere_data', header=None)

# The first row (header) contains surface values: altitude=0, T, P, rho
# Subsequent rows contain the actual data
# Let's read properly
df_atm = pd.read_excel(atm_file, sheet_name='atmosphere_data', header=0)

# The column names are the surface values, let's rename them
df_atm.columns = ['altitude', 'temperature', 'pressure', 'density']

# Add the surface row (from the original headers)
surface_data = pd.DataFrame({
    'altitude': [0.0],
    'temperature': [288.16],
    'pressure': [101325.0],
    'density': [1.225]
})

# Combine surface + altitude data
df_atm_full = pd.concat([surface_data, df_atm], ignore_index=True)
df_atm_full = df_atm_full.sort_values('altitude').reset_index(drop=True)

# Save for RocketPy
atm_csv = output_dir / "environment" / "atmosphere.csv"
df_atm_full.to_csv(atm_csv, index=False, float_format='%.6f')
print(f"   ✓ Saved: {atm_csv}")
print(f"   - Altitude range: {df_atm_full['altitude'].min():.0f} to {df_atm_full['altitude'].max():.0f} m")
print(f"   - Temperature range: {df_atm_full['temperature'].min():.2f} to {df_atm_full['temperature'].max():.2f} K")
print(f"   - Pressure range: {df_atm_full['pressure'].min():.2f} to {df_atm_full['pressure'].max():.2f} Pa")

# =============================================================================
# 4. WIND CONVERSION
# =============================================================================
print("\n4. Converting wind data...")
wind_file = bm001_dir / "wind.xlsx"
df_wind = pd.read_excel(wind_file, sheet_name='Sheet1')

# Save for RocketPy (already in good format)
wind_csv = output_dir / "environment" / "wind_profile.csv"
df_wind.to_csv(wind_csv, index=False, float_format='%.6f')
print(f"   ✓ Saved: {wind_csv}")
print(f"   - Altitude range: {df_wind['altitude (m)'].min():.0f} to {df_wind['altitude (m)'].max():.0f} m")
print(f"   - Wind speed range: {df_wind['magnitude (m/s)'].min():.0f} to {df_wind['magnitude (m/s)'].max():.0f} m/s")
print(f"   - Surface wind: {df_wind.iloc[0]['magnitude (m/s)']:.0f} m/s at {df_wind.iloc[0]['bearing (degrees)']:.0f}°")

# =============================================================================
# 5. MASS PROPERTIES CONVERSION
# =============================================================================
print("\n5. Converting mass properties...")
mass_file = bm001_dir / "mass_properties.xlsx"
df_mass = pd.read_excel(mass_file, sheet_name='Sheet1')

# Save for RocketPy
mass_csv = output_dir / "mass_properties" / "time_varying_mass.csv"
df_mass.to_csv(mass_csv, index=False, float_format='%.6f')
print(f"   ✓ Saved: {mass_csv}")
print(f"   - Time range: {df_mass['time'].min():.3f} to {df_mass['time'].max():.3f} s")
print(f"   - Mass range: {df_mass['mass'].min():.3f} to {df_mass['mass'].max():.3f} kg")
print(f"   - Initial mass: {df_mass.iloc[0]['mass']:.3f} kg")
print(f"   - Final mass (dry): {df_mass.iloc[-1]['mass']:.3f} kg")
print(f"   - Propellant mass: {df_mass.iloc[0]['mass'] - df_mass.iloc[-1]['mass']:.3f} kg")

# =============================================================================
# 6. CREATE SUMMARY JSON
# =============================================================================
print("\n6. Creating conversion summary...")

summary = {
    "conversion_date": "2025-10-19",
    "source": "BM-001 PyROPS benchmark data",
    "motor": {
        "type": "hybrid",
        "thrust_curve_file": "motors/hybrid_thrust_curve.csv",
        "burn_time_s": float(df_thrust['time'].max()),
        "peak_thrust_N": float(df_thrust['thrust'].max()),
        "total_impulse_Ns": float(np.trapz(df_thrust['thrust'], df_thrust['time'])),
        "propellant_mass_kg": float(df_mass.iloc[0]['mass'] - df_mass.iloc[-1]['mass'])
    },
    "aerodynamics": {
        "source": "RASAero II",
        "file": "aerodynamics/rasaero_data.csv",
        "mach_range": [float(df_aero['Mach'].min()), float(df_aero['Mach'].max())],
        "alpha_range_deg": [float(df_aero['Alpha'].min()), float(df_aero['Alpha'].max())],
        "reference_area_m2": 0.0238  # π × (0.087)²
    },
    "atmosphere": {
        "file": "environment/atmosphere.csv",
        "altitude_range_m": [float(df_atm_full['altitude'].min()), float(df_atm_full['altitude'].max())],
        "surface_pressure_Pa": float(df_atm_full.iloc[0]['pressure']),
        "surface_temperature_K": float(df_atm_full.iloc[0]['temperature'])
    },
    "wind": {
        "file": "environment/wind_profile.csv",
        "surface_speed_ms": float(df_wind.iloc[0]['magnitude (m/s)']),
        "surface_bearing_deg": float(df_wind.iloc[0]['bearing (degrees)'])
    },
    "mass_properties": {
        "file": "mass_properties/time_varying_mass.csv",
        "dry_mass_kg": float(df_mass.iloc[-1]['mass']),
        "wet_mass_kg": float(df_mass.iloc[0]['mass']),
        "dry_com_m": float(df_mass.iloc[-1]['centre-of-mass']),
        "dry_MOI": {
            "Ixx": float(df_mass.iloc[-1]['MOIx']),
            "Iyy": float(df_mass.iloc[-1]['MOIy']),
            "Izz": float(df_mass.iloc[-1]['MOIz'])
        }
    },
    "rocket_geometry": {
        "body_radius_m": 0.087,
        "body_length_m": 4.920,
        "nose_length_m": None,  # TBD from RASAero
        "fins": {
            "number": 4,
            "cant_angle_deg": 0
        }
    },
    "launch_conditions": {
        "rail_length_m": 7.0,
        "elevation_deg": 80.0,
        "azimuth_deg": -100.0,
        "latitude_deg": -34.600,
        "longitude_deg": 20.300,
        "altitude_m": 0
    }
}

summary_file = output_dir / "conversion_summary.json"
with open(summary_file, 'w') as f:
    json.dump(summary, f, indent=2)

print(f"   ✓ Saved: {summary_file}")

# =============================================================================
# CONVERSION COMPLETE
# =============================================================================
print("\n" + "=" * 80)
print("CONVERSION COMPLETE!")
print("=" * 80)
print(f"\nConverted data saved to: {output_dir}")
print("\nFiles created:")
print(f"  1. {thrust_csv.name}")
print(f"  2. {aero_csv.name}")
print(f"  3. {atm_csv.name}")
print(f"  4. {wind_csv.name}")
print(f"  5. {mass_csv.name}")
print(f"  6. {summary_file.name}")
print("\nReady for RocketPy implementation!")
