import math
import requests, json, tweepy
from credentials import *
from datetime import datetime
import os.path

def get_least_used_emoji():
    url = "http://emojitracker.com/api/rankings"

    response = requests.request("GET", url)

    data = json.loads(response.text)

    return data[-1]

def update_profile_image(jsonData):
    name = jsonData['name'].lower().replace(' ', '-')
    id = jsonData['id'].lower()

    url = "https://abs.twimg.com/emoji/v2/72x72/%s.png" % id

    response = requests.get(url)
    if response.status_code == 200:
        with open("icon.png", 'wb') as f:
            f.write(response.content)
    api.update_profile_image("icon.png")

def get_emoji_char(jsonData):
    return chr(int(jsonData['id'], 16))

def get_emoji_name(jsonData):
    return jsonData['name'].capitalize()

def compare_results(emojiName, emojiChar):
    resultsPath = "results.txt"
    if (os.path.exists(resultsPath)):
        with open("results.txt", "r") as f:
            current, initialTime = f.readline().split(" ")
            initialTime = datetime.fromtimestamp(int(initialTime))
        if (current == emojiChar):
            timeStanding = datetime.utcnow() - initialTime
            daysStanding = timeStanding.days
            if daysStanding > 1:
                return "%s (%s) has been the least used emoji for %i days" %(emojiChar, emojiName, daysStanding)
        else:
            with open("results.txt", 'w') as f:
                resultsText = str(emojiChar) + " " + str(math.floor(datetime.utcnow().timestamp()))
                f.write(resultsText)
            return "The least used emoji is now: %s (%s)" % (leastUsedEmojiChar, leastUsedEmojiName)

    return "The least used emoji is currently: %s (%s)" % (leastUsedEmojiChar, leastUsedEmojiName)


# Access and authorize our Twitter credentials from credentials.py
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)

leastUsedEmojiData = get_least_used_emoji()
leastUsedEmojiChar = get_emoji_char(leastUsedEmojiData)
leastUsedEmojiName = get_emoji_name(leastUsedEmojiData)


tweetText = compare_results(leastUsedEmojiName, leastUsedEmojiChar)


update_profile_image(leastUsedEmojiData)

try:
    api.update_status("The least used emoji is currently: %s (%s)" % (leastUsedEmojiChar, leastUsedEmojiName))
except tweepy.TweepError as e:
    print(e.reason)

try:
    api.update_status(leastUsedEmojiChar * 140)
except tweepy.TweepError as e:
    print(e.reason)
