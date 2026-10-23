#!/usr/bin/env python3
"""Niveaux des dresseurs de Sevii : plancher par ile (le joueur arrive niv. ~64 apres la Ligue). Idempotent (plancher)."""
import re,glob,json,sys
sys.argv=[sys.argv[0]]
T=open('src/data/trainers.h').read(); P=open('src/data/trainer_parties.h').read()
S_=''.join(open(f).read() for f in glob.glob('data/scripts/*.inc')+glob.glob('data/maps/*/scripts.inc'))
EV={}
for m in re.finditer(r'\[(SPECIES_\w+)\]\s*=\s*\{\{EVO_LEVEL,\s*(\d+),\s*(SPECIES_\w+)\}',open('src/data/pokemon/evolution.h').read()): EV[m.group(1)]=(int(m.group(2)),m.group(3))
def evolve(sp,l):
    while sp in EV and l>=EV[sp][0]: sp=EV[sp][1]
    return sp
def party(tid):
    m=re.search(r'\[%s\] = \{(.*?)\n    \},'%tid,T,re.S)
    if not m or 'trainerClass = TRAINER_CLASS_' not in m.group(1): return None,None
    p=re.search(r'_MOVES\((\w+)\)',m.group(1)); c=re.search(r'TRAINER_CLASS_(\w+)',m.group(1)); return (p.group(1) if p else None),c.group(1)
def scr(sc):
    m=re.search(r'\n%s::\n(?:\t[^\n]*\n)*?\ttrainerbattle_\w+\s+(TRAINER_\w+)'%re.escape(sc),S_); return m.group(1) if m else None
FLOOR=[('OneIsland',58),('MtEmber',60),('TwoIsland',60),('ThreeIsland',61),('FourIsland',62),('FiveIsland',64),('SixIsland',65),('SevenIsland',66)]
SKIP=('ELDER','ECHO','LEADER','ELITE','CHAMPION')
def fl(n):
    for k,v in FLOOR:
        if n.startswith(k): return v
done=set(); tot=0
for f in sorted(glob.glob('data/maps/*/map.json')):
    n=f.split('/')[2]; floor=fl(n)
    if not floor: continue
    for o in json.load(open(f)).get('object_events',[]):
        if o.get('trainer_type','TRAINER_TYPE_NONE')=='TRAINER_TYPE_NONE': continue
        t=scr(o['script']); p,c=party(t) if t else (None,None)
        if not p or p in done or any(c.startswith(x) for x in SKIP): continue
        done.add(p); m=re.search(r'(%s\[\] = \{)(.*?)(\n\};)'%p,P,re.S)
        if not m: continue
        ls=[int(x) for x in re.findall(r'\.lvl = (\d+)',m.group(2))]
        d=floor-max(ls)
        if d<=0: continue
        nb=re.sub(r'\.lvl = (\d+),(\s*\n\s*)\.species = (SPECIES_\w+)',lambda x:'.lvl = %d,%s.species = %s'%(int(x.group(1))+d,x.group(2),evolve(x.group(3),int(x.group(1))+d)),m.group(2))
        P=P.replace(m.group(0),m.group(1)+nb+m.group(3)); tot+=1; print(n,t[8:],max(ls),'->',max(ls)+d)
open('src/data/trainer_parties.h','w').write(P); print(tot,'equipes')
