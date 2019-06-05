from pytrends.request import TrendReq

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

import cbpro

import json

from collections.abc import Iterable

from datetime import datetime, timedelta
import time

timeLoop = 300 # 300 sec = 5 min

def flatten(items):
    """Yield items from any nested iterable; see Reference."""
    for x in items:
        if isinstance(x, Iterable) and not isinstance(x, (str, bytes)):
            for sub_x in flatten(x):
                yield sub_x
        else:
            yield x

now = datetime.now()
currentDay = '%02d' % now.day
currentMonth = '%02d' % now.month
currentYear = now.year
currentHour = '%02d' % now.hour
currentMinute = '%02d' % now.minute
csv_file_name = "data/indicator_" + str(currentYear) + "_" + str(currentMonth) + "_" + str(currentDay) + "_" + str(currentHour) + "_" + str(currentMinute) + ".csv"

indicator = open(csv_file_name,"w")
indicator.write("date,bitcoin,crash,ban,loss,rise,skyrocket,gain,bubble,")
for i in range(50):
    indicator.write("BidPrice" + str(i) + ", BidSize" + str(i) + ",")
for i in range(50):
    indicator.write("AskPrice" + str(i) + ", AskSize" + str(i) + ",")
indicator.write("\r\n")
indicator.close()


while True:
    # Get time for Google Trends search 2 hour span
    now = datetime.now()
    currentDay = now.day
    currentMonth = now.month
    currentYear = now.year
    currentHour = now.hour
    before = now - timedelta(hours=2)
    beforeDay = before.day
    beforeMonth = before.month
    beforeYear = before.year
    beforeHour = before.hour

    # Open Public connection CoinBase Pro 
    public_client = cbpro.PublicClient()

    # Init Trend settings
    pytrend = TrendReq()
    bad =['bitcoin', 'crash', 'ban', 'loss']
    good =['bitcoin', 'rise', 'skyrocket', 'gain', 'bubble']

    
        # BAD TREND
    historical_interest_bad = pytrend.get_historical_interest(bad, year_start=beforeYear, month_start=beforeMonth, day_start=beforeDay, hour_start=beforeHour, year_end=currentYear, month_end=currentMonth, day_end=currentDay, hour_end=currentHour, cat=0, geo='', gprop='', sleep=0)
    historical_interest_bad = historical_interest_bad.drop(labels='isPartial', axis=1) # Delete isPartial
    historical_interest_bad.insert(0, 'TimeStamp', pd.datetime.now().replace(microsecond=0)) # Insert time
    

        # GOOD TREND
    historical_interest_good = pytrend.get_historical_interest(good, year_start=beforeYear, month_start=beforeMonth, day_start=beforeDay, hour_start=beforeHour, year_end=currentYear, month_end=currentMonth, day_end=currentDay, hour_end=currentHour, cat=0, geo='', gprop='', sleep=0)
    historical_interest_good = historical_interest_good.drop(labels='bitcoin', axis=1) # Delete bitcoin
    historical_interest_good = historical_interest_good.drop(labels='isPartial', axis=1) # Delete isPartial
    
    
    

        # Query CoinBase Pro ORDER BOOK
    data = public_client.get_product_order_book('BTC-USD', level=2)

    lBids = data['bids'] # get Bids
    lBids = list(flatten(lBids)) # One dimension
    lBids = [float(i) for i in lBids] # Cast str to float
    del lBids[2::3] # Delete Order Index (Redundancy)
    dfBids = pd.DataFrame(lBids) # Transform to DataFrame
    dfBids = dfBids.T # Transpose
    
    lAsks = data['asks'] # get Asks
    lAsks = list(flatten(lAsks)) # One dimension
    lAsks = [float(i) for i in lAsks] # Cast str to float
    del lAsks[2::3] # Delete Order Index (Redundancy)
    dfAsks = pd.DataFrame(lAsks) # Transform to DataFrame
    dfAsks = dfAsks.T # Transpose
    


    # Write all in CSV
    historical_interest_bad.to_csv(csv_file_name, mode='a', header=False, index=False, line_terminator=',') # Time + Bad Trend
    historical_interest_good.to_csv(csv_file_name, mode='a', header=False, index=False, line_terminator=',') # Good Trend
    dfBids.to_csv(csv_file_name, mode='a', header=False, index=False, line_terminator=',') # Order Book Bids
    dfAsks.to_csv(csv_file_name, mode='a', header=False, index=False) # Order Book Asks

    time.sleep(timeLoop) # 300 sec = 5 min

