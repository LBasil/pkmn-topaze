"""Bibliotheque commune des generateurs de zones (placement atteignable, drapeaux libres, passeurs)."""
import sys, re, json
sys.path.insert(0, 'docs/topaze')
import newmap as N, route_test as R
rd, wr = N.rd, N.wr
SP, IT = rd('include/constants/species.h'), rd('include/constants/items.h')
def sp(n): assert re.search(r'#define SPECIES_%s\b' % n, SP), n; return 'SPECIES_' + n
def it(n): assert re.search(r'#define ITEM_%s\b' % n, IT), n; return 'ITEM_' + n
_fl = rd('include/constants/flags.h')
_used = set(re.findall(r'FLAG_0x[0-9A-F]+', ''.join(l for l in _fl.split('\n') if not re.match(r'#define FLAG_0x[0-9A-F]+\s+0x', l))))
_pool = [('FLAG_0x%X' % i) for i in list(range(0x300, 0x3D8)) + list(range(0x4CF, 0x500)) + list(range(0x220, 0x230)) if ('FLAG_0x%X' % i) not in _used]
_pool += ['FLAG_HIDDEN_ITEM_UNUSED_%s' % h for h in ('0x07','0x10','0x28','0x2B','0x2C','0x2D','0x2E','0x7C') if re.search(r'FLAG_HIDDEN_ITEM_UNUSED_%s\b' % h, _fl)]
_new = []
def flag(name):
    a = _pool.pop(0); _new.append('#define FLAG_TOPAZE_%s %s\n' % (name, a)); return 'FLAG_TOPAZE_' + name
def flush_flags():
    f = rd('include/constants/flags.h'); wr('include/constants/flags.h', f.replace('#endif // GUARD_CONSTANTS_FLAGS_H', ''.join(_new) + '\n#endif // GUARD_CONSTANTS_FLAGS_H')); print('flags utilises:', len(_new), 'restants:', len(_pool))
def comp(nav):
    seen = set(); best = []
    for y in range(nav.h):
        for x in range(nav.w):
            c = (x, y)
            if c in seen or nav.blocked(x, y): continue
            cc = [c]; seen.add(c); st = [c]
            while st:
                u = st.pop()
                for dx, dy in ((0, 1), (0, -1), (1, 0), (-1, 0)):
                    q = (u[0] + dx, u[1] + dy)
                    if q in seen or nav.blocked(*q) or not nav.step_ok(u, q): continue
                    seen.add(q); cc.append(q); st.append(q)
            if len(cc) > len(best): best = cc
    return best
def okc(nav, c, taken, margin):
    x, y = c
    if nav.blocked(x, y) or c in nav.warps or any(abs(x - t[0]) + abs(y - t[1]) <= margin for t in taken): return False
    return all(not nav.blocked(x + dx, y + dy) for dx, dy in ((0, 1), (0, -1), (1, 0), (-1, 0)))
def near(nav, cells, pref, taken, margin=2):
    for mg in (margin, 0):
        for c in sorted(cells, key=lambda c: abs(c[0] - pref[0]) + abs(c[1] - pref[1])):
            if okc(nav, c, taken, mg): return c
    raise SystemExit('pas de place pres de %s' % (pref,))
