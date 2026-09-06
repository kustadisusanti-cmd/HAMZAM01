from backend.core.market import parse_candles
from backend.core.fractal import structure_bias
from backend.core.decision import analyze

def data(n=30):
 return [{'t':i,'o':100+i*.1,'h':101+i*.1,'l':99+i*.1,'c':100.5+i*.1} for i in range(n)]
def test_parse(): assert len(parse_candles(data()))==30
def test_structure(): assert structure_bias(parse_candles(data())) in ('NEUTRAL','RANGE','BULLISH','BEARISH')
def test_analyze(): assert 'score' in analyze(parse_candles(data()),parse_candles(data()))
