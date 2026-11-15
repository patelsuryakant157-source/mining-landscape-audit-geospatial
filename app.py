import streamlit as st
import pandas as pd
import plotly.express as px
import os

st.set_page_config(
    page_title="Dhanpuri–Amlai Coalfield Ecological Audit",
    page_icon="🛰️",
    layout="wide"
)

# Header
st.title("🛰️ Dhanpuri–Amlai Coalfield: Spatiotemporal Ecological Audit (2001–2024)")
st.markdown(
    "**Study Area:** Sohagpur Coalfield, Shahdol District, Madhya Pradesh | "
    "**Sensors:** Landsat 7 ETM+ & Landsat 8 OLI | **Validation:** 88.33% Overall Accuracy (κ = 0.8444)"
)

# Top KPI Metrics
col1, col2, col3, col4 = st.columns(4)
col1.metric("Active Mining Area (2024)", "269.46 ha", "-86.0% vs 2001", delta_color="inverse")
col2.metric("Core Forest Canopy (2024)", "11,664.18 ha", "+406.5% vs 2001")
col3.metric("1 km Son River Buffer Mining", "86.51 ha", "-71.26% vs 2001", delta_color="inverse")
col4.metric("Classification Kappa (κ)", "0.8444", "88.33% Overall Acc.")

st.divider()

# Tabs for Navigation
tab1, tab2, tab3, tab4 = st.tabs([
    "🗺️ Spatial Maps",
    "📊 Landscape Fragmentation",
    "🌊 Son River Buffer Audit",
    "🎯 Accuracy & Methodology"
])

with tab1:
    st.subheader("Multi-Temporal Land Cover & Riparian Buffer Maps")
    c1, c2 = st.columns(2)
    with c1:
        if os.path.exists("figures/dhanpuri_calibrated_comparison.png"):
            st.image(
                "figures/dhanpuri_calibrated_comparison.png",
                caption="Figure 1: Calibrated 4-Class Landscape Grid (2001 Baseline vs. 2024 Extent)",
                use_container_width=True
            )
    with c2:
        if os.path.exists("figures/son_river_buffer_audit.png"):
            st.image(
                "figures/son_river_buffer_audit.png",
                caption="Figure 2: Concentric Riparian Buffers (1 km, 2 km, 5 km) along the Son River",
                use_container_width=True
            )

with tab2:
    st.subheader("FRAGSTATS / PyLandStats Structural Landscape Metrics")
    if os.path.exists("data/dhanpuri_fragmentation_audit.csv"):
        df_frag = pd.read_csv("data/dhanpuri_fragmentation_audit.csv")
        st.dataframe(df_frag, use_container_width=True)

        metric_choice = st.selectbox(
            "Select Landscape Metric to Visualize:",
            ["Area_ha", "Landscape_Pct", "Patch_Count", "Mean_Patch_Size_ha", "Edge_Density_m_per_ha"]
        )
        fig_frag = px.bar(
            df_frag,
            x="class_name",
            y=metric_choice,
            color=df_frag["Year"].astype(str),
            barmode="group",
            title=f"2001 vs. 2024 Comparison: {metric_choice}",
            labels={"color": "Year", "class_name": "Land Cover Class"}
        )
        st.plotly_chart(fig_frag, use_container_width=True)

with tab3:
    st.subheader("Son River Riparian Corridor Encroachment (1 km, 2 km, 5 km)")
    if os.path.exists("data/son_river_encroachment_audit.csv"):
        df_buf = pd.read_csv("data/son_river_encroachment_audit.csv")
        st.dataframe(df_buf, use_container_width=True)

        df_melt = df_buf.melt(
            id_vars="Buffer_Zone",
            value_vars=["Mining_Area_2001_ha", "Mining_Area_2024_ha"],
            var_name="Year",
            value_name="Mining_Area_ha"
        )
        fig_buf = px.bar(
            df_melt,
            x="Buffer_Zone",
            y="Mining_Area_ha",
            color="Year",
            barmode="group",
            title="Active Mining Footprint Inside Riparian Protection Zones"
        )
        st.plotly_chart(fig_buf, use_container_width=True)

with tab4:
    st.subheader("Stratified Confusion Matrix & Accuracy Metrics (N = 240)")
    c_left, c_right = st.columns(2)
    with c_left:
        if os.path.exists("data/dhanpuri_confusion_matrix.csv"):
            st.markdown("**Error Contingency Matrix**")
            df_cm = pd.read_csv("data/dhanpuri_confusion_matrix.csv", index_col=0)
            st.dataframe(df_cm, use_container_width=True)
    with c_right:
        if os.path.exists("data/dhanpuri_accuracy_metrics.csv"):
            st.markdown("**Class-Wise Producer's & User's Accuracy**")
            df_acc = pd.read_csv("data/dhanpuri_accuracy_metrics.csv")
            st.dataframe(df_acc, use_container_width=True)

    st.info(
        "**Spectral Calibration Note:** To prevent dry post-harvest fallow soil and river sand "
        "from being misclassified as coal pits in 2001, a Shortwave Infrared (SWIR < 0.20) and "
        "Visible Red (< 0.15) brightness filter was combined with NDVI and MNDWI."
    )