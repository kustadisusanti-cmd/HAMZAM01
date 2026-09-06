def swing_points(candles,left=2,right=2):
 hs=[];ls=[]
 for i in range(left,len(candles)-right):
  if candles[i].h>max(c.h for c in candles[i-left:i]) and candles[i].h>=max(c.h for c in candles[i+1:i+right+1]):hs.append(i)
  if candles[i].l<min(c.l for c in candles[i-left:i]) and candles[i].l<=min(c.l for c in candles[i+1:i+right+1]):ls.append(i)
 return hs,ls
def candle23(c):
 a,b,d=c[-3:];b2=a.l>b.l and b.c>a.l and b.c>b.o;s2=b.h>a.h and b.c<a.h and b.c<b.o;b3=not b2 and d.c>b.o and d.c>d.o;s3=not s2 and d.c<b.o and d.c<d.o
 return {'bull':b2 or b3,'bear':s2 or s3,'type':'CANDLE_2_BULL' if b2 else 'CANDLE_2_BEAR' if s2 else 'CANDLE_3_BULL' if b3 else 'CANDLE_3_BEAR' if s3 else None}
def structure_bias(c):
 hs,ls=swing_points(c)
 if len(hs)<2 or len(ls)<2:return 'NEUTRAL'
 hh=c[hs[-1]].h>c[hs[-2]].h;hl=c[ls[-1]].l>c[ls[-2]].l;lh=c[hs[-1]].h<c[hs[-2]].h;ll=c[ls[-1]].l<c[ls[-2]].l
 return 'BULLISH' if hh and hl else 'BEARISH' if lh and ll else 'RANGE'
