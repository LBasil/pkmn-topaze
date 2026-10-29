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
_pool = [('FLAG_0x%X' % i) for i in range(0x300, 0x3D8) if ('FLAG_0x%X' % i) not in _used]
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
