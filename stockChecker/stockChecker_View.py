# Controls User Input for stockChecker.py
import stockChecker as stock
from datetime import date

##### import Filename #####

def _create_date(year: int, month: int, day: int) -> date:

    ''' creates datetime object based on function parameters year, month and day '''
    try:
        
        return date(year, month, day)

    except ValueError:

        print('''Invalid input, date does not exist''')

def _menu() -> None:

    print('############## stockChecker Program, written by Jansen Yan 12/20/15 ####################\n')
    print('#####Menu#####:')
    print('''Follow Directions, enter input, hit enter\n''')

    
def _ask_company() -> str:

    ''' prompts user for company, returns uppercase company name '''

    company_name = input('Please enter the company symbol:\n')

    return company_name.upper()

def _ask_start_date() -> date:

    ''' asks for startdate and creates date '''

    date = input(''' Please enter the start date
            Please enter date in the following format:
            date/month/year, if date and/or month is one digit, just enter the digit
            If today\'s date is desired, hit enter:\n''')
 
    if date != '':
        date_info = date.split('/') 
        d = _create_date(int(date_info[2]), int(date_info[1]), int(date_info[0]))
        return d

    else:
        return _create_today_date()
        
def _create_today_date() -> date:

    ''' returns today's date ''' 

    return date.today()

def _ask_end_date(start_date: date) -> date:

    date = input('''Please enter the end date
            Please enter date in the following format:
            date/month/year, if date and/or month is one digit, just enter the digit
            If 1 month's data is desired since the starting point, enter m
            If 1 year's data is desired since the starting point, enter y
            If 5 year's data is desired since the starting point, enter 5y:\n''')

    if date == 'm':
        month = str(start_date.month)
        if str(month[0]) == str('01'):
            end_date = start_date.replace(month = 12, year = start_date.year - 1)
            return end_date            
        else:
            if month[0] == str(0):
                end_date = start_date.replace(month = int(month[1]) - 1)
                return end_date
            else:
                end_date = start_date.replace(month = int(month) - 1)
                return end_date
        
    if date == 'y':
        end_date = start_date.replace(year = start_date.year - 1)
        return end_date
    
    if date == '5y':
        end_date = start_date.replace(year = start_date.year - 5)
        return end_date

    else:
        date_info = date.split('/')
        d = _create_date(int(date_info[2]), int(date_info[1]), int(date_info[0]))
        return d


def _ask_filename() -> str:

    filename = input('Please enter the name of your file, suffix must be a .txt or other format:\n')

    return filename


#### PUBLIC FUNCTIONS ####

def run_user_interface() -> None:

    ''' gets information from user and runs the program '''
    _menu()
    company = _ask_company()
    start_date = _ask_start_date()
    end_date = _ask_end_date(start_date)
    filename = _ask_filename()

    stock.run_program(company, end_date, start_date, filename)

    #the reason why end_date is inserted first as a parameter is because
    #the dates are entered in chronological order (from past to present,
    # vs the other way around which is what is asked in this user interface)
        

if __name__ == '__main__':
    run_user_interface()
        

    
    
  
    

