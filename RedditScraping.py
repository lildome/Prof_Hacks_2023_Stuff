import praw
from pymongo import MongoClient

userInfoFile = open("UserInfo.txt", 'r')
lines = userInfoFile.readlines()
my_client_id = lines[0].strip()
my_client_secret = lines[1].strip()
my_reddit_username = lines[2].strip()
my_reddit_password = lines[3].strip()
mongodb_username = lines[4].strip()
mongodb_password = lines[5].strip()
mongodb_ip = lines[6].strip()

reddit = praw.Reddit(
    client_id=my_client_id,
    client_secret=my_client_secret,
    password = my_reddit_password,
    username = my_reddit_username,
    user_agent="Python:reddit.scraper::v1.0 (by u/lildome)",
)

clientString = "mongodb://" + mongodb_username + ":" + mongodb_password + "@" + mongodb_ip + ":27017"
client = MongoClient(clientString)
db = client['Reddit']

Top100 = ["Rick and Morty","Squid Game","NewsRadio","The Rockford Files","The Muppet Show","The Tonight Show Starring Johnny Carson","The Wonder Years","The Carol Burnett Show","The Crown","The Kids in the Hall","The Bob Newhart Show","Orange Is the New Black","Fargo","I'm Alan Partridge","Party Down","It's Always Sunny in Philadelphia","Band of Brothers","Mr.Show with Bob and David","Sex and the City","The Jeffersons","Justified","Frasier","The Honeymooners","Buffy the Vampire Slayer","Good Times","Better Things","SCTV","Chappelle's Show","Fawlty Towers","NYPD Blue","The Daily Show With Jon Stewart","Girls","The Golden Girls","South Park","The Dick Van Dyke Show","The Underground Railroad","Taxi","Key & Peele","Six Feet Under","Russian Doll","Community","Halt and Catch Fire","ER","The Office (UK)","Barry","The X-Files","Jeopardy!","Friends","The Shield","My So-Called Life","The West Wing","Columbo","Late Night With David Letterman","Insecure","Battlestar Galactica","BoJack Horseman","The Good Place","Curb Your Enthusiasm","Hill Streets Blues","Arrested Development","I Love Lucy","Lost","The Office","Monty Python's Flying Circus","Better Call Saul","Game of Thrones","Parks and Recreation","Roots","Friday Night Lights","Deadwood","Sesame Street","M*A*S*H","Freaks and Geeks","Watchmen","Star Trek","All in the Family","30 Rock","I May Destroy You","Saturday Night Live","The Leftovers","Twin Peaks","The Larry Sanders Show","The Americans","Veep","The Twilight Zone","Succession","The Mary Tyler Moore Show","Atlanta","Cheers","Mad Men","Seinfeld","Fleabag","The Wire","Breaking Bad","The Simpsons","The Sopranos"]
counter = 1
for title in Top100:
    print(counter)
    counter += 1
    post_count = 0
    for submission in reddit.subreddit("television").search(title):
        # if submission.title.contains(movie):
        if post_count >= 50:
            break
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
                "Subreddit": "television",
                "Score": submission.score,
                "Like_Ratio": submission.upvote_ratio,
                "Body": submission.selftext,
                "Sentiment": None,
                "Link": submission.permalink,
                "Comments": comments
                }
        db[title].insert_one(post)

