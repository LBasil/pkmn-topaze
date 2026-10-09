SP = '/tmp/claude-0/-home-claude-pkmn-topaze/63e017b6-62b1-5272-9bc7-2dbea6438581/scratchpad/'
src = open('docs/topaze/route2_gradient.py').read()
i_head = src.index('# ---- portes : sud'); i_art = src.index('# ---- art : cristaux'); i_cut = src.index('for j in range(3):\n    for i in range(3): del OCC[(STONE[0]')
i_tail = src.index('# ------------------------------------------------------------------ ecriture')
head, mid, tail = src[:i_head], src[i_art:i_cut], src[i_tail:]
head = head.replace('# ROUTE 2 « la route du crépuscule »', '# ROUTE 3 « la coulee » (Pyropia -> Route 4), generee avec la machinerie de la Route 2 / de la foret (etage 2 seulement).\n# (en-tete herite de) ROUTE 2 « la route du crépuscule »', 1)
head = head.replace('W, H = 26, 56', 'W, H = 80, 24')
head = head.replace('general_dusk', 'general_scoria').replace('dusk_road', 'scoria_road')
head = head.replace('s = min(0.30, s * 0.45); l = l * 0.58', 's = min(0.10, s * 0.2); l = l * 0.42').replace('s = s * 0.8; l = l * 0.62', 's = s * 0.6; l = l * 0.5')
head = head.replace('PALS[ROCK_SLOT] = stage_pal(3, 0.5)', '''PALS[ROCK_SLOT] = stage_pal(3, 0.5)
def lighten(c):
    h, l, s = colorsys.rgb_to_hls(*[x / 255 for x in c]); r, g, b = colorsys.hls_to_rgb(0.07, min(0.5, l * 1.18 + 0.02), min(0.1, s * 0.3 + 0.015))
    return int(r * 255 + .5), int(g * 255 + .5), int(b * 255 + .5)
for _s in (1, 3, 4): PALS[_s] = [PALS[_s][0]] + [lighten(c) for c in PALS[_s][1:]]
PALS[ROCK_SLOT] = [PALS[ROCK_SLOT][0]] + [tuple(int(v * 0.7) for v in c) for c in PALS[ROCK_SLOT][1:]]''', 1)
head = head.replace('PALS[ROCK_SLOT] = stage_pal(3, 0.5)\n', 'PALS[ROCK_SLOT] = stage_pal(3, 0.5)\nPALS[ROCK_SLOT] = [PALS[ROCK_SLOT][0]] + [tuple(int(v * 0.72) for v in c) for c in PALS[ROCK_SLOT][1:]]\n', 1) if False else head
head = head.replace('def put(x, y, raw_flags', 'def stage_at(x, y): return 2\ndef stage_smooth(x, y): return 2\ndef put(x, y, raw_flags', 1)
mid = mid.replace("b = tube_img(2); ART[('tube', 2)] =", "ART[('tube', 2)] = {} if True else ")
mid = mid.replace("    b = big(st); ART[('big', st)] =", "    ART[('big', st)] = {} if True else ")
mid = mid.replace('for st in range(3):\n    for mask', 'for st in (2,):\n    for mask').replace('for st in range(3)', 'for st in (2,)')
tail = tail.replace('PALS[ART_SLOT[0]]', 'PALS[ART_SLOT[2]]').replace('variant(_m, 1)', 'variant(_m, 2)')
tail = tail.replace('GeneralDusk', 'GeneralScoria').replace('DuskRoad', 'ScoriaRoad').replace('LAYOUT_ROUTE2', 'LAYOUT_ROUTE3').replace('data/layouts/Route2/', 'data/layouts/Route3/')
tail = tail.replace('variant(m, 1) for m in (468, 469, 476, 477)', 'variant(m, 2) for m in (468, 469, 476, 477)')
a = tail.index("json.dump({'signS'"); b = tail.index("blk = sorted")
tail = tail[:a] + "json.dump({'w': W, 'h': H, 'obj': OBJ, 'hid': HID, 'signs': SIGNS, 'face': FACE, 'sight': SIGHT, 'tall': TALL, 'gap': sorted(GAPC)}, open('/tmp/route3_info.json', 'w'))\n" + tail[b:]
tail = tail.replace('/tmp/route2_col.json', '/tmp/route3_col.json').replace("print('route 2 :", "print('route 3 :")
ART_F = open(SP + 'artF.py').read()
import re as _re
ART_F = '\n'.join(l for l in ART_F.split('\n') if "giant_img(st)" not in l and "crater_img(st)" not in l)
ART_F = ART_F.replace("for var in (0, 1):\n        b = dead_img", "for var in (0, 1):\n        b = dead_img")
open('docs/topaze/route3_map.py', 'w').write(head + open(SP + 'geom3.py').read() + '\n' + mid + '\n' + ART_F + '\n' + open(SP + 'block3.py').read() + '\n' + tail)
print('ok')
