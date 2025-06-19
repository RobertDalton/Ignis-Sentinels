import streamlit as st
from streamlit.components.v1 import html
from utils.forest_agent import generate_animation
import numpy as np



with st.sidebar:
    
    st.header("Parameters")
    valor1 = st.slider("Wind Speed (km/hr)", 0, 100, 50)
    valor2 = st.slider("Temperature (°C)", 0, 50, 25)
    valor3 = st.slider("RH (%)", 0, 100, 25)
    
    run_button = st.button("Run Simulation",key='but')

    st.info("Press Run Simulation to start.")


col1, col2 = st.columns([2,2])

with col1:
    if run_button:
        with st.spinner("Running Simulation...", show_time=True):
            an = generate_animation()
            html(an.to_jshtml(), height=620, width=700)
            st.success("Done!")
            
            with col2:
                    prediction_agent= st.chat_message("assistant",avatar='data/prediction_agent.png')
                    prediction_agent.write("Simulation finished!")
                    prediction_agent.write("Fire intensity is extremly high and will takedown almost all threes in the zone")
                    
                    evacuation_agent = st.chat_message("assistant",avatar='data/prediction_agent.png')
                    evacuation_agent.write("Here is the distribution plot ")
                    evacuation_agent.bar_chart(np.random.randn(30, 3))

