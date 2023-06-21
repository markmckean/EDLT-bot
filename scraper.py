import requests
from requests.structures import CaseInsensitiveDict
import datetime

START_TIME = 11.30


def retreive():
    date = datetime.datetime.now()
    time = str(date)[0: 10]
    url = # URL to scrape
    headers = CaseInsensitiveDict()
    # Contains token
    headers["Cookie"] = # Add the headers of a logged in user

    res = requests.get(url, headers=headers)
    data = res.json()
    return data


def sort_completed(data):
    # Take in new_format and send out same format but ordered by completed %
    new_data = [0]
    smallest_precent = 100
    for driver in data:
        temp = driver['percent_complete']
        temp2 = temp.split('.')
        temp3 = temp2[0]
        if int(temp3) < smallest_precent:
            new_data[0] = driver
            smallest_precent = int(temp3)

    return new_data


def find_small(data):
    name = 'unknown'
    smallest_precent = 1000
    for driver in data:
        temp = driver['percent_complete']
        if temp < smallest_precent:
            name = driver['name']
            smallest_precent = temp
    return name


def pop_name(data, name):
    i = 0
    for driver in data:
        if name == driver['name']:
            data.pop(i)
        else:
            i += 1
    return data


def new_format():
    data = retreive()
    all_driver_data = []
    for driver in data['transporters']:
        driver_data = {
            'name': 'unknown',
            'id': -1,
            'phone': -1,
            'route': 'unknown',
            'route_status': 'unknown',
            'completed': -1,
            'total': -1,
            'break_time': -1,
            'departed': False,
            'sph': -1,
            'percent_complete': -1
        }
        driver_data['name'] = driver['firstName'] + ' ' + driver['lastName']
        driver_data['id'] = driver['transporterId']
        driver_data['phone'] = driver['workPhoneNumber']
        all_driver_data.append(driver_data)

    for driver in data['itinerarySummaries']:
        curr_id = driver['transporterId']
        for worker in all_driver_data:
            if worker['id'] == curr_id:
                # Departed or NOT_DEPARTED
                if driver['executionStatus'] == 'NOT_DEPARTED':
                    worker['departed'] = False
                else:
                    worker['departed'] = True
                # Ahead behind completed
                worker['route_status'] = driver['progressStatus']
                # CX num
                worker['route'] = driver['routeCode']
                # Break time
                worker['break_time'] = driver['totalBreaksDurationSecs']
                # total / completed
                progress_dict = driver['stopProgress']
                worker['total'] = progress_dict['total']
                worker['completed'] = progress_dict['completed']

    cur_time = datetime.datetime.now()
    for driver in all_driver_data:
        per = 100 * float(driver['completed']) / float(driver['total'])
        per = round(per, 1)
        #str_per = str(per) + '%'
        driver['percent_complete'] = per
        if (cur_time.hour) >= 13:
            hours_since_12 = cur_time.hour - 12
            driver['sph'] = float(int(driver['completed']) / hours_since_12)
        else:
            driver['sph'] = driver['completed']
    return all_driver_data


def sort(data, sorted):
    while len(data) >= 1:
        small = find_small(data)
        sorted.append(small)
        data = pop_name(data, small)
        sort(data, sorted)
