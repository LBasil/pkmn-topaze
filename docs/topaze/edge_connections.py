#!/usr/bin/env python3
"""Convertit les warps de bord (ville/route <-> ville/route) en connexions de carte.
Usage: edge_connections.py plan | apply   (apply : NON rejouable, partir d'un git propre)"""
import json,glob,os,re,sys,collections
R='/home/claude/pkmn-topaze/'
L={l.get('id'):l for l in json.load(open(R+'data/layouts/layouts.json'))['layouts']}
M={};P={}
for f in glob.glob(R+'data/maps/*/map.json'):
    j=json.load(open(f)); M[j['id']]=j; P[j['id']]=f
OUT={'MAP_TYPE_TOWN','MAP_TYPE_CITY','MAP_TYPE_ROUTE'}
OPP={'U':'D','D':'U','L':'R','R':'L'}; DIR={'U':'up','D':'down','L':'left','R':'right'}
def dims(mid): l=L[M[mid]['layout']]; return l['width'],l['height']
def side_of(mid,w):
    W,H=dims(mid)
    if w['y']==0: return 'U'
    if w['y']==H-1: return 'D'
    if w['x']==0: return 'L'
    if w['x']==W-1: return 'R'
groups=collections.OrderedDict()
for mid,j in M.items():
    if j.get('map_type') not in OUT or j['layout'] not in L: continue
    for i,w in enumerate(j.get('warp_events',[])):
        d=w['dest_map']
        if d not in M or M[d].get('map_type') not in OUT or M[d]['layout'] not in L: continue
        s=side_of(mid,w)
        if not s: continue
        groups.setdefault((mid,s,d),[]).append(i)
plan=[];skip=[]
done=set()
for (a,s,b),idx in groups.items():
    if (a,s,b) in done: continue
    key=(b,OPP[s],a)
    if key not in groups: skip.append((a,s,b,'pas de retour symetrique')); continue
    if any((c['direction']==DIR[s]) for c in (M[a].get('connections') or [])): skip.append((a,s,b,'connexion deja presente cote '+s)); continue
    if any((c['direction']==DIR[OPP[s]]) for c in (M[b].get('connections') or [])): skip.append((a,s,b,'connexion deja presente cote oppose')); continue
    # offset
    offs=set()
    for i in idx:
        w=M[a]['warp_events'][i]; k=int(w['dest_warp_id'])
        if k>=len(M[b]['warp_events']) or M[b]['warp_events'][k]['dest_map']!=a: continue
        wb=M[b]['warp_events'][k]
        offs.add((w['x']-wb['x']) if s in 'UD' else (w['y']-wb['y']))
    if len(offs)!=1: skip.append((a,s,b,'offsets incoherents %s'%sorted(offs))); continue
    if len(idx)<2 and len(groups[key])<2: skip.append((a,s,b,'un seul warp (coin)')); continue
    plan.append((a,s,b,offs.pop(),idx,groups[key])); done.add((a,s,b)); done.add(key)
N=lambda m: M[m]['name'] if 'name' in M[m] else m
if sys.argv[1]=='plan':
    for p in plan: print('OK  %-34s %s -> %-34s offset %3d (%d+%d warps)'%(p[0][4:],p[1],p[2][4:],p[3],len(p[4]),len(p[5])))
    for s in skip: print('SKIP %-34s %s -> %-34s %s'%(s[0][4:],s[1],s[2][4:],s[3]))
    print(len(plan),'conversions,',len(skip),'ignorees')

if sys.argv[1]=='apply':
    removed=collections.defaultdict(set)
    for a,sd,b,off,ia,ib in plan:
        removed[a]|=set(ia); removed[b]|=set(ib)
        M[a].setdefault('connections',None); M[b].setdefault('connections',None)
        M[a]['connections']=(M[a]['connections'] or [])+[{'map':b,'offset':off,'direction':DIR[sd]}]
        M[b]['connections']=(M[b]['connections'] or [])+[{'map':a,'offset':-off,'direction':DIR[OPP[sd]]}]
    newidx={}
    for m,rs in removed.items():
        k=0; mp={}
        for i in range(len(M[m]['warp_events'])):
            if i in rs: continue
            mp[i]=k; k+=1
        newidx[m]=mp
    bad=[]
    for mid,j in M.items():
        for w in j.get('warp_events',[]):
            d=w['dest_map']
            if d in newidx:
                k=int(w['dest_warp_id'])
                if k in newidx[d]: w['dest_warp_id']=str(newidx[d][k])
                elif k in removed[d]: bad.append((mid,w['x'],w['y'],d,k))
    for m,rs in removed.items():
        M[m]['warp_events']=[w for i,w in enumerate(M[m]['warp_events']) if i not in rs]
    for mid,j in M.items(): open(P[mid],'w').write(json.dumps(j,indent=2)+'\n')
    print('warps vers warps supprimes (a verifier):',bad)
    # scripts : warp MAP_X, id
    ids={mid:newidx[mid] for mid in newidx}
    pat=re.compile(r'^(\s*warp\w*\s+)(MAP_\w+)(\s*,\s*)(\d+)(\s*(?:,.*)?)$')
    n=0
    for f in glob.glob(R+'data/**/*.inc',recursive=True):
        t=open(f).read(); out=[]; ch=False
        for line in t.split('\n'):
            m=pat.match(line)
            if m and m.group(2) in ids and int(m.group(4))!=255:
                rest=m.group(5); nargs=rest.count(',')
                if nargs in (0,2) and int(m.group(4)) in ids[m.group(2)]:
                    nl=m.group(1)+m.group(2)+m.group(3)+str(ids[m.group(2)][int(m.group(4))])+rest
                    if nl!=line: ch=True; n+=1; line=nl
            out.append(line)
        if ch: open(f,'w').write('\n'.join(out))
    print('lignes de scripts remappees:',n)
    # table de brouillard : paires dont les tilesets different
    def ts(mid): l=L[M[mid]['layout']]; return l['primary_tileset'],l['secondary_tileset']
    pairs=[(M[a]['layout'],M[b]['layout']) for a,sd,b,o,ia,ib in plan if ts(a)!=ts(b)]
    with open(R+'include/topaze_fog_pairs.h','w') as f:
        f.write('// genere par docs/topaze/edge_connections.py : connexions dont les tilesets different (bande de raccord remplacee par un decor neutre)\n')
        f.write('static const u16 sTopazeFogPairs[][2] = {\n')
        for x,y in pairs: f.write('    {%s, %s},\n    {%s, %s},\n'%(x,y,y,x))
        f.write('    {0xFFFF, 0xFFFF},\n};\n')
    print(len(pairs),'paires en mode brouillard sur',len(plan))
