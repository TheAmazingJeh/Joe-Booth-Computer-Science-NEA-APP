import sys, os, json, csv

from tkinter import Tk, Menu, Canvas                      # Import Base Tkinter class
from tkinter.constants import *                           # Import Tkinter constants
from tkinter.messagebox import showinfo, showerror, askyesno # Import Tkinter standard dialogs
from tkinter.filedialog import askopenfile, asksaveasfile # Import Tkinter file dialogs
from tkinter.font import Font, ITALIC                     # Import Tkinter fonts
# Import Tkinter widgets
from tkinter.ttk import Label, Button, Frame              # Import Tkinter widgets

from lib.local_lib.DoubleScrollFrame import DoubleScrolledFrame     # Import DoubleScrolledFrame class
from lib.MainFrames import WelcomeFrame, TaskFrame                  # Import MainContent classes
from lib.TaskHandler import NewTask                                 # Import TaskHandler classes
from lib.local_lib.classroom.Credfilegen import GenerateCredentials # Import Credfilegen class
from lib.local_lib.classroom.Classroom import Classroom             # Import Classroom class

class Window(Tk):
    """Main Window"""
    def __init__(self):
        
        super().__init__()
        self.appName = "The Organizer"                                              # Set the app name variable
        self.firstTime = False                                                 # Set firstTime to False
        self.tasks = []                                                        # Create a list to store tasks
        self.fileLocation = os.path.dirname(os.path.abspath(__file__))         # Get current directory
        self.Startup()                                                         # Run the startup function
        size = (800, 600)                                                      # Set the window size
        self.title(self.appName)                                                    # Set the window title
        self.geometry(f"{size[0]}x{size[1]}")                                               # Set the window size

        # Put all widgets in a scrollable frame
        self.scrollFrame = DoubleScrolledFrame(self, height=size[1]-20, width=size[0]-20)             
        self.scrollFrame.grid(row=0, column=0, sticky="nsew")                  # Put the scrollFrame in the window
    
        # Create a menu
        self.config(menu=self.Menu())


        # Create the frames
        self.welcomeFrame = WelcomeFrame(self.scrollFrame, 0, 0, appName=self.appName)
        self.taskFrame = TaskFrame(self.scrollFrame, 1, 0)
        
        

        self.frames = [self.welcomeFrame, self.taskFrame]

        # Select a frame to display
        if self.firstTime:
            self.welcomeFrame.PlaceText()
            self.welcomeFrame.Show()
            self.taskFrame.Show()
        else:
            self.tasks = json.load(open(self.fileLocation + "\\data\\tasks.json"))
            self.taskFrame.LoadTasks(self.tasks)
            self.ShowFrame(self.taskFrame)


        

    def Menu(self):
        """Create a menu"""
        menuBar = Menu(self)
        fileMenu = Menu(menuBar, tearoff=0)
        fileMenu.add_command(label="New Task", command=self.InvokeNewTask)
        fileMenu.add_command(label=("Link Classroom Account" if self.firstTime else "Sync Classroom Data"), command=self.ClassroomSync)

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
        self.ShowFrame(self.taskFrame)
        self.welcomeFrame.Hide()

    def ClassroomSync(self):
        doSync = askyesno("Sync Classroom Data", "This will sync your classroom data with the app. Do you want to continue? (this will take a while)")
        if doSync:
            # remove existing classroom tasks
            tasks = json.load(open(self.fileLocation + "\\data\\tasks.json"))
            
            i = 0
            while i < len(tasks):
                if tasks[i]['type'] == "classroom":
                    del tasks[i]
                else:
                    i += 1
            json.dump(tasks, open(self.fileLocation + "\\data\\tasks.json", "w"), indent=4)


            creds = GenerateCredentials(self.fileLocation)
            if creds == "ERR_CANCEL": showerror("Error", "You must link your account to continue"); return
            classroom = Classroom()
            self.title(f"{self.appName} - Syncing...")
            dat = classroom.get_all_data(creds, use_cache=False, remove_handed_in=True, remove_empty_courses=True)
            if dat["response"] == 200:
                existingFile = json.load(open(self.fileLocation + "\\data\\tasks.json"))
                for userClass in dat["data"]:
                    for assignment in userClass["coursework"]:
                        existingFile.append({
                            "title": assignment["title"],
                            "description": userClass["name"],
                            "dueDate": assignment["due_date"],
                            "id": f"gc{assignment['id']}",
                            "type": "classroom"
                        })
                json.dump(existingFile, open(self.fileLocation + "\\data\\tasks.json", "w"), indent=4)
                self.taskFrame.RefreshTasks(json.load(open(self.fileLocation + "\\data\\tasks.json")))
                showinfo("Success", "Successfully synced classroom data")
            self.title(self.appName)
        self.ShowFrame(self.taskFrame)
    def ShowFrame(self, frame: Frame):
        for item in self.frames: item.Hide()
        frame.Show()

if __name__ == "__main__":
  w = Window()
  w.mainloop()