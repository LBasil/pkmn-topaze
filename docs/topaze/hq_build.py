#!/usr/bin/env python3
"""Repaire de Bourg Quartz : plans neufs + palettes 'ancienne base Rocket' (rouille) / 'reprise Onybris' (bleu).
Reecrit les 4 map.bin, layouts.json, le tileset SilphCoQuartz (variantes de metatuiles sur des ids inutilises + palettes 8/9/11),
et les map.json (warps, objets, evenements)."""
import json, os, re, struct, sys, colorsys
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import hq_lib as H, hq_floors as F
TS = ROOT + '/data/tilesets/secondary/silph_co_quartz/'
SRC = ROOT + '/docs/topaze/hideout_orig/tileset/'      # copie des fichiers d'origine du tileset (entrees idempotentes)
if not os.path.isdir(SRC):
    os.makedirs(SRC + 'palettes')
    for f in ('metatiles.bin', 'metatile_attributes.bin'): open(SRC + f, 'wb').write(open(TS + f, 'rb').read())
    for i in range(16): open(SRC + 'palettes/%02d.pal' % i, 'w').write(open(TS + 'palettes/%02d.pal' % i).read())
floors = {'B1F': F.b1f(), 'B2F': F.b2f(), 'B3F': F.b3f(), 'B4F': F.b4f()}
MT = bytearray(open(SRC + 'metatiles.bin', 'rb').read()); AT = bytearray(open(SRC + 'metatile_attributes.bin', 'rb').read())
NM = len(MT) // 16
sys.path.insert(0, ROOT + '/tools/topaze/maps'); import mapkit
_pd = mapkit.ts_dir(mapkit.layouts()['LAYOUT_ROCKET_HIDEOUT_B1F']['primary_tileset'])
PM = open(_pd + '/metatiles.bin', 'rb').read(); PA = open(_pd + '/metatile_attributes.bin', 'rb').read()
# ---- ids a conserver : tout ce qui sert aux plans d'origine, aux nouveaux plans, aux constantes SilphCo
keep = set()
for n in ('B1F', 'B2F', 'B3F', 'B4F', 'ELEVATOR'):
    g = H.orig(n) if n != 'ELEVATOR' else struct.unpack('<%dH' % (os.path.getsize(H.ORIGD + '/ELEVATOR.bin') // 2), open(H.ORIGD + '/ELEVATOR.bin', 'rb').read())
    keep |= {v & 0x3ff for v in g}
for c, _ in floors.values(): keep |= {v & 0x3ff for v in c.g}
for m in re.finditer(r'METATILE_SilphCo_\w+\s+0x([0-9A-Fa-f]+)', open(ROOT + '/include/constants/metatile_labels.h').read()): keep.add(int(m.group(1), 16))
# ---- variantes rouille
PALMAP = {12: 8, 10: 9, 7: 11}
need = set()
for c, _ in floors.values():
    for i, v in enumerate(c.g):
        t = v & 0x3ff
        if c.z[i] == 0 and t != 8 and (t >= 640 or t < 640): need.add(t)
free = [i for i in range(640, 640 + 384) if i not in keep and (i - 640) < 384]
need = sorted(need)
assert len(free) >= len(need), (len(free), len(need))
var = {}
for t, f in zip(need, free):
    var[t] = f
    if t >= 640: raw, att = MT[(t - 640) * 16:(t - 640) * 16 + 16], AT[(t - 640) * 4:(t - 640) * 4 + 4]
    else: raw, att = PM[t * 16:t * 16 + 16], PA[t * 4:t * 4 + 4]
    ent = list(struct.unpack('<8H', raw))
    ent = [(e & 0x0fff) | (PALMAP.get(e >> 12, e >> 12) << 12) for e in ent]
    off = (f - 640) * 16
    if off + 16 > len(MT): MT.extend(bytes(off + 16 - len(MT))); 
    MT[off:off + 16] = struct.pack('<8H', *ent)
    ao = (f - 640) * 4
    if ao + 4 > len(AT): AT.extend(bytes(ao + 4 - len(AT)))
    AT[ao:ao + 4] = att
open(TS + 'metatiles.bin', 'wb').write(MT); open(TS + 'metatile_attributes.bin', 'wb').write(AT)
print('variantes rouille :', len(var), '/ ids libres', len(free))
# ---- palettes : 8 <- 12 ; 9 <- 10 ; 11 <- 7  (poussiere : desature, chauffe, assombrit)
def rust(col):
    r, g, b = col
    if (r, g, b) == (255, 0, 255): return col
    h, l, s = colorsys.rgb_to_hls(r / 255, g / 255, b / 255)
    # bleu glace -> beige/gris-brun poussiereux
    l2 = l * 0.80 + 0.02
    h2 = 0.085 if s > 0.05 else h
    s2 = s * 0.42
    rr, gg, bb = colorsys.hls_to_rgb(h2, l2, s2)
    return (min(255, int(rr * 255)), min(255, int(gg * 255)), min(255, int(bb * 255)))
def rdpal(p): L = open(p).read().split(); n = int(L[2]); return [tuple(int(x) for x in L[3 + 3 * i:6 + 3 * i]) for i in range(n)]
for dst, srcp in ((8, 12), (9, 10), (11, 7)):
    pal = [rust(c) for c in rdpal(SRC + 'palettes/%02d.pal' % srcp)]
    open(TS + 'palettes/%02d.pal' % dst, 'w').write('JASC-PAL\n0100\n16\n' + ''.join('%d %d %d\n' % c for c in pal))
# ---- map.bin
LJ = json.load(open(ROOT + '/data/layouts/layouts.json'))
for name, (c, A) in floors.items():
    words = [(v & 0xfc00) | var.get(v & 0x3ff, v & 0x3ff) if c.z[i] == 0 else v for i, v in enumerate(c.g)]
    c.g = words
    c.save(ROOT + '/data/layouts/RocketHideout_%s/map.bin' % name)
    for l in LJ['layouts']:
        if l.get('id') == 'LAYOUT_ROCKET_HIDEOUT_' + name: l['width'], l['height'] = c.w, c.h
json.dump(LJ, open(ROOT + '/data/layouts/layouts.json', 'w'), indent=2); open(ROOT + '/data/layouts/layouts.json', 'a').write('\n')
# ---- map.json
def edit(name, fn):
    p = ROOT + '/data/maps/RocketHideout_%s/map.json' % name
    m = json.load(open(p)); fn(m); json.dump(m, open(p, 'w'), indent=2); open(p, 'a').write('\n')
def place(m, script, x, y, mv=None):
    for o in m['object_events']:
        if o['script'] == script:
            o['x'], o['y'] = x, y
            if mv: o['movement_type'] = 'MOVEMENT_TYPE_FACE_' + mv
            return
    raise KeyError(script)
def hidden(m, item, x, y):
    for b in m['bg_events']:
        if b.get('item') == item: b['x'], b['y'] = x, y; return
    raise KeyError(item)
def setwarps(m, lst):
    ws = m['warp_events']; assert len(ws) == len(lst), (len(ws), len(lst))
    for w, (x, y) in zip(ws, lst): w['x'], w['y'] = x, y
def f_b1(m):
    P = 'RocketHideout_B1F_EventScript_'
    setwarps(m, [(12, 2), (1, 17), (6, 17), (23, 16), (24, 16), (25, 16)])
    place(m, P + 'Grunt1', 22, 17, 'LEFT'); place(m, P + 'Grunt2', 15, 4, 'DOWN'); place(m, P + 'Grunt3', 14, 21, 'UP')
    place(m, P + 'Grunt4', 5, 20, 'UP'); place(m, P + 'Grunt5', 7, 13, 'LEFT')
    place(m, P + 'ItemEscapeRope', 15, 26); place(m, P + 'ItemHyperPotion', 8, 19)
    hidden(m, 'ITEM_PP_UP', 15, 18)
def f_b4(m):
    P = 'RocketHideout_B4F_EventScript_'
    setwarps(m, [(4, 20), (19, 19), (20, 19), (21, 19)] if len(m['warp_events']) == 4 else [(4, 20), (19, 19), (20, 19)])
    place(m, P + 'Giovanni', 19, 2, 'DOWN'); place(m, P + 'SilphScope', 21, 2); place(m, P + 'Grunt1', 5, 6, 'DOWN'); place(m, P + 'LiftKey', 3, 2)
    place(m, P + 'Grunt2', 16, 12, 'RIGHT'); place(m, P + 'Grunt3', 19, 12, 'LEFT')
    place(m, P + 'ItemTM49', 1, 7); place(m, P + 'ItemMaxEther', 2, 15); place(m, P + 'ItemCalcium', 8, 22)
    hidden(m, 'ITEM_NEST_BALL', 21, 7); hidden(m, 'ITEM_NET_BALL', 14, 6)
def f_b3(m):
    for b in m['bg_events']:
        if b.get('script') == 'RocketHideout_B3F_EventScript_Ledger': b['x'], b['y'] = 15, 7
edit('B3F', f_b3)
edit('B1F', f_b1)
def f_b4_pre(m):
    if len(m['warp_events']) == 3:
        w = dict(m['warp_events'][2]); m['warp_events'].append(w)
    f_b4(m)
edit('B4F', f_b4_pre)
# ---- scripts : barrieres + ascenseur
def sub(path, pairs):
    s = open(ROOT + path).read()
    for a, b in pairs:
        assert a in s, (path, a); s = s.replace(a, b)
    open(ROOT + path, 'w').write(s)
def barrier(x0, y0):
    return ('\tsetmetatile %d, %d, METATILE_SilphCo_HideoutBarrier_TopLeft_Floor, 1\n\tsetmetatile %d, %d, METATILE_SilphCo_HideoutBarrier_TopRight_Floor, 1\n'
            '\tsetmetatile %d, %d, METATILE_SilphCo_HideoutBarrier_BottomLeft, 1\n\tsetmetatile %d, %d, METATILE_SilphCo_HideoutBarrier_BottomRight, 1\n'
            '\tsetmetatile %d, %d, METATILE_SilphCo_HideoutFloor_ShadeFull, 0\n\tsetmetatile %d, %d, METATILE_SilphCo_HideoutFloor_ShadeFull, 0\n'
            % (x0, y0, x0 + 1, y0, x0, y0 + 1, x0 + 1, y0 + 1, x0, y0 + 2, x0 + 1, y0 + 2))
def unbarrier(x0, y0):
    return ('\tsetmetatile %d, %d, METATILE_SilphCo_HideoutFloor_ShadeFull, 0\n\tsetmetatile %d, %d, METATILE_SilphCo_HideoutFloor, 0\n'
            '\tsetmetatile %d, %d, METATILE_SilphCo_HideoutFloor_ShadeFull, 0\n\tsetmetatile %d, %d, METATILE_SilphCo_HideoutFloor, 0\n'
            '\tsetmetatile %d, %d, METATILE_SilphCo_HideoutFloor_ShadeFull, 0\n\tsetmetatile %d, %d, METATILE_SilphCo_HideoutFloor, 0\n'
            % (x0, y0, x0 + 1, y0, x0, y0 + 1, x0 + 1, y0 + 1, x0, y0 + 2, x0 + 1, y0 + 2))
def swap_block(path, label, new):
    s = open(ROOT + path).read()
    m = re.search(r'(%s::\n)((?:\tsetmetatile[^\n]*\n)+)' % re.escape(label), s); assert m, label
    s = s[:m.start(2)] + new + s[m.end(2):]; open(ROOT + path, 'w').write(s)
B1 = '/data/maps/RocketHideout_B1F/scripts.inc'; B4 = '/data/maps/RocketHideout_B4F/scripts.inc'
swap_block(B1, 'RocketHideout_B1F_EventScript_SetBarrier', barrier(4, 14)); swap_block(B1, 'RocketHideout_B1F_EventScript_RemoveBarrier', unbarrier(4, 14))
swap_block(B4, 'RocketHideout_B4F_EventScript_SetBarrier', barrier(17, 9)); swap_block(B4, 'RocketHideout_B4F_EventScript_RemoveBarrier', unbarrier(17, 9))
EL = '/data/maps/RocketHideout_Elevator/scripts.inc'
s = open(ROOT + EL).read()
s = re.sub(r'(setdynamicwarp MAP_ROCKET_HIDEOUT_B1F, 255, )\d+, \d+', r'\g<1>24, 16', s)
s = re.sub(r'(setdynamicwarp MAP_ROCKET_HIDEOUT_B4F, 255, )\d+, \d+', r'\g<1>20, 19', s)
open(ROOT + EL, 'w').write(s)
print('ok')
