import requests

baseurl = 'https://ctftime.org/api/v1/'

def get_event_info(event_id):
    url = baseurl + 'events/' + event_id + '/'
    
    response = requests.get(url)
    return response.json()

def get_upcoming_events(num_events):
    url = baseurl + 'events/'
    params = {'limit': num_events}

    response = requests.get(url, params)
    return response.json()


