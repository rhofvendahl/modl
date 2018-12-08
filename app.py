from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

import spacy
nlp = spacy.load('en_core_web_sm')

import textacy

from allennlp.predictors import Predictor
print('loading predictor...')
# import os
# root_dir = os.path.dirname(os.path.abspath(__file__))
# config_path = os.path.join(root_dir, 'data/decomposable-attention-elmo-2018.02.19.tar.gz')
# predictor = Predictor.from_path('data/decomposable-attention.tar.gz')
print('done')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/update')
def update():
    text = request.args.get('text')
    return jsonify(text)

if __name__ == "__main__":
    app.run()
