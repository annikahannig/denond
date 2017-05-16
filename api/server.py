"""
Lightweight RESTful API server for the denon.
"""

from flask import Flask, jsonify, request

__version__ = "0.1.0"

app = Flask(__name__)


@app.route('/')
def api_welcome():
    return "Denond API {}".format(__version__)




if __name__ == '__main__':
    app.run(debug=True)

