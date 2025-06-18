

from azure.cosmos import CosmosClient 
from dotenv import dotenv_values
from models.active_points import ActivePoints
from models.data_collection_agent import DataCollectionAgent
from models.evacuation_agent import EvacuationAgent
from models.prediction_agent import PredictionAgent
from models.vulnerable_zones_agent import VulnerableZonesAgent


config = dotenv_values()

class CosmosDB:

    def __init__(self,database_name:str ='fire1'):
        self.cosmos_key = config.get('COSMOS_KEY')
        self.cosmos_url = config.get('COSMOS_URL')
        self.client = CosmosClient(self.cosmos_url, self.cosmos_key)
        self.database =  self.client.get_database_client(database_name)
    
    def get_collection_fields(self, collection:str):

        collections = {
            "active_points": ActivePoints,
            "data_collection_agent": DataCollectionAgent ,
            "evacuation_agent": EvacuationAgent,
            "prediction_agent": PredictionAgent,
            "vulnerable_zones_agent": VulnerableZonesAgent,
            }
        
        collection = collections.get(collection)

        return collection


    def get_document_by_id(self,id:str,collection:str):
        container = self.database.get_container_client(collection)
        collection_fields =  self.get_collection_fields(collection)
        iterable = container.query_items(query=f'SELECT * FROM {collection} c WHERE c.id="{id}"')
        item = next(iterable)
        return {key: item[key] for key in collection_fields.model_fields if key in item}

