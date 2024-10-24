from openai import OpenAI
import pandas as pd
import constants
import data
import os

def get_response(client, src_text : str, prompt_llm :str, model_type: str):
    prompt=f"Using this information: {src_text}, answer the following question: {prompt_llm}"

    chat_completion=client.chat.completions.create(
        temperature = 0.2,
        messages=[
            {
                "role": "system",
                "content": prompt_llm,
                },
            {
                "role": "user",
                "content": prompt,
                }
            ],
        model= model_type,
    )
    resp=chat_completion.choices[0].message.content
    return resp

def parse_response(response) -> pd.DataFrame:
    df =pd.DataFrame()
    
    start_idx=response.find("data = ")
    
    if response[start_idx+7] == '[':
        end_idx=response[start_idx:].find(']')
    else:
        end_idx=response[start_idx:].find('}')
        
    response=response[start_idx+7:start_idx+end_idx+1]
    
    df=pd.concat([df, pd.DataFrame(eval(response))])
    df=df.drop_duplicates(subset=['subj', 'obj', 'rel'], keep='first')
    return df

def main():
    client= OpenAI( api_key= constants.API_KEY)
    file_text = ''
    for documents in os.listdir(constants.DOCS_DIR):
        text =  data.read_file_text(documents)
        if text:
            file_text += data.read_file_text(documents)
    response = get_response(client, file_text, constants.PROMPT, constants.MODEL_TYPE)
    triplet_dataframe = parse_response(response)
    print(triplet_dataframe)
main()
    