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
    # for entity in model_dict['entities']:
    #     print(type(entity['text']))
    #     print()
    # for s in model_dict['statements']:
    #     print(type(s['subject_text']))
    #     print(type(s['predicate_text']))
    #     print(type(s['object_text']))
    #     print()
    print('ent_length', len(model.doc.ents))
    for ent in model.doc.ents:
        print(ent.text, ent.label_)
    return jsonify({'model': model_dict})

if __name__ == "__main__":
    app.run()
