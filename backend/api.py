import os,csv,io
from fastapi import FastAPI,UploadFile,File,HTTPException
from fastapi.responses import FileResponse
from pydantic import BaseModel
from backend.core.market import parse_candles
from backend.core.decision import analyze
from backend.core.backtest import run as backtest_run
from backend.core.scanner import scan
from backend.journal.store import Journal
from backend.intelligence.memory import Memory
from backend.providers.binance import klines
from backend.live import live_scanner
DB=os.getenv('HAMZAM_DB','hamzam.db');RISK=float(os.getenv('HAMZAM_RISK_PCT','1'));MIN_SCORE=int(os.getenv('HAMZAM_MIN_SCORE','70'));journal=Journal(DB);memory=Memory(DB);app=FastAPI(title='HAMZAM',version='READY-1.4')
class AnalysisIn(BaseModel):htf:list;ltf:list;account_balance:float=10000;risk_pct:float=RISK;rr:float=2
class JournalIn(BaseModel):symbol:str='';timeframe:str='';action:str;entry:float|None=None;sl:float|None=None;tp:float|None=None;score:float|None=None;grade:str='';result:str='OPEN';pnl:float=0;notes:str=''
class FeedbackIn(BaseModel):pattern:str;outcome:str;correction:str='';note:str=''
@app.get('/health')
def health():return {'ok':True,'name':'HAMZAM','version':'READY-1.4','live_data':'binance_public','live_scanner':live_scanner.running}
@app.get('/market/binance')
def market_binance(symbol='BTCUSDT',interval='15m',limit=200):
 try:return {'symbol':symbol.upper(),'interval':interval,'candles':klines(symbol,interval,limit)}
 except Exception as e:raise HTTPException(502,f'Market data unavailable: {e}')
@app.get('/analyze/binance')
def analyze_binance(symbol='BTCUSDT',htf_interval='1h',ltf_interval='15m',account_balance=10000,risk_pct=1,rr=2):
 try:return {'symbol':symbol.upper(),'htf_interval':htf_interval,'ltf_interval':ltf_interval,'analysis':analyze(parse_candles(klines(symbol,htf_interval,200)),parse_candles(klines(symbol,ltf_interval,300)),account_balance,risk_pct,rr)}
 except Exception as e:raise HTTPException(502,f'Live analysis unavailable: {e}')
@app.post('/live/config')
def live_config(x:dict):live_scanner.configure(x.get('symbols'),x.get('htf'),x.get('ltf'),x.get('seconds'),x.get('alerts'));return live_scanner.status()
@app.post('/live/start')
def live_start():live_scanner.start();return live_scanner.status()
@app.post('/live/stop')
def live_stop():live_scanner.stop();return live_scanner.status()
@app.post('/live/scan')
def live_scan():return {'results':live_scanner.scan_once(),'status':live_scanner.status()}
@app.get('/live/status')
def live_status():return live_scanner.status()
@app.get('/')
def home():return FileResponse('frontend/index.html')
@app.get('/manifest.webmanifest')
def manifest():return FileResponse('frontend/manifest.webmanifest')
@app.get('/sw.js')
def sw():return FileResponse('frontend/sw.js')
@app.post('/analyze')
def do_analyze(x:AnalysisIn):return analyze(parse_candles(x.htf),parse_candles(x.ltf),x.account_balance,x.risk_pct,x.rr)
@app.post('/backtest')
def do_backtest(x:AnalysisIn):return backtest_run(x.htf,x.ltf,x.account_balance,x.risk_pct,x.rr)
@app.post('/scan')
def do_scan(x:dict):return {'results':scan(x.get('items',[]),int(x.get('min_score',MIN_SCORE)))}
@app.post('/journal')
def add_journal(x:JournalIn):return {'id':journal.add(x.model_dump())}
@app.get('/journal')
def get_journal():return journal.list()
@app.post('/feedback')
def add_feedback(x:FeedbackIn):memory.add(x.pattern,x.outcome,x.correction,x.note);return {'ok':True,'memory':memory.summary()}
@app.get('/memory')
def get_memory():return memory.summary()
@app.post('/import/csv')
async def import_csv(file:UploadFile=File(...)):
 rows=list(csv.DictReader(io.StringIO((await file.read()).decode('utf-8-sig'))));out=[]
 for i,r in enumerate(rows):
  def g(*n):
   for a in n:
    for k,v in r.items():
     if k.lower()==a.lower() and v!='':return v
   return None
  o,h,l,c=g('o','open'),g('h','high'),g('l','low'),g('c','close')
  if None in (o,h,l,c):raise HTTPException(400,'CSV must contain open/high/low/close columns')
  out.append({'t':g('t','time','timestamp') or i,'o':float(o),'h':float(h),'l':float(l),'c':float(c),'v':float(g('v','volume') or 0)})
 return {'count':len(out),'candles':out}
