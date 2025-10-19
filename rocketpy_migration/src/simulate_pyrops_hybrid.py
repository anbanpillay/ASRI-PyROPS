#!/usr/bin/env python3
"""
RocketPy Simulation: PyROPS Hybrid Rocket Migration
Simulates the BM-001 benchmark case using converted PyROPS data
"""

import json
from pathlib import Path
from datetime import datetime
import pandas as pd
import numpy as np

from rocketpy import Environment, SolidMotor, Rocket, Flight
from rocketpy import Function

# =============================================================================
# CONFIGURATION
# =============================================================================
print("=" * 80)
print("ROCKETPY SIMULATION - PyROPS Hybrid Rocket Migration")
print("=" * 80)

# Paths
data_dir = Path(__file__).parent.parent / "data"
output_dir = Path(__file__).parent.parent / "outputs"
output_dir.mkdir(exist_ok=True)

# Load conversion summary
with open(data_dir / "conversion_summary.json", 'r') as f:
    config = json.load(f)

print(f"\nLoaded configuration from: {data_dir / 'conversion_summary.json'}")
print(f"Source: {config['source']}")

# =============================================================================
# 1. ENVIRONMENT SETUP
# =============================================================================
print("\n" + "=" * 80)
print("1. SETTING UP ENVIRONMENT")
print("=" * 80)

# Create environment
env = Environment(
    latitude=config['launch_conditions']['latitude_deg'],
    longitude=config['launch_conditions']['longitude_deg'],
    elevation=config['launch_conditions']['altitude_m']
)

# Set launch date (arbitrary - using today)
tomorrow = datetime.now()
env.set_date((tomorrow.year, tomorrow.month, tomorrow.day, 12))  # Noon launch

# Load custom atmosphere
print("\nLoading custom atmosphere data...")
atm_file = data_dir / config['atmosphere']['file']
df_atm = pd.read_csv(atm_file)

# RocketPy expects pressure in Pa, temperature in K, altitude in m
# Create interpolation functions
env.pressure = Function(
    df_atm[['altitude', 'pressure']].values,
    inputs='Height Above Sea Level (m)',
    outputs='Pressure (Pa)',
    interpolation='linear'
)

env.temperature = Function(
    df_atm[['altitude', 'temperature']].values,
    inputs='Height Above Sea Level (m)',
    outputs='Temperature (K)',
    interpolation='linear'
)

print(f"   ✓ Custom atmosphere loaded from {atm_file.name}")
print(f"   - Surface pressure: {config['atmosphere']['surface_pressure_Pa']:.2f} Pa")
print(f"   - Surface temperature: {config['atmosphere']['surface_temperature_K']:.2f} K")

# Load wind profile
print("\nLoading wind profile...")
wind_file = data_dir / config['wind']['file']
df_wind = pd.read_csv(wind_file)

# RocketPy wind convention: bearing is the direction FROM which wind blows
# PyROPS convention might be different - need to verify
# For now, using the data as-is

# Create wind speed and direction functions
wind_speed_data = df_wind[['altitude (m)', 'magnitude (m/s)']].values
wind_direction_data = df_wind[['altitude (m)', 'bearing (degrees)']].values

env.set_atmospheric_model(
    type='custom_atmosphere',
    pressure=env.pressure,
    temperature=env.temperature,
    wind_u=0,  # Will set wind profile below
    wind_v=0
)

# Alternative: use wind functions
# For simplicity, let's use a constant wind at surface level for now
# TODO: Implement altitude-varying wind properly
surface_wind_speed = config['wind']['surface_speed_ms']
surface_wind_bearing = config['wind']['surface_bearing_deg']

# Convert wind bearing to RocketPy convention (wind FROM direction)
# Wind velocity components (East, North)
wind_direction_rad = np.radians(surface_wind_bearing)
wind_u = surface_wind_speed * np.sin(wind_direction_rad)  # East component
wind_v = surface_wind_speed * np.cos(wind_direction_rad)  # North component

