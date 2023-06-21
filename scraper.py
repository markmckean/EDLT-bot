import requests
from requests.structures import CaseInsensitiveDict
import datetime
import test_values

START_TIME = 11.30


def retreive():
    date = datetime.datetime.now()
    time = str(date)[0: 10]
    url = f"https://logistics.amazon.com/operations/execution/api/summaries?localDate={time}&serviceAreaId=5704de31-3889-4b52-9594-fdcb29aef0cd"
    headers = CaseInsensitiveDict()
    # Contains token
    headers["Cookie"] = r'_RCRTX03-samesite=5a5482390c2e11edbe22a51fea3e8a32cab6038c59e641e7867237852fbb246e; ubid-main=135-4736869-6372061; aws-target-data=%7B%22support%22%3A%221%22%7D; regStatus=pre-register; session-id-apay=141-7576606-6639863; x-amz-log-portal-locale=en-US; s_nr=1676327967954-New; s_vnum=2108327967954%26vn%3D1; s_dslv=1676327967955; aws-target-visitor-id=1676329916848-428029.35_0; AMCV_7742037254C95E840A4C98A6%40AdobeOrg=1585540135%7CMCIDTS%7C19418%7CMCMID%7C28875472614817624971379149702857793518%7CMCAAMLH-1678311107%7C9%7CMCAAMB-1678311107%7CRKhpRz8krg2tLO6pguXWp5olkAcUniQYPHaMWWgdJ3xzPWQmdj0y%7CMCOPTOUT-1677713507s%7CNONE%7CMCAID%7CNONE%7CvVersion%7C4.4.0; sst-main=Sst1|PQFTmLuBzdG4LDe8S_IWjEFNCSONNKTeqFYC-LcDdcQap8qFF4SzpRstaPzf0DszZ8XKrjEuzXASEZpY9G751H1bQ8M9bHNSa_Hkijt-LDDG_qEx-kE606YLolgZwUDi-pxFTOGPA0_xXPr12z78aYgweECq_dchYcgMZTrA_-pasLnJnDu3ZuGKQt6S92MvTT_20lSLtzctnJrMP7nmdDVOw44Iv0UWzrRZ3tnFU52mhFBjW6B9lV1gtM6bxNmJeDcl-suQ61l3kEn4uMixykp_5_425EhSpn6Q8ImF7stqkeo; lc-main=en_US; i18n-prefs=USD; session-id=136-4685400-0403837; session-token=lDHnGPOjld50VTN8ZpPg+0XXxlUxJrlacITSS5zKqxBIAaydYMuoV0BhH3jjaris5BUroRSlhGTbnL/QCgsRCPeMzq1ji00FPh5RBNgFmFWPSpSO7nKXbFmK0wO9bcfxo0CpVcOEu8yt97KL/5U9q1Xrp2zyPZpqb85BEYrxDdJ6yXxHYK+/rlSpg+oVAtMgRwM82dyRnE45AhjaJTrh5DK1hK44XfnYg8Op91X4I8cOzSr4iBzRy2jueJ67ZcnY; x-main="v5c9@gA0@Eq6@oYGlYKjAKK?W3DPxWHtEWJwhGcHuMnUipakM5gOmhswRIpQ107m"; at-main=Atza|IwEBIJWchP5JC1qy8-K0agoqMBd9C9_qZpbx1p1I2cOfMc6zefEL7Ixzxn6R_Qu-fI-dacOhlqPp1hHHXcJuac_g04b_tOjzwCIbdI-XhM9-0eKcrl1JJdMO8q-Kks0-slliy4lR-JPF1rBdiziRWOJw2Tbwixxqgr2Mu3PKbu7ERbuLGztsK0A0Je64PHCmXwLBX3Ey3xJHDJckhQWWiDSsLv7j; sess-at-main="sJnqSy8LG3E/majTa2lPscPAutaJ2i+BLIKa9xdKoTY = "; session-id-time=2082787201l; skin=noskin'

    res = requests.get(url, headers=headers)
    data = res.json()
    return data


def get_time_delivering(data, name):
    # This function should check to see if the driver has
    # taken their lunch, and determine the amount of time they have
    # worked that day.
    ...


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
