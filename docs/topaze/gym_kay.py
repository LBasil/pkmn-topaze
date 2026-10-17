#!/usr/bin/env python3
"""Arene de KAY (Pyropia, feu) : decor de l'arene de Rustboro (Emeraude) recolore en roche volcanique / lave. Idempotent."""
import sys; sys.path.insert(0, 'docs/topaze')
from gym_lib import *
def lava(h, s, v, i, ci):
    if s < 0.18:                       # gris, blancs -> basalte
        return 10, 0.25, 0.09 + 0.30 * v ** 1.2
    if 20 <= h < 70:                   # or/ocre des plateformes -> roche rouge sombre, liseres de braise
        return 8 + (h - 40) * 0.2, 0.6, 0.16 + 0.42 * v
    if h < 20 or h >= 330:             # roses -> fissures de braise
        return 16, 0.9, 0.40 + 0.35 * v
    return 6, 0.35, 0.10 + 0.30 * v    # bleus/verts -> roche sombre

if __name__ == '__main__':
    recolor('rustboro', lava)
    L = load('LAYOUT_GYM_EM_RUSTBORO'); L.render().convert('RGB').save('/tmp/kay_gym.png')
    apply_gym('PewterCity_Gym', 'LAYOUT_GYM_EM_RUSTBORO',
        objs={0: (5, 2, 'FACE_DOWN'), 1: (5, 13, 'FACE_DOWN', 4), 2: (3, 18, 'FACE_DOWN')},
        warps=[(5, 19), (6, 19), (6, 19)], bg=[(2, 18), (8, 18)])
