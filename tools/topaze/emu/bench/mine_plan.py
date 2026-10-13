import sys,collections; sys.path.insert(0,'/tmp/gx')
from tz import *
import tz
def mapname(dm): return tz._NAMES[dm.replace('MAP_','').replace('_','').lower()]
def plan(start_map, start_cell, goal_map, goal_cell):
    navs={}
    def nv(n):
        if n not in navs: navs[n]=R.Nav(n)
        return navs[n]
    q=collections.deque([(start_map,start_cell,[])]); seen={(start_map,start_cell)}
    while q:
        m,c,steps=q.popleft(); nav=nv(m)
        nav.objs={(o['x'],o['y']) for o in nav.mj['object_events']}
        if m==goal_map and nav.path(c,goal_cell): return steps+[goal_cell]
        for i,w in enumerate(nav.mj['warp_events']):
            wc=(w['x'],w['y'])
            if nav.path(c,wc) is None: continue
            try: dn=mapname(w['dest_map'])
            except KeyError: continue
            if not dn.startswith('GrenaluxMine'): continue
            dnav=nv(dn); dw=dnav.mj['warp_events'][int(w['dest_warp_id'])]
            nc=(dw['x'],dw['y'])
            if (dn,nc) in seen: continue
            seen.add((dn,nc))
            ws=[x for x in nav.mj['warp_events'] if x['dest_map']==w['dest_map']]
            q.append((dn,nc,steps+[('warp',dn,ws.index(w))]))
    return None
if __name__=='__main__':
    import os; os.chdir('/home/claude/pkmn-topaze')
    print(plan('GrenaluxMine_1F',(18,37),'GrenaluxMine_3F',(14,11)))
