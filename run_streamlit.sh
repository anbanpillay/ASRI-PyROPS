#!/bin/bash
# Streamlit App Launcher for RocketPy Simulator

echo "════════════════════════════════════════════════════════════════"
echo "🚀 RocketPy Streamlit Interface"
echo "════════════════════════════════════════════════════════════════"
echo ""
echo "Starting Streamlit web application..."
echo ""

# Activate virtual environment
source .venv/bin/activate

# Run Streamlit
streamlit run rocketpy_migration/src/streamlit_app.py \
    --server.port 8502 \
    --server.headless true \
    --browser.gatherUsageStats false
