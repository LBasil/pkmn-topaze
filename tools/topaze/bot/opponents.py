#!/usr/bin/env python3
"""Connaissance des adversaires : parse src/data/trainers.h + trainer_parties.h -> opponents.json
{id_dresseur: {name, class, double, ai, party:[{species,lvl,moves,item}]}} ; helpers power()/need_level()."""
import re, json, sys, os
ROOT = os.environ.get('TZ_ROOT', '/home/claude/pkmn-topaze')

def parse(root=ROOT):
    tr = open(root + '/src/data/trainers.h', encoding='utf-8').read()
    pt = open(root + '/src/data/trainer_parties.h', encoding='utf-8').read()
    parties = {}
    for m in re.finditer(r'static const struct TrainerMon\w+ (sParty_\w+)\[\] = \{(.*?)\n\};', pt, re.S):
        mons = []
        for b in re.finditer(r'\{(.*?)\}(?=,\s*(?:\{|\n\}|$))', m.group(2), re.S):
            body = b.group(1)
            g = lambda k: (re.search(r'\.%s\s*=\s*([^,\n]+)' % k, body) or [None, None])[1]
            sp = g('species')
            if not sp: continue
            mv = re.search(r'\.moves\s*=\s*\{([^}]*)\}', body)
            mons.append({'species': sp.strip(), 'lvl': int(g('lvl') or 0), 'item': (g('heldItem') or '').strip() or None,
                         'moves': [x.strip() for x in mv.group(1).split(',') if x.strip()] if mv else []})
        parties[m.group(1)] = mons
    out = {}
    for m in re.finditer(r'\[(TRAINER_\w+)\] = \{(.*?)\n    \},', tr, re.S):
        body = m.group(2)
        nm = re.search(r'\.trainerName = _\("([^"]*)"\)', body)
        cl = re.search(r'\.trainerClass = (\w+)', body)
        dbl = re.search(r'\.doubleBattle = (\w+)', body)
        ai = re.search(r'\.aiFlags = ([^,]+),', body)
        pr = re.search(r'\.party = \w+\((\w+)\)', body)
        if not pr or pr.group(1) not in parties: continue
        out[m.group(1)] = {'name': nm.group(1) if nm else '', 'class': cl.group(1) if cl else '',
                           'double': bool(dbl and dbl.group(1) == 'TRUE'), 'ai': ai.group(1).strip() if ai else '',
                           'party': parties[pr.group(1)]}
    return out

def power(t):
    """(niveau max, niveau moyen, effectif) de l'equipe adverse."""
    lv = [m['lvl'] for m in t['party']] or [0]
    return max(lv), sum(lv) / len(lv), len(lv)

def need_level(t, margin=2):
    """Niveau conseille pour la tete d'equipe : un peu au-dessus du meilleur adverse (double : +2 ; IA forte : +1)."""
    mx, _, n = power(t)
    return mx + margin + (2 if t['double'] else 0) + (1 if 'TRY_TO_FAINT' in t['ai'] or 'SMART' in t['ai'] else 0)

_DB = None
def db():
    global _DB
    if _DB is None:
        p = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'opponents.json')
        _DB = json.load(open(p)) if os.path.exists(p) else parse()
    return _DB

if __name__ == '__main__':
    d = parse(); p = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'opponents.json')
    json.dump(d, open(p, 'w'), indent=0, ensure_ascii=False)
    print(len(d), 'dresseurs ->', p)
    top = sorted(d.items(), key=lambda kv: -power(kv[1])[0])[:8]
    for k, v in top: print(k, v['name'], power(v), need_level(v))
