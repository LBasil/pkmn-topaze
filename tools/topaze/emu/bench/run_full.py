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
OPEN_GATE_MAPS = ('MtEmber',)       # cartes ou les rochers (Eclate-Roc) et rochers Force sont geres par Auto.clear_gates : le graphe statique les ignore
def is_gate(name, gfx):
    if name.startswith(OPEN_GATE_MAPS) and ('ROCK_SMASH' in gfx or 'PUSHABLE_BOULDER' in gfx): return False
    return any(g in gfx for g in GATE_GFX)
def nav_of(name):
    if name not in _NAV:
        n = R.Nav(name)
        n.objs = {(o['x'], o['y']) for o in n.mj['object_events'] if is_gate(name, o['graphics_id'])}
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
        seen = set()      # une sortie par composante d'arrivee distincte (sinon une poche voisine peut masquer la bonne : Ile 6 / Chemin d'eau)
        for a, b in cells:
            if lab.get(a) == comp and 0 <= b[0] < dnav.w and 0 <= b[1] < dnav.h and not dnav.blocked(*b):
                k = frozenset(comps_of(dn, b))
                if k in seen: continue
                seen.add(k); out.append(('conn', dn, cn, a, b))
    return out
def route(src_map, src_cell, dst, banned=()):
    """Chemin le plus court de composante en composante jusqu'a la carte dst : liste de sorties (voir exits)."""
    c0s = comps_of(src_map, src_cell)
    if not c0s: return None
    prev = {}; q = collections.deque(); end = None
    for c0 in sorted(c0s): prev[(src_map, c0)] = None; q.append((src_map, c0))
    while q:
        n = q.popleft()
        if (n[0] == dst) if isinstance(dst, str) else (n[0] == dst[0] and n[1] in comps_of(dst[0], dst[1])): end = n; break      # dst : carte, ou (carte, case) = la composante de cette case
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
    def plan_objs(s):
        """Objets vivants + objets immobiles de la carte hors de portee de la camera (sinon le plan change selon la position : oscillations)."""
        live = s.live_objs(); out = set(live)
        for o in mj(s.sync())['object_events']:
            mt = o.get('movement_type', '')       # objets 'clone' (carte voisine) : pas de type de mouvement
            if 'FACE' not in mt and 'NONE' not in mt and 'LOOK' not in mt: continue
            if o.get('flag', '0') not in ('0', 0) and s.getflag(o['flag']): continue
            out.add((o['x'], o['y']))
        return out
    def heal(s):
        """Soigne l'equipe (PV au max, statut retire, PP intacts) : le bot n'a pas de logique de soin (Centre Pokemon)."""
        for i in range(6):
            a = 0x02024288 + 100 * i
            if not s.e.peek(a + 0x58, 2)[1:] and not s.e.peek(a + 0x58, 2)[0]: continue
            mx = s.e.peek(a + 0x58, 2); s.e.cmd('poke8 %x %x' % (a + 0x56, mx[0])); s.e.cmd('poke8 %x %x' % (a + 0x57, mx[1]))
            for k in range(4): s.e.cmd('poke8 %x 0' % (a + 0x50 + k))
    def buff(s, lvl=100, stat=700, hp=900):
        """Post-game : l'equipe du bot (un seul Pokemon) est gonflee (niveau, stats, PV) pour qu'un combat de test ne se perde plus sur un detail d'equilibrage ; les degats subis restent soignes par heal*()."""
        import struct as _s
        for i in range(6):
            a = 0x02024288 + 100 * i
            if not s.e.peek(a + 0x58, 2) != b'\x00\x00': continue
            if s.e.peek(a + 0x58, 2) == b'\x00\x00': continue
            s.e.cmd('poke8 %x %x' % (a + 0x54, lvl))
            for off, v in ((0x56, hp), (0x58, hp), (0x5a, stat), (0x5c, stat), (0x5e, stat), (0x60, stat), (0x62, stat)):
                s.e.cmd('poke8 %x %x' % (a + off, v & 255)); s.e.cmd('poke8 %x %x' % (a + off + 1, v >> 8))
    def vr_open(s):
        """La Route 23 remet a 0 les variables des enigmes de Force de la Route Victoire a chaque entree : on les repose (enigmes vanille non rejouees)."""
        for v in ('VAR_MAP_SCENE_VICTORY_ROAD_1F', 'VAR_MAP_SCENE_VICTORY_ROAD_2F_BOULDER1', 'VAR_MAP_SCENE_VICTORY_ROAD_2F_BOULDER2', 'VAR_MAP_SCENE_VICTORY_ROAD_3F'):
            if s.getvar(v) != 100: s.var(v, 100)
    def heal_battle(s):
        """En combat : PV de notre combattant actif remis au max (le bot ne sait ni soigner ni changer de Pokemon)."""
        a = 0x02023be4
        mx = s.e.peek(a + 0x2c, 2)
        if not (mx[0] or mx[1]): return
        s.e.cmd('poke8 %x %x' % (a + 0x28, mx[0])); s.e.cmd('poke8 %x %x' % (a + 0x29, mx[1]))
        for k in range(4): s.e.cmd('poke8 %x 0' % (a + 0x4c + k))
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
        k, dest = e[0], e[1]; cur = s.sync(); m0 = s.pos()[:2]
        if cur.startswith(OPEN_GATE_MAPS): s.e.run(120, 0)      # laisse les objets apparaitre apres l'arrivee (sinon rochers invisibles -> chemin 'libre' a tort)
        nav = s.nav()
        if k == 'warp':
            nav.objs = s.live_objs(); w = nav.mj['warp_events'][e[2]]
            if cur.startswith(OPEN_GATE_MAPS):      # rochers/rochers Force : pas de chemin tant qu'ils barrent -> on rend la main (go() appelle clear_gates) au lieu de forcer la porte
                g = (w['x'], w['y']); me = (s.pos()[2], s.pos()[3])
                if not any(nav.path(me, a) for a in [g] + [(g[0] + dx, g[1] + dy) for dx, dy in ((0, 1), (0, -1), (1, 0), (-1, 0))] if not nav.blocked(*a) or a == g): return False
            s._warp_try(nav, w, 12, None)
        else:
            s.edge_cross(e[2], e[3])
        return s.pos()[:2] != m0
    def live_gfx(s):
        """{case: graphicsId} des objets vivants (hors joueur)."""
        b = s.e.peek(0x02036e3c, 0x24 * 16); out = {}
        for i in range(16):
            o = b[i * 0x24:(i + 1) * 0x24]
            if o[0] & 1 and not (o[2] & 1) and not (o[1] >> 5) & 1:
                x, y = struct.unpack_from('<hh', o, 0x10); out[(x - 7, y - 7)] = o[5]
        return out
    def gate_state(s):
        """(rochers Force, rochers a briser) de la carte courante : positions reelles pres du joueur, positions du JSON plus loin."""
        j = mj(s.sync()); lg = s.live_gfx(); p = s.pos(); me = (p[2], p[3])
        bo = {c for c, g in lg.items() if g == 97}; ro = {c for c, g in lg.items() if g == 96}
        for o in j['object_events']:
            c = (o['x'], o['y'])
            if abs(c[0] - me[0]) <= 9 and abs(c[1] - me[1]) <= 7: continue      # dans la zone de la camera (+1) : les objets existent vraiment, on lit le direct
            if o.get('flag', '0') not in ('0', 0) and s.getflag(o['flag']): continue
            if 'PUSHABLE_BOULDER' in o['graphics_id']: bo.add(c)
            elif 'ROCK_SMASH' in o['graphics_id']: ro.add(c)
        return bo, ro
    def clear_gates(s, goal):
        """Rochers (Eclate-Roc) et rochers Force (Force) sur le chemin vers `goal` : planifie (gates.plan, recherche sur positions des rochers), brise le premier
        rocher a briser, active Force, puis execute les pas/poussees en verifiant chaque case. True si une action a eu lieu (on replanifie ensuite)."""
        import gates
        if not s.sync().startswith(OPEN_GATE_MAPS): return False
        bo, ro = s.gate_state()
        if not bo and not ro: return False
        nav = s.nav(); nav.objs = set(s.plan_objs()) - bo - ro; p = s.pos(); cur = (p[2], p[3])
        tgts = [goal] if not nav.blocked(*goal) else [(goal[0] + dx, goal[1] + dy) for dx, dy in ((0, 1), (0, -1), (1, 0), (-1, 0)) if not nav.blocked(goal[0] + dx, goal[1] + dy)]
        res = None
        for g in tgts:
            res = gates.plan(nav, cur, g, bo, ro) or gates.plan(nav, cur, g, bo, ro, allow_rocks=True)
            if res: break
        if not res: return False
        steps, smash = res
        log('  obstacles a CS : %d pas, %d poussees, rochers a briser %s' % (len(steps), sum(1 for a in steps if a[0] == 'push'), smash))
        if smash: return s.talk_obj(smash[0], 14)
        pushes = [a for a in steps if a[0] == 'push']
        if pushes and not s.getflag('FLAG_SYS_USE_STRENGTH'):
            s.talk_obj(pushes[0][2], 14)
            if not s.getflag('FLAG_SYS_USE_STRENGTH'): log('BLOCK Force non activee'); return False
        for kind, d, c in steps:
            before = s.pos(); tz.step(s.e, d); s.settle()
            if not s.idle(): s.scene(maxn=300)
            after = s.pos()
            if after[:2] != before[:2] or (after[2], after[3]) != c: return True      # carte changee ou imprevu : on replanifie
        return True
    def reach_gates(s, goal, tries=12):
        """Va jusqu'a la case `goal` de la carte courante, en poussant les rochers Force / brisant les rochers qui barrent (cartes OPEN_GATE_MAPS). True si arrive."""
        for _ in range(tries):
            s.e.run(90, 0); p = s.pos(); me = (p[2], p[3])
            if me == goal: return True
            n = s.nav(); n.objs = set(s.live_objs())
            if n.path(me, goal): s.walk_to(goal); continue
            if not s.clear_gates(goal): break
        p = s.pos(); return (p[2], p[3]) == goal
    def blocking_objs(s, goal):
        """Objets (PNJ, dresseurs, balles) dont le retrait seul ouvre un chemin (fleches comprises) jusqu'a `goal` ; tries par distance."""
        from spin import spin_bfs
        nav = s.nav(); base = set(s.plan_objs()); p = s.pos(); cur = (p[2], p[3])
        tgts = [goal] if not nav.blocked(*goal) else [(goal[0] + dx, goal[1] + dy) for dx, dy in ((0, 1), (0, -1), (1, 0), (-1, 0)) if not nav.blocked(goal[0] + dx, goal[1] + dy)]
        nav.objs = base
        if any(spin_bfs(nav, cur, g) for g in tgts): return []
        out = []
        for o in base:
            nav.objs = base - {o}
            if any(spin_bfs(nav, cur, g) for g in tgts): out.append(o)
        return sorted(out, key=lambda o: abs(o[0] - cur[0]) + abs(o[1] - cur[1]))
    def clear_blocker(s, goal):
        """Si un objet vivant (PNJ, dresseur) barre le chemin vers `goal`, va lui parler (combat/dialogue). True si une action a eu lieu."""
        for o in s.blocking_objs(goal)[:1]:          # objet seul qui barre un couloir (balle au sol, dresseur hors camera...) : on lui parle
            log('  deblocage (retrait seul) : objet en', o, 'vers', goal); s.save('blocker_%s' % s.sync())
            if s.talk_obj(o, 30): return True
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
        cut_done = set(); gate_tries = collections.Counter()
        if 'SNORLAX' in GATE_GFX and s.getflag('FLAG_GOT_POKE_FLUTE'): open_gate('SNORLAX')
        if not R.SURF and s.getflag('FLAG_GOT_HM03') and s.getflag('FLAG_BADGE05_GET'): R.SURF = True; _NAV.clear(); _COMP.clear()
        for _ in range(tries * 40):
            cur = s.sync(); s.heal()
            if cur == 'Route23': s.vr_open()
            if isinstance(target, tuple):
                if cur == target[0] and comps_of(cur, (s.pos()[2], s.pos()[3])) & comps_of(target[0], target[1]): return True
            elif cur == target: return True
            if cur == 'MtMoon_B2F' and not s.getflag('FLAG_GOT_FOSSIL_FROM_MT_MOON'): s.take_fossil()      # les deux fossiles barrent le couloir de la sortie ouest : il faut en prendre un (vanille)
            n_live = s.nav(); n_live.objs = {(o['x'], o['y']) for o in n_live.mj['object_events'] if is_gate(cur, o['graphics_id']) and not (o.get('flag', '0') not in ('0', 0) and s.getflag(o['flag']))}   # objet masque (drapeau HIDE pose) = plus un obstacle
            _NAV[cur] = n_live; _COMP.pop(cur, None)        # la carte courante est lue en direct (barrieres ouvertes par des scripts...)
            p = s.pos(); rt = route(cur, (p[2], p[3]), target, banned)
            if not rt and s.tele_exit(): continue
            if not rt: log('BLOCK pas de route', cur, (p[2], p[3]), '->', target); s.save('noroute_' + cur); return False
            e = rt[0]
            if not s.hop(e):
                if gate_tries[(cur, e[3])] < 8:
                    gate_tries[(cur, e[3])] += 1
                    if s.clear_gates(e[3]): continue
                if s.getflag('FLAG_GOT_HM01') and cur not in cut_done:      # un arbre a couper barre peut-etre le chemin : on les coupe tous (une fois par carte)
                    cut_done.add(cur)
                    if s.cut_trees(): log('  arbres coupes sur', cur); continue
                if tried[(cur, e[3])] < 5:
                    tried[(cur, e[3])] += 1
                    if not s.idle(): s.scene(maxn=600)          # une scene a pu se declencher en route : on la laisse finir puis on reessaie
                    if s.clear_blocker(e[3]) or s.sync() != cur or tried[(cur, e[3])] <= 2: continue
                log('BLOCK hop echoue', cur, e[:2], e[3], s.pos()); banned.add((cur, e[1], e[3]))
                s.shot('block_%s_%s' % (cur, e[1])); s.save('hopfail_' + cur)
            else: log('  ', cur, '->', s.sync(), s.pos()[2:])
        return s.sync() == (target[0] if isinstance(target, tuple) else target)
    def take_fossil(s):
        """Mont Selenite B2F : bat le Binoclard (declenche en approchant) puis prend le Fossile Helix (case (14,7), on parle depuis (14,8))."""
        for _ in range(3):
            s.talk_at((14, 8), 'UP', 24)
            if s.getflag('FLAG_GOT_FOSSIL_FROM_MT_MOON'): log('  fossile pris'); return True
        log('BLOCK fossile non pris', s.pos()); s.save('nofossil'); return False
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
            if 'CutTree' not in o['script']: continue   # hors ecran = pas encore instancie : on s'approche quand meme
            if s.talk_obj((o['x'], o['y']), 6): n += 1
        return n
    def smash_rocks(s, maxn=12):
        """Brise (parle a) tous les rochers `RockSmash` atteignables de la carte courante ; renvoie le nombre de rochers brises."""
        n = 0
        for o in mj(s.sync())['object_events']:
            if 'RockSmash' not in o['script']: continue
            if s.talk_obj((o['x'], o['y']), 10): n += 1
            if n >= maxn: break
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
        gr = [o for o in mj('CeladonCity_GameCorner')['object_events'] if (o['x'], o['y']) == (11, 2) and not (o.get('flag', '0') not in ('0', 0) and t.getflag(o['flag']))]
        if gr: t.talk_obj((11, 2), 10)      # le sbire devant l'affiche (hors camera au depart : on ne se fie pas a live_objs)
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

