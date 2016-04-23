import pandas as pd
import mechanize
import numpy as np
from bs4  import BeautifulSoup
import os, re, pickle, sys, datetime,time

def initMechanize():
    br = mechanize.Browser()
    br.set_handle_robots(False)
    br.addheaders = [('User-agent', 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1')]
    return br

def getExchangeRate(br,date,fromCurrency,toCurrency):
    url = "http://currencies.apps.grandtrunk.net/getrate/"+date+"/"+fromCurrency +"/"+toCurrency
    br.open(url)
    html_source = br.response().read()
#    text_file = open("temp.txt","w")
#    text_file.write(html_source)
#    text_file.close()
    exchange = BeautifulSoup(html_source)
    rate = exchange.body.string
    return float(rate)

if __name__== '__main__': # this need to be later converted i a function
    starting_year = "2000"
    ending_year = "2001"

    outDir = os.path.join( os.getcwd(),'exchangeDatabase') # dir for all inputs and outputs
    if not os.path.exists(outDir):
        os.makedirs(outDir)

    br = initMechanize()
    start = datetime.datetime.strptime("01-01-"+starting_year,"%d-%m-%Y")
    end = datetime.datetime.strptime("01-01-"+ending_year,"%d-%m-%Y")
    date_generated = [start + datetime.timedelta(days=x) for x in range(0, (end-start).days)]

    exchange_dict = dict()
    index = []

    for idx,date in enumerate(date_generated):
        index.append(idx)
        rate = getExchangeRate(br,date.strftime("%Y-%m-%d"),"myr","twd")
        sys.stdout.write( 'Scraping: {}... '.format(date.strftime("%Y-%m-%d")) )
        if "date" in exchange_dict:
            exchange_dict["date"].append(date.strftime("%Y-%m-%d"))
            exchange_dict["rates"].append(rate)
        else:
            exchange_dict["date"] = [date.strftime("%Y-%m-%d")]
            exchange_dict["rates"] = [rate]
        time.sleep(1)
        sys.stdout.write( '\n' )
    df = pd.DataFrame(data=exchange_dict,index = index)
    df.to_pickle(outDir+"/"+starting_year+"-"+ending_year+".p")