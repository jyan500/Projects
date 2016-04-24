# project_3_json
# Jansen Yan 1265454



import json
import urllib.parse
import urllib.request




MAP_URL = 'http://open.mapquestapi.com/directions/v2'

ELEVATION_URL = 'http://open.mapquestapi.com/elevation/v1'

MY_API = 'cvRRjMd7HzxtGdp35qKhv3xCga7w9ZrC'




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

    

    


def direction_url(startpoint: str, endpoints: [str]) -> 'encoded URL':

    ''' constructs a valid, encoded url based on keywords '''

    url_query = [('key', MY_API), ('from', startpoint)]

    for endpoint in endpoints:

        url_query.append(('to', endpoint))


    return MAP_URL + '/route?' + urllib.parse.urlencode(url_query)


def elevation_url(lat_long: dict) -> 'encoded URL':

    ''' constructs a valid, encoded url based on key parameters '''

    key_list = []

    url_query = [('key', MY_API), ('unit', 'f')]

    key_list.append(str(lat_long['lat']))

    key_list.append(str(lat_long['lng']))

    return ELEVATION_URL + '/profile?' + urllib.parse.urlencode(url_query) + '&latLngCollection=' + ','.join(key_list)




    





    





    

    




                       