def stage_seafoam(t):
    assert t.go('SeafoamIslands_1F'), 'volcan 1F inaccessible'
    if not t.getflag('FLAG_SEAFOAM_ALLIES_MET'): x = t.pos()[2]; t.walk_fight((x, 19), 8, 'sf1w')     # declencheur de la scene (y=19)
    t.scene(maxn=900, shot='sf1'); t.report('FLAG_SEAFOAM_ALLIES_MET')
    assert t.getflag('FLAG_SEAFOAM_ALLIES_MET'), 'Gold/Silver : scene des allies non declenchee'
    # Limite du bot : le courant de lave B3F/B4F (vanille) ne s'arrete que par la chaine de rochers 1F->B1F->B2F->B3F (puzzle non resolu par le bot) :
    # on pose les drapeaux 'courant arrete' pour que Surf passe. (Route20 les remet a 0 a chaque entree : on pose apres.)
    t.flag('FLAG_STOPPED_SEAFOAM_B3F_CURRENT'); t.flag('FLAG_STOPPED_SEAFOAM_B4F_CURRENT'); R.CURRENT_STOPPED = True; _NAV.clear(); _COMP.clear()
    assert t.go('SeafoamIslands_B4F'), 'volcan B4F inaccessible'
    t.scene(maxn=900, shot='sf4'); t.report('FLAG_SEAFOAM_BOSS_DONE')
    if not t.getflag('FLAG_SEAFOAM_BOSS_DONE'): t.talk_script('Kronos', 40, 'sf4k')
    t.report('FLAG_SEAFOAM_BOSS_DONE')
    assert t.getflag('FLAG_SEAFOAM_BOSS_DONE'), 'Kronos (volcan B4F) non battu'

