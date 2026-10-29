#!/usr/bin/env python3
"""Grotte sans fond : relie les 3 etages (D1->D2 toujours ; D2 -> D3 ou D1 au hasard ; D3 passeur de retour)."""
import sys, json
sys.path.insert(0, 'docs/topaze')
import newmap as N, route_test as R
def reach(nav, s):
    seen = {s}; st = [s]
    while st:
        c = st.pop()
        for dx, dy in ((0, 1), (0, -1), (1, 0), (-1, 0)):
            q = (c[0] + dx, c[1] + dy)
            if q not in seen and not nav.blocked(*q) and nav.step_ok(c, q): seen.add(q); st.append(q)
    return seen
def far(nav, s, avoid):
    r = reach(nav, s)
    ok = [c for c in r if c not in nav.warps and all(abs(c[0]-a[0])+abs(c[1]-a[1]) > 3 for a in avoid)]
    return max(ok, key=lambda c: abs(c[0]-s[0]) + abs(c[1]-s[1]))
M = lambda n: json.load(open('data/maps/%s/map.json' % n))
d1, d2, d3 = M('Depths_1F'), M('Depths_2F'), M('Depths_3F')
st = (18, 21)
n1 = R.Nav('Depths_1F'); f1 = far(n1, st, [st])
d1['warp_events'].append(N.warp(f1[0], f1[1], 'MAP_DEPTHS_2F', 0))
n2 = R.Nav('Depths_2F'); f2 = far(n2, st, [st]); 
d2['warp_events'] = [N.warp(st[0], st[1] + 1, 'MAP_DEPTHS_1F', 1)]   # arrivee: pas de warp d'entree utile ; warp 0 = retour
d2['coord_events'] = [N.trigger(f2[0], f2[1], 'VAR_TEMP_1', 0, 'Depths_2F_EventScript_Fall')]
d2['bg_events'] = []
n3 = R.Nav('Depths_3F')
d3['warp_events'] = [N.warp(st[0], st[1] + 1, 'MAP_DEPTHS_2F', 0)]
for n, d in (('Depths_1F', d1), ('Depths_2F', d2), ('Depths_3F', d3)): N.jdump(d, 'data/maps/%s/map.json' % n)
# warp d'arrivee : D1 warp 1 (f1) -> D2 arrive sur warp 0 (st+1) ; D2 chute -> aleatoire
s2 = open('data/maps/Depths_2F/scripts.inc').read()
s2 += ('Depths_2F_EventScript_Fall::\n\tlockall\n\tmsgbox Depths_2F_Text_Fall\n\trandom 2\n\tcompare VAR_RESULT, 0\n\tgoto_if_eq Depths_2F_EventScript_FallDown\n\twarp MAP_DEPTHS_1F, 255, %d, %d\n\twaitstate\n\tend\n\n'
       'Depths_2F_EventScript_FallDown::\n\twarp MAP_DEPTHS_3F, 255, %d, %d\n\twaitstate\n\tend\n') % (st[0], st[1], st[0], st[1])
s2 = s2.replace('\tcompare VAR_RESULT, 0\n\tgoto_if_eq Depths_2F_EventScript_FallDown', '\tgoto_if_eq VAR_RESULT, 0, Depths_2F_EventScript_FallDown')
open('data/maps/Depths_2F/scripts.inc', 'w').write(s2)
open('data/maps/Depths_2F/text.inc', 'a').write(N.text('Depths_2F_Text_Fall', 'The floor gives way beneath you!'))
# D3 : passeur de retour pres de l'arrivee
nv = R.Nav('Depths_3F'); rc = None
for c in sorted(reach(nv, st), key=lambda c: abs(c[0]-st[0]-2) + abs(c[1]-st[1])):
    if c not in nv.warps and c not in nv.objs and abs(c[0]-st[0]) + abs(c[1]-st[1]) >= 2 and all(not nv.blocked(c[0]+dx, c[1]+dy) for dx, dy in ((0,1),(0,-1),(1,0),(-1,0))): rc = c; break
d3 = M('Depths_3F'); d3['object_events'].append(N.obj('SAILOR', rc[0], rc[1], 'Depths_3F_EventScript_ReturnFerry', el=nv.g[rc[1]*nv.w+rc[0]] >> 12 or 3)); N.jdump(d3, 'data/maps/Depths_3F/map.json')
open('data/maps/Depths_3F/scripts.inc', 'a').write('Depths_3F_EventScript_ReturnFerry::\n\tlock\n\tfaceplayer\n\tmsgbox Depths_3F_Text_ReturnAsk, MSGBOX_YESNO\n\tgoto_if_eq VAR_RESULT, NO, Depths_3F_EventScript_Stay\n\twarp MAP_FUCHSIA_CITY, 255, 24, 27\n\twaitstate\n\tend\n\nDepths_3F_EventScript_Stay::\n\tmsgbox Depths_3F_Text_Stay\n\trelease\n\tend\n')
open('data/maps/Depths_3F/text.inc', 'a').write(N.text('Depths_3F_Text_ReturnAsk', 'Ready to go back to the dock?') + N.text('Depths_3F_Text_Stay', 'Take your time. The tide can wait.'))
