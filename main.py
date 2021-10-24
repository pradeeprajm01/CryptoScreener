''' 10OCT 2021 - MPR '''

from binance import Client
import requests, json, time
import pandas as pd

client = Client()
url = 'https://api.binance.com/api/v1/ticker/24hr?symbol='

def top(i):
    allpairs = pd.DataFrame(client.get_ticker())
    relev = allpairs[allpairs.symbol.str.contains('USDT')] #Channge Pair as per need
    non_lev = relev[~((relev.symbol.str.contains('UP')) | (relev.symbol.str.contains('DOWN')))]
    top = non_lev.symbol.values[i]
    return top


def get_top(n):    
    while True:
        time.sleep(5)
        if n == 313: #here 313, because there is only 313 USDT pairs are available for trade in binance 
            break
        top_asset = top(n)
        response = requests.get(url + top_asset)
        content = response.content.decode("utf8")
        updates = json.loads(content)
        percent = float(updates['priceChangePercent'])
        
        if percent >= 4  :
            return top_asset,percent,n
        else:
            n += 1
            
n = 0
percent =  []
crypto = []

while True:
    cryptoN, percentN, n = get_top(n)
    crypto.append(cryptoN)
    percent.append(percentN)
    #print(percent,crypto)
    n += 1
    if n == 313:
        coins = [percent,crypto]
        cd = pd.DataFrame(coins,columns=['PercentChange','Crypto'])
        cd.to_csv('TopPerformingCrypto.csv')
        break
