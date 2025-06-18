import streamlit as st
from streamlit.components.v1 import html
from mock_api import generate_animation
import numpy as np


st.set_page_config(
    page_title="Agent Spread Simulation",
    page_icon="🔥",
    layout="wide",
    initial_sidebar_state="expanded")


if 'chat' not in st.session_state:
    st.session_state['chat'] = False


with st.sidebar:

    #st.image("data/p9.png", width=100)

    
    st.header("Parameters")
    valor1 = st.slider("Wind Speed (km/hr)", 0, 100, 50)
    valor2 = st.slider("Temperature (°C)", 0, 50, 25)
    valor3 = st.slider("RH %", 0, 100, 25)
    
    run_button = st.button("Run Simulation",key='but')

    st.info("Press Run Simulation to start.")


col1, col2 = st.columns([2,2])

with col1:
    if run_button :
        with st.spinner("Running Simulation...", show_time=True):
            an = generate_animation()
            html(an.to_jshtml(), height=620, width=700)
            st.success("Done!")
            st.session_state['chat'] = True
            

with col2:
    if st.session_state['chat']:

        prediction_agent= st.chat_message("assistant",avatar='data/p9.png')
        prediction_agent.write("Simulation finished!")
        prediction_agent.write("Fire intensity is extremly high and will takedown almost all threes in the zone")
        
        evacuation_agent = st.chat_message("assistant",avatar='data/p7.png')
        evacuation_agent.write("Here is the suggested action plan: ")
        evacuation_agent.bar_chart(np.random.randn(30, 3))
    
        #messages = st.container(height=150)
        if prompt := st.chat_input("Ask something"):
            pass
            #messages.chat_message("assistant",avatar='data/p9.png').write(f"Analizing ... ")