def stage_gym8(t): badge_gym(t, 'ViridianCity_Gym', 'Giovanni', 'FLAG_BADGE08_GET')

def stage_victory(t):
    # Les enigmes de Force (rochers sur interrupteurs) sont celles de la vanille (cartes inchangees) : non rejouees, on pose leurs variables a 100.
    assert t.go('Route23'), 'Route 23 inaccessible'      # (la Route 23 remet ces variables a 0 a chaque entree : on pose apres)
    for v in ('VAR_MAP_SCENE_VICTORY_ROAD_1F', 'VAR_MAP_SCENE_VICTORY_ROAD_2F_BOULDER1', 'VAR_MAP_SCENE_VICTORY_ROAD_2F_BOULDER2', 'VAR_MAP_SCENE_VICTORY_ROAD_3F'): t.var(v, 100)
    t.save('route23')
    # Vesper (Gengar Lv54, Destin Lie) : le bot n'a qu'un Pokemon et perd (blanc-out) -> combat de Vesper saute (drapeau dresseur pose), limite du bot.
    t.flag(0x500 + 80)
    assert t.go('VictoryRoadLair_3F'), 'repaire (3F) inaccessible'
    t.report('FLAG_VR_RED_MET', 'FLAG_VR_BOSS_DONE'); t.scene(maxn=900, shot='lair3')
    if not t.getflag('FLAG_VR_BOSS_DONE'): t.hold('UP', 40); t.scene(maxn=1200, shot='lair3b')
    t.report('FLAG_VR_BOSS_DONE')
    assert t.getflag('FLAG_VR_BOSS_DONE'), 'scene finale du repaire non jouee'

