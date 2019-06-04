from pytrends.request import TrendReq

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

pytrend = TrendReq()

bad =['bitcoin', 'crash', 'ban', 'loss']

good =['bitcoin', 'rise', 'skyrocket', 'gain', 'bubble']

#pytrend.build_payload(bad)

#interest_over_time_df = pytrend.interest_over_time()
#print(interest_over_time_df.head())

print("BAD GOOGLE TREND:")
historical_interest_bad = pytrend.get_historical_interest(bad, year_start=2019, month_start=3, day_start=1, hour_start=0, year_end=2019, month_end=3, day_end=5, hour_end=0, cat=0, geo='', gprop='', sleep=0)
#print(historical_interest_bad)
historical_interest_bad = historical_interest_bad.drop(labels='isPartial', axis=1) 
shortBad = historical_interest_bad.sum(axis = 0, skipna = True)
#print(shortBad)

#print("GOOD GOOGLE TREND:")
#historical_interest_good = pytrend.get_historical_interest(good, year_start=2019, month_start=3, day_start=1, hour_start=0, year_end=2019, month_end=4, day_end=5, hour_end=0, cat=0, geo='', gprop='', sleep=0)
#shortGood = historical_interest_good.sum(axis = 0, skipna = True)
#print(shortGood)

historical_interest_bad.to_csv("historical_interest_bad.csv", sep=',')

df = pd.read_csv('historical_interest_bad.csv', skiprows=1, index_col='date', names=['date', 'bitcoin', 'crash', 'ban', 'loss'])

df.plot()
plt.show()