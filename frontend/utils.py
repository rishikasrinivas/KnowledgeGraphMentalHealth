
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

from pymongo.server_api import ServerApi
import uuid
def connect_to_db(password):
    uri = f"mongodb+srv://rishika:{password}@cluster0.2eptsaa.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
    
    # Create a new client and connect to the server
    client = MongoClient(uri, server_api=ServerApi('1'))
    db =client.mydatabase
    collection_name = f"collection_rels_{uuid.uuid4().hex}"
    collection = client.mydatabase[collection_name]

    return collection
    
    
    