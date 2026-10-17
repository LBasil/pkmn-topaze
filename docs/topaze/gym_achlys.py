#!/usr/bin/env python3
"""Arene d'ACHLYS (Amethiolite, poison) : decor de l'arene de Fortree (Emeraude) -> haies violettes / sol d'amethyste. Idempotent."""
import sys; sys.path.insert(0, 'docs/topaze')
from gym_lib import *
def poison(h, s, v, i, ci):
    if 40 <= h < 75 and s > 0.12:      # sol jaune -> lilas pale
        return 272, 0.20 + s * 0.15, 0.55 + 0.40 * v
    if 75 <= h < 180 and s > 0.12:     # haies vertes -> violet profond (reflets toxiques verts sur les plus clairs)
        if v > 0.8: return 120, 0.55, 0.75
        return 282, 0.45 + s * 0.2, 0.22 + 0.55 * v
    return h, s * 0.9, v
if __name__ == '__main__':
    recolor('fortree', poison)
    L = load('LAYOUT_GYM_EM_FORTREE'); L.render().convert('RGB').save('/tmp/achlys_gym.png')
    apply_gym('FuchsiaCity_Gym', 'LAYOUT_GYM_EM_FORTREE',
        objs={0: (4, 14, 'FACE_DOWN', 3), 1: (10, 10, 'FACE_LEFT', 2), 2: (5, 17, 'FACE_LEFT', 2), 3: (9, 8, 'FACE_DOWN', 2),
              4: (4, 23, 'FACE_RIGHT', 2), 5: (1, 10, 'FACE_UP', 3), 6: (15, 2, 'FACE_DOWN'), 7: (15, 21, 'FACE_DOWN')},
        warps=[(15, 24), (16, 24), (16, 24)], bg=[(14, 21), (17, 21)])
