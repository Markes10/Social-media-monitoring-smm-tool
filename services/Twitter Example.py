import snscrape.modules.twitter as sntwitter
import pandas as pd

def scrape_competitor_tweets(competitor_handle, max_tweets=50):
    """Scrape latest tweets from a competitor's Twitter account."""
    tweets = []
    for i, tweet in enumerate(sntwitter.TwitterUserScraper(competitor_handle).get_items()):
        if i >= max_tweets:
            break
        tweets.append([tweet.date, tweet.content, tweet.likeCount, tweet.retweetCount])
    
    df = pd.DataFrame(tweets, columns=["Date", "Content", "Likes", "Retweets"])
    return df

# Example Usage:
# df = scrape_competitor_tweets("Nike", 20)
# print(df)
