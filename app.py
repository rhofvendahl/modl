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
        'text': model.doc.text,
        'resolved_text': model.resolved_text,
        'people': []
    }
    for person in model.people:
        person_dict = {
            'name': person.name,
            'statements': []
        }
        for entity, cue, fragment in person.statements:
            statement_dict = {
                'entity': entity.text,
                'cue': cue.text,
                'fragment': fragment.text
            }
            person_dict['statements'] += [statement_dict]
        model_dict['people'] += [person_dict]
    return jsonify({'model': model_dict})

if __name__ == "__main__":
    app.run()
