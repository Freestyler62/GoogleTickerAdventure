# -*- coding: utf-8 -*-
"""
Created on Sun Jun 28 18:23:47 2015

@author: Bobster

This is my first serious python project edited for test. The aim is to be able to develop a utility that can extract real
time stocks/shares information from the internet. Or in other words a share price tracker.
"""
print 'Hello there. Welcome to Varghese Ltd. This is the stocks/share price tracker.'

import time, os, re, csv
import requests


def fetch_quote(ticker):
    "Get a quote from Google Finance for the ticker."

    url = "http://www.google.com/finance?&q="
    response = requests.get(url + ticker)
    if response.status_code != 200:
        raise requests.ConnectionError("HTTP response is not 200")
    html_content = response.content
    
    regexp = re.search('id="ref_(.*?)">(.*?)<', html_content)
    if regexp:
        tmp = regexp.group(2)
        quote = tmp.replace(',', '')
    else:
        quote = "Nothing found for: " + googleticker
    
    return quote


def make_csv_row(ticker):
    "Output a list that includes time and quote info."

    quote = fetch_quote(ticker)  # Use the core-engine function
    t = time.localtime()     # Grasp the moment of time
    output = [t.tm_year, t.tm_mon, t.tm_mday, t.tm_hour,  # Build a list
              t.tm_min, t.tm_sec, ticker, quote]
    return output


if __name__ == '__main__':

    tickers = ["AAPL"]

    # Define file name of the output record
    fname = "aapl.dat"

    # Display time corresponding to your location
    print(time.ctime())
    print
     
    # Set local time zone to NYC
    os.environ['TZ'] = 'America/New_York'
    time.tzset()
    t = time.localtime()  # String
    print(time.ctime())
    print

    freq = 2  # Fetch data every 600 sec (10 min)

    with open(fname, 'a') as f:
        writer = csv.writer(f, dialect="excel")
        while(t.tm_hour <= 16):
            if(t.tm_hour == 16):
                while(t.tm_min < 01):
                    data = make_csv_row(ticker)
                    print(data)
                    writer.writerow(data)  # Save data in the file
                    time.sleep(freq)
                else:
                    break
            else:
                for ticker in tickers:
                    data = make_csv_row(ticker)
                    print(data)
                    writer.writerow(data)  # Save data in the file
                    time.sleep(freq)
