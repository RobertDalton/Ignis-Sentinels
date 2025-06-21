

from fastapi import FastAPI

from db.cosmos_client import CosmosDB


app = FastAPI(
    title="Cosmos DB API - Collection Read Operations For Agents Data",
    description="A RESTful API with FastAPI to access documents from Cosmos DB.",
    version="1.0.0",
)

client = CosmosDB()

@app.get("/active_points/{id}")
async def read_book(id:str):
    id = str(id)
    data = client.get_document_by_id(id,'active_points')
    
    return data

@app.get("/data_collection_agent/{id}")
async def read_book(id:str):
    id = str(id)
    data = client.get_document_by_id(id,'data_collection_agent')
    
    return data


@app.get("/prediction_agent/{id}")
async def read_book(id:str):
    id = str(id)
    data = client.get_document_by_id(id,'prediction_agent')
    
    return data


@app.get("/vulnerable_zones_agent/{id}")
async def read_book(id:str):
    id = str(id)
    data = client.get_document_by_id(id,'vulnerable_zones_agent')
    
    return data

@app.get("/evacuation_agent/{id}")
async def read_book(id:str):
    id = str(id)
    data = client.get_document_by_id(id,'evacuation_agent')
    
    return data
