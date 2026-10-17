#!/usr/bin/env python3
"""Arene de HEPHA (Opanihrum, acier) : decor de l'arene de Dewford (Emeraude) recolore en acier / opale noire. Idempotent."""
import sys; sys.path.insert(0, 'docs/topaze')
from gym_lib import *
def steel(h, s, v, i, ci):
    if 12 <= h < 70 and s > 0.2:       # bruns du sol -> acier sombre bleuté
        return 222, 0.30, 0.10 + 0.40 * v
    if 150 <= h < 250 and s > 0.2:     # turquoise des rebords -> acier clair / reflets d'opale
        return 205, 0.35, 0.42 + 0.50 * v
    return 218, 0.14, 0.10 + 0.78 * v  # neutres -> gris acier
if __name__ == '__main__':
    recolor('dewford', steel)
    L = load('LAYOUT_GYM_EM_DEWFORD'); L.render().convert('RGB').save('/tmp/hepha_gym.png')
    apply_gym('ViridianCity_Gym', 'LAYOUT_GYM_EM_DEWFORD',
        objs={0: (15, 3, 'FACE_DOWN', 3), 1: (7, 8, 'FACE_RIGHT', 3), 2: (16, 9, 'FACE_DOWN', 3), 3: (14, 12, 'FACE_RIGHT', 2),
              4: (2, 18, 'FACE_UP', 3), 5: (12, 25, 'FACE_UP', 2), 6: (9, 10, 'FACE_DOWN', 3), 7: (4, 3, 'FACE_DOWN'),
              8: (1, 16, 'FACE_RIGHT', 3), 9: (5, 24, 'FACE_DOWN')},
        warps=[(5, 27), (6, 27), (6, 27)], bg=[(4, 24), (7, 24), (1, 4)])
