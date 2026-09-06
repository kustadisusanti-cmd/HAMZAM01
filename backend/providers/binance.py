import json,urllib.parse,urllib.request
BASE='https://api.binance.com/api/v3/klines'
def klines(symbol='BTCUSDT',interval='15m',limit=200):
 q=urllib.parse.urlencode({'symbol':symbol.upper(),'interval':interval,'limit':min(int(limit),1000)});req=urllib.request.Request(BASE+'?'+q,headers={'User-Agent':'HAMZAM/1.4'})
 with urllib.request.urlopen(req,timeout=10) as r:rows=json.loads(r.read().decode())
 return [{'t':x[0],'o':float(x[1]),'h':float(x[2]),'l':float(x[3]),'c':float(x[4]),'v':float(x[5])} for x in rows]
