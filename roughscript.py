from app_store_scraper import AppStore
from google_play_scraper import app, Sort, reviews_all
from pprint import pprint #print objects in a formatted way
import pandas as pd
import numpy as np
import datetime as datetime
import openai
import os
import csv
import nltk
from textblob import TextBlob
import nltk
import requests
import re
import string
from bs4 import BeautifulSoup 
import collections
import pandas as pd
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.util import ngrams


# Download the stopwords if not already downloaded
nltk.download('stopwords')
nltk.download('punkt')

#counters
posEntries=0
negEntries=0
undefined=0
hash_map = {}#hash map for the review words

#date declaration
inputYear=int(input("Enter Year: "))
inputMonth= int(input("Month: "))
inputDay=int(input("Day:"))
threshold=5

#variables from user input
appName="zelle"
#appName=input("enter App Name: ")
appCountry="us"
reviewNum=2000


#setup NLP stuff
stop_words = set(stopwords.words('english'))
stop_words.update(['app', appName, 'stars'])

timelowerBounds=datetime.datetime(inputYear-1,inputMonth, inputDay)
timeInput=datetime.datetime(inputYear,inputMonth,inputDay) 

beforeUpdate = AppStore(country=appCountry, app_name=appName) #creates object called "FIRST APP" for the US and an application name
beforeUpdate.review(how_many=reviewNum) #review is an element of the object that contains the dictionary of data

appID=str(beforeUpdate.app_id)

app_url = "https://apps.apple.com/app/"+appID
response = requests.get(app_url)
soup = BeautifulSoup(response.content, "html.parser")

scrapeRating=soup.find("div", {"class": "we-customer-ratings__averages"})
overallRating_element = soup.find('span', {'class': 'we-customer-ratings__averages__display'})
overallRating = overallRating_element.text
print(overallRating)
#pprint(firstapp.reviews)
counter=0
reviewArr=[]



for element in beforeUpdate.reviews :
    if (counter < 200):
        #print(element["rating"])
        if ((timelowerBounds<element["date"] < timeInput) & (element["rating"] <=4)):
            print(element["rating"])
            print(element["review"])
            reviewArr.append(element["review"].lower().replace(',',' '))
            counter+=1
    else:
       print(counter)
       break

#pandas data frame
data = pd.DataFrame({'Phrases': reviewArr})
most_common_phrases = data['Phrases'].value_counts()
subset = data['Phrases'].head(counter)
all_text = ' '.join(subset)

# Split the text into individual words
words = all_text.split()

filtered_words = [word for word in words if word.lower() not in stop_words]
trigrams = list(ngrams(filtered_words, 3)) #modify tbis to get phrase amount

# Count the occurrences of each trigram
trigram_counts = collections.Counter(trigrams)

# Get the three most common trigrams
most_common_trigrams = trigram_counts.most_common(15)

# Count the occurrences of each word
# Print the most common trigrams and their counts
for trigram, count in most_common_trigrams:
    print(f"{' '.join(trigram)}: {count}")
    


'''   for word in blob.words:
# Calculate the polarity of the word
        word_polarity = TextBlob(word).sentiment.polarity
        print(f"{word}: {word_polarity}")
        '''



    #perform nlp analysis
pprint(beforeUpdate.reviews_count)