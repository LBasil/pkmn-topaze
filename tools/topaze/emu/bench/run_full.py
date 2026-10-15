#!/usr/bin/env python3
"""Autopilote de la RUN COMPLETE (nouvelle partie -> generique) en emulateur (mGBA headless).

Prerequis : /tmp/gx (harness avec commandes ss/ls, drive.py, tz.py, spin.py, dbg2.gba via mkdbg2.py).
ROM de debug utilisee SANS teleport utile : on demarre dans la chambre du joueur (nouvelle partie), mode DIEU actif (le joueur
ne perd jamais, tue en un coup), mais combats et scenes normaux. Aucun drapeau n'est pre-positionne : les verrous doivent se lever
naturellement. Chaque etape sauvegarde un etat (/tmp/gx/st/<etape>.ss) pour pouvoir reprendre : `run_full.py <etape>` repart de la
sauvegarde de l'etape precedente.

Navigation : graphe des cartes (warps + connexions), BFS statique ; les obstacles dynamiques (dresseurs, policiers) sont geres
par walk_fight / scene. Tout blocage est journalise dans /tmp/gx/run.log (`BLOCK ...`).
"""
import sys, os, json, collections, time
sys.path.insert(0, '/tmp/gx')
from tz import *
import tz

ST = '/tmp/gx/st'; os.makedirs(ST, exist_ok=True); os.makedirs('/tmp/gx/out', exist_ok=True)
LOG = open('/tmp/gx/run.log', 'a')
def log(*a):
    s = ' '.join(str(x) for x in a); print(s, flush=True); LOG.write(s + '\n'); LOG.flush()

_MJ = {}
def mj(name):
    if name not in _MJ: _MJ[name] = json.load(open('data/maps/%s/map.json' % name))
    return _MJ[name]
def mname(dm):
    return tz._NAMES[dm.replace('MAP_', '').replace('_', '').lower()]
# --- graphe des composantes (carte, zone atteignable) : warps + connexions ---------------------------------------
_NAV = {}; _COMP = {}
GATE_GFX = ('SNORLAX', 'PUSHABLE_BOULDER', 'BREAKABLE_ROCK', 'STRENGTH', 'ROCK_SMASH')
def open_gate(g):
    """Retire un type d'obstacle du graphe statique (ex. apres la Flute : Ronflex se reveille) et vide les caches."""
    global GATE_GFX
    GATE_GFX = tuple(x for x in GATE_GFX if x != g); _NAV.clear(); _COMP.clear()
def nav_of(name):
    if name not in _NAV:
        n = R.Nav(name)
        n.objs = {(o['x'], o['y']) for o in n.mj['object_events'] if any(g in o['graphics_id'] for g in GATE_GFX)}
        _NAV[name] = n
    return _NAV[name]
def comps(name):
    """etiquette de composante de chaque case marchable (les cases de warp ne se traversent pas)."""
    if name in _COMP: return _COMP[name]
    nav = nav_of(name); lab = {}; k = 0
    for y in range(nav.h):
        for x in range(nav.w):
            if (x, y) in lab or nav.blocked(x, y) or (x, y) in nav.warps: continue
            q = collections.deque([(x, y)]); lab[(x, y)] = k
            while q:
                c = q.popleft()
                for dx, dy in ((0, 1), (0, -1), (1, 0), (-1, 0)):
                    m = (c[0] + dx, c[1] + dy)
                    if m in lab or not (0 <= m[0] < nav.w and 0 <= m[1] < nav.h) or nav.blocked(*m) or m in nav.warps or not nav.step_ok(c, m): continue
                    lab[m] = k; q.append(m)
            k += 1
    _COMP[name] = lab; return lab
def comp_of(name, cell):
    """composante d'une case (case de warp/porte : composante d'un voisin libre)."""
    lab = comps(name)
    if cell in lab: return lab[cell]
    for dx, dy in ((0, 1), (0, -1), (1, 0), (-1, 0)):
        m = (cell[0] + dx, cell[1] + dy)
        if m in lab: return lab[m]
    return None
def comps_of(name, cell):
    """toutes les composantes touchees par une case (une case de warp peut en relier plusieurs)."""
    lab = comps(name)
    if cell in lab: return {lab[cell]}
    return {lab[m] for m in ((cell[0], cell[1] + 1), (cell[0], cell[1] - 1), (cell[0] + 1, cell[1]), (cell[0] - 1, cell[1])) if m in lab}
