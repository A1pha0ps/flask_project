from flask import Flask, render_template, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
cors = CORS(app)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0

# No cacheing at all for API endpoints.
@app.after_request
def add_header(response):
    response.cache_control.no_store = True
    if 'Cache-Control' not in response.headers:
        response.headers['Cache-Control'] = 'no-store'
    return response

# Create the receiver API POST endpoint:
@app.route("/receiver", methods=["POST"])
def postME():
    data = request.get_json()
    data = jsonify(data)
    return data


@app.route('/')
def index():
    return render_template('index.html')