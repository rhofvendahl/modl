from flask import Flask, render_template, request, jsonify

from modl import Model

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/model')
def model():
    text = request.args.get('text')
    model = Model(text)
    return jsonify({
        'names': [person.name for person in model.people],
        'resolved': model.resolved
    })

if __name__ == "__main__":
    app.run()
