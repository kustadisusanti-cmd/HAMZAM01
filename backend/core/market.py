from dataclasses import dataclass
@dataclass
class Candle:
 t:object;o:float;h:float;l:float;c:float;v:float=0.0
 @property
 def body(self):return abs(self.c-self.o)
 @property
 def bull(self):return self.c>self.o
 @property
 def bear(self):return self.c<self.o
def parse_candles(rows):
 out=[]
 for i,r in enumerate(rows):
  if isinstance(r,dict):out.append(Candle(r.get('t',i),float(r['o']),float(r['h']),float(r['l']),float(r['c']),float(r.get('v',0))))
  else:
   v=list(r)
   if len(v)<5:raise ValueError('Each candle needs at least 5 values')
   out.append(Candle(i,*map(float,v)) if len(v)==5 else Candle(v[0],*map(float,v[1:6])))
 if len(out)<5:raise ValueError('At least 5 candles are required')
 return out
def atr(candles,n=14):
 if len(candles)<2:return 0
 tr=[]
 for i,x in enumerate(candles):
  p=candles[i-1].c if i else x.o;tr.append(max(x.h-x.l,abs(x.h-p),abs(x.l-p)))
 return sum(tr[-n:])/min(n,len(tr))
