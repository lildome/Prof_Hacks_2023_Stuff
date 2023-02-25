import praw
from pymongo import MongoClient

userInfoFile = open("UserInfo.txt", 'r')
lines = userInfoFile.readlines()
my_client_id = lines[0]
my_client_secret = lines[1]
mongodb_username = lines[2]
mongodb_password = lines[3]
mongodb_ip = lines[4]

reddit = praw.Reddit(
    client_id=my_client_id,
    client_secret=my_client_secret,
    user_agent="Post and comment scraping by u/No-Background7103",
)

clientString = "mongodb://" + mongodb_username + ":" + mongodb_password + "@" + mongodb_ip + ":27017"
client = MongoClient(clientString)
db = client['Reddit']

top100MoviesAllTime = ["The Godfather","The Shawshank Redemption","Schindler's List","Raging Bull","Casablanca","Citizen Kane","Gone with the Wind","The Wizard of Oz","One Flew Over the Cuckoo's Nest","Lawrence of Arabia","Vertigo","Psycho","The Godfather Part II","On the Waterfront","Sunset Blvd.","Forrest Gump","The Sound of Music","Angry Men","West Side Story","Star Wars: Episode IV - A New Hope","2001: A Space Odyssey","E.T. the Extra-Terrestrial","The Silence of the Lambs","Chinatown","The Bridge on the River Kwai","Singin' in the Rain","It's a Wonderful Life","Dr.Strangelove or: How I learned to Stop Worrying and Love the Bomb","Some Like It Hot","Ben-Hur","Apocalypse Now","Amadeus","The Lord of the Rings: The Return of the King","Gladiator","Titanic","From Here to Eternity","Saving Private Ryan","Unforgiven","Indiana Jones and the Raiders of the Lost Ark","Rocky","A Streetcar Named Desire","The Philadelphia Story","To Kill a Mockingbird","An American in Paris","The Best Years of Our Lives","My Fair Lady","A Clockwork Orange","Doctor Zhivago","The Searches","Jaws","Patton","Butch Cassidy and the Sundance Kid","The Treasure of the Sierra Madre","The Good, the Bad and the Ugly","The Apartment","Platoon","High Noon","Braveheart","Dances with Wolves","Jurassic Park","The Exorcist","The Pianist","Goodfellas","The Deer Hunter","All Quiet on the Western Front","Bonnie and Clyde","The French Connection","City Lights","It Happened One Night","A Place in the Sun","Midnight Cowboy","Mr. Smith Goes to Washington","Rain Man","Annie Hall","Fargo","Giant","Shane","The Grapes of Wrath","The Green Mile","Close Encounters of the Third Kind","Nashville","Network","The Graduate","American Graffiti","Pulp Fiction","Terms of Endearment","Good Will Hunting","The African Queen","Stagecoach","Mutiny on the Bounty","The Great Dictator","Double Indemnity","The Maltese Falcon","Wuthering Heights","Taxi Driver","Rear Window","The Third Man","Rebel Without a Cause","North by Northwest","Yankee Doodle Dandy"]

counter = 1
for movie in top100MoviesAllTime:
    print(counter)
    counter += 1
    for submission in reddit.subreddit("movies").search(movie):
        # if submission.title.contains(movie):
        submission.comments.replace_more(limit=None)
        comments = []
        for comment in submission.comments.list():
            nextCom = {"Body" : comment.body,
                       "Score" : comment.score,
                       "Sentiment" : None,
                       "Link" : comment.permalink
                       }
            comments.append(nextCom)
        post = {"Title": submission.title,
                "Subreddit": "movies",
                "Score": submission.score,
                "Like_Ratio": submission.upvote_ratio,
                "Body": submission.selftext,
                "Sentiment": None,
                "Link": submission.permalink,
                "Comments": comments
                }
        db[movie].insert_one(post)

