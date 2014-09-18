#!/usr/bin/env python

'''

#### teraQuery.py ####
A simple script to query Tera data by webscraping teracodex.com (and soon others).
Why? Because I was bored one day.

Installation (Ubuntu/Debian):

# apt-get install python-setuptools
# pip install prettytable==0.5 BeautifulSoup
# python teraQuery.py

'''
import re
import urllib2
import sys
import readline
from prettytable import PrettyTable
from BeautifulSoup import BeautifulSoup

class bcolors:
    ''' Terminal Colors! '''

    HEADER = '\033[94m'
    BLUE = '\033[96m'
    GREEN = '\033[92m'
    PURPLE = '\033[93m'
    YELLOW = '\033[33m'
    RED = '\033[91m'
    WHITE = '\033[37m'
    ENDC = '\033[0m'

    def disable(self):
        self.HEADER = ''
        self.BLUE = ''
        self.GREEN = ''
        self.PURPLE = ''
        self.RED = ''
        self.ENDC = ''


def queryTera():
    #Ask user for query
    query = raw_input("Enter a search term or item ID: ")
    print "Querying " + query + "..."
    query = query.replace(" ", "+")

    #If user input is a number, then look for an item id
    if query.isdigit() == True:
        #query html
        html = BeautifulSoup(urllib2.urlopen('http://teracodex.com/item.php?id=%s' % query).read())

        #Render output nicely
        print '\n======================================='
        print '     ' + bcolors.HEADER + html.find('div', {'class' : re.compile(r".*\bname\b.*")}).text + bcolors.ENDC
        print '======================================='

        #If 'text' dom class exists, then print stats
        try:
            ptag = html.find('div', {'class' : 'codex-tooltip-details'}).findAll('p')

            for i in ptag:
                print bcolors.WHITE + ' ' + i.text + bcolors.ENDC

            print '---------------------------------------'
        except:
            pass

        #If 'stats clearfix' class exists
        try:
            ptag = html.find('table', {'class' : 'codex-tooltip-stats'}).findAll('td')

            for i in ptag:
                print bcolors.GREEN + '-', i.text + bcolors.ENDC

            print '---------------------------------------'
        except:
            pass

        #If 'bonus' class exists
        try:
            ptag = html.find('div', {'class' : 'codex-tooltip-bonus-normal'}).findAll('p')

            for i in ptag:
                print bcolors.YELLOW + '-', i.text + bcolors.ENDC

            print '---------------------------------------'
        except:
            pass

        #If 'crystal' class exists
        try:
            ptag = html.find('div', {'class' : 'codex-tooltip-crystal'}).findAll('p')

            for i in ptag:
                print bcolors.BLUE + '[', i.text.replace('&nbsp;', ''), ']' + bcolors.ENDC

            print '---------------------------------------\n'
        except:
            pass

    #If user input is not a number, then run a search
    elif query.isdigit() == False:

        #Make query to search form
        html = BeautifulSoup(urllib2.urlopen('http://teracodex.com/search.php?q=%s' % query).read())

        #Initialize pretty table
        x = PrettyTable(["ID", "Item Name", "Level", "Type", "Usable", "Obtained"])
        x.set_field_align("Item Name", "l")
        x.set_padding_width(1)

        #Gather data and enter into pretty rows
        for row in html('table', {'class' : 'itemList itemsearch'})[0].tbody('tr'):
            x.add_row([row.findAll('a')[0]['rel'],
                        row.findAll('a')[0].text,
                        row.findAll('td')[1].text,
                        row.findAll('td')[2].text,
                        row.findAll('td')[3].text,
                        row.findAll('td')[4].text])

        #Self explanitory
        print x

    else:
        "Ruh Roh"

#Launch queryTera if invoked from interpreter
if __name__ == "__main__":
    while True:
        try:
            queryTera()
        except KeyboardInterrupt:
            print "\n Bye"
            sys.exit()
        except IndexError:
            print "No results found. Try another query or press Ctrl+C to quit."

