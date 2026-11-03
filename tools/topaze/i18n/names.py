#!/usr/bin/env python3
"""Localise les noms (especes, attaques, objets, talents, types, natures) dans les sources, le temps d'un build.
   python3 tools/topaze/i18n/names.py apply fr | restore"""
import os, re, sys, shutil
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, '../../..'))
BACKUP = os.path.join(ROOT, 'build/i18n/names')
sys.path.insert(0, HERE)
import lang

def table(lg, name):
    d = {}
    p = os.path.join(HERE, lg, name + '.txt')
    for l in open(p, encoding='utf-8'):
        l = l.rstrip('\n')
        if '=' in l:
            k, v = l.split('=', 1); d[k] = v
    return d

SKIP = {'DE', 'DU', 'DES', 'LA', 'LE', 'LES', "D'", 'DE LA'}
def fit(v, lim):
    """raccourcit proprement : retire les articles, puis abrege le mot le plus long avec un point."""
    if len(v) <= lim: return v
    toks = [t for t in v.split(' ') if t not in SKIP]
    toks = [t[2:] if t.startswith("D'") and len(t) > 4 else t for t in toks]
    while len(' '.join(toks)) > lim:
        i = max(range(len(toks)), key=lambda k: len(toks[k]))
        t = toks[i].rstrip('.')
        if len(t) <= 3: break
        toks[i] = t[:-1] + '.'
    out = ' '.join(toks)
    return out if len(out) <= lim else out[:lim]

TARGETS = [  # (fichier, table, limite)
    ('src/data/text/species_names.h', 'species', 10),
    ('src/data/text/move_names.h', 'moves', 12),
    ('src/data/text/abilities.h', 'abilities', 12),
    ('src/data/items.h', 'items', 13),
    ('src/battle_main.c', 'types', 6),
    ('src/data/text/nature_names.h', 'natures', 99),
    ('src/data/text/trainer_class_names.h', 'classes', 12),
]
LINE = re.compile(r'_\("([^"]*)"\)')

def apply(lg):
    os.makedirs(BACKUP, exist_ok=True)
    cs = lang.charset()
    n = miss = 0
    for rel, tab, lim in TARGETS:
        t = table(lg, tab)
        p = os.path.join(ROOT, rel)
        src = open(p, encoding='utf-8').read()
        shutil.copy(p, os.path.join(BACKUP, rel.replace('/', '__')))
        def rep(m):
            nonlocal n, miss
            en = m.group(1)
            if '{' in en and tab != 'classes': return m.group(0)
            fr = t.get(en)
            if fr is None and tab == 'items':
                mm = re.fullmatch(r'(TM|HM)(\d\d)', en)
                if mm: fr = ('CT' if mm.group(1) == 'TM' else 'CS') + mm.group(2)
            if fr is None: return m.group(0)
            fr = fr if '{' in fr else fit(fr, lim)
            bad = [c for c in re.sub(r'\{[A-Z]+\}', '', fr) if c not in cs]
            if bad:
                print('! %s -> %s : %r' % (en, fr, bad)); miss += 1; return m.group(0)
            n += 1
            return '_("%s")' % fr
        if tab == 'items':
            src = re.sub(r'(\.name\s*=\s*)_\("([^"]*)"\)', lambda m: m.group(1) + rep(re.match(r'_\("([^"]*)"\)', '_("%s")' % m.group(2))), src)
        elif tab == 'types':
            a = src.index('const u8 gTypeNames'); b = src.index('};', a)
            src = src[:a] + LINE.sub(rep, src[a:b]) + src[b:]
        elif tab == 'abilities':
            a = src.index('const u8 gAbilityNames'); b = src.index('};', a)
            src = src[:a] + LINE.sub(rep, src[a:b]) + src[b:]
        else:
            src = LINE.sub(rep, src)
        open(p, 'w', encoding='utf-8').write(src)
    print('noms localises :', n, '| refuses :', miss)

DESC_TARGETS = [('src/move_descriptions.c', 'move_desc'), ('src/data/items.h', 'item_desc'), ('src/data/text/abilities.h', 'ability_desc')]

def fixtxt(t):
    t = t.replace('Pokémon', 'POKéMON').replace('Poké Ball', 'POKé BALL').replace('Poké', 'POKé').replace('POKÉ', 'POKé')
    return t.replace('\u2019', "'").replace('\u202f', ' ').replace('\u00a0', ' ')

