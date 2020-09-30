from tkinter import *
from tkinter import messagebox

from cryptography import exceptions

from random import SystemRandom

from crypto import *
from utils import *
from pm import *

# CONSTANTS 
DEFAULT_GEOMETRY = "300x350"
DEFAULT_TITLE = "new window"
DEFAULT_BG_COLOUR = "slate gray"

DEFAULT_LABEL_TITLE = "new label"
DEFAULT_LABEL_WIDTH = 200
DEFAULT_LABEL_HEIGHT = 1
DEFAULT_LABEL_BG = "light slate gray"

DEFAULT_ENTRY_TITLE = "new entry"
DEFAULT_ENTRY_WIDTH = 200
DEFAULT_ENTRY_HEIGHT = 1
DEFAULT_LABEL_BG = "light grey"

DEFAULT_BUTTON_TITLE = "new button"
DEFAULT_BUTTON_WIDTH = 30
DEFAULT_BUTTON_HEIGHT = 1
DEFAULT_BUTTON_BG = "dark slate gray"

DEFAULT_FONT = "Consolas"
DEFAULT_FONT_SIZE = 12

class newWindow:
    
    

    def __init__(self, parent = None, title = DEFAULT_TITLE, geometry = DEFAULT_GEOMETRY, bg=DEFAULT_BG_COLOUR):
        
        if parent == None:
            # root
            self.window = Tk()
            self.parent = None
            
        else:
            self.window = Toplevel(parent.window)
            self.parent = parent.window
        
        self.window.title(title)
        self.window.geometry(geometry)
        self.window.configure(bg=bg)

        self.buttons = list()
        self.labels = list()
        self.entries = list()

        self.addLabel(text=title, font_size=15)

    def isRoot(self):
        return self.parent == None

    def addButton(self, bg=DEFAULT_BUTTON_BG,text=DEFAULT_BUTTON_TITLE, width=DEFAULT_BUTTON_WIDTH, height=DEFAULT_BUTTON_HEIGHT, command=None):
        b = Button(self.window, bg=bg, text=text, width=width, height =height, command=command)
        b.pack()
        self.buttons.append(b)
        return b
    
    def addLabel(self, bg=DEFAULT_LABEL_BG,text=DEFAULT_LABEL_TITLE, width=DEFAULT_LABEL_WIDTH, height=DEFAULT_LABEL_HEIGHT, font=DEFAULT_FONT, font_size=DEFAULT_FONT_SIZE):
        l = Label(self.window, text=text, bg=bg, width=width, height=height, font=(font, font_size))
        l.pack()
        self.labels.append(l)
        return l

    def addListbox(self, *data : list):
        l = Listbox(self.window)
        l.insert(END, *data)
        l.pack()
        return l
    
    def addEntry(self, text="", hidden=False, width=DEFAULT_ENTRY_WIDTH):
        if hidden:
            show = "*"
        else:
            show = ""

        e = Entry(self.window, show=show, width = width,justify=CENTER)
        e.insert(0, text)
        e.pack()
        
        return e


    def leaveBlank(self, size=1):
        self.addLabel(text="", height=size, bg=self.window["bg"])
    
    def destroy(self):
        self.window.destroy()

    def center(self):
        #root.window.eval('tk::PlaceWindow %s center' % self.window.winfo_pathname(self.window.winfo_id()))

        positionRight = int(self.window.winfo_screenwidth()/2 - self.window.winfo_reqwidth()/2)
        positionDown = int(self.window.winfo_screenheight()/2 - self.window.winfo_reqheight()/2)
        
        self.window.geometry("+{}+{}".format(positionRight, positionDown))
    
    def mainloop(self):
        if self.isRoot():
            self.window.mainloop()
        else:
            raise RuntimeError("trying to mainloop a topLevel").with_traceback()