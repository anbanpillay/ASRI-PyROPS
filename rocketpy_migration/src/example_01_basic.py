"""
Example 1: Basic RocketPy Simulation
=====================================

This is a simple example to verify RocketPy installation and understand basic usage.
Based on the Calisto rocket example from RocketPy documentation.

Run: python example_01_basic.py
"""

from rocketpy import Environment, SolidMotor, Rocket, Flight
import datetime

print("="*60)
print("RocketPy Basic Example - Calisto Rocket")
print("="*60)
print()

# Step 1: Create Environment
print("1. Creating environment...")
env = Environment(
    latitude=32.990254,
    longitude=-106.974998,
    elevation=1400,
    date=(2020, 3, 4, 12)  # Tomorrow 12:00 UTC
)

# Set atmospheric model to standard atmosphere
env.set_atmospheric_model(type='standard_atmosphere')

print(f"   Location: {env.latitude}°N, {env.longitude}°E")
print(f"   Elevation: {env.elevation} m")
print()

# Step 2: Create Motor
print("2. Creating solid motor...")
motor = SolidMotor(
    thrust_source="../data/motors/Cesaroni_M1670.eng",  # Will create this file
    burn_time=3.9,
    dry_mass=1.815,
    dry_inertia=(0.125, 0.125, 0.002),
    center_of_dry_mass_position=0.317,
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

print(f"   Motor: Cesaroni M1670")
print(f"   Burn time: {motor.burn_time} s")
print(f"   Dry mass: {motor.dry_mass} kg")
print()

# Step 3: Create Rocket
print("3. Creating rocket...")
rocket = Rocket(
    radius=0.0635,
    mass=14.426,
    inertia=(6.321, 6.321, 0.034),
    power_off_drag=0.5,  # Simple constant drag coefficient
    power_on_drag=0.5,
    center_of_mass_without_motor=0,
    coordinate_system_orientation="tail_to_nose",
)

# Add motor to rocket
rocket.add_motor(motor, position=-1.373)

print(f"   Rocket radius: {rocket.radius} m")
print(f"   Total mass: {rocket.mass} kg")
print()

# Step 4: Add fins
print("4. Adding fins...")
fins = rocket.add_trapezoidal_fins(
    n=4,
    span=0.100,
    root_chord=0.120,
    tip_chord=0.040,
    position=-1.168,
)

print(f"   Number of fins: 4")
print(f"   Fin span: 0.100 m")
print()

# Step 5: Add parachute
print("5. Adding parachute...")
parachute = rocket.add_parachute(
    name="Main",
    cd_s=10.0,
    trigger="apogee",
    sampling_rate=105,
    lag=1.5,
    noise=(0, 8.3, 0.5),
)

print(f"   Parachute CD*S: 10.0 m²")
print(f"   Trigger: apogee + 1.5 s delay")
print()

# Step 6: Simulate Flight
print("6. Running flight simulation...")
print("   (This may take a few seconds)")
print()

flight = Flight(
    rocket=rocket,
    environment=env,
    rail_length=5.2,
    inclination=85,
    heading=0,
)

print("="*60)
print("SIMULATION RESULTS")
print("="*60)
print()

# Display key results
print(f"Launch Site:")
print(f"  Latitude:  {env.latitude:.6f}°")
print(f"  Longitude: {env.longitude:.6f}°")
print(f"  Elevation: {env.elevation} m")
print()

print(f"Flight Performance:")
print(f"  Apogee:              {flight.apogee:.2f} m")
print(f"  Apogee Time:         {flight.apogee_time:.2f} s")
print(f"  Max Speed:           {flight.max_speed:.2f} m/s")
print(f"  Max Acceleration:    {flight.max_acceleration:.2f} m/s²")
print(f"  Max Mach:            {flight.max_mach_number:.3f}")
print()

print(f"Landing:")
print(f"  Impact Time:         {flight.t_final:.2f} s")
print(f"  Impact Velocity:     {flight.impact_velocity:.2f} m/s")
print(f"  Landing Position:    x={flight.x_impact:.2f} m, y={flight.y_impact:.2f} m")
print()

print("="*60)
print("✓ Simulation completed successfully!")
print("="*60)
print()

print("Next steps:")
print("  1. Review RocketPy documentation: https://docs.rocketpy.org/")
print("  2. Understand Environment, Motor, Rocket, Flight classes")
print("  3. Proceed to Phase 2: Extract PyROPS benchmark test cases")
print()
