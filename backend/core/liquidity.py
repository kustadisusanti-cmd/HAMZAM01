def detect(candles,lookback=10):
 x=candles[-1];p=candles[max(0,len(candles)-lookback-1):-1];hi=max(z.h for z in p);lo=min(z.l for z in p);bs=x.l<lo and x.c>lo;ss=x.h>hi and x.c<hi
 return {'bull_sweep':bs,'bear_sweep':ss,'swept_low':lo if bs else None,'swept_high':hi if ss else None}
def fvg(c):
 a,_,d=c[-3:]
 if d.l>a.h:return {'type':'BULLISH','low':a.h,'high':d.l}
 if d.h<a.l:return {'type':'BEARISH','low':d.h,'high':a.l}
 return None
