import os
import streamlit as st
import time
import numpy as np
import pandas as pd
import folium
from streamlit_folium import st_folium
from utils.make_rest import fetch_with_params

def get_map(coord1, coord2):
    lat_cent = (coord1[0] + coord2[0]) / 2
    lon_cent= (coord1[1] + coord2[1]) / 2

    mapa = folium.Map(location=[lat_cent, lon_cent], zoom_start=14)

    folium.PolyLine([coord1, coord2], color="blue", weight=4).add_to(mapa)

    kw = {"prefix": "fa", "color": "green", "icon": "arrow-up"}
    angle = 300
    icon = folium.Icon(angle=angle, **kw)

    fire_icon = folium.Icon(icon="fire", prefix="fa", color="orange")

    folium.Marker(coord1, tooltip="Chapultepec",icon=fire_icon).add_to(mapa)
    folium.Marker(coord2, tooltip="Polanco",icon=icon).add_to(mapa)

    return mapa

def response_generator(response:str, time_val:int):
    
    time.sleep(time_val)

    for word in response.split():
        yield word + " "
        time.sleep(0.05)
 


st.title("Agents chat")
st.markdown("<br>", unsafe_allow_html=True)

if "messages" not in st.session_state:
    st.session_state.messages = []

if "answer" not in st.session_state:
    st.session_state['answer']= False

col1, col2 = st.columns([2,2])

with col1:

    for message in st.session_state.messages:
        if message["role"] == "assistant":
            with st.chat_message(message["role"],avatar="data/semantic_kernel.png"):
                st.markdown(message["content"])
        else:
            with st.chat_message(message["role"],avatar="data/user.png"):
                st.markdown(message["content"])

    if prompt := st.chat_input("Input Location"):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user",avatar="data/user.png"):
            st.markdown(prompt)

        with st.chat_message("assistant",avatar="data/semantic_kernel.png"):

            url = os.getenv("CHAT_AGENT_URL")
            query = {"collection": "chat_kernel", "id": f"{prompt}"}

            full_response =  fetch_with_params(url, params=query)
            response = full_response.get('message')
            map= full_response.get('map')

        st.session_state.messages.append({"role": "assistant", "content": response})
        st.session_state['answer'] = True

with col2:

    if st.session_state['answer'] :

        ev_agent= st.chat_message("assistant",avatar='data/semantic_kernel.png')
        ev_agent.write("Evacuation Route")
        st.markdown("<br>", unsafe_allow_html=True)


        st_data = st_folium(map)