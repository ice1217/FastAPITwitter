import json

import tweepy
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from pydantic import BaseModel

app = FastAPI()


class TweetRequest(BaseModel):
  query: str
  limit: int
  consumer_key: str
  consumer_secret: str
  access_token: str
  access_token_secret: str
  language: str


# Default root endpoint
@app.get("/")
async def root():
  return {
    "message": "This is a custom Twitter API Search with Python and FastAPI"
  }


# Example path parameter
@app.post("/tweets/")
async def read_items(request: Request, tweet_request: TweetRequest):
  # Retrieve the JSON body from the request
  json_body = await request.json()

  # Extract values from the JSON body
  search_query = json_body['query']
  try:
    num_of_tweets = int(json_body['limit'])
  except ValueError:
    num_of_tweets = json_body['limit']
  consumer_key = json_body['consumer_key']
  consumer_secret = json_body['consumer_secret']
  access_token = json_body['access_token']
  access_token_secret = json_body['access_token_secret']
  lang = json_body['language']

  # Authenticate to Twitter API
  auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
  auth.set_access_token(access_token, access_token_secret)
  # Create API object
  api = tweepy.API(auth)

  # Search for tweets
  tweets = tweepy.Cursor(api.search_tweets, q=search_query,
                         lang=lang).items(num_of_tweets)

  # Convert the tweet results to JSON without escaped double quotes
  json_tweets = [
    json.loads(json.dumps(tweet._json, ensure_ascii=False)) for tweet in tweets
  ]

  return JSONResponse(content=json_tweets)
