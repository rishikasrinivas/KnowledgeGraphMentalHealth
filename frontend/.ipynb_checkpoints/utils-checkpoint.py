
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

from pymongo.server_api import ServerApi
import uuid
def connect_to_db():
    uri="mongodb://127.0.0.1:27017/"
    
    # Create a new client and connect to the server
    client = MongoClient(uri)
    print("DATABASES =====================\n", client.list_database_names())
 
    collection_name = f"Brightside"
    
    collection = client[collection_name]['Rels']
    
    print(collection)

    return collection
    
    