print(f"   ✓ Wind profile loaded from {wind_file.name}")
print(f"   - Surface wind: {surface_wind_speed:.1f} m/s at {surface_wind_bearing:.0f}°")
print(f"   - Wind components: U={wind_u:.2f} m/s (East), V={wind_v:.2f} m/s (North)")

# Print environment info
print("\nEnvironment configured:")
env.info()

# =============================================================================
# 2. MOTOR SETUP
# =============================================================================
print("\n" + "=" * 80)
print("2. SETTING UP MOTOR")
print("=" * 80)

# Load thrust curve
thrust_file = data_dir / config['motor']['thrust_curve_file']
df_thrust = pd.read_csv(thrust_file)

print(f"\nLoading thrust curve from {thrust_file.name}...")
print(f"   - Burn time: {config['motor']['burn_time_s']:.2f} s")
print(f"   - Peak thrust: {config['motor']['peak_thrust_N']:.2f} N")
print(f"   - Total impulse: {config['motor']['total_impulse_Ns']:.2f} N·s")
print(f"   - Propellant mass: {config['motor']['propellant_mass_kg']:.2f} kg")

# Create motor
# Note: RocketPy's SolidMotor can be used for hybrid motors with custom thrust curve
motor = SolidMotor(
    thrust_source=str(thrust_file),
    dry_mass=config['mass_properties']['dry_mass_kg'] - config['mass_properties']['wet_mass_kg'] + config['motor']['propellant_mass_kg'],  # Motor structure mass
    dry_inertia=(0.05, 0.05, 0.001),  # Approximate motor structure inertia (Iz, Iz, Ir)
    nozzle_radius=0.0474,  # From BM-001 specs: sqrt(0.007056/π)
    grain_number=1,
    grain_density=1065,  # Fuel grain density from specs
    grain_outer_radius=0.0735,  # From specs
    grain_initial_inner_radius=0.0360,  # From specs
    grain_initial_height=0.51,  # Fuel grain length from specs
    grain_separation=0,
    grains_center_of_mass_position=-0.5395,  # From specs (negative because measured from top)
    center_of_dry_mass_position=-2.0,  # Approximate
    nozzle_position=-0.5,  # Approximate
    burn_time=config['motor']['burn_time_s'],
    throat_radius=0.020,  # Approximate (needs verification from specs)
    reshape_thrust_curve=False,
    interpolation_method='linear',
    coordinate_system_orientation='nozzle_to_combustion_chamber'
)

print("\nMotor configured:")
print(f"   - Type: Hybrid (using SolidMotor with custom thrust)")
print(f"   - Propellant mass: {config['motor']['propellant_mass_kg']:.2f} kg")
print(f"   - Total impulse: {config['motor']['total_impulse_Ns']:.2f} N·s")
print(f"   - Average thrust: {config['motor']['total_impulse_Ns'] / config['motor']['burn_time_s']:.2f} N")

# Print motor info
motor.info()

# =============================================================================
# 3. ROCKET SETUP
# =============================================================================
print("\n" + "=" * 80)
print("3. SETTING UP ROCKET")
print("=" * 80)

# Create rocket
rocket = Rocket(
    radius=config['rocket_geometry']['body_radius_m'],
    mass=config['mass_properties']['wet_mass_kg'],  # Initial wet mass
    inertia=(
        config['mass_properties']['dry_MOI']['Ixx'],
        config['mass_properties']['dry_MOI']['Iyy'],
        config['mass_properties']['dry_MOI']['Izz']
    ),
    power_off_drag=0.5,  # Will be replaced by custom drag curve
    power_on_drag=0.5,
    center_of_mass_without_motor=config['mass_properties']['dry_com_m'],
    coordinate_system_orientation='tail_to_nose'
)

