#!/usr/bin/env python3
"""Arene de GRIM (Bourg Quartz, glace/eau) : decor de l'arene de Sootopolis (Emeraude), murs en quartz rose, glace cyan. Idempotent."""
import sys; sys.path.insert(0, 'docs/topaze')
from gym_lib import *
def quartz(h, s, v, i, ci):
    if 235 <= h < 300 and s > 0.08:    # murs lilas -> quartz rose pale
        return 345, 0.18 + s * 0.25, 0.60 + 0.38 * v
    if 190 <= h < 235 and s > 0.35 and v < 0.55:   # bleu acier du fond -> bleu glacier profond
        return 212, s, v * 0.9
    return h, s, v
if __name__ == '__main__':
    recolor('sootopolis', quartz)
    L = load('LAYOUT_GYM_EM_SOOTOPOLIS'); L.render().convert('RGB').save('/tmp/grim_gym.png')
    apply_gym('CeladonCity_Gym', 'LAYOUT_GYM_EM_SOOTOPOLIS',
        objs={0: (4, 9, 'FACE_RIGHT', 3), 1: (13, 8, 'FACE_LEFT', 3), 2: (6, 6, 'FACE_DOWN', 2), 3: (11, 7, 'FACE_DOWN', 2),
              4: (5, 12, 'FACE_RIGHT', 3), 5: (11, 14, 'FACE_LEFT', 3), 6: (8, 2, 'FACE_DOWN'), 7: (6, 23, 'FACE_RIGHT', 3)},
        warps=[(8, 25), (9, 25), (9, 25)], bg=[(6, 24), (10, 24)], drop_objects=(8, 9, 10))
