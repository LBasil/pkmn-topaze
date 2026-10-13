import sys; sys.path.insert(0,'/tmp/gx')
from tz import *
import collections
SP={0x54:(1,0),0x55:(-1,0),0x56:(0,-1),0x57:(0,1)}
D4=[('UP',(0,-1)),('DOWN',(0,1)),('LEFT',(-1,0)),('RIGHT',(1,0))]
def spin_bfs(nav,a,b,extra_block=()):
    beh=lambda c: nav.attr(*c)&0x1ff
    bl=lambda c: nav.blocked(*c) or c in extra_block
    def land(n):
        # Une fois lancé sur une flèche, le joueur continue tout droit (même sur sol normal), change de direction sur une autre flèche,
        # et s'arrête sur une case 0x58, ou quand la case suivante est bloquée.
        if beh(n) not in SP: return n
        seen=set(); d=SP[beh(n)]
        while (n,d) not in seen:
            seen.add((n,d))
            m=(n[0]+d[0],n[1]+d[1])
            if bl(m): return n
            n=m
            if beh(n)==0x58: return n
            if beh(n) in SP: d=SP[beh(n)]
        return n
    prev={a:None}; q=collections.deque([a])
    while q:
        c=q.popleft()
        if c==b: break
        for d,(dx,dy) in D4:
            n=(c[0]+dx,c[1]+dy)
            if bl(n) or (n in nav.warps and n!=b): continue
            n2=land(n)
            if n2 in prev: continue
            prev[n2]=(c,d); q.append(n2)
    if b not in prev: return None
    out=[]; c=b
    while prev[c]: out.append(prev[c][1]); c=prev[c][0]
    return out[::-1]
if __name__=='__main__':
    nav=R.Nav(sys.argv[1]); a=tuple(map(int,sys.argv[2:4])); b=tuple(map(int,sys.argv[4:6]))
    print(spin_bfs(nav,a,b))
