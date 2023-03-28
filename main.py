import json
import time
import pickle
import pandas as pd
from sklearn.datasets import load_files

from nltk.stem import WordNetLemmatizer
import re

from sklearn.feature_extraction.text import TfidfVectorizer
from nltk.corpus import stopwords

from flask import jsonify
from flask import Flask, request
from flask_cors import CORS

from utils import *
from plagiarism_detection import *

app = Flask(__name__)
CORS(app)

###### INIT CONSTANT
SOURCE = '../data/_vie.json'
n = 4 # set ngram number
threshold_ngram = 0.7
threshold_lcs_cs = 0.54
threshold_fuzzy = 0.6

# load data
source_data = pd.read_json(SOURCE)[0]

############################### 

@app.route('/')
def hello():
    res = 'Hello, World!'

    return res

@app.route('/check-plagiarism', methods=['POST'])
def check_plagiarism():  
    record = json.loads(request.data)   
    SEARCH_TERM = record['search_term']

    test_data = []
    test_data.append(SEARCH_TERM)

    ratio = 0
    
    # preprocessing
    test_data = preprocessing(test_data)

    for doc in test_data:
        ratio = plagiarism_detection(source_data, doc, n, threshold_ngram, threshold_lcs_cs, threshold_fuzzy)
        # if temp == 0:
        #     ewp.append(doc)
        # tp_exact += temp
    
    
    res = jsonify({
                "data": SEARCH_TERM,
                "result": str(round(ratio, 4))
            })

    return res

if __name__=="__main__":
    app.run("0.0.0.0")