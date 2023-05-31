from app_store_scraper import AppStore
from google_play_scraper import app, Sort, reviews_all
from pprint import pprint #print objects in a formatted way
import pandas as pd
import numpy as np
import datetime as datetime
import os
import csv
import nltk
from textblob import TextBlob
import nltk
import requests

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
trigramNum=20
posEntries=0
negEntries=0
undefined=0
hash_map = {}#hash map for the review words
#hash map format: index: (rating, review)

#date declaration
inputYear=int(input("Enter Year: "))
inputMonth= int(input("Month: "))
inputDay=int(input("Day: "))
threshold=4

#variables from user input
appName="genshin impact"
#appName=input("enter App Name: ")
appCountry="us"

#setup NLP stuff
stop_words = set(stopwords.words('english'))
stop_words.update(['app', appName, 'stars', 'great', 'good'])

timelowerBounds=datetime.datetime(inputYear-1,inputMonth, inputDay)
print(timelowerBounds)
timeInput=datetime.datetime(inputYear,inputMonth,inputDay) 

beforeUpdate = AppStore(country=appCountry, app_name=appName) #creates object called "FIRST APP" for the US and an application name


appID=str(beforeUpdate.app_id)

app_url = "https://apps.apple.com/app/"+appID
response = requests.get(app_url)
soup = BeautifulSoup(response.content, "html.parser")

overallRating_element = soup.find('span', {'class': 'we-customer-ratings__averages__display'})
overallRating = overallRating_element.text
print(overallRating)

scrapenumRating = soup.find('figcaption', class_='we-rating-count')
# Extract the rating count
totalnumRating = scrapenumRating.text.strip().split(' ')[-2]

if totalnumRating.find('K') != -1:
    totalnumRating=totalnumRating.replace('K','')
    totalnumRating = int(float(totalnumRating) * 1000)
elif totalnumRating.find('M') != -1:
    totalnumRating=totalnumRating.replace('M','')
    totalnumRating = int(float(totalnumRating) * 1000000)
else:
    totalnumRating = int(float(totalnumRating))
print(totalnumRating)
#using slovins formula, determine appropriate sample size
reviewNum=int(totalnumRating/(1+(totalnumRating*(.03**2)))) #4% margin of error
print(reviewNum)
beforeUpdate.review(how_many=reviewNum) #review is an element of the object that contains the dictionary of data


#pprint(firstapp.reviews)
counter=0
reviewArr=[]

for element in beforeUpdate.reviews :
    if (counter < reviewNum):
        #print(element["rating"])
        if ((timelowerBounds<element["date"] < timeInput) & (element["rating"] <=4)):
            #print(element["rating"])
            #print(element["review"])
            hash_map[counter]=(element["rating"], element["review"]) 
            reviewArr.append(element["review"].lower().replace(',',' '))

            counter+=1
    else:
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
most_common_trigrams = trigram_counts.most_common(trigramNum) #contains dictionary 20 

# Count the occurrences of each word
# Print the most common trigrams and their counts
for trigram, count in most_common_trigrams:
    print(f"{' '.join(trigram)}: {count}")

#create dictionary here?
#iterate through trigrams and determine the date of each
upperBounds=len(reviewArr)
print(upperBounds)
for trigram, count in most_common_trigrams:
    iterator=count
    index=0
    while ((index<(upperBounds))&(iterator>0)):
        #print(index)
        #print(hash_map[index])
        if reviewArr[index].find(str(trigram))!=-1:
            iterator-=1
        index+=1
        #turn review arr into a dictionary?

        


pprint(beforeUpdate.reviews_count)
