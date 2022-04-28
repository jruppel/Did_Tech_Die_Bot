from datetime import date, datetime
import random
import time
import tweepy
import constants
import did_tech_die

# Authenticate to Twitter
consumer_key = constants.twitter_consumer_key
consumer_secret = constants.twitter_consumer_secret
access_token = constants.twitter_access_token
access_token_secret = constants.twitter_access_token_secret
bearer_token = constants.twitter_bearer_token
client = tweepy.Client(bearer_token=bearer_token, consumer_key=consumer_key,consumer_secret=consumer_secret,access_token=access_token,access_token_secret=access_token_secret)

Y = 2000 # dummy leap year to allow input X-02-29 (leap day)
seasons = [('winter', (date(Y,  1,  1),  date(Y,  3, 20))),
           ('spring', (date(Y,  3, 21),  date(Y,  6, 20))),
           ('summer', (date(Y,  6, 21),  date(Y,  9, 22))),
           ('autumn', (date(Y,  9, 23),  date(Y, 12, 20))),
           ('winter', (date(Y, 12, 21),  date(Y, 12, 31)))]
winter_sports = {'football', 'mens-basketball', 'womens-basketball', 'baseball', 'softball', 'womens-tennis'}
spring_sports = {'mens-basketball', 'womens-basketball', 'baseball', 'softball', 'womens-tennis'}
summer_sports = {'football', 'womens-volleyball'}
autumn_sports = {'football', 'mens-basketball', 'womens-basketball', 'womens-volleyball', 'womens-tennis'}

#Get season to only tweet sports that are in-season
def get_season():
    now = date.today()
    if isinstance(now, datetime):
        now = now.date()
    now = now.replace(year=Y)
    return next(season for season, (start, end) in seasons
                if start <= now <= end)

#Check for tweet duplication before tweeting
def is_tweet_duplicate(recent_tweets, new_tweet):
    print("Checking if tweet already exists...")
    if recent_tweets != None:
        for tweet in range(len(recent_tweets)):
            if recent_tweets[tweet]["text"] == new_tweet:
                print("Duplicate tweet exists! No tweets to create!\n")
                return True
    print("Tweet does not exist!\n")
    return False

def create_sport_tweets(sport):
    delay = random.randint(3, 15)
    time.sleep(delay)
    print("----------------------------------------------------------------------------------------")
    print("Checking for recent {} games...".format(sport))
    url = did_tech_die.get_sport_url(sport)
    games = did_tech_die.get_game_data(url, sport)
    if games is not None:
        for game in range(len(games)):
            print("Checking if {} game {} is final...".format(sport, game+1))
            game_is_final = did_tech_die.is_game_final(games[game])
            if game_is_final:
                is_duplicate = did_tech_die.is_game_in_db(games[game])
                if not is_duplicate:
                    new_tweet = did_tech_die.get_resulting_tweet(sport, games[game])
                    response = client.create_tweet(text=new_tweet)
                    url = f"https://twitter.com/user/status/{response.data['id']}"
                    print("New {} tweet:\n{}\n".format(sport, url))
                    did_tech_die.update_game_db(games[game])

#Mass tweeting based on season
def tweet_seasonal_sports():
    season = get_season()
    if season == 'winter':
        for sport in winter_sports:
            create_sport_tweets(sport)
    if season == 'spring':
        for sport in spring_sports:
            create_sport_tweets(sport)
    if season == "summer":
        for sport in summer_sports:
            create_sport_tweets(sport)
    if season == "autumn":
        for sport in autumn_sports:
            create_sport_tweets(sport)
  
tweet_seasonal_sports()