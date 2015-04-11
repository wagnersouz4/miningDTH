from flask import Flask, render_template, redirect, jsonify, request, json
from flask.ext.cors import CORS, cross_origin
app = Flask(__name__)

cors = CORS(app, resources={r"/": {"origins": "*"}})
app.config['CORS_HEADERS'] = 'Content-Type'
app.secret_key = 'why would I tell you my secret key?'


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/bubble")
@cross_origin(origin='*',headers=['Content-Type','Authorization'])
def bubble():
    return render_template('bubble.html')

if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=int("8080"),
        debug=True
    )