def exits(name, comp):
    """sorties d'une composante : ('warp', dest, idx, case) / ('conn', dest, conn, case_depart, case_arrivee)."""
    nav = nav_of(name); lab = comps(name); out = []
    for i, w in enumerate(nav.mj['warp_events']):
        d = w['dest_map']
        if d in ('MAP_DYNAMIC', 'DYNAMIC'): continue
        c = (w['x'], w['y'])
        if comp not in comps_of(name, c): continue
        try: dn = mname(d)
        except KeyError: continue
        dw = nav_of(dn).mj['warp_events']; di = int(w['dest_warp_id']) if str(w['dest_warp_id']).isdigit() else -1
        if not (0 <= di < len(dw)): continue
        out.append(('warp', dn, i, c, (dw[di]['x'], dw[di]['y'])))
    for cn in nav.mj.get('connections') or []:
        d = cn['direction']
        if d not in ('up', 'down', 'left', 'right'): continue
        try: dn = mname(cn['map'])
        except KeyError: continue
        dnav = nav_of(dn); off = cn['offset']
        if d == 'up': cells = [((x, 0), (x - off, dnav.h - 1)) for x in range(nav.w)]
        elif d == 'down': cells = [((x, nav.h - 1), (x - off, 0)) for x in range(nav.w)]
        elif d == 'left': cells = [((0, y), (dnav.w - 1, y - off)) for y in range(nav.h)]
        else: cells = [((nav.w - 1, y), (0, y - off)) for y in range(nav.h)]
        for a, b in cells:
            if lab.get(a) == comp and 0 <= b[0] < dnav.w and 0 <= b[1] < dnav.h and not dnav.blocked(*b):
                out.append(('conn', dn, cn, a, b)); break
    return out
def route(src_map, src_cell, dst, banned=()):
    """Chemin le plus court de composante en composante jusqu'a la carte dst : liste de sorties (voir exits)."""
    c0s = comps_of(src_map, src_cell)
    if not c0s: return None
    prev = {}; q = collections.deque(); end = None
    for c0 in sorted(c0s): prev[(src_map, c0)] = None; q.append((src_map, c0))
    while q:
        n = q.popleft()
        if n[0] == dst: end = n; break
        for e in exits(n[0], n[1]):
            if (n[0], e[1], e[3]) in banned or e[1] in banned: continue
            for nc in comps_of(e[1], e[4]):
                nn = (e[1], nc)
                if nn in prev: continue
                prev[nn] = (n, e); q.append(nn)
    if end is None: return None
    out = []; c = end
    while prev[c]: pn, e = prev[c]; out.append(e); c = pn
    return out[::-1]

