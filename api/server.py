"""
Lightweight RESTful API server for the denon.
"""
import os
import sys
import signal
import atexit

import requests

from flask import Flask, jsonify, request

import denon
import matrix_config_manager

__version__ = "0.1.0"

app = Flask(__name__)

host = '172.23.42.28'

client = denon.Client(host)

config_manager = matrix_config_manager.ConfigManager()

def shutdown_server(sig, frame):
    """Stop services"""
    print("Stopping server")
    config_manager.terminate()
    print("Exiting")
    sys.exit(0)


def _config_name_from_file(f):
    """Only get the filename, strip yml"""
    return os.path.basename(f).replace('.yml', '')


@app.errorhandler(denon.AmpOfflineException)
def handle_amp_offline(err):
    response = jsonify({"error": "amp offline"})
    response.status_code = 500
    return response

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


@app.route("/api/mainzone/state")
def get_main_zone_state():
    """Get main zone status"""
    result = client.get_main_zone_state()
    return jsonify({"state": result})


@app.route("/api/matrix-config/upload-state")
def get_config_upload_state():
    result = config_manager.get_upload_state()
    return jsonify({"state": result})


@app.route("/api/matrix-config/configs")
def get_audio_matrix_configs():
    result = config_manager.list_configurations()
    _, current_filename = config_manager.get_current_matrix_config()
    current_config_name = _config_name_from_file(current_filename)

    files = [{'id': i,
              'name': _config_name_from_file(f),
              'selected': _config_name_from_file(f) == current_config_name}
             for i, f in enumerate(result)]




    return jsonify({"configs": files})


@app.route("/api/matrix-config/configs", methods=['POST'])
def select_audio_matrix_config():
    params = request.get_json(force=True)
    fileid = params['id']

    files = config_manager.list_configurations()
    config_file = files[fileid]

    # Upload matrix config
    res = config_manager.upload(config_file)
    return jsonify({'state': res})



if __name__ == '__main__':
    signal.signal(signal.SIGINT, shutdown_server)
    config_manager.spawn(host)
    app.run(debug=False)


