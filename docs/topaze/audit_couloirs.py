# Audit : un dresseur qui voit le joueur s arrete sur la case voisine ; verifie qu il ne coupe aucun warp (lancer a la racine du depot).
import sys,glob,os,json,collections; sys.path[:0]=['/tmp/gx','docs/topaze','tools/topaze/maps']
import route_test as R
V={'UP':(0,-1),'DOWN':(0,1),'LEFT':(-1,0),'RIGHT':(1,0)}
def reach(nav,start,block,objs):
    seen={start}; q=collections.deque([start]); warps=set()
    while q:
        c=q.popleft()
        for dx,dy in V.values():
            m=(c[0]+dx,c[1]+dy)
            if m in seen: continue
            if not(0<=m[0]<nav.w and 0<=m[1]<nav.h): continue
            if m in block or m in objs: continue
            if (nav.g[m[1]*nav.w+m[0]]>>10)&3 or (nav.attr(*m)&0x1ff) in R.WATER: continue
            seen.add(m)
            if m in nav.warps: warps.add(m); continue
            q.append(m)
    return seen,warps
bad=[]
for d in sorted(glob.glob('data/maps/*/map.json')):
    name=d.split('/')[2]
    try: nav=R.Nav(name)
    except Exception as e: continue
    mj=nav.mj
    allobj={(o['x'],o['y']) for o in mj['object_events']}
    for o in mj['object_events']:
        if o.get('trainer_type')!='TRAINER_TYPE_NORMAL' or o.get('trainer_sight_or_berry_tree_id') in ('0',0,None): continue
        mv=o['movement_type'].replace('MOVEMENT_TYPE_FACE_','')
        if mv not in V: continue
        sight=int(o['trainer_sight_or_berry_tree_id']); dx,dy=V[mv]; ox,oy=o['x'],o['y']
        others=allobj-{(ox,oy)}
        for k in range(1,sight+1):
            c=(ox+dx*k,oy+dy*k)
            if not(0<=c[0]<nav.w and 0<=c[1]<nav.h) or nav.blocked(*c) and c not in allobj: break
            if c in allobj: break
            stop=(ox+dx*(k-1),oy+dy*(k-1)) if k>1 else (ox,oy)
            # joueur en c ; dresseur finit en stop
            base_seen,base_w=reach(nav,c,{(ox,oy)},others)
            new_seen,new_w=reach(nav,c,{stop},others)
            if base_w-new_w:
                bad.append((name,o['script'].split('_')[-1],(ox,oy),mv,sight,'joueur',c,'perd',sorted(base_w-new_w)))
                break
for b in bad: print(b)
print(len(bad))
