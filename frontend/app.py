from flask import Flask, render_template, jsonify, request
import requests
from utils import connect_to_db
app = Flask(__name__)
from extract_relations import extract_rels
from urllib.parse import quote_plus

app = Flask(__name__)



   
collection = connect_to_db(password = quote_plus('k90t1ml6GXtFTvUK'))

@app.route('/')
def index():
    return render_template('index.html')

        
    

@app.route("/upload_results", methods=['POST'])
def upload_results():
    try:
        
        
        data=request.get_json()
        print("data ", data)
        collection.insert_many(data)
    
        return jsonify({
          'message': 'Data added',
        }), 201
    except:
        return jsonify({'error': str(e)}), 500
        
@app.route("/get_results", methods=['GET'])
def get_results():
    try:
        data=[]
        # Fetch all documents from the collection
        results = collection.find()
        for res in results:
        # Convert the results to a list of dictionaries
            res['_id'] = str(res['_id'])  # Convert ObjectId to string
            data.append(res)
        print(data)
  
        
        return jsonify(data), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
        
@app.route("/upload", methods=['POST'])
def upload_files():
    responses= extract_rels(request.files.getlist('files[]'))

    try:
        response = requests.post('http://127.0.0.1:5000/upload_results', json=responses)
        return jsonify({
          'message': 'Data added',
        }), 201
    except:
        return jsonify({'error': str(e)}), 500
   
if __name__ == '__main__':
    app.run(debug=True)
    
    
    
