from flask import Flask, request,render_template

from flask_cors import CORS

app = Flask(__name__)
CORS(app)
ALLOWED_EXTENSIONS = {'pdf'}
UPLOAD_FOLDER = 'Docs/'
DATA_FOLDER = 'Results/'

@app.route('/')
def home():
    return render_template('index.html')

def valid_file():
    pass

@app.route('/Docs', methods=['POST'])
def upload_files(): #calls get_relations and return jsonify(data), 200 if valid
    return [i.filename for i in request.files.getlist('files[]')]

def get_relations():  #json for data if valid else -1
    pass

if __name__ == '__main__':
    app.run(debug=True)


