from enum import Enum

class SafetyMonitor(Enum):
    FORCE_SLIP   = 1
    TACTILE_SLIP = 2
    FUSED_SLIP   = 3
    NO_SELECTION = 4


class Sensors(Enum):
    FORCE_SENSOR   = 1
    TACTILE_SENSOR = 2
    FORCE_TACTILE_SENSORS = 3
    NO_SELECTION = 4

#The need for this has to be verified
class Platforms(Enum):
    INTEL = 1
    AMD = 2
    NXP = 3
    NVIDIA = 4
    NO_SELECTION = 5