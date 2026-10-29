#!/usr/bin/env python3
"""LOT 6 : quetes d'objets dans 9 villes (chaine d'objets entre les zones), 10 objets caches en ville, Hall du Pokedex (recompenses par paliers), passeur du scribe,
corrections d'approvisionnement (Écailles Cœur, Sel). Textes anglais PROVISOIRES. Idempotent."""
import sys; sys.path.insert(0, 'docs/topaze')
from zonelib import *
if 'FuchsiaCity_EventScript_ScribeFerryman' in rd('data/maps/FuchsiaCity/scripts.inc'): print('deja applique'); raise SystemExit
journal = ['# ---- LOT 6 (quetes de villes, hall du pokedex)']
# approvisionnement
for _ in range(2): hidden_on('HoennWestReserve', 'HEART_SCALE', 'SUP')
hidden_on('HoennEastReserve', 'SHOAL_SALT', 'SUP')
TQ = [
 ('PalletTown', 'WOMAN_1', 'MOOMOO_MILK', 2, 'EXP_SHARE', 1, 'MILK FOR THE LAB', 'PALLET TOWN: bring 2 MOOMOO MILKS.', 'The lab kids love MOOMOO MILK. Bring me 2 and I will reward you.', 'Wonderful! A little help for your team.', 'The lab is happy, thanks to you.'),
 ('ViridianCity', 'GENTLEMAN', 'NUGGET', 1, 'SILK_SCARF', 1, 'THE GILDED GIFT', 'VIRIDIAN CITY: bring a NUGGET.', 'A NUGGET for my collection. Bring me one, will you?', 'How it shines! Take this SCARF.', 'My shelf has never looked better.'),
 ('PewterCity', 'HIKER', 'STAR_PIECE', 1, 'HARD_STONE', 1, 'THE FALLEN STAR', 'PEWTER CITY: bring a STAR PIECE.', 'A STAR PIECE would complete my rock collection.', 'Beautiful! A HARD STONE for you.', 'It sparkles above my desk.'),
 ('VermilionCity', 'SAILOR', 'BIG_PEARL', 1, 'MYSTIC_WATER', 1, 'THE SAILOR\'S PEARL', 'VERMILION CITY: bring a BIG PEARL.', 'A BIG PEARL! My wife would cry. I will trade a charm.', 'She will be overjoyed. Take this MYSTIC WATER.', 'The sea has been kind lately.'),
 ('LavenderTown', 'OLD_WOMAN', 'SPELL_TAG', 1, 'BLACK_GLASSES', 1, 'A TAG FOR THE DEAD', 'LAVENDER TOWN: bring a SPELL TAG.', 'The spirits ask for a SPELL TAG. Can you find one?', 'They are at peace. Take these glasses.', 'The tower is quieter now.'),
 ('CeladonCity', 'LASS', 'ELIXIR', 1, 'MIRACLE_SEED', 1, 'THE SPA REGULAR', 'CELADON CITY: bring an ELIXIR.', 'I need an ELIXIR for my spa day. Do you have one?', 'Bliss! This is for you.', 'My skin has never been so good.'),
 ('FuchsiaCity', 'FISHER', 'SITRUS_BERRY', 1, 'CHARCOAL', 1, 'A BERRY GOOD DEAL', 'AMETHIOLITE: bring a SITRUS BERRY.', 'A SITRUS BERRY would warm me up. I will pay in charcoal.', 'Delicious! Here is your charcoal.', 'I am warm all night.'),
 ('CinnabarIsland', 'SCIENTIST', 'MAGNET', 1, 'NEVER_MELT_ICE', 1, 'THE MAGNET EXPERIMENT', 'CINNABAR ISLAND: bring a MAGNET.', 'I need a MAGNET for my experiment. Can you spare one?', 'Fascinating! Take this ICE.', 'The experiment is a success.'),
 ('SaffronCity', 'WOMAN_3', 'TWISTED_SPOON', 1, 'SILVER_POWDER', 1, 'THE FORTUNE SPOON', 'SAFFRON CITY: bring a TWISTED SPOON.', 'A TWISTED SPOON helps my fortune telling. Bring me one.', 'The future is clear. Take this powder.', 'I see good things for you.'),
]
for q in TQ: route_quest(*q, journal=journal, tag='TQ')
for m, itn in [('PalletTown', 'POTION'), ('ViridianCity', 'ULTRA_BALL'), ('PewterCity', 'REVIVE'), ('VermilionCity', 'ELIXIR'), ('LavenderTown', 'MAX_ETHER'), ('CeladonCity', 'ULTRA_BALL'), ('FuchsiaCity', 'HYPER_POTION'), ('CinnabarIsland', 'ELIXIR'), ('SaffronCity', 'MAX_REVIVE'), ('IndigoPlateau_Exterior', 'RARE_CANDY')]:
    hidden_on(m, itn, 'TOWN')