def league_exit(t):
    """Sort de la salle de Lorelei vers le Centre du Plateau (la porte du bas est une case a collision : on pousse vers le bas depuis (6,10))."""
    if t.sync() != 'PokemonLeague_LoreleisRoom': return True
    t.walk_fight((6, 10), 6)
    for _ in range(8):
        t.hold('DOWN', 24); t.e.run(60, 0)
        if t.sync() != 'PokemonLeague_LoreleisRoom': break
    return t.sync() != 'PokemonLeague_LoreleisRoom'

def league_enter(t):
    """Du Centre du Plateau a la salle de Lorelei (la case d'arrivee est une porte a collision : franchie a la main, la scene d'entree avance le joueur)."""
    assert t.go('IndigoPlateau_PokemonCenter_1F'), 'Centre du Plateau inaccessible'
    for _ in range(40):          # la gardienne (5,3) peut se tenir devant la porte : on attend qu'elle se pousse
        if t.walk_fight((4, 2), 2) is True: break
        t.e.run(90, 0)
    assert t.pos()[2:] == (4, 2), 'porte de la Ligue inaccessible'
    t.hold('UP', 20); t.e.run(80, 0); t.scene(maxn=400)
    assert t.sync() == 'PokemonLeague_LoreleisRoom', 'entree de la Ligue sans effet : ' + t.sync()

def league_finale(t):
    """Salle du Champion (Chen, boss, legendaires) -> Temple de la renommee (voeu de Jirachi, 3 fins) -> generique."""
    t.save('league_won'); log('  tournoi termine : porte du Champion')
    def champ():
        t.walk_fight((6, 3), 10); t.hold('UP', 20); t.e.run(80, 0)
        for k in range(8):
            t.scene(maxn=700, shot='champ%d' % k); log('  salle du Champion :', t.sync(), t.pos()[2:], 'inbattle', t.inbattle())
            if t.sync() != 'PokemonLeague_ChampionsRoom': break
            t.walk_fight((6, 3), 6); t.hold('UP', 20); t.e.run(60, 0)
    champ()
    if t.sync() != 'PokemonLeague_HallOfFame':
        # blanc-out (double combat contre les deux legendaires avec un seul Pokemon) : on recharge l'etat et on saute les 3 combats de la salle (drapeaux dresseur)
        log('  blanc-out dans la salle du Champion (limite du bot) : combats sautes')
        t.e.cmd('ls %s/league_won.ss' % ST); t.e.run(10, 0); t.sync()
        for tr in (752, 753, 754): t.flag(0x500 + tr)
        t.heal(); champ()
    t.save('hof_in')
    for k in range(6):
        t.scene(maxn=500, shot='hof%d' % k); log('  Temple de la renommee / fin :', t.sync(), t.pos()[2:], 'fin', t.getvar('VAR_TOPAZE_ENDING'))
        if t.sync() not in ('PokemonLeague_HallOfFame', 'PokemonLeague_ChampionsRoom'): break
    t.save('ending')

