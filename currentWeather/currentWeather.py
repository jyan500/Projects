#### Jansen Yan currentWeather.py data ####

import json
import urllib.parse
import urllib.request
import base64

MY_API = '8a5dc1aa45530816'
MY_URL = 'http://api.wunderground.com/api/8a5dc1aa45530816/forecast/conditions/q/'

### URL request format 'http://api.wunderground.com/api/API_KEY/features/settings/q/query.format

#### request, decode and process URL ####

def _decode_url(url_content: bytes) -> str:
    
    ''' encodes the content from type <bytes> to
type <str>, returns the content as a str '''
    
    json_string = url_content.decode(encoding = 'utf-8')
    return json_string


def _request_url(url: str) -> bytes:

    ''' requests a valid url and reads it'''

    response = None
    try:
        response = urllib.request.urlopen(url)
        url_content = response.read()
        return url_content
    finally:
        if response != None:
            response.close()


def _json_content(url_content: str) -> 'JSON object':

    ''' returns the content type <str> into JSON object ''' 
    json_obj = json.loads(url_content)
    return json_obj


def process_url(url: str) -> 'JSON object':

    ''' does the url processing, starting and ending location
keywords are input, returns the json version of the url content '''

    url_content = _request_url(url)
    json_string = _decode_url(url_content)
    json_object = _json_content(json_string)
    return json_object

def build_url(state, city):
    
    ''' Add state and city to the url '''
    assert type(state) is str
    assert type(city) is str
    if '_' not in city:
        city = '_'.join(city.split())
    q = state + '/' + city + '.json'
    return MY_URL + q

##### PROCESS JSON #####

def get_condition(json_obj: 'json_obj') -> (str):
    ''' gets current location and temperature from json object '''
    try:
        temp_f = json_obj["current_observation"]["temperature_string"]
        current_weather = json_obj["current_observation"]["weather"]
        current_time = json_obj["current_observation"]["observation_time"]
        location = json_obj["current_observation"]["display_location"]["full"]
        return (location, temp_f, current_time, current_weather)
    except KeyError:
        return ("Invalid Location", "", "", "")
    
def process_forecast(json_obj: 'json_obj') -> {str: {str: str}}:
    '''processes forecast information based on json object and returns as dict'''

    forecast_dict = dict()
    inner_dict = dict()
    try:
        forecast = json_obj["forecast"]["txt_forecast"]["forecastday"]
        for d in forecast:
            forecast_dict[d['title']] = {'condition': d['icon'], 'forecast': d['fcttext'], "icon": d["icon_url"], "period": d["period"]}
        return forecast_dict
    except KeyError:
        pass

def get_forecast_pictures_url(json_obj: 'json_obj'):
    url_dict = dict()
    try:
        forecast = json_obj["forecast"]["txt_forecast"]["forecastday"]
        for d in forecast:
            url_dict[d["title"]] = d["icon_url"]
        return url_dict
    except KeyError:
        pass

def get_current_pic_url(json_obj: "json_obj"):
    try:
        return json_obj["current_observation"]["icon_url"]
    except KeyError:
        pass
##### MAIN ######

def main(state: str, city: str):
    ''' gets all the necessary information by requesting, decoding, processing the url into
json object, then parses the json for forecast information '''
    p = process_url(build_url(state, city))
    return get_condition(p), process_forecast(p), get_current_pic_url(p)

def decode_picture(url):
    ''' takes url, and decodes if url is link to gif image '''
    url_content = _request_url(url)
    image64 = base64.encodestring(url_content)
    return image64
    

if __name__ == '__main__':
    #print(main("CA", "San Mateo"))
    pass
        
    # the city must have an underscore if more than one word

   

