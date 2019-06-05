from pytrends.request import TrendReq

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

import cbpro

import json

from collections.abc import Iterable

from datetime import datetime, timedelta


def flatten(items):
    """Yield items from any nested iterable; see Reference."""
    for x in items:
        if isinstance(x, Iterable) and not isinstance(x, (str, bytes)):
            for sub_x in flatten(x):
                yield sub_x
        else:
            yield x


pytrend = TrendReq()

bad =['bitcoin', 'crash', 'ban', 'loss']

good =['bitcoin', 'rise', 'skyrocket', 'gain', 'bubble']

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




# print("BAD GOOGLE TREND:")
historical_interest_bad = pytrend.get_historical_interest(bad, year_start=beforeYear, month_start=beforeMonth, day_start=beforeDay, hour_start=beforeHour, year_end=currentYear, month_end=currentMonth, day_end=currentDay, hour_end=currentHour, cat=0, geo='', gprop='', sleep=0)
print(historical_interest_bad)
historical_interest_bad = historical_interest_bad.drop(labels='isPartial', axis=1) 
shortBad = historical_interest_bad.sum(axis = 0, skipna = True)
# print(shortBad)
historical_interest_bad.to_csv("historical_interest_bad.csv", sep=',')
dfBad = pd.read_csv('historical_interest_bad.csv', skiprows=1, index_col='date', names=['date', 'bitcoin', 'crash', 'ban', 'loss'])
dfBad.plot()
plt.show()

# print("GOOD GOOGLE TREND:")
# historical_interest_good = pytrend.get_historical_interest(good, year_start=beforeYear, month_start=beforeMonth, day_start=beforeDay, hour_start=beforeHour, year_end=currentYear, month_end=currentMonth, day_end=currentDay, hour_end=currentHour, cat=0, geo='', gprop='', sleep=0)
# historical_interest_good = historical_interest_good.drop(labels='isPartial', axis=1) 
# shortGood = historical_interest_good.sum(axis = 0, skipna = True)
# #print(shortGood)
# historical_interest_good.to_csv("historical_interest_good.csv", sep=',')
# dfGood = pd.read_csv('historical_interest_good.csv', skiprows=1, index_col='date', names=['date', 'bitcoin', 'rise', 'skyrocket', 'gain', 'bubble'])
# dfGood.plot()
# plt.show()


public_client = cbpro.PublicClient()

data = public_client.get_product_order_book('BTC-USD', level=2)
with open('data.txt', 'w') as outfile:  
    json.dump(data, outfile, indent=4)


l = data['bids']
l = list(flatten(l))
l = [float(i) for i in l]

