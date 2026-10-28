#!/usr/bin/env python3
"""Mini-quetes PNJ (apporte N objets -> recompense), 7 routes. Idempotent. Textes anglais PROVISOIRES.
Drapeaux FLAG_TOPAZE_QUEST_1..7 = FLAG_0x204.. (verifies inutilises). Usage : python3 docs/topaze/miniquetes.py"""
import sys, os, json, re, textwrap
sys.path.insert(0, 'docs/topaze'); sys.path.insert(0, 'tools/topaze/emu'); sys.path.insert(0, '/tmp/gx')
import route_test as R
Q = [
 dict(map='Route2', gfx='PICNICKER', item='ANTIDOTE', n=3, rew='PP_UP', rn=1, name='BUG BITES', hint='ROUTE 2: a girl needs 3 ANTIDOTES.',
      ask='Ouch! The bugs here bite so hard. Please bring me 3 ANTIDOTES!', ok='Thank you! Take this as thanks.', done='My poison is gone. You are a lifesaver!'),
 dict(map='Route5', gfx='GENTLEMAN', item='REVIVE', n=2, rew='HP_UP', rn=1, name='LOST HEIRLOOM', hint='ROUTE 5: a man needs 2 REVIVES.',
      ask='My POKéMON fainted, and I lost my way. Could you spare 2 REVIVES?', ok='Wonderful! A token of my gratitude.', done='Back on my feet. Thanks to you.'),
 dict(map='Route9', gfx='HIKER', item='REPEL', n=3, rew='PROTEIN', rn=1, name='NO MORE BUGS', hint='ROUTE 9: a hiker needs 3 REPELS.',
      ask='Wild POKéMON keep jumping me. 3 REPELS would save my trip!', ok='Ahh, peace! Take this. I do not need it.', done='Not a single POKéMON bothers me now.'),
 dict(map='Route13', gfx='FISHER', item='ETHER', n=2, rew='IRON', rn=1, name='THE ANGLER', hint='ROUTE 13: an angler needs 2 ETHERS.',
      ask='My best fighter is out of PP. Got 2 ETHERS for an old angler?', ok='That did it! Here, a reward.', done='The big one did not get away this time.'),
 dict(map='Route17', gfx='BIKER', item='FIRE_STONE', n=1, rew='CALCIUM', rn=1, name='THE COLLECTOR', hint='ROUTE 17: a biker wants FIRE STONE.',
      ask='I collect STONES. Bring me a FIRE STONE and I will make it worth your while.', ok='Beautiful! Take this for your trouble.', done='My collection is shining. Thanks, friend.'),
 dict(map='Route20', gfx='SWIMMER_M_LAND', item='ELIXIR', n=2, rew='CARBOS', rn=1, name='SEA MARATHON', hint='ROUTE 20: a swimmer needs ELIXIRS.',
      ask='Long swim ahead. 2 ELIXIRS would keep my team going!', ok='Perfect! Here, a little something.', done='The sea is calm. Good luck out there!'),
 dict(map='Route23', gfx='SCIENTIST', item='LEAF_STONE', n=1, rew='ZINC', rn=1, name='THE RESEARCHER', hint='ROUTE 23: a nerd wants LEAF STONE.',
      ask='I study evolution. Bring me a LEAF STONE for my research.', ok='Fascinating! Please take this in return.', done='My research is moving forward. Thanks!'),
]
def wrap(t):
    L = textwrap.wrap(t, 35)
    return '\n'.join('\t.string "%s%s"' % (l, '$' if i == len(L) - 1 else ('\\p' if i % 2 else '\\n')) for i, l in enumerate(L))
fl = open('include/constants/flags.h').read()
if 'FLAG_TOPAZE_QUEST_1' not in fl:
    add = ''.join('#define FLAG_TOPAZE_QUEST_%d FLAG_0x%X // mini-quete PNJ %d\n' % (i + 1, 0x204 + i, i + 1) for i in range(len(Q)))
    fl = fl.replace('\n#endif // GUARD_CONSTANTS_FLAGS_H', '\n// Topaze: mini-quetes\n' + add + '\n#endif // GUARD_CONSTANTS_FLAGS_H')
    open('include/constants/flags.h', 'w').write(fl)
