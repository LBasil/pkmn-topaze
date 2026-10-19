#!/usr/bin/env python3
"""Attribue les talents de la vague 3 (add_abilities3.py). Usage : python3 docs/topaze/assign_abilities3.py <depot>. Idempotent."""
import re, sys
repo = sys.argv[1]
P = repo + '/src/data/pokemon/species_info.h'
M = {}
for names, b in [('WHISMUR LOUDRED EXPLOUD', 'PUNK_ROCK'), ('SKARMORY ARON LAIRON AGGRON', 'STEELY_SPIRIT'), ('MILTANK', 'TRIAGE'),
                 ('RAIKOU ENTEI SUICUNE', 'BEAST_BOOST'), ('VOLTORB', 'PUNK_ROCK')]:
    for n in names.split(): M[n] = b
s = open(P).read(); miss = []; ch = 0
for n, b in M.items():
    pat = re.compile(r'(\[SPECIES_%s\] =\s*\{.*?\.abilities = \{)(ABILITY_[A-Z_0-9]+), (ABILITY_[A-Z_0-9]+)(\})' % n, re.S)
    m = pat.search(s)
    if not m: miss.append(n); continue
    if m.group(3) != 'ABILITY_' + b: ch += 1
    s = s[:m.start()] + m.group(1) + '%s, ABILITY_%s' % (m.group(2), b) + m.group(4) + s[m.end():]
open(P, 'w').write(s); print('modifies', ch, 'manquants', miss)
