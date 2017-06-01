
import pytest

from matrix_config import MatrixConfig

def test_diff():
    """Test diffing"""
    m1 = MatrixConfig({
        'a': 'foo',
        'b': 'bar',
        'c': 42,
    })

    m2 = MatrixConfig({
        'a': 'foo',
        'b': 'baz',
    })

    diff = m1.diff(m2)

    assert diff.get('a') == None
    assert diff.get('b') == 'bar'
    assert diff.get('c') == 42