for k, q in enumerate(Q, 1):
    m = q['map']; mp = 'data/maps/%s/map.json' % m; d = json.load(open(mp)); S = '%s_EventScript_Quest%d' % (m, k); T = '%s_Text_Quest%d' % (m, k)
    if any(o.get('script') == S for o in d['object_events']): continue
    nav = R.Nav(m); objs = [(o['x'], o['y']) for o in d['object_events']]
    trainers = [(o['x'], o['y']) for o in d['object_events'] if o.get('trainer_type', 'TRAINER_TYPE_NONE') != 'TRAINER_TYPE_NONE']
    free = lambda c: not nav.blocked(*c)
    cells = [(x, y) for y in range(nav.h) for x in range(nav.w) if free((x, y)) and (x, y) not in nav.warps]
    def comp(skip=None):
        seen = set(); best = 0
        for s in cells:
            if s in seen or s == skip: continue
            st = [s]; seen.add(s); n = 0
            while st:
                c = st.pop(); n += 1
                for dx, dy in ((0, 1), (0, -1), (1, 0), (-1, 0)):
                    p = (c[0] + dx, c[1] + dy)
                    if p in seen or p == skip or not free(p) or not nav.step_ok(c, p): continue
                    seen.add(p); st.append(p)
            best = max(best, n)
        return best
    base = comp(); cx, cy = nav.w // 2 - 5, nav.h // 2 - 2; pick = None
    bgs = [(b['x'], b['y']) for b in d['bg_events']]
    for c in sorted(cells, key=lambda c: abs(c[0] - cx) + abs(c[1] - cy)):
        x, y = c
        if any(abs(x - o[0]) + abs(y - o[1]) < 3 for o in objs + bgs) or any(abs(x - w[0]) + abs(y - w[1]) < 3 for w in nav.warps): continue
        if any((x == t[0] and abs(y - t[1]) <= 7) or (y == t[1] and abs(x - t[0]) <= 7) for t in trainers): continue
        if any(not free((x + dx, y + dy)) for dx in (-1, 0, 1) for dy in (-1, 0, 1)): continue
        if x <= 1 or y <= 1 or x >= nav.w - 2 or y >= nav.h - 2: continue
        if comp(c) != base - 1: continue
        pick = c; break
    assert pick, m
    x, y = pick; e = nav.g[y * nav.w + x] >> 12
    d['object_events'].append({"graphics_id": "OBJ_EVENT_GFX_" + q['gfx'], "x": x, "y": y, "elevation": e if e not in (0, 15) else 3, "movement_type": "MOVEMENT_TYPE_FACE_DOWN",
        "movement_range_x": 1, "movement_range_y": 1, "trainer_type": "TRAINER_TYPE_NONE", "trainer_sight_or_berry_tree_id": "0", "script": S, "flag": "0"})
    json.dump(d, open(mp, 'w'), indent=2, ensure_ascii=False); open(mp, 'a').write('\n')
    F = 'FLAG_TOPAZE_QUEST_%d' % k
    sc = ('\n@ Topaze: mini-quete %d (%s)\n%s::\n\tlock\n\tfaceplayer\n\tgoto_if_set %s, %s_Done\n\tcheckitem ITEM_%s, %d\n\tgoto_if_eq VAR_RESULT, FALSE, %s_Ask\n'
          '\tcheckitemspace ITEM_%s, %d\n\tgoto_if_eq VAR_RESULT, FALSE, %s_NoRoom\n\tremoveitem ITEM_%s, %d\n\tsetflag %s\n\tmsgbox %s_Ok\n\tgiveitem ITEM_%s, %d\n\trelease\n\tend\n\n'
          '%s_Ask::\n\tmsgbox %s_Ask\n\trelease\n\tend\n\n%s_Done::\n\tmsgbox %s_Done\n\trelease\n\tend\n\n%s_NoRoom::\n\tmsgbox %s_NoRoom\n\trelease\n\tend\n') % (
        k, q['name'], S, F, S, q['item'], q['n'], S, q['rew'], q['rn'], S, q['item'], q['n'], F, T, q['rew'], q['rn'], S, T, S, T, S, T)
    tx = '\n%s_Ask::\n%s\n\n%s_Ok::\n%s\n\n%s_Done::\n%s\n\n%s_NoRoom::\n%s\n' % (T, wrap(q['ask']), T, wrap(q['ok']), T, wrap(q['done']), T, wrap('Your BAG is full. Make room, then come back.'))
    open('data/maps/%s/scripts.inc' % m, 'a').write(sc); open('data/maps/%s/text.inc' % m, 'a').write(tx)
    print(m, pick)
g = open('docs/topaze/journal_gen.py').read()
if '# ---- MINI-QUETES' not in g:
    L = ['# ---- MINI-QUETES (PNJ des routes)']
    for k, q in enumerate(Q, 1):
        L.append('add("SIDE QUESTS", F, "FLAG_TOPAZE_QUEST_%d", 0, "%s", "%s", A)' % (k, q['name'], q['hint']))
    i = g.index('assert len(SECTIONS) <= 12'); g = g[:i] + '\n'.join(L) + '\n\n' + g[i:]
    open('docs/topaze/journal_gen.py', 'w').write(g)
