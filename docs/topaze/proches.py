#!/usr/bin/env python3
"""Les PROCHES : 13 dresseurs optionnels, tres forts, caches sur la route (amis du createur).
Reutilise 13 ids de dresseurs inutilises (renommes TRAINER_PROCHE_*), ecrit equipes + entrees + scripts + textes + objets de carte.
Idempotent (marqueur dans opponents.h). Usage : python3 docs/topaze/proches.py"""
import re, os, sys, json, textwrap
sys.path.insert(0, 'docs/topaze'); sys.path.insert(0, 'tools/topaze/emu'); sys.path.insert(0, '/tmp/gx')
ROOT = os.getcwd()
def rd(p): return open(p, encoding='utf-8').read()
def wr(p, s): open(p, 'w', encoding='utf-8').write(s)

# nom, ancien id (constante), carte, badge requis (0 = postgame), pic, genre, sprite, niveaux, iv, objets-dresseur, recompense, equipe
P = [
 dict(n='THOMAS', old='CYCLING_TRIATHLETE_M', map='Route3', badge=2, pic='LEADER_KOGA', g='M', gfx='BUG_CATCHER', lv=(24, 28), iv=160, bag='ITEM_SUPER_POTION', item='SILVER_POWDER', hint='ROUTE 3', tag='BUG',
      team=[('BUTTERFREE', 'BUG_BUZZ SLEEP_POWDER PSYCHIC PROTECT'), ('BEEDRILL', 'X_SCISSOR POISON_JAB SWORDS_DANCE U_TURN'), ('VENOMOTH', 'BUG_BUZZ SLUDGE_BOMB SLEEP_POWDER PSYCHIC'),
            ('PARASECT', 'SPORE X_SCISSOR SEED_BOMB LEECH_LIFE'), ('PINSIR', 'X_SCISSOR EARTHQUAKE SWORDS_DANCE ROCK_SLIDE'), ('SCYTHER', 'X_SCISSOR AIR_SLASH SWORDS_DANCE U_TURN')],
      t=dict(intro='Yo, {PLAYER}! Nobody takes BUG types seriously. Let me change your mind!', defeat='Ha! Not bad at all!',
             win='Take this. Bugs love it. You earned it!', after='Never underestimate bugs. They always come back stronger.', early='Come back with 2 BADGES. I want a real fight, not a warm-up.')),
 dict(n='LOLA', old='CYCLING_TRIATHLETE_F', map='Route25', badge=3, pic='ELITE_FOUR_LORELEI', g='F', gfx='LORELEI', lv=(30, 34), iv=170, bag='ITEM_SUPER_POTION', item='NEVER_MELT_ICE', hint='ROUTE 25', tag='ICE',
      team=[('DEWGONG', 'ICE_BEAM SURF REST SLEEP_TALK'), ('CLOYSTER', 'ICICLE_CRASH HYDRO_PUMP ROCK_BLAST SPIKES'), ('JYNX', 'ICE_BEAM PSYCHIC LOVELY_KISS NASTY_PLOT'),
            ('SLOWBRO', 'SURF PSYCHIC ICE_BEAM CALM_MIND'), ('SEADRA', 'HYDRO_PUMP ICE_BEAM DRAGON_PULSE AGILITY'), ('LAPRAS', 'ICE_BEAM SURF THUNDERBOLT HYPNOSIS')],
      t=dict(intro='There you are, {PLAYER}! Cold hands, warm heart... but my team is pure ice!', defeat='You melted my team...',
             win='Keep this one. It never melts!', after='Winter is my favorite season. Come see me anytime.', early='Not yet, {PLAYER}. Earn 3 BADGES, then we talk.')),
 dict(n='JORDAN', old='RUNNING_TRIATHLETE_M', map='Route6', badge=4, pic='LEADER_NORMAN', g='M', gfx='MAN', lv=(38, 42), iv=185, bag='ITEM_HYPER_POTION', item='SILK_SCARF', hint='ROUTE 6', tag='NORMAL',
      team=[('PERSIAN', 'DOUBLE_EDGE KNOCK_OFF THUNDERBOLT HYPER_BEAM'), ('CHANSEY', 'BODY_SLAM ICE_BEAM THUNDERBOLT REFLECT'), ('KANGASKHAN', 'DOUBLE_EDGE EARTHQUAKE CRUNCH FIRE_PUNCH'),
            ('PORYGON', 'TRI_ATTACK ICE_BEAM THUNDERBOLT RECOVER'), ('TAUROS', 'DOUBLE_EDGE EARTHQUAKE ZEN_HEADBUTT ROCK_SLIDE'), ('SNORLAX', 'BODY_SLAM EARTHQUAKE REST SLEEP_TALK')],
      t=dict(intro='Normal is not boring, {PLAYER}. Normal is solid. Prove me wrong!', defeat='Solid... and yet you broke through.',
             win='A little gift. Nothing fancy, just good.', after='Keep it simple, keep it strong. That is the way.', early='Come back with 4 BADGES. Then I will not hold back.')),
 dict(n='VIOLETTE', old='RUNNING_TRIATHLETE_F', map='SaffronCity', badge=5, pic='LEADER_SABRINA', g='F', gfx='WOMAN_2', lv=(44, 48), iv=200, bag='ITEM_HYPER_POTION', item='TWISTED_SPOON', hint='SAFFRON CITY', tag='PSYCHIC',
      team=[('MR_MIME', 'PSYCHIC THUNDERBOLT ENERGY_BALL REFLECT'), ('HYPNO', 'PSYCHIC SHADOW_BALL HYPNOSIS NASTY_PLOT'), ('SLOWBRO', 'PSYCHIC SURF ICE_BEAM CALM_MIND'),
            ('EXEGGUTOR', 'PSYCHIC GIGA_DRAIN SLEEP_POWDER EARTHQUAKE'), ('STARMIE', 'SURF PSYCHIC ICE_BEAM THUNDERBOLT'), ('ALAKAZAM', 'PSYCHIC SHADOW_BALL FOCUS_BLAST CALM_MIND')],
      t=dict(intro='I knew you would come, {PLAYER}. I saw it. Now let us see if you can see my moves.', defeat='So you did see it coming...',
             win='Take this. I foresaw you would win.', after='The future is not fixed. You proved that today.', early='Not yet. I see 5 BADGES in your future.')),
 dict(n='EDOUARD', old='SWIMMING_TRIATHLETE_M', map='Route10', badge=5, pic='CHAMPION_STEVEN', g='M', gfx='HIKER', lv=(46, 50), iv=200, bag='ITEM_HYPER_POTION', item='HARD_STONE', hint='ROUTE 10', tag='ROCK',
      team=[('OMASTAR', 'HYDRO_PUMP ICE_BEAM EARTH_POWER SPIKES'), ('KABUTOPS', 'STONE_EDGE WATERFALL SWORDS_DANCE X_SCISSOR'), ('GOLEM', 'EARTHQUAKE ROCK_SLIDE STONE_EDGE FIRE_PUNCH'),
            ('RHYDON', 'EARTHQUAKE STONE_EDGE MEGAHORN SWORDS_DANCE'), ('AERODACTYL', 'STONE_EDGE EARTHQUAKE FLY ROOST'), ('ONIX', 'STONE_EDGE EARTHQUAKE IRON_HEAD ROCK_TOMB')],
      t=dict(intro='{PLAYER}! I have been digging up fossils all week. Ready to face the old ones?', defeat='Crushed... by the new generation!',
             win='Found this in a cave. It is yours now.', after='Stone remembers everything. So will I.', early='Come back with 5 BADGES. Rocks are patient.')),
 dict(n='EMMA', old='SWIMMING_TRIATHLETE_F', map='Route12', badge=6, pic='LEADER_ERIKA', g='F', gfx='WOMAN_3', lv=(50, 54), iv=215, bag='ITEM_FULL_RESTORE', item='MIRACLE_SEED', hint='ROUTE 12', tag='GRASS',
      team=[('NIDOQUEEN', 'EARTH_POWER SLUDGE_WAVE ICE_BEAM THUNDERBOLT'), ('TANGELA', 'GIGA_DRAIN SLEEP_POWDER KNOCK_OFF LEECH_SEED'), ('VICTREEBEL', 'LEAF_STORM SLUDGE_BOMB SWORDS_DANCE POWER_WHIP'),
            ('VILEPLUME', 'GIGA_DRAIN SLUDGE_BOMB SLEEP_POWDER MOONBLAST'), ('EXEGGUTOR', 'ENERGY_BALL PSYCHIC SLEEP_POWDER EARTHQUAKE'), ('VENUSAUR', 'GIGA_DRAIN SLUDGE_BOMB SLEEP_POWDER EARTHQUAKE')],
      t=dict(intro='Oh, {PLAYER}, what a lovely day for a battle! My flowers are in full bloom.', defeat='Oh my... you trampled my garden!',
             win='For you. It grew in my garden.', after='Come back in spring. Everything is prettier then.', early='Come back with 6 BADGES, dear. The flowers can wait.')),
 dict(n='GAUTHIER', old='BATTLE_GIRL', map='Route15', badge=6, pic='ELITE_FOUR_BRUNO', g='M', gfx='BLACK_BELT', lv=(52, 56), iv=215, bag='ITEM_FULL_RESTORE', item='BLACK_BELT', hint='ROUTE 15', tag='FIGHT',
      team=[('HITMONLEE', 'HI_JUMP_KICK BLAZE_KICK STONE_EDGE BULK_UP'), ('HITMONCHAN', 'DRAIN_PUNCH THUNDER_PUNCH ICE_PUNCH FIRE_PUNCH'), ('PRIMEAPE', 'CLOSE_COMBAT ROCK_SLIDE EARTHQUAKE U_TURN'),
            ('POLIWRATH', 'WATERFALL DRAIN_PUNCH ICE_PUNCH BULK_UP'), ('ARCANINE', 'FLARE_BLITZ EXTREME_SPEED CLOSE_COMBAT CRUNCH'), ('MACHAMP', 'CLOSE_COMBAT STONE_EDGE EARTHQUAKE BULLET_PUNCH')],
      t=dict(intro='{PLAYER}! Finally. I have trained every single day for this. Give me everything!', defeat='Haha! THAT is what I was waiting for!',
             win='You earned this. Wear it with pride.', after='Strength is a habit. Keep training, {PLAYER}.', early='Come back with 6 BADGES. I want your full strength.')),
 dict(n='CHLOE', old='PARASOL_LADY', map='CinnabarIsland', badge=7, pic='LEADER_FLANNERY', g='F', gfx='BEAUTY', lv=(58, 62), iv=230, bag='ITEM_FULL_RESTORE', item='CHARCOAL', hint='CINNABAR ISLAND', tag='FIRE',
      team=[('NINETALES', 'FLAMETHROWER SHADOW_BALL NASTY_PLOT WILL_O_WISP'), ('RAPIDASH', 'FLARE_BLITZ MEGAHORN WILL_O_WISP EARTHQUAKE'), ('MAGMAR', 'FIRE_BLAST THUNDERBOLT FOCUS_BLAST PSYCHIC'),
            ('FLAREON', 'FLARE_BLITZ SUPERPOWER WILL_O_WISP SUCKER_PUNCH'), ('CHARIZARD', 'FLAMETHROWER AIR_SLASH DRAGON_PULSE ROOST'), ('ARCANINE', 'FLARE_BLITZ EXTREME_SPEED CRUNCH CLOSE_COMBAT')],
      t=dict(intro='Hey {PLAYER}! Hot day, hotter team. Try not to get burned!', defeat='Okay okay, you are on fire too!',
             win='Here, a little spark for your team.', after='Stay fiery, {PLAYER}. Never let the flame go out.', early='Come back with 7 BADGES. I like my fights well done.')),
 dict(n='VINCENT', old='BOARDER_M', map='Route22', badge=8, pic='LEADER_WATTSON', g='M', gfx='ROCKER', lv=(62, 66), iv=240, bag='ITEM_FULL_RESTORE', item='MAGNET', hint='ROUTE 22', tag='ELECTRIC',
      team=[('RAICHU', 'THUNDERBOLT FOCUS_BLAST SURF NASTY_PLOT'), ('ELECTRODE', 'THUNDERBOLT VOLT_SWITCH THUNDER_WAVE ENERGY_BALL'), ('MAGNETON', 'THUNDERBOLT FLASH_CANNON THUNDER_WAVE PROTECT'),
            ('ELECTABUZZ', 'THUNDERBOLT ICE_PUNCH PSYCHIC FOCUS_BLAST'), ('PORYGON', 'THUNDERBOLT TRI_ATTACK ICE_BEAM RECOVER'), ('JOLTEON', 'THUNDER SHADOW_BALL VOLT_SWITCH ENERGY_BALL')],
      t=dict(intro='Whoa, {PLAYER}! You look charged up. Let us see whose spark is brighter!', defeat='Lights out... for me.',
             win='Plug this in. It will serve you well.', after='Stay shocking, {PLAYER}!', early='Come back with all 8 BADGES. High voltage only.')),
 dict(n='THIBAULT', old='BOARDER_F', map='FuchsiaCity', badge=8, pic='LEADER_WALLACE', g='M', gfx='SWIMMER_M_LAND', lv=(64, 68), iv=240, bag='ITEM_FULL_RESTORE', item='MYSTIC_WATER', hint='FUCHSIA CITY', tag='WATER',
      team=[('KINGLER', 'WATERFALL X_SCISSOR SWORDS_DANCE SUPERPOWER'), ('VAPOREON', 'SURF ICE_BEAM SHADOW_BALL PROTECT'), ('LAPRAS', 'SURF ICE_BEAM THUNDERBOLT REST'),
            ('STARMIE', 'HYDRO_PUMP ICE_BEAM PSYCHIC RECOVER'), ('GYARADOS', 'WATERFALL CRUNCH EARTHQUAKE DRAGON_DANCE'), ('BLASTOISE', 'SCALD ICE_BEAM FLASH_CANNON ROAR')],
      t=dict(intro='{PLAYER}! The tide is perfect today. Come, ride the wave with me!', defeat='Washed away... what a wave!',
             win='From the deep. A gift for you.', after='The sea is calm now. Thanks for the fight, {PLAYER}.', early='Come back with all 8 BADGES. The sea is deep.')),
 dict(n='NATHAN', old='COLLECTOR', map='LavenderTown', badge=8, pic='ELITE_FOUR_SIDNEY', g='M', gfx='GENTLEMAN', lv=(68, 72), iv=250, bag='ITEM_FULL_RESTORE', item='SPELL_TAG', hint='LAVENDER TOWN', tag='GHOST',
      team=[('UMBREON', 'KNOCK_OFF SUCKER_PUNCH TOXIC PROTECT'), ('MISDREAVUS', 'SHADOW_BALL THUNDERBOLT NASTY_PLOT PSYCHIC'), ('SABLEYE', 'KNOCK_OFF SHADOW_CLAW RECOVER WILL_O_WISP'),
            ('HOUNDOOM', 'DARK_PULSE FLAMETHROWER SLUDGE_BOMB NASTY_PLOT'), ('TYRANITAR', 'CRUNCH STONE_EDGE EARTHQUAKE DRAGON_DANCE'), ('GENGAR', 'SHADOW_BALL SLUDGE_BOMB FOCUS_BLAST THUNDERBOLT')],
      t=dict(intro='{PLAYER}. I felt you coming. This town keeps its secrets... and so does my team.', defeat='Even the dead cheer for you...',
             win='Take it. It whispers your name.', after='Some shadows are only friends in disguise.', early='Not yet, {PLAYER}. Return with all 8 BADGES.')),
 dict(n='DYLAN', old='MAGMA_LEADER', map='FourIsland', badge=0, pic='ELITE_FOUR_DRAKE', g='M', gfx='SAILOR', lv=(80, 86), iv=255, bag='ITEM_FULL_RESTORE', item='DRAGON_FANG', hint='FOUR ISLAND', tag='DRAGON',
      team=[('ALTARIA', 'DRAGON_PULSE MOONBLAST HURRICANE ROOST'), ('KINGDRA', 'HYDRO_PUMP DRAGON_PULSE ICE_BEAM DRAGON_DANCE'), ('FLYGON', 'EARTHQUAKE DRAGON_CLAW U_TURN ROOST'),
            ('CHARIZARD', 'DRAGON_CLAW FLARE_BLITZ EARTHQUAKE SWORDS_DANCE'), ('SALAMENCE', 'OUTRAGE FIRE_BLAST EARTHQUAKE DRAGON_DANCE'), ('DRAGONITE', 'OUTRAGE EXTREME_SPEED EARTHQUAKE DRAGON_DANCE')],
      t=dict(intro='{PLAYER}! You beat the LEAGUE? Then you can handle my dragons. Do not hold back!', defeat='Magnificent! The dragons approve!',
             win='A fang from my oldest dragon. Take it.', after='Dragons respect strength. You have it.', early='Come back after the LEAGUE. Dragons wait for no one.')),
 dict(n='ADRIAN', old='OLD_COUPLE', map='PalletTown', badge=0, pic='CHAMPION_RIVAL', g='M', gfx='COOLTRAINER_M', lv=(88, 93), iv=255, bag='ITEM_FULL_RESTORE', item='MASTER_BALL', hint='PALLET TOWN', tag='FLYING',
      team=[('DODRIO', 'BRAVE_BIRD DOUBLE_EDGE EARTHQUAKE ROOST'), ('PIDGEOT', 'BRAVE_BIRD HURRICANE ROOST U_TURN'), ('SKARMORY', 'BRAVE_BIRD IRON_HEAD ROOST SPIKES'),
            ('ARTICUNO', 'ICE_BEAM HURRICANE ROOST FREEZE_DRY'), ('ZAPDOS', 'THUNDER HURRICANE HEAT_WAVE ROOST'), ('MOLTRES', 'FIRE_BLAST HURRICANE ROOST AIR_SLASH')],
      t=dict(intro='{PLAYER}. You met all of them. So now it is my turn. Let us see the sky together.', defeat='You flew higher than all of us.',
             win='Take it. You have earned the sky.', after='We will always be here, {PLAYER}. Fly high.', early='Come back once you have beaten all my friends.')),
]
MAXG = ['THOMAS', 'LOLA', 'JORDAN', 'VIOLETTE', 'EDOUARD', 'EMMA', 'GAUTHIER', 'CHLOE', 'VINCENT', 'THIBAULT', 'NATHAN', 'DYLAN']
NAMES = {'CHLOE': 'CHLOE'}
for p in P:
    p['K'] = 'PROCHE_' + p['n']; p['C'] = 'TRAINER_' + p['K']
    p['scr'] = '%s_EventScript_Proche%s' % (p['map'], p['n'].capitalize())
    p['txt'] = '%s_Text_Proche%s' % (p['map'], p['n'].capitalize())


