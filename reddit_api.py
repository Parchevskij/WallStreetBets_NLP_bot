import requests
from requests.auth import HTTPBasicAuth
import pandas as pd


class RedditConfig:
  def __init__(self):
    self.CLIENT_ID = ''
    self.SECRET_TOKEN = ''
    self.auth = HTTPBasicAuth(self.CLIENT_ID, self.SECRET_TOKEN)

    self.headers = {'User-Agent': 'StockBot/0.0.1'}
    self.data = {
        'grant_type': 'password',
        'username': 'GorgeousYevhenii',
        'password': 'seFhiw-4zuxve-torxaf'
      }

    self.TOKEN = self.get_access_token()
    self.HEADERS = {**self.headers, **{'Authorization': f"bearer {self.TOKEN}"}}
    

  def get_access_token(self):
    res = requests.post('https://www.reddit.com/api/v1/access_token',
                        auth=self.auth, 
                        data=self.data, 
                        headers=self.headers)
    return res.json()['access_token']


  def get_request(self, topic, config, **kwargs): # config = ['new', 'top'][i]
    res = requests.get(f'https://oauth.reddit.com/r/{topic}/{config}',
                        headers=self.HEADERS, **kwargs).json()
    df = pd.DataFrame()

    for post in res['data']['children']:
        df = df.append({
            'subreddit': post['data']['subreddit'],
            'title': post['data']['title'],
            'selftext': post['data']['selftext'],
            'upvote_ratio': post['data']['upvote_ratio'],
            'ups': post['data']['ups'],
            'downs': post['data']['downs'],
            'score': post['data']['score']
        }, ignore_index=True)

    return df[df.selftext != '']