#!/usr/bin/env python3
"""Traductions des dialogues : stockage, validation, application temporaire au build.

Stockage : i18n/fr/<Carte>.json  ->  {label: {"fr": "texte", "en": "<EN au moment de la trad>"}}
Format du texte : celui de text.inc (\\n \\p \\l litteraux, {PLAYER}...), sans le $ final.

    python3 tools/topaze/i18n/lang.py stats
    python3 tools/topaze/i18n/lang.py apply fr      # ecrit les textes FR dans data/maps/*/text.inc (sauvegarde dans build/i18n/en)
    python3 tools/topaze/i18n/lang.py restore       # remet l'anglais
    sh tools/topaze/i18n/build_lang.sh fr           # fait tout : apply, make, copie Topaze_FR.gba, restore
"""
import os, re, sys, json, glob, shutil, hashlib
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
from extract import ROOT, parse_text_inc, parse_text_inc_order

STORE = os.path.join(ROOT, 'i18n')
BACKUP = os.path.join(ROOT, 'build', 'i18n', 'en')
MAXW = 35
CHARS = None

def charset():
    global CHARS
    if CHARS is None:
        CHARS = set()
        for l in open(os.path.join(ROOT, 'charmap.txt'), encoding='utf-8'):
            m = re.match(r"^'(.+)'\s+=", l)
            if m:
                CHARS.add(m.group(1).replace("\\'", "'"))
    return CHARS

def load(lang, m):
    p = os.path.join(STORE, lang, m + '.json')
    return json.load(open(p, encoding='utf-8')) if os.path.exists(p) else {}

def save(lang, m, d):
    os.makedirs(os.path.join(STORE, lang), exist_ok=True)
    p = os.path.join(STORE, lang, m + '.json')
    if d:
        json.dump(d, open(p, 'w', encoding='utf-8'), ensure_ascii=False, indent=1, sort_keys=True)
        open(p, 'a').write('\n')
    elif os.path.exists(p):
        os.remove(p)

def lines_of(raw):
    """decoupe en lignes affichees (apres \\n \\l \\p)."""
    return re.split(r'\\n|\\l|\\p', raw)

def vis_len(line):
    return len(re.sub(r'\{[A-Z_0-9]+\}', 'XXXXXXX', line))

def check(raw):
    """liste de problemes d'un texte (vide = ok)."""
    pb = []
    for ln in lines_of(raw):
        if vis_len(ln) > MAXW:
            pb.append('ligne trop longue (%d>%d) : %s' % (vis_len(ln), MAXW, ln))
    cs = charset()
    for ch in re.sub(r'\{[A-Z_0-9]+\}|\\[nlpc]', '', raw):
        if ch not in cs:
            pb.append('caractere absent de la police : %r' % ch)
    if '$' in raw or '"' in raw:
        pb.append('$ et " interdits')
    return pb

def to_inc(label, raw):
    """re-ecrit le texte en lignes .string (coupe apres chaque \\n \\l \\p)."""
    parts = re.findall(r'.*?(?:\\n|\\l|\\p)|.+$', raw, re.S)
    out = ['%s::' % label]
    for i, p in enumerate(parts):
        out.append('\t.string "%s%s"' % (p, '$' if i == len(parts) - 1 else ''))
    return '\n'.join(out) + '\n'

def apply(lang):
    n = 0
    os.makedirs(BACKUP, exist_ok=True)
    for p in sorted(glob.glob(os.path.join(STORE, lang, '*.json'))):
        m = os.path.basename(p)[:-5]
        tr = {k: v['fr'] for k, v in json.load(open(p, encoding='utf-8')).items() if v.get('fr', '').strip()}
        if not tr:
            continue
        ti = os.path.join(ROOT, 'data/maps/%s/text.inc' % m)
        src = open(ti, encoding='utf-8').read()
        shutil.copy(ti, os.path.join(BACKUP, m + '.text.inc'))
        for lab, raw in tr.items():
            pb = check(raw)
            if pb:
                print('! %s : %s' % (lab, pb[0])); continue
            pat = re.compile(r'^%s::\n(?:[ \t]*\.string .*\n?)+' % re.escape(lab), re.M)
            if pat.search(src):
                src = pat.sub(lambda _m: to_inc(lab, raw), src, count=1); n += 1
        open(ti, 'w', encoding='utf-8').write(src)
    print('appliques :', n)

def restore():
    for b in glob.glob(os.path.join(BACKUP, '*.text.inc')):
        m = os.path.basename(b)[:-len('.text.inc')]
        shutil.copy(b, os.path.join(ROOT, 'data/maps/%s/text.inc' % m)); os.remove(b)
    print('anglais restaure')

def stats(lang='fr'):
    from extract import build
    db = build(); tot = done = stale = 0
    for m, es in db.items():
        tr = load(lang, m)
        for e in es:
            tot += 1
            t = tr.get(e['label'])
            if t and t.get('fr', '').strip():
                done += 1
                if t.get('en') != e['en']: stale += 1
    print('%d/%d traduits (%.1f%%), %d a revoir (EN modifie depuis)' % (done, tot, 100.0 * done / max(tot, 1), stale))

if __name__ == '__main__':
    c = sys.argv[1] if len(sys.argv) > 1 else 'stats'
    if c == 'stats': stats()
    elif c == 'apply': apply(sys.argv[2] if len(sys.argv) > 2 else 'fr')
    elif c == 'restore': restore()
