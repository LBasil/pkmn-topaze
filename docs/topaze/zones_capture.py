#!/usr/bin/env python3
"""ZONES DE CAPTURE : la PASSEUSE (2e quai d'Amethiolite) mene a 5 zones sauvages a theme (evolutions, pierres, echanges, fossiles, rares).
Marais des Reflets | Serre des Pierres | Quai des Echanges | Aire des Fossiles | Etang des Cycles. Textes anglais PROVISOIRES. Idempotent."""
import sys, os, re, json, random
sys.path.insert(0, 'docs/topaze')
import newmap as N, route_test as R
rd, wr = N.rd, N.wr
if 'FuchsiaCity_EventScript_TideFerrywoman' in rd('data/maps/FuchsiaCity/scripts.inc'): print('deja applique'); raise SystemExit
SP = rd('include/constants/species.h')
def sp(n): assert re.search(r'#define SPECIES_%s\b' % n, SP), n; return 'SPECIES_' + n
RATE = [20, 20, 10, 10, 10, 10, 5, 5, 4, 4, 1, 1]
def mons(lst, lo, hi):
    return [{'min_level': lo + (i % 3), 'max_level': hi - (2 - i % 3 if hi - lo >= 2 else 0), 'species': sp(n)} for i, n in enumerate(lst)]
Z = [
 dict(k='MARSH', map='ReflectionMarsh', tpl='SixIsland_PatternBush', badge=3, lv=(22, 27), music=None,
      land=['EEVEE', 'RHYHORN', 'PIKACHU', 'TANGELA', 'LICKITUNG', 'PINSIR', 'SCYTHER', 'KANGASKHAN', 'ABRA', 'DITTO', 'HERACROSS', 'CHANSEY'],
      ask='The MARSH OF REFLECTIONS shows what POKéMON could become, or were. Visit?', gate='Come back with 3 BADGES.',
      npcs=[('BUG_CATCHER', 'Everything here looks like another POKéMON, before or after.'), ('LASS', 'I caught an EEVEE here. It would not stop looking at its reflection.')]),
 dict(k='GREENHOUSE', map='StoneGreenhouse', tpl='TwoIsland_CapeBrink', badge=4, lv=(28, 33), music=None,
      land=['GROWLITHE', 'VULPIX', 'ODDISH', 'POLIWHIRL', 'CLEFAIRY', 'JIGGLYPUFF', 'NIDORINA', 'NIDORINO', 'SHELLDER', 'STARYU', 'EXEGGCUTE', 'EEVEE'],
      ask='The STONE GREENHOUSE grows POKéMON that wait for a stone. Visit?', gate='Come back with 4 BADGES.',
      npcs=[('WOMAN_1', 'Each stone has a POKéMON that waits for it.')]),
 dict(k='DOCK', map='TradeDock', tpl='ThreeIsland_BondBridge', badge=5, lv=(32, 37), music=None,
      land=['KADABRA', 'MACHOKE', 'GRAVELER', 'HAUNTER', 'ONIX', 'SEADRA', 'SLOWPOKE', 'SCYTHER', 'PORYGON', 'ELECTABUZZ', 'MAGMAR', 'DRAGONAIR'],
      water=['SEADRA', 'POLIWHIRL', 'SLOWPOKE', 'HORSEA', 'KINGLER'], fish=['MAGIKARP', 'HORSEA', 'POLIWAG', 'SEADRA', 'POLIWHIRL', 'KINGLER', 'SLOWPOKE', 'LAPRAS', 'DRAGONAIR', 'DRATINI'],
      ask='The TRADE DOCK, where POKéMON that evolve by trade wait on the pier. Visit?', gate='Come back with 5 BADGES.',
      npcs=[('SAILOR', 'Some POKéMON only change when traded. Here they arrive already changed.'), ('OLD_MAN_1', 'Three birds, three beasts and a dreamer sleep in this world. Listen to the wind and the water.')]),
 dict(k='DIG', map='FossilDig', tpl='SixIsland_RuinValley', badge=6, lv=(36, 41), music=None,
      land=['GEODUDE', 'ONIX', 'RHYHORN', 'CUBONE', 'SANDSLASH', 'DUGTRIO', 'MAROWAK', 'GOLEM', 'NOSEPASS', 'LARVITAR', 'ARON', 'AERODACTYL'],
      ask='The FOSSIL DIG: five fossils sleep in the sand. Visit?', gate='Come back with 6 BADGES.',
      npcs=[('HIKER', 'Brush the sand with care. A fossil waits under the five spots that shine.')]),
 dict(k='POND', map='CyclePond', tpl='SixIsland_WaterPath', badge=7, lv=(40, 46), music=None,
      land=['PSYDUCK', 'POLIWHIRL', 'WOOPER', 'MARILL', 'LOTAD', 'SURSKIT', 'SLOWPOKE', 'LOMBRE', 'GOLDEEN', 'SEAKING', 'SLOWBRO', 'AZUMARILL'],
      water=['PSYDUCK', 'GOLDEEN', 'POLIWAG', 'WAILMER', 'LAPRAS'], fish=['MAGIKARP', 'BARBOACH', 'HORSEA', 'CORSOLA', 'WAILMER', 'SEADRA', 'STARYU', 'DRATINI', 'FEEBAS', 'LAPRAS'],
      ask='The POND OF CYCLES: water, patience and rare catches. Visit?', gate='Come back with 7 BADGES.',
      npcs=[('FISHER', 'The rarest fish bite when nobody is watching. FEEBAS likes the quiet water.')]),
]
FISHR = [70, 30, 60, 20, 20, 40, 40, 15, 4, 1]; WATR = [60, 30, 5, 4, 1]
# ---------------- helpers
def comp(nav):
    seen = set(); best = []
    for y in range(nav.h):
        for x in range(nav.w):
            c = (x, y)
            if c in seen or nav.blocked(x, y): continue
            comp_ = [c]; seen.add(c); st = [c]
            while st:
                u = st.pop()
                for dx, dy in ((0, 1), (0, -1), (1, 0), (-1, 0)):
                    q = (u[0] + dx, u[1] + dy)
                    if q in seen or nav.blocked(*q) or not nav.step_ok(u, q): continue
                    seen.add(q); comp_.append(q); st.append(q)
            if len(comp_) > len(best): best = comp_
    return best
