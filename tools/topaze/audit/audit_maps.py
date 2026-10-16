import json,glob,os,collections
M={}
for f in glob.glob('data/maps/*/map.json'):
    n=os.path.basename(os.path.dirname(f))
    try: M[n]=json.load(open(f))
    except: pass
byid={d['id']:n for n,d in M.items() if 'id' in d}
bad=collections.defaultdict(list)
opp={'up':'down','down':'up','left':'right','right':'left'}
for n,d in M.items():
    ws=d.get('warp_events',[])
    for i,w in enumerate(ws):
        dm=w['dest_map']
        if dm in('MAP_DYNAMIC','DYNAMIC'): continue
        if dm not in byid: bad['dest_map inconnue'].append((n,i,dm)); continue
        t=M[byid[dm]]; dw=t.get('warp_events',[]); di=str(w['dest_warp_id'])
        if not di.isdigit() or int(di)>=len(dw): bad['dest_warp_id invalide'].append((n,i,dm,di)); continue
        back=dw[int(di)]
        if back['dest_map']!=d.get('id'): bad['warp non reciproque'].append((n,i,'->',byid[dm],int(di),'revient vers',back['dest_map']))
    for c in d.get('connections') or []:
        cm=c['map']
        if cm not in byid: bad['connexion map inconnue'].append((n,cm)); continue
        t=M[byid[cm]]
        r=[x for x in (t.get('connections') or []) if x['map']==d.get('id') and x['direction']==opp[c['direction']]]
        if not r: bad['connexion non reciproque'].append((n,c['direction'],byid[cm]))
        elif r[0]['offset']!=-c['offset']: bad['offset incoherent'].append((n,c['direction'],byid[cm],c['offset'],r[0]['offset']))
for k,v in bad.items():
    print('##',k,len(v))
    for x in v: print('  ',x)
print(len(M),'cartes')
