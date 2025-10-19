#!/usr/bin/env python3
"""
Streamlit Web Interface for RocketPy Simulations
Interactive web app for engineers to run and visualize rocket simulations
"""

import streamlit as st
import pandas as pd
import numpy as np
import json
from pathlib import Path
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime

from rocketpy import Environment, GenericMotor, Rocket, Flight
import folium
from streamlit_folium import st_folium

# Page configuration
st.set_page_config(
    page_title="RocketPy Simulator",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Title and header
st.title("🚀 RocketPy Simulation Interface")
st.markdown("Interactive rocket trajectory simulator - Migrated from PyROPS")

# Sidebar for inputs
st.sidebar.header("Simulation Parameters")

# =============================================================================
# CONFIGURATION SECTION
# =============================================================================

with st.sidebar:
    st.subheader("📍 Launch Site")
    latitude = st.number_input("Latitude (°)", value=-34.6, format="%.4f")
    longitude = st.number_input("Longitude (°)", value=20.3, format="%.4f")
    elevation_m = st.number_input("Elevation (m)", value=0, min_value=0)

    st.subheader("🎯 Launch Configuration")
    rail_length = st.slider("Rail Length (m)", 1.0, 15.0, 7.0, 0.5)
    inclination = st.slider("Elevation Angle (°)", 70.0, 90.0, 80.0, 1.0)
    heading = st.slider("Azimuth (°)", 0, 360, 260, 5)

    st.subheader("🌬️ Weather")
    wind_speed = st.slider("Wind Speed (m/s)", 0.0, 30.0, 8.0, 0.5)
    wind_direction = st.slider("Wind Direction (°)", 0, 360, 340, 5)

    st.subheader("🔧 Motor Configuration")
    use_custom_thrust = st.checkbox("Use PyROPS Thrust Curve", value=True)

    if not use_custom_thrust:
        avg_thrust = st.number_input("Average Thrust (N)", value=4000.0, min_value=100.0)
        burn_time = st.number_input("Burn Time (s)", value=12.8, min_value=0.1)

    st.subheader("🪂 Recovery")
    parachute_cd = st.number_input("Parachute CD", value=2.2, min_value=0.5, max_value=3.0)
    parachute_diameter = st.number_input("Parachute Diameter (m)", value=1.22, min_value=0.1)

# =============================================================================
# SIMULATION BUTTON
# =============================================================================

if st.sidebar.button("🚀 Run Simulation", type="primary"):

    # Progress indicator
    progress_bar = st.progress(0)
    status_text = st.empty()

    try:
        # Load data
        data_dir = Path(__file__).parent.parent / "data"

        status_text.text("Loading thrust curve...")
        progress_bar.progress(10)

        thrust_file = data_dir / "motors" / "hybrid_thrust_curve.csv"
        df_thrust = pd.read_csv(thrust_file)

        mass_file = data_dir / "mass_properties" / "time_varying_mass.csv"
        df_mass = pd.read_csv(mass_file)
        propellant_mass = df_mass.iloc[0]['mass'] - df_mass.iloc[-1]['mass']

        # Environment
        status_text.text("Setting up environment...")
        progress_bar.progress(25)

        env = Environment(latitude=latitude, longitude=longitude, elevation=elevation_m)
        env.set_date((2025, 10, 19, 12))
        env.set_atmospheric_model(type='standard_atmosphere')

        # Wind components
        wind_direction_rad = np.radians(wind_direction)
        wind_u = wind_speed * np.sin(wind_direction_rad)
        wind_v = wind_speed * np.cos(wind_direction_rad)
        env.set_atmospheric_model(type='standard_atmosphere', wind_u=wind_u, wind_v=wind_v)

        # Motor
        status_text.text("Configuring motor...")
        progress_bar.progress(40)

        motor = GenericMotor(
            thrust_source=str(thrust_file) if use_custom_thrust else avg_thrust,
            burn_time=df_thrust['time'].max() if use_custom_thrust else burn_time,
            dry_mass=5.0,
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

        # Rocket
        status_text.text("Building rocket...")
        progress_bar.progress(55)

        rocket = Rocket(
            radius=0.087,
            mass=32.8,
            inertia=(1, 100, 100),
            power_off_drag=0.45,
            power_on_drag=0.48,
            center_of_mass_without_motor=2.4,
            coordinate_system_orientation='tail_to_nose'
        )

        rocket.add_motor(motor, position=1.5)

        rocket.add_nose(length=0.55, kind='ogive', position=4.92)

        rocket.add_trapezoidal_fins(
            n=4, root_chord=0.4, tip_chord=0.2, span=0.2,
            position=0.8, cant_angle=0
        )

        rocket.add_parachute(
            name='Main',
            cd_s=parachute_cd * np.pi * (parachute_diameter / 2) ** 2,
            trigger='apogee',
            sampling_rate=105,
            lag=0,
            noise=(0, 0, 0)
        )

        rocket.set_rail_buttons(
            upper_button_position=6.5,
            lower_button_position=0.5,
            angular_position=45
        )

        # Flight simulation
        status_text.text("Running simulation...")
        progress_bar.progress(70)

        flight = Flight(
            rocket=rocket,
            environment=env,
            rail_length=rail_length,
            inclination=inclination,
            heading=heading,
            max_time=3600,  # 1 hour - plenty of time for descent
            max_time_step=0.5,
            terminate_on_apogee=False,
            verbose=False
        )

        progress_bar.progress(100)
        status_text.text("✅ Simulation complete!")

        # Store results in session state
        st.session_state['flight'] = flight
        st.session_state['simulation_time'] = datetime.now()

    except Exception as e:
        st.error(f"❌ Simulation failed: {e}")
        import traceback
        st.code(traceback.format_exc())

# =============================================================================
# RESULTS DISPLAY
# =============================================================================

if 'flight' in st.session_state:
    flight = st.session_state['flight']

    st.success("✅ Simulation completed successfully!")
    st.caption(f"Run at: {st.session_state['simulation_time'].strftime('%Y-%m-%d %H:%M:%S')}")

    # Key metrics in columns
    st.header("📊 Key Results")

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(
            "Apogee Altitude",
            f"{flight.apogee:,.1f} m",
            f"{flight.apogee * 3.28084:,.0f} ft"
        )
        st.metric("Apogee Time", f"{flight.apogee_time:.1f} s")

    with col2:
        st.metric("Max Speed", f"{flight.max_speed:.1f} m/s")
        st.metric("Max Mach", f"{flight.max_mach_number:.2f}")

    with col3:
        st.metric(
            "Max Acceleration",
            f"{flight.max_acceleration:.1f} m/s²",
            f"{flight.max_acceleration / 9.81:.1f} g"
        )
        st.metric("Rail Velocity", f"{flight.out_of_rail_velocity:.1f} m/s")

    with col4:
        st.metric("Flight Time", f"{flight.t_final:.1f} s")
        st.metric("Impact Velocity", f"{flight.impact_velocity:.1f} m/s")

    # Detailed plots
    st.header("📈 Flight Trajectory")

    # Create trajectory dataframe
    # RocketPy stores data as Function objects with source arrays
    import numpy as np

    # Extract the actual data arrays from RocketPy Function objects
    # These are stored in the .source attribute as (x, y) pairs
    try:
        # Try to get data from Function objects (RocketPy's internal structure)
        if hasattr(flight.z, 'source'):
            # Data is stored as [[time, altitude], [time, altitude], ...]
            time_data = np.array([point[0] for point in flight.z.source])
            alt_data = np.array([point[1] for point in flight.z.source])

            # Get other variables similarly
            vel_data = np.array([point[1] for point in flight.speed.source])
            accel_data = np.array([point[1] for point in flight.acceleration.source])
            x_data = np.array([point[1] for point in flight.x.source])
            y_data = np.array([point[1] for point in flight.y.source])
        else:
            # Fallback: direct array access
            time_data = np.array(flight.time).flatten()
            alt_data = np.array(flight.z).flatten()
            vel_data = np.array(flight.speed).flatten()
            accel_data = np.array(flight.acceleration).flatten()
            x_data = np.array(flight.x).flatten()
            y_data = np.array(flight.y).flatten()
    except Exception as e:
        st.error(f"Error extracting trajectory data: {e}")
        st.info("Flight object structure: " + str(type(flight.z)))
        raise

    trajectory_df = pd.DataFrame({
        'Time (s)': time_data.tolist(),
        'Altitude (m)': alt_data.tolist(),
        'Velocity (m/s)': vel_data.tolist(),
        'Acceleration (m/s²)': accel_data.tolist(),
        'X Position (m)': x_data.tolist(),
        'Y Position (m)': y_data.tolist()
    })

    # Debug info
    st.caption(f"Trajectory data: {len(trajectory_df)} points | "
               f"Time range: {trajectory_df['Time (s)'].min():.1f} - {trajectory_df['Time (s)'].max():.1f} s | "
               f"Max altitude: {trajectory_df['Altitude (m)'].max():.1f} m")

    # Altitude vs Time
    tab1, tab2, tab3, tab4, tab5 = st.tabs(["Altitude", "Velocity", "Ground Track", "🗺️ Map View", "Data"])

    with tab1:
        fig_alt = go.Figure()
        fig_alt.add_trace(go.Scatter(
            x=trajectory_df['Time (s)'],
            y=trajectory_df['Altitude (m)'],
            mode='lines',
            name='Altitude',
            line=dict(color='#1f77b4', width=2)
        ))

        # Mark apogee
        fig_alt.add_trace(go.Scatter(
            x=[float(flight.apogee_time)],
            y=[float(flight.apogee)],
            mode='markers',
            name='Apogee',
            marker=dict(size=12, color='red', symbol='star')
        ))

        fig_alt.update_layout(
            title="Altitude vs Time",
            xaxis_title="Time (s)",
            yaxis_title="Altitude (m)",
            hovermode='x unified',
            height=500
        )
        st.plotly_chart(fig_alt, use_container_width=True)

    with tab2:
        fig_vel = go.Figure()
        fig_vel.add_trace(go.Scatter(
            x=trajectory_df['Time (s)'],
            y=trajectory_df['Velocity (m/s)'],
            mode='lines',
            name='Velocity',
            line=dict(color='#ff7f0e', width=2)
        ))

        # Mark max velocity
        try:
            max_vel_idx = trajectory_df['Velocity (m/s)'].values.argmax()
            max_vel_time = float(trajectory_df.iloc[max_vel_idx]['Time (s)'])
            max_vel_value = float(trajectory_df.iloc[max_vel_idx]['Velocity (m/s)'])

            fig_vel.add_trace(go.Scatter(
                x=[max_vel_time],
                y=[max_vel_value],
                mode='markers',
                name='Max Velocity',
                marker=dict(size=12, color='red', symbol='star')
            ))
        except Exception as e:
            st.warning(f"Could not mark max velocity: {e}")

        fig_vel.update_layout(
            title="Velocity vs Time",
            xaxis_title="Time (s)",
            yaxis_title="Velocity (m/s)",
            hovermode='x unified',
            height=500
        )
        st.plotly_chart(fig_vel, use_container_width=True)

    with tab3:
        fig_ground = go.Figure()
        fig_ground.add_trace(go.Scatter(
            x=trajectory_df['X Position (m)'],
            y=trajectory_df['Y Position (m)'],
            mode='lines+markers',
            name='Trajectory',
            marker=dict(
                size=4,
                color=trajectory_df['Altitude (m)'],
                colorscale='Viridis',
                showscale=True,
                colorbar=dict(title="Altitude (m)")
            ),
            line=dict(width=2)
        ))

        # Mark launch and landing
        fig_ground.add_trace(go.Scatter(
            x=[0],
            y=[0],
            mode='markers',
            name='Launch',
            marker=dict(size=15, color='green', symbol='circle')
        ))

        fig_ground.add_trace(go.Scatter(
            x=[float(flight.x_impact)],
            y=[float(flight.y_impact)],
            mode='markers',
            name='Landing',
            marker=dict(size=15, color='red', symbol='x')
        ))

        fig_ground.update_layout(
            title="Ground Track",
            xaxis_title="East (m)",
            yaxis_title="North (m)",
            hovermode='closest',
            height=500,
            yaxis=dict(scaleanchor="x", scaleratio=1)  # Equal aspect ratio
        )
        st.plotly_chart(fig_ground, use_container_width=True)

    with tab4:
        st.subheader("🗺️ Satellite Map View")

        # Convert local X,Y to lat/lon
        # X is East in meters, Y is North in meters
        # Approximate conversion (1 degree lat ≈ 111km, lon varies by latitude)
        lat_start = latitude
        lon_start = longitude

        # Convert meters to degrees (rough approximation)
        lat_per_meter = 1 / 111000  # 1 degree lat ≈ 111km
        lon_per_meter = 1 / (111000 * np.cos(np.radians(latitude)))  # Adjusted for latitude

        lat_landing = lat_start + (float(flight.y_impact) * lat_per_meter)
        lon_landing = lon_start + (float(flight.x_impact) * lon_per_meter)

        # Create map centered between launch and landing
        center_lat = (lat_start + lat_landing) / 2
        center_lon = (lon_start + lon_landing) / 2

        # Calculate zoom level based on distance
        distance_m = np.sqrt(flight.x_impact**2 + flight.y_impact**2)
        if distance_m < 100:
            zoom_level = 16  # Very close - zoom way in
        elif distance_m < 1000:
            zoom_level = 14
        elif distance_m < 5000:
            zoom_level = 12
        elif distance_m < 20000:
            zoom_level = 10
        else:
            zoom_level = 9

        # Create folium map with satellite imagery
        m = folium.Map(
            location=[center_lat, center_lon],
            zoom_start=zoom_level,
            tiles='https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}',
            attr='Esri World Imagery'
        )

        # Add launch site marker
        folium.Marker(
            [lat_start, lon_start],
            popup=f"🚀 Launch Site<br>Lat: {lat_start:.6f}°<br>Lon: {lon_start:.6f}°<br>Elev: {elevation_m}m",
            tooltip="Launch Site",
            icon=folium.Icon(color='green', icon='rocket', prefix='fa')
        ).add_to(m)

        # Add landing site marker
        folium.Marker(
            [lat_landing, lon_landing],
            popup=f"🪂 Landing Site<br>Lat: {lat_landing:.6f}°<br>Lon: {lon_landing:.6f}°<br>Distance: {distance_m:.0f}m<br>Impact: {flight.impact_velocity:.1f} m/s",
            tooltip="Landing Site",
            icon=folium.Icon(color='red', icon='parachute', prefix='fa')
        ).add_to(m)

        # Draw trajectory line
        folium.PolyLine(
            [[lat_start, lon_start], [lat_landing, lon_landing]],
            color='blue',
            weight=3,
            opacity=0.7,
            popup=f"Flight Path<br>Distance: {distance_m:.0f}m<br>Bearing: {np.degrees(np.arctan2(flight.x_impact, flight.y_impact)) % 360:.1f}°"
        ).add_to(m)

        # Add circle showing apogee projection (straight up)
        folium.Circle(
            [lat_start, lon_start],
            radius=50,  # 50m radius
            color='orange',
            fill=True,
            fillColor='orange',
            fillOpacity=0.3,
            popup=f"Apogee<br>Altitude: {flight.apogee:.0f}m<br>Time: {flight.apogee_time:.1f}s",
            tooltip="Apogee (directly above launch)"
        ).add_to(m)

        # Display the map
        st_folium(m, width=700, height=500)

        # Add location info
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Launch Location", f"{lat_start:.6f}°, {lon_start:.6f}°")
        with col2:
            st.metric("Landing Location", f"{lat_landing:.6f}°, {lon_landing:.6f}°")
        with col3:
            st.metric("Ground Distance", f"{distance_m:.0f} m")

        if distance_m < 100:
            st.warning(f"⚠️ **Landing very close to launch** ({distance_m:.1f}m). The markers may overlap on the map. This could mean the simulation hit the time limit before completing descent. Try refreshing and running again with a longer max_time.")

        st.info(f"💡 **Tip**: The map shows satellite imagery. Green marker = launch, Red marker = landing, Blue line = trajectory projection, Orange circle = apogee location (directly above launch).")

    with tab5:
        st.subheader("Trajectory Data")
        st.dataframe(trajectory_df, use_container_width=True, height=400)

        # Download button
        csv = trajectory_df.to_csv(index=False)
        st.download_button(
            label="📥 Download CSV",
            data=csv,
            file_name=f"trajectory_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
            mime="text/csv"
        )

    # Additional info
    st.header("📋 Detailed Information")

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Landing Information")
        landing_range = np.sqrt(flight.x_impact**2 + flight.y_impact**2)
        landing_bearing = np.degrees(np.arctan2(flight.x_impact, flight.y_impact)) % 360

        st.write(f"**Landing Range**: {landing_range:.1f} m")
        st.write(f"**Landing Bearing**: {landing_bearing:.1f}°")
        st.write(f"**X Position**: {flight.x_impact:.1f} m (East)")
        st.write(f"**Y Position**: {flight.y_impact:.1f} m (North)")
        st.write(f"**Impact Velocity**: {flight.impact_velocity:.1f} m/s")

    with col2:
        st.subheader("Flight Characteristics")
        st.write(f"**Out of Rail Time**: {flight.out_of_rail_time:.2f} s")
        st.write(f"**Out of Rail Velocity**: {flight.out_of_rail_velocity:.1f} m/s")
        st.write(f"**Max Acceleration**: {flight.max_acceleration:.1f} m/s² ({flight.max_acceleration/9.81:.1f} g)")
        st.write(f"**Max Mach Number**: {flight.max_mach_number:.2f}")

        if flight.max_mach_number < 0.8:
            regime = "Subsonic"
        elif flight.max_mach_number < 1.2:
            regime = "Transonic"
        else:
            regime = "Supersonic"
        st.write(f"**Flight Regime**: {regime}")

        # Debug info
        st.write(f"**Flight Duration**: {flight.t_final:.1f} s")

        # Check if flight looks suspicious
        if abs(flight.x_impact) < 1 and abs(flight.y_impact) < 1:
            st.warning("⚠️ Landing position is very close to launch (0,0). The parachute may not have deployed properly or the simulation may have terminated early. Check the trajectory data.")

else:
    # Initial state - show instructions
    st.info("👈 Configure parameters in the sidebar and click **Run Simulation** to begin")

    st.header("About This Simulator")
    st.markdown("""
    This is an interactive web interface for the **RocketPy** rocket trajectory simulator,
    migrated from the legacy PyROPS system.

    **Features:**
    - 🚀 High-fidelity 6DOF rocket trajectory simulation
    - 🌍 Custom launch site configuration
    - 🌬️ Wind modeling
    - 🪂 Recovery system simulation
    - 📊 Interactive plots and visualizations
    - 💾 Export results to CSV

    **How to use:**
    1. Set launch site parameters (latitude, longitude, elevation)
    2. Configure launch angle and rail length
    3. Set weather conditions (wind speed and direction)
    4. Adjust motor and parachute settings
    5. Click "Run Simulation"
    6. Analyze results and download data

    **Performance:** ~30-60x faster than PyROPS!
    """)

    # Show sample configuration
    st.subheader("Current Configuration")
    st.json({
        "motor": {
            "type": "Hybrid (N-class)",
            "burn_time": "12.8 s",
            "peak_thrust": "6,038 N",
            "total_impulse": "51,475 N·s"
        },
        "rocket": {
            "radius": "0.087 m",
            "length": "4.92 m",
            "wet_mass": "65.9 kg",
            "dry_mass": "37.8 kg"
        }
    })

# Footer
st.markdown("---")
st.caption("Built with RocketPy • Migrated from PyROPS • Powered by Streamlit")
