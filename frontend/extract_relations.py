import requests
import sys,io
from openai import OpenAI
sys.path.append("/Users/rishikasrinivas/KnowledgeGraphMentalHealth/")
import src.model as model
import src.data as data 
import src.constants as constants
import os

def extract_rels(files):
    client= OpenAI( api_key= constants.API_KEY)
    file_text = []
    responses=[]
    dfs=[]
    for documents in files:
        file=documents.filename
        if file[-4:] != ".pdf":
            return "Inv"
        text =  data.read_file_text(io.BytesIO(documents.read()) )
        if text:
            print("Reading text from ", documents)
            file_text.append(text)
        print("entering model")
        response = model.get_response(client, file_text, constants.PROMPT, constants.MODEL_TYPE)
        print(response)
        responses.extend(response)
        break
    print(responses)
    return responses

    

