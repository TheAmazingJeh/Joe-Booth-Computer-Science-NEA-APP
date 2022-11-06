import json
from datetime import date
from random import randint

from tkinter import Tk, IntVar
from tkinter.constants import *                           # Import Tkinter constants
from tkinter.font import Font                     # Import Tkinter fonts
# Import Tkinter widgets
from tkinter.simpledialog import Dialog
from tkinter.ttk import Label, Labelframe, Entry, Frame, Checkbutton
from tkinter.messagebox import *

from lib.local_lib.tkcalendar.dateentry import DateEntry

class Task():
    def __init__(self, master: Frame, data: dict, fontTitle: Font, fontDefault: Font, fontItalic: Font):
        self.taskFrame = Labelframe(master, width=150, text = f"ID - {data['id']}") # Create a frame for the task

        # Create the widgets
        self.title = Label(self.taskFrame, text=data["title"],font=fontTitle)
        self.description = Label(self.taskFrame, text=data["description"],font=fontDefault)
        self.taskType = Label(self.taskFrame, text=data["dueDate"],font=fontItalic)

        # Pack the widgets
        self.taskFrame.pack(side=TOP, fill=X, expand=True, padx=5, pady=5) # Pack the frame
        self.title.pack(side=TOP, fill=X, expand=True, padx=5, pady=1)                     # Pack the title
        self.description.pack(side=TOP, fill=X, expand=True, padx=5, pady=1)               # Pack the description
        self.taskType.pack(side=TOP, fill=X, expand=True, padx=5, pady=1)                  # Pack the task type

    def Remove(self):
        self.taskFrame.pack_forget()
        self.title.pack_forget()
        self.description.pack_forget()

class SimpleTaskInput(Dialog):
    def body(self, master):
        self.title("New Task")
        Label(master, text="Task Title:").grid(row=0, sticky=E)
        self.title = Entry(master)
        self.title.grid(row=0, column=1, columnspan=2)
        Label(master, text="Task Description:").grid(row=1, sticky=E)
        self.description = Entry(master)
        self.description.grid(row=1, column=1, columnspan=2)

        dateToday = date.today()
        Label(master, text="Due Date:").grid(row=2, sticky=E)
        self.dueDate = DateEntry(master, width=12, background='grey',foreground='white', borderwidth=2, 
            year=dateToday.year, month=dateToday.month, day=dateToday.day)
        self.dueDate.grid(row=2, column=1)

        useDueDate = IntVar(value=1)
        self.dueDateCheck = Checkbutton(master, variable = useDueDate, onvalue = 1, offvalue = 0)
        self.dueDateCheck.grid(row=2, column=2)


        return

    def apply(self):

        # Block if title is empty
        if self.title.get() == "":
            return "TITLE_EMPTY"

        if self.dueDateCheck.instate(['selected']): # If the due date checkbox is checked
            dueDate = self.dueDate.get_date().strftime("%Y/%m/%d") # from m/d/y to y/m/d
        else: dueDate = None

        self.result = {
            "title": self.title.get(),
            "description": self.description.get(),
            "dueDate": dueDate # Y/m/d format
        }

        return

def NewTask(master: Tk, loc: str):
    while 1:
        d = SimpleTaskInput(master)
        if d.result != "TITLE_EMPTY": break              # If the user entered a title
        showwarning("New Task", "Title cannot be empty") # If the user didn't enter a title
    
    if d.result == None: return
    
    data = json.load(open(loc+"/data/tasks.json", "r"))


    # Produce a new ID
    while 1:
        ID = randint(111111111111, 999999999999)
        isid = False
        for item in data:
            if item["id"] == f"lt{ID}":
                isid = True
        if isid == False: break
                
        

    data.append({
        "id": f"lt{ID}",
        "title": d.result["title"],
        "description": d.result["description"],
        "dueDate": d.result["dueDate"],
        "type": "Simple"
    })

    json.dump(data, open(loc+"/data/tasks.json", "w"), indent=4)
        
    
    


if __name__ == "__main__":
    w = Tk()
    
    