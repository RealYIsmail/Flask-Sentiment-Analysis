from flask import Flask, redirect, url_for, render_template, request
import tweepy
from textblob import TextBlob
app = Flask(__name__)
 

@app.route('/')
def home():
    return render_template("index.html")

@app.route("/SentimentAnalysis", methods= ["GET", "POST"])
def SentimentAnalysis():
    if request.method == "POST":
        ## collecting input
        user = request.form["nm"]
        """
        Task: Get the user input from the app.py and process the semantic analysis here

        Afterwards send back the output the app.py to be sent back to the webpage.

        """

        # Title : Sentiment based tourist guide application

        # Author: Yonis Ismail

        # Module: Digital systems project

        api_key = "LmeRKu0EwN1OsCK3y9dbkYiem"
        api_secretkey = "nKGZvgIuxvE3hAOSYmHCA1vBImwW0jqE6Y3ea8K5olKUeFb3Xw"
        access_token = "1411819667665080325-cStfnLbQTYOI2StzPzHbLUnFCfxq8A"
        secret_access_token = "fe1S0y2bAv8ba5KRZtSoAlGBBvCMa5mWVn5b7Wd69oL39"
        # Polarity is the sentiment value as a float
        polarity = 0

        positive = 0
        negative = 0
        neutral = 0

        auth_handler = tweepy.OAuthHandler(consumer_key=api_key, consumer_secret=api_secretkey)
        auth_handler.set_access_token(access_token, secret_access_token)
        api = tweepy.API(auth_handler, wait_on_rate_limit=True)
        #################################################################
        # Search term for the algorithm
        search_term = user
        tweet_amount = 200
        tweets = tweepy.Cursor(api.search, q=search_term, lang="en").items(tweet_amount)
        ##################################################################
        # Process tweets
        # Gather tweets
        print("Working")

        for tweet in tweets:
            final_text = tweet.text.replace("RT", '')
            if final_text.startswith(' @'):
                position = final_text.index(':')
                final_text = final_text[position + 2:]
            if final_text.startswith(' @'):
                position = final_text.index(' ')
                final_text = final_text[position + 2:]
            # Analyse the tweets that have been gathered
            analysis = TextBlob(final_text)
            tweet_polarity = analysis.polarity
            if tweet_polarity > 0.00:
                positive += 1
            elif tweet_polarity < 0.00:
                negative += 1
            else:
                neutral += 1
            polarity += tweet_polarity

        # Output data
        print("The polarity of", search_term, "is: ", polarity)
        print(f" Amount of Positive tweets: {positive}")
        print(f" Amount of neutral tweets: {neutral}")
        print(f" Amount of negative tweets: {negative}")

        return render_template("SentimentAnalysis.html", content=user, polaritycontent=polarity)
    else:
        return render_template("SentimentAnalysis.html")

@app.route("/<usr>")
def user(usr):
    return f"<h1>{usr}<h1>"

@app.route("/Images.html", methods= ["GET", "POST"])
def Images():
    if request.method == "POST":
        ## collecting input
        location = request.form["subject"]
        return render_template("Images.html", locationA=location)
    else:
        return render_template("Images.html")

@app.route("/Mapping", methods= ["GET", "POST"])
def Mapping():
    if request.method == "POST":
        ## collecting input
        location = request.form["pac-input"]
        return render_template("Mapping.html", locationA=location)
    else:
        return render_template("Mapping.html")

if __name__ == "__main__":
    app.run(debug=True)