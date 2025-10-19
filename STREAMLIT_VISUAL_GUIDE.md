# 🎨 Streamlit Interface Visual Guide

## What You'll See When You Open http://localhost:8502

```
┌─────────────────────────────────────────────────────────────────────────┐
│                                                                         │
│  🚀 RocketPy Simulation Interface                                      │
│  Interactive rocket trajectory simulator - Migrated from PyROPS        │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘

┌──────────────────────┬──────────────────────────────────────────────────┐
│                      │                                                  │
│  SIDEBAR             │  MAIN AREA                                       │
│  (Left Side)         │  (Right Side - Large)                            │
│                      │                                                  │
│  ┌────────────────┐  │  Before First Run:                               │
│  │ Simulation     │  │  ╔═══════════════════════════════════════╗       │
│  │ Parameters     │  │  ║ 👈 Configure parameters in the       ║       │
│  └────────────────┘  │  ║    sidebar and click Run Simulation  ║       │
│                      │  ║    to begin                           ║       │
│  📍 Launch Site      │  ╚═══════════════════════════════════════╝       │
│  [Latitude  -34.6 ]  │                                                  │
│  [Longitude  20.3 ]  │  About This Simulator                            │
│  [Elevation    0m ]  │  • High-fidelity 6DOF simulation                 │
│                      │  • Custom launch site configuration              │
│  🎯 Launch Config    │  • Wind modeling                                 │
│  Rail: [====7.0==]   │  • Recovery system simulation                    │
│  Elev: [====80°==]   │  • Interactive plots                             │
│  Azim: [===260°==]   │                                                  │
│                      │  After You Run:                                  │
│  🌬️ Weather          │  ╔══════════════════════════════════════╗        │
│  Wind: [====8===]    │  ║ ✅ Simulation completed!             ║        │
│  Dir:  [==340°==]    │  ╚══════════════════════════════════════╝        │
│                      │                                                  │
│  🔧 Motor Config     │  📊 Key Results                                  │
│  [✓] PyROPS Curve    │  ┌─────────┬─────────┬─────────┬─────────┐      │
│                      │  │ Apogee  │Max Speed│Max Accel│Rail Vel │      │
│  🪂 Recovery         │  │12,860 m │ 629.8   │ 82.1    │ 18.1    │      │
│  CD:    [==2.2==]    │  │42,190ft │  m/s    │  m/s²   │  m/s    │      │
│  Diam:  [==1.2==]    │  └─────────┴─────────┴─────────┴─────────┘      │
│                      │                                                  │
│  ┌────────────────┐  │  📈 Flight Trajectory                            │
│  │  🚀 Run        │  │  [Altitude] [Velocity] [Ground Track] [Data]    │
│  │  Simulation    │  │  ┌───────────────────────────────────────┐      │
│  └────────────────┘  │  │           Altitude vs Time            │      │
│                      │  │  15000─┐                    ★ Apogee   │      │
│                      │  │        │                  ╱   ╲        │      │
│                      │  │  10000─┤                ╱       ╲      │      │
│                      │  │        │              ╱           ╲    │      │
│                      │  │   5000─┤            ╱              ╲  │      │
│                      │  │        │          ╱                  ╲│      │
│                      │  │      0─┴────────────────────────────── │      │
│                      │  │        0s    20s   40s   60s   80s    │      │
│                      │  │                                        │      │
│                      │  │  🔍 Hover for details                  │      │
│                      │  │  🖱️ Click and drag to zoom             │      │
│                      │  └───────────────────────────────────────┘      │
│                      │                                                  │
└──────────────────────┴──────────────────────────────────────────────────┘
```

---

## Detailed View: Each Section

### 1. Sidebar Controls