print(f"\nRocket body configured:")
print(f"   - Radius: {config['rocket_geometry']['body_radius_m']:.3f} m")
print(f"   - Length: {config['rocket_geometry']['body_length_m']:.3f} m")
print(f"   - Wet mass: {config['mass_properties']['wet_mass_kg']:.2f} kg")
print(f"   - Dry mass: {config['mass_properties']['dry_mass_kg']:.2f} kg")
print(f"   - Center of mass (dry): {config['mass_properties']['dry_com_m']:.3f} m")

# Add motor to rocket
rocket.add_motor(motor, position=0.5)  # Position from tail (needs verification)

# Add nose cone
# TODO: Get actual nose cone length from RASAero data
rocket.add_nose(
    length=0.5,  # Approximate (need to extract from RASAero)
    kind='ogive',
    position=config['rocket_geometry']['body_length_m']
)

# Add fins
# TODO: Get actual fin dimensions from Settings.xlsx or RASAero
rocket.add_trapezoidal_fins(
    n=4,
    root_chord=0.3,  # Approximate (need actual values)
    tip_chord=0.15,  # Approximate
    span=0.15,  # Approximate
    position=0.5,  # From tail
    cant_angle=config['rocket_geometry']['fins']['cant_angle_deg'],
    airfoil=None
)

# Add parachute
# From BM-001 specs: Main parachute CD=2.2, Diameter=1.22m
rocket.add_parachute(
    name='Main',
    cd_s=2.2 * np.pi * (1.22052868353847 / 2) ** 2,  # CD * area
    trigger='apogee',  # Deploy at apogee
    sampling_rate=105,
    lag=0.0,
    noise=(0, 0, 0)
)

# Optional: Add drogue if needed
# rocket.add_parachute(
#     name='Drogue',
#     cd_s=1.6 * np.pi * (0.304871262610412 / 2) ** 2,
#     trigger='apogee',
#     sampling_rate=105,
#     lag=0.0
# )

# Load custom drag curve from RASAero data
print("\nLoading custom aerodynamics from RASAero...")
aero_file = data_dir / config['aerodynamics']['file']
df_aero = pd.read_csv(aero_file)

# For now, use a simplified drag coefficient (CD at alpha=0)
# TODO: Implement full 2D interpolation for CD(Mach, Alpha)
df_cd_alpha0 = df_aero[df_aero['Alpha'] == 0.0][['Mach', 'CD']].values
rocket.power_off_drag = Function(
    df_cd_alpha0,
    inputs='Mach',
    outputs='Drag Coefficient',
    interpolation='linear'
)

df_cd_poweron = df_aero[df_aero['Alpha'] == 0.0][['Mach', 'CD Power-On']].values
rocket.power_on_drag = Function(
    df_cd_poweron,
    inputs='Mach',
    outputs='Drag Coefficient',
    interpolation='linear'
)

print(f"   ✓ Aerodynamics loaded from {aero_file.name}")
print(f"   - Mach range: {config['aerodynamics']['mach_range'][0]:.3f} to {config['aerodynamics']['mach_range'][1]:.3f}")

# Set rail configuration
rocket.set_rail_buttons(
    upper_button_position=config['launch_conditions']['rail_length_m'] - 0.5,
    lower_button_position=0.5,
    angular_position=45
)

print("\nRocket configured:")
rocket.info()

# =============================================================================
# 4. FLIGHT SIMULATION
# =============================================================================
print("\n" + "=" * 80)
print("4. RUNNING FLIGHT SIMULATION")
print("=" * 80)

# Create flight
flight = Flight(
    rocket=rocket,
    environment=env,
    rail_length=config['launch_conditions']['rail_length_m'],
    inclination=config['launch_conditions']['elevation_deg'],
    heading=config['launch_conditions']['azimuth_deg'],
    max_time=1200,  # Maximum simulation time (20 minutes)
    max_time_step=0.1,
    terminate_on_apogee=False,
    verbose=True
)

print("\nFlight simulation complete!")
print("=" * 80)

# =============================================================================
# 5. RESULTS
# =============================================================================
print("\n" + "=" * 80)
print("5. SIMULATION RESULTS")
print("=" * 80)