def wrap(s):
    """texte -> lignes .string (35 car. max, placeholder compte 7), 2 lignes par boite"""
    s2 = s.replace('{PLAYER}', 'PLAYERX')
    lines = textwrap.wrap(s2, 35)
    lines = [l.replace('PLAYERX', '{PLAYER}') for l in lines]
    out = []
    for i, l in enumerate(lines):
        last = i == len(lines) - 1
        sep = '$' if last else ('\\p' if i % 2 == 1 else '\\n')
        out.append('\t.string "%s%s"' % (l, sep))
    return '\n'.join(out)


def main():
    op = rd('include/constants/opponents.h')
    if 'TRAINER_PROCHE_THOMAS' in op:
        print('deja applique'); return
    consts = rd('include/constants/moves.h') + rd('include/constants/species.h') + rd('include/constants/items.h')
    for p in P:
        for sp, mv in p['team']:
            assert re.search(r'#define SPECIES_%s\b' % sp, consts), sp
            for m in mv.split():
                assert re.search(r'#define MOVE_%s\b' % m, consts), m
        assert re.search(r'#define ITEM_%s\b' % p['item'], consts), p['item']
    tr = rd('src/data/trainers.h'); tp = rd('src/data/trainer_parties.h')
    pics = rd('include/constants/trainers.h')
    for p in P:
        assert 'TRAINER_PIC_' + p['pic'] in pics, p['pic']
        old = 'TRAINER_' + p['old']
        op, k = re.subn(r'(#define )%s(\s+)' % old, r'\1%s\2' % p['C'], op)
        assert k == 1, old
        # entree dresseur
        m = re.search(r'    \[%s\] = \{.*?\n    \},\n' % old, tr, re.S); assert m, old
        pname = 'sParty_' + p['n'].capitalize() + 'Proche'
        gend = 'MALE' if p['g'] == 'M' else 'FEMALE'
        ent = ('    [%s] = {\n        .trainerClass = TRAINER_CLASS_PKMN_TRAINER,\n        .encounterMusic_gender = TRAINER_ENCOUNTER_MUSIC_%s,\n        .trainerPic = TRAINER_PIC_%s,\n'
               '        .trainerName = _("%s"),\n        .items = {%s, %s},\n        .doubleBattle = FALSE,\n'
               '        .aiFlags = AI_SCRIPT_CHECK_BAD_MOVE | AI_SCRIPT_TRY_TO_FAINT | AI_SCRIPT_CHECK_VIABILITY,\n        .party = ITEM_CUSTOM_MOVES(%s),\n    },\n') % (
            p['C'], gend, p['pic'], p['n'], p['bag'], p['bag'], pname)
        tr = tr[:m.start()] + ent + tr[m.end():]
        # equipe
        cap = ''.join(w.capitalize() for w in p['old'].split('_'))
        mm = re.search(r'static const struct TrainerMonNoItemDefaultMoves sParty_%s\[\] = \{DUMMY_TRAINER_MON\};\n' % cap, tp)
        if not mm:  # nom irregulier : cherche par l'ordre de la constante
            raise SystemExit('party introuvable ' + cap)
        lo, hi = p['lv']; n = len(p['team'])
        mons = []
        gen = ['ITEM_LEFTOVERS', 'ITEM_SCOPE_LENS', 'ITEM_FOCUS_BAND', 'ITEM_QUICK_CLAW', 'ITEM_KINGS_ROCK']
        for i, (sp, mv) in enumerate(p['team']):
            lvl = lo + round(i * (hi - lo) / (n - 1))
            held = 'ITEM_' + p['item'] if i == n - 1 and p['item'] != 'MASTER_BALL' else gen[i % len(gen)]
            mons.append('    {\n        .iv = %d,\n        .lvl = %d,\n        .species = SPECIES_%s,\n        .heldItem = %s,\n        .moves = {%s},\n    },\n' % (
                p['iv'], lvl, sp, held, ', '.join('MOVE_' + x for x in mv.split())))
        arr = '// Topaze: PROCHE %s (%s), optionnel, fort\nstatic const struct TrainerMonItemCustomMoves %s[] = {\n%s};\n' % (p['n'], p['tag'], pname, ''.join(mons))
        tp = tp[:mm.start()] + arr + tp[mm.end():]
    wr('include/constants/opponents.h', op); wr('src/data/trainers.h', tr); wr('src/data/trainer_parties.h', tp)
    place_all()
    journal()


