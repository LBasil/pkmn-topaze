#!/usr/bin/env python3
"""Lieux 'legers' (sans nouvelle carte) : HORLOGE DE SAFRANIA (quete des 3 indices), MARCHE NOCTURNE (post-game, Safrania), ARCHIVISTE DES ECHOS (Bourg Palette).
Flags FLAG_TOPAZE_CLOCK_1..3 / CLOCK_DONE / ARCHIVE_DONE = FLAG_0x20B..0x20F. Idempotent. Textes anglais PROVISOIRES."""
import sys, os, json, textwrap
sys.path.insert(0, 'docs/topaze'); sys.path.insert(0, 'tools/topaze/emu'); sys.path.insert(0, '/tmp/gx')
import route_test as R
def rd(p): return open(p, encoding='utf-8').read()
def wrap(t):
    s = t.replace('{PLAYER}', 'PLAYERX'); L = [l.replace('PLAYERX', '{PLAYER}') for l in textwrap.wrap(s, 35)]
    return '\n'.join('\t.string "%s%s"' % (l, '$' if i == len(L) - 1 else ('\\p' if i % 2 else '\\n')) for i, l in enumerate(L))
fl = rd('include/constants/flags.h')
if 'FLAG_TOPAZE_CLOCK_1' not in fl:
    add = '\n'.join('#define %s FLAG_0x%X' % (n, 0x20B + i) for i, n in enumerate(['FLAG_TOPAZE_CLOCK_1', 'FLAG_TOPAZE_CLOCK_2', 'FLAG_TOPAZE_CLOCK_3', 'FLAG_TOPAZE_CLOCK_DONE', 'FLAG_TOPAZE_ARCHIVE_DONE'])) + '\n'
    open('include/constants/flags.h', 'w').write(fl.replace('\n#endif // GUARD_CONSTANTS_FLAGS_H', '\n// Topaze: horloge de Safrania / archiviste\n' + add + '\n#endif // GUARD_CONSTANTS_FLAGS_H'))
# les 3 indices qui comptent
for k, m in enumerate(['Route1', 'Route11', 'Route22'], 1):
    p = 'data/maps/%s/scripts.inc' % m; s = rd(p); a = '%s_EventScript_TimeHint::\n' % m
    if 'FLAG_TOPAZE_CLOCK_%d' % k not in s: open(p, 'w').write(s.replace(a, a + '\tsetflag FLAG_TOPAZE_CLOCK_%d\n' % k))
def place(m, gfx, script, prefer, extra_objs=()):
    mp = 'data/maps/%s/map.json' % m; d = json.load(open(mp))
    if any(o.get('script') == script for o in d['object_events']): return None
    nav = R.Nav(m); objs = [(o['x'], o['y']) for o in d['object_events']] + [(b['x'], b['y']) for b in d['bg_events']] + list(extra_objs)
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
                    q = (c[0] + dx, c[1] + dy)
                    if q in seen or q == skip or not free(q) or not nav.step_ok(c, q): continue
                    seen.add(q); st.append(q)
            best = max(best, n)
        return best
    base = comp(); pick = None
    for c in sorted(cells, key=lambda c: abs(c[0] - prefer[0]) + abs(c[1] - prefer[1])):
        x, y = c
        if any(abs(x - o[0]) + abs(y - o[1]) < 3 for o in objs) or any(abs(x - w[0]) + abs(y - w[1]) < 3 for w in nav.warps): continue
        if any((x == t[0] and abs(y - t[1]) <= 7) or (y == t[1] and abs(x - t[0]) <= 7) for t in trainers): continue
        if any(not free((x + dx, y + dy)) for dx in (-1, 0, 1) for dy in (-1, 0, 1)) or x <= 1 or y <= 1 or x >= nav.w - 2 or y >= nav.h - 2: continue
        if comp(c) != base - 1: continue
        pick = c; break
    assert pick, m
    x, y = pick; e = nav.g[y * nav.w + x] >> 12
    d['object_events'].append({"graphics_id": "OBJ_EVENT_GFX_" + gfx, "x": x, "y": y, "elevation": e if e not in (0, 15) else 3, "movement_type": "MOVEMENT_TYPE_FACE_DOWN", "movement_range_x": 1, "movement_range_y": 1,
        "trainer_type": "TRAINER_TYPE_NONE", "trainer_sight_or_berry_tree_id": "0", "script": script, "flag": "0"})
    json.dump(d, open(mp, 'w'), indent=2, ensure_ascii=False); open(mp, 'a').write('\n'); print(m, script, pick); return pick
def app(m, sc, tx):
    open('data/maps/%s/scripts.inc' % m, 'a').write(sc); open('data/maps/%s/text.inc' % m, 'a').write(tx)
