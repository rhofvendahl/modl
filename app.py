from flask import Flask, render_template, request, jsonify
from modl import Model

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/model', methods = ['POST'])
def model():
    content = request.get_json()
    model = Model(content['text'])

    model_dict = {
        'entities': [{
            'id': entity.id,
            'text': entity.text,
            'class': entity.class_
        } for entity in model.entities],
        'statements': [{
            'id': statement.id,
            'subject_text': statement.subject_text,
            'subject_id': statement.subject_id,
            'predicate_text': statement.predicate_text,
            'object_text': statement.object_text,
            'object_id': statement.object_id,
            'weight': statement.weight
        } for statement in model.statements],
    }
    return jsonify({'model': model_dict})

if __name__ == "__main__":
    app.run()
