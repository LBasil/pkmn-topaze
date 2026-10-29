#!/usr/bin/env python3
"""ZONES EXTRA (lot 3) : le PASSEUR DES LANTERNES (3e quai d'Amethiolite) mene a 5 zones (reserves Hoenn Ouest/Est, prairie de Johto, mine, verger)
et 3 batiments (cafe, bibliotheque des evolutions, boutique du collectionneur). Quetes d'objets, objets caches, cadeaux. Textes anglais PROVISOIRES. Idempotent."""
import sys, os, re, json
sys.path.insert(0, 'docs/topaze')
import newmap as N, route_test as R
rd, wr = N.rd, N.wr
if 'FuchsiaCity_EventScript_LanternBoatman' in rd('data/maps/FuchsiaCity/scripts.inc'): print('deja applique'); raise SystemExit
SP, IT = rd('include/constants/species.h'), rd('include/constants/items.h')
def sp(n): assert re.search(r'#define SPECIES_%s\b' % n, SP), n; return 'SPECIES_' + n
def it(n): assert re.search(r'#define ITEM_%s\b' % n, IT), n; return 'ITEM_' + n
# ---- flags : alias vers les FLAG_0x libres (0x300+)
fl = rd('include/constants/flags.h'); used = set(re.findall(r'(?:FLAG_0x[0-9A-F]+)', ''.join(l for l in fl.split('\n') if not re.match(r'#define FLAG_0x[0-9A-F]+\s+0x', l))))
pool = [('FLAG_0x%X' % i) for i in range(0x300, 0x3D8) if ('FLAG_0x%X' % i) not in used]
NEWFL = []
def flag(name):
    a = pool.pop(0); NEWFL.append('#define FLAG_TOPAZE_%s %s\n' % (name, a)); return 'FLAG_TOPAZE_' + name
