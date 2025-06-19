
import streamlit as st
from streamlit_option_menu import option_menu
import numpy as np
from streamlit.components.v1 import html
from utils.forest_agent import generate_animation

st.set_page_config(
    page_title="Ignis Sentinels",
    page_icon="🔥",
    layout="wide",
    initial_sidebar_state="expanded")

st.markdown("<h1 style='text-align: center;'> 🔥 IGNIS SENTINELS 🌐 </h1>", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

selected = option_menu(
    menu_title = None,
    options = ['about us','map','evacuation','simulation','chat'],
    icons = ['tree-fill','geo','sign-turn-slight-right-fill','fire','chat-left'],
    orientation = "horizontal"
)

if selected == 'about us':
    st.title(f"Selected {selected}")

if selected == 'map':
    st.title(f"Selected {selected}")

if selected == 'evacuation':
    st.title(f"Selected {selected}")

if selected == 'simulation':

    with st.sidebar:

        st.header("Parameters")
        st.markdown("<br>", unsafe_allow_html=True)
        valor1 = st.slider("Wind Speed (km/hr)", 0, 100, 50)
        valor2 = st.slider("Temperature (°C)", 0, 50, 25)
        valor3 = st.slider("RH (%)", 0, 100, 25)
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

        prediction_agent= st.chat_message("assistant",avatar='data/prediction_agent.png')
        prediction_agent.write("Press run button to start")

    col1, col2 = st.columns([2,2])

    with col1:
        if run_button :
            st.markdown("<br>", unsafe_allow_html=True)
            with st.spinner("Running Simulation...", show_time=True):
                an = generate_animation()
                html(an.to_jshtml(), height=620, width=700)
                st.success("Done!")
                
                with col2:

                        prediction_agent= st.chat_message("assistant",avatar='data/prediction_agent.png')
                        prediction_agent.write("Simulation finished!")
                        prediction_agent.write("Fire intensity is extremly high and will takedown almost all threes in the zone")
                        
                        evacuation_agent = st.chat_message("assistant",avatar='data/prediction_agent.png')
                        evacuation_agent.write("Here is the suggested action plan: ")
                        evacuation_agent.bar_chart(np.random.randn(30, 3))
                    

if selected == 'chat':

    st.title("Simple chat")

    if "messages" not in st.session_state:
        st.session_state.messages = []

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if prompt := st.chat_input("What is up?"):
        with st.chat_message("user"):
            st.markdown(prompt)
        st.session_state.messages.append({"role": "user", "content": prompt})