def apply_desc(lg):
    cs = lang.charset(); n = bad = 0
    for rel, tab in DESC_TARGETS:
        p = os.path.join(ROOT, rel)
        src = open(p, encoding='utf-8').read()
        bk = os.path.join(BACKUP, rel.replace('/', '__'))
        if not os.path.exists(bk): shutil.copy(p, bk)
        d = {}
        for l in open(os.path.join(HERE, lg, tab + '.txt'), encoding='utf-8'):
            l = l.rstrip('\n')
            if '|' in l:
                k, v = l.split('|', 1); d[k] = fixtxt(v)
        if tab == 'move_desc':
            sym = dict((c, s) for c, s in re.findall(r'\[(MOVE_\w+)\s*-\s*1\]\s*=\s*(gMoveDescription_\w+)', src))
            d = dict((sym[k], v) for k, v in d.items() if k in sym)
            rx = re.compile(r'(const u8 (gMoveDescription_\w+)\[\] = _\(")((?:[^"\\]|\\.)*)("\))')
        elif tab == 'item_desc':
            rx = re.compile(r'(const u8 (gItemDescription_\w+)\[\] = _\(")((?:[^"\\]|\\.)*)("\))')
            d = dict(('gItemDescription_' + k, v) for k, v in d.items())
        else:
            rx = re.compile(r'(static const u8 (s\w+Description)\[\] = _\(")((?:[^"\\]|\\.)*)("\))')
            d = dict(('s' + k + 'Description', v) for k, v in d.items())
        def rep(m):
            nonlocal n, bad
            v = d.get(m.group(2))
            if v is None: return m.group(0)
            ch = [c for c in re.sub(r'\\[nlp]', '', v) if c not in cs]
            if ch: bad += 1; print('! desc', m.group(2), ch); return m.group(0)
            n += 1
            return m.group(1) + v + m.group(4)
        src = rx.sub(rep, src)
        open(p, 'w', encoding='utf-8').write(src)
    print('descriptions localisees :', n, '| refusees :', bad)

def apply_dex(lg):
    cs = lang.charset(); n = bad = 0
    pe = os.path.join(ROOT, 'src/data/pokemon/pokedex_entries.h'); pt = os.path.join(ROOT, 'src/data/pokemon/pokedex_text_fr.h')
    for p in (pe, pt):
        bk = os.path.join(BACKUP, p[len(ROOT) + 1:].replace('/', '__'))
        if not os.path.exists(bk): shutil.copy(p, bk)
    ent = open(pe, encoding='utf-8').read(); txt = open(pt, encoding='utf-8').read()
    for l in open(os.path.join(HERE, lg, 'dex.txt'), encoding='utf-8'):
        c, cat, t = l.rstrip('\n').split('|', 2)
        t = t.replace('°', ' degrés'); chk = (t + cat).replace('\\n', '')
        if any(ch not in cs for ch in chk):
            bad += 1; print('! dex', c, [ch for ch in chk if ch not in cs][:5]); continue
        m = re.search(r'\[%s\]\s*=\s*\{(.*?)\n    \}' % c, ent, re.S)
        blk = m.group(1)
        sym = re.search(r'\.description = g(\w+)PokedexText', blk).group(1)
        nb = re.sub(r'\.categoryName = _\("[^"]*"\)', '.categoryName = _("%s")' % cat, blk, 1)
        ent = ent.replace(blk, nb, 1)
        body = '\n'.join('    "%s%s"' % (x, '\\n' if i < len(t.split('\\n')) - 1 else '') for i, x in enumerate(t.split('\\n')))
        txt, k = re.subn(r'(const u8 g%sPokedexText\[\] = _\()\s*(?:"(?:[^"\\]|\\.)*"\s*)+(\);)' % sym, lambda mm: mm.group(1) + '\n' + body + mm.group(2), txt, 1)
        n += k
    open(pe, 'w', encoding='utf-8').write(ent); open(pt, 'w', encoding='utf-8').write(txt)
    print('pokedex localise :', n, '| refuses :', bad)

def restore():
    for b in glob_backups():
        rel = os.path.basename(b).replace('__', '/')
        shutil.copy(b, os.path.join(ROOT, rel)); os.remove(b)
    print('noms anglais restaures')

def glob_backups():
    return [os.path.join(BACKUP, f) for f in os.listdir(BACKUP)] if os.path.isdir(BACKUP) else []

if __name__ == '__main__':
    if sys.argv[1] == 'apply': apply(sys.argv[2] if len(sys.argv) > 2 else 'fr'); apply_desc(sys.argv[2] if len(sys.argv) > 2 else 'fr'); apply_dex(sys.argv[2] if len(sys.argv) > 2 else 'fr')
    else: restore()