FEM = ()
Z = [
 dict(k='HOENNW', map='HoennWestReserve', tpl='OneIsland_KindleRoad', gate=6, lv=(36, 42), kind='out',
      land=['SPINDA', 'ZANGOOSE', 'SEVIPER', 'TORKOAL', 'PLUSLE', 'MINUN', 'VOLBEAT', 'ILLUMISE', 'KECLEON', 'SLAKOTH', 'RALTS', 'ABSOL'],
      ask='The WEST RESERVE, home of POKeMON from a far region. Visit?', gt='Come back with 6 BADGES.',
      npcs=[('MAN', 'These POKeMON came from beyond the sea. They like the dry grass.'), ('LASS', 'I saw an ABSOL on the ridge. It left before I could say hello.')],
      hidden=['HEART_SCALE', 'HEART_SCALE', 'HEART_SCALE', 'TINY_MUSHROOM'],
      quests=[dict(g='OLD_WOMAN', want=('HEART_SCALE', 2), rew=('SOOTHE_BELL', 1), ask='I collect HEART SCALEs. Bring me two and I will trade you something warm.', done='Lovely! Take this SOOTHE BELL.', after='My collection grows.', miss='Two HEART SCALEs, please. Look for shiny spots.', j=('THE SCALE COLLECTOR', 'WEST RESERVE: bring 2 HEART SCALES.'))]),
 dict(k='HOENNE', map='HoennEastReserve', tpl='FiveIsland_MemorialPillar', gate=6, lv=(38, 44), kind='out',
      land=['SPHEAL', 'SNORUNT', 'NUMEL', 'TRAPINCH', 'SURSKIT', 'SHUPPET', 'DUSKULL', 'SABLEYE', 'MAWILE', 'ARON', 'WHISMUR', 'LOTAD'],
      water=['LUVDISC', 'WAILMER', 'CARVANHA', 'CORSOLA', 'CLAMPERL'], fish=['MAGIKARP', 'FEEBAS', 'BARBOACH', 'LUVDISC', 'CARVANHA', 'WAILMER', 'CORSOLA', 'SPHEAL', 'RELICANTH', 'CLAMPERL'],
      ask='The EAST RESERVE: sea and cliffs from a far region. Visit?', gt='Come back with 6 BADGES.',
      npcs=[('FISHER', 'CLAMPERL evolves with the right item and a trade. I only know half the story.'), ('SAILOR', 'LUVDISC and CORSOLA like warm water. RELICANTH hides deep.')],
      hidden=['SHOAL_SALT', 'SHOAL_SHELL', 'PEARL'],
      quests=[dict(g='WOMAN_3', want=('SHOAL_SALT', 1), rew=('BIG_PEARL', 1), ask='Seasalt from the beach! Bring me one SHOAL SALT, I will pay in pearls.', done='Perfect. A BIG PEARL for you.', after='The sea gives, the sea takes.', miss='Not yet. Look along the shore.', j=('THE SALT TRADE', 'EAST RESERVE: bring a SHOAL SALT.'))]),
 dict(k='JOHTO', map='SunriseMeadow', tpl='FiveIsland_Meadow', gate=4, lv=(24, 30), kind='out',
      land=['SENTRET', 'HOOTHOOT', 'LEDYBA', 'SPINARAK', 'MAREEP', 'HOPPIP', 'SUNKERN', 'SNUBBULL', 'TEDDIURSA', 'PHANPY', 'STANTLER', 'MILTANK'],
      water=['PSYDUCK', 'MARILL', 'WOOPER', 'POLIWAG', 'REMORAID'], fish=['MAGIKARP', 'POLIWAG', 'REMORAID', 'MARILL', 'WOOPER', 'CORSOLA', 'KRABBY', 'CHINCHOU', 'QWILFISH', 'LAPRAS'],
      ask='The SUNRISE MEADOW: POKeMON from the other side of the sea. Visit?', gt='Come back with 4 BADGES.',
      npcs=[('BOY' if False else 'LITTLE_BOY', 'The sun comes up here before anywhere else.'), ('WOMAN_1', 'MAREEP and HOPPIP love the morning dew.')],
      hidden=['STAR_PIECE'], gifts=[('TOGEPI', 5, 'A little egg hatched on this meadow. It needs a friend. Will you take it?')],
      quests=[dict(g='FAT_MAN', want=('STAR_PIECE', 1), rew=('LUCKY_EGG', 1), ask='A STAR PIECE glints like the morning. Find me one, I will pay in luck.', done='It shines! Take this LUCKY EGG.', after='The meadow shines brighter today.', miss='No STAR PIECE yet. Try digging in the mine.', j=('THE MORNING STAR', 'SUNRISE MEADOW: bring a STAR PIECE.'))]),
 dict(k='MINE', map='AshenMine', tpl='SevenIsland_SevaultCanyon', gate=7, lv=(38, 44), kind='out',
      land=['ARON', 'NOSEPASS', 'SABLEYE', 'MAWILE', 'LUNATONE', 'SOLROCK', 'WHISMUR', 'TRAPINCH', 'NUMEL', 'BALTOY', 'SHUPPET', 'SNORUNT'],
      ask='The ASHEN MINE: gems, stones, odd POKeMON. Visit?', gt='Come back with 7 BADGES.',
      npcs=[('HIKER', 'Gems hide in the rock. Stones too. Keep your eyes on the shiny spots.')],
      hidden=['STAR_PIECE', 'STAR_PIECE', 'STARDUST', 'STARDUST', 'SUN_STONE', 'MOON_STONE'],
      quests=[dict(g='HIKER', want=('STARDUST', 2), rew=('DRAGON_SCALE', 1), ask='STARDUST! I need two for my collection. I will give you a rare scale.', done='Wonderful! A DRAGON SCALE for you.', after='The mine is generous today.', miss='Two STARDUSTs. Look around the shiny spots.', j=('THE GEM COLLECTOR', 'ASHEN MINE: bring 2 STARDUST.'))]),
 dict(k='ORCHARD', map='BerryOrchard', tpl='ThreeIsland_BerryForest', gate=3, lv=(20, 26), kind='out',
      land=['ODDISH', 'BELLSPROUT', 'PARAS', 'VENONAT', 'SUNKERN', 'HOPPIP', 'LEDYBA', 'SPINARAK', 'PINECO', 'WURMPLE', 'SEEDOT', 'SHROOMISH'],
      ask='The BERRY ORCHARD grows every kind of berry. Visit?', gt='Come back with 3 BADGES.',
      npcs=[('WOMAN_1', 'Berries ripen here all year. Take what you find, but leave the trees.'), ('BUG_CATCHER', 'Bug POKeMON love the orchard. Me too.')],
      hidden=['ORAN_BERRY', 'PECHA_BERRY', 'CHERI_BERRY', 'RAWST_BERRY', 'LUM_BERRY', 'SITRUS_BERRY', 'LEPPA_BERRY', 'PERSIM_BERRY'],
      quests=[dict(g='OLD_MAN_1', want=('LUM_BERRY', 1), rew=('WHITE_HERB', 1), ask='A LUM BERRY cures anything. Bring me one and I will trade you a herb.', done='Fresh as the morning. Take this WHITE HERB.', after='The orchard thanks you.', miss='No LUM BERRY yet. Search the grass.', j=('THE LUM BERRY', 'BERRY ORCHARD: bring a LUM BERRY.'))]),
 dict(k='CAFE', map='DockCafe', tpl='SaffronCity_HomeA', gate=0, lv=None, kind='in',
      ask='The DOCK CAFE: rest, a drink and a chat. Visit?', gt='',
      npcs=[('WOMAN_2', 'Everyone passes through the DOCK CAFE sooner or later.'), ('SAILOR', 'A hot drink fixes any tide.')],
      heal=True, shop=['FRESH_WATER', 'SODA_POP', 'LEMONADE', 'MOOMOO_MILK', 'BERRY_JUICE', 'ENERGY_POWDER', 'HEAL_POWDER', 'REVIVAL_HERB', 'ENERGY_ROOT'], shopname='Barista'),
 dict(k='LIBRARY', map='EvolutionLibrary', tpl='SaffronCity_HomeB', gate=0, lv=None, kind='in',
      ask='The EVOLUTION LIBRARY: every way a POKeMON can change. Visit?', gt='',
      npcs=[('OLD_MAN_1', 'STONES change many: FIRE, WATER, THUNDER, LEAF, MOON and SUN. The GREENHOUSE sells them.'),
            ('WOMAN_3', 'A LINK CABLE works like a trade. KADABRA, MACHOKE, GRAVELER and HAUNTER like it.'),
            ('OLD_WOMAN', 'Some change only with a held item: KING\'S ROCK, METAL COAT, DRAGON SCALE, UP-GRADE.'),
            ('LASS', 'Love changes some: EEVEE, GOLBAT, CHANSEY. The CYCLE POND spa raises the bond.'),
            ('FAT_MAN', 'FEEBAS changes with beauty, not level. Raise its looks with the right food.')]),
 dict(k='SHOP', map='CollectorShop', tpl='SaffronCity_HomeC', gate=0, lv=None, kind='in',
      ask='The COLLECTOR SHOP: little treasures for sale. Visit?', gt='',
      npcs=[('MAN', 'Small things make a big difference in a fight.')],
      shop=['SOFT_SAND', 'SHARP_BEAK', 'POISON_BARB', 'SILVER_POWDER', 'SCOPE_LENS', 'QUICK_CLAW', 'FOCUS_BAND', 'SMOKE_BALL', 'CLEANSE_TAG', 'SOOTHE_BELL'], shopname='Collector'),
]
RATE = [20, 20, 10, 10, 10, 10, 5, 5, 4, 4, 1, 1]
def mons(lst, lo, hi): return [{'min_level': lo + (i % 3), 'max_level': max(lo + 1, hi - (2 - i % 3)), 'species': sp(n)} for i, n in enumerate(lst)]
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
    for c in sorted(cells, key=lambda c: abs(c[0] - pref[0]) + abs(c[1] - pref[1])):
        if okc(nav, c, taken, margin): return c
    for c in sorted(cells, key=lambda c: abs(c[0] - pref[0]) + abs(c[1] - pref[1])):
        if okc(nav, c, taken, 0): return c
    raise SystemExit('pas de place pres de %s' % (pref,))
