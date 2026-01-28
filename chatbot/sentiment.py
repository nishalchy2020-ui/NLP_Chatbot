from textblob import TextBlob

def analyse_sentiment(text):
    polarity = TextBlob(text).sentiment.polarity

    if polarity > 0.3:
        return "positive"
    elif polarity < -0.3:
        return "negative"
    return "neutral"
