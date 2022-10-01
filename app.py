from flask import Flask, render_template, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
cors = CORS(app)

# Create the receiver API POST endpoint:


@app.route("/receiver", methods=["POST"])
def postME():
    data = request.get_json()
    data = jsonify(data)
    return data


@app.route('/')
def index():
    return render_template('index.html')
