import json
import time
import pickle
from sklearn.datasets import load_files

from nltk.stem import WordNetLemmatizer
import re

from sklearn.feature_extraction.text import TfidfVectorizer
from nltk.corpus import stopwords

from flask import jsonify
from flask import Flask, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

###### INIT CONSTANT
SEVERITY = ["Critical", "High", "Low", "Medium"]
TYPE = ["API", "Configuration/ DevOps", "Database", "UI", "UI logic"]

# load model
with open('data/bug_severity/bug_severity', 'rb') as severity_model:
    bug_severity_model = pickle.load(severity_model)

with open('data/bug_type/bug_type', 'rb') as type_model:
    bug_type_model = pickle.load(type_model)

# load data
bug_severity_data = load_files(r"data\bug_severity\train")
bug_type_data = load_files(r"data\bug_type\train")

############################### 

@app.route('/')
def hello():
    res = 'Hello, World!'

    return res

@app.route('/check-plagiarism', methods=['POST'])
def check_plagiarism():  
    record = json.loads(request.data)   
    SEARCH_TERM = record['search_term'] 

    ratio = 0
    
    
    res = jsonify({
                "data": SEARCH_TERM,
                "result": str(round(ratio, 4))
            })

    return res

if __name__=="__main__":
    app.run("0.0.0.0")