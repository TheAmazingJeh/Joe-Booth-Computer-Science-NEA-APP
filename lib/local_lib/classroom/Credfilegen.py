
import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

from tkinter import Tk
from tkinter.messagebox import showinfo, showerror, askyesno


# If modifying these scopes, delete the file token.json.
SCOPES = [
    "https://www.googleapis.com/auth/classroom.rosters.readonly",
    "https://www.googleapis.com/auth/classroom.courses.readonly",
    "https://www.googleapis.com/auth/classroom.coursework.me",
    ]

def GenerateCredentials(loc):
    TOKEN_PATH = f'{loc}/data/classroom/token.json'
    CREDS_PATH = f'{loc}/data/classroom/credentials.json'
    """Shows basic usage of the Classroom API.
    Prints the names of the first 10 courses the user has access to.
    """
    creds = None
    # If the token file exists, load it
    if os.path.exists(TOKEN_PATH): 
        creds = Credentials.from_authorized_user_file(TOKEN_PATH, SCOPES)

    # If there are no (valid) credentials available, let the user log in.
    try:
        if not creds or not creds.valid:
            doRefresh = askyesno("Refresh Token", "Your session has expired. Would you like to refresh it? This may open a browser window.")
            if doRefresh:
                if creds and creds.expired and creds.refresh_token:
                    creds.refresh(Request())
                else:
                    flow = InstalledAppFlow.from_client_secrets_file(CREDS_PATH, SCOPES)
                    creds = flow.run_local_server(
                        port=0,
                        prompt="consent",
                        success_message="You may close this window.",
                    )
                    print("✔️   Consent given")
                # Save the credentials for the next run
                with open(TOKEN_PATH, 'w') as token:
                    print("✔️   Saving new token")
                    token.write(creds.to_json())
            else:
                return "ERR_CANCEL"
    except Exception:
        return "ERR_CANCEL"
    return creds


def APIRequest(creds):
    try:
        service = build('classroom', 'v1', credentials=creds)

        # Call the Classroom API
        results = service.courses().list(pageSize=10).execute()
        if results is None:
            return False   
        else:
            return True

    except HttpError as error:
        return False


if __name__ == '__main__':
    w = Tk()
    c = GenerateCredentials("C:\\Users\\joehb\\Documents\\Coding\\Joe-Booth-Computer-Science-NEA-2")
    if c == "ERR_CANCEL":
        showerror("Error", "An error occurred during Authentication. Please try again.")
    if APIRequest(c):
        showinfo("API Test", "API request successful")
    else:
        showerror("API Test", "API request failed")