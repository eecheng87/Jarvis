import logging
import requests
from datetime import datetime
import json

CWB_URL = 'http://opendata.cwb.gov.tw/api/v1/rest/datastore/'
DATA_ID = 'O-A0001-001'
AUTH_KEY = 'CWB-B20C4C5C-23EF-47A9-81DE-41D6E7487E70'
ID_MAP = {'kaohsiung':'C0V490','tainan':'C0X110','taichung':'C0F9N0'}
def get_data_from_cwb(data_id, auth_key, params={}):
    '''limit, offset, format, locationName, elementName, sort'''
    logging.info('getting data from CWB...')

    dest_url = CWB_URL + '{}'.format(data_id)
    r = requests.get(dest_url, headers={'Authorization': auth_key})
    params_list = ['{}={}'.format(key, params[key]) for key in params]
    params_str = '?' + '&'.join(params_list)
    dest_url += params_str
    logging.debug('dest_url: {}'.format(dest_url))

    if r.status_code != 200:
        logging.error('r.status_code: {}'.format(r.status_code))
        return None

    data = r.json()

    if data.get('success') != 'true':
        return None
    return data

def parse_json_to_dataframe(data,id):
    for unit in data['records']['location']:
        if unit['stationId'] == id:
            for wea_unit in unit['weatherElement']: # unit['weatherElement'] is list
                if wea_unit['elementName'] == 'TEMP':
                    print(type(wea_unit['elementValue']))
                    return wea_unit['elementValue']

def search(json_str, no):
    return [datum for datum in json_str if datum['stationId']==no]



#if __name__ == '__main__':
    #json_data = get_data_from_cwb(DATA_ID, AUTH_KEY, {})
    #temp = parse_json_to_dataframe(json_data)
    #print(temp)