```
┌─────────────────────────────┐
│ 📍 Launch Site              │
│ ───────────────────────────│
│ Latitude (°)                │
│ ┌─────────────────────────┐│
│ │ -34.6                   ││
│ └─────────────────────────┘│
│                             │
│ Longitude (°)               │
│ ┌─────────────────────────┐│
│ │ 20.3                    ││
│ └─────────────────────────┘│
│                             │
│ Elevation (m)               │
│ ┌─────────────────────────┐│
│ │ 0                       ││
│ └─────────────────────────┘│
└─────────────────────────────┘

┌─────────────────────────────┐
│ 🎯 Launch Configuration     │
│ ───────────────────────────│
│ Rail Length (m)             │
│ ├──────●──────┤ 7.0        │
│ 1.0         15.0            │
│                             │
│ Elevation Angle (°)         │
│ ├───────────●─┤ 80.0       │
│ 70°         90°             │
│                             │
│ Azimuth (°)                 │
│ ├────────●────┤ 260        │
│ 0          360              │
└─────────────────────────────┘

┌─────────────────────────────┐
│ 🌬️ Weather                  │
│ ───────────────────────────│
│ Wind Speed (m/s)            │
│ ├───●──────────┤ 8.0       │
│ 0.0         30.0            │
│                             │
│ Wind Direction (°)          │
│ ├─────────●────┤ 340       │
│ 0          360              │
└─────────────────────────────┘

┌─────────────────────────────┐
│         Big Button!         │
│  ┌─────────────────────────┐│
│  │  🚀 Run Simulation      ││
│  │  (Click me!)            ││
│  └─────────────────────────┘│
└─────────────────────────────┘
```

### 2. Results Display

```
After clicking "Run Simulation":

┌──────────────────────────────────────────────┐
│ ✅ Simulation completed successfully!        │
│ Run at: 2025-10-19 19:32:15                  │
└──────────────────────────────────────────────┘

📊 Key Results
┌───────────────┬───────────────┬───────────────┬──────────────┐
│ Apogee Alt.   │ Apogee Time   │ Max Speed     │ Max Mach     │
│ 12,859.99 m   │ 49.40 s       │ 629.82 m/s    │ 1.927        │
│ 42,189.93 ft  │               │               │              │
└───────────────┴───────────────┴───────────────┴──────────────┘

┌───────────────┬───────────────┬───────────────┬──────────────┐
│ Max Accel     │ Rail Velocity │ Flight Time   │ Impact Vel   │
│ 82.14 m/s²    │ 18.06 m/s     │ 600.00 s      │ 0.00 m/s     │
│ 8.4 g         │               │               │              │
└───────────────┴───────────────┴───────────────┴──────────────┘
```

### 3. Interactive Plots

```
📈 Flight Trajectory

┌─────────────────────────────────────────────────────┐
│ [Altitude] [Velocity] [Ground Track] [Data]         │
└─────────────────────────────────────────────────────┘

TAB 1: Altitude
┌──────────────────────────────────────────────────────┐
│            Altitude vs Time                          │
│                                                      │
│  15000 ┐                                             │
│        │                         ★ Apogee           │
│        │                      ╱      ╲               │
│  10000 ┤                   ╱           ╲             │
│        │                 ╱               ╲           │
│   5000 ┤              ╱                    ╲         │
│        │           ╱                         ╲       │
│      0 ┴────────────────────────────────────────╲───│
│        0s    100s    200s    300s    400s    500s   │
│                                                      │
│  Hover over line to see exact values!               │
└──────────────────────────────────────────────────────┘

TAB 2: Velocity
┌──────────────────────────────────────────────────────┐
│            Velocity vs Time                          │
│                                                      │
│   700 ┐                                              │
│       │          ★ Max                               │
│   500 ┤        ╱  ╲                                  │
│       │      ╱      ╲___                             │
│   300 ┤    ╱            ───___                       │
│       │  ╱                     ────___               │
│   100 ┤╱                               ────___       │
│       │                                       ──___  │
│     0 ┴──────────────────────────────────────────── │
│       0s    100s    200s    300s    400s    500s    │
└──────────────────────────────────────────────────────┘

TAB 3: Ground Track
┌──────────────────────────────────────────────────────┐
│            Ground Track (Landing Footprint)          │
│                                                      │
│   N                                                  │
│   ↑                         ×  Landing               │
│   │                       ╱                          │
│   │                     ╱                            │
│   │                   ╱                              │
│   │                 ╱                                │
│   │               ●  Launch                          │
│   │                                                  │
│   └──────────────────→ E                            │
│                                                      │
│  Colors show altitude (red=high, blue=low)          │
└──────────────────────────────────────────────────────┘

TAB 4: Data
┌──────────────────────────────────────────────────────┐
│  Time | Altitude | Velocity | Acceleration | ...     │
│ ──────┼──────────┼──────────┼──────────────┼────    │
│  0.00 │    0.00  │    0.00  │     0.00     │        │
│  0.10 │    0.09  │    1.80  │    18.00     │        │
│  0.20 │    0.36  │    3.60  │    18.00     │        │
│  ...  │    ...   │    ...   │     ...      │        │
│                                                      │
│  [📥 Download CSV]                                   │
└──────────────────────────────────────────────────────┘
```

