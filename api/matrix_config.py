
"""
Audiomatrix Configuration
--------------------------

Create an audiomatrix setup and map it to
query params sent to the web config interface.
"""

# Inputs:
INPUT_HDMI     = 'Hdmi'
INPUT_DIGITAL  = 'Digital'
INPUT_ANALOG   = 'Analog'
INPUT_COMP     = 'Comp'
INPUT_VIDEO    = 'Video'

# Sources:
SOURCE_SAT_CBL      = 'SAT/CBL'
SOURCE_DVD          = 'DVD'
SOURCE_BLUERAY      = 'BD'
SOURCE_GAME         = 'GAME'
SOURCE_MEDIA_PLAYER = 'MPLAY'
SOURCE_TV           = 'TV'
SOURCE_AUX          = 'AUX1'
SOURCE_CD           = 'CD'

# HDMI inputs:
HDMI_1     = 'HD1'
HDMI_2     = 'HD2'
HDMI_3     = 'HD3'
HDMI_4     = 'HD4'
HDMI_5     = 'HD5'
HDMI_6     = 'HD6'
HDMI_FRONT = 'HD7'
HDMI_OFF   = 'OFF'

# DIGITAL Inputs
DIGITAL_COAX = 'CO1'
DIGITAL_OPT  = 'OP1'
DIGITAL_OFF  = 'OFF'

# COMP inputs
COMP_IN  = 'IN1'
COMP_OFF = 'OFF'

# VIDEO inputs
VIDEO_1   = 'VD1'
VIDEO_2   = 'VD2'
VIDEO_OFF = 'OFF'

# General off
OFF = 'OFF'


class MatrixConfig(object):
    """Represent the audiomatrix configuration"""

    def __init__(self):
        """Initialize new matrix"""
        self.inputs = [INPUT_HDMI, INPUT_DIGITAL, INPUT_ANALOG,
                       INPUT_COMP, INPUT_VIDEO]

        self.sources = [SOURCE_SAT_CBL, SOURCE_DVD, SOURCE_BLUERAY,
                        SOURCE_GAME, SOURCE_MEDIA_PLAYER, SOURCE_TV,
                        SOURCE_AUX, SOURCE_CD]

        self.mapping = {"list{}Assign{}".format(inp, source): OFF
                        for source in self.sources
                        for inp    in self.inputs}


    def set_input(source, inp):
        """Assign input to source"""
        key = "list{}Assign{}".format(inp, source)
        self.mapping[key] = inp
