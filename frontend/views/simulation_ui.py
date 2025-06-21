import streamlit as st
from streamlit.components.v1 import html
from utils.make_rest import fetch_with_params
import numpy as np
import os

with st.sidebar:

    st.header("Parameters")
    st.markdown("<br>", unsafe_allow_html=True)
    wind_speed = st.slider("Wind Speed (km/hr)", 0, 100, 50)
    temperature = st.slider("Temperature (°C)", 0, 50, 25)
    rh = st.slider("RH (%)", 0, 100, 25)
    days_since_rain = st.slider(
                    "Days Since Last Significant Rain",
                    0, 60, 7, 
                    help="Number of days since the last rainfall of 5mm or more. Higher values increase fire risk."
                )
    fwi_value = st.slider(
                        "Fire Weather Index (FWI)",
                        min_value=float(0),
                        max_value=float(120),
                        value=float(30),
                        help="The FWI (Fire Weather Index) indicates the fire risk. Higher values mean greater danger."
                    )
    
    st.markdown("<br>", unsafe_allow_html=True)
    run_button = st.button("Run Simulation",key='but')

    url_pred = os.getenv("PREDICTION_AGENT_URL_SIMULATION")
    query_pred = {"collection": "prediction_agent",
                  "days_since_rain": days_since_rain,
                  "fwi_value": fwi_value,
                  "wind_speed":wind_speed,
                  "temperature":temperature,
                  "rh":rh,
                  }

    prediction_agent_data = fetch_with_params(query_pred)

    prediction_agent= st.chat_message("assistant",avatar='data/prediction_agent.png')
    prediction_agent.write("Press run button to start")


col1, col2 = st.columns([2,2])

with col1:
    if run_button :
        st.markdown("<br>", unsafe_allow_html=True)
        with st.spinner("Running Simulation...", show_time=True):
            an = prediction_agent["spread"]["matplot"],
            html(an.to_jshtml(), height=620, width=700)
            prediction_agent.write("Simulation finished!")

        with col2:
            st.markdown("<br>", unsafe_allow_html=True)
            prediction_agent= st.chat_message("assistant",avatar='data/prediction_agent.png')
            prediction_agent.write("Use the widget buttons to see the simulation")
