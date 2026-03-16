from __future__ import annotations

# --- Fix Python import path so FRAMEWORK package is found ---

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path.append(str(ROOT))

# --- Imports ---

import streamlit as st

from FRAMEWORK.ARCHY.stability_models.archy_system_model import (
    ArchySystemInput,
    analyze_archy_system,
)

from FRAMEWORK.ARCHY.environments.archy_environments import ENVIRONMENTS


# --- UI ---

st.title("ARCHY Design Explorer")

# Environment selection
env_name = st.selectbox("Environment", list(ENVIRONMENTS.keys()))
env = ENVIRONMENTS[env_name]

# Sidebar parameters
st.sidebar.header("Architecture Parameters")

mass = st.sidebar.slider("mass", 0.0, 1.0, 0.5)
medium = st.sidebar.slider("medium", 0.0, 1.0, 0.5)
geometry = st.sidebar.slider("geometry", 0.0, 1.0, 0.5)
location = st.sidebar.slider("location", 0.0, 1.0, 0.5)
layering = st.sidebar.slider("layering", 0.0, 1.0, 0.5)
orientation = st.sidebar.slider("orientation", 0.0, 1.0, 0.5)
urban_form = st.sidebar.slider("urban_form", 0.0, 1.0, 0.5)

st.sidebar.header("Interior Conditions")

inside_thermal = st.sidebar.slider("inside thermal", 0.0, 10.0, 5.0)
inside_acoustic = st.sidebar.slider("inside acoustic", 0.0, 2.0, 0.5)
inside_humidity = st.sidebar.slider("inside humidity", 0.0, 1.0, 0.5)

# --- Create ARCHY input model ---

input_model = ArchySystemInput(
    name="interactive",

    outside=env.outside,

    inside={
        "thermal": inside_thermal,
        "pressure": 0.3,
        "acoustic": inside_acoustic,
        "humidity": inside_humidity,
    },

    active_elements={
        "mass": mass,
        "medium": medium,
        "geometry": geometry,
        "location": location,
        "layering": layering,
        "orientation": orientation,
        "urban_form": urban_form,
    },

    base_orientation=0,
    architectural_delta=0.05,
    environmental_delta=0.02,
)

# --- Run analysis ---

result = analyze_archy_system(input_model)

# --- Output ---

st.header("ARCHY Results")

col1, col2 = st.columns(2)

with col1:
    st.metric("ARCHY Score", round(result.archy_score, 3))
    st.metric("Stability Index", round(result.stability.weighted_score, 3))

with col2:
    st.metric("Hybrid Coherence", round(result.coherence.hybrid_coherence, 3))
    st.metric("Orientation Drift", round(result.delta.drift_magnitude, 3))

st.subheader("Regime")
st.write(result.regime_label)

# Notes
if result.notes:
    st.subheader("Notes")
    for n in result.notes:
        st.write("-", n)
