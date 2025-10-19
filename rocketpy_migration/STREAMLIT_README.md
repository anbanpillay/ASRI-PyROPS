# 🚀 RocketPy Streamlit Web Interface

## Quick Start

```bash
# From the project root directory
source .venv/bin/activate
streamlit run rocketpy_migration/src/streamlit_app.py
```

The app will open in your browser at `http://localhost:8501`

## Features

✅ **Interactive Parameter Configuration**
- Launch site (latitude, longitude, elevation)
- Launch angle and rail configuration
- Wind conditions
- Motor settings
- Parachute parameters

✅ **Real-time Simulation**
- Runs RocketPy simulation with your parameters
- Progress indicators
- Error handling

✅ **Rich Visualizations**
- Altitude vs time plot
- Velocity profile
- Ground track (landing footprint)
- Interactive plots (zoom, pan, hover)

✅ **Data Export**
- Download trajectory data as CSV
- Share results with team
- Post-analysis in Excel/Python

✅ **Engineer-Friendly**
- No coding required
- Visual feedback
- Metric/imperial units
- Clear documentation

## What Your Engineers Can Do

1. **Run "What-If" Scenarios**
   - "What if we increase the rail length?"
   - "How does wind affect landing position?"
   - "What parachute size do we need?"

2. **Compare Configurations**
   - Run simulation, screenshot results
   - Change parameters, run again
   - Compare side-by-side

3. **Generate Reports**
   - Export CSV data
   - Capture plots (right-click → Save)
   - Document flight performance

4. **Collaborate**
   - Share URL (if deployed on server)
   - Discuss results in real-time
   - No software installation needed (if cloud-hosted)

## Deployment Options

### Option 1: Local (Current)
```bash
streamlit run rocketpy_migration/src/streamlit_app.py
```
- Runs on your machine
- Access at http://localhost:8501
- Good for development

### Option 2: Network (Team Access)
```bash
streamlit run rocketpy_migration/src/streamlit_app.py --server.address 0.0.0.0
```
- Accessible to anyone on your network
- Access at http://YOUR_IP:8501
- Good for team in same office

### Option 3: Cloud Deployment
Deploy to Streamlit Cloud (free for public repos):
```bash
# Push to GitHub
# Connect at https://streamlit.io/cloud
# Auto-deploys from your repo
```
- Accessible anywhere
- No server maintenance
- Free tier available

### Option 4: Enterprise Server
Deploy on your own server with Docker:
```dockerfile
FROM python:3.13
COPY . /app
WORKDIR /app
RUN pip install -r requirements.txt
CMD ["streamlit", "run", "rocketpy_migration/src/streamlit_app.py"]
```

## Screenshots

### Main Interface
- Sidebar: All input parameters
- Main area: Results and plots

### Results Display
- Key metrics in cards
- 4 tabs: Altitude, Velocity, Ground Track, Data

### Interactive Plots
- Zoom, pan, hover for details
- Download plots as PNG/SVG
- Professional quality for presentations

## Comments & Collaboration

**Add Comments Feature:**
You can extend the app to include:
```python
# At the bottom of the app
st.header("💬 Comments")
comment = st.text_area("Add comments about this simulation:")
if st.button("Save Comment"):
    # Save to database or file
    save_comment(comment, simulation_params, results)
```

**Multi-user Features:**
- User authentication (Streamlit has built-in auth)
- Save/load simulation configurations
- Compare multiple runs
- Team annotations

## Next Steps

1. **Run it**: Try the current version
2. **Customize**: Add your team's specific parameters
3. **Extend**: Add features you need (see below)
4. **Deploy**: Put it on a server for team access

## Possible Extensions

**Easy Additions:**
- [ ] Comparison mode (run 2 simulations side-by-side)
- [ ] Save/load configurations
- [ ] Monte Carlo mode (multiple runs with uncertainty)
- [ ] Export to PDF report
- [ ] Email results
- [ ] Comments/annotations system

**Advanced Features:**
- [ ] Multi-stage rockets
- [ ] Real-time telemetry comparison
- [ ] Optimization (find best fin size, etc.)
- [ ] 3D trajectory visualization
- [ ] Flight animation
- [ ] Weather API integration (real-time wind data)

## Comparison: Streamlit vs Command Line

| Feature | Command Line | Streamlit App |
|---------|-------------|---------------|
| Ease of Use | Requires coding | Click & type |
| Visualization | Separate scripts | Built-in interactive |
| Parameter Changes | Edit code | Sliders & inputs |
| Results | Text output | Visual dashboards |
| Sharing | Send files | Share URL |
| Learning Curve | Python knowledge | None |
| Team Friendly | ❌ | ✅ |
| Engineer Friendly | ❌ | ✅ |

## Technical Notes

**Browser Requirements:**
- Modern browser (Chrome, Firefox, Safari, Edge)
- JavaScript enabled
- No special plugins needed

**Performance:**
- Simulation runs server-side
- Results sent to browser
- Fast for single simulations
- For Monte Carlo (1000s of runs), consider CLI

**Security:**
- If deployed publicly, add authentication
- Use HTTPS for production
- Validate all user inputs (already done)

---

**Made for Engineers, by Engineers** 🛠️
