# functions

import numpy as np
import pandas as pd
import datetime as dt
import re

import matplotlib.pyplot as plt
import seaborn as sns

import GetOldTweets3 as got
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

def get_username():
    print("Input a Twitter handle...")
    username = input()
    return username

def get_date():
    output = []

    # Check format of date input
    def bad_format(date):
        pattern = r"[\d]{4}-[\d]{2}-[\d]{2}"
        if re.search(pattern, date) == None:
            print("Entered date is invalid format, please enter a new date...")
            return True
        else:
            return False
    # Check that date is a real date
    def bad_date(date):
        try:
            date = dt.datetime.strptime(date, "%Y-%m-%d")
        except:
            print("Entered date is invalid format, please enter a new date...")
            return True
        else:
            return False
    # Check that dates are not in the future
    def bad_time(date):
        if dt.datetime.strptime(date, "%Y-%m-%d") > dt.datetime.now():
            print("Entered date cannot be in the future, please enter a new date...")
            return True
        else:
            return False
    # Check that ending date is later than beginning date
    def bad_end_date(date):
        if dt.datetime.strptime(start, "%Y-%m-%d") > dt.datetime.strptime(end, "%Y-%m-%d"):
            print("End date cannot be later than start date, please enter a new date...")
            return True
        else:
            return False
    # Starting date
    print("Input a start date as 'YYYY-MM-DD'")
    start = input()
    while bad_format(start) or bad_date(start) or bad_time(start):
        start = input()
    output.append(start)
    # Ending date
    print("Input an end date as 'YYYY-MM-DD'")
    end = input()
    while bad_format(end) or bad_date(end) or bad_time(end) or bad_end_date(end):
        end = input()
    output.append(end)
    # Return is of the form [start date, end date]
    return output

# Get the dataframe of their tweets
def get_tweets(user, start, end):
    # specifying search criteria
    tweet_criteria = got.manager.TweetCriteria().setUsername(user)\
                                                .setSince(start)\
                                                .setUntil(end)\
    # scraping tweets
    tweets = got.manager.TweetManager.getTweets(tweet_criteria)
    # creating the dataframe
    tweet_texts = [[tw.username,
                    tw.text,
                    tw.date,
                    tw.retweets,
                    tw.favorites,
                    tw.mentions,
                    tw.hashtags,
                    tw.geo] for tw in tweets]

    df = pd.DataFrame(tweet_texts, columns = ["User", "Text", "Date", \
    "Retweets", "Favorites", "Mentions", "Hashtags", "Geo"])
    return df

# Perform sentiment analysis and return a copy of the dataframe with sentiment included
def analyze_sentiment(data):
    analyzer = SentimentIntensityAnalyzer()
    analyzed_text = [analyzer.polarity_scores(tweet) for tweet in data["Text"]]
    copy = data.copy()
    copy["compound"] = [i['compound'] for i in analyzed_text]
    copy["pos"] = [i["pos"] for i in analyzed_text]
    copy["neu"] = [i["neu"] for i in analyzed_text]
    copy["neg"] = [i["neg"] for i in analyzed_text]
    return copy



def aggregate_data(df, cols, func):
    copy = df.copy()
    copy["day"] = [i.date() for i in copy['Date']]
    data_grouped = copy.groupby("day")[cols].agg(func)
    return data_grouped
