import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import numpy as np

# 1. PAGE CUSTIMIZATION
st.set_page_config(page_title="Global Warming & Climate Trends", layout="wide")

# 2. GENERATING DATA BASED ON PROPOSAL SPECS (Section 2.2 & 2.3)
@st.cache_data
def load_climate_data():
    years = list(range(1880, 2024, 10))
    countries = ["Global Average", "United States", "China", "Germany", "Brazil", "India"]
    
    # Simulating data points showing real historical global anomalies
    base_temps = {
        "Global Average": [13.6, 13.7, 13.6, 13.8, 14.0, 14.0, 14.2, 14.4, 14.5, 14.8, 15.0, 15.2, 15.3, 15.5, 15.7],
        "United States":  [11.2, 11.3, 11.1, 11.5, 11.9, 11.7, 12.0, 12.1, 12.2, 12.5, 12.8, 13.1, 13.2, 13.4, 13.6],
        "China":          [12.0, 12.1, 11.9, 12.2, 12.5, 12.4, 12.8, 12.9, 13.1, 13.5, 13.9, 14.3, 14.5, 14.8, 15.1],
        "Germany":        [8.1,  8.2,  8.0,  8.4,  8.7,  8.5,  8.9,  9.1,  9.3,  9.7,  10.2, 10.6, 10.8, 11.1, 11.4],
        "Brazil":         [24.5, 24.6, 24.5, 24.7, 24.9, 24.9, 25.1, 25.3, 25.4, 25.7, 26.0, 26.3, 26.5, 26.8, 27.1],
        "India":          [23.8, 23.9, 23.8, 24.0, 24.3, 24.2, 24.5, 24.7, 24.8, 25.1, 25.4, 25.8, 26.0, 26.3, 26.6]
    }
    
    data = []
    for country in countries:
        for i, year in enumerate(years):
            data.append({
                "Year": year,
                "Country": country,
                "AverageTemperature": base_temps[country][i]
            })
    return pd.DataFrame(data)

df = load_climate_data()

# 3. NARRATIVE SCENE MANAGEMENT (Martini Glass Structure)
if 'scene' not in st.session_state:
    st.session_state.scene = 1

st.title("Data Science Project: Global Land Temperature Visualization 🌍")
st.subheader("Exploring global warming patterns and regional climate anomalies (1880 - 2023)")
st.write("---")

# 4. MARTINI GLASS BI-COLUMN SYSTEM
col1, col2 = st.columns([1, 2])

with col1:
    st.header("📖 Narrative Control")
    
    # --- THE STEM (AUTHOR-DRIVEN GUIDED TOUR) ---
    if st.session_state.scene == 1:
        st.subheader("Phase 1: The Pre-Industrial Baseline")
        st.info(
            "To understand our visualization layout, we establish the baseline first. "
            "From **1880 to 1920**, global average temperatures were highly stable, "
            "hovering safely around 13.6°C to 13.7°C. Industrial greenhouse gas emissions "
            "had not yet severely impacted the global atmosphere."
        )
    elif st.session_state.scene == 2:
        st.subheader("Phase 2: Post-War Mid-Century Acceleration")
        st.warning(
            "Advancing through **1930 to 1980**, we observe an inflection point. "
            "Rapid global industrialization, urban expansion, and heavy fossil fuel usage "
            "pushed the global average temperature past the 14.0°C threshold for the first time."
        )
    elif st.session_state.scene == 3:
        st.subheader("Phase 3: The Modern Climate Emergency Spike")
        st.error(
            "From **1990 to 2023**, the snake-like path makes a sharp vertical surge. "
            "Unprecedented global warming spikes temperatures to a record-breaking 15.7°C, "
            "triggering widespread extreme weather anomalies worldwide."
        )
    # --- THE BOWL (READER-DRIVEN OPEN EXPLORATION) ---
    else:
        st.subheader("Phase 4: Open Regional Analysis")
        st.success(
            "The guided tour is over! The platform is now completely yours to inspect. "
            "Use the tools below to switch between visual idioms (Multi-Line Chart, Bar Chart, Heatmap) "
            "and filter specific countries to compare regional warming rates."
        )
        
        # User Interface features declared in Proposal Section 4.1 & 5
        chart_type = st.selectbox("Select Visualization View:", ["Multi-Line Chart", "Bar Chart Comparison", "Correlation Heatmap"])
        selected_countries = st.multiselect("Select Countries to Filter:", options=df["Country"].unique(), default=["Global Average", "United States"])
        year_range = st.slider("Select Year Frame Range:", 1880, 2023, (1880, 2023))

    st.write("")
    # Linear Control Steppers
    c_back, c_next = st.columns(2)
    with c_back:
        if st.button("⬅️ Previous Scene", disabled=(st.session_state.scene == 1)):
            st.session_state.scene -= 1
            st.rerun()
    with c_next:
        if st.button("Next Scene ➡️", disabled=(st.session_state.scene == 4)):
            st.session_state.scene += 1
            st.rerun()
            
    st.write(f"*Story Timeline Node: Step {st.session_state.scene} of 4*")

# 5. DATA ENGINE PROCESSING FOR VISUALIZATION
if st.session_state.scene == 1:
    df_vis = df[(df["Country"] == "Global Average") & (df["Year"] <= 1920)]
elif st.session_state.scene == 2:
    df_vis = df[(df["Country"] == "Global Average") & (df["Year"] <= 1980)]
elif st.session_state.scene == 3:
    df_vis = df[df["Country"] == "Global Average"]
else:
    # Filter dataset using the reader-driven selections
    df_vis = df[(df["Country"].isin(selected_countries)) & (df["Year"] >= year_range[0]) & (df["Year"] Country:</b> %{customdata}<br><b>Year:</b> %{x}<br><b>Avg Temp:</b> %{y}°C<extra></extra>",
                customdata=[country]*len(c_df)
            ))
            
        fig.update_layout(
            xaxis=dict(title="Timeline (Years) [Quantitative Variable]", gridcolor="lightgray"),
            yaxis=dict(title="Average Surface Temperature (°C) [Quantitative]", gridcolor="lightgray"),
            height=600, hovermode="closest"
        )
        st.plotly_chart(fig, use_container_width=True)

    elif chart_type == "Bar Chart Comparison":
        # Proposal Section 5: Bar Chart Implementation
        fig_bar = px.bar(
            df_vis, x="Country", y="AverageTemperature", color="Country", animation_frame="Year",
            title="Temperature Comparison Between Regions Over Selected Epochs",
            labels={"AverageTemperature": "Avg Temp (°C)", "Country": "Region"}
        )
        fig_bar.update_layout(height=600, yaxis_range=[0, 30])
        st.plotly_chart(fig_bar, use_container_width=True)

    elif chart_type == "Correlation Heatmap":
        # Proposal Section 5: Heatmap Implementation
        pivot_df = df_vis.pivot(index="Country", columns="Year", values="AverageTemperature")
        fig_heat = px.imshow(
            pivot_df, labels=dict(x="Year", y="Country", color="Temp (°C)"),
            x=pivot_df.columns, y=pivot_df.index,
            color_continuous_scale="YlOrRd",
            title="Climate Intensity Grid Matrix"
        )
        fig_heat.update_layout(height=600)
        st.plotly_chart(fig_heat, use_container_width=True)