def place_all():
    import route_test as R
    for p in P:
        mp = 'data/maps/%s/map.json' % p['map']; d = json.load(open(mp))
        nav = R.Nav(p['map'])
        trainers = [(o['x'], o['y']) for o in d['object_events'] if o.get('trainer_type', 'TRAINER_TYPE_NONE') != 'TRAINER_TYPE_NONE']
        objs = [(o['x'], o['y']) for o in d['object_events']]
        free = lambda c: not nav.blocked(*c)
        cells = [(x, y) for y in range(nav.h) for x in range(nav.w) if free((x, y)) and (x, y) not in nav.warps]
        def comp(skip=None):
            seen = set(); best = 0
            for s in cells:
                if s in seen or s == skip: continue
                st = [s]; seen.add(s); n = 0
                while st:
                    c = st.pop(); n += 1
                    for dx, dy in ((0, 1), (0, -1), (1, 0), (-1, 0)):
                        q = (c[0] + dx, c[1] + dy)
                        if q in seen or q == skip or not free(q) or q in nav.warps and False: continue
                        if not nav.step_ok(c, q): continue
                        seen.add(q); st.append(q)
                best = max(best, n)
            return best
        base = comp()
        cx, cy = nav.w // 2, nav.h // 2
        pick = None
        for c in sorted(cells, key=lambda c: abs(c[0] - cx) + abs(c[1] - cy)):
            x, y = c
            if any(abs(x - w[0]) + abs(y - w[1]) < 3 for w in nav.warps): continue
            if any(abs(x - o[0]) + abs(y - o[1]) < 3 for o in objs): continue
            if any((x == t[0] and abs(y - t[1]) <= 7) or (y == t[1] and abs(x - t[0]) <= 7) for t in trainers): continue
            if any(not free((x + dx, y + dy)) for dx in (-1, 0, 1) for dy in (-1, 0, 1)): continue
            if any((x + dx, y + dy) in nav.warps for dx in (-2, -1, 0, 1, 2) for dy in (-2, -1, 0, 1, 2)): continue
            if x <= 1 or y <= 1 or x >= nav.w - 2 or y >= nav.h - 2: continue
            if comp(c) != base - 1: continue
            pick = c; break
        assert pick, p['map']
        x, y = pick; elev = nav.g[y * nav.w + x] >> 12
        d['object_events'].append({"graphics_id": "OBJ_EVENT_GFX_" + p['gfx'], "x": x, "y": y, "elevation": elev if elev not in (0, 15) else 3,
                                   "movement_type": "MOVEMENT_TYPE_FACE_DOWN", "movement_range_x": 1, "movement_range_y": 1,
                                   "trainer_type": "TRAINER_TYPE_NONE", "trainer_sight_or_berry_tree_id": "0", "script": p['scr'], "flag": "0"})
        json.dump(d, open(mp, 'w'), indent=2, ensure_ascii=False); open(mp, 'a').write('\n')
        p['xy'] = (x, y)
        # scripts + textes
        t = p['t']; C = p['C']; s = p['scr']; T = p['txt']
        ok = ''
        if p['badge']:
            ok = '\tgoto_if_unset FLAG_BADGE%02d_GET, %s_TooEarly\n' % (p['badge'], s)
        else:
            if p['n'] == 'ADRIAN':
                ok = '\tgoto_if_unset FLAG_TOPAZE_POSTGAME, %s_TooEarly\n' % s + ''.join('\tgoto_if_not_defeated TRAINER_PROCHE_%s, %s_TooEarly\n' % (o, s) for o in MAXG)
            else:
                ok = '\tgoto_if_unset FLAG_TOPAZE_POSTGAME, %s_TooEarly\n' % s
        sc = ('\n@ Topaze: PROCHE %s (optionnel, fort)\n%s::\n\tlock\n\tfaceplayer\n%s\tgoto_if_defeated %s, %s_After\n\tmsgbox %s_Intro\n'
              '\tcheckitemspace ITEM_%s\n\tgoto_if_eq VAR_RESULT, FALSE, %s_NoRoom\n'
              '\ttrainerbattle_no_intro %s, %s_Defeat\n\tmsgbox %s_Win\n\tgiveitem ITEM_%s\n\tmsgbox %s_After\n\trelease\n\tend\n\n'
              '%s_After::\n\tmsgbox %s_After\n\trelease\n\tend\n\n%s_TooEarly::\n\tmsgbox %s_Early\n\trelease\n\tend\n\n%s_NoRoom::\n\tmsgbox %s_NoRoom\n\trelease\n\tend\n') % (
            p['n'], s, ok, C, s, T, p['item'], s, C, T, T, p['item'], T, s, T, s, T, s, T)
        tx = '\n%s_Intro::\n%s\n\n%s_Defeat::\n%s\n\n%s_Win::\n%s\n\n%s_After::\n%s\n\n%s_Early::\n%s\n\n%s_NoRoom::\n%s\n' % (
            T, wrap(t['intro']), T, wrap(t['defeat']), T, wrap(t['win']), T, wrap(t['after']), T, wrap(t['early']), T, wrap('Your BAG is full. Make some room first, then talk to me again.'))
        with open('data/maps/%s/scripts.inc' % p['map'], 'a', encoding='utf-8') as f: f.write(sc)
        with open('data/maps/%s/text.inc' % p['map'], 'a', encoding='utf-8') as f: f.write(tx)
        print(p['n'], p['map'], pick)