def texts(T, **kw): return ''.join('\n%s_%s::\n%s\n' % (T, k, wrap(v)) for k, v in kw.items())
# ---- Horloge de Safrania + marche nocturne
m = 'SaffronCity'
S = 'SaffronCity_EventScript_ClockKeeper'; T = 'SaffronCity_Text_Clock'
if place(m, 'SCIENTIST', S, (30, 28)):
    sc = ('\n@ Topaze: HORLOGE DE SAFRANIA (quete des 3 indices : R1, R11, R22)\n%s::\n\tlock\n\tfaceplayer\n\tgoto_if_set FLAG_TOPAZE_CLOCK_DONE, %s_Done\n'
          '\tgoto_if_unset FLAG_TOPAZE_CLOCK_1, %s_Ask\n\tgoto_if_unset FLAG_TOPAZE_CLOCK_2, %s_Ask\n\tgoto_if_unset FLAG_TOPAZE_CLOCK_3, %s_Ask\n'
          '\tcheckitemspace ITEM_EXP_SHARE, 1\n\tgoto_if_eq VAR_RESULT, FALSE, %s_NoRoom\n\tsetflag FLAG_TOPAZE_CLOCK_DONE\n\tmsgbox %s_Solved\n\tgiveitem ITEM_EXP_SHARE, 1\n\trelease\n\tend\n\n'
          '%s_Ask::\n\tmsgbox %s_Ask\n\trelease\n\tend\n\n%s_Done::\n\tmsgbox %s_Done\n\trelease\n\tend\n\n%s_NoRoom::\n\tmsgbox %s_NoRoom\n\trelease\n\tend\n') % (
        (S,) * 6 + (T,) + (S, T, S, T, S, T))
    tx = texts(T, Ask='The big clock stopped the day the lights died. Read the clocks on ROUTE 1, ROUTE 11 and ROUTE 22 for me, then come back.',
               Solved='3:07 stuck, hands spinning backwards, sand falling up. The same stop, three times. So the clock is not broken. Time is. Take this, it will help you.',
               Done='I stopped fixing the clock. I watch it now. It helps to know where time went.', NoRoom='Your BAG is full. Make room, then come back.')
    app(m, sc, tx)
S2 = 'SaffronCity_EventScript_NightMarket'; T2 = 'SaffronCity_Text_Market'
if place(m, 'MAN', S2, (36, 32)):
    sc = ('\n@ Topaze: MARCHE NOCTURNE (post-game)\n%s::\n\tlock\n\tfaceplayer\n\tgoto_if_unset FLAG_TOPAZE_POSTGAME, %s_Closed\n\tmsgbox %s_Open\n\tpokemart SaffronCity_NightMarketItems\n\tmsgbox %s_Bye\n\trelease\n\tend\n\n'
          '%s_Closed::\n\tmsgbox %s_Closed\n\trelease\n\tend\n\n\t.align 2\nSaffronCity_NightMarketItems::\n\t.2byte ITEM_RARE_CANDY\n\t.2byte ITEM_PP_MAX\n\t.2byte ITEM_MAX_REVIVE\n\t.2byte ITEM_FULL_RESTORE\n\t.2byte ITEM_LUCKY_EGG\n\t.2byte ITEM_NONE\n') % (S2, S2, T2, T2, S2, T2)
    tx = texts(T2, Open='The night market opens when the clocks stop. Look around, {PLAYER}.', Bye='The market closes whenever time says so.', Closed='Come back when the LEAGUE is behind you. The market is not open for you yet.')
    app(m, sc, tx)
# ---- Archiviste des Echos (Bourg Palette)
m = 'PalletTown'; S3 = 'PalletTown_EventScript_EchoArchivist'; T3 = 'PalletTown_Text_Archive'
if place(m, 'WOMAN_1', S3, (26, 22)):
    flags = ['FLAG_ECHO_BEAST_DONE', 'FLAG_ECHO_BEAST2_DONE', 'FLAG_ECHO_BEAST3_DONE', 'FLAG_ECHO_BEAST4_DONE', 'FLAG_ECHO_BEAST5_DONE', 'FLAG_ECHO_BEAST6_DONE', 'FLAG_DONE_ECHO_CELEBI']
    sc = ('\n@ Topaze: ARCHIVISTE DES ECHOS (recompense quand les 7 Echos sont clos)\n%s::\n\tlock\n\tfaceplayer\n\tgoto_if_set FLAG_TOPAZE_ARCHIVE_DONE, %s_Done\n' % (S3, S3)
          + ''.join('\tgoto_if_unset %s, %s_Ask\n' % (f, S3) for f in flags)
          + '\tcheckitemspace ITEM_RARE_CANDY, 5\n\tgoto_if_eq VAR_RESULT, FALSE, %s_NoRoom\n\tsetflag FLAG_TOPAZE_ARCHIVE_DONE\n\tmsgbox %s_Solved\n\tgiveitem ITEM_RARE_CANDY, 5\n\trelease\n\tend\n\n' % (S3, T3)
          + '%s_Ask::\n\tmsgbox %s_Ask\n\trelease\n\tend\n\n%s_Done::\n\tmsgbox %s_Done\n\trelease\n\tend\n\n%s_NoRoom::\n\tmsgbox %s_NoRoom\n\trelease\n\tend\n' % (S3, T3, S3, T3, S3, T3))
    tx = texts(T3, Ask='I keep a record of every ECHO that washed ashore. Seven fragments, seven stories. Close them all and the archive is complete.',
               Solved='Seven ECHOES, seven stories closed. The archive is complete. You may keep these, they never fit on my shelves.',
               Done='The archive is complete. Thank you for writing its last pages.', NoRoom='Your BAG is full. Make room, then come back.')
    app(m, sc, tx)
g = rd('docs/topaze/journal_gen.py')
if 'FLAG_TOPAZE_CLOCK_DONE' not in g:
    i = g.index('assert len(SECTIONS) <= 12')
    g = g[:i] + ('add("SIDE QUESTS", F, "FLAG_TOPAZE_CLOCK_DONE", 0, "THE STOPPED CLOCK", "SAFFRON: a man asks you to read\\\\nthe clocks on ROUTES 1, 11 and 22.", B(2))\n'
                 'add("POST-GAME", F, "FLAG_TOPAZE_ARCHIVE_DONE", 0, "THE ECHO ARCHIVE", "PALLET: a woman keeps record\\\\nof the 7 ECHOES. Close them all.", PV())\n\n') + g[i:]
    open('docs/topaze/journal_gen.py', 'w').write(g)