EL = lambda nav, c: (nav.g[c[1] * nav.w + c[0]] >> 12) or 3
def ferry(name, gfx, pref, hello, closed, never, dests, fx=24, fy=27):
    """dests : [(map, (x,y), gate_badge|0, ask, gatetxt)] ; ajoute un PNJ passeur sur FuchsiaCity + script/texte."""
    S = 'FuchsiaCity_EventScript_' + name; T = 'FuchsiaCity_Text_' + name
    fn = R.Nav('FuchsiaCity'); fj = json.load(open('data/maps/FuchsiaCity/map.json')); fo = [(o['x'], o['y']) for o in fj['object_events']]
    fp = near(fn, [(x, y) for y in range(fn.h) for x in range(fn.w)], pref, fo + list(fn.warps), margin=2)
    fj['object_events'].append(N.obj(gfx, fp[0], fp[1], S, el=EL(fn, fp))); N.jdump(fj, 'data/maps/FuchsiaCity/map.json')
    sc = '%s::\n\tlock\n\tfaceplayer\n\tgoto_if_unset FLAG_TOPAZE_CLOCK_DONE, %s_EventScript_Closed\n\tmsgbox %s_Hello\n' % (S, S, T)
    tx = N.text(T + '_Hello', hello) + N.text(T + '_Closed', closed) + N.text(T + '_Never', never)
    for i, (m, a, gate, ask, gt) in enumerate(dests):
        nxt = '%s_EventScript_Dest%d' % (S, i + 1) if i < len(dests) - 1 else S + '_EventScript_End'
        sc += ('%s_EventScript_Dest%d::\n' % (S, i) if i else '')
        if gate: sc += '\tgoto_if_unset FLAG_BADGE0%d_GET, %s_EventScript_Gate%d\n' % (gate, S, i)
        sc += '\tmsgbox %s_Ask%d, MSGBOX_YESNO\n\tgoto_if_eq VAR_RESULT, NO, %s\n\tsetdynamicwarp MAP_FUCHSIA_CITY, 255, %d, %d\n\twarp %s, 255, %d, %d\n\twaitstate\n\tend\n' % (T, i, nxt, fx, fy, N.mapid(m), a[0], a[1])
        if gate: sc += '%s_EventScript_Gate%d::\n\tmsgbox %s_GateText%d\n\tgoto %s\n' % (S, i, T, i, nxt); tx += N.text('%s_GateText%d' % (T, i), gt)
        tx += N.text('%s_Ask%d' % (T, i), ask)
    sc += '%s_EventScript_End::\n\tmsgbox %s_Never\n\trelease\n\tend\n\n%s_EventScript_Closed::\n\tmsgbox %s_Closed\n\trelease\n\tend\n' % (S, T, S, T)
    open('data/maps/FuchsiaCity/scripts.inc', 'a').write('\n@ Topaze: passeur %s\n' % name + sc); open('data/maps/FuchsiaCity/text.inc', 'a').write(tx)
def journal_add(lines):
    g = rd('docs/topaze/journal_gen.py'); i = g.index('assert len(SECTIONS) <= 12'); wr('docs/topaze/journal_gen.py', g[:i] + '\n'.join(lines) + '\n\n' + g[i:])
def jl(sec, flg, name, hint, vis='FL("FLAG_TOPAZE_CLOCK_DONE")'):
    return 'add("%s", F, "%s", 0, "%s", "%s", %s)' % (sec, flg, name, hint.replace('\n', '\\\\n'), vis)

