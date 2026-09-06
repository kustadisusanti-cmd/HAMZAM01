import os,json,urllib.request,urllib.parse
def notify(message):
 out=[];u=os.getenv('HAMZAM_WEBHOOK_URL','').strip()
 if u:
  try:
   d=json.dumps({'text':message,'message':message}).encode();r=urllib.request.urlopen(urllib.request.Request(u,data=d,headers={'Content-Type':'application/json'}),timeout=8);out.append({'channel':'webhook','ok':r.status<400})
  except Exception as e:out.append({'channel':'webhook','ok':False,'error':str(e)})
 t=os.getenv('HAMZAM_TELEGRAM_BOT_TOKEN','').strip();chat=os.getenv('HAMZAM_TELEGRAM_CHAT_ID','').strip()
 if t and chat:
  try:
   d=urllib.parse.urlencode({'chat_id':chat,'text':message}).encode();r=urllib.request.urlopen(urllib.request.Request(f'https://api.telegram.org/bot{t}/sendMessage',data=d),timeout=8);out.append({'channel':'telegram','ok':r.status<400})
  except Exception as e:out.append({'channel':'telegram','ok':False,'error':str(e)})
 return out