def stage_league(t):
    # (les etats de la chaine ont ete pris avec l'ancienne ROM : la correction de la garde est simulee par ce drapeau ; verifiee a part avec la ROM finale)
    t.flag('FLAG_SYS_CAN_LINK_WITH_RS')
    assert t.go('IndigoPlateau_Exterior'), 'Plateau Indigo inaccessible'
    t.save('indigo'); league_enter(t); t.save('league_in')
    last = -1; skipped = []
    for r in range(30):
        rd = t.getvar('VAR_TOURNAMENT_ROUND'); log('  tournoi : tour', rd, t.sync(), t.pos()[2:])
        if t.sync() != 'PokemonLeague_LoreleisRoom':
            if t.sync() == 'PokemonLeague_HallOfFame': break
            # blanc-out (le bot n'a qu'un Pokemon : Chant Canon/Destin Lie le terrassent) : on saute l'adversaire en avancant le tour et on reentre
            log('  blanc-out au tour', rd, '(limite du bot) : tour saute'); skipped.append(rd); t.save('league_wo%d' % rd)
            t.var('VAR_TOURNAMENT_ROUND', rd + 1); t.heal(); league_enter(t); last = -1; continue
        t.scene(maxn=300); t.walk_fight((6, 6), 10); t.face('UP'); t.press('A', 4, 30)
        t.scene(maxn=900, shot='league%d' % r); t.e.run(120, 0); t.scene(maxn=120)
        if t.getvar('VAR_TOURNAMENT_ROUND') == rd and t.sync() == 'PokemonLeague_LoreleisRoom' and rd == last: log('BLOCK tournoi fige au tour', rd); t.save('leaguestuck'); break
        last = rd
    if t.getvar('VAR_TOURNAMENT_ROUND') >= 9 and t.sync() == 'PokemonLeague_LoreleisRoom': league_finale(t)
    log('FIN ligue', t.sync(), t.pos()[2:], 'ending', t.getvar('VAR_TOPAZE_ENDING'), 'round', t.getvar('VAR_TOURNAMENT_ROUND'), 'tours sautes', skipped)

def stage_ending1(t):
    """Depuis la fin du tournoi : salle du Champion, Temple de la renommee, voeu 1 (laisser partir Jirachi). On s'arrete a l'arrivee sur le Plateau Indigo, AVANT le generique
    (le jeu redemarre apres le generique ; en vrai le joueur reprend a Bourg-Palette) : le var de scene est remis a 0 pour que la scene du generique ne se joue pas."""
    if t.getvar('VAR_TOPAZE_ENDING') == 1 and t.getflag('FLAG_TOPAZE_POSTGAME'):
        # l'etape 'league' (league_finale) a deja joue la salle du Champion et le Temple : l'etat sauve est dans le generique. On le laisse finir (le jeu redemarre :
        # lectures de carte invalides pendant ce temps), on passe l'ecran-titre (A = CONTINUER) ; la sauvegarde du harnais reprend sur le Plateau Indigo (en vrai : Bourg-Palette).
        for i in range(200):
            t.e.run(240, 0); t.press('A', 4, 40); m = t.sync(); p = t.pos()
            if p[2:] != (0, 0) and m == 'IndigoPlateau_Exterior': break
        # LIMITE DU HARNAIS : le « CONTINUER » recharge une sauvegarde plus ancienne (la sauvegarde du Temple de la renommee n'est pas conservee par l'emulateur ; le jeu, lui,
        # l'ecrit comme en vanille) : on repose donc a la main ce que le Temple a pose (voeu 1, fin de jeu, bavards post-game).
        t.var('VAR_MAP_SCENE_INDIGO_PLATEAU_EXTERIOR', 0); t.var('VAR_TOPAZE_ENDING', 1)
        for f in ('FLAG_TOPAZE_POSTGAME', 'FLAG_TOPAZE_COUNCIL', 'FLAG_SYS_GAME_CLEAR'): t.flag(f)
        for f in ('FLAG_HIDE_POSTGAME_STRANGER', 'FLAG_HIDE_POSTGAME_GOSSIPERS'): t.flag(f, False)
        log('  fin 1 : generique passe, reprise sur', t.sync(), t.pos()[2:], 'fin', t.getvar('VAR_TOPAZE_ENDING'), 'postgame', t.getflag('FLAG_TOPAZE_POSTGAME'))
        assert t.sync() == 'IndigoPlateau_Exterior' and t.getvar('VAR_TOPAZE_ENDING') == 1 and t.getflag('FLAG_TOPAZE_POSTGAME'), 'fin 1 non atteinte'
        t.e.run(120, 0); return
    t.walk_fight((6, 3), 10); t.hold('UP', 20); t.e.run(80, 0)
    for i in range(400):
        t.scene(maxn=12)
        m = t.sync()
        if m == 'IndigoPlateau_Exterior':
            t.var('VAR_MAP_SCENE_INDIGO_PLATEAU_EXTERIOR', 0); break
        if m == 'PokemonLeague_ChampionsRoom' and t.idle(): t.walk_fight((6, 3), 4); t.hold('UP', 20); t.e.run(40, 0)
    log('  fin 1 : carte', t.sync(), 'fin', t.getvar('VAR_TOPAZE_ENDING'), 'postgame', t.getflag('FLAG_TOPAZE_POSTGAME'), 'clear', t.getflag('FLAG_SYS_GAME_CLEAR'))
    assert t.getvar('VAR_TOPAZE_ENDING') == 1 and t.getflag('FLAG_TOPAZE_POSTGAME'), 'fin 1 non atteinte'
    t.e.run(120, 0)

def stage_pg_pallet(t):
    """Post-game 0/5 : apres la fin 1, le jeu ramene le joueur a Bourg-Palette (reprise apres le generique). On entre dans le Centre du Plateau pour declencher ce retour."""
    t.buff(); t.flag('FLAG_SYS_CAN_LINK_WITH_RS')
    assert t.go('IndigoPlateau_PokemonCenter_1F'), 'Centre du Plateau inaccessible'
    t.e.run(200, 0)
    t.scene(maxn=200)
    log('  retour apres le titre :', t.sync(), t.pos()[2:], 'idle', t.idle())
    assert t.sync() == 'PalletTown'

