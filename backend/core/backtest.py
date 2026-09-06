from .market import parse_candles
from .decision import analyze
def run(htf_rows,ltf_rows,initial_balance=10000,risk_pct=1,rr=2):
 h=parse_candles(htf_rows);l=parse_candles(ltf_rows);bal=initial_balance;peak=bal;dd=0;tr=[]
 for i in range(max(10,len(l)//4),len(l)-1):
  try:a=analyze(h[:max(5,min(len(h),int(len(h)*i/len(l))+1))],l[:i+1],bal,risk_pct,rr)
  except Exception:continue
  if a['action']=='WAIT':continue
  n=l[i+1];sl=a['sl'];tp=a['tp'];hs=n.l<=sl if a['action']=='BUY' else n.h>=sl;ht=n.h>=tp if a['action']=='BUY' else n.l<=tp;ht=ht and not hs;o='LOSS' if hs else 'WIN' if ht else 'OPEN';p=-bal*risk_pct/100 if hs else bal*risk_pct/100*rr if ht else 0
  if o!='OPEN':bal+=p;peak=max(peak,bal);dd=max(dd,peak-bal)
  tr.append({'index':i+1,'action':a['action'],'score':a['score'],'outcome':o,'pnl':p})
 w=sum(x['outcome']=='WIN' for x in tr);lo=sum(x['outcome']=='LOSS' for x in tr);gp=sum(x['pnl'] for x in tr if x['pnl']>0);gl=-sum(x['pnl'] for x in tr if x['pnl']<0)
 return {'initial_balance':initial_balance,'final_balance':round(bal,2),'return_pct':round((bal/initial_balance-1)*100,2),'trades':len(tr),'wins':w,'losses':lo,'win_rate':round(w/(w+lo)*100,2) if w+lo else 0,'profit_factor':round(gp/gl,2) if gl else None,'max_drawdown':round(dd,2),'trade_log':tr}
