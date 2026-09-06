import sqlite3
class Journal:
 def __init__(self,db):
  self.db=db;c=sqlite3.connect(db);c.execute('CREATE TABLE IF NOT EXISTS trades(id INTEGER PRIMARY KEY,symbol TEXT,timeframe TEXT,action TEXT,entry REAL,sl REAL,tp REAL,score REAL,grade TEXT,result TEXT,pnl REAL,notes TEXT,created_at TEXT DEFAULT CURRENT_TIMESTAMP)');c.commit();c.close()
 def add(self,x):
  c=sqlite3.connect(self.db);q='INSERT INTO trades(symbol,timeframe,action,entry,sl,tp,score,grade,result,pnl,notes) VALUES(?,?,?,?,?,?,?,?,?,?,?)';cur=c.execute(q,tuple(x.get(k) for k in ['symbol','timeframe','action','entry','sl','tp','score','grade','result','pnl','notes']));c.commit();i=cur.lastrowid;c.close();return i
 def list(self):
  c=sqlite3.connect(self.db);c.row_factory=sqlite3.Row;r=[dict(x) for x in c.execute('SELECT * FROM trades ORDER BY id DESC')];c.close();return r
