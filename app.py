#!/usr/bin/python
import sys, os
sys.path.insert(0, os.environ['VORTAN']+'/src/')
from flask import Flask, jsonify, request, abort
from spellchecker import *

app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello, World!'

@app.route('/correct/<string:word>', methods=['GET'])
def correct(word):
    response = {
        "word": word
    }
    correct = sp.isCorrect(word)
    response["correct"] = correct
    if not correct:
        response["suggestions"] = sp.correct(word, 3)
    return jsonify(response), 201

if __name__ == '__main__':
    freq_dict_file = os.environ['VORTAN'] + '/db/freq_dict.txt'
    corr_dict_file = os.environ['VORTAN'] + '/db/corr_dict.txt'
    print("Reading dictionary...")
    freq_dict, corr_dict = train(freq_dict_file, corr_dict_file)
    print("Initializing spellchecker...")
    sp = spellchecker(fwords=freq_dict, cwords=corr_dict)
    app.run(debug=True)
