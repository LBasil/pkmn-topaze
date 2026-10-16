import sys,json,os; sys.dont_write_bytecode=True
sys.path.insert(0,'/tmp/gx')
from tz import T
R='/home/claude/pkmn-topaze/'
L={d['id']:d for d in json.load(open(R+'data/layouts/layouts.json'))['layouts'] if 'id' in d}
M={};ID={}
import glob
for f in glob.glob(R+'data/maps/*/map.json'):
    d=json.load(open(f)); n=os.path.basename(os.path.dirname(f)); M[n]=d; ID[d['id']]=n
def dim(n): l=L[M[n]['layout']]; return l['width'],l['height']
def tl(n): l=L[M[n]['layout']]; return (l['primary_tileset'],l['secondary_tileset'])
opp={'up':'down','down':'up','left':'right','right':'left'}
jobs=[];seen=set()
for a,d in M.items():
    for c in d.get('connections') or []:
        b=ID.get(c['map'])
        if not b: continue
        k=tuple(sorted((a,b)))
        if k in seen or tl(a)==tl(b): continue
        seen.add(k)
        for (p,q,dr,off) in ((a,b,c['direction'],c['offset']),):
            pw,ph=dim(p); qw,qh=dim(q)
            for (s,t,dd,o) in ((p,q,dr,off),(q,p,opp[dr],-off)):
                sw,sh=dim(s); tw,th=dim(t)
                if dd in('up','down'):
                    lo=max(0,o); hi=min(sw,tw+o)-1
                    if hi<lo: continue
                    x=(lo+hi)//2; y=2 if dd=='up' else sh-3
                else:
                    lo=max(0,o); hi=min(sh,th+o)-1
                    if hi<lo: continue
                    y=(lo+hi)//2; x=2 if dd=='left' else sw-3
                jobs.append((s,t,x,y))
print(len(jobs),flush=True)
out=open('/tmp/gx/out/seam_index.txt','w')
for i,(s,t,x,y) in enumerate(jobs):
    try:
        te=T(s,x,y); f=te.shot('sm_%02d'%i); out.write('%02d %s->%s (%d,%d)\n'%(i,s,t,x,y)); out.flush(); print(i,s,t,flush=True)
    except Exception as ex: print(i,'ERR',s,ex,flush=True)
