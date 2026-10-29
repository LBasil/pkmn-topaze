#!/usr/bin/env python3
"""Passeurs : (1) reparer les 'Gate' qui sautaient a End au lieu de la destination suivante, (2) decouper les chaines > 8 destinations en plusieurs passeurs. Idempotent."""
import sys, re, json; sys.path.insert(0, 'docs/topaze')
from zonelib import *
fp = 'data/maps/FuchsiaCity/scripts.inc'; fs = rd(fp)
FER = ['EchoFerryman', 'TideFerrywoman', 'LanternBoatman', 'Apprentice', 'DuskFerrywoman', 'ScribeFerryman', 'SeasonsFerryman']
CH = 10**6        # pas de troncons : trop d'objets sur le quai (limite de 16 objets actifs) ; on utilise SKIP a la place
if 'TOPAZE FERRY CHUNK' in fs: print('deja applique'); raise SystemExit
jm = json.load(open('data/maps/FuchsiaCity/map.json')); nav = R.Nav('FuchsiaCity')
GFX = ['SAILOR', 'FISHER', 'OLD_MAN_1', 'WOMAN_1', 'GENTLEMAN', 'SCIENTIST']
newobjs = []; extra = ''; gi = 0
for F in FER:
    S = 'FuchsiaCity_EventScript_' + F
    dests = sorted(int(x) for x in re.findall(re.escape(S) + r'_EventScript_Dest(\d+)::', fs))
    nums = [0] + dests                                         # 0 = destination inline du script principal
    # (1) gates : GateK -> destination suivante
    for i, k in enumerate(nums):
        nxt = (S + '_EventScript_Dest%d' % nums[i + 1]) if i + 1 < len(nums) else (S + '_EventScript_End')
        if (i + 1) % CH == 0 and i + 1 < len(nums): nxt = S + '_EventScript_End'     # fin de tronçon
        g = re.search(re.escape(S) + r'_EventScript_Gate%d::\n\tmsgbox \w+\n\tgoto (\w+)\n' % k, fs)
        if g: fs = fs[:g.start(1)] + nxt + fs[g.end(1):]
        # NEXT du bloc k
        pat = re.compile(r'(' + (re.escape(S) + '::\n' if k == 0 else re.escape(S) + r'_EventScript_Dest%d::\n' % k) + r'(?:.*\n)*?\tgoto_if_eq VAR_RESULT, 1, )(\w+)\n')
        m = pat.search(fs)
        if m: fs = fs[:m.start(2)] + nxt + fs[m.end(2):]
    # (2) tronçons : nouveaux passeurs
    if len(nums) > CH:
        head = re.search(re.escape(S) + r'::\n((?:\t.*\n)*?\tmsgbox \w+_Hello\n)', fs).group(1)
        orig = [o for o in jm['object_events'] if o['script'] == S][0]
        for p in range(1, (len(nums) + CH - 1) // CH):
            b = nums[p * CH]; PS = S + '_Part%d' % p; gfx = GFX[gi % len(GFX)]; gi += 1
            extra += '%s::\n%s\tgoto %s_EventScript_Dest%d\n\n' % (PS, head, S, b)
            taken = [(o['x'], o['y']) for o in jm['object_events']] + [(o['x'], o['y']) for o in jm['bg_events']] + list(nav.warps) + [(o['x'], o['y']) for o in newobjs]
            c = near(nav, [(x, y) for y in range(nav.h) for x in range(nav.w)], (orig['x'] + 3 * p, orig['y'] + 1), taken, margin=1)
            newobjs.append(N.obj(gfx, c[0], c[1], PS, el=EL(nav, c)))
            print(F, 'part', p, 'dest', b, '->', c, gfx)
wr(fp, fs + '\n@ TOPAZE FERRY CHUNK : passeurs supplementaires (troncons de %d destinations)\n' % CH + extra)
jm['object_events'] += newobjs; N.jdump(jm, 'data/maps/FuchsiaCity/map.json')
