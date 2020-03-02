import tika
import csv
import requests
from bs4 import BeautifulSoup
import re
import sqlite3 as sql

def run():
    fileLocale = input('PDF name: ')
    parsed = readPDF(fileLocale)
    getRoutines(parsed)

def readPDF(fileLocation):
    """Upon retrieving PDFs listed on the eventlist returned from getEvents, will parse them to get the data necessary.
        Data will be sent in JSON format to another function to be committed to the SQLite database."""
    return tika.parser.from_file(fileLocation)['content']

def getEvents(url):
    """Function for retrieving the event results of all events easily accesible on the ISU website.
        Will return a list of strings representing the URLs where the different sections (male/female/junior/senior)
        can be found."""
    soup = BeautifulSoup(requests.get(url).content)
    rows = soup.find_all('tr')
    eventList = []
    for row in rows:
        #link = row.find('a')['href']
        if row.find('a'):
            event = row.find('a')['href']
            #? Newer links on the results page lead to the event page which then links to the specific event's results page.
            #?  This nested if handles such occasions as well as when no results are found for an event.
            if 'events' in event:
                tempSoup = BeautifulSoup(requests.get(event).content)
                event = tempSoup.find('a', text=re.compile('Result Details'))
                if event:
                    eventList.append(event['href'])
            eventList.append(event)
    return eventList
    
def parseEvent(listings):
    """Should grab the PDFs from the eventlist and pass them to the PDF reader function."""
    pass

def getRoutines(rawString):
    routines = rawString.split('Total\n\nDeductions')
    print(routines[1] + '\n' + routines[2])
    for routine in routines:
        routine = routine.replace('Total\n\nDeductions', '').strip()

if __name__ == "__main__":
    run()