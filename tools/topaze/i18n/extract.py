#!/usr/bin/env python3
"""Extrait tous les dialogues des cartes avec leur contexte (qui parle, ou, a quelle condition de progression).

    python3 tools/topaze/i18n/extract.py            # stats
    from extract import build; db = build()          # {carte: [entree, ...]}

Une entree : {label, en, kind, who:{gfx,x,y,hide,script}, conds:[...], also:[autres chemins]}
`en` = corps du texte tel qu'ecrit dans text.inc (lignes jointes, \\n et \\p conserves, sans le $ final).
"""
import re, os, glob, json, sys

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..'))
def rd(p): return open(os.path.join(ROOT, p), encoding='utf-8').read()


def parse_text_inc(src):
    """{label: corps} ; corps = concatenation des .string (guillemets retires) sans le $ final."""
    out, cur = {}, None
    for line in src.splitlines():
        m = re.match(r'^(\w+)::?\s*$', line)
        if m:
            cur = m.group(1); out[cur] = []; continue
        if cur is None:
            continue
        m = re.match(r'^\s*\.string\s+"(.*)"\s*(@.*)?$', line)
        if m:
            out[cur].append(m.group(1))
        elif line.strip() and not line.strip().startswith('@'):
            cur = None
    res = {}
    for k, v in out.items():
        if not v:
            continue
        s = ''.join(v)
        if s.endswith('$'):
            s = s[:-1]
        res[k] = s
    return res


def parse_scripts(src):
    """{label: [commandes]} (commande = liste de tokens)."""
    out, cur = {}, None
    for line in src.splitlines():
        line = line.split('@')[0].rstrip()
        m = re.match(r'^(\w+)::?\s*$', line)
        if m:
            cur = m.group(1); out[cur] = []; continue
        if cur is None or not line.strip() or line.strip().startswith('.'):
            continue
        t = line.strip().replace(',', ' ').split()
        if t:
            out[cur].append(t)
    return out


def parse_events(src):
    ev = {'npc': [], 'coord': [], 'sign': []}
    for line in src.splitlines():
        t = [x.strip() for x in line.strip().split(None, 1)]
        if not t:
            continue
        a = [x.strip() for x in t[1].split(',')] if len(t) > 1 else []
        if t[0] == 'object_event' and len(a) >= 12:
            ev['npc'].append({'id': a[0], 'gfx': a[1], 'x': int(a[2]), 'y': int(a[3]), 'script': a[10], 'hide': a[11], 'ttype': a[8]})
        elif t[0] == 'coord_event' and len(a) >= 6:
            ev['coord'].append({'x': int(a[0]), 'y': int(a[1]), 'var': a[3], 'val': a[4], 'script': a[5]})
        elif t[0] in ('bg_event', 'bg_sign_event') and len(a) >= 5:
            ev['sign'].append({'x': int(a[0]), 'y': int(a[1]), 'script': a[4] if len(a) > 4 else '0'})
    return ev


COND = {  # commande -> (nb args avant la destination, texte)
    'goto_if_set': 1, 'goto_if_unset': 1, 'goto_if_eq': 2, 'goto_if_ne': 2, 'goto_if_lt': 2, 'goto_if_ge': 2,
    'goto_if_le': 2, 'goto_if_gt': 2, 'goto_if_defeated': 1, 'goto_if_not_defeated': 1,
    'call_if_set': 1, 'call_if_unset': 1, 'call_if_eq': 2, 'call_if_ne': 2, 'call_if_lt': 2, 'call_if_ge': 2,
    'call_if_le': 2, 'call_if_gt': 2, 'call_if_defeated': 1, 'call_if_not_defeated': 1,
}
NEG = {'set': 'unset', 'unset': 'set', 'eq': 'ne', 'ne': 'eq', 'lt': 'ge', 'ge': 'lt', 'le': 'gt', 'gt': 'le',
       'defeated': 'not_defeated', 'not_defeated': 'defeated'}


def cond_str(kind, args):
    return '%s %s' % (kind, ' '.join(args))


