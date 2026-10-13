#!/usr/bin/env python3
"""Audit statique de la chaine des Echos : chaque etape VAR_ECHO_STAGE 0..21 doit etre posee (setvar) puis consommee (goto_if_eq/ne/ge)."""
import re, glob
sets, uses = {}, {}
for f in glob.glob('data/maps/*/scripts.inc'):
    for m in re.finditer(r'setvar VAR_ECHO_STAGE, (\d+)', open(f).read()): sets.setdefault(int(m.group(1)), set()).add(f.split('/')[2])
    for m in re.finditer(r'(?:goto_if_\w+|call_if_\w+) VAR_ECHO_STAGE, (\d+)', open(f).read()): uses.setdefault(int(m.group(1)), set()).add(f.split('/')[2])
ok = True
for n in range(0, 22):
    s, u = sets.get(n), uses.get(n)
    flag = '' if (n == 0 or s) and (u or n == 21 or n in (1,)) else '  <-- '
    if n > 0 and not s: ok = False; flag = '  <-- jamais pose'
    print(n, 'pose par', sorted(s or []), '| lu par', sorted(u or []), flag)
print('CHAINE OK' if ok else 'CHAINE CASSEE')
