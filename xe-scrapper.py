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
    fromCurrency = fromCurrency.upper()
    url = "http://www.xe.com/currencytables/?from="+fromCurrency+"&date="+date
    br.open(url)
    html_source = br.response().read()
    exchange = BeautifulSoup(html_source)
    exchange = exchange.find('table',{'id':'historicalRateTbl'})
    tr_soup = exchange.find_all('tr')
    for tr in tr_soup[2:]:
        if toCurrency.upper() in str(tr):
            td = tr.find_all('td')
            rate = td[2].string
            return float(rate)

if __name__== '__main__': # this need to be later converted i a function
    starting_year = raw_input("Input the starting year ")
    ending_year = raw_input("Input the ending year ")
    sys.stdout.write("\nThe starting year {}\n".format(starting_year))
    sys.stdout.write("\n The ending year {}\n".format(ending_year))

    outDir = os.path.join( os.getcwd(),'xeDatabase') # dir for all inputs and outputs
    if not os.path.exists(outDir):
        os.makedirs(outDir)
    print("\n")
    br = initMechanize()
    start = datetime.datetime.strptime("01-01-"+starting_year,"%d-%m-%Y")
    end = datetime.datetime.strptime("01-01-"+ending_year,"%d-%m-%Y")
    date_generated = [start + datetime.timedelta(days=x) for x in range(0, (end-start).days)]
    checkFileExist = os.path.join(outDir,starting_year+"-"+ending_year+".p")

    if not os.path.exists(checkFileExist):
        exchange_dict = dict()
        index = []
        for idx,date in enumerate(date_generated):
            index.append(idx)
            rate = getExchangeRate(br,date.strftime("%Y-%m-%d"),"myr","twd")
            print 'Scraping: {}... \r'.format(date.strftime("%Y-%m-%d")),
            sys.stdout.write("\033[F")
            if "date" in exchange_dict:
                exchange_dict["date"].append(date.strftime("%Y-%m-%d"))
                exchange_dict["rates"].append(rate)
            else:
                exchange_dict["date"] = [date.strftime("%Y-%m-%d")]
                exchange_dict["rates"] = [rate]
            time.sleep(5)
            sys.stdout.write( '\n' )
        df = pd.DataFrame(data=exchange_dict,index = index)
        df.to_pickle(outDir+"/"+starting_year+"-"+ending_year+".p")
    else:
        sys.stdout.write('File already exist')