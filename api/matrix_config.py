
"""
Audiomatrix Configuration
--------------------------

Create an audiomatrix setup and map it to
query params sent to the web config interface.
"""

# Inputs:
INPUT_HDMI     = 'listHdmi'
INPUT_DIGITAL  = 'listDigital'
INPUT_ANALOG   = 'listAnalog'
INPUT_COMP     = 'listComp'
INPUT_VIDEO    = 'listVideo'

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



class MatrixConfig(object):
    """Represent the audiomatrix configuration"""

    def __init__(self):
        """Initialize new matrix"""
        inputs = [INPUT_HDMI, INPUT_DIGITAL, INPUT_ANALOG,
                  INPUT_COMP, INPUT_VIDEO]

        sources = [SOURCE_SAT_CBL, SOURCE_DVD, SOURCE_BLUERAY,
                   SOURCE_GAME, SOURCE_MEDIA_PLAYER, SOURCE_TV,
                   SOURCE_AUX, SOURCE_CD]

        mapping = {}

