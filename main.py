import sys, os, json, csv

from tkinter import Tk, Menu, Canvas                      # Import Base Tkinter class
from tkinter.constants import *                           # Import Tkinter constants
from tkinter.messagebox import showinfo                   # Import Tkinter standard dialogs
from tkinter.filedialog import askopenfile, asksaveasfile # Import Tkinter file dialogs
from tkinter.font import Font, ITALIC                     # Import Tkinter fonts
# Import Tkinter widgets
from tkinter.ttk import Label, Button, Frame              # Import Tkinter widgets

from lib.local_lib.DoubleScrollFrame import DoubleScrolledFrame     # Import DoubleScrolledFrame class
from lib.MainFrames import WelcomeFrame, TaskFrame                  # Import MainContent classes
from lib.TaskHandler import NewTask                         # Import TaskHandler classes


class Window(Tk):
    """Main Window"""
    def __init__(self):
        
        super().__init__()
        appName = "The Organizer"                                              # Set the app name variable
        self.firstTime = False                                                 # Set firstTime to False
        self.tasks = []                                                        # Create a list to store tasks
        self.fileLocation = loc = os.path.dirname(os.path.abspath(__file__))   # Get current directory
        self.Startup()                                                         # Run the startup function
        size = (800, 600)                                                      # Set the window size
        self.title(appName)                                                    # Set the window title
        self.geometry(f"{size[0]}x{size[1]}")                                               # Set the window size

        # Put all widgets in a scrollable frame
        self.scrollFrame = DoubleScrolledFrame(self, height=size[1]-20, width=size[0]-20)             
        self.scrollFrame.grid(row=0, column=0, sticky="nsew")                  # Put the scrollFrame in the window
    
        # Create a menu
        self.config(menu=self.Menu())

        # Create the frames
        self.welcomeFrame = WelcomeFrame(self.scrollFrame, 0, 1, appName=appName)
        self.taskFrame = TaskFrame(self.scrollFrame, 0, 0)
        
        

        self.frames = [self.welcomeFrame, self.taskFrame]

        # Select a frame to display
        if self.firstTime:
            self.welcomeFrame.PlaceText()
            self.ShowFrame(self.welcomeFrame)
        else:
            self.tasks = json.load(open(loc + "\\data\\tasks.json"))
            self.taskFrame.LoadTasks(self.tasks)
            self.ShowFrame(self.taskFrame)


        

    def Menu(self):
        """Create a menu"""
        menuBar = Menu(self)
        fileMenu = Menu(menuBar, tearoff=0)
        fileMenu.add_command(label="New Task", command=self.InvokeNewTask)
        fileMenu.add_command(label="Link to Classroom", command=None)

        fileMenu.add_separator()
        fileMenu.add_command(label="Exit", command=self.quit)

        menuBar.add_cascade(label="Options", menu=fileMenu)
        return menuBar # Return the menu

    def Startup(self):
        # Check if the user has already used the app
        if not os.path.exists(self.fileLocation + "\\data"): os.mkdir(self.fileLocation + "\\data") # Create the data folder
        if not os.path.exists(self.fileLocation + "\\data\\tasks.json"):                            # Check if the tasks file exists
            with open(self.fileLocation + "\\data\\tasks.json", "w") as f:                           # Create the tasks file
                json.dump([], f)                                                                      # Write an empty list to the file 
            self.firstTime = True                                                                    # Set firstTime to True
        if json.load(open(self.fileLocation + "\\data\\tasks.json")) == []:                        # Check if the tasks file is empty
            self.firstTime = True                                                                   # Set firstTime to True
            
    def InvokeNewTask(self):
        NewTask(self, self.fileLocation) 
        self.taskFrame.RefreshTasks(json.load(open(self.fileLocation + "\\data\\tasks.json")))

    def ShowFrame(self, frame: Frame):
        for item in self.frames: item.Hide()
        frame.Show()

if __name__ == "__main__":
  w = Window()
  w.mainloop()