def okc(nav, c, taken, margin):
    x, y = c
    if nav.blocked(x, y) or c in nav.warps or any(abs(x - t[0]) + abs(y - t[1]) <= margin for t in taken): return False
    return all(not nav.blocked(x + dx, y + dy) for dx, dy in ((0, 1), (0, -1), (1, 0), (-1, 0)))
def near(nav, cells, pref, taken, margin=2):
    for c in sorted(cells, key=lambda c: abs(c[0] - pref[0]) + abs(c[1] - pref[1])):
        if okc(nav, c, taken, margin): return c
    raise SystemExit('pas de place pres de %s' % (pref,))
EL = lambda nav, c: (nav.g[c[1] * nav.w + c[0]] >> 12) or 3
# ---------------- passeuse
FERRY = 'FuchsiaCity_EventScript_TideFerrywoman'; FT = 'FuchsiaCity_Text_Tide'
fn = R.Nav('FuchsiaCity'); fj = json.load(open('data/maps/FuchsiaCity/map.json'))
fo = [(o['x'], o['y']) for o in fj['object_events']]
fp = near(fn, [(x, y) for y in range(fn.h) for x in range(fn.w)], (21, 26), fo + list(fn.warps), margin=2)
fj['object_events'].append(N.obj('WOMAN_2', fp[0], fp[1], FERRY, el=EL(fn, fp))); N.jdump(fj, 'data/maps/FuchsiaCity/map.json')
fx, fy = 24, 27
# ---------------- zones
WE = json.load(open('src/data/wild_encounters.json')); grp = WE['wild_encounter_groups'][0]['encounters']
entry = {}
for z in Z:
    k, mn, tpl = z['k'], z['map'], z['tpl']
    N.clone(mn, tpl, objects=[], warps=[], scripts='', txt='')
    nav = R.Nav(mn); cells = comp(nav); cs = set(cells)
    a = near(nav, cells, (nav.w // 2, int(nav.h * .75)), [], margin=0); entry[k] = (a[0], a[1])
    sc = ''; tx = ''; objs = []; taken = [a]
    def place(gfx, pref, script, margin=2):
        c = near(nav, cells, pref, taken, margin); taken.append(c); objs.append(N.obj(gfx, c[0], c[1], script, el=EL(nav, c))); return c
    # retour
    place('SAILOR', (a[0] + 2, a[1]), '%s_EventScript_ReturnFerry' % mn, 1)
    sc += ('%s_EventScript_ReturnFerry::\n\tlock\n\tfaceplayer\n\tmsgbox %s_Text_ReturnAsk, MSGBOX_YESNO\n\tgoto_if_eq VAR_RESULT, NO, %s_EventScript_Stay\n\twarp MAP_FUCHSIA_CITY, 255, %d, %d\n\twaitstate\n\tend\n\n%s_EventScript_Stay::\n\tmsgbox %s_Text_Stay\n\trelease\n\tend\n\n') % (mn, mn, mn, fx, fy, mn, mn)
    tx += N.text(mn + '_Text_ReturnAsk', 'Ready to go back to the dock?') + N.text(mn + '_Text_Stay', 'Take your time. The tide can wait.')
    pk = [a[0], a[1]]; far = lambda d: (a[0] + d * (1 if (d // 3) % 2 == 0 else -1), a[1] - abs(d))
    for j, (gfx, line) in enumerate(z['npcs']):
        S_, T_ = '%s_EventScript_Npc%d' % (mn, j), '%s_Text_Npc%d' % (mn, j)
        place(gfx, far(4 + 3 * j), S_); sc += '%s::\n\tmsgbox %s, MSGBOX_NPC\n\tend\n\n' % (S_, T_); tx += N.text(T_, line)
    # --- specifique
    if k == 'MARSH':   # radar de rares
        place('MAN', far(8), mn + '_EventScript_Radar')
        sc += ('%s_EventScript_Radar::\n\tlock\n\tfaceplayer\n\tmsgbox %s_Text_Radar0\n\trandom 3\n\tgoto_if_eq VAR_RESULT, 0, %s_EventScript_R1\n\tgoto_if_eq VAR_RESULT, 1, %s_EventScript_R2\n\tmsgbox %s_Text_Radar3\n\trelease\n\tend\n\n'
               '%s_EventScript_R1::\n\tmsgbox %s_Text_Radar1\n\trelease\n\tend\n\n%s_EventScript_R2::\n\tmsgbox %s_Text_Radar2\n\trelease\n\tend\n\n').replace('%s', mn)
        tx += N.text(mn + '_Text_Radar0', 'I track rare POKéMON. Today my radar says...') + N.text(mn + '_Text_Radar1', 'FEEBAS bites in the quiet water of the POND OF CYCLES, by fishing.') + N.text(mn + '_Text_Radar2', 'AERODACTYL is sighted in the FOSSIL DIG, among the rocks.') + N.text(mn + '_Text_Radar3', 'DRATINI hides under the water of the POND and the TRADE DOCK.')
    if k == 'GREENHOUSE':   # marchand de pierres
        place('FAT_MAN', far(8), mn + '_EventScript_Merchant')
        sc += ('%s_EventScript_Merchant::\n\tlock\n\tfaceplayer\n\tmsgbox %s_Text_Merchant\n\tpokemart %s_Stock\n\tmsgbox %s_Text_Bye\n\trelease\n\tend\n\n\t.align 2\n%s_Stock::\n').replace('%s', mn)
        sc += ''.join('\t.2byte ITEM_%s\n' % i for i in ['FIRE_STONE', 'WATER_STONE', 'THUNDER_STONE', 'LEAF_STONE', 'MOON_STONE', 'SUN_STONE', 'DRAGON_SCALE', 'UP_GRADE', 'METAL_COAT', 'KINGS_ROCK', 'DEEP_SEA_TOOTH', 'DEEP_SEA_SCALE', 'LINK_CABLE', 'ITEM_NONE'][:-1]) + '\t.2byte ITEM_NONE\n\n'
        tx += N.text(mn + '_Text_Merchant', 'Evolution items, all in one place. What do you need?') + N.text(mn + '_Text_Bye', 'May your POKéMON become what they dream of.')
    if k == 'DOCK':    # indices legendaires
        place('OLD_WOMAN', far(8), mn + '_EventScript_Sage')
        sc += ('%s_EventScript_Sage::\n\tlock\n\tfaceplayer\n\tmsgbox %s_Text_Sage0\n\trandom 3\n\tgoto_if_eq VAR_RESULT, 0, %s_EventScript_S1\n\tgoto_if_eq VAR_RESULT, 1, %s_EventScript_S2\n\tmsgbox %s_Text_Sage3\n\trelease\n\tend\n\n'
               '%s_EventScript_S1::\n\tmsgbox %s_Text_Sage1\n\trelease\n\tend\n\n%s_EventScript_S2::\n\tmsgbox %s_Text_Sage2\n\trelease\n\tend\n\n').replace('%s', mn)
        tx += N.text(mn + '_Text_Sage0', 'I read the winds. Listen.') + N.text(mn + '_Text_Sage1', 'The bird of ice sleeps where frozen water falls.') + N.text(mn + '_Text_Sage2', 'The bird of lightning waits where the lamps went out.') + N.text(mn + '_Text_Sage3', 'The bird of fire dreams in the mountain that never sleeps.')
    bgs = []
    if k == 'DIG':     # fossiles + fantomes
        items = ['OLD_AMBER', 'HELIX_FOSSIL', 'DOME_FOSSIL', 'ROOT_FOSSIL', 'CLAW_FOSSIL']
        spots = []
        for i, it in enumerate(items):
            c = near(nav, cells, (a[0] + (i - 2) * 6, a[1] - 5 - 4 * (i % 3)), taken + spots, margin=3); spots.append(c); taken.append(c)
            bgs.append({'type': 'hidden_item', 'x': c[0], 'y': c[1], 'elevation': 0, 'item': 'ITEM_' + it, 'flag': 'FLAG_TOPAZE_FOSSIL_%d' % (i + 1), 'quantity': 1, 'underfoot': False})
        G = [('LARVITAR', 25, 'a LARVITAR'), ('DRATINI', 25, 'a DRATINI'), ('BAGON', 25, 'a BAGON'), ('BELDUM', 25, 'a BELDUM')]
        for i, (spn, lvl, nm) in enumerate(G):
            S_ = '%s_EventScript_Ghost%d' % (mn, i + 1); T_ = '%s_Text_Ghost%d' % (mn, i + 1); F = 'FLAG_TOPAZE_GHOST_%d' % (i + 1)
            place('BOY' if False else 'MAN', (a[0] + (i - 2) * 5, a[1] - 14), S_)
            sc += ('%s::\n\tlock\n\tfaceplayer\n\tgoto_if_set %s, %s_Done\n\tmsgbox %s_Offer, MSGBOX_YESNO\n\tgoto_if_eq VAR_RESULT, NO, %s_No\n\tgivemon %s, %d\n\tgoto_if_eq VAR_RESULT, 2, EventScript_NoMoreRoomForPokemon\n\tsetflag %s\n\tmsgbox %s_Got\n\trelease\n\tend\n\n'
                   '%s_Done::\n\tmsgbox %s_After\n\trelease\n\tend\n\n%s_No::\n\tmsgbox %s_Refuse\n\trelease\n\tend\n\n') % (S_, F, S_, T_, S_, sp(spn), lvl, F, T_, S_, T_, S_, T_)
            tx += N.text(T_ + '_Offer', 'A ghost left this egg-shaped dream behind. Take care of %s?' % nm) + N.text(T_ + '_Got', 'Take good care of it.') + N.text(T_ + '_After', 'It was a good home, in the end.') + N.text(T_ + '_Refuse', 'Then I will wait a little longer.')
    if k == 'POND':    # spa du lien + pierre eternelle
        place('WOMAN_3', far(8), mn + '_EventScript_Spa')
        sc += ('%s_EventScript_Spa::\n\tlock\n\tfaceplayer\n\tmsgbox %s_Text_SpaOffer, MSGBOX_YESNO\n\tgoto_if_eq VAR_RESULT, NO, %s_EventScript_SpaNo\n\tcheckmoney 2000\n\tgoto_if_eq VAR_RESULT, FALSE, %s_EventScript_SpaPoor\n'
               '\tmsgbox %s_Text_SpaWhich\n\tspecial ChoosePartyMon\n\twaitstate\n\tlock\n\tfaceplayer\n\tgoto_if_ge VAR_0x8004, PARTY_SIZE, %s_EventScript_SpaNo\n\tspecialvar VAR_RESULT, GetPartyMonSpecies\n\tgoto_if_eq VAR_RESULT, SPECIES_EGG, %s_EventScript_SpaNo\n'
               '\tremovemoney 2000\n\tclosemessage\n\tfadescreen FADE_TO_BLACK\n\tplayfanfare MUS_HEAL\n\twaitfanfare\n\tspecial TopazeBondMax\n\tsetflag FLAG_TOPAZE_BOND\n\tfadescreen FADE_FROM_BLACK\n\tspecial BufferMonNickname\n\tmsgbox %s_Text_SpaDone\n\trelease\n\tend\n\n'
               '%s_EventScript_SpaNo::\n\tmsgbox %s_Text_SpaNo\n\trelease\n\tend\n\n%s_EventScript_SpaPoor::\n\tmsgbox %s_Text_SpaPoor\n\trelease\n\tend\n\n').replace('%s', mn)
        tx += (N.text(mn + '_Text_SpaOffer', 'A bond treatment for 2000 turns a POKéMON into your best friend. Interested?') + N.text(mn + '_Text_SpaWhich', 'Which POKéMON needs the treatment?') + N.text(mn + '_Text_SpaDone', 'Wonderful! @ adores you now. Evolutions that need bonds will follow.').replace('@', '{STR_VAR_1}') +
               N.text(mn + '_Text_SpaNo', 'Another time, then.') + N.text(mn + '_Text_SpaPoor', 'The treatment costs 2000. Come back with enough.'))
        place('OLD_MAN_1', far(11), mn + '_EventScript_Hermit')
        sc += ('%s_EventScript_Hermit::\n\tlock\n\tfaceplayer\n\tgoto_if_set FLAG_TOPAZE_EVERSTONE, %s_EventScript_HermitDone\n\tmsgbox %s_Text_Hermit\n\tcheckitemspace ITEM_EVERSTONE, 1\n\tgoto_if_eq VAR_RESULT, FALSE, %s_EventScript_HermitFull\n\tgiveitem ITEM_EVERSTONE\n\tsetflag FLAG_TOPAZE_EVERSTONE\n\trelease\n\tend\n\n'
               '%s_EventScript_HermitDone::\n\tmsgbox %s_Text_HermitDone\n\trelease\n\tend\n\n%s_EventScript_HermitFull::\n\tmsgbox %s_Text_HermitFull\n\trelease\n\tend\n\n').replace('%s', mn)
        tx += N.text(mn + '_Text_Hermit', 'Some POKéMON should never evolve. This stone will keep them as they are. Take it.') + N.text(mn + '_Text_HermitDone', 'Hold it, and nothing changes. That is the point.') + N.text(mn + '_Text_HermitFull', 'Your BAG is full.')
    N.rewrite(mn, objs, sc, tx, bgs=bgs)
    # --- sauvages : FireRed + LeafGreen
    ent = {'land_mons': {'encounter_rate': 20, 'mons': mons(z['land'], *z['lv'])}}
    if z.get('water'): ent['water_mons'] = {'encounter_rate': 4, 'mons': mons(z['water'], z['lv'][0], z['lv'][1])}
    if z.get('fish'):
        fm = []; lo, hi = z['lv']
        for i, n in enumerate(z['fish']): fm.append({'min_level': 5 if i < 2 else (lo if i < 5 else lo + 2), 'max_level': 10 if i < 2 else (lo + 3 if i < 5 else hi), 'species': sp(n)})
        ent['fishing_mons'] = {'encounter_rate': 20, 'mons': fm}
    for ver in ('FireRed', 'LeafGreen'):
        e = {'map': N.mapid(mn), 'base_label': 's%s_%s' % (mn, ver)}; e.update(json.loads(json.dumps(ent))); grp.append(e)
    print(k, mn, 'arrivee', entry[k], 'cells', len(cells))
N.jdump(WE, 'src/data/wild_encounters.json')
# ---------------- passeuse : script + textes
sc = '%s::\n\tlock\n\tfaceplayer\n\tgoto_if_unset FLAG_TOPAZE_CLOCK_DONE, %s_EventScript_Closed\n\tmsgbox %s_Hello\n' % (FERRY, FERRY, FT)
tx = N.text(FT + '_Hello', 'I row to places where POKéMON gather to become something else, {PLAYER}.') + N.text(FT + '_Closed', 'The tide is not ready. Come back once the clocks make sense.') + N.text(FT + '_Never', 'Another time, then. The tide can wait.')
for i, z in enumerate(Z):
    nxt = '%s_EventScript_Dest%d' % (FERRY, i + 1) if i < len(Z) - 1 else '%s_EventScript_End' % FERRY
    sc += ('%s_EventScript_Dest%d::\n' % (FERRY, i) if i else '') + '\tgoto_if_unset FLAG_BADGE0%d_GET, %s_EventScript_Gate%d\n\tmsgbox %s_Ask%d, MSGBOX_YESNO\n\tgoto_if_eq VAR_RESULT, NO, %s\n\tsetdynamicwarp MAP_FUCHSIA_CITY, 255, %d, %d\n' % (z['badge'], FERRY, i, FT, i, nxt, fx, fy)
    sc += '\twarp %s, 255, %d, %d\n\twaitstate\n\tend\n%s_EventScript_Gate%d::\n\tmsgbox %s_GateText%d\n\tgoto %s\n' % (N.mapid(z['map']), entry[z['k']][0], entry[z['k']][1], FERRY, i, FT, i, nxt)
    tx += N.text('%s_Ask%d' % (FT, i), z['ask']) + N.text('%s_GateText%d' % (FT, i), z['gate'])
sc += '%s_EventScript_End::\n\tmsgbox %s_Never\n\trelease\n\tend\n\n%s_EventScript_Closed::\n\tmsgbox %s_Closed\n\trelease\n\tend\n' % (FERRY, FT, FERRY, FT)
open('data/maps/FuchsiaCity/scripts.inc', 'a').write('\n@ Topaze: la PASSEUSE (zones de capture)\n' + sc); open('data/maps/FuchsiaCity/text.inc', 'a').write(tx)
# ---------------- journal
g = rd('docs/topaze/journal_gen.py')
if 'FLAG_TOPAZE_FOSSIL_5' not in g:
    i = g.index('assert len(SECTIONS) <= 12')
    L = ['# ---- ZONES DE CAPTURE (la passeuse)',
         'add("SIDE QUESTS", F, "FLAG_TOPAZE_FOSSIL_5", 0, "THE FOSSIL DIG", "Ferry from AMETHIOLITE. Dig the\\\\n5 shining spots in the sand.", FL("FLAG_TOPAZE_CLOCK_DONE"))',
         'add("SIDE QUESTS", F, "FLAG_TOPAZE_GHOST_4", 0, "THE GHOST EGGS", "FOSSIL DIG: 4 ghosts leave a rare\\\\nPOKéMON each.", FL("FLAG_TOPAZE_CLOCK_DONE"))',
         'add("SIDE QUESTS", F, "FLAG_TOPAZE_BOND", 0, "THE BOND TREATMENT", "CYCLE POND: a treatment for\\\\nbond evolutions.", FL("FLAG_TOPAZE_CLOCK_DONE"))',
         'add("SIDE QUESTS", F, "FLAG_TOPAZE_EVERSTONE", 0, "THE FORBIDDEN EVOLUTION", "CYCLE POND hermit keeps a stone.\\\\nPOKéMON that never evolve.", FL("FLAG_TOPAZE_CLOCK_DONE"))']
    wr('docs/topaze/journal_gen.py', g[:i] + '\n'.join(L) + '\n\n' + g[i:])
