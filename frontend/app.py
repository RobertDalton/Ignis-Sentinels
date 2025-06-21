import streamlit as st


about = st.Page("views/about_ui.py", title="About us", icon="")
map = st.Page("views/map_ui.py", title="Map", icon="")
evacuation= st.Page("views/evacuation_ui.py", title="Evacuation", icon="")
simulation= st.Page("views/simulation_ui.py", title="Simulation", icon="")
chat = st.Page("views/chat_ui.py", title="Agent Chat", icon="")
pg = st.navigation([about,map,evacuation,simulation,chat])

st.set_page_config(
    page_title="Ignis Sentinels",
    page_icon="🔥",
    layout="wide",
    initial_sidebar_state="expanded")
pg.run()