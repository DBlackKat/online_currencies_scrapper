# online_currencies_scrapper
Get all the history exchange rates of MYR ---> TWD

    please read through the python code for your need
    all scrap code are set to get the EXCHANGE RATE from malaysia RINGGIT 
    to TAIWAN DOLLAR conversion rate
    
    Library Required:
    Mechanize
    BeautifulSoup
    Numpy
    Pandas

    available scrap source:
        currencies_app.py:
            http://currencies.apps.grandtrunk.net/
        xe_scrapper.py:
            scrap xe website currecies

    How to use:
        execute using python currencies_app.py
        you will be prompted to input the year you wanted to scrap
        Note: if you want to get year 2002 then you should input 2002 and 2003
        
    Issues to resolve:
        return null if the input year is not available
        currrenly use pickle for data dumping which isn't effective at all, should consider changing to json  
        convert the main function to a define function
        
