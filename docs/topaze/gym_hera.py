#!/usr/bin/env python3
"""Arene de HERA (Apatia, vol/dragon) : decor de l'arene de Mauville (Emeraude), sans faisceaux ni interrupteurs, ciel/ambre. Idempotent."""
import sys; sys.path.insert(0, 'docs/topaze')
from gym_lib import *
def sky(h, s, v, i, ci):
    if 40 <= h < 70 and s > 0.1:       # damier jaune -> ambre / peche du couchant
        return 32 + (h - 55) * 0.3, 0.42 + s * 0.2, 0.70 + 0.28 * v
    if 235 <= h < 300 and s > 0.08:    # murs lilas -> bleu ciel profond
        return 200, 0.35 + s * 0.25, 0.35 + 0.60 * v
    if 160 <= h < 210 and s > 0.4:     # arcs cyan -> blanc (vent)
        return 200, 0.10, 0.95
    return h, s, v
def edits(L):
    replace_ids(L, {672: 650, 673: 650, 680: 650, 681: 650, 712: 650, 720: 650}, collision=0)   # faisceaux -> sol libre
    replace_ids(L, {645: 650}, collision=0)   # eclairs au sol -> sol uni (arene Vol/Dragon, pas electrique)
if __name__ == '__main__':
    edit_layout('mauville', edits)
    recolor('mauville', sky)
    L = load('LAYOUT_GYM_EM_MAUVILLE'); L.render().convert('RGB').save('/tmp/hera_gym.png')
    r = bfs(L, (4, 19)); print('leader atteignable', (5, 3) in r)
    apply_gym('VermilionCity_Gym', 'LAYOUT_GYM_EM_MAUVILLE',
        objs={0: (5, 2, 'FACE_DOWN'), 1: (1, 13, 'FACE_RIGHT', 3), 2: (7, 10, 'FACE_UP', 3), 3: (6, 19, 'FACE_DOWN'), 4: (4, 9, 'FACE_DOWN', 3)},
        warps=[(4, 20), (5, 20), (5, 20)], bg=[(3, 18), (6, 18)], drop_bg_from=2)
