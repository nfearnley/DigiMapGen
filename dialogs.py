from collections import abc

import tkinter
from tkinter import LEFT, W, E
from tkinter import Label, OptionMenu, StringVar
from tkinter import messagebox
from tkinter.simpledialog import Dialog, askinteger

from tileset import tileset


# Dialog for multiple choice dropdown (based on tkinter.simpledialog.askstring())
class ChooseDialog(Dialog):
    def __init__(self, title, prompt, options, defaultValue=None, parent=None):
        if not parent:
            parent = tkinter._default_root

        self.selected = None
        self.optionMenu = None

        self.prompt = prompt

        if not options:
            raise Exception("No options given")

        # If options is not a dict type, assume it's a list and convert it to a dict
        if isinstance(options, abc.Mapping):
            self.options = options
        else:
            self.options = {str(v): v for v in options}

        self.defaultValue = defaultValue

        Dialog.__init__(self, parent, title)

    def destroy(self):
        self.optionMenu = None
        self.selected = None
        Dialog.destroy(self)

    def body(self, master):
        self.selected = StringVar(master)

        w = Label(master, text=self.prompt, justify=LEFT)
        w.grid(row=0, padx=5, sticky=W)

        self.optionMenu = OptionMenu(master, self.selected, *self.options.keys())
        self.optionMenu.configure()
        self.optionMenu.grid(row=1, padx=1, sticky=W+E)

        if self.defaultValue:
            self.selected.set(str(self.defaultValue))

        return self.optionMenu

    def validate(self):
        try:
            result = self.getresult()
        except KeyError:
            messagebox.showwarning(
                "Illegal value",
                "Invalid choice\nPlease try again",
                parent=self
            )
            return 0

        self.result = result

        return 1

    def getresult(self):
        return self.options[self.selected.get()]

# Ask the user to choose from a list of options, return None if cancelled
def choose(title, prompt, options, defaultValue):
    d = ChooseDialog(title, prompt, options, defaultValue)
    return d.result


# Ask the user which generator they want to use, return None if cancelled
def chooseGenerator(generators):
    defaultValue = next(iter(generators))
    generator = choose("DigiMapGen", "Pick a generator:", generators, defaultValue)
    return generator


# Ask the user how many tiles across they want the map to be, return None if cancelled
def chooseMapwidth():
    mapwidth = askinteger("DigiMapGen", "Set map width:", initialvalue=10)
    return mapwidth


# Get turtle speed from user, return None if cancelled
def chooseSpeed():
    speed = choose("DigiMapGen", "Set speed:", ["slowest", "slow", "normal", "fast", "fastest", "instant"], defaultValue="slow")
    return speed


# Choose a map tile, return None if cancelled
def chooseTile():
    tileids = {t.name: t.id for t in tileset}
    tileid = choose("DigiMapGen", "What tile?:", tileids, "missing")
    return tileid
