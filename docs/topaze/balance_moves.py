#!/usr/bin/env python3
"""Équilibrage des attaques (jalon 4). Usage : python3 docs/topaze/balance_moves.py <dépôt>
Chaque entrée : MOVE -> {champ: (ancienne valeur attendue, nouvelle valeur)}. Le script refuse de s'appliquer
si l'ancienne valeur ne correspond pas (donc non rejouable deux fois)."""
import re, sys
repo = sys.argv[1]
P = repo + '/src/data/battle_moves.h'
C = {  # précision
 'HYDRO_PUMP': {'accuracy': (80, 85)}, 'BLIZZARD': {'accuracy': (70, 80)}, 'THUNDER': {'accuracy': (70, 80)},
 'FIRE_BLAST': {'accuracy': (85, 90)}, 'SLAM': {'accuracy': (75, 85)}, 'MEGA_KICK': {'accuracy': (75, 80)},
 'CROSS_CHOP': {'accuracy': (80, 85)}, 'DYNAMIC_PUNCH': {'accuracy': (50, 60)}, 'EGG_BOMB': {'accuracy': (75, 80)},
 'SUBMISSION': {'accuracy': (80, 85)}, 'FIRE_SPIN': {'accuracy': (70, 85)}, 'WHIRLPOOL': {'accuracy': (70, 85)},
 'SAND_TOMB': {'accuracy': (70, 85)}, 'CLAMP': {'accuracy': (75, 85), 'power': (35, 40)},
 # trop faibles
 'VINE_WHIP': {'power': (35, 45), 'pp': (10, 25)}, 'SMOG': {'power': (20, 30), 'accuracy': (70, 80)},
 'LICK': {'power': (20, 30)}, 'MUD_SLAP': {'power': (20, 35), 'pp': (10, 15)},
 'THIEF': {'power': (40, 60)}, 'COVET': {'power': (40, 60)}, 'KNOCK_OFF': {'power': (20, 50)},
 # CS : cohérence (Coupe < Force/Cascade/Surf, Vol = 2 tours donc plus fort)
 'CUT': {'power': (60, 65), 'accuracy': (95, 100)}, 'FLY': {'power': (70, 90)},
 'FLASH': {'power': (30, 40)}, 'DIVE': {'power': (60, 80)},
}
s = open(P).read()
for mv, ch in C.items():
    m = re.search(r'(\[MOVE_%s\] =\s*\{.*?\n    \})' % mv, s, re.S)
    b = m.group(1); nb = b
    for k, (old, new) in ch.items():
        a = '.%s = %d,' % (k, old)
        assert a in nb, (mv, k, old)
        nb = nb.replace(a, '.%s = %d,' % (k, new), 1)
    s = s.replace(b, nb, 1)
open(P, 'w').write(s)
print(len(C), 'attaques modifiées')
