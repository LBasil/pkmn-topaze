#!/usr/bin/env python3
"""Detecte les mots inconnus dans les textes de data/maps (anglais). Ignore les mots en MAJUSCULES (noms propres/POKéMON),
les codes {..} et les mots d'une liste blanche (tools/topaze/lint/spell_ok.txt). Usage: spell.py [fichier.inc ...]"""
import re, sys, glob, collections, os
from spellchecker import SpellChecker
sp = SpellChecker()
ok = set()
p = os.path.join(os.path.dirname(__file__), 'spell_ok.txt')
if os.path.exists(p): ok = set(w.strip().lower() for w in open(p) if w.strip())
files = sys.argv[1:] or glob.glob('data/maps/*/*.inc')
cnt = collections.defaultdict(list)
for f in files:
    cur = []
    for i, l in enumerate(open(f, encoding='utf-8', errors='replace'), 1):
        m = re.match(r'^\s*\.string\s+"(.*)"\s*$', l)
        if not m: continue
        t = re.sub(r'\{[^}]*\}|\\[nlp]|\$', ' ', m.group(1))
        for w in re.findall(r"[A-Za-z][a-z']+", t):
            wl = w.lower().strip("'")
            if len(wl) < 4 or wl in ok: continue
            cnt[wl].append((f, i))
unk = sp.unknown(list(cnt))
for w in sorted(unk):
    if w.endswith("'s") or w.endswith("n't") or "'" in w or len(w) < 5: continue
    if re.search(r'(.)\1\1', w): continue          # onomatopees (aaaah, kwaaah...)
    cands = sp.candidates(w) or set()
    close = [c for c in cands if c != w and abs(len(c) - len(w)) <= 1 and sum(a != b for a, b in zip(c, w)) <= 1]
    if not close: continue                            # interjections / noms propres : pas de correction proche
    f, i = cnt[w][0]
    print('%-18s -> %-18s x%-3d %s:%d' % (w, sorted(close)[0], len(cnt[w]), f, i))
