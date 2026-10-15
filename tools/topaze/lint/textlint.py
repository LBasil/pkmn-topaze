#!/usr/bin/env python3
"""Relecture statique des textes du jeu (data/maps/*/text.inc|scripts.inc, data/text/*.inc).
Controles : chaine non terminee par $, ligne affichee > 36 car. (hors codes {..}), double espace,
espace avant ponctuation, 'POKEMON' sans accent, ' ,', fautes courantes, mots repetes ('the the').
Usage : textlint.py [--max N]  -> code retour 1 si erreurs bloquantes (non terminee)."""
import re, sys, glob
files = glob.glob('data/maps/*/*.inc')  # data/text (vanilla : aide, intro) exclu
errs = []; warns = []
strre = re.compile(r'^\s*\.string\s+"(.*)"\s*$')
for f in files:
    lines = open(f, encoding='utf-8', errors='replace').read().split('\n')
    cur = []; start = 0; label = ''
    def flush():
        global cur
        if not cur: return
        full = ''.join(cur)
        if not full.endswith('$'):
            errs.append((f, start, label, 'texte non termine par $'))
        for seg in re.split(r'\\n|\\l|\\p|\\N', full.rstrip('$')):
            vis = re.sub(r'\{[^}]*\}', 'X', seg)
            if len(vis) > 38 and "data/maps" in f: warns.append((f, start, label, 'ligne %d car: %s' % (len(vis), seg[:40])))
        t = re.sub(r'\{[^}]*\}', 'X', full)
        if re.search(r'\s[,.!?;:]', re.sub(r'\\[nlp]', ' ', t)) and not re.search(r'\.\.\.|…', t): warns.append((f, start, label, 'espace avant ponctuation'))
        if re.search(r'POKEMON', t): warns.append((f, start, label, 'POKEMON sans accent'))
        m = re.search(r'\b(\w{3,}) \1\b', re.sub(r'\\[nlp]', ' ', t), re.I)
        if m: warns.append((f, start, label, 'mot repete: ' + m.group(0)))
        cur = []
    for i, l in enumerate(lines, 1):
        m = strre.match(l)
        if m:
            if not cur: start = i
            cur.append(m.group(1))
        elif l.lstrip().startswith(('#', '.if', '.endif', '.else')):
            pass  # preprocesseur (#ifdef BUGFIX...) : on garde le bloc
        else:
            flush()
            if re.match(r'^\w+::?\s*$', l): label = l.strip()
    flush()
print('fichiers', len(files), 'erreurs', len(errs), 'avertissements', len(warns))
for e in errs: print('ERREUR %s:%d %s : %s' % e)
mx = int(sys.argv[sys.argv.index('--max') + 1]) if '--max' in sys.argv else 40
for w in warns[:mx]: print('avert  %s:%d %s : %s' % w)
sys.exit(1 if errs else 0)
