from enum import Enum

# Using ANS coding for color 
class Color(Enum):
    RED = '\33[91m'
    GREEN = '\33[92m'
    YELLOW = '\33[93m'
    BLUE = '\33[94m'
    PURPLE ='\33[95m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    END = '\033[0m'
    CENTER = '\033[2m'