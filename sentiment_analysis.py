from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from pymongo import MongoClient
from bson.objectid import ObjectId


userInfoFile = open("UserInfo.txt", 'r')
lines = userInfoFile.readlines()
my_client_id = lines[0].strip()
my_client_secret = lines[1].strip()
mongodb_username = lines[4].strip()
mongodb_password = lines[5].strip()
mongodb_ip = lines[6].strip()

sentiment = SentimentIntensityAnalyzer()

clientString = "mongodb://" + mongodb_username + ":" + mongodb_password + "@" + mongodb_ip + ":27017"
client = MongoClient(clientString)
db = client['Reddit']
for collection in db.list_collection_names():
    print(collection)
    for document in db[collection].find({"Sentiment" : None}):
        body = document['Body']
        post_sentiment = sentiment.polarity_scores(body)
        document['Sentiment'] = post_sentiment['compound']
        for comment in document['Comments']:
            comment_body = comment['Body']
            comment_sentiment = sentiment.polarity_scores(comment_body)
            result = db[collection].update_one({"_id" : ObjectId(document["_id"]), "Comments.Body" : comment["Body"]},
                                      {"$set" : {"Comments.$.Sentiment" : comment_sentiment['compound']}})
        result = db[collection].update_one({"_id" : ObjectId(document['_id'])},
                                    {"$set" : {"Sentiment" : post_sentiment['compound']}})