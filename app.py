import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import joblib
import time
from datetime import datetime
<<<<<<< HEAD
import os
import joblib
import gdown
=======

import os
import joblib
>>>>>>> 903456d (my changes)
# -----------------------------
# PAGE CONFIG
# -----------------------------

st.set_page_config(
    page_title="GridPulse · National Load Forecasting",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# -----------------------------
# CUSTOM CSS — Industrial Precision Theme
# Monospace + amber on deep charcoal, CRT-inspired grid lines
# -----------------------------
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@300;400;600;700&family=IBM+Plex+Sans:wght@300;400;600&display=swap');

/* ── GLOBAL RESET ── */
*, *::before, *::after { box-sizing: border-box; }

html, body, [class*="css"] {
    font-family: 'IBM Plex Sans', sans-serif;
    background-color: #0b0c0f;
    color: #d4d8e0;
}

/* ── SIDEBAR ── */
[data-testid="stSidebar"] {
    background: #0d0e12;
    border-right: 1px solid #1e2030;
}
section[data-testid="stSidebar"] button {
    width: 100%;
    text-align: left;
    padding: 10px 12px;
    border-radius: 8px;
    background: transparent;
    border: none;
    color: #cfd6e6;
    font-size: 14px;
    transition: 0.2s;
}

section[data-testid="stSidebar"] button:hover {
    background-color: #1e2030;
}

section[data-testid="stSidebar"] button[kind="secondary"] {
    background-color: #2a2d3e;
    color: #3de8a0;
}

[data-testid="stSidebar"] .block-container {
    padding: 2rem 1.2rem;
}

/* ── HIDE STREAMLIT BRANDING ── */
#MainMenu, footer, header { visibility: hidden; }

/* ── MAIN CONTENT PADDING ── */
.block-container {
    padding: 2rem 2.5rem 4rem;
    max-width: 1400px;
}

/* ── PAGE HEADER ── */
.gp-header {
    display: flex;
    align-items: flex-end;
    gap: 1rem;
    padding-bottom: 1.2rem;
    border-bottom: 1px solid #1e2030;
    margin-bottom: 2rem;
}
.gp-logo {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 1.9rem;
    font-weight: 700;
    color: #f5a623;
    letter-spacing: -0.04em;
    line-height: 1;
}
.gp-logo span { color: #ffffff; }
.gp-subtitle {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.72rem;
    color: #5a6070;
    text-transform: uppercase;
    letter-spacing: 0.15em;
    margin-bottom: 0.2rem;
}
.gp-live-badge {
    margin-left: auto;
    display: flex;
    align-items: center;
    gap: 0.4rem;
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.7rem;
    color: #3de8a0;
    text-transform: uppercase;
    letter-spacing: 0.1em;
}
.gp-live-dot {
    width: 7px; height: 7px;
    border-radius: 50%;
    background: #3de8a0;
    animation: pulse 1.8s infinite;
}
@keyframes pulse {
    0%, 100% { opacity: 1; }
    50% { opacity: 0.3; }
}

/* ── METRIC CARDS ── */
.metric-row { display: flex; gap: 1rem; margin-bottom: 2rem; flex-wrap: wrap; }
.metric-card {
    flex: 1;
    min-width: 160px;
    background: #111318;
    border: 1px solid #1e2030;
    border-top: 2px solid #f5a623;
    padding: 1.2rem 1.4rem;
    position: relative;
    overflow: hidden;
}
.metric-card::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0; bottom: 0;
    background: repeating-linear-gradient(
        0deg,
        transparent,
        transparent 24px,
        rgba(255,255,255,0.012) 24px,
        rgba(255,255,255,0.012) 25px
    );
    pointer-events: none;
}
.metric-card.best { border-top-color: #3de8a0; }
.metric-card.warn { border-top-color: #e87e3d; }

.metric-label {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.65rem;
    color: #5a6070;
    text-transform: uppercase;
    letter-spacing: 0.12em;
    margin-bottom: 0.5rem;
}
.metric-value {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 1.65rem;
    font-weight: 700;
    color: #f5a623;
    line-height: 1;
}
.metric-card.best .metric-value { color: #3de8a0; }
.metric-unit {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.7rem;
    color: #5a6070;
    margin-top: 0.3rem;
}

/* ── SECTION HEADERS ── */
.section-header {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.7rem;
    text-transform: uppercase;
    letter-spacing: 0.2em;
    color: #5a6070;
    padding: 0.4rem 0;
    border-bottom: 1px solid #1e2030;
    margin: 2rem 0 1.2rem;
}
.section-header span {
    color: #f5a623;
    margin-right: 0.5rem;
}

/* ── PREDICTION OUTPUT ── */
.prediction-block {
    background: #0d0e12;
    border: 1px solid #1e2030;
    border-left: 3px solid #3de8a0;
    padding: 1.8rem 2rem;
    margin-top: 1.5rem;
    position: relative;
}
.prediction-block::after {
    content: 'FORECAST OUTPUT';
    position: absolute;
    top: -9px; left: 1.5rem;
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.6rem;
    color: #3de8a0;
    background: #0d0e12;
    padding: 0 0.5rem;
    letter-spacing: 0.15em;
}
.pred-label {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.68rem;
    color: #5a6070;
    text-transform: uppercase;
    letter-spacing: 0.12em;
    margin-bottom: 0.6rem;
}
.pred-value {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 3rem;
    font-weight: 700;
    color: #3de8a0;
    line-height: 1;
}
.pred-unit {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.85rem;
    color: #5a6070;
    margin-top: 0.4rem;
}
.pred-model-tag {
    display: inline-block;
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.65rem;
    color: #f5a623;
    border: 1px solid #f5a623;
    padding: 0.15rem 0.5rem;
    margin-top: 0.8rem;
    letter-spacing: 0.1em;
}

/* ── SIDEBAR NAV ── */
.nav-label {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.6rem;
    color: #3a4050;
    text-transform: uppercase;
    letter-spacing: 0.2em;
    margin-bottom: 0.8rem;
    padding-bottom: 0.4rem;
    border-bottom: 1px solid #1a1c24;
}
.sidebar-wordmark {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 1.1rem;
    font-weight: 700;
    color: #f5a623;
    margin-bottom: 0.3rem;
}
.sidebar-tagline {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.6rem;
    color: #3a4050;
    margin-bottom: 2rem;
    letter-spacing: 0.08em;
}

/* ── TABLES ── */
[data-testid="stDataFrame"] table {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.8rem;
}

/* ── SLIDERS & INPUTS ── */
[data-testid="stSlider"] label,
[data-testid="stNumberInput"] label {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.72rem;
    color: #8090a8;
    text-transform: uppercase;
    letter-spacing: 0.08em;
}

/* ── ALERT BOXES ── */
.stSuccess, .stWarning, .stInfo {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.8rem;
}

/* ── RADIO BUTTON LABELS ── */
[data-testid="stRadio"] label {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.8rem;
}

/* ── STATUS STRIP ── */
.status-strip {
    display: flex;
    gap: 1.5rem;
    padding: 0.6rem 1rem;
    background: #0d0e12;
    border: 1px solid #1e2030;
    margin-bottom: 1.5rem;
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.68rem;
    color: #5a6070;
    flex-wrap: wrap;
}
.status-item { display: flex; align-items: center; gap: 0.4rem; }
.status-ok { color: #3de8a0; }
.status-warn { color: #f5a623; }

/* ── REGION MAP CARD ── */
.region-grid {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 0.8rem;
    margin-top: 0.5rem;
}
.region-cell {
    background: #111318;
    border: 1px solid #1e2030;
    padding: 0.9rem 1rem;
}
.region-name {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.62rem;
    color: #5a6070;
    text-transform: uppercase;
    letter-spacing: 0.1em;
    margin-bottom: 0.3rem;
}
.region-val {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 1.1rem;
    font-weight: 600;
    color: #d4d8e0;
}

/* ── PLOTLY TWEAKS ── */
.js-plotly-plot .plotly .modebar { background: transparent !important; }
</style>
""", unsafe_allow_html=True)

# -----------------------------
# LOAD DATA & MODELS
# -----------------------------
@st.cache_data
def load_data():
    return pd.read_csv("model_results.csv")

@st.cache_data
def load_raw_data():
    """Load and preprocess the raw Excel data for display."""
    df = pd.read_excel("hourlyLoadDataIndia.xlsx")
    # Convert datetime columns to strings to avoid PyArrow serialization errors
    for col in df.columns:
        if pd.api.types.is_datetime64_any_dtype(df[col]):
            df[col] = df[col].astype(str)
    return df

@st.cache_resource
def load_models():
    # Google Drive File IDs provided by the user
    drive_files = {
        "Linear_Regression.pkl": "1qkIxenIIvkENGQPg2LgV-tLA0ImLh0kk",
        "Random_Forest.pkl": "12QsWc4kRQ_hC9pBKcgb2VuiIVMYKfq9o",
        "XGBoost.pkl": "1Rt5f5l9u7xWqTtLVI88GU2g7aJZo0LZK"
    }

    # Download models from Google Drive if they don't exist
    for filename, file_id in drive_files.items():
        if not os.path.exists(filename):
            url = f'https://drive.google.com/uc?id={file_id}'
            print(f"Downloading {filename} from Google Drive...")
            try:
                gdown.download(url, filename, quiet=False)
            except Exception as e:
                st.error(f"Failed to download {filename} from Google Drive. Ensure the link is set to 'Anyone with the link'. Error: {e}")

    lr  = joblib.load("Linear_Regression.pkl")
    rf  = joblib.load("Random_Forest.pkl")
    xgb = joblib.load("XGBoost.pkl")
    return lr, rf, xgb

model_df = load_data()
lr_model, rf_model, xgb_model = load_models()

MODEL_MAP = {
    "Linear Regression": lr_model,
    "Random Forest":     rf_model,
    "XGBoost":           xgb_model,
}

def get_best_model_row(df):
    return df.loc[df["MAE"].idxmin()]

best_row        = get_best_model_row(model_df)
best_model_name = best_row["Model"]
best_model      = MODEL_MAP.get(best_model_name, lr_model)

# ── Plotly base theme ──────────────────────────────────────────────────────
PLOTLY_LAYOUT = dict(
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(13,14,18,0.9)",
    font=dict(family="IBM Plex Mono, monospace", color="#8090a8", size=11),
    margin=dict(l=10, r=10, t=40, b=10),
    colorway=["#f5a623", "#3de8a0", "#e87e3d", "#5ab8f5", "#c97ef5"],
    xaxis=dict(
        gridcolor="#1e2030", gridwidth=1,
        zeroline=False,
        tickfont=dict(family="IBM Plex Mono, monospace", size=10),
    ),
    yaxis=dict(
        gridcolor="#1e2030", gridwidth=1,
        zeroline=False,
        tickfont=dict(family="IBM Plex Mono, monospace", size=10),
    ),
)

# -----------------------------
# SIDEBAR
# -----------------------------

with st.sidebar:
    

    st.markdown('<div class="sidebar-wordmark">⚡ GRIDPULSE</div>', unsafe_allow_html=True)
    st.markdown('<div class="sidebar-tagline">National Load Forecasting System</div>', unsafe_allow_html=True)

    st.markdown('<div class="nav-label">MODEL ANALYTICS</div>', unsafe_allow_html=True)

    if "page" not in st.session_state:
        st.session_state.page = "Overview"
   
    # Navigation buttons
    if st.button("🏠 Overview"):
        st.session_state.page = "Overview"

    if st.button("📊 Model Comparison"):
        st.session_state.page = "Model Comparison"

    if st.button("🎯 Feature Importance"):
        st.session_state.page = "Feature Importance"

    if st.button("📝 Predictions"):
        st.session_state.page = "Predictions"

    if st.button("📁 Dataset Info"):
        st.session_state.page = "Dataset Info"
    

    page = st.session_state.page

    st.markdown("---")
    now = datetime.now()
    st.markdown(f"""
    <div style="font-family:'IBM Plex Mono',monospace; font-size:0.65rem; color:#3a4050; line-height:1.8;">
        <div style="color:#5a6070;">System Time</div>
        <div style="color:#f5a623;">{now.strftime('%Y-%m-%d')}</div>
        <div style="color:#f5a623;">{now.strftime('%H:%M:%S')} IST</div>
        <br>
        <div style="color:#5a6070;">Active Model</div>
        <div style="color:#3de8a0;">{best_model_name}</div>
        <br>
        <div style="color:#5a6070;">Status</div>
        <div style="color:#3de8a0;">● ONLINE</div>
    </div>
    """, unsafe_allow_html=True)
    

# ── Page Header (shared) ──────────────────────────────────────────────────
st.markdown(f"""
<div class="gp-header">
    <div>
        <div class="gp-logo">GRID<span>PULSE</span></div>
        <div class="gp-subtitle">National Electricity Load Forecasting · India</div>
    </div>
    <div class="gp-live-badge">
        <div class="gp-live-dot"></div>
        Live Session
    </div>
</div>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────────────────────
# PAGE: OVERVIEW
# ─────────────────────────────────────────────────────────────────────────────
if page == "Overview":

    # Status strip
    st.markdown(f"""
    <div class="status-strip">
        <div class="status-item"><span class="status-ok">■</span> FORECAST ENGINE READY</div>
        <div class="status-item"><span class="status-ok">■</span> MODELS LOADED: 3</div>
        <div class="status-item"><span class="status-warn">■</span> BEST MODEL: {best_model_name.upper()}</div>
        <div class="status-item"><span>■</span> REGIONS: 5 + NATIONAL</div>
    </div>
    """, unsafe_allow_html=True)

    # KPI Row
    r2_pct   = round(float(best_row["R2"]) * 100, 2)
    mae_val  = round(float(best_row["MAE"]), 1)
    rmse_val = round(float(best_row["RMSE"]), 1)
    mape_val = round(float(best_row["MAPE"]), 2)

    st.markdown(f"""
    <div class="metric-row">
        <div class="metric-card best">
            <div class="metric-label">Best Model</div>
            <div class="metric-value" style="font-size:1.2rem; color:#3de8a0;">{best_model_name}</div>
            <div class="metric-unit">Selected by lowest MAE</div>
        </div>
        <div class="metric-card best">
            <div class="metric-label">R² Score</div>
            <div class="metric-value">{r2_pct}%</div>
            <div class="metric-unit">Variance explained</div>
        </div>
        <div class="metric-card">
            <div class="metric-label">MAE</div>
            <div class="metric-value">{mae_val}</div>
            <div class="metric-unit">MW · Mean Abs. Error</div>
        </div>
        <div class="metric-card">
            <div class="metric-label">RMSE</div>
            <div class="metric-value">{rmse_val}</div>
            <div class="metric-unit">MW · Root Mean Sq.</div>
        </div>
        <div class="metric-card warn">
            <div class="metric-label">MAPE</div>
            <div class="metric-value">{mape_val}%</div>
            <div class="metric-unit">Mean Abs. % Error</div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    

    # Generate predictions from all models for 24-hour profile
    np.random.seed(42)
    hours = list(range(24))
    
    # Base load curve (actual)
    base = [115000, 108000, 103000, 100000, 99000, 102000,
            112000, 128000, 142000, 155000, 160000, 162000,
            158000, 155000, 152000, 150000, 153000, 160000,
            168000, 172000, 170000, 162000, 148000, 130000]
    noise = np.random.normal(0, 1500, 24)
    actual_load = [b + n for b, n in zip(base, noise)]
    
    # Get predictions from each model
    model_predictions = {}
    for model_name, model in MODEL_MAP.items():
        preds = []
        for h in hours:
            # Create input for this hour (using previous hour's load as prev_load)
            prev_load_val = base[h-1] if h > 0 else base[0]
            input_df = pd.DataFrame([{
                "north": 32000,
                "west": 45000,
                "east": 28000,
                "south": 38000,
                "north_east": 12000,
                "hour": h,
                "day": 15,
                "month": 4,
                "day_of_week": 1,
                "prev_load": prev_load_val,
            }])
            pred = model.predict(input_df)[0]
            preds.append(pred)
        model_predictions[model_name] = preds

    fig = go.Figure()
    
    # Actual load
    fig.add_trace(go.Scatter(
        x=hours, y=actual_load,
        mode="lines", name="Actual Load",
        line=dict(color="#f5a623", width=2),
        fill="tozeroy", fillcolor="rgba(245,166,35,0.06)"
    ))
    
    # Model predictions
    colors = {"Linear Regression": "#3de8a0", "Random Forest": "#5ab8f5", "XGBoost": "#e87e3d"}
    dashes = {"Linear Regression": "dot", "Random Forest": "dash", "XGBoost": "longdash"}
    
    for model_name, preds in model_predictions.items():
        fig.add_trace(go.Scatter(
            x=hours, y=preds,
            mode="lines", name=model_name,
            line=dict(color=colors[model_name], width=2, dash=dashes[model_name]),
        ))
    
    fig.add_vline(
        x=datetime.now().hour,
        line=dict(color="#e87e3d", width=1, dash="dash"),
        annotation_text="NOW",
        annotation_font=dict(family="IBM Plex Mono, monospace", size=10, color="#e87e3d")
    )
    fig.update_layout(
        **PLOTLY_LAYOUT,
        height=320,
        xaxis_title="Hour of Day",
        yaxis_title="Load (MW)",
        legend=dict(
            font=dict(family="IBM Plex Mono, monospace", size=10),
            bgcolor="rgba(0,0,0,0)",
            x=0.01, y=0.99
        )
    )
    
    st.plotly_chart(fig, width='stretch')
    

    # Regional snapshot
    st.markdown('<div class="section-header"><span>//</span> REGIONAL LOAD SNAPSHOT (ILLUSTRATIVE)</div>', unsafe_allow_html=True)
    regions = {
        "North":      32000,
        "West":       45000,
        "East":       28000,
        "South":      38000,
        "North-East": 12000,
    }
    cols = st.columns(len(regions))
    for col, (region, val) in zip(cols, regions.items()):
        share = round(val / sum(regions.values()) * 100, 1)
        col.markdown(f"""
        <div class="region-cell">
            <div class="region-name">{region}</div>
            <div class="region-val">{val:,} MW</div>
            <div style="font-family:'IBM Plex Mono',monospace; font-size:0.62rem; color:#5a6070; margin-top:0.2rem;">{share}% of national</div>
        </div>
        """, unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────────────────────
# PAGE: MODEL COMPARISON
# ─────────────────────────────────────────────────────────────────────────────
elif page == "Model Comparison":

    st.markdown('<div class="section-header"><span>//</span> PERFORMANCE BENCHMARKS — ALL MODELS</div>', unsafe_allow_html=True)

    # Table
    styled_df = model_df.style\
        .highlight_min(subset=["MAE","RMSE","MAPE"], color="#0d2a1e", props="color:#3de8a0; font-weight:600;")\
        .highlight_max(subset=["R2"],                color="#0d2a1e", props="color:#3de8a0; font-weight:600;")\
        .set_properties(**{"font-family": "IBM Plex Mono, monospace", "font-size": "0.8rem"})
    st.dataframe(styled_df, width='stretch', height=160)

    col_a, col_b = st.columns(2)

    with col_a:
        st.markdown('<div class="section-header"><span>//</span> MAE BY MODEL</div>', unsafe_allow_html=True)
        fig_mae = px.bar(
            model_df, x="Model", y="MAE", color="Model",
            color_discrete_sequence=["#f5a623", "#3de8a0", "#e87e3d"],
            title=""
        )
        fig_mae.update_traces(marker_line_width=0)
        fig_mae.update_layout(**PLOTLY_LAYOUT, height=280, showlegend=False)
        st.plotly_chart(fig_mae, width='stretch')

    with col_b:
        st.markdown('<div class="section-header"><span>//</span> R² SCORE BY MODEL</div>', unsafe_allow_html=True)
        fig_r2 = px.bar(
            model_df, x="Model", y="R2", color="Model",
            color_discrete_sequence=["#f5a623", "#3de8a0", "#e87e3d"],
            title=""
        )
        fig_r2.update_traces(marker_line_width=0)
        fig_r2.update_layout(**PLOTLY_LAYOUT, height=280, showlegend=False)
        st.plotly_chart(fig_r2, width='stretch')

    col_c, col_d = st.columns(2)

    with col_c:
        st.markdown('<div class="section-header"><span>//</span> RMSE COMPARISON</div>', unsafe_allow_html=True)
        fig_rmse = go.Figure(go.Bar(
            x=model_df["Model"], y=model_df["RMSE"],
            marker=dict(color=["#f5a623", "#3de8a0", "#e87e3d"], line=dict(width=0)),
        ))
        fig_rmse.update_layout(**PLOTLY_LAYOUT, height=240)
        st.plotly_chart(fig_rmse, width='stretch')

    with col_d:
        st.markdown('<div class="section-header"><span>//</span> MAPE COMPARISON</div>', unsafe_allow_html=True)
        fig_mape = go.Figure(go.Bar(
            x=model_df["Model"], y=model_df["MAPE"],
            marker=dict(color=["#f5a623", "#3de8a0", "#e87e3d"], line=dict(width=0)),
        ))
        fig_mape.update_layout(**PLOTLY_LAYOUT, height=240)
        st.plotly_chart(fig_mape, width='stretch')

    # Radar chart
    st.markdown('<div class="section-header"><span>//</span> MULTI-METRIC RADAR</div>', unsafe_allow_html=True)

    metrics_cols = ["MAE", "RMSE", "MAPE"]
    df_norm = model_df.copy()
    for c in metrics_cols:
        df_norm[c + "_norm"] = 1 - (df_norm[c] - df_norm[c].min()) / (df_norm[c].max() - df_norm[c].min() + 1e-9)
    df_norm["R2_norm"] = (df_norm["R2"] - df_norm["R2"].min()) / (df_norm["R2"].max() - df_norm["R2"].min() + 1e-9)

    radar_cats  = ["R² ↑", "MAE ↓ (inv)", "RMSE ↓ (inv)", "MAPE ↓ (inv)"]
    colors_rad  = ["#f5a623", "#3de8a0", "#e87e3d"]

    fig_rad = go.Figure()
    for i, row in df_norm.iterrows():
        vals = [row["R2_norm"], row["MAE_norm"], row["RMSE_norm"], row["MAPE_norm"]]
        vals += vals[:1]
        fig_rad.add_trace(go.Scatterpolar(
            r=vals,
            theta=radar_cats + [radar_cats[0]],
            fill="toself",
            name=row["Model"],
            line=dict(color=colors_rad[i % 3], width=2),
            fillcolor=f"rgba{tuple(int(colors_rad[i%3].lstrip('#')[j:j+2],16) for j in (0,2,4))+(0.07,)}"
        ))
    fig_rad.update_layout(
        **{k: v for k, v in PLOTLY_LAYOUT.items() if k not in ["xaxis","yaxis"]},
        polar=dict(
            bgcolor="rgba(0,0,0,0)",
            radialaxis=dict(visible=True, range=[0,1], gridcolor="#1e2030", tickfont=dict(size=9)),
            angularaxis=dict(gridcolor="#1e2030", tickfont=dict(family="IBM Plex Mono, monospace", size=10, color="#8090a8")),
        ),
        height=360,
        legend=dict(font=dict(family="IBM Plex Mono, monospace", size=10), bgcolor="rgba(0,0,0,0)"),
        title=dict(text="", font=dict(size=1))
    )
    st.plotly_chart(fig_rad, width='stretch')


# ─────────────────────────────────────────────────────────────────────────────
# PAGE: FEATURE IMPORTANCE
# ─────────────────────────────────────────────────────────────────────────────
elif page == "Feature Importance":

    st.markdown('<div class="section-header"><span>//</span> FEATURE IMPORTANCE ANALYSIS</div>', unsafe_allow_html=True)

    if best_model_name in ["Random Forest", "XGBoost"]:
        importance = best_model.feature_importances_
        features   = list(best_model.feature_names_in_)

        df_feat = pd.DataFrame({
            "Feature":    features,
            "Importance": importance
        }).sort_values("Importance", ascending=True)

        df_feat["Pct"] = (df_feat["Importance"] / df_feat["Importance"].sum() * 100).round(2)

        # Horizontal bar
        fig_imp = go.Figure(go.Bar(
            x=df_feat["Importance"],
            y=df_feat["Feature"],
            orientation="h",
            marker=dict(
                color=df_feat["Importance"],
                colorscale=[[0, "#1e2030"], [0.5, "#f5a623"], [1, "#3de8a0"]],
                line=dict(width=0)
            ),
            text=[f"{v:.3f}" for v in df_feat["Importance"]],
            textposition="outside",
            textfont=dict(family="IBM Plex Mono, monospace", size=10, color="#8090a8"),
        ))
        fig_imp.update_layout(
            **PLOTLY_LAYOUT,
            height=max(320, len(features) * 42),
            xaxis_title="Importance Score",
            yaxis=dict(
                **PLOTLY_LAYOUT["yaxis"],
                tickfont=dict(family="IBM Plex Mono, monospace", size=11, color="#d4d8e0"),
            ),
        )
        st.plotly_chart(fig_imp, width='stretch')

        # Table
        st.markdown('<div class="section-header"><span>//</span> FEATURE IMPORTANCE TABLE</div>', unsafe_allow_html=True)
        df_disp = df_feat[["Feature","Importance","Pct"]].sort_values("Importance", ascending=False)
        df_disp.columns = ["Feature", "Score", "% Contribution"]
        st.dataframe(
            df_disp.style.bar(subset=["% Contribution"], color="#f5a623")
                         .format({"Score": "{:.5f}", "% Contribution": "{:.2f}%"})
                         .set_properties(**{"font-family":"IBM Plex Mono, monospace","font-size":"0.8rem"}),
            width='stretch'
        )

    else:
        # Linear Regression coefficients (mock if no coef available)
        st.warning("⚠  Feature importance plots are available for tree-based models (Random Forest / XGBoost). Linear Regression uses coefficient magnitudes instead.")
        try:
            coef   = best_model.coef_
            feats  = best_model.feature_names_in_
            df_coef = pd.DataFrame({"Feature": feats, "Coefficient": coef})
            df_coef["Abs"] = df_coef["Coefficient"].abs()
            df_coef = df_coef.sort_values("Abs", ascending=True)

            colors = ["#3de8a0" if c > 0 else "#e87e3d" for c in df_coef["Coefficient"]]
            fig_coef = go.Figure(go.Bar(
                x=df_coef["Coefficient"], y=df_coef["Feature"],
                orientation="h",
                marker=dict(color=colors, line=dict(width=0)),
            ))
            fig_coef.update_layout(**PLOTLY_LAYOUT, height=320, xaxis_title="Coefficient Value")
            st.plotly_chart(fig_coef, width='stretch')
        except Exception:
            st.info("Coefficient data unavailable for this model.")

# ─────────────────────────────────────────────────────────────────────────────
# PAGE: PREDICTIONS
# ─────────────────────────────────────────────────────────────────────────────
elif page == "Predictions":

    st.markdown('<div class="section-header"><span>//</span> MODEL SELECTION</div>', unsafe_allow_html=True)
    
    # Model selection tabs
    model_options = list(MODEL_MAP.keys())
    selected_model_name = st.radio(
        "Select Model for Prediction:",
        model_options,
        index=model_options.index(best_model_name),
        horizontal=True,
        label_visibility="collapsed"
    )
    selected_model = MODEL_MAP[selected_model_name]
    
    # Get metrics for selected model
    selected_row = model_df[model_df["Model"] == selected_model_name].iloc[0]
    
    st.markdown(f"""
    <div style="display:flex; gap:1.5rem; margin-bottom:1.5rem; padding:0.8rem 1rem; background:#111318; border:1px solid #1e2030; border-left:3px solid #f5a623;">
        <div style="font-family:'IBM Plex Mono',monospace; font-size:0.7rem; color:#5a6070;">SELECTED MODEL</div>
        <div style="font-family:'IBM Plex Mono',monospace; font-size:0.9rem; color:#f5a623; font-weight:600;">{selected_model_name}</div>
        <div style="font-family:'IBM Plex Mono',monospace; font-size:0.7rem; color:#3de8a0; margin-left:auto;">MAE: {round(selected_row['MAE'],1)} · R²: {round(selected_row['R2'],3)}</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="section-header"><span>//</span> INPUT PARAMETERS — TEMPORAL & REGIONAL</div>', unsafe_allow_html=True)

    col1, col2 = st.columns([1, 1], gap="large")

    with col1:
        st.markdown("**⏱ Temporal Inputs**")
        hour        = st.slider("Hour of Day (0–23)",         0, 23, datetime.now().hour)
        day         = st.slider("Day of Month (1–31)",         1, 31, datetime.now().day)
        month       = st.slider("Month (1–12)",                1, 12, datetime.now().month)
        day_of_week = st.slider("Day of Week  (0 = Monday)",  0,  6, datetime.now().weekday())

    with col2:
        st.markdown("**🗺 Regional Load Inputs (MW)**")
        prev_load = st.number_input("Previous National Load (MW)", value=155000, step=1000)
        north     = st.number_input("North Region (MW)",           value=32000,  step=500)
        west      = st.number_input("West Region (MW)",            value=45000,  step=500)
        east      = st.number_input("East Region (MW)",            value=28000,  step=500)
        south     = st.number_input("South Region (MW)",           value=38000,  step=500)
        north_east= st.number_input("North-East Region (MW)",      value=12000,  step=500)

    # ── Forecast ──────────────────────────────────────────────────────────
    input_df = pd.DataFrame([{
        "north":      north,
        "west":       west,
        "east":       east,
        "south":      south,
        "north_east": north_east,
        "hour":       hour,
        "day":        day,
        "month":      month,
        "day_of_week":day_of_week,
        "prev_load":  prev_load,
    }])

    prediction = selected_model.predict(input_df)[0]
    regional_sum = north + west + east + south + north_east
    deviation = round((prediction - prev_load) / prev_load * 100, 2)
    dev_sign  = "▲" if deviation >= 0 else "▼"
    dev_color = "#3de8a0" if deviation >= 0 else "#e87e3d"

    st.markdown(f"""
    <div class="prediction-block">
        <div class="pred-label">Predicted National Load</div>
        <div class="pred-value">{round(prediction/1000, 2)} GW</div>
        <div class="pred-unit">{round(prediction):,} MW</div>
        <div class="pred-model-tag">MODEL: {selected_model_name.upper()}</div>
        <div style="margin-top:1rem; font-family:'IBM Plex Mono',monospace; font-size:0.72rem; color:#5a6070;">
            Period: {['Mon','Tue','Wed','Thu','Fri','Sat','Sun'][day_of_week]} &nbsp;|&nbsp;
            Hour: {hour:02d}:00 &nbsp;|&nbsp;
            Month: {month:02d} &nbsp;|&nbsp;
            Δ vs prev: <span style="color:{dev_color};">{dev_sign} {abs(deviation)}%</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Regional contribution donut
    st.markdown('<div class="section-header"><span>//</span> REGIONAL CONTRIBUTION TO FORECAST INPUT</div>', unsafe_allow_html=True)

    col_donut, col_bar = st.columns([1, 1])

    region_data = pd.DataFrame({
        "Region":     ["North", "West", "East", "South", "North-East"],
        "Load (MW)":  [north,   west,   east,   south,   north_east],
    })

    with col_donut:
        fig_donut = go.Figure(go.Pie(
            labels=region_data["Region"],
            values=region_data["Load (MW)"],
            hole=0.6,
            marker=dict(
                colors=["#f5a623", "#3de8a0", "#5ab8f5", "#e87e3d", "#c97ef5"],
                line=dict(color="#0b0c0f", width=2)
            ),
            textinfo="label+percent",
            textfont=dict(family="IBM Plex Mono, monospace", size=10, color="#d4d8e0"),
        ))
        fig_donut.update_layout(
            **{k: v for k, v in PLOTLY_LAYOUT.items() if k not in ["xaxis","yaxis"]},
            height=300,
            showlegend=False,
            annotations=[dict(
                text=f"{regional_sum/1000:.1f} GW<br><span style='font-size:9px'>Regional Sum</span>",
                x=0.5, y=0.5, font_size=14, showarrow=False,
                font=dict(family="IBM Plex Mono, monospace", color="#d4d8e0")
            )]
        )
        st.plotly_chart(fig_donut, width='stretch')

    with col_bar:
        # Scale each region's bar to the selected model's prediction
        if regional_sum > 0:
            region_scaled = [prediction * (v / regional_sum) for v in region_data["Load (MW)"]]
        else:
            region_scaled = [0 for _ in region_data["Load (MW)"]]

        fig_rbar = go.Figure(go.Bar(
            x=region_scaled,
            y=region_data["Region"],
            orientation="h",
            marker=dict(
                color=["#f5a623", "#3de8a0", "#5ab8f5", "#e87e3d", "#c97ef5"],
                line=dict(width=0)
            ),
            text=[f"{v/1000:.1f} GW" for v in region_scaled],
            textposition="outside",
            textfont=dict(family="IBM Plex Mono, monospace", size=10, color="#8090a8")
        ))
        fig_rbar.update_layout(
            xaxis_title="Model-Scaled Regional Contribution (MW)",
        )
        st.plotly_chart(fig_rbar, width='stretch')

    # Sensitivity hint
    st.markdown('<div class="section-header"><span>//</span> DIAGNOSTIC</div>', unsafe_allow_html=True)
    col_d1, col_d2, col_d3 = st.columns(3)
    col_d1.metric("Regional Sum",    f"{regional_sum:,} MW",        f"{round(regional_sum/1000,2)} GW")
    col_d2.metric("Forecast Output", f"{round(prediction):,} MW",  f"{round(prediction/1000,2)} GW")
    col_d3.metric("Δ vs Previous",   f"{deviation:+.2f}%",          "▲ higher" if deviation >= 0 else "▼ lower")

# ─────────────────────────────────────────────────────────────────────────────
# PAGE: DATASET INFO
# ─────────────────────────────────────────────────────────────────────────────
elif page == "Dataset Info":
    st.markdown('<div class="section-header"><span>//</span> TRAINING DATASET: HOURLY LOAD DATA INDIA</div>', unsafe_allow_html=True)
    
    try:
        # Load the Excel file
        df = load_raw_data()
        
        # Basic info
        num_rows, num_cols = df.shape
        columns = list(df.columns)
        
        col_info1, col_info2, col_info3 = st.columns(3)
        col_info1.metric("Total Records", num_rows)
        col_info2.metric("Total Features", num_cols)
        col_info3.metric("Data Points", f"{num_rows:,}")
        
        # Column names with descriptions
        st.markdown("**📊 Columns in Dataset**")
        st.write(columns)
        
        # Sample preview
        st.markdown("**🔍 Sample Data Preview**")
        st.dataframe(df.head(10), width='stretch')
        
        # Data types
        st.markdown("**📋 Data Types**")
        st.dataframe(df.dtypes, width='stretch')
        
        # Statistical summary
        st.markdown("**📈 Statistical Summary**")
        st.dataframe(df.describe(), width='stretch')
        
        # Missing values
        st.markdown("**❌ Missing Values**")
        missing = df.isnull().sum()
        missing_df = pd.DataFrame({"Missing Count": missing, "Missing %": (missing/len(df)*100).round(2)})
        st.dataframe(missing_df, width='stretch')
        
    except Exception as e:
        st.error(f"Error loading dataset: {e}")