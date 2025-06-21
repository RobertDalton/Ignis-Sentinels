
import os
from azure.ai.projects import AIProjectClient
from azure.ai.projects.models import FunctionTool, ToolSet, CodeInterpreterTool
from azure.identity import DefaultAzureCredential
from functions import user_functions
from dotenv import load_dotenv

load_dotenv()

e_format = {
  "message": "content",
  "spread": {
     "route": "content",
     "accuracy": "",
  }
}

s_format =  {
  "spread": {
    "gif_link": "content",
  }
}

agent_prompt = f'You will perform  web and db search and the best of your knowledge to answer as best as possible, answer in this format {e_format}'

model = os.getenv("MODEL_DEPLOYMENT_NAME")
project_connection_string = os.getenv("PROJECT_CONNECTION_STRING")  


project_client = AIProjectClient.from_connection_string(
    credential= DefaultAzureCredential() ,
    conn_str=project_connection_string,
)


with project_client:

    functions = FunctionTool(user_functions)
    
    toolset = ToolSet()
    toolset.add(functions)
   

    agent = project_client.agents.create_agent(
        model=model,
        name="Evacuation-Agent",
        instructions=agent_prompt ,
        toolset=toolset,
    )
    print(f"Created agent, ID: {agent.id}")

    # Create thread for communication
    thread = project_client.agents.create_thread()
    print(f"Created thread, ID: {thread.id}")

    message = project_client.agents.create_message(
        thread_id=thread.id,
        role="user",
        content="Mexico",
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