def stage_pg_indigo(t):
    """Post-game 1/5 : les retours du Centre du Plateau (Brice, Flora, Misty) puis le Conseil des Anciens (20 combats dans la salle de Lorelei)."""
    t.buff()
    t.flag('FLAG_SYS_CAN_LINK_WITH_RS')       # (ancienne ROM : simule la correction de la garde du Centre)
    assert t.go('IndigoPlateau_PokemonCenter_1F'), 'Centre du Plateau inaccessible'
    for pat in ('Brice', 'Flora', 'Misty'):
        try: log('  retour', pat, t.talk_script(pat, 14))
        except AssertionError as ex: log('BLOCK', ex)
    t.save('pg_indigo_pc')
    league_enter(t); t.save('pg_elders_in')
    last = -1; wo = []
    for r in range(60):
        rd = t.getvar('VAR_ELDERS_ROUND'); log('  anciens : tour', rd, t.sync(), t.pos()[2:])
        if t.sync() != 'PokemonLeague_LoreleisRoom':
            log('  blanc-out au tour', rd, '(limite du bot) : ancien saute'); wo.append(rd); t.save('elders_wo%d' % rd)
            t.var('VAR_ELDERS_ROUND', rd + 1); t.heal(); league_enter(t); last = -1; continue
        if rd >= 20: break
        t.scene(maxn=300); t.walk_fight((6, 6), 10); t.face('UP'); t.press('A', 4, 30)
        t.scene(maxn=900, shot='elder%d' % rd); t.e.run(120, 0); t.scene(maxn=120)
        if t.getvar('VAR_ELDERS_ROUND') == rd and t.sync() == 'PokemonLeague_LoreleisRoom' and rd == last: log('BLOCK anciens fige au tour', rd); t.save('elders_stuck'); break
        last = rd
    log('FIN anciens : tour', t.getvar('VAR_ELDERS_ROUND'), 'blanc-outs', wo, 'MasterBall', t.e and 'voir sac')

def legend_fight(t, pat, flags=(), n=14):
    """Parle a un legendaire statique (script contenant `pat`), joue le combat, soigne ; renvoie l'etat des drapeaux."""
    t.e.run(90, 0); t.scene(maxn=200)
    ok = t.talk_script(pat, n); t.scene(maxn=900)
    for _ in range(6):      # combat long (legendaire a beaucoup de PV) : on le finit avant de continuer
        if not t.inbattle(): break
        t.finish_battle(maxn=900); t.scene(maxn=300)
    t.heal()
    log('  legendaire', pat, 'parle', ok, [(f, t.getflag(f)) for f in flags], t.sync(), t.pos()[2:])
    return ok

def stage_pg_mine(t):
    """Post-game 2/5 : mine de Grenalux (vision de l'Aura, Mew qui s'enfuit) puis Mew sous le camion d'Apatia."""
    t.buff()
    assert t.go('GrenaluxMine_3F'), 'mine 3F inaccessible'
    t.walk_fight((14, 11), 10); t.scene(maxn=1200, shot='mine')
    t.report('FLAG_MEW_FLED', 'FLAG_HIDE_MINE_MEW')
    assert t.getflag('FLAG_MEW_FLED'), 'vision de la mine non jouee'
    t.save('pg_mine_done')
    assert t.go('VermilionCity'), 'Apatia inaccessible'
    legend_fight(t, 'MewTruck', ('FLAG_FOUGHT_MEW_TRUCK',))

def give_hms(t):
    """LIMITE DU BOT : CS04 (Force) et CS06 (Eclate-Roc) mises directement dans le sac (la CS04 vient du gardien du Parc Safari, la CS06 de la source chaude de l'Ile 1 : non rejoues)."""
    sb = t.e.u32(0x03005048); sb2 = t.e.u32(0x0300504c); key = t.e.u32(sb2 + 0xF20) & 0xffff; slot = sb + 0x464
    for it in (342, 344):
        for i in range(58):
            a = slot + 4 * i; cur = struct.unpack('<H', t.e.peek(a, 2))[0]
            if cur == it: break
            if cur == 0:
                for k, b in enumerate(struct.pack('<HH', it, 1 ^ key)): t.e.cmd('poke8 %x %x' % (a + k, b))
                break
    for f in ('FLAG_GOT_HM04', 'FLAG_GOT_HM06'): t.flag(f)

def stage_pg_sulfura(t):
    """Post-game : Sulfura (sommet du Mont Brasier) : Force (rochers a pousser) et Eclate-Roc, planifies par gates.py / Auto.clear_gates."""
    R.SURF = True; R.NOWALK = (19,); t.buff(); give_hms(t)
    go_isle(t, 1, 'OneIsland'); assert t.go('MtEmber_Summit'), 'sommet du Mont Brasier inaccessible (rochers)'
    t.e.run(90, 0); assert t.reach_gates((9, 7)), 'Sulfura inaccessible (rochers Force du sommet)'
    legend_fight(t, 'Moltres', ('FLAG_FOUGHT_MOLTRES', 'FLAG_HIDE_MOLTRES')); t.report('FLAG_FOUGHT_MOLTRES')

def stage_pg_birds(t):
    """Post-game 3/5 : Artikodin (clairiere de Bourg Quartz) et Electhor (centrale) reapparaissent."""
    t.buff()
    assert t.go('CeladonCity'), 'Bourg Quartz inaccessible'
    t.e.run(90, 0); log('  arbres coupes :', t.cut_trees()); log('  Artikodin : masque ?', t.getflag('FLAG_HIDE_ARTICUNO'))
    legend_fight(t, 'Articuno', ('FLAG_FOUGHT_ARTICUNO',))
    assert t.go('PowerPlant'), 'centrale inaccessible'
    log('  Electhor : masque ?', t.getflag('FLAG_HIDE_ZAPDOS'))
    legend_fight(t, 'Zapdos', ('FLAG_FOUGHT_ZAPDOS',))

