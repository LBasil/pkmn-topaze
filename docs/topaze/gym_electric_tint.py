#!/usr/bin/env python3
"""Arene de Chrondrolia (ELECTRIK) : on garde le plan (quiz, portes) et on reteinte le laboratoire : sol indigo/ardoise sombre, lueur cyan, jaune des murs conserve.
Idempotent : repart des palettes d'origine (git show). Palettes 7, 8, 12 du tileset cinnabar_gym."""
import colorsys, subprocess, os
D = 'data/tilesets/secondary/cinnabar_gym/palettes/'
def orig(i):
    return subprocess.run(['git', 'show', '03d149d:' + D + '%02d.pal' % i], capture_output=True, text=True).stdout
def tint(r, g, b):
    h, l, s = colorsys.rgb_to_hls(r / 255, g / 255, b / 255)
    if (r, g, b) == (255, 0, 255): return r, g, b
    if s > 0.45 and 0.08 < h < 0.2: return r, g, b            # jaune / or des murs : conserve
    if s > 0.45 and (h < 0.05 or h > 0.9): return r, g, b      # rouge des portes
    if l > 0.88: nh, nl, ns = 0.5, min(0.95, l), 0.55        # blancs -> cyan pale (eclairs, tube)
    else: nh, nl, ns = 0.66, l * 0.62, 0.38 + 0.2 * (1 - l)   # gris -> indigo sombre
    r2, g2, b2 = colorsys.hls_to_rgb(nh, nl, ns)
    return int(r2 * 255 + .5), int(g2 * 255 + .5), int(b2 * 255 + .5)
for i in (7, 8, 12):
    L = orig(i).splitlines(); head = L[:3]; vals = [int(x) for x in ' '.join(L[3:]).split()]
    out = []
    for k in range(0, len(vals), 3): out += list(tint(*vals[k:k + 3]))
    open(D + '%02d.pal' % i, 'w', newline='').write('\r\n'.join(head + [' '.join(map(str, out[k:k + 3])) for k in range(0, len(out), 3)]) + '\r\n')
