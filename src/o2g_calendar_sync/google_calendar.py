"""
Modified from:
https://github.com/googleworkspace/python-samples/blob/master/calendar/
quickstart/quickstart.py
"""
import os.path
from typing import Any, Dict, List

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

# If modifying these scopes, delete the file token.json.
SCOPES = ["https://www.googleapis.com/auth/calendar"]


class GoogleCalendar:
    """
    Class for interacting with Google Calendar via the Calendar API
    """

    def __init__(self) -> None:
        """
        Initialize class and get a Calendar API service object for interacting
        with the API in other class methods
        """
        self.creds = self.get_creds()
        self.service = build("calendar", "v3", credentials=self.creds)

    def get_creds(self) -> Credentials:
        """
        Get credentials object from user's credentials.json file for a desktop
        application. See the following guide for details on how to create this:

        https://developers.google.com/workspace/guides/create-credentials

        Returns:
            Credentials: Credentials object. Note that this is also saved to
                disk (and checked prior to retrieving a renewed credential).
        """
        creds = None
        # The file token.json stores the user's access and refresh tokens, and
        # is created automatically when the authorization flow completes for the
        # first time.
        if os.path.exists("token.json"):
            creds = Credentials.from_authorized_user_file("token.json", SCOPES)
        # If there are no (valid) credentials available, let the user log in.
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    "credentials.json", SCOPES
                )
                creds = flow.run_local_server(port=0)
            # Save the credentials for the next run
            with open("token.json", "w") as token:
                token.write(creds.to_json())
        return creds

    def get_calendar_list(self) -> List[Dict[str, Any]]:
        """
        Retrieves calendar list, for additional details see:

        https://developers.google.com/calendar/api/v3/reference/calendarList

        Returns:
            List[Dict[str, Any]]: Calendar list with details about each (id,
                summary, accessRole, etc.).
        """
        page_token = None
        result: List[Dict[str, Any]] = []
        while True:
            calendar_list = (
                self.service.calendarList().list(pageToken=page_token).execute()
            )
            result.extend(calendar_list["items"])
            page_token = calendar_list.get("nextPageToken")
            if not page_token:
                break
        return result