class Auto(T):
    @classmethod
    def boot(cls, mapname='PalletTown_PlayersHouse_2F', x=6, y=6):
        t = cls(mapname, x, y, party=False, nocombat=False, god=True)
        t.e.cmd('unpin'); return t
    @classmethod
    def resume(cls, name, rom='/tmp/gx/dbg2.gba'):
        t = cls.__new__(cls); t.e = Emu(rom); t.shots = []
        r = t.e.cmd('ls %s/%s.ss' % (ST, name)); assert r == 'ok', 'etat introuvable ' + name
        t.e.run(10, 0); t.sync(); return t
    def nav(s, name=None):
        """Nav de la carte courante avec la grille VIVANTE (RAM) et les objets vivants."""
        n = R.Nav(name or s.sync()); s.live_grid(n); return n
    def save(s, name):
        r = s.e.cmd('ss %s/%s.ss' % (ST, name)); log('SAVE', name, r, s.pos(), s.sync())
    def st(s):
        return (s.sync(), s.pos()[2:])
    # --- passage de connexion (bord de carte)
    def edge_cross(s, c, goal):
        """Traverse la connexion c en partant de la case de bord `goal` (accessible)."""
        d = c['direction']; name = s.sync(); nav = s.nav(); p = s.pos(); cur = (p[2], p[3])
        key = {'up': 'UP', 'down': 'DOWN', 'left': 'LEFT', 'right': 'RIGHT'}[d]
        nav.objs = s.live_objs()
        cells = [goal]
        # cases voisines du meme bord au cas ou la premiere est occupee
        for k in (1, -1, 2, -2):
            g2 = (goal[0] + (k if d in ('up', 'down') else 0), goal[1] + (k if d in ('left', 'right') else 0))
            if 0 <= g2[0] < nav.w and 0 <= g2[1] < nav.h and not nav.blocked(*g2): cells.append(g2)
        for g in cells:
            if cur != g and not nav.path(cur, g): continue
            s.walk_fight(g, 10)
            if s.pos()[:2] != p[:2]: return True
            s.e.run(24, KEYS[key]); s.e.run(40, 0)
            if s.pos()[:2] != p[:2]: return True
            p = s.pos(); cur = (p[2], p[3])
        return False
    def hop(s, e):
        """Franchit la sortie e (voir exits). True si la carte a change."""
        k, dest = e[0], e[1]; cur = s.sync(); m0 = s.pos()[:2]; nav = s.nav()
        if k == 'warp':
            nav.objs = s.live_objs(); w = nav.mj['warp_events'][e[2]]; s._warp_try(nav, w, 12, None)
        else:
            s.edge_cross(e[2], e[3])
        return s.pos()[:2] != m0
    def clear_blocker(s, goal):
        """Si un objet vivant (PNJ, dresseur) barre le chemin vers `goal`, va lui parler (combat/dialogue). True si une action a eu lieu."""
        nav = s.nav(); live = s.live_objs(); p = s.pos(); cur = (p[2], p[3])
        nav.objs = set(); path = nav.path(cur, goal)
        if not path:     # but bloque (porte a collision) : on vise une case voisine accessible
            for dx, dy in ((0, 1), (0, -1), (1, 0), (-1, 0)):
                a = (goal[0] + dx, goal[1] + dy)
                if not nav.blocked(*a):
                    path = nav.path(cur, a)
                    if path: break
        if not path: return False
        for c in path:
            if c in live:
                log('  deblocage : objet en', c, 'sur le chemin', cur, '->', goal)
                s.save('blocker_%s' % s.sync())
                return s.talk_obj(c, 30)
        return False
    def go(s, target, banned=(), tries=4):
        """Va jusqu'a la carte `target` par le graphe de composantes. Renvoie True si arrive."""
        banned = set(banned); tried = collections.Counter()
        if 'SNORLAX' in GATE_GFX and s.getflag('FLAG_GOT_POKE_FLUTE'): open_gate('SNORLAX')
        if not R.SURF and s.getflag('FLAG_GOT_HM03') and s.getflag('FLAG_BADGE05_GET'): R.SURF = True; _NAV.clear(); _COMP.clear()
        for _ in range(tries * 40):
            cur = s.sync()
            if cur == target: return True
            n_live = s.nav(); n_live.objs = {(o['x'], o['y']) for o in n_live.mj['object_events'] if any(g in o['graphics_id'] for g in GATE_GFX)}
            _NAV[cur] = n_live; _COMP.pop(cur, None)        # la carte courante est lue en direct (barrieres ouvertes par des scripts...)
            p = s.pos(); rt = route(cur, (p[2], p[3]), target, banned)
            if not rt and s.tele_exit(): continue
            if not rt: log('BLOCK pas de route', cur, (p[2], p[3]), '->', target); s.save('noroute_' + cur); return False
            e = rt[0]
            if not s.hop(e):
                if tried[(cur, e[3])] < 5:
                    tried[(cur, e[3])] += 1
                    if not s.idle(): s.scene(maxn=600)          # une scene a pu se declencher en route : on la laisse finir puis on reessaie
                    if s.clear_blocker(e[3]) or s.sync() != cur or tried[(cur, e[3])] <= 2: continue
                log('BLOCK hop echoue', cur, e[:2], e[3], s.pos()); banned.add((cur, e[1], e[3]))
                s.shot('block_%s_%s' % (cur, e[1])); s.save('hopfail_' + cur)
            else: log('  ', cur, '->', s.sync(), s.pos()[2:])
        return s.sync() == target
    def pause_to_free(s, maxn=300, shot=None):
        return s.scene(maxn=maxn, shot=shot)
    def talk_at(s, tile, face, n=14, shot=None):
        """Va sur `tile` (case voisine du PNJ), se tourne vers `face`, parle, laisse la scene se terminer."""
        r = s.walk_fight(tile, 10)
        s.face(face); s.mash(n, shot); return s.scene(120)
    def tele_plan(s, start, goal):
        """Chemin (liste de directions) dans la carte courante en comptant les teleporteurs internes (warps vers la meme carte)."""
        nav = s.nav(); s.live_grid(nav); nav.objs = s.live_objs(); me = nav.mj['id']; ws = nav.warps; evs = nav.mj['warp_events']
        def tele(c):
            w = ws.get(c)
            if w and w['dest_map'] == me and str(w['dest_warp_id']).isdigit():
                d = evs[int(w['dest_warp_id'])]; return (d['x'], d['y'])
        prev = {start: None}; q = collections.deque([start])
        while q:
            c = q.popleft()
            if c == goal: break
            for d, (dx, dy) in (('UP', (0, -1)), ('DOWN', (0, 1)), ('LEFT', (-1, 0)), ('RIGHT', (1, 0))):
                n = (c[0] + dx, c[1] + dy)
                if nav.blocked(*n) or not nav.step_ok(c, n): continue
                if n in ws:
                    t = tele(n)
                    if t is None and n != goal: continue
                    if t is not None: n = t
                if n in prev: continue
                prev[n] = (c, d); q.append(n)
        if goal not in prev: return None
        out = []; c = goal
        while prev[c]: out.append(prev[c][1]); c = prev[c][0]
        return out[::-1]
    def tele_exit(s):
        """Sort de la carte courante par une de ses sorties en passant par les teleporteurs internes. True si la carte a change."""
        m0 = s.pos()[:2]; nav = s.nav(); me = nav.mj['id']; p = s.pos(); cur = (p[2], p[3]); cands = []
        for w in nav.mj['warp_events']:
            if w['dest_map'] == me or w['dest_map'] in ('MAP_DYNAMIC', 'DYNAMIC'): continue
            pl = s.tele_plan(cur, (w['x'], w['y']))
            if pl is not None: cands.append((len(pl), (w['x'], w['y'])))
        for _, c in sorted(cands)[:4]:
            p = s.pos(); cur = (p[2], p[3])
            if s.tele_plan(cur, c) is None: continue
            s.walk_tele(c); s.e.run(60, 0)
            for d in ('DOWN', 'LEFT', 'RIGHT', 'UP'):      # case de sortie atteinte : on pousse vers le bord pour franchir la porte
                if s.pos()[:2] != m0: return True
                s.hold(d, 16); s.e.run(60, 0)
            if s.pos()[:2] != m0: return True
        return False
    def walk_tele(s, goal, tries=300):
        """Marche pas a pas vers goal en utilisant les teleporteurs internes (arene d'Hematown) ; replanifie a chaque pas."""
        for _ in range(tries):
            if not s.idle(): s.scene(maxn=300)
            p = s.pos(); cur = (p[2], p[3])
            if cur == goal: return True
            plan = s.tele_plan(cur, goal)
            if not plan: return False
            s.hold(plan[0], 16); s.e.run(24, 0)
        p = s.pos(); return (p[2], p[3]) == goal
    def approach(s, pos, rounds=10):
        """Se place sur une case voisine accessible de `pos` (objet) et se tourne vers lui. True si en place."""
        name = s.sync(); nav = s.nav(); nav.objs = s.live_objs() - {tuple(pos)}
        p = s.pos(); cur = (p[2], p[3]); best = None
        for d, (dx, dy) in (('DOWN', (0, -1)), ('UP', (0, 1)), ('RIGHT', (-1, 0)), ('LEFT', (1, 0))):   # d = direction a viser depuis la case
            c = (pos[0] + dx, pos[1] + dy)
            if nav.blocked(*c) or c in nav.warps: continue
            path = nav.path(cur, c) if c != cur else [c]
            if path and (best is None or len(path) < best[0]): best = (len(path), c, d)
        if not best:     # pas de chemin a pied : teleporteurs internes ?
            for d, (dx, dy) in (('DOWN', (0, -1)), ('UP', (0, 1)), ('RIGHT', (-1, 0)), ('LEFT', (1, 0))):
                c = (pos[0] + dx, pos[1] + dy)
                if nav.blocked(*c) or c in nav.warps: continue
                pl = s.tele_plan(cur, c) if c != cur else []
                if pl is not None and (best is None or len(pl) < best[0]): best = (len(pl), c, d)
            if not best or not s.walk_tele(best[1]): return False
            s.face(best[2]); s._facing = {'UP': (0, -1), 'DOWN': (0, 1), 'LEFT': (-1, 0), 'RIGHT': (1, 0)}[best[2]]; return True
        if s.walk_fight(best[1], rounds) not in (True,): return False
        s.face(best[2]); s._facing = {'UP': (0, -1), 'DOWN': (0, 1), 'LEFT': (-1, 0), 'RIGHT': (1, 0)}[best[2]]; return True
    def talk_obj(s, pos, n=14, shot=None):
        pos = tuple(pos)
        for _ in range(5):       # un PNJ qui se promene a pu bouger : on verifie qu'il est bien en face avant de parler
            if not s.approach(pos): return False
            p = s.pos(); fx, fy = s._facing; front = (p[2] + fx, p[3] + fy)
            if front in s.live_objs() or front == pos and not s.live_objs(): break
            near = [o for o in s.live_objs() if abs(o[0] - pos[0]) + abs(o[1] - pos[1]) <= 3]
            if near: pos = min(near, key=lambda o: abs(o[0] - pos[0]) + abs(o[1] - pos[1]))
        s.mash(n, shot); s.scene(900); return True
    def find_obj(s, script_pat):
        """Position (carte JSON) de l'objet dont le script contient script_pat sur la carte courante."""
        for o in mj(s.sync())['object_events']:
            if script_pat in o['script']: return (o['x'], o['y'])
    def talk_script(s, script_pat, n=14, shot=None):
        pos = s.find_obj(script_pat); assert pos, 'objet introuvable ' + script_pat
        near = [o for o in s.live_objs() if abs(o[0] - pos[0]) + abs(o[1] - pos[1]) <= 4]    # PNJ qui se deplace : position reelle
        if near: pos = min(near, key=lambda o: abs(o[0] - pos[0]) + abs(o[1] - pos[1]))
        return s.talk_obj(pos, n, shot)
    def talk_wanderers(s, flags, area, rounds=8):
        """Parle aux objets mobiles de la zone `area` (x0,y0,x1,y1) jusqu'a ce que tous les `flags` soient poses."""
        x0, y0, x1, y1 = area
        for _ in range(rounds):
            if all(s.getflag(f) for f in flags): return True
            objs = sorted(o for o in s.live_objs() if x0 <= o[0] <= x1 and y0 <= o[1] <= y1)
            p = s.pos()
            objs.sort(key=lambda o: abs(o[0] - p[2]) + abs(o[1] - p[3]))
            for o in objs:
                if s.talk_obj(o, 8) and all(s.getflag(f) for f in flags): return True
        return all(s.getflag(f) for f in flags)
    def cut_trees(s):
        """Coupe (parle a) tous les arbres de la carte courante atteignables ; renvoie le nombre de passages tentes."""
        n = 0
        for o in mj(s.sync())['object_events']:
            if 'CutTree' not in o['script'] or (o['x'], o['y']) not in s.live_objs(): continue
            if s.talk_obj((o['x'], o['y']), 6): n += 1
        return n
    def quiz_signs(s, cells, n=30):
        """Arene a quiz : se place devant chaque case-panneau (BG event) et repond (A = OUI) ; une mauvaise reponse declenche le dresseur."""
        for c in cells:
            if not s.approach(c): log('QUIZ inaccessible', c); continue
            s._facing = (0, -1); s.face('UP'); s.mash(n); s.scene(900)
    def sail(s, downs):
        """Parle au marin du port courant et choisit la destination (nombre de DOWN dans le menu)."""
        pos = s.find_obj('Sailor'); assert pos and s.approach(pos), 'marin inaccessible'
        s.press('A', 4, 120)
        for _ in range(downs): s.press('DOWN', 4, 20)
        s.press('A', 4, 60); s.scene(900)
    def report(s, *items):
        out = []
        for i in items:
            if i.startswith('VAR_'): out.append('%s=%s' % (i, s.getvar(i)))
            else: out.append('%s=%s' % (i, s.getflag(i)))
        log('STATE', s.st(), ' '.join(out))

