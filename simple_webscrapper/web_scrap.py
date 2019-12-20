import requests
import pprint
from bs4 import BeautifulSoup
import os
import json

json_model = {
}

URL = 'https://www.viralagenda.com/pt/home'
page = requests.get(URL)

soup = BeautifulSoup(page.content, 'html.parser', from_encoding='ascii')

event_list = soup.find(id='viral-events')

event_thing = event_list.find_all('li')

for event in event_thing:

    #Get the url to the event details
    plus_url = 'https://www.viralagenda.com' + event.get('data-url')
    event_detailed = requests.get(plus_url)

    #Parse it
    soup_detailed = BeautifulSoup(event_detailed.content, 'html.parser')

    #Get the info about it
    event_detailed_date = soup_detailed.find(id='viral-event')
    event_detailed_name_div = soup_detailed.find('div', class_="viral-title")
    event_detailed_name_div_name = event_detailed_name_div.find('h1')
    event_detailed_nav_box = soup_detailed.find('div', class_='viral-event-nav')
    event_detailed_nav_box_place = event_detailed_nav_box.find('div', class_='event-detail-place').get_text()


    location_text = os.linesep.join([s for s in event_detailed_nav_box_place.splitlines() if s])
    location_text = location_text.replace('\t', '').split('\n')

    name = event_detailed_name_div_name.text

    #Add the data to a json model
    json_model['name'] = name
    json_model['start-date'] = event_detailed_date.get('data-date-start').split('T')
    json_model['location'] = location_text
    json_model['url'] = plus_url

    with open('events.json') as f:
        data = json.load(f)

    data.append(json_model)

    with open('events.json', 'w') as f:
        json.dump(data, f)
