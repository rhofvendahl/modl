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
predictor = Predictor.from_path('data/decomposable-attention-elmo-2018.02.19.tar.gz')
print('done')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/parse')
def parse():
    query = request.args.get('query')
    doc = nlp(query)

    sentences = [sent.text for sent in doc.sents]
    predictions = []

    premise_n = 0
    for premise in doc.sents:
        hypothesis_n = 0
        for hypothesis in doc.sents:
            if (premise != hypothesis):
                prediction = predictor.predict(hypothesis=hypothesis.text, premise = premise.text)
                entailment, contradiction, neutral = prediction['label_probs']
                predictions += {
                    'premise': premise_n,
                    'hypothesis': hypothesis_n,
                    'entailment': entailment,
                    'contradiction': contradiction,
                    'neutral': neutral
                    }
            hypothesis_n += 1
        premise_n += 1
    return jsonify({'sentences': sentences, 'predictions': predictions})

if __name__ == "__main__":
    app.run()
