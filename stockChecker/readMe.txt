# stockChecker

# written by Jansen Yan, 12/20/15
# for yahoo developers

# The function of this program:

# input: takes company, startDate and endDate
# creates proper YQL statement based on an existing global str
# requests and processes URL into json content
# parses json content for each day's stock quote
# writes stock quotes to a text file

# There are two modules to this program:

# stockChecker.py, which requests the url content, formats the content and writes to file
# stockChecker_View.py which asks for user input

# stockChecker_View.py is the executable, you won't be able to run
# the program without python 3.4.3 downloaded 