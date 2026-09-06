from .market import atr
from .fractal import candle23,structure_bias
from .liquidity import detect,fvg
from .cisd_engine import cisd
def analyze(htf,ltf,account_balance=10000,risk_pct=1,rr=2):
 hb=structure_bias(htf);lb=structure_bias(ltf);h23=candle23(htf);l23=candle23(ltf);q=cisd(ltf);liq=detect(ltf);gap=fvg(ltf);side='BUY' if q['bull'] else 'SELL' if q['bear'] else None;s=28 if side else 0;r=[]
 if side:r.append('LTF CISD')
 if side=='BUY' and liq['bull_sweep']:s+=15;r.append('bullish liquidity sweep')
 if side=='SELL' and liq['bear_sweep']:s+=15;r.append('bearish liquidity sweep')
 if side=='BUY' and h23['bull'] or side=='SELL' and h23['bear']:s+=15;r.append('HTF Candle 2/3 confirmation')
 if side=='BUY' and hb=='BULLISH' or side=='SELL' and hb=='BEARISH':s+=12;r.append('HTF structure aligned')
 if side=='BUY' and lb=='BULLISH' or side=='SELL' and lb=='BEARISH':s+=8;r.append('LTF structure aligned')
 if q['quality']=='HIGH':s+=12;r.append('displacement/V-shape')
 elif q['quality']=='MEDIUM':s+=5
 if gap and (side=='BUY' and gap['type']=='BULLISH' or side=='SELL' and gap['type']=='BEARISH'):s+=5;r.append('supporting FVG')
 s=min(100,s);grade='A+' if s>=90 else 'A' if s>=80 else 'B' if s>=70 else 'C' if s>=55 else 'NO TRADE';act=side if side and s>=70 else 'WAIT';price=ltf[-1].c;a=atr(ltf)
 if act=='BUY':sl=min(x.l for x in ltf[-5:])-.1*a;tp=price+(price-sl)*rr
 elif act=='SELL':sl=max(x.h for x in ltf[-5:])+.1*a;tp=price-(sl-price)*rr
 else:sl=tp=None
 risk=account_balance*risk_pct/100;size=risk/abs(price-sl) if sl is not None and price!=sl else 0
 return {'action':act,'side':side,'score':s,'grade':grade,'confidence':s,'reasons':r,'htf_bias':hb,'ltf_bias':lb,'htf_candle23':h23,'ltf_candle23':l23,'liquidity':liq,'cisd':q,'fvg':gap,'entry':price if act!='WAIT' else None,'sl':sl,'tp':tp,'rr':rr if act!='WAIT' else None,'position_size':size,'risk_amount':risk}
