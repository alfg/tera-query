#!/usr/bin/env python

'''

#### teraQuery.py ####
A simple script to query Tera data by webscraping teracodex.com (and soon others).
Why? Because I was bored one day.

Installation (Ubuntu/Debian):

# apt-get install python-setuptools
# easy_install BeautifulSoup prettytable
# python teraQuery.py

'''
import re
import urllib2
import sys
from prettytable import PrettyTable
from BeautifulSoup import BeautifulSoup

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
        print '\n============================'
        print html.find('div', {'class' : re.compile(r".*\bname\b.*")}).text
        print '============================'

        #If 'text' dom class exists, then print stats
        try:
            ptag = html.find('div', {'class' : 'text'}).findAll('p')

            for i in ptag:
                print i.text

            print '---------------------'
        except:
            pass

        #If 'stats clearfix' class exists
        try:
            ptag = html.find('div', {'class' : 'stats clearfix'}).findAll('div')

            for i in ptag:
                print '==', i.text

            print '---------------------'
        except:
            pass

        #If 'bonus' class exists
        try:
            ptag = html.find('div', {'class' : 'bonus'}).findAll('p')

            for i in ptag:
                print '-', i.text

            print '---------------------'
        except:
            pass

        #If 'crystal' class exists
        try:
            ptag = html.find('div', {'class' : 'crystal'}).findAll('p')

            for i in ptag:
                print '[', i.text.replace('&nbsp;', ''), ']'

            print '---------------------\n'
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
            x.add_row([row.findAll('a')[0]['href'][13:],
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
