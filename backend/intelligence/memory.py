import sqlite3
from collections import defaultdict
class Memory:
 def __init__(self,db):
  self.db=db;c=sqlite3.connect(db);c.execute('CREATE TABLE IF NOT EXISTS feedback(id INTEGER PRIMARY KEY,pattern TEXT,outcome TEXT,correction TEXT,note TEXT,created_at TEXT DEFAULT CURRENT_TIMESTAMP)');c.commit();c.close()
 def add(self,pattern,outcome,correction='',note=''):
  c=sqlite3.connect(self.db);c.execute('INSERT INTO feedback(pattern,outcome,correction,note) VALUES(?,?,?,?)',(pattern,outcome,correction,note));c.commit();c.close()
 def summary(self):
  c=sqlite3.connect(self.db);rows=c.execute('SELECT pattern,outcome,correction FROM feedback ORDER BY id DESC').fetchall();c.close();d=defaultdict(lambda:{'wins':0,'losses':0,'other':0,'corrections':[]})
  for p,o,cor in rows:
   if o.upper() in ('WIN','PROFIT'):d[p]['wins']+=1
   elif o.upper() in ('LOSS','LOST'):d[p]['losses']+=1
   else:d[p]['other']+=1
   if cor:d[p]['corrections'].append(cor)
  for x in d.values():
   n=x['wins']+x['losses'];x['win_rate']=round(x['wins']/n*100,2) if n else None;x['reliability']=round(50+(x['win_rate']-50)*min(1,n/20),2) if x['win_rate'] is not None else 50
  return dict(d)
