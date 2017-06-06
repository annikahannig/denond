
from os import path

def read_sample_data(filename):
    """Helper to read sample data"""
    sample_path = path.dirname(__file__) + '/../../tests/data/' + filename

    with open(sample_path, 'r') as f:
        return f.read()
