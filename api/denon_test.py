
import pytest

import matrix_config

from tests.utils import read_sample_data
from webinterface import scraper



def test_update_matrix_config__no_change():
    """Simulate matrix updating with no change"""
    html = read_sample_data('assigned_inputs.html')
    data = read_sample_data('assigned_inputs.yml')

    current = matrix_config.MatrixConfig(scraper.parse_assigned_inputs(html))
    loaded = matrix_config.MatrixConfig().read(data)

    # The diff should be an empty dict
    diff = loaded.diff(current)

    assert diff.mapping == {}


def test_update_matrix_config__all_off():
    """Simulate updating with all changed to off"""
    html = read_sample_data('assigned_inputs.html')
    data = read_sample_data('all_off.yml')

    current = matrix_config.MatrixConfig(scraper.parse_assigned_inputs(html))
    loaded = matrix_config.MatrixConfig().read(data)

    diff = loaded.diff(current)

    expected = [
        (matrix_config.INPUT_HDMI,
         matrix_config.SOURCE_SAT_CBL,
         matrix_config.OFF),

        (matrix_config.INPUT_HDMI,
         matrix_config.SOURCE_GAME,
         matrix_config.OFF),

        (matrix_config.INPUT_DIGITAL,
         matrix_config.SOURCE_BLUERAY,
         matrix_config.OFF),

        (matrix_config.INPUT_ANALOG,
         matrix_config.SOURCE_MEDIA_PLAYER,
         matrix_config.OFF),

        (matrix_config.INPUT_COMP,
         matrix_config.SOURCE_GAME,
         matrix_config.OFF),
    ]


    unexpected = [
        (matrix_config.INPUT_VIDEO,
         matrix_config.SOURCE_GAME,
         matrix_config.OFF),
    ]


    for (inp, source, val) in expected:
        assert diff.mapping.get(
            matrix_config.assign_input_source_key(inp, source)) == val

    for (inp, source, val) in unexpected:
        assert diff.mapping.get(
            matrix_config.assign_input_source_key(inp, source)) == None
