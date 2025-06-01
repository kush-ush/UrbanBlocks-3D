import streamlit as st
import pandas as pd
from zoning_engine import run_zoning_ga, evaluate_layout
from utils import generate_plot_map, zoning_summary, plotly_3d_map

st.set_page_config(page_title="UrbanBlocks 3D", layout="wide")

st.title("🏙️ UrbanBlocks 3D – AI-Powered Zoning Simulator")

if "df" not in st.session_state:
    st.session_state.df = None

if "grid_size" not in st.session_state:
    st.session_state.grid_size = 10

# --- SIDEBAR SETTINGS ---
st.sidebar.title("⚙️ Configure Layout")

grid_size = st.sidebar.selectbox("Grid Size (NxN)", [6, 8, 10, 12], index=2)
total_plots = grid_size * grid_size
area_mode = st.sidebar.radio("Area Input", ["Random", "Manual"])
if area_mode == "Random":
    min_area = st.sidebar.slider("Min Area", 50, 300, 80)
    max_area = st.sidebar.slider("Max Area", 100, 600, 150)
    manual_areas = None
else:
    st.sidebar.markdown("Enter area manually (for all plots):")
    manual_areas = [st.sidebar.number_input(f"Plot {i+1}", 50, 1000, 100, key=f"a{i}") for i in range(total_plots)]
    min_area = max_area = 0

st.sidebar.markdown("---")
res_range = st.sidebar.slider("🏠 Residential %", 0, 100, (40, 60))
com_range = st.sidebar.slider("🏢 Commercial %", 0, 100, (20, 30))
green_range = st.sidebar.slider("🌳 Green %", 0, 100, (10, 20))

if st.sidebar.button("🚀 Run AI Zoning"):
    with st.spinner("Generating layout using Genetic Algorithm..."):
        df, fig = run_zoning_ga(grid_size, min_area, max_area, res_range, com_range, green_range, manual_areas)
        st.session_state.df = df
        st.session_state.grid_size = grid_size
        df.to_csv("output/zoning_result.csv", index=False)
        st.success("✅ Layout generated successfully!")

# --- MAIN TABS ---
tabs = st.tabs(["🧱 View Layout", "📝 Edit Zone", "📈 Insights", "📊 Summary", "ℹ️ About"])

with tabs[0]:
    st.header("🧱 Zoning Layout (2D & 3D)")
    if st.session_state.df is not None:
        st.pyplot(generate_plot_map(st.session_state.df, st.session_state.grid_size))
        st.plotly_chart(plotly_3d_map(st.session_state.df), use_container_width=True)
    else:
        st.warning("⚠️ Please generate a layout first.")

with tabs[1]:
    st.header("📝 Manual Edit (Override Zone)")
    if st.session_state.df is not None:
        df = st.session_state.df.copy()
        selected_plot = st.selectbox("Choose Plot ID", df["PlotID"])
        current_zone = df[df["PlotID"] == selected_plot]["Zone"].values[0]
        current_subtype = df[df["PlotID"] == selected_plot]["Subtype"].values[0]

        new_zone = st.selectbox("New Zone", ["Residential", "Commercial", "Green", "Road"], index=["Residential", "Commercial", "Green", "Road"].index(current_zone))
        new_subtype = st.text_input("Subtype (e.g. Mall, Hospital)", value=current_subtype)

        if st.button("💾 Apply Edit"):
            st.session_state.df.loc[st.session_state.df["PlotID"] == selected_plot, ["Zone", "Subtype"]] = [new_zone, new_subtype]
            st.success(f"✅ Plot {selected_plot} updated.")
    else:
        st.warning("⚠️ Generate a layout first.")

with tabs[2]:
    st.header("📈 Layout Insights")
    if st.session_state.df is not None:
        score, reasons, suggestions = evaluate_layout(st.session_state.df)
        st.metric("🧠 Layout Score", f"{score} / 100")

        st.subheader("✅ Justifications")
        for r in reasons:
            st.markdown(f"- {r}")

        st.subheader("💡 Suggestions for Improvement")
        for s in suggestions:
            st.markdown(f"- {s}")
    else:
        st.warning("⚠️ Generate a layout first.")

with tabs[3]:
    st.header("📊 Zoning Summary Table")
    if st.session_state.df is not None:
        st.dataframe(zoning_summary(st.session_state.df))
    else:
        st.warning("⚠️ Generate a layout first.")

with tabs[4]:
    st.header("ℹ️ About UrbanBlocks")
    st.markdown("""
UrbanBlocks 3D is an AIML-powered city zoning engine built using Genetic Algorithms,  
explainable AI logic, and semantic zone assignment. It supports user edits, layout scoring,  
and interactive visual feedback to design smarter, sustainable city layouts.

**Key Features:**
- Semantic zones like 🏬 malls, 🏥 hospitals, 🌳 parks  
- Explainable decisions for every plot  
- Editable layout (human-in-the-loop)  
- Layout quality scoring + suggestions  
- 2D + 3D interactive visualization  

Built by **Kushal S Gowda** for AIML Lab & International Journal Publication (IEEE/Springer).
""")
