from openai import OpenAI
import pandas as pd
import constants
import data
import os

def get_response(client, src_text : list, prompt_llm :str, model_type: str):
    text = [txt for txt in src_text]
    final_resp = pd.DataFrame()
    for text in src_text:
        prompt=f'Using this information: {text}, answer the following question: {prompt_llm}'
    
        chat_completion=client.chat.completions.create(
            temperature = constants.TEMPERATURE,
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
        final_resp = pd.concat([final_resp, parse_response(chat_completion.choices[0].message.content)])
    return final_resp

def parse_response(response) -> pd.DataFrame:
    df =pd.DataFrame()
    start_idx=response.find('[')
    print(response)
    end_idx=response[start_idx:].find(']')
    while response[start_idx + end_idx-2] != '}':
        
      
        old=end_idx
        end_idx=response[start_idx+end_idx+1:].find(']')+old+1
                                                    
        

      
    response=response[start_idx:start_idx+end_idx+2]

    df=pd.concat([df, pd.DataFrame(eval(response))])
    df=df.drop_duplicates(subset=['subj', 'rel', 'obj'], keep='first').reset_index().drop(columns= ['index'])

    return df

def main():
    client= OpenAI( api_key= constants.API_KEY)
    file_text = []
    dfs=[]
    for documents in os.listdir(constants.DOCS_DIR):
        text =  data.read_file_text(documents)
        if text:
            print("Reading text from ", documents)
            file_text.append(text)
        
        response = get_response(client, file_text, constants.PROMPT, constants.MODEL_TYPE) 
        dfs.append(response)
    pd.concat([df for df in dfs]).to_csv(constants.SAVE_FILE)
main()
    