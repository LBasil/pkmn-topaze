import sys,collections; sys.path.insert(0,'/tmp/gx')
from tz import *
import tz
_NAMES=tz._NAMES
def mapname(dm): return _NAMES[dm.replace('MAP_','').replace('_','').lower()]
def xreach(start_map,start_cell,passable_objs=lambda n,o: False,limit=None):
    """Atteignabilité à travers les warps (statique). passable_objs(map,obj)->True si l'objet ne bloque pas. Renvoie {map:set(cases)}."""
    navs={}
    def nv(n):
        if n not in navs: navs[n]=R.Nav(n)
        return navs[n]
    seen={}; todo=[(start_map,start_cell)]
    while todo:
        n,c0=todo.pop()
        nav=nv(n)
        if n in seen and c0 in seen[n]: continue
        nav.objs={(o['x'],o['y']) for o in nav.mj['object_events'] if not passable_objs(n,o)}
        comp={c0}; q=collections.deque([c0]); wl=[]
        while q:
            c=q.popleft()
            for dx,dy in((0,1),(0,-1),(1,0),(-1,0)):
                m=(c[0]+dx,c[1]+dy)
                if m in comp: continue
                if m in nav.warps: wl.append(m); comp.add(m); continue
                if nav.blocked(*m):
                    # porte à collision ou warp bloqué : le joueur peut pousser vers elle
                    continue
                comp.add(m); q.append(m)
        # warps à collision (portes) adjacents à la composante
        for w in nav.mj['warp_events']:
            wc=(w['x'],w['y'])
            if wc in comp: continue
            if any(((wc[0]+dx,wc[1]+dy) in comp) for dx,dy in((0,1),(0,-1),(1,0),(-1,0))): wl.append(wc); comp.add(wc)
        seen.setdefault(n,set()).update(comp)
        for wc in wl:
            w=nav.warps[wc]; d=w['dest_map']
            if d in ('MAP_DYNAMIC','DYNAMIC'): continue
            try: dn=mapname(d)
            except KeyError: continue
            if limit and dn not in limit: continue
            dnav=nv(dn); dw=dnav.mj['warp_events'][int(w['dest_warp_id'])] if str(w['dest_warp_id']).isdigit() and int(w['dest_warp_id'])<len(dnav.mj['warp_events']) else None
            if not dw: continue
            ds=(dw['x'],dw['y'])
            for st in [ds]+[(ds[0]+dx,ds[1]+dy) for dx,dy in((0,1),(0,-1),(1,0),(-1,0))]:
                if st==ds or not dnav.blocked(*st):
                    if not(dn in seen and st in seen[dn]): todo.append((dn,st))
    return seen
