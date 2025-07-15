from __future__ import print_function

import datetime
import pprint
import os.path

from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

SCOPES = ['https://www.googleapis.com/auth/calendar']
SCOPES2 = ['https://www.googleapis.com/auth/tasks']


creds = None
if os.path.exists('key_calendar.json'):
    creds = service_account.Credentials.from_service_account_file(filename='key_calendar.json', scopes=SCOPES)

try:
    service = build('calendar', 'v3', credentials=creds)
except HttpError as error:
    print('An error occurred: %s' % error)


def add_calendar(calendar_id):
    try:
        calendar_list_enty = {
            'id': calendar_id
        }
        service.calendarList().insert(
            body=calendar_list_enty).execute()
        return 'Спасибо, мы добавили ваш календарь'
    except Exception as e:
        print(e)
        if 'Not Found' in str(e):
            return 'Вы указали неверный идентификатор календаря или не предоставили доступ к календарю для бота'


def get_events(calendar_id, date):
    if not calendar_id:
        return
    ans = []
    events = service.events().list(calendarId=calendar_id).execute()
    for event in events['items']:
        if 'dateTime' in event['end']:
            if event['end']['dateTime'].split('T')[0] == date:
                ans.append(event['summary'])
        else:
            if event['end']['date'] == date:
                ans.append(event['summary'])
    return ans


if __name__ == '__main__':
    ans = get_events('dimon0myxin@gmail.com', '2023-01-09')
    print(ans)
    # ans = add_calendar('dimon0myxin@gmail.com')
    # print(ans)

    # calendar_list = service.calendarList().list().execute()
    # pprint.pprint(calendar_list)

    events = service.events().list(calendarId='dimon0myxin@gmail.com').execute()
    pprint.pprint(events)
