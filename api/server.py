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
def api_get_master_volume():
    """Get master volume"""
    volume = client.get_master_volume()
    return jsonify({"volume": { "master": volume }})


@app.route('/api/volume/master', methods=['POST'])
def api_set_master_volume():
    """Set master volume"""
    params = request.get_json(force=True)
    result = client.set_master_volume(params['volume'])
    return jsonify({"volume": { "master": result }})



if __name__ == '__main__':
    app.run(debug=True)

