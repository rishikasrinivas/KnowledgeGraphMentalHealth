from openai import OpenAI
import pandas as pd
import src.constants as constants
import src.data as data
import os,json

def get_response(client, src_text : list, prompt_llm :str, model_type: str):
    '''
        client: OpenAI objected
        src_text: text model uses to extract relationships from
        prompt_llm: prompt llm uses as a basis for determining relationships
        model_type: version of gpt

        This function returns the results from the llm in the form of a list of dictionaries (with all items lowered)
    '''

    responses=[]
    prompt=f'Using this information: {src_text}, answer the following question: {prompt_llm}'


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
    resp = parse_response(chat_completion.choices[0].message.content)

    try:
        resp_list = json.loads(resp)
        for i in range(len(resp_list)):
            resp_list[i] = {k.lower(): v.lower() for k,v in resp_list[i].items()}
    except:
        return "Error"

    responses.extend(resp_list)
    return responses

def parse_response(response):
    '''
        response: response from the llm as a string

        The function takes the llm response which is a returns a list of dictionaries 
    '''
    start_idx=response.find('[')
    
    end_idx=response[start_idx:].find(']')
    while response[start_idx + end_idx-2] != '}':
        old=end_idx
        end_idx=response[start_idx+end_idx+1:].find(']')+old+1
                                                    
        

      
    response=response[start_idx:start_idx+end_idx+2]
    return response


def save_resp_as_df(response):
    '''
        This functions takes a response as a list of dictionaries and populates a dataframe
    '''
    df=pd.DataFrame()
    df=pd.concat([df, pd.DataFrame(response)])
    df=df.drop_duplicates(subset=['subj', 'rel', 'obj'], keep='first').reset_index().drop(columns= ['index'])

    return df
    


def main():
    OpenAI.api_key = os.environ["OPENAI_API_KEY"]
    client= OpenAI()
    responses=[]
    dfs=[]
    for documents in os.listdir(constants.DOCS_DIR):
        documents="Docs/" + documents
        if documents[-4:] != ".pdf":
            continue
        for text in data.read_file_text(documents):
            if text:
                response = get_response(client, text, constants.PROMPT, constants.MODEL_TYPE) 
                responses.extend(response)
                dfs.append(save_resp_as_df(response))
    pd.concat([df for df in dfs]).to_csv(constants.SAVE_FILE)


    

