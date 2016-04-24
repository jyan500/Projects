# project_3_output
# 12658454 Jansen Yan

import project_3_json
import project_3_input



#### OUTPUT CLASSES ####
        
        
class Steps(list):

    def __init__(self, some_json: 'json object'):

        ''' initializes the Class '''

        self.directions = []

        self.json = some_json

    def gather(self):

        ''' gathers narrative information from json object and appends to self.directions '''

        for item in self.json['route']['legs']:

            for maneuvers in item['maneuvers']:

                self.directions.append(maneuvers['narrative'])

        

    def display(self):

        ''' displays the formatted narrative information '''

        print('DIRECTIONS')

        for steps in self.directions:

            print(steps)

        print()

 


class LatLong(list):

    def __init__(self, some_json: 'json object'):

        ''' initializes LatLong Class '''

        self.latlong = []

        self.json = some_json

    def gather(self):

        ''' gathers necessary latlong information into self.latlong '''

        for item in self.json['route']['locations']:

            self.latlong.append(item['displayLatLng'])

        

    def display(self):

        ''' formats the latitude and longitude information and prints it out '''

        print('LATLONGS')

        for item in self.latlong:

            if item['lat'] > 0 and item['lng'] < 0:
                
                format_str = "{0:1.2f}N {1:1.2f}W".format(item['lat'], item['lng'] * -1)

                print(format_str)

            if item['lat'] < 0 and item ['lng'] > 0:

                format_str = "{0:1.2f}S {1:1.2f}E".format(item['lat'] * -1, item['lng'])

                print(format_str)

            if item['lat'] < 0 and item['lng'] < 0:

                format_str = "{0:1.2f}S {1:1.2f}W".format(item['lat'] * -1, item['lng'] * -1)

                print(format_str)

            if item['lat'] > 0 and item['lng'] > 0:

                format_str = "{0:1.2f}N {1:1.2f}E".format(item['lat'], item['lng'])

                print(format_str)

        print()
                
    def get_latlong(self):

        ''' returns self.latlong, which is a list of dictionaries, function is needed for

    the sake of getting Elevation class '''

        return self.latlong


class Distance(object):

    def __init__(self, some_json: 'json object'):

        ''' initializes Distance class '''

        self.distance = 0

        self.json = some_json

    def gather(self):

        ''' gathers distance information and stores it in self.distance '''

        self.distance += self.json['route']['distance']

    def display(self):

        ''' formats distance information and prints it '''

        format_str = "TOTAL DISTANCE: {0:1.0f} miles".format(self.distance)

        print(format_str)

        print()

    


class Time(object):

    def __init__(self, some_json: 'json object'):

        ''' initializes Time Class '''

        self.time = 0

        self.json = some_json

    def gather(self):

        ''' gathers total time information and converts it from seconds to minutes '''

        self.time += (self.json['route']['time'])/60

    def display(self):

        ''' formats the time information and prints it out '''

        

        format_str = "TOTAL TIME: {0:1.0f} minutes".format(self.time)

        print(format_str)

        print()
    


class Elevations(list):

    def __init__(self, json_list: ['json object']):

        ''' initializes Elevations Class, note that it takes a list of json objects as a parameter,

    unlike the other classes, which take one json object as parameter '''

        self.elevations = []

        self.json = json_list

    def gather(self):

        ''' gathers necessary information about elevations from the list of jsons '''
        
        for elevation_dict in self.json:

            for profile in elevation_dict['elevationProfile']:

                self.elevations.append(profile['height'])        

    def display(self):

        ''' displays elevations '''

        print('ELEVATIONS')

        for item in self.elevations:

            print("{0:1.0f}".format(item))

        print()

class Credits(object):

    def __init__(self):

        self.credits = ''

    def display(self):

        self.credits += 'Directions Courtesy of MapQuest; Map Data Copyright OpenStreetMap Contributors'

        print(self.credits)

        


### GETS URLS ACCORDING TO USER, PROCESSES THEM ###


def get_directions_url(start: str, ends: [str]) -> 'url string':

    '''gets the url for direction service '''

    url = project_3_json.direction_url(start, ends)

    return url


def get_directions_json(url: str) -> 'json object':

    ''' gets json of the direction service based on url '''

    json = project_3_json.process_url(url)

    return json

def get_elevations_url(json: 'json object') -> ['urls']:

    ''' get elevation urls based on latitude and longitude information '''

    url_list = []

    latlng = LatLong(json)

    latlng.gather()

    latlng_list = latlng.get_latlong()

    for dic in latlng_list:

        url_list.append(project_3_json.elevation_url(dic))

    return url_list


def get_elevations_json(list_of_urls: list) -> ['json objects']:

    ''' gets the json elevation profiles based on the urls of the input list '''

    json_elevation_list = [] 

    for item in list_of_urls:

        json_elevation_list.append(project_3_json.process_url(item))

    return json_elevation_list


def _class_action(class_obj: 'any obj of the defined classes below') -> None:

    ''' performs the actions necessary on the class to gather and display the necessary output '''

    class_obj.gather()

    class_obj.display()


    

def process_commands(command_list: [str], json: 'json_object') -> None:

    ''' processes user commands and prints out the specified output '''

    print()

    for command in command_list:

        if command == 'STEPS':

            # call class Steps

            steps = Steps(json)

            _class_action(steps)
            
        if command == 'TOTALDISTANCE':

            # call class Distance

            distance = Distance(json)

            _class_action(distance)

        if command == 'TOTALTIME':

            # call class Distance

            time = Time(json)

            _class_action(time)

        if command == 'LATLONG':

            # call class LatLng

            latlng = LatLong(json)

            _class_action(latlng)

        if command == 'ELEVATION':

            # call class Elevation

            url_list = get_elevations_url(json)

            json_list = get_elevations_json(url_list)

            elevation = Elevations(json_list)

            _class_action(elevation)

        else:

            # do nothing

            pass




    





    




    

    



    
    



        
        
                

            

                

            

                

            

      

          









