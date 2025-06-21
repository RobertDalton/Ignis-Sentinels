
import os
from azure.ai.projects import AIProjectClient
from azure.ai.projects.models import FunctionTool, ToolSet, CodeInterpreterTool
from azure.identity import DefaultAzureCredential
from functions import user_functions
from dotenv import load_dotenv

load_dotenv()

p_format = {
  "id": "content",
  "intensity": {
    "FFMC": "content",
    "DMC": "content",
    "DC": "content",
    "ISI": "content",
    "BUI": "content",
    "FWI": "content"
  },
  "spread": {
    "gif_link": "content",
    "accuracy": "content"
  }
}

s_format =  {
  "spread": {
    "gif_link": "content",
  }
}

agent_prompt = f'You will predict data base on a FWI (Fire Weather Index) and climate paramerts, you will use your tool simulation for the animation' \
'and internet and web search formulas for the FWI and the other indexes, web search and your knowledge to answer as best as possible, answer in this format if is simulation {s_format} and ' \
'{p_format} otherwise'

model = os.getenv("MODEL_DEPLOYMENT_NAME")
project_connection_string = os.getenv("PROJECT_CONNECTION_STRING")  


project_client = AIProjectClient.from_connection_string(
    credential=DefaultAzureCredential ,
    conn_str=project_connection_string,
)


with project_client:

    functions = FunctionTool(user_functions)
    
    toolset = ToolSet()
    toolset.add(functions)
   

    agent = project_client.agents.create_agent(
        model=model,
        name="Prediction-Agent",
        instructions=agent_prompt ,
        toolset=toolset,
    )
    print(f"Created agent, ID: {agent.id}")

    # Create thread for communication
    thread = project_client.agents.create_thread()
    print(f"Created thread, ID: {thread.id}")

    test_collection = {
  "id": "1",
  "location_name": "San Pedro Columbia",
  "weather_conditions": {
    "temperature": "34.2",
    "relative_humidity": "48",
    "wind_speed": "12.4",
    "precipitation": "0.0",
    "prob_precipitation": "62"
  },
  "location_coordinates": {
    "lat": 18.15221,
    "lon": -88.41259
  },
  "location_details": {
    "altitude_meters": 312.0,
    "slope_degrees": 11.3,
    "aspect_degrees": 135.0,
    "aspect_cardinal": "SE",
    "terrain_type": "forest foothills",
    "source": "DEM SRTM 30m"
  },
  "satellite_wildfire_image": "https://landinginputs.blob.core.windows.net/satelite/s1.jpg?se=2035-06-15T04%3A35%3A37Z&sp=r&sv=2025-05-05&sr=b&sig=jfYQ6KWCQPUyxcFbDFXKO6sxrGZXNs3tItZ6qQVtmVw%3D",
  "vegetation_distribution": "https://landinginputs.blob.core.windows.net/vegetation/v1.jpg?se=2035-06-15T04%3A35%3A38Z&sp=r&sv=2025-05-05&sr=b&sig=GgS4ITPZKUD%2BFAeECSQ6m4d/S6MZPLWF2jikQuMGSq8%3D"
}

    message = project_client.agents.create_message(
        thread_id=thread.id,
        role="user",
        content=test_collection,
    )

    run = project_client.agents.create_and_process_run(thread_id=thread.id, assistant_id=agent.id)
    # [END create_and_process_run]
    print(f"Run finished with status: {run.status}")

    if run.status == "failed":
        print(f"Run failed: {run.last_error}")

    

    messages = project_client.agents.list_messages(thread_id=thread.id)
    print(f"Messages: {messages}")
    print("\n")
    
    print(f"Weather: {messages.data[0].content[0].text.value}")