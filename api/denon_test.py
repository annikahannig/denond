
import pytest

from tests.utils import read_sample_data

from webinterface import scraper
from matrix_config import MatrixConfig


def test_update_matrix_config__no_change():
    """Simulate matrix updating"""
    html = read_sample_data('assigned_inputs.html')
    data = read_sample_data('assigned_inputs.yml')

    current = MatrixConfig(scraper.parse_assigned_inputs(html))
    loaded = MatrixConfig().read(data)

    # The diff should be an empty dict
    diff = loaded.diff(current)

    assert diff.mapping == {}


