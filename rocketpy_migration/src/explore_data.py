#!/usr/bin/env python3
"""
Data Exploration Script
Examines PyROPS input Excel files to understand their structure
"""

import pandas as pd
import numpy as np
from pathlib import Path

# Define paths
inputs_dir = Path(__file__).parent.parent.parent / "Inputs"
bm001_dir = Path(__file__).parent.parent / "benchmarks" / "BM-001"

print("=" * 80)
print("PyROPS DATA EXPLORATION")
print("=" * 80)

# 1. THRUST CURVE
print("\n" + "=" * 80)
print("1. THRUST CURVE (thrust_curve_hybrid.xlsx)")
print("=" * 80)
thrust_file = bm001_dir / "thrust_curve_hybrid.xlsx"
try:
    # Try to read - might have multiple sheets
    xl = pd.ExcelFile(thrust_file)
    print(f"\nSheets found: {xl.sheet_names}")

    for sheet in xl.sheet_names[:3]:  # Show first 3 sheets
        print(f"\n--- Sheet: {sheet} ---")
        df = pd.read_excel(thrust_file, sheet_name=sheet, nrows=10)
        print(f"Shape: {df.shape}")
        print(f"Columns: {df.columns.tolist()}")
        print("\nFirst few rows:")
        print(df.head())
except Exception as e:
    print(f"Error reading thrust curve: {e}")

# 2. AERODYNAMICS
print("\n" + "=" * 80)
print("2. AERODYNAMICS (RASAeroII.xlsx)")
print("=" * 80)
aero_file = bm001_dir / "RASAeroII.xlsx"
try:
    xl = pd.ExcelFile(aero_file)
    print(f"\nSheets found: {xl.sheet_names}")

    for sheet in xl.sheet_names[:5]:  # Show first 5 sheets
        print(f"\n--- Sheet: {sheet} ---")
        df = pd.read_excel(aero_file, sheet_name=sheet, nrows=10)
        print(f"Shape: {df.shape}")
        print(f"Columns: {df.columns.tolist()}")
        print("\nFirst few rows:")
        print(df.head())
except Exception as e:
    print(f"Error reading aerodynamics: {e}")

# 3. ATMOSPHERE
print("\n" + "=" * 80)
print("3. ATMOSPHERE (atmosphere_data.xlsx)")
print("=" * 80)
atm_file = bm001_dir / "atmosphere_data.xlsx"
try:
    xl = pd.ExcelFile(atm_file)
    print(f"\nSheets found: {xl.sheet_names}")

    df = pd.read_excel(atm_file, sheet_name=xl.sheet_names[0], nrows=20)
    print(f"\nShape: {df.shape}")
    print(f"Columns: {df.columns.tolist()}")
    print("\nFirst few rows:")
    print(df.head(20))
except Exception as e:
    print(f"Error reading atmosphere: {e}")

# 4. WIND
print("\n" + "=" * 80)
print("4. WIND (wind.xlsx)")
print("=" * 80)
wind_file = bm001_dir / "wind.xlsx"
try:
    xl = pd.ExcelFile(wind_file)
    print(f"\nSheets found: {xl.sheet_names}")

    df = pd.read_excel(wind_file, sheet_name=xl.sheet_names[0])
    print(f"\nShape: {df.shape}")
    print(f"Columns: {df.columns.tolist()}")
    print("\nAll data:")
    print(df)
except Exception as e:
    print(f"Error reading wind: {e}")

# 5. MASS PROPERTIES
print("\n" + "=" * 80)
print("5. MASS PROPERTIES (mass_properties.xlsx)")
print("=" * 80)
mass_file = bm001_dir / "mass_properties.xlsx"
try:
    xl = pd.ExcelFile(mass_file)
    print(f"\nSheets found: {xl.sheet_names}")

    for sheet in xl.sheet_names[:3]:  # First 3 sheets
        print(f"\n--- Sheet: {sheet} ---")
        df = pd.read_excel(mass_file, sheet_name=sheet, nrows=15)
        print(f"Shape: {df.shape}")
        print(f"Columns: {df.columns.tolist()}")
        print("\nFirst few rows:")
        print(df.head(15))
except Exception as e:
    print(f"Error reading mass properties: {e}")

print("\n" + "=" * 80)
print("EXPLORATION COMPLETE")
print("=" * 80)
