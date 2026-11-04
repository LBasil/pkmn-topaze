#!/usr/bin/env python3
"""Partie « joueur reel » complete : les etapes de run_full.py jouees SANS mode dieu (vrai combat, captures, Centre Pokemon, entrainement).

Usage (cwd = racine du depot, copies dans /tmp/gx) :  python3 -u play.py [etape ...]
Reprend de l'etat sauvegarde de l'etape precedente dans /tmp/gx/st/real_<etape>.ss ; les etats du pilote en mode dieu (st/<etape>.ss)
servent de depart jusqu'a `opan` (aucun combat avant).
"""
import sys, os, json
sys.path.insert(0, '/tmp/gx')
from real_run import *
import run_full as RF

# niveau cible de la meilleure creature avant l'etape (repere : run du 24/10, equipes 11-19, 24-25, 26-30, 35-43, ...)
LEVELS = {'gym1': 14, 'gym2': 22, 'cottage': 24, 'ssanne': 24, 'gym3': 28, 'tower': 30, 'quartz': 30, 'gym4': 38, 'ameth': 38,
          'gym5': 44, 'hema_in': 44, 'hema_tower': 46, 'gym6': 49, 'chron_in': 50, 'chron_key': 50, 'gym7': 52, 'chron_raid': 52,
          'seafoam': 54, 'gym8': 57, 'victory': 58, 'league': 66, 'pg_indigo': 76, 'pg_mine': 70, 'pg_birds': 72, 'pg_ferry': 72, 'pg_sevii': 74, 'pg_sulfura': 76, 'pg_echoes': 76}

_ENC = None
def enc_maps():
    """{carte: (niveau min, niveau max)} des rencontres en herbe."""
    global _ENC
    if _ENC is None:
        _ENC = {}
        d = json.load(open('src/data/wild_encounters.json'))
        for e in d['wild_encounter_groups'][0]['encounters']:
            if 'land_mons' not in e: continue
            ms = e['land_mons']['mons']
            try: nm = RF.mname(e['map'])
            except Exception: continue
            _ENC[nm] = (min(m['min_level'] for m in ms), max(m['max_level'] for m in ms))
    return _ENC

class Player(Real):
    dbg_save = bool(os.environ.get("DBG"))
    def grind_map(s, lvl):
        """Carte avec de l'herbe dont les niveaux sauvages sont proches de `lvl`, la plus proche par le graphe."""
        cur = s.sync(); p = s.pos(); best = None
        for nm, (lo, hi) in enc_maps().items():
            if not (lvl - 14 <= hi <= lvl + 4): continue
            if os.path.isdir('data/maps/' + nm) is False: continue
            if nm in getattr(s, 'bad_maps', set()): continue
            if nm == cur: return nm
            try: rt = RF.route(cur, (p[2], p[3]), nm)
            except Exception: rt = None
            if rt and (best is None or len(rt) < best[0]): best = (len(rt), nm)
        return best[1] if best else None
    def buff(s, *a, **k): log('  (pas de buff : joueur reel)')
    TEAM_MAPS = ('MtMoon_B1F', 'Route4')      # zones atteignables avant le ticket du S.S. Anne
    def ready(s, p, lvl):
        """Equipe prete : 5 membres (si possible), la meilleure creature a `lvl`, la 2e et la 3e pas trop loin derriere."""
        lv = sorted((q['level'] for q in p), reverse=True)
        if not lv or lv[0] < lvl: return False
        if len(p) < 5 and getattr(s, 'can_catch', True): return False
        return all(l >= lvl - (8 if lvl < 60 else 10) for l in lv[1:(3 if lvl < 60 else 5)])
    def ensure(s, lvl, maxsteps=300):
        if not s.getflag('FLAG_GOT_SS_TICKET'): lvl = min(lvl, 30)      # avant le ticket, peu de zones atteignables : on ne s'acharne pas
        if s.ready(s.party(), lvl): return True
        nm = None
        if s.balls() < 3 and getattr(s, 'can_catch', True) and not getattr(s, '_shopped', False):
            s._shopped = True; s.shop_balls()
        if not s.getflag('FLAG_GOT_SS_TICKET') and (len(s.party()) < 5 or max(q['level'] for q in s.party()) >= lvl):
            # constitution de l'equipe : captures dans la grotte (especes encore inconnues)
            for nm in s.TEAM_MAPS:
                if s.ready(s.party(), lvl): return True
                if nm in getattr(s, 'bad_maps', set()): continue
                log('CAPTURES / ENTRAINEMENT', nm, [(q['species'], q['level']) for q in s.party()])
                s.train(nm, lvl, maxsteps, until=lambda p: s.ready(p, lvl) or (len(p) >= 5 and s.balls() < 3))
            if len(s.party()) < 5: s.can_catch = False
            return s.ready(s.party(), lvl) or True
        if not s.getflag('FLAG_GOT_SS_TICKET'): return True
        nm = s.grind_map(lvl)
        if not nm: log('pas de carte d entrainement pour', lvl); return False
        log('ENTRAINEMENT', nm, 'objectif', lvl, [(q['level'], q['hp']) for q in s.party()])
        ok = s.train(nm, lvl, maxsteps, until=lambda p: s.ready(p, lvl))
        if not ok:
            s.bad_maps = getattr(s, 'bad_maps', set()) | {nm}; log('carte d entrainement ecartee', nm)
            return s.ensure(lvl, maxsteps) if len(s.bad_maps) < 6 else False
        return ok

def main(seq):
    names = [n for n, _ in RF.STAGES]
    t = None
    for nm in seq:
        i = names.index(nm)
        if t is None:
            prev = names[i - 1] if i else None
            real = '/tmp/gx/st/real_%s.ss' % prev
            src = ('real_%s' % prev) if os.path.exists(real) else prev
            t = Player.resume(os.environ.get('FROM') or src)
        if os.environ.get('BAD'): t.bad_maps = set(os.environ['BAD'].split(','))
        log('=== REAL STAGE', nm, time.strftime('%H:%M:%S'), [(q['level'], q['hp'], q['maxhp']) for q in t.party()])
        bump = 0
        for attempt in range(10):
            try:
                if t.idle(): t.heal(True); t.learn_hms()
                t.ensure(LEVELS.get(nm, 0) + bump)
                if t.idle():
                    pp = t.party(); b = max(pp, key=lambda q: (q['hp'] > 0, q['level']))
                    if b['i'] > 0: t.lead_swap(b['i']); log('  tete d equipe remise : niveau', b['level'])
                RF.STAGES[i][1](t); break
            except AssertionError as e:
                log('ECHEC etape', nm, 'essai', attempt, e); bump += 3
                if not t.idle(): t.scene(maxn=300)
                t.heal()
        else:
            log('ABANDON etape', nm); t.save('real_fail_' + nm); return
        t.save('real_' + nm)

if __name__ == '__main__':
    main(sys.argv[1:])