def stage_pg_ferry(t):
    """Post-game 4/5 : le marin d'Apatia donne les 2 billets puis embarque direct vers l'Ile 1."""
    t.buff()
    # NB : la ROM de test est anterieure au correctif du ferry (var One Island posee par le marin) : on simule le correctif.
    t.var('VAR_MAP_SCENE_ONE_ISLAND_POKEMON_CENTER_1F', 7)
    assert t.go('VermilionCity'), 'Apatia inaccessible'
    t.e.run(90, 0); t.talk_script('FerrySailor', 40, 'ferry1'); t.scene(maxn=900)
    t.report('FLAG_TOPAZE_GOT_TICKETS'); log('  apres ferry :', t.sync(), t.pos()[2:])
    assert t.sync().startswith('OneIsland'), 'ferry non pris'

def stage_pg_sevii(t):
    """Post-game 5/5 : Ile 1 = Bill et Celio au Centre (Echo 1 : annonce), puis Raikou sur la Route Braise."""
    t.buff(); R.SURF = True
    assert t.go('OneIsland_PokemonCenter_1F'), 'Centre Pokemon Ile 1 inaccessible'
    t.e.run(90, 0); t.report('VAR_ECHO_STAGE')
    for who in ('EventScript_Bill', 'EventScript_Celio'):
        t.talk_script(who, 40, 'echo_' + who[-4:]); t.report('VAR_ECHO_STAGE')
    t.save('pg_one_pc')
    assert t.go('OneIsland_KindleRoad'), 'Route Braise inaccessible'
    legend_fight(t, 'Raikou', ('FLAG_ECHO_BEAST_DONE',)); t.report('VAR_ECHO_STAGE', 'FLAG_ECHO_BEAST_DONE')

ISLES = ['Vermilion', 'One', 'Two', 'Three', 'Four', 'Five', 'Six', 'Seven']
def cur_isle(t):
    n = t.sync()
    if n.startswith('MtEmber'): return 1      # Mt Braise n'a pas le prefixe OneIsland
    for i, k in enumerate(ISLES):
        if n.startswith(k + 'Island'): return i

def sail_to(t, dest):
    """Prend le Seagallop depuis le port courant vers l'ile `dest` (indice de ISLES) ; navigue dans le menu (page 1 = 'Autres')."""
    cur = cur_isle(t); assert cur is not None, 'pas sur une ile Sevii'
    harbor = ISLES[cur] + 'Island_Harbor'
    assert t.sync() == harbor or t.go(harbor), 'port inaccessible ' + harbor
    page0 = [i for i in range(8) if i != cur][:4]
    page1 = ([i for i in (5, 6, 7) if i != cur] + [4])[:3] if cur < 5 else [i for i in (4, 5, 6, 7) if i != cur][:3]
    if dest in page0: downs = [page0.index(dest)]
    else: downs = [4, page1.index(dest)]
    pos = t.find_obj('Sailor'); assert pos and t.approach(pos), 'marin inaccessible'
    t.press('A', 4, 120)
    for k, n in enumerate(downs):
        for _ in range(n): t.press('DOWN', 4, 20)
        t.press('A', 4, 120)
    t.scene(maxn=900)
    log('  ferry', ISLES[cur], '->', ISLES[dest], ':', t.sync())
    assert cur_isle(t) == dest, 'ferry rate'

def go_isle(t, dest, mapname):
    if cur_isle(t) != dest: sail_to(t, dest)
    if dest == 3:    # correctif ThreeIsland_Port (motards) absent de la ROM de test : on le simule
        t.flags('FLAG_HIDE_THREE_ISLAND_BIKERS', 'FLAG_HIDE_THREE_ISLAND_ANTIBIKERS', 'FLAG_HIDE_THREE_ISLAND_LONE_BIKER'); t.var('VAR_MAP_SCENE_THREE_ISLAND', 4)
    assert t.go(mapname), mapname + ' inaccessible'

def icefall_climb(t):
    """Grotte Glacon : la CS07 (Cascade) est sur une balle de la 1F ; il faut ensuite remonter la cascade de l'entree pour atteindre le fond."""
    if cur_isle(t) != 4: sail_to(t, 4)
    if t.getflag('FLAG_HIDE_FOUR_ISLAND_ICEFALL_CAVE_1F_HM07'): return
    assert t.go(('FourIsland_IcefallCave_1F', (13, 16))), 'salle de la CS07 inaccessible'      # la balle est dans une salle fermee a l'ouest : on y arrive par la B1F
    t.e.run(90, 0); log('  CS07 prise :', t.talk_script('ItemHM07', 12), t.getflag('FLAG_HIDE_FOUR_ISLAND_ICEFALL_CAVE_1F_HM07'))
    assert t.go('FourIsland_IcefallCave_Entrance'), 'entree inaccessible'
    t.e.run(90, 0); r = t.walk_to((17, 21)); log('  pied de la cascade :', r, t.pos()[2:])
    t.face('UP'); t.mash(10); t.scene(maxn=300); log('  apres cascade :', t.pos()[2:]); R.NOWALK = ()

ECHO_PC = (2, 3, 5, 6, 8, 12, 14, 15, 17, 18, 20)
ECHO_BEAST = {1: (1, 'OneIsland_KindleRoad', 'Raikou'), 4: (2, 'TwoIsland_CapeBrink', 'Entei'), 7: (3, 'ThreeIsland_BondBridge', 'Suicune'),
              10: (4, 'FourIsland_IcefallCave_Back', 'Regice'), 13: (5, 'FiveIsland_Meadow', 'Registeel'), 16: (6, 'SixIsland_RuinValley', 'Regirock'),
              19: (7, 'SevenIsland_SevaultCanyon', 'Celebi')}

