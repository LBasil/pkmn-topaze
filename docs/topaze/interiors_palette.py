#!/usr/bin/env python3
"""Interieurs (19/10) : met la Tour Spinelle (pokemon_tower), le Tunnel Roche (rock_tunnel) et le musee de Pyropia (museum) a l'ambiance de leur ville voisine
par remappage de palettes (degrades par luminance). Idempotent : les palettes d'origine sont sauvegardees dans docs/topaze/reference/pal_orig/<tileset>/ et
toujours relues de la. Usage : python3 docs/topaze/interiors_palette.py"""
import colorsys, os, shutil
T = 'data/tilesets/secondary/'
B = 'docs/topaze/reference/pal_orig/'
def ramp(stops):
    def f(v):
        v = max(0, min(1, v)) * (len(stops) - 1); i = min(int(v), len(stops) - 2); t = v - i
        return tuple(int(round(stops[i][k] + (stops[i + 1][k] - stops[i][k]) * t)) for k in range(3))
    return f
q = lambda c: tuple(min(255, (x // 8) * 8 + 7) if x > 247 else (x // 8) * 8 for x in c)
SLATE = ramp([(20, 14, 32), (46, 52, 70), (90, 90, 115), (126, 122, 142), (172, 189, 205), (222, 230, 238)])
TEAL = ramp([(8, 36, 44), (30, 70, 84), (60, 120, 138), (110, 170, 190), (190, 228, 238), (240, 250, 255)])
COBALT = ramp([(16, 24, 72), (41, 57, 148), (74, 123, 197), (156, 189, 238), (230, 240, 255)])
BASALT = ramp([(18, 14, 12), (42, 34, 30), (77, 64, 58), (115, 100, 92), (164, 130, 110), (222, 190, 170)])
EMBER = ramp([(60, 16, 8), (150, 40, 20), (229, 106, 30), (255, 190, 90), (255, 240, 190)])
def hsv(c): return colorsys.rgb_to_hsv(c[0] / 255, c[1] / 255, c[2] / 255)
def lum(c): return (0.3 * c[0] + 0.59 * c[1] + 0.11 * c[2]) / 255
def rock_tunnel(c):
    h, s, v = hsv(c); h *= 360
    if s < 0.08 and v > 0.2: return c
    if 30 <= h <= 80 and s > 0.15: return SLATE(lum(c) * 1.05)      # sol olive -> gris-violet
    if 150 <= h <= 215 and s > 0.1: return TEAL(lum(c) * 0.82)       # roches pales -> sarcelle de Spinellia
    return c
def tower(c):
    h, s, v = hsv(c); h *= 360
    if (h >= 320 or h <= 20) and s > 0.18 and v > 0.3: return COBALT(lum(c) * 1.25)   # rambarde/escalier rose -> cobalt
    return c
def museum(c):
    h, s, v = hsv(c); h *= 360
    if v < 0.12: return c
    if 170 <= h <= 250 and s > 0.15: return EMBER(lum(c) * 1.1)      # vitrines d'eau -> vitrines de braise
    if (h <= 75 or h >= 335) and s > 0.12 and not (s > 0.45 and (h <= 15 or h >= 345)): return BASALT(lum(c) * 1.05)   # bois, murs beiges -> basalte
    if s <= 0.12: return BASALT(lum(c))                               # gris neutres -> basalte
    return c
for ts, fn in (('rock_tunnel', rock_tunnel), ('pokemon_tower', tower), ('museum', museum)):
    od = B + ts + '/'
    os.makedirs(od, exist_ok=True)
    n = 0
    for i in range(16):
        src = T + ts + '/palettes/%02d.pal' % i
        if not os.path.exists(src): continue
        if not os.path.exists(od + '%02d.pal' % i): shutil.copy(src, od + '%02d.pal' % i)
        L = open(od + '%02d.pal' % i).read().split('\n'); out = L[:3]
        for j, l in enumerate(L[3:19]):
            c = tuple(map(int, l.split()))
            r = c if j == 0 else q(fn(c))
            n += r != c; out.append('%d %d %d' % r)
        out += L[19:]
        open(src, 'w').write('\n'.join(out))
        g = T + ts + '/palettes/%02d.gbapal' % i
        if os.path.exists(g): os.remove(g)
    print(ts, 'couleurs changees :', n)
