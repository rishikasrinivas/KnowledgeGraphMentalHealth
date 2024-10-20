import requests
import sys
from openai import OpenAI
sys.path.append("/Users/rishikasrinivas/KnowledgeGraphMentalHealth/")
import src.model as model
import src.data as data 
import src.constants as constants
import os

def main():
    client= OpenAI( api_key= constants.API_KEY)
    file_text = []
    responses=[]
    dfs=[]
    for documents in os.listdir(constants.DOCS_DIR):
        text =  data.read_file_text(documents)
        if text:
            print("Reading text from ", documents)
            file_text.append(text)
        
        response = model.get_response(client, file_text, constants.PROMPT, constants.MODEL_TYPE) 
        responses.extend(response)
        break
    print(responses)
    return responses
#responses = main()
    

    
# Send a POST request to the Flask endpoint
#response = requests.post('http://127.0.0.1:5000/upload_results', json=responses)
response = requests.get('http://127.0.0.1:5000/get_results')
print(response.json())    