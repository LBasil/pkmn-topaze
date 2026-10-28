#!/usr/bin/env python3
"""Le RIVAL DU PASSE : dresseur qui jure t'avoir deja battu (Echos du temps). Route 8, badge 4. Reutilise TRAINER_SR_AND_JR (32).
+ Adrian : scene du 'bal des Proches' (monologue). Idempotent. Usage : python3 docs/topaze/rival_passe.py"""
import sys, os, re, json, textwrap
sys.path.insert(0, 'docs/topaze'); sys.path.insert(0, 'tools/topaze/emu'); sys.path.insert(0, '/tmp/gx')
import route_test as R
def rd(p): return open(p, encoding='utf-8').read()
def wr(p, s): open(p, 'w', encoding='utf-8').write(s)
def wrap(t):
    s = t.replace('{PLAYER}', 'PLAYERX'); L = [l.replace('PLAYERX', '{PLAYER}') for l in textwrap.wrap(s, 35)]
    return '\n'.join('\t.string "%s%s"' % (l, '$' if i == len(L) - 1 else ('\\p' if i % 2 else '\\n')) for i, l in enumerate(L))
op = rd('include/constants/opponents.h')
if 'TRAINER_ECHO_RIVAL' not in op:
    wr('include/constants/opponents.h', re.sub(r'(#define )TRAINER_SR_AND_JR(\s+)', r'\1TRAINER_ECHO_RIVAL\2', op))
    tr = rd('src/data/trainers.h'); m = re.search(r'    \[TRAINER_SR_AND_JR\] = \{.*?\n    \},\n', tr, re.S)
    ent = ('    [TRAINER_ECHO_RIVAL] = {\n        .trainerClass = TRAINER_CLASS_PKMN_TRAINER,\n        .encounterMusic_gender = TRAINER_ENCOUNTER_MUSIC_MALE,\n        .trainerPic = TRAINER_PIC_PSYCHIC_M,\n'
           '        .trainerName = _("ECHO"),\n        .items = {ITEM_HYPER_POTION, ITEM_HYPER_POTION},\n        .doubleBattle = FALSE,\n'
           '        .aiFlags = AI_SCRIPT_CHECK_BAD_MOVE | AI_SCRIPT_TRY_TO_FAINT | AI_SCRIPT_CHECK_VIABILITY,\n        .party = ITEM_CUSTOM_MOVES(sParty_EchoRival),\n    },\n')
    wr('src/data/trainers.h', tr[:m.start()] + ent + tr[m.end():])
    T = [('DUGTRIO', 36, 'EARTHQUAKE ROCK_SLIDE SWORDS_DANCE SUCKER_PUNCH'), ('KADABRA', 36, 'PSYCHIC SHADOW_BALL CALM_MIND RECOVER'), ('HAUNTER', 37, 'SHADOW_BALL SLUDGE_BOMB THUNDERBOLT HYPNOSIS'),
         ('ARCANINE', 38, 'FLARE_BLITZ EXTREME_SPEED CRUNCH CLOSE_COMBAT'), ('SANDSLASH', 39, 'EARTHQUAKE X_SCISSOR SWORDS_DANCE ROCK_SLIDE'), ('GYARADOS', 40, 'WATERFALL CRUNCH EARTHQUAKE DRAGON_DANCE')]
    arr = '// Topaze: ECHO, le rival du passe (Route 8)\nstatic const struct TrainerMonItemCustomMoves sParty_EchoRival[] = {\n' + ''.join(
        '    {\n        .iv = 200,\n        .lvl = %d,\n        .species = SPECIES_%s,\n        .heldItem = ITEM_%s,\n        .moves = {%s},\n    },\n' % (l, s, 'LEFTOVERS' if i < 5 else 'MYSTIC_WATER', ', '.join('MOVE_' + x for x in mv.split())) for i, (s, l, mv) in enumerate(T)) + '};\n'
    tp = rd('src/data/trainer_parties.h')
    wr('src/data/trainer_parties.h', tp.replace('static const struct TrainerMonNoItemDefaultMoves sParty_SrAndJr[] = {DUMMY_TRAINER_MON};\n', arr))