# ----------------------------------------------------------------------------------------------------------------
def stage_opening_ranch(t):
    """Chambre -> rez-de-chaussee -> Grenalux -> sortie nord : scene du rival, du ranch, choix du partenaire, combat, pendentif."""
    assert t.go('PalletTown'), 'sortie maison'
    r = t.walk_fight((22, 3), 8, 'op_ranch')
    t.scene(maxn=400)
    t.report('FLAG_GRENALUX_ONYBRIS_STRIKE', 'VAR_GRENALUX_OPENING')
    assert t.getflag('FLAG_GRENALUX_ONYBRIS_STRIKE'), 'attaque non declenchee'

def stage_school(t):
    assert t.go('PalletTown_School'), 'ecole inaccessible'
    t.scene(maxn=500, shot='sch'); t.report('VAR_GRENALUX_OPENING')
    assert t.getvar('VAR_GRENALUX_OPENING') == 3, 'ecole : VAR_GRENALUX_OPENING != 3'

def stage_lab(t):
    assert t.go('PalletTown_ProfessorOaksLab'), 'labo inaccessible'
    t.scene(maxn=500, shot='lab'); t.report('VAR_GRENALUX_OPENING', 'FLAG_SYS_POKEDEX_GET')
    assert t.getvar('VAR_GRENALUX_OPENING') == 4, 'labo : OPENING != 4'

