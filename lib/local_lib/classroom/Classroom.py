from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import os, json, datetime

loc = os.path.dirname(os.path.realpath(__file__))

SCOPES = [
    "https://www.googleapis.com/auth/classroom.rosters.readonly",
    "https://www.googleapis.com/auth/classroom.courses.readonly",
    "https://www.googleapis.com/auth/classroom.coursework.me"
    ]

class Classroom:
    def __init__(self):
        self.log = False
        self.log_timer = False
        self.log_start = datetime.datetime.now()
        self.current_date = "None"
        self._construct_current_date()
    def _log(self, text, end="\n"):
        """Logs text to the console"""
        if self.log: print(text, end=end)
    def _construct_current_date(self):
        """Creates the current date in the format YY/MM/DD
        """
        d = datetime.datetime.now()
        d = d.strftime("%Y/%m/%d")
        self.current_date = d
    def _compare_time(self, date):
        """Returns the difference between the current time and the due time as an integer

        Args:
            date (dict): Due date (YY/MM/DD)
        """
        return (datetime.datetime.strptime(date, "%Y/%m/%d") - datetime.datetime.strptime(self.current_date, "%Y/%m/%d")).days

    def _classroom_api_get_enrolled_courses(self, creds):
        """Returns a list of courses the user has access to (course id)

        Args:
            creds (Credentials): Credentials for the service account
        """
        try:
            service = build("classroom", "v1", credentials=creds)
            # Call the Classroom API
            self._log("Getting enrolled courses...",end="\r")
            results = service.courses().list().execute()
            self._log("Getting enrolled courses... Done!")
            courses = results.get("courses", [])

            if not courses:
                return { # Return an empty dict if there are no current pieces of coursework
                    "response":200,
                    "courses":False,
                    "data":None
                }
            else:
                return { # Return the current pieces of coursework if there are any
                    "response":200,
                    "courses":True,
                    "data":courses
                }

        except HttpError as error:
            return { # Return an error if there is one
                    "response":400,
                    "courses":False,
                    "data":None,
                    "error":error
                }
    def get_enrolled_courses(self, creds):
        """Returns a list of courses the user has access to (course id)"""
        api_response =  self._classroom_api_get_enrolled_courses(creds)
        response = {
            "response":200,
            "courses":True,
            "data":[]
        }
        for item in api_response["data"]:
            if item["courseState"] == "ACTIVE":
                response["data"].append(
                    {
                        "id":item["id"],
                        "name":item["name"],
                        "link":item["alternateLink"],
                    }
                )
            
        return response
            
    def _classroom_api_get_course_coursework(self, creds, course_id):
        """Returns a list of all current current pieces of coursework for a given course

        Args:
            creds (Credentials): Credentials for the service account
            course_id (str): Course ID
        """
        try:
            service = build("classroom", "v1", credentials=creds)
            self._log("Getting course coursework...",end="\r")
            results = service.courses().courseWork().list(courseId=course_id).execute()
            self._log("Getting course coursework... Done!")
            coursework = results.get("courseWork", [])

            if not coursework:
                return { # Return an empty dict if there are no current pieces of coursework
                    "response":200,
                    "coursework":False,
                    "data":None
                }
            else:
                return { # Return the current pieces of coursework if there are any
                    "response":200,
                    "coursework":True,
                    "data":coursework
                }
        except HttpError as error:
            return { # Return an error if there is one
                    "response":400,
                    "coursework":False,
                    "data":None,
                    "error":error
                }
    def get_course_coursework(self, creds, course_id):
        """Returns a list of all current current pieces of coursework for a given course"""
        api_response = self._classroom_api_get_course_coursework(creds, course_id)
        response = {
            "response":200,
            "coursework":True,
            "data":[]
        }
        if api_response["coursework"]:
            for item in api_response["data"]:
                if item["state"] == "PUBLISHED" and "dueDate" in item:
                    response["data"].append(
                        {
                            "id":item["id"],
                            "course_id":course_id,
                            "title":item["title"],
                            "description":item["description"] if "description" in item else "",
                            "due_date":f"{item['dueDate']['year']}/{item['dueDate']['month']}/{item['dueDate']['day']}",
                            "link":item["alternateLink"],                            
                        }
                    )
        else:
            response["coursework"] = False
            response["data"] = None
        return response

    def _classroom_api_get_extra_coursework_data(self, creds, courseID, courseworkID):
        """Returns the data for a given assignment (Used to check if handed in or not)

        Args:
            creds (Credentials): Credentials for the service account
            courseID (str): Course ID
            assignmentID (str): Assignment ID
        """
        try:
            service = build("classroom", "v1", credentials=creds)
            self._log("Getting extra coursework data...",end="\r")
            results = service.courses().courseWork().studentSubmissions().list(courseId=courseID, courseWorkId=courseworkID).execute()
            self._log("Getting extra coursework data... Done!")
            
            
            if not results:
                return { # Return an empty dict if there are no current pieces of coursework
                    "response":200,
                    "data":None
                }
            else:
                return { # Return the current pieces of coursework if there are any
                    "response":200,
                    "data":results
                }

        except HttpError as error:
            return { # Return an error if there is one
                    "response":400,
                    "data":None,
                    "error":error
                }
    def get_extra_coursework_data(self, creds, courseID, courseworkID):
        """Returns the data for a given assignment (Used to check if handed in or not)"""
        api_response = self._classroom_api_get_extra_coursework_data(creds, courseID, courseworkID)
        response = {
            "response":200,
            "data":{
                "course_id":courseID,
                "coursework_id":courseworkID,
                "handed_in":False,
            }
        }
        if api_response["data"]["studentSubmissions"][0] is not None:
            for item in api_response["data"]["studentSubmissions"]:
                if item["state"] == "TURNED_IN":
                    response["data"]["handed_in"] = True
        return response

    def get_all_data(self,creds: dict,  remove_handed_in=False, remove_overdue=False, remove_empty_courses=False, use_cache=False):
        """Returns all data for all courses and coursework"""
        
        if self.log_timer: self.log_start = datetime.datetime.now()

        if use_cache:
            dat = json.load(open(r"C:\Users\joehb\Documents\Coding\Joe-Booth-Computer-Science-NEA-2\lib\local_lib\classroom\example.json","r"))
        else:
            # Get all enrolled courses
            dat = self.get_enrolled_courses(creds)

            # Create empty coursework list for each course
            for item in dat["data"]: 
                item["coursework"] = []

            # Add coursework to each course
            for item in dat["data"]: 
                coursework_response = self.get_course_coursework(creds, item["id"])
                if coursework_response["coursework"]:
                    for coursework in coursework_response["data"]:
                        item["coursework"].append(coursework)

            # Remove coursework more than one month out of date
            for item in dat["data"]:
                for coursework in item["coursework"]:
                    if datetime.datetime.strptime(coursework["due_date"], "%Y/%m/%d") < datetime.datetime.now() - datetime.timedelta(days=30):
                        item["coursework"].remove(coursework)


            # Remove overdue coursework
            if remove_overdue:
                for item in dat["data"]:
                    for coursework in item["coursework"]:
                        if datetime.datetime.strptime(coursework["due_date"],"%Y/%m/%d") < datetime.datetime.now():
                            item["coursework"].remove(coursework)

            # Remove coursework that has been handed in (Optional)
            if remove_handed_in:
                for item in dat["data"]:
                    i = 0
                    while i < len(item["coursework"]):
                        extra_data = self.get_extra_coursework_data(creds, item["id"], item["coursework"][i]["id"])
                        if extra_data["data"]["handed_in"]:
                            del item["coursework"][i]
                        else:
                            i += 1

            # Remove courses with no coursework (Optional)
            if remove_empty_courses:
                i = 0
                while i < len(dat["data"]):
                    if len(dat["data"][i]["coursework"]) == 0:
                        del dat["data"][i]
                    else:
                        i += 1

            # Get some useful information that people might need to use idk
            dat["courseCount"] = len(dat["data"])
            dat["courseworkCount"] = 0
            for item in dat["data"]:
                dat["courseworkCount"] += len(item["coursework"])

        if self.log_timer: 
            difference = datetime.datetime.now() - self.log_start
            seconds_in_day = 24 * 60 * 60
            difference = divmod(difference.days * seconds_in_day + difference.seconds, 60)
            print(f"Processing Data Took {difference[0]} Minute(s) and {difference[1]} Second(s)")
        # Return the data
        return dat

if __name__ == "__main__":
    c = Classroom()
    c.log = False
    c.log_timer = True
    creds = c.GetCredentials()
    print(" Processing...", end="\r")
    courses = c.get_all_data(creds, use_cache=False, remove_handed_in=True, remove_empty_courses=True)
    json.dump(courses, open(f"{loc}/JSON Response/user.json", "w"), indent=4)
