#!/usr/bin/env python3
"""Pilote « joueur reel » : Auto (run_full.py) sans mode dieu + cerveau de combat (real.py)."""
import sys, os, struct
sys.path.insert(0, '/tmp/gx')
from run_full import *
import real
import run_full as RF
from real import BattleMixin, sym, name_of

class Real(BattleMixin, Auto):
    _healing = False
    def inbattle(s):
        """Combat en cours, y compris pendant l'ecran d'equipe du combat (gMain.inBattle y est a 0)."""
        if Auto.inbattle(s): return True
        return s.cb2() in ((sym('CB2_UpdatePartyMenu') & ~1), (sym('CB2_InitPartyMenu') & ~1)) and s.ctl() == (sym('WaitForMonSelection') & ~1)
    def press(s, k, n=4, wait=20):
        """Touche ; si une evolution est en cours (apres un combat gagne), on la laisse aller au bout avec A (B l'annulerait)."""
        for _ in range(60):
            nm = name_of(s.cb2())
            if 'Evolution' not in nm and 'EvolutionScene' not in nm: break
            s.e.run(4, KEYS['A']); s.e.run(40, 0)
        s.e.run(n, KEYS[k]); s.e.run(wait, 0)
    def hop(s, e):
        """Si on arrive SUR le tapis de la porte (sortie d'un Centre, d'une maison), le warp ne se redeclenche pas : on pousse vers la sortie."""
        if e[0] == 'warp' and s.knows(15) and any('CutTree' in o.get('script', '') for o in mj(s.sync())['object_events']):
            nav = s.nav(); trees = {(o['x'], o['y']) for o in nav.mj['object_events'] if 'CutTree' in o.get('script', '') and not (o.get('flag', '0') not in ('0', 0) and s.getflag(o['flag']))}
            cd = getattr(s, '_cut_done', set()); trees = {t for t in trees if (s.sync(), t) not in cd}
            nav.objs = set(s.live_objs()) | trees; w0 = nav.mj['warp_events'][e[2]]; me = (s.pos()[2], s.pos()[3])
            if trees and not nav.path(me, (w0['x'], w0['y'])):
                log('  arbre a couper sur le chemin : COUPE'); s._cut_done = cd | {(s.sync(), t) for t in trees}; s.cut_trees()
        if e[0] == 'warp':
            nv = s.nav(); ws = nv.mj['warp_events']; w = ws[e[2]]; p = s.pos(); m0 = p[:2]
            if (nv.attr(w['x'], w['y']) & 0x1ff) == 0:      # warp pose sur du sol normal (Centre : 3 warps, un seul tapis) : on prend un warp voisin vers la meme carte sur un vrai tapis
                alt = [i for i, x in enumerate(ws) if x['dest_map'] == w['dest_map'] and (nv.attr(x['x'], x['y']) & 0x1ff) != 0]
                if alt: e = (e[0], e[1], alt[0]) + tuple(e[3:]); w = ws[alt[0]]
            if (p[2], p[3]) == (w['x'], w['y']):
                for d in ('DOWN', 'UP', 'DOWN', 'DOWN', 'LEFT', 'RIGHT', 'DOWN'):
                    s.e.run(14, KEYS[d]); s.e.run(70, 0)
                    if s.pos()[:2] != m0: return True
        return Auto.hop(s, e)
    def go(s, target, banned=(), tries=4):
        """Auto.go + verification : un trajet au Centre (heal) lance pendant go() peut nous deposer ailleurs que la cible."""
        fought = set()
        for _ in range(12):
            RF._NAV.clear(); RF._COMP.clear()      # cartes lues en direct pendant une visite precedente : les PNJ d'alors (battus depuis) barreraient a tort les couloirs
            r = Auto.go(s, target, banned, tries)
            if r and (isinstance(target, tuple) or s.sync() == target): return r
            if not r:
                # un dresseur barre peut-etre un couloir : on va l'affronter (vrai joueur), puis on reessaie
                cur = s.sync(); me = s.pos()
                if s.knows(15) and ('cut', cur) not in fought and any('CutTree' in o.get('script', '') for o in mj(cur)['object_events']):
                    fought.add(('cut', cur)); log('  pas de route : COUPE sur', cur); s.cut_trees(); continue
                tr = [o for o in mj(cur)['object_events'] if o.get('trainer_type', 'TRAINER_TYPE_NONE') != 'TRAINER_TYPE_NONE'
                      and (cur, o['x'], o['y']) not in fought and not (o.get('flag', '0') not in ('0', 0) and s.getflag(o['flag']))]
                if not tr: return r
                o = min(tr, key=lambda o: abs(o['x'] - me[2]) + abs(o['y'] - me[3]))
                fought.add((cur, o['x'], o['y'])); log('  dresseur sur le chemin : combat', cur, (o['x'], o['y']))
                s.talk_obj((o['x'], o['y']), 20); s.scene(maxn=900); continue
        return False
    def need_heal(s):
        p = s.party()
        if not p: return False
        tot = sum(q['hp'] for q in p) / max(sum(q['maxhp'] for q in p), 1)
        lead = next((q for q in p if q['hp'] > 0), None)
        return lead is None or tot < 0.5 or lead['hp'] < 0.35 * lead['maxhp'] or all(sum(q['pp']) < 6 for q in p if q['hp'] > 0)
    def centers(s):
        import glob
        cur = s.sync(); p = s.pos(); out = []
        for d in sorted(glob.glob('data/maps/*_PokemonCenter_1F')):
            nm = os.path.basename(d)
            if nm == cur: out.append((0, nm)); continue
            try: rt = route(cur, (p[2], p[3]), nm)
            except Exception: rt = None
            if rt: out.append((len(rt), nm))
        return sorted(out)
    def center_trip(s):
        """Va au Centre Pokemon le plus proche (en nombre de composantes de carte) et parle a l'infirmiere."""
        for dist, nm in s.centers()[:4]:
            log('  SOINS : trajet vers', nm, 'depuis', s.sync())
            if s.sync() != nm and not s.go(nm): continue
            nu = s.find_obj('_Nurse'); s.talk_at((nu[0], nu[1] + 2), 'UP', 50)
            s.e.run(60, 0)
            if not s.idle(): s.scene(maxn=200)
            log('  soigne :', [(q['level'], q['hp'], q['maxhp']) for q in s.party()])
            return True
        log('BLOCK aucun Centre Pokemon accessible'); return False
    def heal(s, force=False):
        if s._healing: return
        if not s.need_heal() and not (force and any(q['hp'] < 0.8 * q['maxhp'] for q in s.party())): return
        s._healing = True
        try: s.center_trip()
        finally: s._healing = False
    def heal_battle(s): pass
    def knows(s, move):
        return any(move in q['moves'] for q in s.party())
    def teach_hm(s, item, move, prefer=(1, 2, 3, 4, 5, 0)):
        """Vrai joueur : START > SAC > Objets Cles > CT/CS (BOITE CT) > la CS > UTILISER > Pokemon apte. Essaie les Pokemon dans l'ordre `prefer` jusqu'a ce que l'un apprenne `move`."""
        if s.knows(move): return True
        sb = s.e.u32(0x03005108)
        def pocket(off, n): return [i for i in (struct.unpack_from('<H', s.e.peek(sb + off + 4 * k, 4), 0)[0] for k in range(n)) if i]
        tm = pocket(0x464, 58); keys = pocket(0x3b8, 30)
        if item not in tm or 364 not in keys: log('  CS ou boite CT absente'); return False
        pos = len([i for i in tm if 339 <= i < item]); kpos = keys.index(364); n = len(s.party())
        for slot in prefer:
            if slot >= n: continue
            s.press('START', 4, 40)
            for _ in range(9):
                if s.e.peek(0x02037428, 1)[0] == 2: break
                s.press('DOWN', 4, 14)
            s.press('A', 4, 90)
            for _ in range(4): s.press('LEFT', 4, 30)
            s.press('RIGHT', 4, 30)                                   # pochette Objets Cles
            for _ in range(len(keys) + 2): s.press('UP', 4, 8)
            for _ in range(kpos): s.press('DOWN', 4, 14)              # TM CASE
            s.press('A', 4, 40); s.press('A', 4, 60)               # OUVRIR
            for _ in range(len(tm) + 2): s.press('UP', 4, 8)
            for _ in range(pos): s.press('DOWN', 4, 14)
            s.press('A', 4, 50); s.press('A', 4, 90)               # UTILISER
            for _ in range(8):
                if s.e.peek(sym('gPartyMenu') + 9, 1)[0] == slot: break
                s.press('DOWN', 4, 14)
            s.press('A', 4, 80)
            for _ in range(30):
                nm = name_of(s.cb2())
                if 'Summary' in nm:      # oublier une attaque : la moins puissante
                    b = s._brain(); pm = b.party()
                    sl = s.e.peek(sym('gPartyMenu') + 9, 1)[0]
                    if sl < len(pm):
                        pw = [((b.move(m)['power'] or 0) if m else -1, i) for i, m in enumerate(pm[sl]['moves'])]
                        for _ in range(min(pw)[1]): s.press('DOWN', 4, 14)
                    s.press('A', 4, 60); s.press('A', 4, 60); break
                s.press('A', 4, 40)
                if s.idle(): break
            for _ in range(25):
                if s.idle(): break
                s.press('B', 4, 30)
            if s.knows(move): log('  CS apprise : %d par le slot %d' % (move, slot)); return True
        log('  CS non apprise', move); return False
    HMS = ((339, 15), (341, 57), (342, 70), (343, 148), (344, 249), (345, 127), (340, 19), (346, 291))
    def learn_hms(s):
        """Apprend toutes les CS du sac qu'aucun membre de l'equipe ne connait encore."""
        for item, mv in s.HMS:
            try:
                if item == 341 and s.has_tm(341) and not s.knows(57): s.get_surfer()
                s.teach_hm(item, mv) if s.has_tm(item) else None
            except Exception as e: log('  CS erreur', item, e)
    SURFERS = (108,)       # especes capturables a pied (Kanto) qui peuvent apprendre Surf : Excelangue (Route 11)
    def pc_deposit(s, slot=5):
        """Centre le plus proche > PC > DEPOSER POKEMON > la case `slot` > BOITE1 : libere une place dans l'equipe."""
        if len(s.party()) < 2: return False
        for dist, nm in s.centers()[:3]:
            if s.sync() != nm and not s.go(nm): continue
            n = s.nav(); pc = [(x, y) for y in range(n.h) for x in range(n.w) if (n.attr(x, y) & 0xff) == 0x83]
            if not pc: continue
            x, y = pc[0]; s.talk_at((x, y + 1), 'UP', 40); s.press('A', 4, 40)
            s.press('DOWN', 4, 14); s.press('A', 4, 60)
            for _ in range(slot): s.press('DOWN', 4, 14)
            s.press('A', 4, 40); s.press('A', 4, 40); s.press('A', 4, 60)
            for _ in range(6): s.press('B', 4, 40)
            log('  PC : depose la case', slot, '->', len(s.party()), 'membres')
            return True
        return False
    def get_surfer(s, mapname='Route11', maxsteps=300):
        """Surf demande, mais personne ne peut l'apprendre : on libere une place et on capture un Pokemon compatible."""
        if not s.has_tm(341) or s.knows(57): return True
        if any(q['species'] in s.SURFERS for q in s.party()): return True
        if len(s.party()) >= 6 and not s.pc_deposit(5): return False
        if s.balls() < 3: s.shop_balls()
        s.catch_only = set(s.SURFERS); log('CAPTURE D UN POKEMON COMPATIBLE SURF', mapname)
        try: ok = s.train(mapname, 99, maxsteps, until=lambda p: any(q['species'] in s.SURFERS for q in p))
        finally: s.catch_only = None
        return ok
    def has_tm(s, item):
        sb = s.e.u32(0x03005108)
        return item in [struct.unpack_from('<H', s.e.peek(sb + 0x464 + 4 * k, 4), 0)[0] for k in range(58)]
    def shop_balls(s, want=12):
        """Achete des POKE BALLS au Supermarche le plus proche (1er article de la liste ; on baisse la quantite si l'argent manque)."""
        import glob
        cur = s.sync(); p = s.pos(); out = []
        for d in glob.glob('data/maps/*_Mart'):
            nm = os.path.basename(d)
            try: rt = [] if nm == cur else route(cur, (p[2], p[3]), nm)
            except Exception: rt = None
            if rt is not None: out.append((len(rt), nm))
        for _, nm in sorted(out)[:3]:
            if s.sync() != nm and not s.go(nm): continue
            ck = s.find_obj('_Clerk')
            if not ck: continue
            for qty in (want, 8, 5, 3, 2, 1):
                n0 = s.balls()
                s.talk_at((ck[0], ck[1] + 2), 'UP', 50); s.e.run(60, 0)
                for k in ['A', 'A'] + ['UP'] * (qty - 1) + ['A', 'A']: s.press(k, 4, 50)
                for _ in range(5): s.press('B', 4, 40)
                if s.balls() > n0: log('  ACHAT : balls', n0, '->', s.balls()); return True
            log('BLOCK pas assez d argent pour des balls'); return False
        return False
    @classmethod
    def resume(cls, name, rom='/tmp/gx/dbg2.gba'):
        t = Auto.resume.__func__(cls, name, rom)
        t.e.cmd('poke8 %x 0' % 0x030075e8)      # gTopazeGod = 0
        t._b = real.Brain(t.e)
        orig = t.e.run; busy = [False]
        def run(n, keys=0, _o=orig, _t=t):
            """Toute avance d'emulation : si une evolution est en cours (combat gagne), on la mene au bout avec A (B l'annulerait)."""
            if not busy[0]:
                busy[0] = True
                try:
                    for _ in range(80):
                        if 'Evolution' not in name_of(_t.cb2()): break
                        _o(4, KEYS['A']); _o(40, 0)
                finally: busy[0] = False
            return _o(n, keys)
        t.e.run = run
        return t
    def grass(s):
        n = s.nav(); g = [(x, y) for y in range(n.h) for x in range(n.w) if (n.attr(x, y) & 0xff) == 2 and not n.blocked(x, y)]
        if g: return g
        return [(x, y) for y in range(n.h) for x in range(n.w) if (n.attr(x, y) & 0xff) == 0 and not n.blocked(x, y)]      # grotte : le sol libre declenche les rencontres
    def party(s):
        p = s._brain().party()
        if not hasattr(s, 'owned'): s.owned = set()
        s.owned |= {q['species'] for q in p}
        return p
    def train(s, mapname, lvl, maxsteps=400, until=None):
        """Combat dans l'herbe de `mapname` jusqu'a ce que la tete d'equipe atteigne `lvl`."""
        for it in range(maxsteps):
            s.heal()
            if s.sync() != mapname and not s.go(mapname): log('BLOCK carte d entrainement inaccessible', mapname); return False
            p = s.party()
            if until is not None:
                if until(p): return True
            elif p and max(q['level'] for q in p) >= lvl: return True
            s.xp_swap = True
            top = max(q['level'] for q in p)
            weak = [q for q in p if q['hp'] * 2 > q['maxhp'] and q['level'] + 3 <= top and not q['egg']]
            if weak and p[0]['level'] >= top - 2 and len(p) > 1:
                w = min(weak, key=lambda q: q['level'])
                if s.idle(): s.lead_swap(w['i']); log('  tete d equipe -> niveau', w['level'])
            gr = s.grass(); me = s.pos()[2:]
            if not gr: log('pas d\'herbe', mapname); return False
            tgt = min(gr, key=lambda c: abs(c[0] - me[0]) + abs(c[1] - me[1]))
            s.walk_fight(tgt, 6)
            for k in range(30):
                s.press('LEFT' if (k // 2) % 2 == 0 else 'RIGHT', 2, 2)
                if s.inbattle(): break
            if s.inbattle():
                s._throws = 0; s.scene(maxn=600); s.party(); s.save('real_cur'); log('combat fini', [(q['level'], q['hp'], q['maxhp']) for q in s.party()])
        return False

if __name__ == '__main__':
    t = Real.resume(sys.argv[1] if len(sys.argv) > 1 else 'opan')
    print(t.train('Route22', 10))