def journal():
    g = rd('docs/topaze/journal_gen.py')
    if '"FRIENDS"' in g: return
    g = g.replace('("LEGENDS", None), ("RARE POKéMON", None),\n]', '("LEGENDS", None), ("RARE POKéMON", None), ("FRIENDS", None),\n]')
    lines = ['\n# ---- FRIENDS (les Proches : dresseurs optionnels tres forts)']
    for p in P:
        vis = ('B(%d)' % p['badge']) if p['badge'] else 'FL("FLAG_TOPAZE_POSTGAME")'
        need = ('Needs %d BADGES.' % p['badge']) if p['badge'] else ('Needs the LEAGUE beaten.' if p['n'] != 'ADRIAN' else 'Beat all your other friends.')
        lines.append('add("FRIENDS", T, "%s", 0, "%s", "%s: a %s specialist.\\n%s", %s)' % (p['C'], p['n'] if p['n'] != 'CHLOE' else 'CHLOE', p['hint'], p['tag'], need, vis))
    g = g.replace('\n# ---- BADGES', '\n'.join(lines) + '\n\n# ---- BADGES', 1) if False else g.rstrip('\n') + '\n' if False else g
    # insere avant le bloc d'ecriture (assert len(SECTIONS))
    i = g.index('assert len(SECTIONS) <= 12')
    g = g[:i] + '\n'.join(lines) + '\n\n' + g[i:]
    wr('docs/topaze/journal_gen.py', g)


if __name__ == '__main__':
    main()
