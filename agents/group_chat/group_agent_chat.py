from semantic_kernel import Kernel
import os
import asyncio
from semantic_kernel.connectors.ai.open_ai import AzureChatCompletion
from dotenv import load_dotenv
from semantic_kernel.planners import SequentialPlanner
from typing import Annotated
from semantic_kernel.functions.kernel_function_decorator import kernel_function
from azure.ai.projects import AIProjectClient
from azure.identity import DefaultAzureCredential
from azure.ai.projects.models import BingGroundingTool
from azure.ai.projects.models import FunctionTool, ToolSet, CodeInterpreterTool
from functions import user_functions


load_dotenv()
azure_openai_key = os.getenv("AZURE_OPENAI_API_KEY")
azure_openai_endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
azure_openai_deployment_name = os.getenv("AZURE_OPENAI_CHAT_COMPLETION_MODEL")
ai_project_connection_string = os.getenv("AI_PROJECT_CONNECTION_STRING")
bing_connection_name = os.getenv("BING_CONNECTION_NAME")


project_client = AIProjectClient.from_connection_string(
        credential=DefaultAzureCredential(),
        conn_str=ai_project_connection_string
        )


class Agents:
    @kernel_function(
        description="This function will be used to use an azure ai agent with web weather search",
        name="WebSearchAgent"
    )
    def data_collection_agent(
        self,
        query: Annotated[str, "Coordenates or location nam"]
        
    ) -> Annotated[str, "The response from  agent"]:
        functions = FunctionTool(user_functions)
        
        toolset = ToolSet()
        toolset.add(functions)

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


        collection_agent = project_client.agents.create_agent(
            model= os.getenv("MODEL_DEPLOYMENT_NAME"),
            name="Data-Collection-Agent",
            instructions= agent_prompt,
            toolset=toolset)
        
        thread = project_client.agents.create_thread()
            
        message = project_client.agents.create_message(
                thread_id=thread.id,
                role="user",
                content=query,
            )
            
        run = project_client.agents.create_and_process_run(thread_id=thread.id, assistant_id=collection_agent.id)
            
        messages = project_client.agents.list_messages(thread_id=thread.id)
        
        print("#DATA COLLECTION AGENT:")
        print(messages.data[0].content[0].text.value)
            
        return messages.data[0].content[0].text.value
        

    @kernel_function(
       description="This function will use an azure ai agent to create an evacuation route",
         name="NewsReporterAgent"
   )
    def evacuation_agent(
        self,
        weather_conditions: Annotated[str, "The location details"],
    ) -> Annotated[str, "the response from the  evacuation agent"]:

        agent = project_client.agents.create_agent(
        model=azure_openai_deployment_name,
        name="news-reporter",
        instructions="""You are a rescue assistant, you will search for traffic and routes from a wildfire evacuation""",
            headers={"x-ms-enable-preview": "true"},
        )
        
        thread = project_client.agents.create_thread()
            
        message = project_client.agents.create_message(
                thread_id=thread.id,
                role="user",
                content=f"""{weather_conditions}""",
            )
            
        run = project_client.agents.create_and_process_run(thread_id=thread.id, assistant_id=agent.id)
            
        messages = project_client.agents.list_messages(thread_id=thread.id)
        
        print("#EVACUATION AGENT:")
        print(messages.data[0].content[0].text.value)
            
        return messages.data[0].content[0].text.value

kernel = Kernel()

service_id = "default"

kernel.add_service(
    AzureChatCompletion(service_id=service_id,
                        api_key=azure_openai_key,
                        deployment_name=azure_openai_deployment_name,
                        endpoint = azure_openai_endpoint
    )
)

planner = SequentialPlanner(
    kernel,
    service_id
)

goal = f"get a route evacuation from Chapultepec"

async def call_planner():
    return await planner.create_plan(goal)

async def generate_answer(plan):
    return await plan.invoke(kernel)

async def main():
    sequential_plan = await call_planner()
    answer = await generate_answer(sequential_plan)
    print(answer)

