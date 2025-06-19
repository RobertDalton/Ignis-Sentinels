import streamlit as st
import pandas as pd
import pydeck as pdk

st.set_page_config(layout="wide")

# Simular datos de incendios activos
active_points = [
    {
        "id": "1",
        "incident_id": "🔥INC-001",
        "location_name": "San Pedro Columbia",
        "lat": 18.15221,
        "lon": -88.41259,
        "FWI": 42.9
    },
    {
        "id": "2",
        "incident_id": "🔥INC-002",
        "location_name": "Xucaneb",
        "lat": 17.5,
        "lon": -88.7,
        "FWI": 40
    },
    {
        "id": "3",
        "incident_id": "🔥INC-003",
        "location_name": "Blue Creek",
        "lat": 16.9,
        "lon": -88.3,
        "FWI": 15
    }
]
map_df = pd.DataFrame(active_points)
if "selected_fire" not in st.session_state:
    st.session_state.selected_fire = None

# Filtro, selección y alertas en la barra lateral
with st.sidebar:
    st.markdown("## 🔍 Search and Filters")

    # --- Search by ID ---
    search = st.text_input("Search by ID (e.g., INC-001)").upper().strip()

    # --- Title: Risk filter BEFORE the checkboxes ---
    st.markdown("### 🔥 Filter by Risk Level (FWI)")

    # --- Risk checkboxes ---
    low = st.checkbox("Low (FWI < 20)", value=True)
    medium = st.checkbox("Moderate (20 ≤ FWI < 40)", value=True)
    high = st.checkbox("High (FWI ≥ 40)", value=True)

    # --- Apply filters to map ---
    fwi_filtered_df = map_df[
        ((low & (map_df["FWI"] < 20)) |
         (medium & (map_df["FWI"] >= 20) & (map_df["FWI"] < 40)) |
         (high & (map_df["FWI"] >= 40)))
    ]

    # --- Filter by ID ---
    filtered_df = (
        fwi_filtered_df[fwi_filtered_df["incident_id"].str.contains(search, case=False)]
        if search else fwi_filtered_df
    )

    # --- Select buttons ---
    st.markdown("### 📍 Select Incident")
    for _, row in filtered_df.iterrows():
        if st.button(row["incident_id"]):
            st.session_state.selected_fire = row

    if st.session_state.selected_fire is not None:
        current_id = st.session_state.selected_fire["id"]
        if current_id not in fwi_filtered_df["id"].tolist():
            st.session_state.selected_fire = None

    # --- Warnings ---
    st.markdown("---")
    st.markdown("### ⚠️ Early Warnings")
    st.markdown("- *High ignition* likelihood in **Xucaneb**")
    st.markdown("- *Severe drought* risk in **Blue Creek**")
    st.markdown("- Active monitoring in southern riparian areas")


# -----------------------
# Agentes de datos (panel inferior)
# -----------------------
data_collection_agent = {
    "weather_conditions": {
        "temperature": "34.2",
        "relative_humidity": "48",
        "wind_speed": "12.4",
        "precipitation": "0.0",
        "prob_precipitation": "62"
    },
    "vegetation_distribution": "https://landinginputs.blob.core.windows.net/vegetation/v1.jpg?se=2035-06-15T04%3A35%3A38Z&sp=r&sv=2025-05-05&sr=b&sig=GgS4ITPZKUD%2BFAeECSQ6m4d/S6MZPLWF2jikQuMGSq8%3D"
}

prediction_agent = {
    "intensity": {
        "FFMC": 94.6,
        "DMC": 81.3,
        "DC": 328.1,
        "ISI": 20.5,
        "BUI": 114.7,
        "FWI": 42.9
    },
    "spread": {
        "gif_link": "https://landinginputs.blob.core.windows.net/gifs/gif1.gif?se=2035-06-15T06%3A14%3A12Z&sp=r&sv=2025-05-05&sr=b&sig=NDnNuYHBKrJnrDRlO9XV3fd1emCJHPzNqLMxb2B7YtI%3D",
        "accuracy": 90
    }
}

