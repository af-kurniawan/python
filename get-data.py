import requests
import json
import os
from datetime import datetime

BASE_URL = 'https://api.domain.com.au'

MELBOURNE_AREAS = ['Whitehorse', 'Buroondara', 'Knox', 'Manningham', 'Maroondah', 'Yarra Ranges', 'Yarra-Dandenong Ranges', 'Bayside', ]

def getBody(city, state): 
    return {
    "listingType": "Sale",
    "locations": [
    {
        "state": state,
        "area": city
    }
    ]
}

    
# get credentials
with open('creds/domain-api.json') as f:
    headers = json.load(f)


def getSearchCount(body):
    end_point = BASE_URL + '/v1/listings/residential/_search'
    r = requests.post(end_point, headers=headers, json=body)
    print(body, r.headers['X-Total-Count'], '\n')


def add_index(el):
    if 'listing' in el:
        return {str(el['listing']['id']): el}
    elif 'id' in el:
        return {str(el['id']): el}
    else:
        print('no id', el)
        return el

def arr_to_dict(arr):
    return list(map(add_index, arr))

def unpack_projects(arr):
    ans = []
    for x in arr:
        if 'listings' in x:
            # add in listings in project
            ans += (x['listings'])
        else:
            ans.append(x)
    return ans

# returns list of dicts
def get_listings(base_url, body): 
    end_point = base_url + '/v1/listings/residential/_search'
    get_next_page = True
    current_page = 1
    all_result_str = []
    body['pageSize'] = '200'
    while get_next_page:
        body['pageNumber'] = str(current_page)
        r = requests.post(end_point, headers=headers, json=body)
        if len(r.json()) > 0 and current_page < 5:
            print('requesting page ' + str(current_page))
            all_result_str += r.json()
            current_page += 1
        else:
            get_next_page = False


    # return all_result_str
    arr = arr_to_dict(unpack_projects(all_result_str))
    ans = {}
    for x in arr:
        # print(x['id'])
        ans.update(x)
    return ans

def get_sales_data(city): 
    end_point = BASE_URL + '/v1/salesResults/' + city + '/listings'
    r = requests.get(end_point, headers=headers)

def save_to_file(data):
    with open('data.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

def overwriteFile(new_data):
    filename = 'data.json'
    if os.path.exists(filename):
        with open(filename, 'r') as f:
            data = json.load(f)
            data.update(new_data)
            

        time = datetime.now().strftime('%Y-%m-%d %H:%M:%S').replace(':', '-')
        os.rename(filename, 'old/' + time + '.json')    
        save_to_file(data)

    else:
        save_to_file(new_data)

def search_and_save(base_url, body):
    to_save = get_listings(base_url, body)
    overwriteFile(to_save)

def count_file_length(file_name):
    with open(file_name, 'r', encoding='utf-8') as f:
        data = json.load(f)
    print(len(data.keys()))

# for searching areas that return > 1000 results
def search_big_area(city, state, maxFraction=1500000):
    n = 50000
    arr = []
    to_save = {}
    while n <= maxFraction:
        arr.append(n)
        n += 50000
    body = getBody(city, state)
    for price in arr:
        body['minPrice'] = price
        body['maxPrice'] = price + 50000
        to_save.update(get_listings(BASE_URL, body))
        print(len(to_save.keys()))
        

        # for counting
        # getSearchCount(body)    
    # search the rest
    body['minPrice'] = maxFraction
    body['maxPrice'] = None
    to_save.update(get_listings(BASE_URL, body))
    print(len(to_save.keys()))
    overwriteFile(to_save)



    # for counting
    # getSearchCount(body)

# to_save = get_listings(BASE_URL, test_body)
# print(len(to_save.keys()))
# overwriteFile(to_save)

# getSearchCount(getBody('North', 'VIC'))

# search_big_area('West', 'VIC', 1100000)
count_file_length('data.json')
