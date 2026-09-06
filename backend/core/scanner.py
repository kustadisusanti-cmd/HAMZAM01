from .decision import analyze
def scan(items,min_score=70):
 out=[]
 for x in items:
  try:
   a=analyze(x['htf'],x['ltf'],x.get('account_balance',10000),x.get('risk_pct',1),x.get('rr',2))
   if a['score']>=min_score:out.append({'symbol':x.get('symbol',''),'timeframe':x.get('timeframe',''),'action':a['action'],'score':a['score'],'grade':a['grade'],'analysis':a})
  except Exception as e:out.append({'symbol':x.get('symbol',''),'error':str(e)})
 return sorted(out,key=lambda x:x.get('score',0),reverse=True)
