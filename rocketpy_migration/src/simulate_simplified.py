#!/usr/bin/env python3
"""
Simplified RocketPy Simulation - Get it working first!
Focus on essential physics with simpler motor model
"""

import json
from pathlib import Path
from datetime import datetime
import pandas as pd
import numpy as np

from rocketpy import Environment, GenericMotor, Rocket, Flight

# =============================================================================
# SIMPLIFIED CONFIGURATION
# =============================================================================
print("=" * 80)
print("SIMPLIFIED ROCKETPY SIMULATION")
print("=" * 80)

data_dir = Path(__file__).parent.parent / "data"
output_dir = Path(__file__).parent.parent / "outputs"
output_dir.mkdir(exist_ok=True)

# Load thrust curve
thrust_file = data_dir / "motors" / "hybrid_thrust_curve.csv"
df_thrust = pd.read_csv(thrust_file)

print(f"\nThrust curve loaded:")
print(f"  - Burn time: {df_thrust['time'].max():.2f} s")
print(f"  - Peak thrust: {df_thrust['thrust'].max():.2f} N")

# Load mass properties for time-varying mass
mass_file = data_dir / "mass_properties" / "time_varying_mass.csv"
df_mass = pd.read_csv(mass_file)

print(f"\nMass properties loaded:")
print(f"  - Initial mass: {df_mass.iloc[0]['mass']:.2f} kg")
print(f"  - Final mass: {df_mass.iloc[-1]['mass']:.2f} kg")
print(f"  - Propellant: {df_mass.iloc[0]['mass'] - df_mass.iloc[-1]['mass']:.2f} kg")

# =============================================================================
# 1. ENVIRONMENT - SIMPLIFIED
# =============================================================================
print("\n" + "=" * 80)
print("1. ENVIRONMENT SETUP")
print("=" * 80)

env = Environment(
    latitude=-34.6,
    longitude=20.3,
    elevation=0
)

# Use standard atmosphere for simplicity
env.set_date((2025, 10, 19, 12))
env.set_atmospheric_model(type='standard_atmosphere')

# Simple constant wind
env.set_atmospheric_model(type='standard_atmosphere', wind_u=0, wind_v=8)

print("Environment: Standard atmosphere, 8 m/s wind")

# =============================================================================
# 2. MOTOR - GENERIC MOTOR WITH CUSTOM THRUST
# =============================================================================
print("\n" + "=" * 80)
print("2. MOTOR SETUP (Generic Motor)")
print("=" * 80)

# Use GenericMotor which is simpler
propellant_mass = df_mass.iloc[0]['mass'] - df_mass.iloc[-1]['mass']

motor = GenericMotor(
    thrust_source=str(thrust_file),
    burn_time=df_thrust['time'].max(),
    dry_mass=5.0,  # Motor structure mass (approximate)
    dry_inertia=(0.1, 0.1, 0.01),
    nozzle_radius=0.047,
    center_of_dry_mass_position=1.8,
    nozzle_position=0.0,
    chamber_radius=0.075,
    chamber_height=0.5,
    chamber_position=1.5,
    propellant_initial_mass=propellant_mass,
    interpolation_method='linear',
    coordinate_system_orientation='nozzle_to_combustion_chamber'
)

print(f"Motor: Generic")
print(f"  - Burn time: {df_thrust['time'].max():.2f} s")
print(f"  - Propellant mass: {propellant_mass:.2f} kg")
print(f"  - Dry mass: 5.0 kg")

# =============================================================================
# 3. ROCKET - SIMPLIFIED
# =============================================================================
print("\n" + "=" * 80)
print("3. ROCKET SETUP")
print("=" * 80)

rocket = Rocket(
    radius=0.087,
    mass=32.8,  # Rocket body mass (approx: total dry - motor structure)
    inertia=(1, 100, 100),  # Approximate
    power_off_drag=0.45,
    power_on_drag=0.48,
    center_of_mass_without_motor=2.4,  # Approximate COM position
    coordinate_system_orientation='tail_to_nose'
)

print(f"Rocket:")
print(f"  - Radius: 0.087 m")
print(f"  - Length: ~4.92 m")

# Add motor
rocket.add_motor(motor, position=1.5)

# Nose cone
rocket.add_nose(
    length=0.55,
    kind='ogive',
    position=4.92
)

# Fins - larger for stability
rocket.add_trapezoidal_fins(
    n=4,
    root_chord=0.4,
    tip_chord=0.2,
    span=0.2,  # Larger span for stability
    position=0.8,
    cant_angle=0,
    airfoil=None
)

# Parachute
rocket.add_parachute(
    name='Main',
    cd_s=2.2 * np.pi * (1.22 / 2) ** 2,
    trigger='apogee',
    sampling_rate=105,
    lag=0,
    noise=(0, 0, 0)
)

# Rail buttons
rocket.set_rail_buttons(
    upper_button_position=6.5,
    lower_button_position=0.5,
    angular_position=45
)

print("\nRocket configured (skipping draw for headless mode)")

# =============================================================================
# 4. FLIGHT SIMULATION
# =============================================================================
print("\n" + "=" * 80)
print("4. RUNNING SIMULATION")
print("=" * 80)

try:
    flight = Flight(
        rocket=rocket,
        environment=env,
        rail_length=7.0,
        inclination=80,  # degrees from horizontal
        heading=260,  # -100° in PyROPS convention
        max_time=600,
        max_time_step=0.5,
        terminate_on_apogee=False,
        verbose=False  # Disable verbose to avoid stuck output
    )

    print("\n✓ SIMULATION COMPLETE!")

    # =============================================================================
    # 5. RESULTS
    # =============================================================================
    print("\n" + "=" * 80)
    print("RESULTS")
    print("=" * 80)

    print(f"\nApogee Altitude:      {flight.apogee:>10.2f} m")
    print(f"Apogee Time:          {flight.apogee_time:>10.2f} s")
    print(f"Maximum Speed:        {flight.max_speed:>10.2f} m/s")
    print(f"Maximum Mach:         {flight.max_mach_number:>10.3f}")
    print(f"Maximum Acceleration: {flight.max_acceleration:>10.2f} m/s²")
    print(f"Total Flight Time:    {flight.t_final:>10.2f} s")
    print(f"Impact Velocity:      {flight.impact_velocity:>10.2f} m/s")
    print(f"Out of Rail Velocity: {flight.out_of_rail_velocity:>10.2f} m/s")

    # Save results
    results = {
        "simulation_date": datetime.now().isoformat(),
        "simulation_type": "simplified",
        "apogee_m": float(flight.apogee),
        "apogee_time_s": float(flight.apogee_time),
        "max_speed_ms": float(flight.max_speed),
        "max_mach": float(flight.max_mach_number),
        "max_acceleration_ms2": float(flight.max_acceleration),
        "flight_time_s": float(flight.t_final),
        "impact_velocity_ms": float(flight.impact_velocity),
        "out_of_rail_velocity_ms": float(flight.out_of_rail_velocity),
        "x_impact_m": float(flight.x_impact),
        "y_impact_m": float(flight.y_impact)
    }

    results_file = output_dir / "simplified_results.json"
    with open(results_file, 'w') as f:
        json.dump(results, f, indent=2)

    print(f"\n✓ Results saved to: {results_file.name}")

    # Skip plots for headless mode
    print("\n(Skipping plot generation for headless mode)")

    print("\n" + "=" * 80)
    print("SUCCESS!")
    print("=" * 80)

except Exception as e:
    print(f"\n✗ SIMULATION FAILED:")
    print(f"  Error: {e}")
    import traceback
    traceback.print_exc()