def stage_route1_quest(t):
    assert t.go('Route1'), 'Route 1 inaccessible'
    fl = ['FLAG_ROUTE1_TALKED_DODUO', 'FLAG_ROUTE1_TALKED_NIDORANM', 'FLAG_ROUTE1_TALKED_NIDORANF']
    ok = t.talk_wanderers(fl, (5, 20, 22, 40), rounds=12)
    t.report(*fl, 'FLAG_ONYBRIS_ANIMALS_FOUND')
    assert ok, 'quete du ranch : animaux non tous trouves'
    assert t.go('PalletTown_Ranch'), 'ranch inaccessible'
    t.talk_script('Hand1', 20); t.report('FLAG_ONYBRIS_ANIMALS_FOUND', 'FLAG_GRENALUX_GEM_REWARD')
    assert t.getflag('FLAG_GRENALUX_GEM_REWARD'), 'recompense du ranch non donnee'

def stage_opanihrum(t):
    assert t.go('ViridianCity'), 'Opanihrum inaccessible'
    t.talk_script('TutorialOldMan', 30, 'opan'); t.report('FLAG_VIRIDIAN_TUTORIAL_DONE')

def badge_gym(t, gymmap, leader_pat, badge, n=40):
    assert t.go(gymmap), gymmap + ' inaccessible'
    for _ in range(6):
        t.cut_trees()
        t.talk_script(leader_pat, n, 'gym_' + gymmap)
        if t.getflag(badge): break
    t.report(badge)
    assert t.getflag(badge), 'badge non obtenu ' + badge