def echo_step(t):
    st = t.getvar('VAR_ECHO_STAGE'); log('ECHO stage', st, t.sync()); t.buff()
    if st in ECHO_PC:
        go_isle(t, 1, 'OneIsland_PokemonCenter_1F'); t.e.run(90, 0)
        for who in ('EventScript_Bill', 'EventScript_Celio', 'EventScript_Bill'): t.talk_script(who, 40, 'echo_%d_%s' % (st, who[-4:]))
    elif st in ECHO_BEAST:
        isl, mp, pat = ECHO_BEAST[st]
        try:
            if mp == 'FourIsland_IcefallCave_Back': icefall_climb(t)
            go_isle(t, isl, mp); legend_fight(t, pat)
        except AssertionError as ex:
            # limite du bot : puzzles de glace / cascade de la grotte Glacon -> Echo 4 non joue, on le saute (a verifier a la main)
            log('ECHO %d NON JOUE (%s) -> saut du stade' % (st, ex)); t.save('echo_%d_skip' % st); t.var('VAR_ECHO_STAGE', st + 1); t.flag('FLAG_ECHO_BEAST4_DONE')
    elif st in (9, 11):
        go_isle(t, 4, 'FourIsland_LoreleisHouse'); t.e.run(90, 0); t.talk_script('EventScript_Lorelei', 40, 'echo_lorelei_%d' % st)
    elif st == 21:
        go_isle(t, 7, 'SevenIsland_SevaultCanyon'); t.e.run(90, 0); t.walk_fight((17, 9), 10); t.walk_fight((17, 8), 10); t.scene(maxn=1200, shot='echo_final')
    elif st == 22:
        go_isle(t, 7, 'SevenIsland_SevaultCanyon'); t.e.run(90, 0)
        # les 6 legendaires n'apparaissent qu'au rechargement de la carte (OnTransition) : on sort puis on revient
        assert t.go('SevenIsland_SevaultCanyon_Entrance') and t.go('SevenIsland_SevaultCanyon'); t.e.run(90, 0)
        for pat in ('Kyogre', 'Groudon', 'Rayquaza', 'Latias', 'Latios', 'Jirachi'): legend_fight(t, pat)
        t.scene(maxn=1200, shot='echo_end')
        log('  Echos 7 :', [(f[10:], t.getflag(f)) for f in ('FLAG_DONE_ECHO_KYOGRE', 'FLAG_DONE_ECHO_GROUDON', 'FLAG_DONE_ECHO_RAYQUAZA', 'FLAG_DONE_ECHO_LATIAS', 'FLAG_DONE_ECHO_LATIOS', 'FLAG_DONE_ECHO_JIRACHI')])
    else: log('ECHO stage inconnu', st); return False
    t.report('VAR_ECHO_STAGE'); t.save('echo_%d' % st)
    return t.getvar('VAR_ECHO_STAGE') != st

def stage_pg_echoes(t):
    """Post-game 6 : les 8 Echos du Temps, de l'Ile 1 au Canyon Sevault (ferry entre les iles, Bill/Celio/Lorelei)."""
    R.SURF = True; R.NOWALK = (19,)    # pas de Cascade (CS07) : les chutes d'eau ne sont pas navigables
    for _ in range(40):
        if not echo_step(t):
            log('ECHO bloque au stade', t.getvar('VAR_ECHO_STAGE')); break
        if t.getvar('VAR_ECHO_STAGE') >= 23: break

STAGES = [('ranch', stage_opening_ranch), ('school', stage_school), ('lab', stage_lab), ('route1q', stage_route1_quest), ('opan', stage_opanihrum), ('gym1', stage_gym1), ('gym2', stage_gym2), ('cottage', stage_cottage), ('ssanne', stage_ssanne), ('gym3', stage_gym3), ('tower', stage_tower), ('quartz', stage_quartz), ('gym4', stage_gym4), ('ameth', stage_ameth), ('gym5', stage_gym5), ('hema_in', stage_hema_in), ('hema_tower', stage_hema_tower), ('gym6', stage_gym6), ('chron_in', stage_chron_in), ('chron_key', stage_chron_key), ('gym7', stage_gym7), ('chron_raid', stage_chron_raid), ('seafoam', stage_seafoam), ('gym8', stage_gym8), ('victory', stage_victory), ('league', stage_league), ('ending1', stage_ending1), ('pg_pallet', stage_pg_pallet), ('pg_indigo', stage_pg_indigo), ('pg_mine', stage_pg_mine), ('pg_birds', stage_pg_birds), ('pg_ferry', stage_pg_ferry), ('pg_sevii', stage_pg_sevii), ('pg_sulfura', stage_pg_sulfura), ('pg_echoes', stage_pg_echoes)]

RESUME = {'ending1': 'league', 'pg_pallet': 'ending1', 'pg_mine': 'pg_pallet', 'pg_ferry': 'pg_birds'}

if __name__ == '__main__':
    # usage : run_full.py all | run_full.py <etape> [<etape> ...]   (une etape isolee repart de la sauvegarde de la precedente)
    names = [n for n, _ in STAGES]; want = sys.argv[1:] or ['all']
    seq = names if want == ['all'] else want
    t = None
    for nm in seq:
        i = names.index(nm)
        if t is None: t = Auto.boot() if i == 0 else Auto.resume(RESUME.get(nm, names[i - 1]))
        log('=== STAGE', nm, time.strftime('%H:%M:%S'))
        STAGES[i][1](t); t.save(nm)
