import streamlit as st



create_page = st.Page("views/chat_ui.py", title="Agent Chat", icon="")
delete_page = st.Page("views/simulation_ui.py", title="Simulation", icon="")

pg = st.navigation([create_page, delete_page])

st.set_page_config(
    page_title="Ignis Sentinels",
    page_icon="🔥",
    layout="wide",
    initial_sidebar_state="expanded")
pg.run()