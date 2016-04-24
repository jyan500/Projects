#stockChecker.py
# written by Jansen Yan, 12/20/15
# for yahoo developers

# The function of this program:
# input: takes company, startDate and endDate
# creates proper YQL statement based on an existing global str
# requests and processes URL into json content
# parses json content for each day's stock quote
# writes stock quotes to a text file

import urllib.parse # encode url so special characters are encoded
import urllib.request # downloads the content in the url address as <bytes>
import json # converts url content (the url content has to be converted from <bytes> to <str> from
            # url content which is html to json (javascript object notation), usable by python

from datetime import date # datetime is the module, can create object representing a real time

#MY_API = '''dj0yJmk9MEF2SU9qUjFNTUQzJmQ9WVdrOWMwbGljWFJwTkc4bWNHbzlNQ
#S0tJnM9Y29uc3VtZXJzZWNyZXQmeD0xZA--'''
# MY_SECRET_API = '''ab2b1e82780940e06d6153169a6db8b2147f9029'''

STARTING_URL = 'http://query.yahooapis.com/v1/public/yql'

# STARTING_URL gives the initial address to yahoo, without query parameters added
YQL_STATEMENT = 'select * from yahoo.finance.quotes where symbol= "{}"'
YQL_HISTORICAL_DATA = 'select * from yahoo.finance.historicaldata where symbol = "{}" and startDate = "{}" and endDate = "{}"'
# YQL_HISTORICAL_DATA is used in this program, it is one of the url query parameters
YQL_MULTIPLE = 'select * from yahoo.finance.quotes where symbol in ({})'
RETRIEVE_TABLE = 'http://datatables.org/alltables.env'
# RETRIEVE_TABLE is another url query parameters

# datetime.date instructions: datetime.date(year, month, day)
## where:
##MINYEAR <= year <= MAXYEAR
##1 <= month <= 12
##1 <= day <= number of days in the given month and year

# note startDate and endDate format in YQL_HISTORICAL_DATA: year-month-date, i.e 2012-05-01

##### These two Functions are not used in this program ######

def _create_YQL_statement(company: str) -> str:

    ''' specify the company that you want '''

    return YQL_STATEMENT.format(company)

    
def _create_YQL_statement2(companies: [str]) -> str:

    ''' specify multiple companies that you want '''
    
    a = str(tuple(companies))
    return YQL_MULTIPLE.format(a)

##### Private Functions ######

def _create_YQL_historical_statement(company: str, start: str, end: str) -> str:

    ''' find quote of a company from a start to end date '''

    return YQL_HISTORICAL_DATA.format(company, start, end)

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


def _process_url(url: str) -> 'JSON object':

    ''' does the url processing, starting and ending location
keywords are input, returns the json version of the url content '''

    url_content = _request_url(url)

    json_string = _decode_url(url_content)

    json_object = _json_content(json_string)

    return json_object

def _create_url(yql_statement: str) -> 'encoded URL':
    
    ''' constructs a valid, encoded url based on keywords '''

    url_query = [('q', yql_statement), ('format', 'json'), ('env', RETRIEVE_TABLE)]

    mostly_encoded = STARTING_URL + '?' + urllib.parse.urlencode(url_query)

    return mostly_encoded

def get_information_one_company(json_object: 'json') -> tuple:

    # ignore this function
    
    company = json_object['query']['results']['quote']['symbol']
    current_price = json_object['query']['results']['quote']['LastTradePriceOnly']
    trade_date= json_object['query']['results']['quote']['LastTradeDate']

    return (company, current_price, trade_date)

def _get_information_date_price(json_object: 'json') -> dict:

    # gets information from the json and puts it in dictionary, where the key is the date
    # and the value is a list of the close values, and other desired values that can be
    # added later on

    # This is where I start formatting the data, connecting date to the price

    info_dict = dict()

    list_of_quotes = json_object['query']['results']['quote']

    for i in range(len(list_of_quotes)):
        info_dict[list_of_quotes[i]['Date']] = [list_of_quotes[i]['Close']]

    return info_dict
        
def _sort_keys(stock_dict: dict) -> None:

    ''' sorts the keys in the dictionary and returns the formatted string '''

    big_str = ''

    for key in sorted(stock_dict):
        for item in stock_dict[key]:
            big_str += key + ' ' + item + '\n'

    return big_str

def _write_to_file(filename: str, info: str) -> None:

    # Writes any information to the file
    
    try:
        infile = open(filename, 'w')
        infile.write(info)
        infile.close()
        
    except IOError:
        print('File does not exist')


###### PUBLIC FUNCTIONS #########

def run_program(company: str, start: str, end: str, filename: str) -> str:

    statement = _create_YQL_historical_statement(company, start, end)
    url = _create_url(statement)
    json = _process_url(url)
    dictionary = _get_information_date_price(json)
    formatted_str = _sort_keys(dictionary)
    _write_to_file(filename, formatted_str)

   
        
