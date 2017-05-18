"""
Lightweight RESTful API server for the denon.
"""

from flask import Flask, jsonify, request

import denon

__version__ = "0.1.0"

app = Flask(__name__)


client = denon.Client("172.23.42.28")



@app.route('/')
def api_welcome():
    return "Denond API {}".format(__version__)


@app.route('/api/volume/master')
def api_master_volume():
    """Get and set master volume"""



if __name__ == '__main__':
    app.run(debug=True)