vulnerable_zones_agent = {
    "vulnerable_zones": [
        {"danger_item_name": "Columbia River riparian zone", "accuracy": 88},
        {"danger_item_name": "Xucaneb community nursery", "accuracy": 76}
    ],
    "extra_zone_details": [
        {"details_item_name": "High erosion risk due to deforestation near riverbanks", "accuracy": 82}
    ]
}
# -----------------------
# Agente de topología (datos de relieve, imágenes satelitales y vegetación)
# -----------------------
topology_agent = {
    "location_details": {
        "altitude_meters": 312.0,
        "slope_degrees": 11.3,
        "aspect_degrees": 135.0,
        "aspect_cardinal": "SE",
        "terrain_type": "forest foothills",
        "source": "DEM SRTM 30m"
    },
    "satellite_wildfire_image": "https://landinginputs.blob.core.windows.net/satelite/s1.jpg?se=2035-06-15T04%3A35%3A37Z&sp=r&sv=2025-05-05&sr=b&sig=jfYQ6KWCQPUyxcFbDFXKO6sxqGZXNs3tItZ6qQVtmVw%3D",
    "vegetation_distribution": "https://landinginputs.blob.core.windows.net/vegetation/v1.jpg?se=2035-06-15T04%3A35%3A38Z&sp=r&sv=2025-05-05&sr=b&sig=GgS4ITPZKUD%2BFAeECSQ6m4d/S6MZPLWF2jikQuMGSq8%3D"
}


selected = st.session_state.selected_fire.to_dict() if isinstance(st.session_state.selected_fire, pd.Series) else st.session_state.selected_fire

if selected:
    selected_id = selected["id"]
    view_lat = selected["lat"]
    view_lon = selected["lon"]
    
   
    highlight_df = fwi_filtered_df[fwi_filtered_df["id"] == selected_id]
    other_df = fwi_filtered_df[fwi_filtered_df["id"] != selected_id]
else:
    view_lat = map_df["lat"].mean()
    view_lon = map_df["lon"].mean()
    highlight_df = pd.DataFrame()
    other_df = fwi_filtered_df.copy() 


tooltip = {
    "html": """
    <b>{location_name}</b><br/>
    FWI: {FWI}<br/>
    🌿 Vegetation: forest foothills<br/>
    🌡️ Temp: 34.2 °C<br/>
    🌧️ Rain probability: 62%
    """,
    "style": {
        "backgroundColor": "white",
        "color": "black",
        "fontSize": "13px",
        "padding": "10px",
        "border": "1px solid #ddd"
    }
}

st.subheader("Active Wildfire Locations")

# Distribución: mapa ancho (4) + panel lateral (1)
map_col, topo_col = st.columns([4, 1])

with map_col:
    st.pydeck_chart(
        pdk.Deck(
            map_style="mapbox://styles/mapbox/light-v9",
            initial_view_state=pdk.ViewState(
                latitude=view_lat,
                longitude=view_lon,
                zoom=8 if not selected else 10,
                pitch=50,
            ),
            layers=[
                pdk.Layer(
                    "ScatterplotLayer",
                    data=other_df,
                    get_position="[lon, lat]",
                    get_color="[FWI * 6, 255 - FWI * 6, 0, 160]",
                    get_radius=400,
                    pickable=True,
                ),
                pdk.Layer(
                    "ScatterplotLayer",
                    data=highlight_df,
                    get_position="[lon, lat]",
                    get_color="[255, 0, 0, 200]",
                    get_radius=700,
                    pickable=True,
                ),
                pdk.Layer(
                    "HeatmapLayer",
                    data=fwi_filtered_df,
                    get_position="[lon, lat]",
                    get_weight="FWI",
                    aggregation='"MEAN"',
                ),
            ],
            tooltip=tooltip,
        ),
        height=800,
    )

