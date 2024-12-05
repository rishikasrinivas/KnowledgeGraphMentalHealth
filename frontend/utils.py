
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import sys, os
print(os.getcwd())
sys.path.append("../KnowledgeGraphMentalHealth/")
from src import constants
from pymongo.server_api import ServerApi
import uuid
def connect_to_db():
    uri=constants.MONGO_URI
    # Create a new client and connect to the server
    client = MongoClient(uri)
 
    collection_name = f"Brightside"
    
    collection = client[collection_name]['Rels']
    

    return collection
    
    
