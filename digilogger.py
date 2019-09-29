from time import strftime, localtime
from colored import fore, back, style, fg, bg, attr
import os

#Activate color mode.
os.system('')

# Color styling for terminal messages.
def time():
    return (fore.MAGENTA + strftime("%d %b %H:%M:%S | ", localtime()) + style.RESET)

def warn(message):
    print(time() + fore.YELLOW + message + style.RESET)

def crit(message):
    print(time() + back.RED + style.BOLD + message + style.RESET)

def test(message):
    print(time() + fore.BLUE + message + style.RESET)

def msg(message):
    print(time() + fg(51) + message + style.RESET)

def load(message):
    return (fg(238) + message + style.RESET)
