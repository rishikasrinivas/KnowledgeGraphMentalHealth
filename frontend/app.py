from flask import Flask, render_template, jsonify, request

app = Flask(__name__)


from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from urllib.parse import quote_plus
from pymongo.server_api import ServerApi

app = Flask(__name__)

# Escape special characters in the username and password

password = quote_plus('k90t1ml6GXtFTvUK')
uri = f"mongodb+srv://rishika:{password}@cluster0.2eptsaa.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"

# Create a new client and connect to the server
client = MongoClient(uri, server_api=ServerApi('1'))

# Send a ping to confirm a successful connection
try:
    client.admin.command('ping')
    db =client.mydatabase
    collection = db.mycollection
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)
    

@app.route('/')
def index():
    return render_template('index.html')

@app.route("/upload_results", methods=['POST'])
def upload_results():
    #collection.delete_many({})
    try:
        data=request.get_json()
        print(data)
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
  
        
        return jsonify(data), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

   
if __name__ == '__main__':
    app.run(debug=True)
    
    
    