m = 'Route8'; mp = 'data/maps/%s/map.json' % m; d = json.load(open(mp)); S = 'Route8_EventScript_EchoRival'
if not any(o.get('script') == S for o in d['object_events']):
    nav = R.Nav(m); objs = [(o['x'], o['y']) for o in d['object_events']] + [(b['x'], b['y']) for b in d['bg_events']]
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
    base = comp(); pick = None
    for c in sorted(cells, key=lambda c: abs(c[0] - nav.w // 3) + abs(c[1] - nav.h // 2)):
        x, y = c
        if any(abs(x - o[0]) + abs(y - o[1]) < 3 for o in objs) or any(abs(x - w[0]) + abs(y - w[1]) < 3 for w in nav.warps): continue
        if any((x == t[0] and abs(y - t[1]) <= 7) or (y == t[1] and abs(x - t[0]) <= 7) for t in trainers): continue
        if any(not free((x + dx, y + dy)) for dx in (-1, 0, 1) for dy in (-1, 0, 1)) or x <= 1 or y <= 1 or x >= nav.w - 2 or y >= nav.h - 2: continue
        if comp(c) != base - 1: continue
        pick = c; break
    assert pick; x, y = pick; e = nav.g[y * nav.w + x] >> 12
    d['object_events'].append({"graphics_id": "OBJ_EVENT_GFX_MAN", "x": x, "y": y, "elevation": e if e not in (0, 15) else 3, "movement_type": "MOVEMENT_TYPE_FACE_DOWN", "movement_range_x": 1, "movement_range_y": 1,
        "trainer_type": "TRAINER_TYPE_NONE", "trainer_sight_or_berry_tree_id": "0", "script": S, "flag": "0"})
    json.dump(d, open(mp, 'w'), indent=2, ensure_ascii=False); open(mp, 'a').write('\n'); print('ECHO', pick)
    T0 = 'Route8_Text_Echo'
    sc = ('\n@ Topaze: ECHO, le rival du passe\n%s::\n\tlock\n\tfaceplayer\n\tgoto_if_unset FLAG_BADGE04_GET, %s_Early\n\tgoto_if_defeated TRAINER_ECHO_RIVAL, %s_After\n\tmsgbox %s_Intro\n'
          '\tcheckitemspace ITEM_RARE_CANDY, 1\n\tgoto_if_eq VAR_RESULT, FALSE, %s_NoRoom\n\ttrainerbattle_no_intro TRAINER_ECHO_RIVAL, %s_Defeat\n\tmsgbox %s_Win\n\tgiveitem ITEM_RARE_CANDY, 3\n\tmsgbox %s_After\n\trelease\n\tend\n\n'
          '%s_After::\n\tmsgbox %s_After\n\trelease\n\tend\n\n%s_Early::\n\tmsgbox %s_Early\n\trelease\n\tend\n\n%s_NoRoom::\n\tmsgbox %s_NoRoom\n\trelease\n\tend\n') % (
        (S,) + (S,) * 2 + (T0,) + (S,) + (S,) + (T0, T0) + (S, T0, S, T0, S, T0))
    tx = '\n%s_Intro::\n%s\n\n%s_Defeat::\n%s\n\n%s_Win::\n%s\n\n%s_After::\n%s\n\n%s_Early::\n%s\n\n%s_NoRoom::\n%s\n' % (
        T0, wrap('{PLAYER}! There you are. You beat me yesterday, remember? ...Or tomorrow. The days are tangled.'), T0, wrap('Again! I lose again. At least it is consistent.'),
        T0, wrap('Take these. I owe them to you. I think.'), T0, wrap('Tell me when you beat me. I would like to know which day it was.'),
        T0, wrap('Not yet, {PLAYER}. Come back with 4 BADGES. Or I already told you that?'), T0, wrap('Your BAG is full. Make room, then come back.'))
    open('data/maps/%s/scripts.inc' % m, 'a').write(sc); open('data/maps/%s/text.inc' % m, 'a').write(tx)
    g = rd('docs/topaze/journal_gen.py')
    if 'TRAINER_ECHO_RIVAL' not in g:
        i = g.index('assert len(SECTIONS) <= 12')
        g = g[:i] + 'add("SIDE QUESTS", T, "TRAINER_ECHO_RIVAL", 0, "THE RIVAL FROM YESTERDAY", "ROUTE 8: he swears you already\\\\nbeat him. Needs 4 BADGES.", B(4))\n\n' + g[i:]
        wr('docs/topaze/journal_gen.py', g)
# Adrian : scene du bal des Proches
tp = 'data/maps/PalletTown/text.inc'; s = rd(tp)
if 'Adrian_Gather' not in s:
    s = s.replace('PalletTown_Text_ProcheAdrian_Intro::', 'PalletTown_Text_ProcheAdrian_Gather::\n' + wrap(
        '{PLAYER}. THOMAS, LOLA, JORDAN, VIOLETTE, EDOUARD, EMMA... they all told me about you. GAUTHIER, CHLOE, VINCENT, THIBAULT, NATHAN, DYLAN too. We were all waiting here, in our own time. You came for each of us.') + '\n\nPalletTown_Text_ProcheAdrian_Intro::', 1)
    wr(tp, s)
    sp = 'data/maps/PalletTown/scripts.inc'; t = rd(sp)
    t = t.replace('\tmsgbox PalletTown_Text_ProcheAdrian_Intro\n', '\tmsgbox PalletTown_Text_ProcheAdrian_Gather\n\tmsgbox PalletTown_Text_ProcheAdrian_Intro\n', 1); wr(sp, t)