EL = lambda nav, c: (nav.g[c[1] * nav.w + c[0]] >> 12) or 3
# ---- passeur
FERRY = 'FuchsiaCity_EventScript_LanternBoatman'; FT = 'FuchsiaCity_Text_Lantern'
fn = R.Nav('FuchsiaCity'); fj = json.load(open('data/maps/FuchsiaCity/map.json')); fo = [(o['x'], o['y']) for o in fj['object_events']]
fp = near(fn, [(x, y) for y in range(fn.h) for x in range(fn.w)], (29, 26), fo + list(fn.warps), margin=2)
fj['object_events'].append(N.obj('FISHER', fp[0], fp[1], FERRY, el=EL(fn, fp))); N.jdump(fj, 'data/maps/FuchsiaCity/map.json'); fx, fy = 24, 27
WE = json.load(open('src/data/wild_encounters.json')); grp = WE['wild_encounter_groups'][0]['encounters']
entry = {}; journal = []
for z in Z:
    k, mn, tpl = z['k'], z['map'], z['tpl']
    N.clone(mn, tpl, objects=[], warps=[], scripts='', txt=''); nav = R.Nav(mn); cells = comp(nav)
    a = near(nav, cells, (nav.w // 2, int(nav.h * .75)), [], margin=0); entry[k] = a
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
        journal.append((F, q['j'][0], q['j'][1]))
    for j, (spn, lvl, line) in enumerate(z.get('gifts', [])):
        F = flag('GIFT_%s' % k); S_, T_ = '%s_EventScript_Gift%d' % (mn, j), '%s_Text_Gift%d' % (mn, j)
        place('LITTLE_GIRL', off(d), S_); d += 3
        sc += ('%s::\n\tlock\n\tfaceplayer\n\tgoto_if_set %s, %s_Done\n\tmsgbox %s_Offer, MSGBOX_YESNO\n\tgoto_if_eq VAR_RESULT, NO, %s_No\n\tgivemon %s, %d\n\tgoto_if_eq VAR_RESULT, 2, EventScript_NoMoreRoomForPokemon\n\tsetflag %s\n\tmsgbox %s_Got\n\trelease\n\tend\n\n'
               '%s_Done::\n\tmsgbox %s_After\n\trelease\n\tend\n\n%s_No::\n\tmsgbox %s_Refuse\n\trelease\n\tend\n\n') % (S_, F, S_, T_, S_, sp(spn), lvl, F, T_, S_, T_, S_, T_)
        tx += N.text(T_ + '_Offer', line) + N.text(T_ + '_Got', 'Please look after it.') + N.text(T_ + '_After', 'I hope it is happy with you.') + N.text(T_ + '_Refuse', 'Then I will keep it a little longer.')
        journal.append((F, 'A GIFT FROM THE MEADOW', 'SUNRISE MEADOW: a young one awaits.'))
    if z.get('heal'):
        S_ = mn + '_EventScript_Rest'; place('WOMAN_2', off(d), S_); d += 3
        sc += ('%s::\n\tlock\n\tfaceplayer\n\tmsgbox %s_Text_RestOffer, MSGBOX_YESNO\n\tgoto_if_eq VAR_RESULT, NO, %s_No\n\tfadescreen FADE_TO_BLACK\n\tspecial HealPlayerParty\n\tplayfanfare MUS_HEAL\n\twaitfanfare\n\tfadescreen FADE_FROM_BLACK\n\tmsgbox %s_Text_Rested\n\trelease\n\tend\n\n%s_No::\n\tmsgbox %s_Text_RestNo\n\trelease\n\tend\n\n') % (S_, mn, S_, mn, S_, mn)
        tx += N.text(mn + '_Text_RestOffer', 'Sit down. A hot drink and a nap for your team?') + N.text(mn + '_Text_Rested', 'Rested and ready. Come again.') + N.text(mn + '_Text_RestNo', 'Another time, then.')
    if z.get('shop'):
        S_ = mn + '_EventScript_Shop'; place('MAN' if z['shopname'] == 'Collector' else 'WOMAN_3', off(d), S_); d += 3
        sc += '%s::\n\tlock\n\tfaceplayer\n\tmsgbox %s_Text_ShopHi\n\tpokemart %s_Stock\n\tmsgbox %s_Text_ShopBye\n\trelease\n\tend\n\n\t.align 2\n%s_Stock::\n' % (S_, mn, mn, mn, mn) + ''.join('\t.2byte %s\n' % it(i) for i in z['shop']) + '\t.2byte ITEM_NONE\n\n'
        tx += N.text(mn + '_Text_ShopHi', 'Welcome. Take a look around.') + N.text(mn + '_Text_ShopBye', 'Come back any time.')
    for i, itn in enumerate(z.get('hidden', [])):
        F = flag('FIND_%s_%d' % (k, i)); c = near(nav, cells, (a[0] + (i - len(z['hidden']) // 2) * 4, a[1] - 4 - 3 * (i % 4)), taken, margin=3); taken.append(c)
        bgs.append({'type': 'hidden_item', 'x': c[0], 'y': c[1], 'elevation': 0, 'item': it(itn), 'flag': F, 'quantity': 1, 'underfoot': False})
    N.rewrite(mn, objs, sc, tx, bgs=bgs)
    if z['kind'] == 'out':
        ent = {'land_mons': {'encounter_rate': 20, 'mons': mons(z['land'], *z['lv'])}}
        if z.get('water'): ent['water_mons'] = {'encounter_rate': 4, 'mons': mons(z['water'], *z['lv'])}
        if z.get('fish'):
            lo, hi = z['lv']; ent['fishing_mons'] = {'encounter_rate': 20, 'mons': [{'min_level': 5 if i < 2 else (lo if i < 5 else lo + 2), 'max_level': 10 if i < 2 else (lo + 3 if i < 5 else hi), 'species': sp(n)} for i, n in enumerate(z['fish'])]}
        for ver in ('FireRed', 'LeafGreen'):
            e = {'map': N.mapid(mn), 'base_label': 's%s_%s' % (mn, ver)}; e.update(json.loads(json.dumps(ent))); grp.append(e)
    print(k, mn, 'arrivee', a, 'cells', len(cells))
N.jdump(WE, 'src/data/wild_encounters.json')
# ---- passeur : script
sc = '%s::\n\tlock\n\tfaceplayer\n\tgoto_if_unset FLAG_TOPAZE_CLOCK_DONE, %s_EventScript_Closed\n\tmsgbox %s_Hello\n' % (FERRY, FERRY, FT)
tx = N.text(FT + '_Hello', 'My lantern lights the way to calmer places, {PLAYER}.') + N.text(FT + '_Closed', 'The lantern is lit only for those who read the clocks.') + N.text(FT + '_Never', 'Another time. The lantern stays lit.')
for i, z in enumerate(Z):
    nxt = '%s_EventScript_Dest%d' % (FERRY, i + 1) if i < len(Z) - 1 else '%s_EventScript_End' % FERRY
    sc += ('%s_EventScript_Dest%d::\n' % (FERRY, i) if i else '')
    if z['gate']: sc += '\tgoto_if_unset FLAG_BADGE0%d_GET, %s_EventScript_Gate%d\n' % (z['gate'], FERRY, i)
    sc += '\tmsgbox %s_Ask%d, MSGBOX_YESNO\n\tgoto_if_eq VAR_RESULT, NO, %s\n\tsetdynamicwarp MAP_FUCHSIA_CITY, 255, %d, %d\n\twarp %s, 255, %d, %d\n\twaitstate\n\tend\n' % (FT, i, nxt, fx, fy, N.mapid(z['map']), entry[z['k']][0], entry[z['k']][1])
    if z['gate']: sc += '%s_EventScript_Gate%d::\n\tmsgbox %s_GateText%d\n\tgoto %s\n' % (FERRY, i, FT, i, nxt); tx += N.text('%s_GateText%d' % (FT, i), z['gt'])
    tx += N.text('%s_Ask%d' % (FT, i), z['ask'])
sc += '%s_EventScript_End::\n\tmsgbox %s_Never\n\trelease\n\tend\n\n%s_EventScript_Closed::\n\tmsgbox %s_Closed\n\trelease\n\tend\n' % (FERRY, FT, FERRY, FT)
open('data/maps/FuchsiaCity/scripts.inc', 'a').write('\n@ Topaze: le PASSEUR DES LANTERNES (zones lot 3)\n' + sc); open('data/maps/FuchsiaCity/text.inc', 'a').write(tx)
wr('include/constants/flags.h', fl.replace('#endif // GUARD_CONSTANTS_FLAGS_H', ''.join(NEWFL) + '\n#endif // GUARD_CONSTANTS_FLAGS_H'))
g = rd('docs/topaze/journal_gen.py')
if 'LANTERN' not in g:
    i = g.index('assert len(SECTIONS) <= 12'); L = ['# ---- ZONES LOT 3 (le passeur des lanternes) LANTERN']
    for F, nm, hint in journal: L.append('add("SIDE QUESTS", F, "%s", 0, "%s", "%s\\\\nFerry from AMETHIOLITE.", FL("FLAG_TOPAZE_CLOCK_DONE"))' % (F, nm, hint))
    wr('docs/topaze/journal_gen.py', g[:i] + '\n'.join(L) + '\n\n' + g[i:])
