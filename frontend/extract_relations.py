import requests
import sys,io
from openai import OpenAI
from src import model
from src import data
from src import constants
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
            return f"You uploaded and invalid file type {file[-4:]}. Please reupload your files ensuring they are all pdf forms!"
            
        for text in data.read_file_text(io.BytesIO(documents.read()) ):
            response = model.get_response(client, text, constants.PROMPT, constants.MODEL_TYPE)
            responses.extend(response)
    return responses

    

