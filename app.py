from flask import Flask, render_template, request, jsonify

from modl import Model

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/model')
def model():
    text = request.args.get('text')
    print(text)
    model = Model(text)
    data = {
        'names': [person.name for person in model.people],
        'resolved': model.resolved
    }
    # print(model.doc.text)
    # print([person.name for person in model.people])
    # probably unnecessary, tracking a bug
    # can model or people persist through calls?
    # if the calls are close together?
    for person in model.people:
        del person
    del model

    return jsonify(data)


if __name__ == "__main__":
    app.run()