def stage_gym1(t): badge_gym(t, 'PewterCity_Gym', 'Brock', 'FLAG_BADGE01_GET')

def stage_gym2(t): badge_gym(t, 'CeruleanCity_Gym', 'Misty', 'FLAG_BADGE02_GET')

def stage_cottage(t):
    assert t.go('Route25_SeaCottage'), 'chaumiere inaccessible'
    t.scene(maxn=900, shot='cottage'); t.report('FLAG_GOT_SS_TICKET')
    assert t.getflag('FLAG_GOT_SS_TICKET'), 'ticket non obtenu'

def stage_ssanne(t):
    assert t.go('SSAnne_CaptainsOffice'), 'bureau du capitaine inaccessible'
    t.scene(maxn=900, shot='ssanne'); t.report('FLAG_GOT_HM01')
    for _ in range(4):
        if t.getflag('FLAG_GOT_HM01'): break
        t.talk_script('Captain', 30, 'ssanne_cap')
    t.report('FLAG_GOT_HM01')
    assert t.getflag('FLAG_GOT_HM01'), 'CUT non obtenue'

def trash_puzzle(t, maxtry=80):
    """Arene d'Apatia : puzzle des poubelles (2 interrupteurs, le 2e voisin du 1er)."""
    cans = {}
    for b in mj('VermilionCity_Gym')['bg_events']:
        if 'TrashCan' in b['script']: cans[int(b['script'].split('TrashCan')[1])] = (b['x'], b['y'])
    def nbrs(k):
        r, c = divmod(k - 1, 5); out = []
        if c > 0: out.append(k - 1)
        if c < 4: out.append(k + 1)
        if r > 0: out.append(k - 5)
        if r < 2: out.append(k + 5)
        return out
    def poke(k):
        ok = t.approach(cans[k])
        if ok: t.press('A', 4, 40); t.scene(120)      # un seul A : d'autres A rouvriraient la poubelle (et reinitialiseraient les verrous)
        log('  can', k, cans[k], 'ok' if ok else 'ECHEC', t.pos()[2:], 'T1=', t.getflag('FLAG_TEMP_1'))
    first = None; todo = list(range(1, 16)); i = 0
    for _ in range(maxtry):
        if t.getflag('FLAG_FOUND_BOTH_VERMILION_GYM_SWITCHES'): break
        if first is None:
            k = todo[i % 15]; i += 1; poke(k)
            if t.getflag('FLAG_TEMP_1'): first = k; cand = nbrs(k)
        else:
            if not cand: first = None; continue
            k = cand.pop(0); poke(k)
            if not t.getflag('FLAG_TEMP_1') and not t.getflag('FLAG_FOUND_BOTH_VERMILION_GYM_SWITCHES'): first = None
    t.report('FLAG_FOUND_BOTH_VERMILION_GYM_SWITCHES')
    assert t.getflag('FLAG_FOUND_BOTH_VERMILION_GYM_SWITCHES'), 'puzzle des poubelles non resolu'

def stage_gym3(t):
    assert t.go('VermilionCity_Gym'), 'arene d Apatia inaccessible'
    trash_puzzle(t)
    badge_gym(t, 'VermilionCity_Gym', 'LtSurge', 'FLAG_BADGE03_GET')

def stage_tower(t):
    assert t.go('PokemonTower_7F', banned=('SaffronCity', 'Hematown')), 'Tour Spinelle 7F inaccessible'
    t.walk_fight((11, 8), 10); t.walk_fight((11, 6), 10); t.scene(maxn=900, shot='tower')
    if not t.getflag('FLAG_RESCUED_MR_FUJI'): t.talk_obj((11, 4), 10)
    t.report('FLAG_RESCUED_MR_FUJI')

BAN = ('SaffronCity', 'Hematown')

def lift(t, target):
    """Ascenseur du repaire (on est dans RocketHideout_Elevator) : target 0=B1F 1=B2F 2=B4F, puis sortie par le tapis."""
    assert t.approach((0, 2)); t.press('A', 4, 60)
    cur = {3: 0, 2: 1, 0: 2}.get(t.getvar('VAR_ELEVATOR_FLOOR'), 0)
    for _ in range(abs(target - cur)): t.press('DOWN' if target > cur else 'UP')
    t.press('A'); t.scene(300)
    t.walk_fight((2, 4), 6); t.hold('DOWN', 24); t.hold('DOWN', 24); t.e.run(80, 0)

