"""Search the bundled modern Chinese translation; Python standard library only."""
import argparse
import json
import re
import sys
from pathlib import Path

def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('query',nargs='?',default='')
    p.add_argument('--volume',type=int,choices=range(1,17))
    p.add_argument('--id')
    p.add_argument('--source-page',type=int)
    p.add_argument('--limit',type=int,default=5)
    a=p.parse_args()
    if a.limit<1:p.error('--limit must be positive')
    data=json.loads((Path(__file__).resolve().parents[1]/'references/corpus.json').read_text(encoding='utf-8'))
    hits=[]
    terms=a.query.casefold().split()
    for s in data:
        if a.volume is not None and s['volume']!=a.volume:continue
        if a.id and s['id']!=a.id:continue
        if a.source_page is not None:
            ns=[int(n) for n in re.findall(r'\d+',s['source'])]
            if not ns or not min(ns)<=a.source_page<=max(ns):continue
        hay='\n'.join([s['title']]+s['text']+s.get('notes',[])).casefold()
        if not all(t in hay for t in terms):continue
        score=sum(10*s['title'].casefold().count(t)+hay.count(t) for t in terms)
        hits.append((score,s))
    hits.sort(key=lambda x:(-x[0],x[1]['volume'],x[1]['section']))
    result={'total_matches':len(hits),'returned':min(len(hits),a.limit),'results':[s for _,s in hits[:a.limit]]}
    if hasattr(sys.stdout,'reconfigure'):sys.stdout.reconfigure(encoding='utf-8')
    print(json.dumps(result,ensure_ascii=False,indent=2))

if __name__=='__main__':main()
