from enum import Enum, auto

class SystemState(Enum):
    '''
    A class that define the system current state
    '''
    OCCUPIED = auto() # State: the room is occupied
    IDLE = auto() # State: the room is not occupied and enter energy saving mode
    PRE_COOLING = auto() # State: pre cooling is undergoing
    PRE_COOLING_FINISH = auto()
    ERROR = auto() # State: Error state to log (not occupied even the estimated time passed)