def stage_quartz(t):
    assert t.go('CeladonCity_GameCorner', banned=BAN), 'Game Corner inaccessible'
    for _ in range(3):
        if t.getflag('FLAG_OPENED_ROCKET_HIDEOUT'): break
        if t.live_objs() and (11, 2) in t.live_objs(): t.talk_obj((11, 2), 10)
        if t.approach((11, 1)): t.mash(6); t.scene(300)
    t.report('FLAG_OPENED_ROCKET_HIDEOUT')
    assert t.getflag('FLAG_OPENED_ROCKET_HIDEOUT'), 'poster du Game Corner sans effet'
    assert t.go('RocketHideout_B4F', banned=BAN), 'repaire B4F inaccessible'
    for _ in range(3):   # cle de l'ascenseur : grunt1 puis la balle
        t.talk_script('Grunt1', 20, 'grunt1')
        t.talk_script('LiftKey', 8)
        if t.getflag('FLAG_CAN_USE_ROCKET_HIDEOUT_LIFT'): break
    assert t.getflag('FLAG_CAN_USE_ROCKET_HIDEOUT_LIFT'), 'cle de l ascenseur introuvable'
    assert t.go('RocketHideout_Elevator', banned=BAN), 'ascenseur inaccessible'
    lift(t, 2)
    t.report('FLAG_CAN_USE_ROCKET_HIDEOUT_LIFT'); log('apres ascenseur', t.sync(), t.pos())
    for g in ('Grunt2', 'Grunt3'): t.talk_script(g, 20, g)   # les deux gardes de la porte (levent la barriere)
    for _ in range(4):
        t.talk_script('Giovanni', 40, 'vesper')
        if t.getflag('FLAG_HIDE_CELADON_ROCKETS'): break
    t.report('FLAG_HIDE_CELADON_ROCKETS')
    t.talk_script('SilphScope', 8); t.report('FLAG_GOT_POKE_FLUTE')
    assert t.go('RocketHideout_Elevator', banned=BAN), 'ascenseur (retour) inaccessible'
    lift(t, 0); t.talk_script('Grunt5', 20, 'grunt5')   # garde de la barriere de B1F
    assert t.go('CeladonCity_GameCorner', banned=BAN), 'retour Game Corner impossible'
    for _ in range(3):
        t.talk_script('VesperDuel', 40, 'duel')
        if t.getflag('FLAG_QUARTZ_DUEL_DONE'): break
    t.report('FLAG_QUARTZ_DUEL_DONE', 'FLAG_QUARTZ_STONE_WON')

def stage_gym4(t): badge_gym(t, 'CeladonCity_Gym', 'Erika', 'FLAG_BADGE04_GET')

def stage_ameth(t):
    assert t.go('FuchsiaCity_WardensHouse', banned=BAN), 'maison du gardien inaccessible'
    if not t.getflag('FLAG_AMETHYST_RAID_DONE'):
        t.walk_fight((6, 8), 6); t.scene(900, shot='raid')
    t.report('FLAG_AMETHYST_RAID_STARTED', 'FLAG_AMETHYST_RAID_DONE')
    assert t.getflag('FLAG_AMETHYST_RAID_DONE'), 'raid de la maison du gardien non declenche'
    assert t.go('SafariZone_West', banned=BAN), 'Parc Safari ouest inaccessible'
    for _ in range(4):
        t.talk_script('OnybrisSelene', 40, 'selene')
        t.talk_script('ItemGoldTeeth', 8)
        if t.getflag('FLAG_HIDE_SAFARI_ZONE_WEST_GOLD_TEETH'): break
    t.report('FLAG_HIDE_SAFARI_ZONE_WEST_GOLD_TEETH')
    assert t.go('SafariZone_SecretHouse', banned=BAN), 'maison secrete du Safari inaccessible'
    t.talk_script('Attendant', 12); t.report('FLAG_GOT_HM03')
    if t.getvar('VAR_MAP_SCENE_FUCHSIA_CITY_SAFARI_ZONE_ENTRANCE') == 0:      # ROM sans le correctif de sortie du Parc occupe : on le simule
        t.var('VAR_MAP_SCENE_FUCHSIA_CITY_SAFARI_ZONE_ENTRANCE', 1)
    assert t.go('FuchsiaCity_WardensHouse', banned=BAN), 'retour chez le gardien impossible'
    t.talk_script('Warden', 30, 'warden'); t.report('FLAG_GOT_HM04', 'FLAG_AMETHYST_STONE_GIVEN')

def stage_gym5(t): badge_gym(t, 'FuchsiaCity_Gym', 'Koga', 'FLAG_BADGE05_GET')

def stage_hema_in(t):
    assert t.go('CeladonCity_Condominiums_1F', banned=BAN), 'manoir de Bourg Quartz inaccessible'
    t.talk_script('TeaWoman', 14); t.report('FLAG_GOT_TEA')
    assert t.getflag('FLAG_GOT_TEA'), 'the non obtenu'
    assert t.go('SaffronCity'), 'Hematown inaccessible (garde de la Route 8 ?)'
    t.report('FLAG_HEMATEK_ALLIES_IN')

