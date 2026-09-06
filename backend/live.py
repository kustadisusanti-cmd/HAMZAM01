import os,threading,time
from datetime import datetime,timezone
from .core.market import parse_candles
from .core.decision import analyze
from .providers.binance import klines
from .alerts.notifier import notify
class LiveScanner:
 def __init__(self):
  self.running=False;self.thread=None;self.lock=threading.Lock();self.interval_seconds=max(15,int(os.getenv('HAMZAM_SCAN_SECONDS','60')));self.symbols=[x.strip().upper() for x in os.getenv('HAMZAM_SCAN_SYMBOLS','BTCUSDT,ETHUSDT,BNBUSDT,SOLUSDT,XRPUSDT').split(',') if x.strip()];self.htf=os.getenv('HAMZAM_SCAN_HTF','1h');self.ltf=os.getenv('HAMZAM_SCAN_LTF','15m');self.min_score=int(os.getenv('HAMZAM_MIN_SCORE','70'));self.alerts=os.getenv('HAMZAM_ALERTS','false').lower() in ('1','true','yes','on');self.signals={};self.last_scan=None;self.last_error=None
 def configure(self,symbols=None,htf=None,ltf=None,seconds=None,alerts=None):
  with self.lock:
   if symbols is not None:self.symbols=[str(x).strip().upper() for x in symbols if str(x).strip()]
   if htf:self.htf=str(htf)
   if ltf:self.ltf=str(ltf)
   if seconds is not None:self.interval_seconds=max(15,int(seconds))
   if alerts is not None:self.alerts=bool(alerts)
 def scan_once(self):
  out=[]
  for s in list(self.symbols):
   try:
    a=analyze(parse_candles(klines(s,self.htf,200)),parse_candles(klines(s,self.ltf,300)),10000,1,2);out.append({'symbol':s,'updated_at':datetime.now(timezone.utc).isoformat(),'analysis':a})
    self.signals[s]=out[-1]
    if self.alerts and a['action'] in ('BUY','SELL') and a['score']>=self.min_score:notify(f'HAMZAM SIGNAL {s} {a["action"]} {a["grade"]} {a["score"]}/100 Entry {a["entry"]} SL {a["sl"]} TP {a["tp"]}')
   except Exception as e:out.append({'symbol':s,'error':str(e)});self.last_error=f'{s}: {e}'
  self.last_scan=datetime.now(timezone.utc).isoformat();return out
 def _loop(self):
  while self.running:
   try:self.scan_once()
   except Exception as e:self.last_error=str(e)
   for _ in range(self.interval_seconds):
    if not self.running:break
    time.sleep(1)
 def start(self):
  if self.running:return False
  self.running=True;self.thread=threading.Thread(target=self._loop,daemon=True);self.thread.start();return True
 def stop(self):self.running=False;return True
 def status(self):return {'running':self.running,'symbols':self.symbols,'htf':self.htf,'ltf':self.ltf,'interval_seconds':self.interval_seconds,'alerts':self.alerts,'last_scan':self.last_scan,'last_error':self.last_error,'signals':list(self.signals.values())}
live_scanner=LiveScanner()
