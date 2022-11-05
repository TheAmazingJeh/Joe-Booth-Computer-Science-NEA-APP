from tkinter import Tk, IntVar, StringVar, Menu, Canvas, font  # Import Base Tkinter class
from tkinter.constants import *                           # Import Tkinter constants
from tkinter.messagebox import showinfo                   # Import Tkinter standard dialogs
from tkinter.filedialog import askopenfile, asksaveasfile
from tkinter.font import Font, ITALIC                     # Import Tkinter fonts
# Import Tkinter widgets
from tkinter.ttk import Label, Labelframe, Button, Entry, OptionMenu, Frame, Checkbutton, Spinbox

class Task():
    def __init__(self, master: Frame, data: dict, fontTitle: Font, fontDefault: Font):
        self.taskFrame = Labelframe(master, width=150, text = f"ID - {data['id']}") # Create a frame for the task

        # Create the widgets
        self.title = Label(self.taskFrame, text=data["title"],font=fontTitle)
        self.description = Label(self.taskFrame, text=data["description"],font=fontDefault)
        self.taskType = Label(self.taskFrame, text=data["type"],font=fontDefault)

        # Pack the widgets
        self.taskFrame.pack(side=TOP, fill=X, expand=True, padx=5, pady=5) # Pack the frame
        self.title.pack(side=TOP, fill=X, expand=True)                     # Pack the title
        self.description.pack(side=TOP, fill=X, expand=True)               # Pack the description
        self.taskType.pack(side=TOP, fill=X, expand=True)                  # Pack the task type

    def Remove(self):
        self.taskFrame.pack_forget()
        self.title.pack_forget()
        self.description.pack_forget()

class CreateTaskPopup():
    pass # TODO: Create the popup