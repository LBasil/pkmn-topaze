#!/usr/bin/env python3
"""ZONES DU TEMPS : le PASSEUR (Amethiolite) mene a 7 zones (cartes clonees sur des layouts existants). Textes anglais PROVISOIRES. Idempotent.
 Phare (3 etages) | Plage des horloges | Village sans lendemain | Grotte sans fond (3 etages) | Jardin d'Echos | Ile du dernier jour | Clairiere des Proches
 Dresseurs reutilises : 25,26,511,512,513,515,530 -> TRAINER_ZONE_*. Usage : python3 docs/topaze/zones_temps.py"""
import sys, os, re, json
sys.path.insert(0, 'docs/topaze'); sys.path.insert(0, 'tools/topaze/emu'); sys.path.insert(0, '/tmp/gx')
import newmap as N, route_test as R
rd, wr = N.rd, N.wr
if 'TRAINER_ZONE_LIGHTHOUSE' in rd('include/constants/opponents.h'): print('deja applique'); raise SystemExit
BADGE = lambda n: 'FLAG_BADGE0%d_GET' % n
# nom, template, carte(s), id dresseur ancien, constante, pic, nom boss, niveau, equipe, recompense (item, n), gate (cmd, arg), texte de gate, ferry label
Z = [
 dict(k='LIGHTHOUSE', maps=['Lighthouse_1F', 'Lighthouse_2F', 'Lighthouse_3F'], tpl='PokemonTower_6F', old='ELITE_FOUR_SIDNEY', pic='EXPERT_M', boss='KEEPER', lvl=52, iv=210,
      team=[('MAGNETON', 'THUNDERBOLT FLASH_CANNON THUNDER_WAVE PROTECT'), ('STARMIE', 'SURF PSYCHIC ICE_BEAM THUNDERBOLT'), ('LAPRAS', 'SURF ICE_BEAM THUNDERBOLT REST'), ('JOLTEON', 'THUNDER SHADOW_BALL VOLT_SWITCH ENERGY_BALL')],
      rew=('PP_MAX', 2), gate=('unset', BADGE(5)), gate_txt='Come back with 5 BADGES.', ask='The old LIGHTHOUSE? Its lamp turns backwards. Want to see it?',
      boss_intro='You climbed all this way? The lamp never lights for visitors. Only for ships that left long ago.', boss_def='The lamp... it turned the right way. Just once.',
      boss_after='Go on, take it. The light was never mine.', npcs=[('SAILOR', 'The tide here has not turned in years. The lamp keeps waiting for a ship.'), ('OLD_MAN_1', 'Each floor is older than the last. The top is the oldest of all.')]),
 dict(k='BEACH', maps=['ClockBeach'], tpl='OneIsland_TreasureBeach', old='ELITE_FOUR_PHOEBE', pic='SWIMMER_M', boss='TIDE', lvl=58, iv=220,
      team=[('KINGLER', 'WATERFALL X_SCISSOR SWORDS_DANCE SUPERPOWER'), ('VAPOREON', 'SURF ICE_BEAM SHADOW_BALL PROTECT'), ('GYARADOS', 'WATERFALL CRUNCH EARTHQUAKE DRAGON_DANCE'), ('BLASTOISE', 'SCALD ICE_BEAM FLASH_CANNON ROAR')],
      rew=('RARE_CANDY', 3), gate=('unset', BADGE(6)), gate_txt='Come back with 6 BADGES.', ask='The CLOCK BEACH? Every wave brings in a broken clock. Want to see it?',
      boss_intro='Another stopped clock washed up: you. Let the sea decide how long you stay!', boss_def='The tide turned for you.', boss_after='The sea keeps what it likes. Today it kept nothing of yours.',
      npcs=[('FISHER', 'A clock washed up at dawn. Another at noon. They all say 3:07.'), ('LITTLE_GIRL', 'I found a shell shaped like a clock. It ticks when it rains.')]),
 dict(k='VILLAGE', maps=['NoTomorrowVillage'], tpl='SevenIsland', old='PKMN_PROF_PROF_OAK', pic='PSYCHIC_M', boss='TOMORROW', lvl=64, iv=235,
      team=[('MR_MIME', 'PSYCHIC THUNDERBOLT ENERGY_BALL REFLECT'), ('HYPNO', 'PSYCHIC SHADOW_BALL HYPNOSIS NASTY_PLOT'), ('SLOWBRO', 'PSYCHIC SURF ICE_BEAM CALM_MIND'), ('ALAKAZAM', 'PSYCHIC SHADOW_BALL FOCUS_BLAST CALM_MIND')],
      rew=('MAX_REVIVE', 3), gate=('unset', BADGE(7)), gate_txt='Come back with 7 BADGES.', ask='A village where today never ends? Do you want to go?',
      boss_intro='Today again. It was a good day, so it stayed. Break it, if you can!', boss_def='So tomorrow finally... arrives.',
      boss_after='The sun is rising. Really rising. Thank you.', npcs=[('WOMAN_2', 'Good morning! Good morning! It is always morning here.'), ('FAT_MAN', 'I bought bread yesterday. Today I bought it again. Same bread.'), ('LITTLE_BOY', 'Mama says tomorrow never comes. I think it is hiding.')],
      npcs_after=['Good evening! Evening! It is evening!', 'Fresh bread, today. A new loaf. How strange!', 'Mama says tomorrow came. I told you it was hiding.']),
 dict(k='CAVE', maps=['Depths_1F', 'Depths_2F', 'Depths_3F'], tpl='SixIsland_AlteringCave', old='TRAINER_ELITE_FOUR_PHOEBE_X', pic='RS_HIKER', boss='DEPTH', lvl=70, iv=245,
      team=[('GOLEM', 'EARTHQUAKE ROCK_SLIDE STONE_EDGE FIRE_PUNCH'), ('RHYDON', 'EARTHQUAKE STONE_EDGE MEGAHORN SWORDS_DANCE'), ('ONIX', 'STONE_EDGE EARTHQUAKE IRON_HEAD ROCK_TOMB'), ('AERODACTYL', 'STONE_EDGE EARTHQUAKE FLY ROOST')],
      rew=('RARE_CANDY', 5), gate=('unset', BADGE(8)), gate_txt='Come back with all 8 BADGES.', ask='The BOTTOMLESS CAVE? Every time you go down, the floor count changes. Brave enough?',
      boss_intro='The bottom? There is no bottom. There is only me, wherever you stop.', boss_def='So there was a floor after all.', boss_after='The cave is quiet now. For today.', npcs=[('HIKER', 'I went down three floors. Then ten. Then one. Do not count.')]),
 dict(k='GARDEN', maps=['EchoGarden'], tpl='FiveIsland_Meadow', old='PLAYER_BRENDAN', pic='AROMA_LADY', boss='GARDENER', lvl=75, iv=255,
      team=[('VENUSAUR', 'GIGA_DRAIN SLUDGE_BOMB SLEEP_POWDER EARTHQUAKE'), ('VILEPLUME', 'GIGA_DRAIN SLUDGE_BOMB SLEEP_POWDER MOONBLAST'), ('VICTREEBEL', 'LEAF_STORM SLUDGE_BOMB SWORDS_DANCE POWER_WHIP'), ('EXEGGUTOR', 'ENERGY_BALL PSYCHIC SLEEP_POWDER EARTHQUAKE')],
      rew=('FULL_RESTORE', 3), gate=('unset', 'FLAG_TOPAZE_ARCHIVE_DONE'), gate_txt='The garden opens once the ARCHIVE of ECHOES is complete.', ask='The GARDEN OF ECHOES blooms with what the ECHOES left behind. Visit?',
      boss_intro='Every flower here grew from an ECHO. Please do not trample them. Battle me instead!', boss_def='Oh! The flowers are cheering for you.', boss_after='Come back in spring. Or any time. It is always spring here.',
      npcs=[('WOMAN_3', 'These seeds fell from ECHOES. I water them with sea air.'), ('GARDENER', 'Do not pick the blue ones. They remember too much.')]),
 dict(k='ISLAND', maps=['LastDayIsland'], tpl='BirthIsland_Exterior', old='PLAYER_LEAF', pic='LEADER_GIOVANNI', boss='LAST', lvl=84, iv=255,
      team=[('MEWTWO', 'PSYCHIC SHADOW_BALL FOCUS_BLAST RECOVER'), ('DRAGONITE', 'OUTRAGE EXTREME_SPEED EARTHQUAKE DRAGON_DANCE'), ('SNORLAX', 'BODY_SLAM EARTHQUAKE REST SLEEP_TALK'), ('ALAKAZAM', 'PSYCHIC SHADOW_BALL FOCUS_BLAST CALM_MIND'), ('GENGAR', 'SHADOW_BALL SLUDGE_BOMB FOCUS_BLAST THUNDERBOLT'), ('MEW', 'PSYCHIC AURA_SPHERE NASTY_PLOT RECOVER')],
      rew=('RARE_CANDY', 10), gate=('unset', 'FLAG_TOPAZE_POSTGAME'), gate_txt='This place opens only after the LEAGUE.', ask='The ISLAND OF THE LAST DAY... no one has come back from there unchanged. Go anyway?',
      boss_intro='The last day of every road ends here. I am its keeper. Show me the end!', boss_def='So that is how it ends. Well fought.', boss_after='There is always one more day. Even after the last.', npcs=[('OLD_WOMAN', 'This is where every clock ends. Quietly.')]),
 dict(k='CLEARING', maps=['FriendsClearing'], tpl='ThreeIsland_BerryForest', old='BIKER_2', pic='CHAMPION_RIVAL', boss='FRIEND', lvl=86, iv=255,
      team=[('DRAGONITE', 'OUTRAGE EXTREME_SPEED EARTHQUAKE DRAGON_DANCE'), ('ARCANINE', 'FLARE_BLITZ EXTREME_SPEED CRUNCH CLOSE_COMBAT'), ('BLASTOISE', 'SCALD ICE_BEAM FLASH_CANNON ROAR'), ('VENUSAUR', 'GIGA_DRAIN SLUDGE_BOMB SLEEP_POWDER EARTHQUAKE'), ('MACHAMP', 'CLOSE_COMBAT STONE_EDGE EARTHQUAKE BULLET_PUNCH'), ('ALAKAZAM', 'PSYCHIC SHADOW_BALL FOCUS_BLAST CALM_MIND')],
      rew=('PP_MAX', 3), gate=('undefeated', 'TRAINER_PROCHE_ADRIAN'), gate_txt='Only those who beat every friend may enter.', ask='A clearing where your friends rest between battles. Visit?',
      boss_intro='All of us, together. One team, for one last fight, {PLAYER}. Ready?', boss_def='We lost! But we lost together.', boss_after='Come back anytime. There is always a seat for you.',
      npcs=[('COOLTRAINER_F', 'Each of us left something here. A memory, an object. Look around.'), ('CAMPER', 'We train in the morning. Rest at noon. Fight at dusk.')]),
]
# ---------------- constantes / dresseurs
OLDID = {'LIGHTHOUSE': 'ELITE_FOUR_SIDNEY', 'BEACH': 'ELITE_FOUR_PHOEBE', 'VILLAGE': 'PKMN_PROF_PROF_OAK', 'CAVE': 'PLAYER_BRENDAN_', 'GARDEN': 'PLAYER_BRENDAN', 'ISLAND': 'PLAYER_LEAF', 'CLEARING': 'BIKER_2'}
OLDID['CAVE'] = 'PLAYER_MAY'
op, tr, tp = rd('include/constants/opponents.h'), rd('src/data/trainers.h'), rd('src/data/trainer_parties.h')
consts = rd('include/constants/moves.h') + rd('include/constants/species.h')
FEM = {'AROMA_LADY'}
for z in Z:
    old = OLDID[z['k']]; z['C'] = 'TRAINER_ZONE_' + z['k']
    op, k = re.subn(r'(#define )TRAINER_%s(\s+)' % old, r'\1%s\2' % z['C'], op); assert k == 1, old
    m = re.search(r'    \[TRAINER_%s\] = \{.*?\n    \},\n' % old, tr, re.S); assert m, old
    pn = 'sParty_Zone' + z['k'].capitalize()
    pic = 'TRAINER_PIC_' + z['pic']; assert pic in rd('include/constants/trainers.h'), pic
    ent = ('    [%s] = {\n        .trainerClass = TRAINER_CLASS_PKMN_TRAINER,\n        .encounterMusic_gender = TRAINER_ENCOUNTER_MUSIC_%s,\n        .trainerPic = %s,\n        .trainerName = _("%s"),\n'
           '        .items = {ITEM_FULL_RESTORE, ITEM_FULL_RESTORE},\n        .doubleBattle = FALSE,\n        .aiFlags = AI_SCRIPT_CHECK_BAD_MOVE | AI_SCRIPT_TRY_TO_FAINT | AI_SCRIPT_CHECK_VIABILITY,\n        .party = ITEM_CUSTOM_MOVES(%s),\n    },\n') % (
        z['C'], 'FEMALE' if z['pic'] in FEM else 'MALE', pic, z['boss'], pn)
    tr = tr[:m.start()] + ent + tr[m.end():]
    mons = ''
    for i, (sp, mv) in enumerate(z['team']):
        assert re.search(r'#define SPECIES_%s\b' % sp, consts), sp
        for x in mv.split(): assert re.search(r'#define MOVE_%s\b' % x, consts), x
        mons += '    {\n        .iv = %d,\n        .lvl = %d,\n        .species = SPECIES_%s,\n        .heldItem = %s,\n        .moves = {%s},\n    },\n' % (z['iv'], z['lvl'] + i, sp, ['ITEM_LEFTOVERS', 'ITEM_SCOPE_LENS', 'ITEM_FOCUS_BAND', 'ITEM_QUICK_CLAW', 'ITEM_KINGS_ROCK'][i % 5], ', '.join('MOVE_' + x for x in mv.split()))
    cap = ''.join(w.capitalize() for w in old.split('_'))
    mm = re.search(r'static const struct \w+ sParty_%s\[\] = (?:\{DUMMY_TRAINER_MON\};|\{\n.*?\n\};)\n' % re.escape(cap), tp, re.S); assert mm, cap
    assert mm, cap
    tp = tp[:mm.start()] + '// Topaze: zone %s (boss %s)\nstatic const struct TrainerMonItemCustomMoves %s[] = {\n%s};\n' % (z['k'], z['boss'], pn, mons) + tp[mm.end():]
