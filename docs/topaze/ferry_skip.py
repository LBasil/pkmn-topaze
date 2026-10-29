#!/usr/bin/env python3
"""Passeurs : (re)genere l'option SKIP (saute 5 destinations) dans chaque bloc de destination. Idempotent ; a relancer apres toute ajout de destination."""
import re
fp = 'data/maps/FuchsiaCity/scripts.inc'; fs = open(fp).read()
fs = re.sub(r'\tgoto_if_eq VAR_RESULT, 2, \w+\n', '', fs)             # retire les anciens SKIP
FER = ['EchoFerryman', 'TideFerrywoman', 'LanternBoatman', 'Apprentice', 'DuskFerrywoman', 'ScribeFerryman', 'SeasonsFerryman']
SK = 5
for F in FER:
    S = 'FuchsiaCity_EventScript_' + F
    dests = sorted(int(x) for x in re.findall(re.escape(S) + r'_EventScript_Dest(\d+)::', fs)); nums = [0] + dests
    for i, k in enumerate(nums):
        tgt = nums[min(i + SK, len(nums) - 1)]
        tl = S + ('_EventScript_Dest%d' % tgt if tgt else '')
        if i == len(nums) - 1: tl = S + '_EventScript_End'
        head = (re.escape(S) + '::\n') if k == 0 else (re.escape(S) + r'_EventScript_Dest%d::\n' % k)
        m = re.search(r'(' + head + r'(?:.*\n)*?\tgoto_if_eq VAR_RESULT, 1, \w+\n)', fs)
        assert m, (F, k)
        fs = fs[:m.end()] + '\tgoto_if_eq VAR_RESULT, 2, %s\n' % tl + fs[m.end():]
open(fp, 'w').write(fs); print('SKIP regenere')
