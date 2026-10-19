#!/usr/bin/env python3
"""Arene d'Apatia : l'arene est maintenant Vol/Fee, mais le decor (tileset vermilion_gym) etait electrique (sol jaune, rayons cyan).
Recolore les palettes du tileset : jaunes -> bleu ciel / lavande, cyans (rayons) -> rose/blanc. Idempotent (ne touche que les teintes jaunes/cyan).
Usage : python3 docs/topaze/apatia_gym_palette.py"""
import colorsys, os
D = 'data/tilesets/secondary/vermilion_gym/palettes/'
def shift(r, g, b):
    h, s, v = colorsys.rgb_to_hsv(r / 255, g / 255, b / 255); h *= 360
    if s < 0.18 or v < 0.2: return (r, g, b)
    if 35 <= h <= 75: h = 205 + (h - 55) * 0.4            # jaune -> bleu ciel
    elif 170 <= h <= 205: h = 322 + (h - 190) * 0.5       # cyan electrique -> rose
    else: return (r, g, b)
    r2, g2, b2 = colorsys.hsv_to_rgb(h / 360, s * 0.85, v)
    q = lambda x: min(255, int(round(x * 255 / 8)) * 8 + (7 if x > 0.99 else 0))
    return (q(r2), q(g2), q(b2))
n = 0
for i in range(16):
    p = D + '%02d.pal' % i
    if not os.path.exists(p): continue
    L = open(p).read().split('\n'); out = L[:3]; ch = 0
    for l in L[3:19]:
        r, g, b = map(int, l.split()); nr = shift(r, g, b)
        ch += nr != (r, g, b); out.append('%d %d %d' % nr)
    out += L[19:]
    open(p, 'w').write('\n'.join(out)); n += ch
    if os.path.exists(D + '%02d.gbapal' % i): os.remove(D + '%02d.gbapal' % i)
print('couleurs changees :', n)
