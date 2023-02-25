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

Top100 = ["What We Do in the Shadows","Oz","The Good FIght","The Odd Couple","Rick and Morty","Squid Game","NewsRadio","The Rockford Files","The Muppet Show","The Tonight Show Starring Johnny Carson","The Wonder Years","The Carol Burnett Show","The Crown","The Kids in the Hall","The Bob Newhart Show","Orange Is the New Black","Fargo","I'm Alan Partridge","Party Down","It's Always Sunny in Philadelphia","Band of Brothers","Mr.Show with Bob and David","Sex and the City","The Jeffersons","Justified","Frasier","The Honeymooners","Buffy the Vampire Slayer","Good Times","Better Things","SCTV","Chappelle's Show","Fawlty Towers","NYPD Blue","The Daily Show With Jon Stewart","Girls","The Golden Girls","South Park","The Dick Van Dyke Show","The Underground Railroad","Taxi","Key & Peele","Six Feet Under","Russian Doll","Community","Halt and Catch Fire","ER","The Office (UK)","Barry","The X-Files","Jeopardy!","Friends","The Shield","My So-Called Life","The West Wing","Columbo","Late Night With David Letterman","Insecure","Battlestar Galactica","BoJack Horseman","The Good Place","Curb Your Enthusiasm","Hill Streets Blues","Arrested Development","I Love Lucy","Lost","The Office","Monty Python's Flying Circus","Better Call Saul","Game of Thrones","Parks and Recreation","Roots","Friday Night Lights","Deadwood","Sesame Street","M*A*S*H","Freaks and Geeks","Watchmen","Star Trek","All in the Family","30 Rock","I May Destroy You","Saturday Night Live","The Leftovers","Twin Peaks","The Larry Sanders Show","The Americans","Veep","The Twilight Zone","Succession","The Mary Tyler Moore Show","Atlanta","Cheers","Mad Men","Seinfeld","Fleabag","The Wire","Breaking Bad","The Simpsons","The Sopranos"]
counter = 1
for title in Top100:
    print(counter)
    counter += 1
    for submission in reddit.subreddit("movies").search(title):
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
        db[title].insert_one(post)

