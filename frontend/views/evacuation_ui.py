import streamlit as st
import pandas as pd
import folium
import glob
import os
import json
import requests

from utils.make_rest import fetch_with_params
from streamlit_folium import st_folium


geojson_files = glob.glob(os.path.join('coordenates', "*.geojson")) #TODO: Will be in DB
fire_points = []

for file in geojson_files:
    with open(file, "r", encoding="utf-8") as f:
        data = json.load(f)
        for feat in data["features"]:
            lon, lat = feat["geometry"]["coordinates"]
            props = feat["properties"]
            unique_id = f"{props.get('acq_date', '')}_{props.get('acq_time', '')}_{lat}_{lon}"
            fire_points.append({
                "id": unique_id,
                "incident_id": f"🔥{file.split('_')[2]}_{props.get('acq_date', '')}_{props.get('acq_time', '')}",
                "location_name": f"{file.split('_')[2]}",
                "lat": lat,
                "lon": lon,
                "brightness": props.get("brightness"),
                "confidence": props.get("confidence"),
                "frp": props.get("frp"),
                "acq_date": props.get("acq_date"),
                "acq_time": props.get("acq_time"),
                "FWI": props.get("brightness", 0) / 10  # Escala ficticia
            })

if not fire_points:
    st.error("No wildfire GeoJSON data found.")
    st.stop()

map_df = pd.DataFrame(fire_points)
map_df = map_df.drop_duplicates(subset="id")

with st.sidebar:
    st.info(f"GeoJSON files loaded: {len(geojson_files)}")
    st.info(f"Unique fires: {len(map_df)}")

with st.sidebar:
    st.markdown("### 🔥 Filter by Risk Level (FWI)")
    low = st.checkbox("Low (FWI < 20)", value=True)
    medium = st.checkbox("Moderate (20 ≤ FWI < 40)", value=True)
    high = st.checkbox("High (FWI ≥ 40)", value=True)

    fwi_filtered_df = map_df[
        ((low & (map_df["FWI"] < 20)) |
         (medium & (map_df["FWI"] >= 20) & (map_df["FWI"] < 40)) |
         (high & (map_df["FWI"] >= 40)))
    ]

    st.markdown("### 📍 Select Incident")
    incident_options = map_df["id"].tolist()
    def incident_label(inc_id):
        row = map_df[map_df["id"] == inc_id].iloc[0]
        return f"{row['incident_id']} | Lat: {row['lat']:.5f}, Lon: {row['lon']:.5f}"

    if incident_options:
        selected_incident = st.selectbox(
            "Select Incident:",
            incident_options,
            format_func=incident_label,
            key="incident_selectbox"
        )
        selected_fire = map_df[map_df["id"] == selected_incident].iloc[0]
    else:
            selected_fire = None
    
    if selected_fire is not None:
        if selected_fire["id"] not in fwi_filtered_df["id"].values:
            fwi_filtered_df = pd.concat([fwi_filtered_df, pd.DataFrame([selected_fire])], ignore_index=True)
    fwi_filtered_df = fwi_filtered_df.drop_duplicates(subset="id")

    if selected_fire is not None:
        base_lat = selected_fire["lat"]
        base_lon = selected_fire["lon"]
        evac_routes = [
            {
                "name": "Pedestrian Route",
                "type": "pedestrian",
                "color": "blue",
                "points": [
                    [base_lat, base_lon],
                    [base_lat + 0.02, base_lon + 0.02],
                    [base_lat + 0.04, base_lon + 0.01]
                ]
            },
            {
                "name": "Vehicle Route",
                "type": "vehicle",
                "color": "orange",
                "points": [
                    [base_lat, base_lon],
                    [base_lat - 0.01, base_lon + 0.03],
                    [base_lat - 0.03, base_lon + 0.04]
                ]
            },
            {
                "name": "Reduced Mobility Route",
                "type": "reduced_mobility",
                "color": "purple",
                "points": [
                    [base_lat, base_lon],
                    [base_lat + 0.01, base_lon - 0.02],
                    [base_lat + 0.03, base_lon - 0.03]
                ]
            },
            {
                "name": "Brigade Route",
                "type": "brigade",
                "color": "green",
                "points": [
                    [base_lat, base_lon],
                    [base_lat - 0.02, base_lon - 0.02],
                    [base_lat - 0.04, base_lon - 0.01]
                ]
            }
        ]

    st.markdown("### 🚨 Evacuation Routes")
    tipo_usuario = st.selectbox(
        "User type",
        ["pedestrian", "vehicle", "brigade", "reduced_mobility"],
        format_func=lambda x: {
            "pedestrian": "🚶‍♂️ Pedestrian",
            "vehicle": "🚒 Emergency Vehicle",
            "brigade": "🧑‍🚒 Brigade Member",
            "reduced_mobility": "🧓 Reduced Mobility"
        }[x],
        key="route_type_selectbox"
    )

    recalcular = st.button("🔄 Recalculate routes")
    if recalcular:
        st.success("Routes automatically recalculated based on fire proximity.")