def build():
    texts, textmap, scripts, labelmap = {}, {}, {}, {}
    events = {}
    maps = sorted(os.path.basename(os.path.dirname(p)) for p in glob.glob(os.path.join(ROOT, 'data/maps/*/map.json')))
    for m in maps:
        tp = os.path.join(ROOT, 'data/maps/%s/text.inc' % m)
        if os.path.exists(tp):
            t = parse_text_inc(open(tp, encoding='utf-8').read())
            for k, v in t.items():
                texts[k] = v; textmap[k] = m
        sp = os.path.join(ROOT, 'data/maps/%s/scripts.inc' % m)
        if os.path.exists(sp):
            s = parse_scripts(open(sp, encoding='utf-8').read())
            for k, v in s.items():
                scripts[k] = v; labelmap[k] = m
        ep = os.path.join(ROOT, 'data/maps/%s/events.inc' % m)
        events[m] = parse_events(open(ep, encoding='utf-8').read()) if os.path.exists(ep) else {'npc': [], 'coord': [], 'sign': []}
    for p in glob.glob(os.path.join(ROOT, 'data/scripts/*.inc')):
        for k, v in parse_scripts(open(p, encoding='utf-8').read()).items():
            scripts.setdefault(k, v)

    found = {}   # text label -> [(owner descriptor, conds)]

    def walk(label, conds, owner, depth, seen):
        if depth > 14 or label not in scripts or (label, tuple(conds)) in seen:
            return
        seen.add((label, tuple(conds)))
        cur = list(conds)
        for cmd in scripts[label]:
            op, args = cmd[0], cmd[1:]
            for tok in args:
                if tok in texts:
                    lst = found.setdefault(tok, [])
                    if len(lst) < 4 and not any(o is owner and c == cur for o, c in lst):
                        lst.append((owner, list(cur)))
            if op in COND:
                n = COND[op]
                kind = op.split('_if_')[1]
                dest = args[n] if len(args) > n else None
                cargs = args[:n]
                if op.startswith('goto'):
                    if dest:
                        walk(dest, cur + [cond_str(kind, cargs)], owner, depth + 1, seen)
                    cur = cur + [cond_str(NEG[kind], cargs)]
                else:
                    if dest:
                        walk(dest, cur + [cond_str(kind, cargs)], owner, depth + 1, seen)
            elif op == 'map_script_2' and len(args) >= 3:
                walk(args[2], cur + ['eq %s %s' % (args[0], args[1])], owner, depth + 1, seen)
            elif op == 'map_script' and len(args) >= 2:
                walk(args[1], cur, owner, depth + 1, seen)
            elif op in ('goto', 'call') and args:
                walk(args[0], cur, owner, depth + 1, seen)
                if op == 'goto':
                    return
            elif op in ('end', 'return'):
                return
            elif op.startswith('trainerbattle') and len(args) >= 1:
                pass

    for m in maps:
        ev = events[m]
        for n in ev['npc']:
            owner = {'kind': 'trainer' if n['ttype'] != 'TRAINER_TYPE_NONE' else 'npc', 'map': m, 'gfx': n['gfx'], 'x': n['x'], 'y': n['y'], 'hide': n['hide'] if n['hide'] != '0' else '', 'script': n['script']}
            if n['script'] not in ('0x0', '0'):
                walk(n['script'], [], owner, 0, set())
        for c in ev['coord']:
            owner = {'kind': 'trigger', 'map': m, 'gfx': '', 'x': c['x'], 'y': c['y'], 'hide': '', 'script': c['script']}
            base = [] if c['var'] in ('0', '0x0') else ['eq %s %s' % (c['var'], c['val'])]
            walk(c['script'], base, owner, 0, set())
        for s in ev['sign']:
            owner = {'kind': 'sign', 'map': m, 'gfx': '', 'x': s['x'], 'y': s['y'], 'hide': '', 'script': s['script']}
            if s['script'] not in ('0x0', '0'):
                walk(s['script'], [], owner, 0, set())
        # scripts de carte (tables OnTransition / OnFrame / OnLoad...) et scripts sans appelant
        owner = {'kind': 'scene', 'map': m, 'gfx': '', 'x': -1, 'y': -1, 'hide': '', 'script': m + '_MapScripts'}
        walk(m + '_MapScripts', [], owner, 0, set())
    # references globales (scripts, C, donnees) : sert a reperer les textes / scripts jamais utilises
    import collections, re as _re
    refs = collections.Counter()
    for pat in ('data/**/*.inc', 'data/**/*.s', 'data/**/*.json', 'src/**/*.c', 'src/**/*.h', 'include/**/*.h', 'asm/**/*.inc'):
        for p in glob.glob(os.path.join(ROOT, pat), recursive=True):
            if p.endswith('/events.inc') or '/layouts/' in p or p.endswith('layouts.json'):
                continue
            try:
                txt = open(p, encoding='utf-8', errors='ignore').read()
            except Exception:
                continue
            refs.update(_re.findall(r'[A-Za-z_]\w*', txt))
    defs = collections.Counter()
    for p in glob.glob(os.path.join(ROOT, 'data/**/*.inc'), recursive=True) + glob.glob(os.path.join(ROOT, 'data/**/*.s'), recursive=True):
        try:
            defs.update(_re.findall(r'^([A-Za-z_]\w*)::?', open(p, encoding='utf-8', errors='ignore').read(), _re.M))
        except Exception:
            pass
    def nrefs(lab): return refs[lab] - defs[lab]
    refd = set(t for body in scripts.values() for cmd in body for t in cmd[1:])
    dead_roots = []
    for lab, mp in labelmap.items():
        if lab not in refd and not lab.endswith('_MapScripts'):
            if nrefs(lab) > 0:     # appele depuis le C ou une table : vivant
                owner = {'kind': 'scene', 'map': mp, 'gfx': '', 'x': -1, 'y': -1, 'hide': '', 'script': lab}
                walk(lab, [], owner, 0, set())
            else:
                dead_roots.append((lab, mp))
    live = set(found)
    found_live = dict(found)
    found.clear()
    for lab, mp in dead_roots:
        owner = {'kind': 'unused', 'map': mp, 'gfx': '', 'x': -1, 'y': -1, 'hide': '', 'script': lab}
        walk(lab, [], owner, 0, set())
    found_dead = dict(found)
    found.clear(); found.update(found_live)
    db = {m: [] for m in maps}
    order = {}
    for m in maps:
        tp = os.path.join(ROOT, 'data/maps/%s/text.inc' % m)
        if not os.path.exists(tp):
            continue
        for k in parse_text_inc_order(open(tp, encoding='utf-8').read()):
            if k not in texts:
                continue
            ow = found.get(k, [])
            dead = (not ow) and (nrefs(k) <= 0 or k in found_dead)
            e = {'label': k, 'en': texts[k]}
            if ow:
                o, c = ow[0]
                e['kind'] = o['kind']; e['who'] = o; e['conds'] = c
                e['also'] = [{'who': o2, 'conds': c2} for o2, c2 in ow[1:]]
                # un texte atteint depuis une autre carte garde sa carte d'origine dans who.map
            elif dead:
                e['kind'] = 'unused'; e['who'] = None; e['conds'] = []; e['also'] = []
            else:
                e['kind'] = 'other'; e['who'] = None; e['conds'] = []; e['also'] = []
            db[m].append(e)
    return db


def parse_text_inc_order(src):
    return [m.group(1) for m in re.finditer(r'^(\w+)::?\s*$', src, re.M)]


if __name__ == '__main__':
    db = build()
    tot = sum(len(v) for v in db.values())
    kinds = {}
    for v in db.values():
        for e in v:
            kinds[e['kind']] = kinds.get(e['kind'], 0) + 1
    print('cartes', len([m for m in db if db[m]]), 'textes', tot, kinds)
    if len(sys.argv) > 1:
        for e in db.get(sys.argv[1], [])[:12]:
            print(json.dumps(e, ensure_ascii=False)[:400])
