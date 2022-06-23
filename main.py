#Plotting Sentiment's of Twitter Users
from functions import *

import numpy as np
import pandas as pd
import datetime as dt
import re

import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.dates import DateFormatter
import seaborn as sns
# sns.set()

import GetOldTweets3 as got
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

# Confirm that input is correct
re_enter = True
while re_enter:
    username = get_username()
    dates = get_date()
    start = dates[0]
    end = dates[1]
    print(f"Grabbing @{username}'s tweets from {dates[0]} to {dates[1]}. Continue? [Y/N]")
    response = input()
    incorrect_response = True
    while incorrect_response:
        if response == 'Y':
            incorrect_response = False
            re_enter = False
        elif response == 'N':
            incorrect_response = False
            re_enter = True
        else:
            print("Please enter 'Y' if you would like to continue or 'N' if you would like to reenter")
            incorrect_response = True
            response = input()

data = get_tweets(username, start, end)
analyzed_data = analyze_sentiment(data)
grouped_data = aggregate_data(analyzed_data, ['compound'], np.mean)

average_sentiment = np.mean(grouped_data['compound'])

days = mdates.DayLocator()

plt.figure(figsize = (16, 9))
ax = sns.lineplot(x = grouped_data.index, y = 'compound', data = grouped_data)
ax.set_xlim([dt.datetime.strptime(start, "%Y-%m-%d"), dt.datetime.strptime(end, "%Y-%m-%d")])
ax.set_ylim([-1,1])
ax.xaxis.set_minor_locator(days)
plt.gcf().autofmt_xdate()
plt.ylabel('Compound Score')
plt.xlabel('Date')
plt.title(f"Average Daily Compound Sentiment Scores - @{username} from {start} to {end}.")
plt.savefig('compound.png', format='png', dpi=300)
