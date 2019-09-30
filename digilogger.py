import os

from time import strftime, localtime
from colored import fore, back, style, fg

# Activate color mode
os.system("")

# Color styling for terminal messages
def time():
    return fore.MAGENTA + strftime("%d %b %H:%M:%S | ", localtime()) + style.RESET

def warn(message):
    print(time() + fore.YELLOW + str(message) + style.RESET)

def crit(message):
    print(time() + back.RED + style.BOLD + str(message) + style.RESET)

def test(message):
    print(time() + fore.BLUE + str(message) + style.RESET)

def msg(message):
    print(time() + fg(51) + str(message) + style.RESET)

def debug(message):
    print(time() + fore.LIGHT_GREEN + str(message) + style.RESET)

def load(message):
    print(fg(238) + str(message) + style.RESET)
