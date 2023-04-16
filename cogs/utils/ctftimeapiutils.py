import requests

import config

baseurl = 'https://ctftime.org/api/v1/'

def fetch_event_info(event_id):
    url = baseurl + 'events/' + str(event_id) + '/'
    headers = {'user-agent': config.user_agent}

    response = requests.get(url, headers=headers)
    response.raise_for_status() # Throws exception when code >= 400
    
    return response.json()

def fetch_upcoming_events(num_events):
    url = baseurl + 'events/'
    params = {'limit': str(num_events)}
    headers = {'user-agent': config.user_agent}
    
    response = requests.get(url, params=params, headers=headers)
    response.raise_for_status() # Throws exception when code >= 400
    
    return response.json()
