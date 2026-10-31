#!/bin/bash
# Start Streamlit app on port 3000 to replace React frontend

cd /app
/root/.venv/bin/streamlit run streamlit_app.py \
    --server.port=3000 \
    --server.address=0.0.0.0 \
    --server.headless=true \
    --server.enableCORS=false \
    --server.enableXsrfProtection=false \
    --browser.gatherUsageStats=false
