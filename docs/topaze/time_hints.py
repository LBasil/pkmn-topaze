#!/usr/bin/env python3
"""Indices du temps deregle sur les routes : 12 panneaux/horloges (bg_events), texte anglais. Idempotent. Usage : python3 docs/topaze/time_hints.py"""
import sys, os, json, textwrap
sys.path.insert(0, 'docs/topaze'); sys.path.insert(0, 'tools/topaze/emu'); sys.path.insert(0, '/tmp/gx')
import route_test as R
H = [
 ('Route1', 'A roadside clock. It says 3:07. It has said 3:07 all week.'),
 ('Route3', 'Someone scratched on the rock: THE SUN ROSE TWICE TODAY.'),
 ('Route24', 'A stopped wristwatch lies in the grass. The second hand trembles but never moves.'),
 ('Route6', 'The signpost shadow points west at noon. Even the shadows are lost.'),
 ('Route8', 'A hiker mutters: I left at dawn and arrived at dusk. The walk took ten minutes.'),
 ('Route11', 'A clock on a post. Its hands spin backwards. Slowly. Then fast.'),
 ('Route12', 'The fishing spot sign: BEST HOUR TO FISH... crossed out. Nobody knows the hour anymore.'),
 ('Route15', 'A broken alarm clock rings, though nobody set it. It rings for yesterday.'),
 ('Route16', 'Two calendars nailed to a post show different days. Both are wrong.'),
 ('Route18', 'A bench plaque: RESERVED FOR 6:00 PM. The sky above is dark. The plaque is dry. It is not raining.'),
 ('Route19', 'The tide has not turned since the lights went out in CHRONDROLIA.'),
 ('Route22', 'A cracked hourglass. The sand falls up.'),
]
def wrap(t):
    L = textwrap.wrap(t, 35)
    return '\n'.join('\t.string "%s%s"' % (l, '$' if i == len(L) - 1 else ('\\p' if i % 2 else '\\n')) for i, l in enumerate(L))
for m, t in H:
    mp = 'data/maps/%s/map.json' % m
    if not os.path.exists(mp): print('absent', m); continue
    d = json.load(open(mp)); lab = '%s_EventScript_TimeHint' % m
    if any(b.get('script') == lab for b in d['bg_events']): continue
    nav = R.Nav(m); occ = {(o['x'], o['y']) for o in d['object_events']} | {(b['x'], b['y']) for b in d['bg_events']}
    cx, cy = nav.w // 2 + 4, nav.h // 2 + 2
    pick = None
    for c in sorted(((x, y) for y in range(2, nav.h - 2) for x in range(2, nav.w - 2)), key=lambda c: abs(c[0] - cx) + abs(c[1] - cy)):
        x, y = c
        if any(nav.blocked(x + dx, y + dy) for dx in (-1, 0, 1) for dy in (-1, 0, 1)): continue
        if any(abs(x - o[0]) + abs(y - o[1]) < 3 for o in occ) or any(abs(x - w[0]) + abs(y - w[1]) < 3 for w in nav.warps): continue
        pick = c; break
    if not pick: print('pas de place', m); continue
    d['bg_events'].append({'type': 'sign', 'x': pick[0], 'y': pick[1], 'elevation': nav.g[pick[1] * nav.w + pick[0]] >> 12 or 3, 'player_facing_dir': 'BG_EVENT_PLAYER_FACING_ANY', 'script': lab})
    json.dump(d, open(mp, 'w'), indent=2, ensure_ascii=False); open(mp, 'a').write('\n')
    open('data/maps/%s/scripts.inc' % m, 'a').write('\n@ Topaze: indice du temps deregle\n%s::\n\tmsgbox %s_Text_TimeHint, MSGBOX_SIGN\n\tend\n' % (lab, m))
    open('data/maps/%s/text.inc' % m, 'a').write('\n%s_Text_TimeHint::\n%s\n' % (m, wrap(t)))
    print(m, pick)