# ---------------- Hall du Pokedex
mn = 'DexHall'; N.clone(mn, 'SaffronCity_HomeF', objects=[], warps=[], scripts='', txt=''); nav = R.Nav(mn); cells = comp(nav); a = near(nav, cells, (nav.w // 2, int(nav.h * .75)), [], margin=0); taken = [a]
def place(gfx, pref, script, mg=1):
    c = near(nav, cells, pref, taken, mg); taken.append(c); return N.obj(gfx, c[0], c[1], script, el=EL(nav, c))
objs = [place('SAILOR', (a[0] + 2, a[1]), mn + '_EventScript_ReturnFerry'), place('SCIENTIST', (a[0], a[1] - 3), mn + '_EventScript_Judge')]
MS = [(25, 'ULTRA_BALL', 5), (50, 'RARE_CANDY', 2), (75, 'PP_UP', 2), (100, 'MAX_REVIVE', 3), (150, 'RARE_CANDY', 5), (200, 'PP_MAX', 3), (250, 'MASTER_BALL', 1), (300, 'RARE_CANDY', 10), (350, 'PP_MAX', 5), (386, 'RARE_CANDY', 30)]
sc = ('%s_EventScript_ReturnFerry::\n\tlock\n\tfaceplayer\n\tmsgbox %s_Text_ReturnAsk, MSGBOX_YESNO\n\tgoto_if_eq VAR_RESULT, NO, %s_EventScript_Stay\n\twarp MAP_FUCHSIA_CITY, 255, 24, 27\n\twaitstate\n\tend\n\n%s_EventScript_Stay::\n\tmsgbox %s_Text_Stay\n\trelease\n\tend\n\n') % ((mn,) * 5)
tx = N.text(mn + '_Text_ReturnAsk', 'Ready to go back to the dock?') + N.text(mn + '_Text_Stay', 'Take your time. The tide can wait.') + N.text(mn + '_Text_Hello', 'I judge the POKeDEX. Every caught species earns a reward at each milestone. Let me count.') + N.text(mn + '_Text_Nothing', 'No new milestone yet. Keep catching them all.') + N.text(mn + '_Text_NoRoom', 'Your BAG is full. Make room, then come back.')
J = mn + '_EventScript_Judge'; sc += '%s::\n\tlock\n\tfaceplayer\n\tmsgbox %s_Text_Hello\n\tsetvar VAR_0x8004, 1\n\tspecialvar VAR_RESULT, GetPokedexCount\n' % (J, mn)
for i, (n, itn, q) in enumerate(MS):
    nxt = '%s_%d' % (J, i + 1) if i < len(MS) - 1 else J + '_End'; F = flag('DEXHALL_%d' % n)
    sc += ('%s_%d::\n' % (J, i) if i else '') + '\tgoto_if_set %s, %s\n\tgoto_if_lt VAR_0x8006, %d, %s\n\tcheckitemspace %s, %d\n\tgoto_if_eq VAR_RESULT, FALSE, %s_NoRoom\n\tgiveitem %s, %d\n\tsetflag %s\n\tmsgbox %s_Text_M%d\n\tsetvar VAR_0x8004, 1\n\tspecialvar VAR_RESULT, GetPokedexCount\n\tgoto %s\n' % (F, nxt, n, nxt, it(itn), q, J, it(itn), q, F, mn, n, nxt)
    tx += N.text('%s_Text_M%d' % (mn, n), 'You have caught %d species! A reward for you.' % n)
sc += '%s_End::\n\tmsgbox %s_Text_Nothing\n\trelease\n\tend\n\n%s_NoRoom::\n\tmsgbox %s_Text_NoRoom\n\trelease\n\tend\n' % (J, mn, J, mn)
N.rewrite(mn, objs, sc, tx)
ferry('ScribeFerryman', 'SCIENTIST', (19, 30), 'The scribe waits for you with his ledger, {PLAYER}.', 'The ledger is closed. Come back when the clocks make sense.', 'Another time, then.', [(mn, a, 0, 'The HALL OF THE POKeDEX: rewards for every milestone. Visit?', '')])
journal.append(jl('SIDE QUESTS', 'FLAG_TOPAZE_DEXHALL_350', 'THE POKeDEX HALL', 'Ferry from AMETHIOLITE: rewards at\n25, 50, 100... species caught.'))
journal_add(journal); flush_flags()