wr('include/constants/opponents.h', op); wr('src/data/trainers.h', tr); wr('src/data/trainer_parties.h', tp)
# ---------------- helpers de placement
def reach(nav, start):
    seen = {start}; st = [start]
    while st:
        c = st.pop()
        for dx, dy in ((0, 1), (0, -1), (1, 0), (-1, 0)):
            q = (c[0] + dx, c[1] + dy)
            if q in seen or nav.blocked(*q) or not nav.step_ok(c, q): continue
            seen.add(q); st.append(q)
    return seen
def pick(nav, prefer, taken, zone=None, margin=1):
    cells = zone if zone is not None else [(x, y) for y in range(nav.h) for x in range(nav.w)]
    for c in sorted(cells, key=lambda c: abs(c[0] - prefer[0]) + abs(c[1] - prefer[1])):
        x, y = c
        if nav.blocked(x, y) or c in nav.warps or any(abs(x - t[0]) + abs(y - t[1]) <= margin for t in taken): continue
        if any(nav.blocked(x + dx, y + dy) for dx, dy in ((0, 1), (0, -1), (1, 0), (-1, 0))): continue
        return c
    raise SystemExit('pas de place pres de %s' % (prefer,))
# ---------------- le passeur (Amethiolite = FuchsiaCity)
FERRY = 'FuchsiaCity_EventScript_EchoFerryman'; FT = 'FuchsiaCity_Text_Ferry'
fn = R.Nav('FuchsiaCity'); fj = json.load(open('data/maps/FuchsiaCity/map.json'))
fo = [(o['x'], o['y']) for o in fj['object_events']]
fp = pick(fn, (24, 29), fo + [(w[0], w[1]) for w in fn.warps], margin=3)
fx, fy = fp[0], fp[1] + 1
if fn.blocked(fx, fy): fx, fy = fp[0], fp[1] - 1
fj['object_events'].append(N.obj('SAILOR', fp[0], fp[1], FERRY, el=fn.g[fp[1] * fn.w + fp[0]] >> 12 or 3)); N.jdump(fj, 'data/maps/FuchsiaCity/map.json')
# ---------------- les zones
entry = {}   # k -> (map, x, y, warpid)
for z in Z:
    maps = z['maps']; k = z['k']; C = z['C']; tpl = z['tpl']
    tw = json.load(open('data/maps/%s/map.json' % tpl))['warp_events']
    bossmap = maps[-1]; arrmap = maps[0]
    # creer toutes les cartes vides (layout du modele)
    for mn in maps: N.clone(mn, tpl, objects=[], warps=[], scripts='', txt='', requires_flash=False)
    # arrivee + sortie
    sc = {mn: '' for mn in maps}; tx = {mn: '' for mn in maps}; objs = {mn: [] for mn in maps}; wps = {mn: [] for mn in maps}
    for i, mn in enumerate(maps):
        nav = R.Nav(mn); el = lambda c: nav.g[c[1] * nav.w + c[0]] >> 12 or 3
        if k == 'LIGHTHOUSE':
            up, down = tw[0], tw[1]   # (11,16)->7F (haut) ; (18,10)->5F (bas)
            wps[mn] = []
            if i == 0: wps[mn].append(N.warp(down['x'], down['y'], 'MAP_DYNAMIC', 'WARP_ID_DYNAMIC'))
            else: wps[mn].append(N.warp(down['x'], down['y'], N.mapid(maps[i - 1]), 1))
            if i < len(maps) - 1: wps[mn].insert(0, N.warp(up['x'], up['y'], N.mapid(maps[i + 1]), 1))
            else: wps[mn].insert(0, N.warp(up['x'], up['y'], N.mapid(mn), 1))   # inutile (haut) -> boucle sur place
            if i == len(maps) - 1: wps[mn] = [wps[mn][1]]; wps[mn] = [N.warp(down['x'], down['y'], N.mapid(maps[i - 1]), 0)]
            # indices : warp0 = haut, warp1 = bas
            if i == 0: wps[mn] = [N.warp(up['x'], up['y'], N.mapid(maps[1]), 1), N.warp(down['x'], down['y'], 'MAP_DYNAMIC', 'WARP_ID_DYNAMIC')]
            elif i == 1: wps[mn] = [N.warp(up['x'], up['y'], N.mapid(maps[2]), 1), N.warp(down['x'], down['y'], N.mapid(maps[0]), 0)]
            else: wps[mn] = [N.warp(up['x'], up['y'], N.mapid(maps[2]), 0), N.warp(down['x'], down['y'], N.mapid(maps[1]), 0)]
    # arrivee
    nav = R.Nav(arrmap); el = lambda c: nav.g[c[1] * nav.w + c[0]] >> 12 or 3
    if k == 'LIGHTHOUSE': entry[k] = (arrmap, 0, 0, 1)     # arrive sur le warp 1 (escalier bas)
    elif k == 'CAVE':
        w0 = tw[0]; a = (w0['x'], w0['y'] - 1) if not nav.blocked(w0['x'], w0['y'] - 1) else pick(nav, (w0['x'], w0['y']), [])
        entry[k] = (arrmap, a[0], a[1], 255); wps[arrmap] = [N.warp(w0['x'], w0['y'], 'MAP_DYNAMIC', 'WARP_ID_DYNAMIC')]
    else:
        pref = {'BEACH': (12, 24), 'VILLAGE': (11, 11), 'GARDEN': (12, 24), 'ISLAND': (15, 20), 'CLEARING': (43, 38)}[k]
        a = pick(nav, pref, []); entry[k] = (arrmap, a[0], a[1], 255)
    # PNJ de retour (passeur) a cote de l'arrivee ; sur Phare et Grotte : pres de l'entree
    ra = entry[k]; base = (ra[1], ra[2]) if ra[3] == 255 else (tw[1]['x'], tw[1]['y'] + 1)
    nv = R.Nav(arrmap); rc = pick(nv, (base[0] + 2, base[1]), [base], margin=1)
    objs[arrmap].append(N.obj('SAILOR', rc[0], rc[1], '%s_EventScript_ReturnFerry' % arrmap, el=nv.g[rc[1] * nv.w + rc[0]] >> 12 or 3))
    sc[arrmap] += ('%s_EventScript_ReturnFerry::\n\tlock\n\tfaceplayer\n\tmsgbox %s_Text_ReturnAsk, MSGBOX_YESNO\n\tgoto_if_eq VAR_RESULT, NO, %s_EventScript_Stay\n\twarp MAP_FUCHSIA_CITY, 255, %d, %d\n\twaitstate\n\tend\n\n'
                   '%s_EventScript_Stay::\n\tmsgbox %s_Text_Stay\n\trelease\n\tend\n\n') % (arrmap, arrmap, arrmap, fx, fy, arrmap, arrmap)
    tx[arrmap] += N.text(arrmap + '_Text_ReturnAsk', 'Ready to go back to the dock?') + N.text(arrmap + '_Text_Stay', 'Take your time. The tide can wait.')
    # boss
    nb = R.Nav(bossmap); reachable = reach(nb, (ra[1], ra[2]) if bossmap == arrmap and ra[3] == 255 else (wps[bossmap][0]['x'], wps[bossmap][0]['y'] + 1) if wps[bossmap] else (nb.w // 2, nb.h // 2))
    if k == 'LIGHTHOUSE': reachable = reach(nb, (nb.w // 2, nb.h // 2 + 3)) if not reach(nb, (tw[0]['x'], tw[0]['y'] + 1)) else reach(nb, (tw[0]['x'], tw[0]['y'] + 1))
    bp = {'LIGHTHOUSE': (12, 8), 'BEACH': (12, 12), 'VILLAGE': (11, 11), 'CAVE': (20, 12), 'GARDEN': (12, 10), 'ISLAND': (15, 8), 'CLEARING': (28, 22)}[k]
    taken = [(o['x'], o['y']) for o in objs[bossmap]]
    bc = pick(nb, bp, taken + [(ra[1], ra[2])], zone=sorted(reachable), margin=3)
    BS = '%s_EventScript_Boss' % bossmap; BT = '%s_Text_Boss' % bossmap
    objs[bossmap].append(N.obj('MAN', bc[0], bc[1], BS, el=nb.g[bc[1] * nb.w + bc[0]] >> 12 or 3))
    sc[bossmap] += ('%s::\n\tlock\n\tfaceplayer\n\tgoto_if_defeated %s, %s_After\n\tmsgbox %s_Intro\n\tcheckitemspace ITEM_%s, %d\n\tgoto_if_eq VAR_RESULT, FALSE, %s_NoRoom\n'
                    '\ttrainerbattle_no_intro %s, %s_Defeat\n\tgiveitem ITEM_%s, %d\n\tmsgbox %s_After\n\trelease\n\tend\n\n%s_After::\n\tmsgbox %s_After\n\trelease\n\tend\n\n%s_NoRoom::\n\tmsgbox %s_NoRoom\n\trelease\n\tend\n\n') % (
        BS, C, BS, BT, z['rew'][0], z['rew'][1], BS, C, BT, z['rew'][0], z['rew'][1], BT, BS, BT, BS, BT)
    tx[bossmap] += N.text(BT + '_Intro', z['boss_intro']) + N.text(BT + '_Defeat', z['boss_def']) + N.text(BT + '_After', z['boss_after']) + N.text(BT + '_NoRoom', 'Your BAG is full. Make room, then come back.')
    # PNJ d'ambiance
    for j, (gfx, line) in enumerate(z['npcs']):
        mn = maps[j % len(maps)]; nn = R.Nav(mn); taken2 = [(o['x'], o['y']) for o in objs[mn]] + [(ra[1], ra[2])]
        pc = pick(nn, (nn.w // 2 + 3 * j - 3, nn.h // 2 + 3), taken2 + wps_pos(wps[mn]) if False else taken2, margin=2) if True else None
        S_ = '%s_EventScript_Npc%d' % (mn, j); T_ = '%s_Text_Npc%d' % (mn, j)
        # apres le boss (village) : dialogue different
        if z.get('npcs_after'):
            sc[mn] += '%s::\n\tgoto_if_defeated %s, %s_After\n\tmsgbox %s, MSGBOX_NPC\n\tend\n\n%s_After::\n\tmsgbox %s_A, MSGBOX_NPC\n\tend\n\n' % (S_, C, S_, T_, S_, T_)
            tx[mn] += N.text(T_, line) + N.text(T_ + '_A', z['npcs_after'][j])
        else:
            sc[mn] += '%s::\n\tmsgbox %s, MSGBOX_NPC\n\tend\n\n' % (S_, T_); tx[mn] += N.text(T_, line)
        objs[mn].append(N.obj(gfx, pc[0], pc[1], S_, mv='MOVEMENT_TYPE_FACE_DOWN', el=nn.g[pc[1] * nn.w + pc[0]] >> 12 or 3))
    # ecrire les cartes
    for mn in maps:
        N.rewrite(mn, objs[mn], sc[mn], tx[mn]); d = json.load(open('data/maps/%s/map.json' % mn)); d['warp_events'] = wps[mn]; N.jdump(d, 'data/maps/%s/map.json' % mn)
    print(k, 'arrivee', entry[k], 'boss', bossmap, bc)
# ---------------- Passeur : script + textes
sc = '%s::\n\tlock\n\tfaceplayer\n\tgoto_if_unset FLAG_TOPAZE_CLOCK_DONE, %s_EventScript_Closed\n\tmsgbox %s_Hello\n' % (FERRY, FERRY, FT)
tx = N.text(FT + '_Hello', 'I row where time runs differently. Where do you want to go, {PLAYER}?') + N.text(FT + '_Closed', 'The ferry is not running. The clocks of the routes are still unread. Come back when you know why they stopped.') + N.text(FT + '_Never', 'Another time, then. The tide will wait.') + N.text(FT + '_Gate', 'The tide says no, {PLAYER}.')
for i, z in enumerate(Z):
    k = z['k']; nxt = '%s_EventScript_Dest%d' % (FERRY, i + 1) if i < len(Z) - 1 else '%s_EventScript_End' % FERRY
    cmd, arg = z['gate']
    sc += '%s_EventScript_Dest%d::\n' % (FERRY, i) if i else ''
    gate_script = '\tgoto_if_%s %s, %s_EventScript_Gate%d\n' % ('unset' if cmd == 'unset' else 'not_defeated', arg, FERRY, i)
    sc += gate_script + '\tmsgbox %s_Ask%d, MSGBOX_YESNO\n\tgoto_if_eq VAR_RESULT, NO, %s\n\tsetdynamicwarp MAP_FUCHSIA_CITY, 255, %d, %d\n' % (FT, i, nxt, fx, fy)
    em, ex, ey, ew = entry[k]
    sc += '\twarp %s, %d, %d, %d\n\twaitstate\n\tend\n' % (N.mapid(em), ew, ex, ey)
    sc += '%s_EventScript_Gate%d::\n\tmsgbox %s_GateText%d\n\tgoto %s\n' % (FERRY, i, FT, i, nxt)
    tx += N.text('%s_Ask%d' % (FT, i), z['ask']) + N.text('%s_GateText%d' % (FT, i), z['gate_txt'])
sc += '%s_EventScript_End::\n\tmsgbox %s_Never\n\trelease\n\tend\n\n%s_EventScript_Closed::\n\tmsgbox %s_Closed\n\trelease\n\tend\n' % (FERRY, FT, FERRY, FT)
open('data/maps/FuchsiaCity/scripts.inc', 'a').write('\n@ Topaze: le PASSEUR des Echos (menu des zones du Temps)\n' + sc); open('data/maps/FuchsiaCity/text.inc', 'a').write(tx)
# ---------------- journal
g = rd('docs/topaze/journal_gen.py')
if 'TRAINER_ZONE_LIGHTHOUSE' not in g:
    i = g.index('assert len(SECTIONS) <= 12')
    L = ['# ---- ZONES DU TEMPS (le passeur d\'Amethiolite)', 'add("SIDE QUESTS", F, "FLAG_TOPAZE_CLOCK_DONE", 0, "THE ECHO FERRYMAN", "AMETHIOLITE dock: a ferryman rows to\\\\nplaces where time runs elsewhere.", PV())']
    H = {'LIGHTHOUSE': ('THE LIGHTHOUSE', 'Needs 5 BADGES.'), 'BEACH': ('THE CLOCK BEACH', 'Needs 6 BADGES.'), 'VILLAGE': ('NO-TOMORROW VILLAGE', 'Needs 7 BADGES.'), 'CAVE': ('THE BOTTOMLESS CAVE', 'Needs 8 BADGES.'),
         'GARDEN': ('GARDEN OF ECHOES', 'Needs the ECHO ARCHIVE done.'), 'ISLAND': ('ISLAND OF THE LAST DAY', 'Needs the LEAGUE beaten.'), 'CLEARING': ('CLEARING OF FRIENDS', 'Beat every friend first.')}
    for z in Z:
        vis = 'FL("FLAG_TOPAZE_POSTGAME")' if z['k'] in ('GARDEN', 'ISLAND', 'CLEARING') else 'FL("FLAG_TOPAZE_CLOCK_DONE")'
        L.append('add("POST-GAME" if "%s" in ("GARDEN","ISLAND","CLEARING") else "SIDE QUESTS", T, "%s", 0, "%s", "AMETHIOLITE ferry: face the %s.\\\\n%s", %s)' % (z['k'], z['C'], H[z['k']][0], z['boss'], H[z['k']][1], vis))
    wr('docs/topaze/journal_gen.py', g[:i] + '\n'.join(L) + '\n\n' + g[i:])
