import requests
import sys,io
from openai import OpenAI
from src import model
from src import data
from src import constants
'''
import src.model as model
import src.data as data 
import src.constants as constants'''
import os
import pandas as pd

def extract_rels(files):
    OpenAI.api_key = os.environ["OPENAI_API_KEY"]
    client= OpenAI()
    responses=[]
    dfs=[]
    for documents in files:
        file=documents.filename
        if file[-4:] != ".pdf":
            return "Invalid"
        for text in data.read_file_text(io.BytesIO(documents.read()) ):
            print("entering model", text)
            response = model.get_response(client, text, constants.PROMPT, constants.MODEL_TYPE)
            print(response)
            responses.extend(response)
    return responses

    