---

## Color Scheme

The interface uses a clean, professional color scheme:
- **Primary**: Blue/Purple (action buttons)
- **Success**: Green (completion messages)
- **Data**: Viridis colormap (scientific standard)
- **Background**: Light gray (easy on eyes)

---

## Interactive Features

### 🖱️ Mouse Actions

**On Plots:**
- **Hover**: See exact values at that point
- **Click & Drag**: Zoom into region
- **Double-click**: Reset zoom
- **Scroll**: Zoom in/out

**On Sliders:**
- **Click & Drag**: Change value smoothly
- **Click on track**: Jump to value
- **Arrow keys**: Fine adjustment

### ⌨️ Keyboard Shortcuts

- **Tab**: Navigate between fields
- **Enter**: Submit text input (doesn't run simulation)
- **Space**: Toggle checkboxes
- **Ctrl+C** (in terminal): Stop server

---

## Mobile View

On phone/tablet, the layout adapts:

```
┌────────────────────┐
│  🚀 RocketPy       │
│  ═══════════════   │
│                    │
│  ≡ Menu (tap here) │
│  ─────────────────│
│                    │
│  📊 Key Results    │
│  ┌────────────────┐│
│  │ Apogee: 12,860 ││
│  │ Max Speed: 630 ││
│  └────────────────┘│
│                    │
│  📈 Plots          │
│  (swipe between)   │
│  ┌────────────────┐│
│  │                ││
│  │   Graph Here   ││
│  │                ││
│  └────────────────┘│
└────────────────────┘
```

Sidebar becomes collapsible menu (≡ button)

---

## Pro Tips

### Make Plots Bigger
- Click fullscreen icon (top-right of plot)
- Or drag window larger

### Export Plot as Image
- Hover over plot
- Camera icon appears
- Click to download PNG

### Copy Values
- Click on data table cells
- Ctrl+C to copy
- Paste into Excel

### Compare Runs
- Screenshot results before changing
- Or open second browser tab
- Or use comparison mode (feature request!)

---

## What Each Color Means

### Ground Track Plot
- 🟢 Green circle: Launch site
- 🔴 Red X: Landing site
- 🌈 Rainbow line: Flight path
  - Red/Yellow: High altitude
  - Green/Blue: Low altitude

### Status Messages
- 🟢 Green box: Success
- 🔴 Red box: Error
- 🔵 Blue box: Info
- ⏳ Progress bar: Running

---

## Common Workflows

### 1. "What If?" Exploration
```
1. Run with defaults
2. Note apogee: 12,860m
3. Increase wind to 15 m/s
4. Run again
5. Note apogee: 12,840m
6. Conclusion: Wind has small effect on apogee!
```

### 2. Landing Zone Sizing
```
1. Run with 5 m/s wind → Landing at (523m, 891m)
2. Run with 10 m/s wind → Landing at (1046m, 1782m)
3. Run with 15 m/s wind → Landing at (1569m, 2673m)
4. Draw circle encompassing all three
5. That's your landing zone!
```

### 3. Performance Optimization
```
1. Try elevation 85° → Apogee: 13,100m
2. Try elevation 80° → Apogee: 12,860m
3. Try elevation 75° → Apogee: 12,350m
4. Optimal: 85° (but less stable)
5. Practical choice: 80° (good balance)
```

---

## Need Help?

If something doesn't look right:

1. **Refresh browser** (F5 or Cmd+R)
2. **Clear cache** (Ctrl+Shift+Del)
3. **Check terminal** for error messages
4. **Restart app** (Ctrl+C, then ./run_streamlit.sh)

Still stuck? Check `QUICK_START.md` troubleshooting section!

---

**Ready to explore?** Open http://localhost:8502 now! 🚀
