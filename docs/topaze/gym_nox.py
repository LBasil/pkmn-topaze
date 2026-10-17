#!/usr/bin/env python3
"""Arene de NOX (Spinellia, spectre/psy) : decor de l'arene de Mossdeep (Emeraude), pastilles de teleportation d'Emeraude
(12 warps internes) ; violet nuit. Idempotent."""
import sys, json; sys.path.insert(0, 'docs/topaze')
from gym_lib import *
def ghost(h, s, v, i, ci):
    if (h < 55 or h >= 330) and s > 0.25:    # orange des bordures -> violet fonce
        return 272, 0.55, 0.20 + 0.55 * v
    if s < 0.22:                              # gris -> indigo sombre
        return 262, 0.28, 0.12 + 0.62 * v ** 1.2
    return h, s * 0.9, v * 0.95
PADS = [(3, 28), (1, 23), (7, 18), (8, 12), (9, 18), (23, 20), (1, 33), (20, 24), (11, 3), (11, 35), (13, 32), (21, 10)]
if __name__ == '__main__':
    recolor('mossdeep', ghost)
    L = load('LAYOUT_GYM_EM_MOSSDEEP'); L.render().convert('RGB').save('/tmp/nox_gym.png')
    apply_gym('SaffronCity_Gym', 'LAYOUT_GYM_EM_MOSSDEEP',
        objs={0: (1, 30, 'FACE_DOWN', 3), 1: (4, 29, 'FACE_UP', 2), 2: (5, 20, 'FACE_DOWN', 2), 3: (4, 23, 'FACE_UP', 2),
              4: (6, 9, 'FACE_DOWN', 2), 5: (7, 5, 'FACE_RIGHT', 2), 6: (23, 7, 'FACE_DOWN'), 7: (22, 25, 'FACE_UP', 2), 8: (5, 33, 'FACE_DOWN')},
        warps=[(6, 35), (7, 35), (7, 35)], bg=[(4, 34), (8, 34)])
    # trainer manquant : 8 dresseurs au total (indices 0..5 et 7 + un dernier ajoute ci-dessous si absent)
    p = 'data/maps/SaffronCity_Gym/map.json'; d = json.load(open(p))
    ex = d['warp_events'][0]
    pairs = {}
    for k in range(0, len(PADS), 2): pairs[PADS[k]] = PADS[k + 1]; pairs[PADS[k + 1]] = PADS[k]
    idx = {xy: 3 + i for i, xy in enumerate(PADS)}
    for xy in PADS:
        t = dict(ex); t['x'], t['y'] = xy; t['dest_map'] = 'MAP_SAFFRON_CITY_GYM'; t['dest_warp_id'] = str(idx[pairs[xy]])
        d['warp_events'].append(t)
    open(p, 'w').write(json.dumps(d, indent=2) + '\n')
