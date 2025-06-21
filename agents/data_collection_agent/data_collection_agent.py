
import os
from azure.ai.projects import AIProjectClient
from azure.ai.projects.models import FunctionTool, ToolSet, CodeInterpreterTool
from functions import user_functions
from dotenv import load_dotenv
from azure.identity import DefaultAzureCredential


load_dotenv()

{
  "id": "content_data",
  "location_name": "content_data",
  "weather_conditions": {
    "temperature": "content_data",
    "relative_humidity": "content_data",
    "wind_speed": "content_data",
    "precipitation": "content_data",
    "prob_precipitation": "content_data"
  },
  "location_coordinates": {
    "lat": "content_data",
    "lon": "content_data"
  },
  "location_details": {
    "altitude_meters": "content_data",
    "slope_degrees": "content_data",
    "aspect_degrees": "content_data",
    "aspect_cardinal": "content_data",
    "terrain_type": "content_data",
    "source": "content_data"
  },
  "satellite_wildfire_image": "content_data",
  "vegetation_distribution": "content_data"
}

agent_prompt = f'You are data collector agent, you will use your tool to extract weather from coordenates or from a location' \
'use your tools, web search and your knowledge to answer as best as possible, answer in this format {a_format}'

model = os.getenv("MODEL_DEPLOYMENT_NAME")
project_connection_string = os.getenv("PROJECT_CONNECTION_STRING")  


project_client = AIProjectClient.from_connection_string(
    credential= DefaultAzureCredential(),
    conn_str=project_connection_string,
)


with project_client:

    functions = FunctionTool(user_functions)
    
    toolset = ToolSet()
    toolset.add(functions)
   

    agent = project_client.agents.create_agent(
        model=model,
        name="Data-Collection-Agent",
        instructions=agent_prompt ,
        toolset=toolset,
    )
    # [END create_agent_toolset]
    print(f"Created agent, ID: {agent.id}")

    # Create thread for communication
    thread = project_client.agents.create_thread()
    print(f"Created thread, ID: {thread.id}")

    message = project_client.agents.create_message(
        thread_id=thread.id,
        role="user",
        content="what is the weather in Mexico",
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