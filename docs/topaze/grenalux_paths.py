import json, heapq, os
BIGMAP=bool(os.environ.get('TOPAZE_COL'))
d=json.load(open(os.environ.get('TOPAZE_COL','/tmp/grenalux_col.json'))); B={tuple(c) for c in d['blocked']}; W,H=d['w'],d['h']
DIRS={'up':(0,-1),'down':(0,1),'left':(-1,0),'right':(1,0)}
def path(a,b):
    pq=[(0,a,None,[a])]; seen={}
    while pq:
        c,p,pd,tr=heapq.heappop(pq)
        if p==b: return tr
        if (p,pd) in seen: continue
        seen[(p,pd)]=1
        for n,(dx,dy) in DIRS.items():
            q=(p[0]+dx,p[1]+dy)
            if not((0<=q[0]<=W-1 and 0<=q[1]<=H-1) if BIGMAP else (2<=q[0]<=W-3 and 0<=q[1]<=H-3)) : continue
            if q in B and q!=b: continue
            heapq.heappush(pq,(c+1+(0.01 if pd and pd!=n else 0),q,n,tr+[q]))
def moves(tr):
    out=[]
    for a,b in zip(tr,tr[1:]):
        for n,(dx,dy) in DIRS.items():
            if (a[0]+dx,a[1]+dy)==b: out.append('walk_'+n)
    return out
if __name__=='__main__':
    for a,b in [((14,14),(6,8)),((6,8),(18,15)),((12,2),(17,8)),((13,2),(17,8))]:
        t=path(a,b); print(a,b,len(t)); print(t)
