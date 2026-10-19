#!/usr/bin/env python3
"""Pokemon visibles dans la Tour Spinelle, le Tunnel Roche, le musee de Pyropia et la Route 8 (19/10). Idempotent (ne rajoute que ce qui manque).
Chaque Pokemon est pose sur une case libre proche de l'indice donne, sans couper aucun chemin (BFS avant/apres). Usage : python3 docs/topaze/interiors_pokemon.py"""
import json, sys, collections
sys.path.insert(0, 'docs/topaze'); sys.path.insert(0, 'tools/topaze/maps'); sys.path.insert(0, 'tools/topaze/emu')
import route_test as R
# (carte, graphisme, espece, indice (x, y), texte, mouvement)
MONS = [
 ('PokemonTower_3F', 'CUBONE', 'CUBONE', (12, 12), 'CUBONE: Kyarugoo...\\nIt keeps vigil over a grave.', 'LOOK_AROUND'),
 ('PokemonTower_4F', 'CLEFAIRY', 'CLEFAIRY', (8, 8), 'CLEFAIRY: Pippi!\\nIt hums softly near the crystals.', 'LOOK_AROUND'),
 ('PokemonTower_5F', 'JIGGLYPUFF', 'JIGGLYPUFF', (15, 12), 'JIGGLYPUFF: Purin...\\nIt sings a lullaby for the spirits.', 'LOOK_AROUND'),
 ('RockTunnel_1F', 'MACHOP', 'MACHOP', (30, 20), 'MACHOP: Gooh!\\nIt is pushing a boulder around.', 'LOOK_AROUND'),
 ('RockTunnel_1F', 'NIDORINO', 'NIDORINO', (14, 30), 'NIDORINO: Gyuu!\\nIt sniffs around for ore.', 'LOOK_AROUND'),
 ('RockTunnel_B1F', 'SLOWPOKE', 'SLOWPOKE', (20, 20), 'SLOWPOKE: ...Yawn.\\nIt dozes in the cool air.', 'LOOK_AROUND'),
 ('PewterCity_Museum_1F', 'KABUTO', 'KABUTO', (18, 8), 'KABUTO: Kabu!\\nA revived fossil, warming up\\nnext to the lava.', 'LOOK_AROUND'),
 ('PewterCity_Museum_2F', 'SLOWPOKE', 'SLOWPOKE', (13, 5), 'SLOWPOKE: ...Yawn.\\nIt basks in the glow of the lava.', 'LOOK_AROUND'),
 ('Route8', 'SPEAROW', 'SPEAROW', (45, 8), 'SPEAROW: Kerr!\\nIt pecks at the crystals.', 'LOOK_AROUND'),
 ('Route8', 'MEOWTH', 'MEOWTH', (36, 6), 'MEOWTH: Nyaa!\\nIt is chasing something shiny.', 'LOOK_AROUND'),
]
def reach(nav, start, extra):
    seen = {start}; q = collections.deque([start])
    while q:
        c = q.popleft()
        for dx, dy in ((0, 1), (0, -1), (1, 0), (-1, 0)):
            n = (c[0] + dx, c[1] + dy)
            if n in seen or n in extra or not (0 <= n[0] < nav.w and 0 <= n[1] < nav.h): continue
            if nav.blocked(*n) and n not in nav.warps: continue
            if not nav.step_ok(c, n): continue
            seen.add(n)
            if n not in nav.warps: q.append(n)
    return seen
def choose(nav, hint):
    warps = list(nav.warps)
    st = next(c for w in warps for c in [(w[0], w[1] + 1), (w[0], w[1] - 1), (w[0] + 1, w[1]), (w[0] - 1, w[1])] if not nav.blocked(*c))
    base = reach(nav, st, set()); need = {w for w in warps if any(abs(w[0] - c[0]) + abs(w[1] - c[1]) == 1 for c in base)}
    for c in sorted(base, key=lambda c: abs(c[0] - hint[0]) + abs(c[1] - hint[1])):
        if c in nav.warps or c in nav.objs: continue
        if any(abs(c[0] - w[0]) + abs(c[1] - w[1]) < 4 for w in warps): continue
        if any(abs(c[0] - o[0]) + abs(c[1] - o[1]) < 2 for o in nav.objs): continue
        free = sum(1 for dx, dy in ((0, 1), (0, -1), (1, 0), (-1, 0)) if not nav.blocked(c[0] + dx, c[1] + dy))
        if free < 3: continue
        if c == st: continue
        after = reach(nav, st, {c})
        adj = lambda o, S: any((o[0] + dx, o[1] + dy) in S for dx, dy in ((0, 1), (0, -1), (1, 0), (-1, 0)))
        objs_ok = all(adj(o, after) for o in nav.objs if adj(o, base))
        if len(after) >= len(base) - 1 and objs_ok and all(any((w[0] + dx, w[1] + dy) in after for dx, dy in ((0, 1), (0, -1), (1, 0), (-1, 0))) for w in need): return c
    return None
done = 0
for mp, gfx, sp, hint, text, mv in MONS:
    p = 'data/maps/%s/' % mp; mj = json.load(open(p + 'map.json'))
    label = '%s_EventScript_Mon%s' % (mp, sp.capitalize())
    if any(o['script'] == label for o in mj['object_events']): continue
    nav = R.Nav(mp); c = choose(nav, hint)
    if not c: print('PAS DE CASE', mp, sp); continue
    mj['object_events'].append({'type': 'object', 'graphics_id': 'OBJ_EVENT_GFX_' + gfx, 'x': c[0], 'y': c[1], 'elevation': nav.g[c[1] * nav.w + c[0]] >> 12 or 3,
        'movement_type': 'MOVEMENT_TYPE_' + mv, 'movement_range_x': 1, 'movement_range_y': 1, 'trainer_type': 'TRAINER_TYPE_NONE',
        'trainer_sight_or_berry_tree_id': '0', 'script': label, 'flag': '0'})
    json.dump(mj, open(p + 'map.json', 'w'), indent=2); open(p + 'map.json', 'a').write('\n')
    open(p + 'scripts.inc', 'a').write('\n%s::\n\tlock\n\tfaceplayer\n\twaitse\n\tplaymoncry SPECIES_%s, CRY_MODE_NORMAL\n\tmsgbox %s_Text_Mon%s\n\twaitmoncry\n\trelease\n\tend\n' % (label, sp, mp, sp.capitalize()))
    open(p + 'text.inc', 'a').write('\n%s_Text_Mon%s::\n    .string "%s$"\n' % (mp, sp.capitalize(), text))
    print(mp, sp, c); done += 1
print('Pokemon ajoutes :', done)
