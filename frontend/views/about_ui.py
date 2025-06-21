import streamlit as st

st.title("About Us")

# Disclaimer section
st.warning("## Explore responsibly \n"
"This system uses multiple artificial intelligence agents to generate predictions and personalized suggestions and collect relevant data based on the environment or scenario analyzed."
"When using this platform, you can enter environmental conditions, terrain variables, or historical data. This information will be used solely to improve the quality of the suggestions and forecasts."
"Your information will not be stored or shared.")
st.info("## Disclaimer \n"
"This multi-agent system uses artificial intelligence to provide predictions, suggestions, and data collection for informational purposes."
"While mechanisms have been implemented to improve accuracy and reliability, critical decisions must be made by trained professionals."
"By using this platform, you acknowledge that its results do not constitute official advice nor guarantee absolute accuracy.")

st.markdown("---")

# Bots/Agents info
bots = [
    {
        "name": "Evacuation Agent",
        "img": "data/evacuation_agent.png",
        "desc": "Recommends safe routes and evacuation actions based on the fire's progress and user type."
    },
    {
        "name": "Prediction Agent",
        "img": "data/prediction_agent.png",
        "desc": "Predicts fire progress and anticipates risk zones using meteorological and topographic data."
    },
    {
        "name": "Vulnerability Agent",
        "img": "data/vulnerable_zones_agent.png",
        "desc": "Identifies vulnerable areas and issues early warnings to communities and firefighters."
    },
    {
        "name": "Data Collection Agent",
        "img": "data/collection_agent.png",
        "desc": "Collects and displays real-time weather, vegetation, and topography data."
    }
]

cols = st.columns(4)
for i, bot in enumerate(bots):
    with cols[i]:
        st.image(bot["img"], width=80)
        st.markdown(f"**{bot['name']}**")
        st.caption(bot["desc"])