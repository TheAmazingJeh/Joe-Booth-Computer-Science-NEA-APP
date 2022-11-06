from tkinter import Tk, IntVar, StringVar, Menu, Canvas, font  # Import Base Tkinter class
from tkinter.constants import *                           # Import Tkinter constants
from tkinter.messagebox import showinfo                   # Import Tkinter standard dialogs
from tkinter.filedialog import askopenfile, asksaveasfile
from tkinter.font import Font, ITALIC                     # Import Tkinter fonts
# Import Tkinter widgets
from tkinter.ttk import Label, Labelframe, Button, Entry, OptionMenu, Frame, Checkbutton, Spinbox
from datetime import datetime


# Import Task Object
from lib.TaskHandler import Task

class SimpleFrame():
    def __init__(self, master:Frame ,x: int, y: int):
        self.y = x                                                              # Set the x position
        self.x = y                                                              # Set the y position
        self.frame = Frame(master, width=150)                                  # Create a master frame
        self.frame.grid(row=self.y, column=self.x, sticky="nsew")              # Put the frame in the window

        # Set Fonts
        self.fontDefault = font.nametofont("TkDefaultFont")
        self.fontDefault.configure(family="Arial", size=9, weight=NORMAL)
        self.fontTitle = Font(family="Arial", size=15, weight=NORMAL)
        self.fontItalic = Font(family="Arial", size=9, weight=NORMAL, slant=ITALIC)

        self.Hide()

    def Hide(self):
        """Hides the frame (Grid Remove)"""
        self.frame.grid_remove()
    def Show(self): # Show the frame
        """Shows the frame (Grid)"""
        self.frame.grid()

class WelcomeFrame(SimpleFrame):
    def __init__(self, master:Frame ,x: int, y: int, appName = " "):
        super().__init__(master, x, y)
        self.appName = appName
        self.welcomeFrame = Frame(master)
        self.welcomeFrame.grid(row=self.y, column=self.x, sticky="nsew")

    def PlaceText(self):
        l1 = Label(self.welcomeFrame, text=f"Welcome to {self.appName}", font=self.fontTitle)
        l1.grid(row=0, column=0, sticky="nsew")
        l2 = Label(self.welcomeFrame, text="\nThis is a program to help you organize your work.")
        l2.grid(row=1, column=0, sticky="nsew")
        l3 = Label(self.welcomeFrame, text="To get started, click on the Options menu and select 'New Task'.")
        l3.grid(row=2, column=0, sticky="nsew")
        l4 = Label(self.welcomeFrame, text="")
        l4.grid(row=3, column=0, sticky="nsew")

class TaskFrame(SimpleFrame):
    def __init__(self, master:Frame ,x: int, y: int):
        super().__init__(master, x, y)         
        self.taskObjects = []
        self.allTaskFrame = Frame(master)
        self.allTaskFrame.grid(row=self.y, column=self.x, sticky="nsew")

    def LoadTasks(self, tasks: list):
        for item in tasks:
            self.taskObjects.append(Task(self.allTaskFrame, item, self.fontTitle, self.fontDefault, self.fontItalic))
    def ClearTasks(self):
        for i in range(len(self.taskObjects)):
            self.taskObjects[i].Remove()
        self.taskObjects.clear()
    
    def RefreshTasks(self, tasks: list):
        self.ClearTasks()
        self.LoadTasks(tasks)




if __name__ == "__main__":
    # Test welcome frame
    root = Tk()
    root.title("Test")
    root.geometry("500x500")

    welcomeFrame = WelcomeFrame(root, 0, 0, "Test")
    root.mainloop()
    print("\n\n\n\nRun main.py, this isn't it :/ .\n")
    pass