def stage_hema_tower(t):
    assert t.go('SilphCo_11F'), 'tour Hematek 11F inaccessible'
    t.report('FLAG_HEMATEK_ALLIES_IN', 'FLAG_HEMATEK_BRICE_GONE', 'FLAG_HEMATEK_FLORA_GONE', 'FLAG_HEMATEK_N_GONE')
    t.walk_fight((6, 16), 8); t.walk_fight((6, 15), 8); t.scene(900, shot='hematek11')
    t.report('FLAG_HEMATEK_BOSS_DONE', 'FLAG_HEMATITE_STOLEN')
    assert t.getflag('FLAG_HEMATEK_BOSS_DONE'), 'scene du boss Hematek non declenchee'

def stage_gym6(t): badge_gym(t, 'SaffronCity_Gym', 'Sabrina', 'FLAG_BADGE06_GET')

def stage_chron_in(t):
    assert t.go('CinnabarIsland', banned=('Route19', 'Route20', 'FuchsiaCity')), 'Chrondrolia inaccessible (Surf ?)'
    t.report('FLAG_CHRONDROLIA_RAID_STARTED')

def stage_chron_key(t):
    assert t.go('CinnabarIsland', banned=('Route19', 'Route20', 'FuchsiaCity')), 'Chrondrolia inaccessible'
    assert t.go('PokemonMansion_B1F', banned=('Route19', 'Route20')), 'manoir B1F inaccessible'
    t.talk_script('SecretKey', 8); t.report('FLAG_HIDE_POKEMON_MANSION_B1F_SECRET_KEY')

def stage_gym7(t):
    assert t.go('CinnabarIsland_Gym'), 'arene 7 inaccessible'
    t.quiz_signs([(22, 10), (15, 2), (13, 10), (13, 17), (1, 18), (1, 10)])
    t.report(*['FLAG_CINNABAR_GYM_QUIZ_%d' % i for i in range(1, 7)])
    badge_gym(t, 'CinnabarIsland_Gym', 'Blaine', 'FLAG_BADGE07_GET')

def stage_chron_raid(t):
    assert t.go('CinnabarIsland'), 'sortie arene 7'
    for k in range(4):      # panne de courant + revelation du maire
        t.scene(maxn=900, shot='chron_scene%d' % k); t.report('FLAG_CHRONDROLIA_RAID_STARTED', 'VAR_TEMP_2')
        if t.st()[0] == 'CinnabarIsland' and t.getflag('FLAG_CHRONDROLIA_RAID_STARTED'): break
        if t.st()[0] == 'CinnabarIsland' and k >= 3: t.go('CinnabarIsland', banned=('Route19', 'Route20', 'FuchsiaCity'))
    if not t.getflag('FLAG_CHRONDROLIA_RAID_STARTED'):
        t.go('CinnabarIsland', banned=('Route19', 'Route20', 'FuchsiaCity')); t.scene(maxn=900)
    assert t.getflag('FLAG_CHRONDROLIA_RAID_STARTED'), 'panne de courant / maire : scene non declenchee'
    assert t.go('PokemonMansion_3F', banned=('Route19', 'Route20', 'FuchsiaCity')), 'manoir 3F inaccessible'
    t.talk_script('OnybrisSelene', 40, 'selene'); t.talk_script('EventScript_Topaz', 30, 'topaz')
    t.report('FLAG_CHRONDROLIA_RAID_DONE')
    assert t.getflag('FLAG_CHRONDROLIA_RAID_DONE'), 'topaze non obtenu'

STAGES = [('ranch', stage_opening_ranch), ('school', stage_school), ('lab', stage_lab), ('route1q', stage_route1_quest), ('opan', stage_opanihrum), ('gym1', stage_gym1), ('gym2', stage_gym2), ('cottage', stage_cottage), ('ssanne', stage_ssanne), ('gym3', stage_gym3), ('tower', stage_tower), ('quartz', stage_quartz), ('gym4', stage_gym4), ('ameth', stage_ameth), ('gym5', stage_gym5), ('hema_in', stage_hema_in), ('hema_tower', stage_hema_tower), ('gym6', stage_gym6), ('chron_in', stage_chron_in), ('chron_key', stage_chron_key), ('gym7', stage_gym7), ('chron_raid', stage_chron_raid)]

if __name__ == '__main__':
    # usage : run_full.py all | run_full.py <etape> [<etape> ...]   (une etape isolee repart de la sauvegarde de la precedente)
    names = [n for n, _ in STAGES]; want = sys.argv[1:] or ['all']
    seq = names if want == ['all'] else want
    t = None
    for nm in seq:
        i = names.index(nm)
        if t is None: t = Auto.boot() if i == 0 else Auto.resume(names[i - 1])
        log('=== STAGE', nm, time.strftime('%H:%M:%S'))
        STAGES[i][1](t); t.save(nm)