with topo_col:
    if selected:
        topo = topology_agent["location_details"]

        # Estilo general ambas tarjetas
        st.markdown("""
        <style>
        .custom-card {
            background-color: rgba(40, 44, 52, 0.95);
            padding: 24px;
            border-radius: 16px;
            font-size: 16px;
            color: #f8f9fa;
            box-shadow: 0 0 12px rgba(0,0,0,0.35);
            margin-bottom: 20px;
            height: 360px;

        }
        .custom-card h3 {
            font-size: 20px;
            margin-bottom: 16px;
            color: #f9c74f;
        }
        .custom-card ul {
            padding-left: 20px;
            margin: 0;
        }
        .custom-card li {
            margin-bottom: 6px;
        }
        .custom-card small {
            font-size: 11px;
            color: #aaa;
        }
        </style>
        """, unsafe_allow_html=True)

        # Topografía
        st.markdown(f"""
        <div class="custom-card">
            <h3>🧭 Topography</h3>
            <div>🗻 <b>Altitude:</b> {topo['altitude_meters']} m</div>
            <div>↘ <b>Slope:</b> {topo['slope_degrees']}°</div>
            <div>🧭 <b>Aspect:</b> {topo['aspect_degrees']}° ({topo['aspect_cardinal']})</div>
            <div>🌳 <b>Terrain:</b> {topo['terrain_type']}</div>
            <div>🛰️ <b>Source:</b> {topo['source']}</div>
        </div>
        """, unsafe_allow_html=True)

        # Zonas vulnerables (ahora justo debajo)
        zones_html = "".join(
            f"<li>{z['danger_item_name']} ({z['accuracy']}% certainty)</li>"
            for z in vulnerable_zones_agent["vulnerable_zones"]
        )
        extras_html = "".join(
            f"<li>{e['details_item_name']} ({e['accuracy']}% certainty)</li>"
            for e in vulnerable_zones_agent["extra_zone_details"]
        )

        st.markdown(f"""
        <div class="custom-card">
            <h3>📍 Vulnerable Zones</h3>
            <ul>{zones_html}</ul>
            <p style="margin-top:12px;"><b>Additional Details</b></p>
            <ul>{extras_html}</ul>
            <small>Vulnerability Agent</small>
        </div>
        """, unsafe_allow_html=True)

# ------------------- Mostrar solo si hay selección -------------------
if st.session_state.selected_fire is not None:
 

    # --------- Paneles de Agentes -----------
    st.markdown("---")
    col1, col2, col3 = st.columns(3)

    with col1:
        st.subheader("Weather Conditions")
        clima = data_collection_agent["weather_conditions"]
        st.image("https://static.vecteezy.com/system/resources/previews/036/353/735/non_2x/cloud-and-rain-free-png.png", width=80)
        st.metric("🌡️ Temperature", f"{clima['temperature']} °C")
        st.metric("🌧️ Rain Probability", f"{clima['prob_precipitation']} %")
        st.markdown("**Additional Data:**")
        st.markdown(f"- 💧 **Relative Humidity:** {clima['relative_humidity']}%")
        st.markdown(f"- 💨 **Wind:** {clima['wind_speed']} km/h")
        st.markdown(f"- ☔ **Precipitation:** {clima['precipitation']} mm")
        st.caption("Weather Agent")

    with col2:
        st.subheader("Topography")
        if st.button("View Satellite Image"):
            st.image(topology_agent["satellite_wildfire_image"], caption="High-resolution Satellite Image")
        if st.button("View Vegetation Distribution"):
            st.image(topology_agent["vegetation_distribution"], caption="Vegetation Distribution")
        

    with col3:
        st.markdown('<h3 style="color:#FF914D;">🔥 Fire Spread Risk</h3>', unsafe_allow_html=True)
        fwi = prediction_agent["intensity"]["FWI"]
        st.metric(
            label="FWI (Fire Weather Index)",
            value=fwi,
            delta=f"certainty: {prediction_agent['spread']['accuracy']}%"
        )
        with st.expander("Fire Index Details"):
            intensity = prediction_agent["intensity"]
            st.markdown(f"- **FFMC:** {intensity['FFMC']}")
            st.markdown(f"- **DMC:** {intensity['DMC']}")
            st.markdown(f"- **DC:** {intensity['DC']}")
            st.markdown(f"- **ISI:** {intensity['ISI']}")
            st.markdown(f"- **BUI:** {intensity['BUI']}")
            st.markdown(f"- **FWI:** {intensity['FWI']}")
        st.image(prediction_agent["spread"]["gif_link"], caption="Spread Prediction")
        st.caption("Prediction Agent")

# ------------------- Cuando NO hay selección -------------------
else:
    st.info("Select a fire from the sidebar or search by ID to display map and data.")