def _mons(lst, lo, hi): return [{'min_level': lo + (i % 3), 'max_level': max(lo + 1, hi - (2 - i % 3)), 'species': sp(n)} for i, n in enumerate(lst)]
def make_zone(z, WE_group, journal, fx=24, fy=27):
    """z : dict(map,tpl,lv,land,[water],[fish],npcs[(gfx,text)],hidden[item],quests[...],gifts[...])  -> clone + PNJ + objets caches + sauvages. Retourne l'arrivee."""
    mn, tpl = z['map'], z['tpl']; k = mn.upper()
    N.clone(mn, tpl, objects=[], warps=[], scripts='', txt=''); nav = R.Nav(mn); cells = comp(nav)
    a = near(nav, cells, (nav.w // 2, int(nav.h * .75)), [], margin=0)
    sc = ''; tx = ''; objs = []; bgs = []; taken = [a]
    def place(gfx, pref, script, margin=2):
        c = near(nav, cells, pref, taken, margin); taken.append(c); objs.append(N.obj(gfx, c[0], c[1], script, el=EL(nav, c))); return c
    off = lambda d: (a[0] + d * (1 if (d // 3) % 2 == 0 else -1), a[1] - abs(d))
    place('SAILOR', (a[0] + 2, a[1]), mn + '_EventScript_ReturnFerry', 1)
    sc += ('%s_EventScript_ReturnFerry::\n\tlock\n\tfaceplayer\n\tmsgbox %s_Text_ReturnAsk, MSGBOX_YESNO\n\tgoto_if_eq VAR_RESULT, NO, %s_EventScript_Stay\n\twarp MAP_FUCHSIA_CITY, 255, %d, %d\n\twaitstate\n\tend\n\n%s_EventScript_Stay::\n\tmsgbox %s_Text_Stay\n\trelease\n\tend\n\n') % (mn, mn, mn, fx, fy, mn, mn)
    tx += N.text(mn + '_Text_ReturnAsk', 'Ready to go back to the dock?') + N.text(mn + '_Text_Stay', 'Take your time. The tide can wait.')
    d = 3
    for j, (gfx, line) in enumerate(z['npcs']):
        S_, T_ = '%s_EventScript_Npc%d' % (mn, j), '%s_Text_Npc%d' % (mn, j)
        place(gfx, off(d), S_); d += 3; sc += '%s::\n\tmsgbox %s, MSGBOX_NPC\n\tend\n\n' % (S_, T_); tx += N.text(T_, line)
    for j, q in enumerate(z.get('quests', [])):
        F = flag('QUEST_%s' % k); S_, T_ = '%s_EventScript_Quest%d' % (mn, j), '%s_Text_Quest%d' % (mn, j); W, R_ = q['want'], q['rew']
        place(q['g'], off(d), S_); d += 3
        sc += ('%s::\n\tlock\n\tfaceplayer\n\tgoto_if_set %s, %s_After\n\tmsgbox %s_Ask\n\tcheckitem %s, %d\n\tgoto_if_eq VAR_RESULT, FALSE, %s_Miss\n\tcheckitemspace %s, %d\n\tgoto_if_eq VAR_RESULT, FALSE, %s_NoRoom\n'
               '\tremoveitem %s, %d\n\tgiveitem %s, %d\n\tsetflag %s\n\tmsgbox %s_Done\n\trelease\n\tend\n\n%s_After::\n\tmsgbox %s_AfterT\n\trelease\n\tend\n\n%s_Miss::\n\tmsgbox %s_MissT\n\trelease\n\tend\n\n%s_NoRoom::\n\tmsgbox %s_NoRoomT\n\trelease\n\tend\n\n') % (
            S_, F, S_, T_, it(W[0]), W[1], S_, it(R_[0]), R_[1], S_, it(W[0]), W[1], it(R_[0]), R_[1], F, T_, S_, T_, S_, T_, S_, T_)
        tx += N.text(T_ + '_Ask', q['ask']) + N.text(T_ + '_Done', q['done']) + N.text(T_ + '_AfterT', q['after']) + N.text(T_ + '_MissT', q['miss']) + N.text(T_ + '_NoRoomT', 'Your BAG is full. Make room, then come back.')
        journal.append(jl('SIDE QUESTS', F, q['j'][0], q['j'][1]))
    for j, (spn, lvl, line) in enumerate(z.get('gifts', [])):
        F = flag('GIFT_%s' % k); S_, T_ = '%s_EventScript_Gift%d' % (mn, j), '%s_Text_Gift%d' % (mn, j)
        place('LITTLE_GIRL', off(d), S_); d += 3
        sc += ('%s::\n\tlock\n\tfaceplayer\n\tgoto_if_set %s, %s_Done\n\tmsgbox %s_Offer, MSGBOX_YESNO\n\tgoto_if_eq VAR_RESULT, NO, %s_No\n\tgivemon %s, %d\n\tgoto_if_eq VAR_RESULT, 2, EventScript_NoMoreRoomForPokemon\n\tsetflag %s\n\tmsgbox %s_Got\n\trelease\n\tend\n\n'
               '%s_Done::\n\tmsgbox %s_After\n\trelease\n\tend\n\n%s_No::\n\tmsgbox %s_Refuse\n\trelease\n\tend\n\n') % (S_, F, S_, T_, S_, sp(spn), lvl, F, T_, S_, T_, S_, T_)
        tx += N.text(T_ + '_Offer', line) + N.text(T_ + '_Got', 'Please look after it.') + N.text(T_ + '_After', 'I hope it is happy with you.') + N.text(T_ + '_Refuse', 'Then I will keep it a little longer.')
        journal.append(jl('SIDE QUESTS', F, z.get('gift_name', 'A GIFT'), z.get('gift_hint', 'A young one awaits.')))
    for i, itn in enumerate(z.get('hidden', [])):
        F = flag('FIND_%s_%d' % (k, i)); c = near(nav, cells, (a[0] + (i - len(z['hidden']) // 2) * 4, a[1] - 4 - 3 * (i % 4)), taken, margin=3); taken.append(c)
        bgs.append({'type': 'hidden_item', 'x': c[0], 'y': c[1], 'elevation': 0, 'item': it(itn), 'flag': F, 'quantity': 1, 'underfoot': False})
    N.rewrite(mn, objs, sc, tx, bgs=bgs)
    ent = {'land_mons': {'encounter_rate': 20, 'mons': _mons(z['land'], *z['lv'])}}
    if z.get('water'): ent['water_mons'] = {'encounter_rate': 4, 'mons': _mons(z['water'], *z['lv'])}
    if z.get('fish'):
        lo, hi = z['lv']; ent['fishing_mons'] = {'encounter_rate': 20, 'mons': [{'min_level': 5 if i < 2 else (lo if i < 5 else lo + 2), 'max_level': 10 if i < 2 else (lo + 3 if i < 5 else hi), 'species': sp(n)} for i, n in enumerate(z['fish'])]}
    for ver in ('FireRed', 'LeafGreen'):
        e = {'map': N.mapid(mn), 'base_label': 's%s_%s' % (mn, ver)}; e.update(json.loads(json.dumps(ent))); WE_group.append(e)
    print(mn, 'arrivee', a, 'cells', len(cells), 'objs', len(objs), 'hidden', len(bgs)); return a

def route_quest(m, gfx, w, wn, r, rn, name, hint, ask, ok, done, journal, tag='RQ', pref=None):
    """PNJ de quete d'objets pose sur une carte existante (route/ville), zone atteignable, hors lignes de vue de dresseurs."""
    nav = R.Nav(m); d = json.load(open('data/maps/%s/map.json' % m)); cells = comp(nav)
    taken = [(o['x'], o['y']) for o in d['object_events']] + [(b['x'], b['y']) for b in d['bg_events']] + list(nav.warps)
    trainers = [(o['x'], o['y']) for o in d['object_events'] if o.get('trainer_type', 'TRAINER_TYPE_NONE') != 'TRAINER_TYPE_NONE']
    cand = [c for c in cells if not any((c[0] == t[0] and abs(c[1] - t[1]) <= 7) or (c[1] == t[1] and abs(c[0] - t[0]) <= 7) for t in trainers) and 2 <= c[0] < nav.w - 2 and 2 <= c[1] < nav.h - 2
            and all(not nav.blocked(c[0] + dx, c[1] + dy) for dx in (-1, 0, 1) for dy in (-1, 0, 1))]
    c = near(nav, cand, pref or (nav.w // 2 + 5, nav.h // 2 + 2), taken, margin=3)
    F = flag('%s_%s' % (tag, m.upper())); S = '%s_EventScript_%s' % (m, tag); T = '%s_Text_%s' % (m, tag)
    d['object_events'].append(N.obj(gfx, c[0], c[1], S, el=EL(nav, c))); N.jdump(d, 'data/maps/%s/map.json' % m)
    sc = ('\n@ Topaze: quete (%s)\n%s::\n\tlock\n\tfaceplayer\n\tgoto_if_set %s, %s_Done\n\tcheckitem %s, %d\n\tgoto_if_eq VAR_RESULT, FALSE, %s_Ask\n\tcheckitemspace %s, %d\n\tgoto_if_eq VAR_RESULT, FALSE, %s_NoRoom\n'
          '\tremoveitem %s, %d\n\tsetflag %s\n\tmsgbox %s_Ok\n\tgiveitem %s, %d\n\trelease\n\tend\n\n%s_Ask::\n\tmsgbox %s_Ask\n\trelease\n\tend\n\n%s_Done::\n\tmsgbox %s_Done\n\trelease\n\tend\n\n%s_NoRoom::\n\tmsgbox %s_NoRoom\n\trelease\n\tend\n') % (
        name, S, F, S, it(w), wn, S, it(r), rn, S, it(w), wn, F, T, it(r), rn, S, T, S, T, S, T)
    open('data/maps/%s/scripts.inc' % m, 'a').write(sc)
    open('data/maps/%s/text.inc' % m, 'a').write(N.text(T + '_Ask', ask) + N.text(T + '_Ok', ok) + N.text(T + '_Done', done) + N.text(T + '_NoRoom', 'Your BAG is full. Make room, then come back.'))
    journal.append(jl('SIDE QUESTS', F, name, hint, 'A'))
def hidden_on(m, itn, tag, pref=None):
    nav = R.Nav(m); d = json.load(open('data/maps/%s/map.json' % m)); cells = comp(nav)
    taken = [(o['x'], o['y']) for o in d['object_events']] + [(b['x'], b['y']) for b in d['bg_events']] + list(nav.warps)
    c = near(nav, [c for c in cells if 2 <= c[0] < nav.w - 2 and 2 <= c[1] < nav.h - 2], pref or (nav.w // 3, nav.h // 3), taken, margin=4)
    d['bg_events'].append({'type': 'hidden_item', 'x': c[0], 'y': c[1], 'elevation': 0, 'item': it(itn), 'flag': flag('HID_%s_%s' % (tag, m.upper())), 'quantity': 1, 'underfoot': False}); N.jdump(d, 'data/maps/%s/map.json' % m)

def ferry_add(name, m, a, gate, ask, gt=''):
    """Ajoute une destination a un passeur existant (avant 'End')."""
    S = 'FuchsiaCity_EventScript_' + name; T = 'FuchsiaCity_Text_' + name
    fs = rd('data/maps/FuchsiaCity/scripts.inc'); txt = rd('data/maps/FuchsiaCity/text.inc')
    ks = [int(x) for x in re.findall(r'%s_Ask(\d+)::' % re.escape(T), txt)]; k = max(ks) + 1
    old = 'goto_if_eq VAR_RESULT, NO, %s_EventScript_End' % S; idx = fs.rindex(old)       # derniere destination
    fs = fs[:idx] + 'goto_if_eq VAR_RESULT, NO, %s_EventScript_Dest%d' % (S, k) + fs[idx + len(old):]
    blk = '%s_EventScript_Dest%d::\n' % (S, k)
    if gate: blk += '\tgoto_if_unset FLAG_BADGE0%d_GET, %s_EventScript_Gate%d\n' % (gate, S, k)
    blk += '\tmsgbox %s_Ask%d, MSGBOX_YESNO\n\tgoto_if_eq VAR_RESULT, NO, %s_EventScript_End\n\tsetdynamicwarp MAP_FUCHSIA_CITY, 255, 24, 27\n\twarp %s, 255, %d, %d\n\twaitstate\n\tend\n' % (T, k, S, N.mapid(m), a[0], a[1])
    if gate: blk += '%s_EventScript_Gate%d::\n\tmsgbox %s_GateText%d\n\tgoto %s_EventScript_End\n' % (S, k, T, k, S)
    anchor = '%s_EventScript_End::' % S; assert anchor in fs
    fs = fs.replace(anchor, blk + anchor, 1); wr('data/maps/FuchsiaCity/scripts.inc', fs)
    t = N.text('%s_Ask%d' % (T, k), ask) + (N.text('%s_GateText%d' % (T, k), gt) if gate else ''); open('data/maps/FuchsiaCity/text.inc', 'a').write(t)
