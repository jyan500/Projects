# project_3_input.py
# Jansen Yan 12658454

import project_3_output
import project_3_json

### PICKING UP FROM WHERE YOU LEFT OFF: ### 12:50 P.M 10/30/15
    ### Starting off from running processing output functions within run_user_interface() function

##### USER INTERFACE IS BELOW #####



def _specify_location_amt() -> int:

    ''' user types in int amount of locations that user wants '''
    print("enter amount of locations: ")

    while True:
    
        response = int(input())

        if response >= 2:

            return response

        else:

            print('Please enter a number that is 2 or greater')


def _start_location() -> str:

    print("please enter the starting location: ")

    response = input()

    return response

        

def _end_locations(line_amt: int) -> list:

    end_locations = []

    # The reason why its line_amt - 1 is because
    # its not including the first line where you specify your start point

    print("Enter the ending location: ")
    
    for i in range(line_amt - 1):

        ends = input()

        end_locations.append(ends)

    return end_locations


def _specify_command_amt() -> int:

    ''' user specifies the amount of information desired '''

    print("Please specify amount of commands, from 1 to 5: ")

    while True:

        response = int(input())

        if 0 < response < 6:

            return response

        else:

            print('Please enter a number from 1 to 5')
            

def _get_commands(line_amt: int) -> [str]:

    ''' user types in the commands that they want, such as STEPS, and such '''

    print("Possible Commands: STEPS, TOTALDISTANCE, LATLONG, TOTALTIME, ELEVATION \n")
    print("Enter command and press enter, you will enter the amount of commands you specified.")

    commands = []

    for i in range(line_amt):

        info = input()

        commands.append(info)

    return commands


def run_user_interface() -> None:

    ''' runs user interface '''

    try:

        location_amt = _specify_location_amt()

        startpoint = _start_location()

        endpoints = _end_locations(location_amt)

        #endpoints should be [str]
        
        command_amt = _specify_command_amt()

        commands = _get_commands(command_amt)

        url = project_3_output.get_directions_url(startpoint, endpoints)

        json = project_3_output.get_directions_json(url)
        
        project_3_output.process_commands(commands, json)

        cred = project_3_output.Credits()

        cred.display()

    except KeyError:

        print('NO ROUTE FOUND')

    except:

        print()

        print('MAPQUEST ERROR')


if __name__ == '__main__':

    run_user_interface()
    

    

    

    


        


        

    

    



       




    

    
