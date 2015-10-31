# -*- coding: utf-8 -*-
"""
Created on Sun Jun 28 18:23:47 2015

@author: Bobster

This is my first serious python project edited for test. The aim is to be able
to develop a utility that can extract real time stocks/shares information from
the internet. Or in other words a share price tracker.
"""

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
        quote = "Nothing found for: " + ticker
    
    return quote


def make_csv_row(ticker):
    "Output a list that includes time and quote info."

    quote = fetch_quote(ticker)  # Use the core-engine function
    t = time.localtime()         # Grasp the moment of time
    output = [t.tm_year, t.tm_mon, t.tm_mday, t.tm_hour,  # Build a list
              t.tm_min, t.tm_sec, ticker, quote]
    return output


if __name__ == '__main__':

    print ('Hello there. Welcome to Varghese Ltd. This is the stocks/share '
           'price tracker.')

    tickers = ["AAPL"]

    # Define file name of the output record
    output_filename = "aapl.dat"

    # Display the time
    t = time.localtime()  # String
    print(time.ctime())
    print

    delay_between_calls = 2  # Fetch data every 600 sec (10 min)

    with open(output_filename, 'a') as output_file:
        writer = csv.writer(output_file, dialect="excel")
        while(t.tm_hour <= 16):
            t = time.localtime()
            if(t.tm_hour == 16):
                while(t.tm_min < 01):
                    row_data = make_csv_row(ticker)
                    print(row_data)
                    writer.writerow(row_data)  # Save data in the file
                    time.sleep(delay_between_calls)
                else:
                    break
            else:
                for ticker in tickers:
                    row_data = make_csv_row(ticker)
                    print(row_data)
                    writer.writerow(row_data)  # Save data in the file
                    time.sleep(delay_between_calls)
