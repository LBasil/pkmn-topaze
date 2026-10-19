#!/usr/bin/env python3
"""Vague 3 de talents (ids 169+). Idempotent. Usage : python3 docs/topaze/add_abilities3.py <depot>"""
import sys
repo = sys.argv[1]
R = lambda p: open(repo + '/' + p).read()
def W(p, s): open(repo + '/' + p, 'w').write(s)
A = [l.split('|') for l in """PUNK_ROCK|PUNK ROCK|Boosts sound moves.
STEELY_SPIRIT|STEELY SPRT|Boosts STEEL moves.
DEFEATIST|DEFEATIST|Weak at half HP or less.
TRIAGE|TRIAGE|Healing moves go first.
BEAST_BOOST|BEAST BOOST|KO raises best stat.""".split('\n')]
h = R('include/constants/abilities.h')
if 'ABILITY_PUNK_ROCK' in h:
    print('deja fait'); sys.exit(0)
n0 = 169
h = h.replace('#define ABILITIES_COUNT %d' % n0, ''.join('#define ABILITY_%s %d\n' % (a[0], n0 + i) for i, a in enumerate(A)) + '\n#define ABILITIES_COUNT %d' % (n0 + len(A)))
W('include/constants/abilities.h', h)
t = R('src/data/text/abilities.h')
ident = lambda c: ''.join(w.capitalize() for w in c.split('_'))
strs = ''.join('static const u8 s%sDescription[] = _("%s");\n' % (ident(a[0]), a[2]) for a in A)
t = t.replace('\nconst u8 *const gAbilityDescriptionPointers', strs + '\nconst u8 *const gAbilityDescriptionPointers', 1)
t = t.replace('    [ABILITY_NORMALIZE] = sNormalizeDescription,\n', '    [ABILITY_NORMALIZE] = sNormalizeDescription,\n' + ''.join('    [ABILITY_%s] = s%sDescription,\n' % (a[0], ident(a[0])) for a in A), 1)
t = t.replace('    [ABILITY_NORMALIZE] = _("NORMALIZE"),\n', '    [ABILITY_NORMALIZE] = _("NORMALIZE"),\n' + ''.join('    [ABILITY_%s] = _("%s"),\n' % (a[0], a[1]) for a in A), 1)
W('src/data/text/abilities.h', t)
print(len(A), 'talents ajoutes')
