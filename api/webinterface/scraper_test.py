

import pytest
from os import path

import scraper

def _read_sample_data(filename):
    """Helper to read sample data"""
    sample_path = path.dirname(__file__) + '/../../tests/data/' + filename

    with open(sample_path, 'r') as f:
        return f.read()


def test_parse_assigned_inputs():
    """Test assigned inputs extraction"""
    html = _read_sample_data("assigned_inputs.html")
    mapping = scraper.parse_assigned_inputs(html)


