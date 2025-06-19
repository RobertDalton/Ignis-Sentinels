import streamlit as st



chat = st.Page("views/chat_ui.py", title="Agent Chat", icon="")
simulation= st.Page("views/simulation_ui.py", title="Simulation", icon="")
map = st.Page("views/map_ui.py", title="Map", icon="")
pg = st.navigation([map,chat,simulation])

st.set_page_config(
    page_title="Ignis Sentinels",
    page_icon="🔥",
    layout="wide",
    initial_sidebar_state="expanded")
pg.run()