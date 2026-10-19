#!/usr/bin/env python3
"""Audit des movepools : pour chaque espece (types du hack, stats, stade d'evolution), attaques offensives apprises (niveau + CT/CS).
Usage : python3 docs/topaze/audit_movepool.py <depot> [--tsv fichier]. Importable : load(repo) -> (species, moves, learn)."""
import re, sys
def load(repo):
    R = lambda p: open(repo + '/' + p).read()
    mv = {}
    for n, b in re.findall(r'\[MOVE_(\w+)\]\s*=\s*\{(.*?)\n    \},', R('src/data/battle_moves.h'), re.S):
        g = lambda k: re.search(r'\.%s = ([-\w]+)' % k, b).group(1)
        fl = re.search(r'\.flags = ([^\n]*)', b).group(1)
        ty = g('type')[5:]
        phys = ('FLAG_FORCE_PHYSICAL' in fl) or (ty in ('NORMAL','FIGHTING','FLYING','POISON','GROUND','ROCK','BUG','GHOST','STEEL') and 'FLAG_FORCE_SPECIAL' not in fl)
        mv[n] = dict(type=ty, power=int(g('power')), acc=int(g('accuracy')), effect=g('effect')[7:], phys=phys, pri=g('priority'))
    sp = {}
    for n, b in re.findall(r'\[SPECIES_(\w+)\]\s*=\s*\{(.*?)\n    \},', R('src/data/pokemon/species_info.h'), re.S):
        t = re.findall(r'\.types = \{TYPE_(\w+), TYPE_(\w+)\}', b)
        if not t or n == 'NONE': continue
        v = lambda k: int(re.search(r'\.%s = (\d+)' % k, b).group(1))
        sp[n] = dict(types=list(dict.fromkeys(t[0])), hp=v('baseHP'), atk=v('baseAttack'), df=v('baseDefense'), spa=v('baseSpAttack'), spd=v('baseSpDefense'), spe=v('baseSpeed'))
        sp[n]['bst'] = sum(sp[n][k] for k in ('hp','atk','df','spa','spd','spe'))
    # evolutions
    pre = {}; nxt = {}
    for a, rest in re.findall(r'\[SPECIES_(\w+)\]\s*=\s*\{(\{.*?\})\},?\n', R('src/data/pokemon/evolution.h'), re.S):
        for b in re.findall(r'SPECIES_(\w+)\}', rest): pre[b] = a; nxt.setdefault(a, []).append(b)
    for n in sp:
        d = 0; x = n
        while x in pre: x = pre[x]; d += 1
        sp[n]['stage'] = d; sp[n]['final'] = n not in nxt; sp[n]['evo'] = nxt.get(n, [])
    ptr = dict(re.findall(r'\[SPECIES_(\w+)\] = (\w+),', R('src/data/pokemon/level_up_learnset_pointers.h')))
    L = R('src/data/pokemon/level_up_learnsets.h')
    lv = {}
    for var, body in re.findall(r'static const u(?:16|32) (\w+)\[\] = \{\n(.*?)LEVEL_UP_END', L, re.S):
        lv[var] = [(int(a), m) for a, m in re.findall(r'LEVEL_UP_MOVE\((\d+), MOVE_(\w+)\)', body)]
    # CT/CS
    tm = [m for m in re.findall(r'MOVE_(\w+),', R('src/data/party_menu.h').split('sTMHMMoves[] =')[1].split('};')[0])]
    tmsets = {}
    for m in re.finditer(r'\[SPECIES_(\w+)\]\s*=\s*TMHM_LEARNSET\((.*?)\)(?=,\n)', R('src/data/pokemon/tmhm_learnsets.h'), re.S):
        tmsets[m.group(1)] = [x for x in re.findall(r'TMHM\((?:TM|HM)\d+_(\w+)\)', m.group(2))]
    learn = {}
    for n in sp:
        var = ptr.get(n)
        learn[n] = dict(lv=lv.get(var, []), tm=tmsets.get(n, []))
    return sp, mv, learn
if __name__ == '__main__':
    repo = sys.argv[1]
    sp, mv, learn = load(repo)
    import collections
    prob = collections.defaultdict(list)
    for n, s in sp.items():
        if n.startswith('UNOWN') or s['bst'] < 100: continue
        allm = {m for _, m in learn[n]['lv']} | set(learn[n]['tm'])
        dm = [(m, mv[m]) for m in allm if m in mv and mv[m]['power'] > 1 and m not in ('HIDDEN_POWER','FRUSTRATION','RETURN')]
        for ty in s['types']:
            st = [x for x in dm if x[1]['type'] == ty]
            best = max([x[1]['power'] for x in st], default=0)
            need = 75 if s['final'] else 55
            if s['stage'] == 0 and not s['final']: need = 40
            if best == 0: prob['STAB absent'].append((n, ty))
            elif best < need and s['bst'] >= 300: prob['STAB faible'].append((n, ty, best))
        nd = len([1 for m, i in dm])
        if s['final'] and nd < 5: prob['peu offensives (<5)'].append((n, nd))
        stat_phys = s['atk'] >= s['spa']
        cat = [x for x in dm if x[1]['phys'] == stat_phys and x[1]['power'] >= 60]
        if s['final'] and s['bst'] >= 400 and len(cat) < 2: prob['categorie faible'].append((n, 'phys' if stat_phys else 'spec', len(cat)))
    for k, v in prob.items(): print('%-22s %d' % (k, len(v)))
    if '--tsv' in sys.argv:
        with open(sys.argv[sys.argv.index('--tsv') + 1], 'w') as f:
            for k, v in prob.items():
                for x in v: f.write(k + '\t' + '\t'.join(map(str, x)) + '\n')