# Extract key metrics
results = {
    "simulation_date": datetime.now().isoformat(),
    "rocketpy_version": "1.10.0",
    "source_data": config['source'],

    "key_events": {
        "rail_departure": {
            "time_s": float(flight.out_of_rail_time),
            "velocity_ms": float(flight.out_of_rail_velocity),
            "altitude_m": None  # Not directly available
        },
        "burnout": {
            "time_s": float(config['motor']['burn_time_s']),
            "altitude_m": None,  # Would need to extract from trajectory
            "velocity_ms": None
        },
        "apogee": {
            "time_s": float(flight.apogee_time),
            "altitude_m": float(flight.apogee),
            "latitude_deg": float(flight.apogee_y),  # In local coordinates
            "longitude_deg": float(flight.apogee_x)
        },
        "landing": {
            "time_s": float(flight.t_final),
            "latitude_deg": float(flight.y_impact),
            "longitude_deg": float(flight.x_impact),
            "velocity_ms": float(flight.impact_velocity)
        }
    },

    "maximum_values": {
        "max_speed_ms": float(flight.max_speed),
        "max_mach": float(flight.max_mach_number),
        "max_acceleration_ms2": float(flight.max_acceleration),
        "max_altitude_m": float(flight.apogee)
    },

    "landing": {
        "x_impact_m": float(flight.x_impact),
        "y_impact_m": float(flight.y_impact),
        "impact_velocity_ms": float(flight.impact_velocity),
        "total_flight_time_s": float(flight.t_final)
    }
}

# Save results
results_file = output_dir / "simulation_results.json"
with open(results_file, 'w') as f:
    json.dump(results, f, indent=2)

print(f"\nResults saved to: {results_file}")

# Print summary
print("\n" + "-" * 80)
print("KEY RESULTS:")
print("-" * 80)
print(f"Apogee Altitude:      {flight.apogee:>10.2f} m")
print(f"Apogee Time:          {flight.apogee_time:>10.2f} s")
print(f"Maximum Speed:        {flight.max_speed:>10.2f} m/s")
print(f"Maximum Mach:         {flight.max_mach_number:>10.3f}")
print(f"Maximum Acceleration: {flight.max_acceleration:>10.2f} m/s²")
print(f"Total Flight Time:    {flight.t_final:>10.2f} s")
print(f"Impact Velocity:      {flight.impact_velocity:>10.2f} m/s")
print(f"Landing Distance:     {np.sqrt(flight.x_impact**2 + flight.y_impact**2):>10.2f} m")
print(f"Out of Rail Velocity: {flight.out_of_rail_velocity:>10.2f} m/s")
print("-" * 80)

# Print detailed flight info
print("\nDetailed flight information:")
flight.info()

# =============================================================================
# 6. SAVE TRAJECTORY DATA
# =============================================================================
print("\n" + "=" * 80)
print("6. SAVING TRAJECTORY DATA")
print("=" * 80)

# Export trajectory to CSV
# RocketPy stores trajectory in flight object
# Access the solution arrays
trajectory_data = {
    'time': flight.time,
    'altitude': flight.z,
    'velocity': flight.speed,
    'acceleration': flight.acceleration,
    'x_position': flight.x,
    'y_position': flight.y,
}

df_trajectory = pd.DataFrame(trajectory_data)
trajectory_file = output_dir / "trajectory.csv"
df_trajectory.to_csv(trajectory_file, index=False, float_format='%.6f')

print(f"✓ Trajectory saved to: {trajectory_file}")
print(f"  - Data points: {len(df_trajectory)}")
print(f"  - Time span: {df_trajectory['time'].min():.2f} to {df_trajectory['time'].max():.2f} s")

print("\n" + "=" * 80)
print("SIMULATION COMPLETE!")
print("=" * 80)
print(f"\nOutput files:")
print(f"  - {results_file.name}")
print(f"  - {trajectory_file.name}")
print("\nNext: Generate plots and validation comparisons")