if 'tipo_usuario' in locals():
    rutas_filtradas = [r for r in evac_routes if r["type"] == tipo_usuario]
else:
    rutas_filtradas = []

if 'map_center' not in st.session_state:
    st.session_state['map_center'] = [0, 0]
    st.session_state['map_zoom'] = 2
    st.session_state['last_selected_fire'] = None

if 'selected_fire' in locals() and selected_fire is not None:
    if st.session_state['last_selected_fire'] != selected_fire["id"]:
        st.session_state['map_center'] = [selected_fire["lat"], selected_fire["lon"]]
        st.session_state['map_zoom'] = 13
        st.session_state['last_selected_fire'] = selected_fire["id"]

center = st.session_state['map_center']
zoom = st.session_state['map_zoom']

st.subheader("Active Wildfire Locations")

m = folium.Map(location=center, zoom_start=zoom, tiles=None, min_zoom=2, max_zoom=18)

folium.TileLayer('cartodbpositron', name='Calles (Claro)').add_to(m)
folium.TileLayer('cartodbdark_matter', name='Calles (Oscuro)').add_to(m)
folium.TileLayer('OpenStreetMap', name='OpenStreetMap').add_to(m)
folium.TileLayer('Esri.WorldImagery', name='Satélite', attr='Tiles © Esri').add_to(m)
folium.TileLayer('Esri.WorldTopoMap', name='Topográfico', attr='Tiles © Esri').add_to(m)

# Añadir marcadores de incendio
for _, row in fwi_filtered_df.iterrows():
    color = "red" if row["FWI"] >= 40 else "orange" if row["FWI"] >= 20 else "green"
    popup = folium.Popup(
        f"<b>Incident:</b> {row['incident_id']}<br>"
        f"<b>Latitude:</b> {row['lat']}<br>"
        f"<b>Length:</b> {row['lon']}<br>"
        f"<b>Brightness:</b> {row['brightness']}<br>"
        f"<b>Confidence:</b> {row['confidence']}<br>"
        f"<b>FRP:</b> {row['frp']}<br>"
        f"<b>FWI:</b> {row['FWI']:.1f}",
        max_width=300
    )
    folium.CircleMarker(
        location=[row["lat"], row["lon"]],
        radius=8 if selected_fire is not None and row["id"] == selected_fire["id"] else 5,
        color=color,
        fill=True,
        fill_color=color,
        fill_opacity=0.7,
        popup=popup
    ).add_to(m)


url = os.getenv("EVACUATION_AGENT_URL")
query = {"collection": "evacuation_agent", "id": f"{row['incident_id']}"}

response =  fetch_with_params(url, params=query)
rutas_filtradas = response.get('routes')
recomendations = response.get('recommendations')

for ruta in rutas_filtradas:
    folium.PolyLine(
        locations=[[lat, lon] for lat, lon in ruta["points"]],
        color=ruta["color"],
        weight=6,
        opacity=0.8,
        popup=ruta["name"]
    ).add_to(m)

folium.LayerControl().add_to(m)

st_data = st_folium(m, width=900, height=600)

if 'selected_fire' in locals() and selected_fire is not None:
    with st.expander("Evacuation Agent Recommendations"):
        st.markdown(f"{recomendations}")
else:
    st.info("Select a fire from the sidebar or search by ID to display map and data.")