

"""
Helper functions
"""

import re

def round_halfstep(value):
    """Round value to 0.5 for half steps"""
    return round(value * 2.0) / 2.0


def pack_float(value):
    """Pack float value into 3 byte ascii"""
    result = "%02d" % value + str(value%1)[1:3]
    sval = re.sub(r'\D', '', result)
    return sval


def limit_range(minval, maxval, value):
    """Limit the value to a fixed range"""
    if value > maxval:
        value = maxval
    if value < minval:
        value = minval
    return value


def numeric_value(value):
    """Get numeric value from response"""
    sval = re.sub(r'\D', '', value)
    val = float(sval)
    if val > 100:
        val = val / 10.0
    return val
