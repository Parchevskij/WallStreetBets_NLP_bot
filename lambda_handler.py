from html.parser import HTMLParser
import http.client
from http.client import HTTPException
import json
import os
from urllib.parse import urljoin
from /reddit_api import RedditConfig

from ./dl_back import create_prediction

accepted_words = [
      "YOLO", "TOS", "CEO", "CFO", "CTO", "DD", "BTFD", "WSB", "OK", "RH",
      "KYS", "FD", "TYS", "US", "USA", "IT", "ATH", "RIP", "BMW", "GDP",
      "OTM", "ATM", "ITM", "IMO", "LOL", "DOJ", "BE", "PR", "PC", "ICE",
      "TYS", "ISIS", "PRAY", "PT", "FBI", "SEC", "GOD", "NOT", "POS", "COD",
      "AYYMD", "FOMO", "TL;DR", "EDIT", "STILL", "LGMA", "WTF", "RAW", "PM",
      "LMAO", "LMFAO", "ROFL", "EZ", "RED", "BEZOS", "TICK", "IS", "DOW"
      "AM", "PM", "LPT", "GOAT", "FL", "CA", "IL", "PDFUA", "MACD", "HQ",
      "OP", "DJIA", "PS", "AH", "TL", "DR", "JAN", "FEB", "JUL", "AUG",
      "SEP", "SEPT", "OCT", "NOV", "DEC", "FDA", "IV", "ER", "IPO", "RISE"
      "IPA", "URL", "MILF", "BUT", "SSN", "FIFA", "USD", "CPU", "AT",
      "GG", "ELON", "I", "WE", "A", "AND","THE","THIS","TO","BUY","MY","MOST","ARK",
      "IN","S","BABY","APES"
   ]
   
accepted = [x.tolower() for x in accepted_words]

reddit_config = RedditConfig()


def lambda_handler(event, context):
    
    conn = http.client.HTTPSConnection("api.telegram.org")
    
    BOT_TOKEN = os.getenv('TELEGRAM_TOKEN')
    last_message_text = 'https://api.telegram.org/bot{token}/getUpdates'.format(token=BOT_TOKEN)
    
    if BOT_TOKEN is not None:
        response = requests.post(MethodGetUpdates).json()
        message_text = response['result'][-1]['message']['text']
        
        if message_text in accepted:
            data_df = reddit_config.get_request(message_text, new, **{'params': {'limit': '10'}})
            if data_df.shape[0] > 1:
                predictions = create_prediction(data_df)
                data_df['predictions'] = predictions
                
                response = ''
                
                for i in tqdm(range(data_df.shape[0])):
                    if data_df.loc[i, 'prediction'] == 1:
                        response += data_df.loc[i, 'title'] + ' is worth to read!\n'
                    else:
                        response += data_df.loc[i, 'title'] + ' can be avoided!\n'
            
            else:
                response = "There is no updated info for you now"
        
        else:
            response = "Try to use another name!"
        
        
                    
        
        destination =  f"/bot{BOT_TOKEN}/sendMessage"
        headers = {'content-type': "application/json"}
        
        payload = {
            'chat_id': 238537280,
            'text': response
        }
        
        conn.request("POST", destination, json.dumps(payload), headers)
        
        res = conn.getresponse()

        return {
            'statusCode': res.status,
            'body': json.dumps('Lambda executed.')
        }
        
    
    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }
