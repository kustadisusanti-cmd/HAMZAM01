from .market import atr
from .fractal import swing_points
def cisd(c):
 hs,ls=swing_points(c);a=atr(c);x=c[-1];bl=c[hs[-1]].h if hs else None;sl=c[ls[-1]].l if ls else None;bull=bl is not None and x.c>bl;bear=sl is not None and x.c<sl;disp=x.body>=.8*a if a else False;p=c[-2];vb=p.bear and x.bull and x.c>p.h;vs=p.bull and x.bear and x.c<p.l
 return {'bull':bull,'bear':bear,'bull_level':bl,'bear_level':sl,'displacement':disp,'v_bull':vb,'v_bear':vs,'quality':'HIGH' if (bull and disp and vb) or (bear and disp and vs) else 'MEDIUM' if bull or bear else 'NONE'}
