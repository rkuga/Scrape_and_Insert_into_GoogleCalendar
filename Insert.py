# -*- coding: utf-8 -*-

from __future__ import print_function
import httplib2
import os

from apiclient import discovery
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage
import pandas as pd


try:
    import argparse
    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
    flags = None

SCOPES = 'https://www.googleapis.com/auth/calendar'
APPLICATION_NAME = 'Google Calendar API Python Insert Events'
CLIENT_SECRET_FILE = 'client_secret.json'

import requests
from bs4 import BeautifulSoup


def scrape_from_wiki():
    url = 'https://ja.wikipedia.org/wiki/日本の記念日一覧'
    res = requests.get(url)
    content = res.content
    soup = BeautifulSoup(content, 'html.parser')
    html_lists = soup.find_all('li')
    list_of_event_set=[]

    for month in range(1,13):
        for day in range(1,32):
            date=str(month)+'月'+str(day)+'日'
            todays_event=''
            for html_list in html_lists:
                events_list=html_list.find_all('a', title=date)
                if len(events_list)>0:
                    events=html_list.find_all('a')
                    for event in events:
                        if event.string==None or event.string==str(day)+'日':
                            continue
                        if not event.string.endswith("デー") and not event.string.endswith("日"):
                            todays_event+=event.string+'の日, '
                        else:
                            todays_event+=event.string+', '

            list_of_event_set.append((str(month),str(day),todays_event[:-2]))
    return list_of_event_set

def get_credentials():
    """Gets valid user credentials from storage.

    If nothing has been stored, or if the stored credentials are invalid,
    the OAuth2 flow is completed to obtain the new credentials.

    Returns:
        Credentials, the obtained credential.
    """
    home_dir = os.path.expanduser('~')
    credential_dir = os.path.join(home_dir, '.credentials')
    if not os.path.exists(credential_dir):
        os.makedirs(credential_dir)
    credential_path = os.path.join(credential_dir,
                                   'calendar-python-quickstart.json')

    store = Storage(credential_path)
    credentials = store.get()
    if not credentials or credentials.invalid:
        flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
        flow.user_agent = APPLICATION_NAME
        if flags:
            credentials = tools.run_flow(flow, store, flags)
        else: # Needed only for compatibility with Python 2.6
            credentials = tools.run(flow, store)
        print('Storing credentials to ' + credential_path)
    return credentials


def get_calendar_id():
    calendar_id = 'your gmail'

    return calendar_id


def create_api_body(event):
    email = 'your gmail'

    month=event[0]
    day=event[1]
    start_time = "2018-"+month+"-"+day+"T00:00:00+09:00"
    end_time = "2018-"+month+"-"+day+"T00:00:00+09:00"

    body = {
        "summary": event[2],
        "start": {
            "dateTime": start_time,
            "timeZone": "Asia/Tokyo",
        },
        "end": {
            "dateTime": end_time,
            "timeZone": "Asia/Tokyo",
        },
    }

    return body


def main():
    """
    Creates a Google Calendar API service object and
    create events on the user's calendar.
    """
    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    service = discovery.build('calendar', 'v3', http=http)

    calendar_id = get_calendar_id()

    event_list = scrape_from_wiki()

    for i,event in enumerate(event_list):
        body = create_api_body(event)

        try:
            event = service.events().insert(calendarId=calendar_id, body=body).execute()
        except:
            pass

if __name__ == '__main__':
    main()
