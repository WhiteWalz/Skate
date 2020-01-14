from tika import parser
import csv
import requests
import bs4

def run():
    fileLocale = input('PDF name: ')
    parsed = readPDF(fileLocale)
    getRoutines(parsed)

def readPDF(fileLocation):
    return parser.from_file(fileLocation)['content']

def getEvents(url):
    soup = bs4.BeautifulSoup(requests.get(url).content)
    rows = soup.find_all('tr')
    eventList = []
    for row in rows:
        if row.find('a'):
            eventList.append(row.find('a')['href'])
    return eventList
    
def parseEvent(listings):
    pass

def getRoutines(rawString):
    routines = rawString.split('Total\n\nDeductions')
    print(routines[1] + '\n' + routines[2])
    for routine in routines:
        routine = routine.replace('Total\n\nDeductions', '').strip()

if __name__ == "__main__":
    run()