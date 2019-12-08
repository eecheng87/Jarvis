import requests
from requests_html import HTML
import time

def parse_entries(doc):
    html = HTML(html=doc)
    post_entries = html.find('div.search-trip tr.trip-column')
    return post_entries
def parse_meta(ent):
    meta = {
        'type': ent.find('li', first=True).text,
        'departure': ent.find('td')[1].text,
        'arrival': ent.find('td')[2].text,
    }
    return meta

def current_time():
    # format is '17:50'
    # fix min < 10 bug (should be :07 instead of :7)
    localtime = time.localtime(time.time())
    mi = '0'+str(localtime.tm_min) if localtime.tm_min<10 else str(localtime.tm_min)
    hr = '0'+str(localtime.tm_hour) if localtime.tm_hour<10 else str(localtime.tm_hour)
    res = hr+':'+mi
    return res

def current_date():
    # format is '2019/11/27'
    localtime = time.localtime(time.time())
    res = str(localtime.tm_year)+'/'+str(localtime.tm_mon)+'/'+str(localtime.tm_mday)
    return res

train_map = {
    'kaohsiung':'4400-高雄',
    'tainan':'4220-臺南',
    'taichung':'3300-臺中',
    'taipei':'1000-臺北',
    'hsinchu':'1210-新竹',
    'jiayi':'4080-嘉義',
    'taoyuan':'1080-桃園'
}

payload = {
    '_csrf': '8eb314af-c2ea-44b9-9da3-407468839313',
    'startStation': '4400-高雄',
    'endStation': '4220-臺南',
    'transfer': 'ONE',
    'rideDate': '2019/11/27',
    'startOrEndTime': 'true',
    'startTime': '19:40',
    'endTime': '23:59',
    'trainTypeList': 'ALL',
    'query': '查詢',
}

if __name__ == '__main__':

    #print(type(payload['startTime']))
    result = input('') # format: 'start' 'dest' 'time'  (time is 0~23)
    word = result.split()
    if len(word) > 3:
        print('Incorrect format')
    else:
        payload['startStation'] = train_map[word[0]]
        payload['endStation'] = train_map[word[1]]
        if len(word) == 2:
            # need table start from now
            payload['startTime'] = current_time()
            payload['rideDate'] = current_date()
        else:
            payload['startTime'] = str(word[2])+':00'
            payload['rideDate'] = current_date()
        res = requests.post("https://www.railway.gov.tw/tra-tip-web/tip/tip001/tip112/querybytime",data=payload)

        parse = parse_entries(res.text)
        metadata = [parse_meta(entry) for entry in parse]
        for a in metadata:
            print(a)
