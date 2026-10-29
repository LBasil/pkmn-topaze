#!/usr/bin/env python3
"""LOT 8 : ~46 objets caches dans 23 donjons (Foret de Jade, Mt Moon, Tunnel Roche, Tour, Manoir, Ile Ecume, Cave Azuree, Route Victoire...), Apothecaire (vitamines) via le passeur de l'apprenti. Idempotent."""
import sys, re; sys.path.insert(0, 'docs/topaze')
from zonelib import *
if 'BuildingApothecary' in rd('docs/topaze/zones_lot8.py') and 'FuchsiaCity_Text_Apprentice_Ask2' in rd('data/maps/FuchsiaCity/text.inc'): print('deja applique'); raise SystemExit
H = {'ViridianForest': ['POTION', 'ANTIDOTE'], 'MtMoon_1F': ['MOON_STONE', 'POTION'], 'MtMoon_B1F': ['REVIVE', 'ETHER'], 'MtMoon_B2F': ['STAR_PIECE', 'SUPER_POTION'], 'DiglettsCave_B1F': ['NUGGET', 'ULTRA_BALL'],
     'RockTunnel_1F': ['SUPER_POTION', 'GREAT_BALL'], 'RockTunnel_B1F': ['REVIVE', 'ELIXIR'], 'PowerPlant': ['THUNDER_STONE', 'MAX_ETHER'], 'SeafoamIslands_1F': ['ULTRA_BALL', 'HYPER_POTION'],
     'SeafoamIslands_B1F': ['WATER_STONE', 'ELIXIR'], 'SeafoamIslands_B2F': ['MAX_REVIVE', 'ULTRA_BALL'], 'SeafoamIslands_B3F': ['NUGGET', 'MAX_ETHER'], 'SeafoamIslands_B4F': ['RARE_CANDY', 'PP_UP'],
     'PokemonMansion_1F': ['FIRE_STONE', 'ULTRA_BALL'], 'PokemonMansion_2F': ['HYPER_POTION', 'ELIXIR'], 'PokemonMansion_3F': ['MAX_REVIVE', 'MAX_ETHER'], 'PokemonMansion_B1F': ['RARE_CANDY', 'NUGGET'],
     'PokemonTower_3F': ['REVIVE', 'ULTRA_BALL'], 'PokemonTower_5F': ['ELIXIR', 'MAX_REVIVE'], 'CeruleanCave_1F': ['MAX_REVIVE', 'ULTRA_BALL'], 'CeruleanCave_2F': ['PP_UP', 'MAX_ELIXIR'], 'CeruleanCave_B1F': ['RARE_CANDY', 'STAR_PIECE'],
     'VictoryRoad_1F': ['MAX_POTION', 'ULTRA_BALL'], 'VictoryRoad_2F': ['MAX_REVIVE', 'ELIXIR'], 'VictoryRoad_3F': ['RARE_CANDY', 'PP_UP']}
nh = 0
for m, items in H.items():
    nav = R.Nav(m); d = json.load(open('data/maps/%s/map.json' % m)); cells = comp(nav)
    taken = [(o['x'], o['y']) for o in d['object_events']] + [(b['x'], b['y']) for b in d['bg_events']] + list(nav.warps)
    cand = [c for c in cells if 1 <= c[0] < nav.w - 1 and 1 <= c[1] < nav.h - 1]
    for i, itn in enumerate(items):
        pref = (int(nav.w * (0.25 + 0.5 * i)), int(nav.h * (0.3 + 0.4 * i)))
        try: c = near(nav, cand, pref, taken, margin=3)
        except SystemExit: print('  sans place:', m, itn); continue
        taken.append(c)
        d['bg_events'].append({'type': 'hidden_item', 'x': c[0], 'y': c[1], 'elevation': 0, 'item': it(itn), 'flag': flag('HID_%s_%d' % (m.upper(), i)), 'quantity': 1, 'underfoot': False}); nh += 1
    N.jdump(d, 'data/maps/%s/map.json' % m)
print('caches donjons', nh)
# Apothecaire (batiment) ajoute au menu de l'apprenti
mn = 'BuildingApothecary'; mn = 'Apothecary'; N.clone(mn, 'SaffronCity_HomeG', objects=[], warps=[], scripts='', txt=''); nav = R.Nav(mn); cells = comp(nav); a = near(nav, cells, (nav.w // 2, int(nav.h * .75)), [], margin=0); taken = [a]
def place(gfx, pref, script, mg=1):
    c = near(nav, cells, pref, taken, mg); taken.append(c); return N.obj(gfx, c[0], c[1], script, el=EL(nav, c))
objs = [place('SAILOR', (a[0] + 2, a[1]), mn + '_EventScript_ReturnFerry'), place('SCIENTIST', (a[0], a[1] - 3), mn + '_EventScript_Shop'), place('WOMAN_3', (a[0] - 3, a[1] - 2), mn + '_EventScript_Npc0')]
sc = ('%s_EventScript_ReturnFerry::\n\tlock\n\tfaceplayer\n\tmsgbox %s_Text_ReturnAsk, MSGBOX_YESNO\n\tgoto_if_eq VAR_RESULT, NO, %s_EventScript_Stay\n\twarp MAP_FUCHSIA_CITY, 255, 24, 27\n\twaitstate\n\tend\n\n%s_EventScript_Stay::\n\tmsgbox %s_Text_Stay\n\trelease\n\tend\n\n') % ((mn,) * 5)
sc += '%s_EventScript_Npc0::\n\tmsgbox %s_Text_Npc0, MSGBOX_NPC\n\tend\n\n%s_EventScript_Shop::\n\tlock\n\tfaceplayer\n\tmsgbox %s_Text_ShopHi\n\tpokemart %s_Stock\n\tmsgbox %s_Text_ShopBye\n\trelease\n\tend\n\n\t.align 2\n%s_Stock::\n' % ((mn,) * 7)
sc += ''.join('\t.2byte %s\n' % it(i) for i in ['HP_UP', 'PROTEIN', 'IRON', 'CALCIUM', 'ZINC', 'CARBOS']) + '\t.2byte ITEM_NONE\n\n'
tx = (N.text(mn + '_Text_ReturnAsk', 'Ready to go back to the dock?') + N.text(mn + '_Text_Stay', 'Take your time. The tide can wait.') + N.text(mn + '_Text_ShopHi', 'Tonics and boosters, made fresh. What is your team missing?') + N.text(mn + '_Text_ShopBye', 'Strength has a price. Pay it wisely.') + N.text(mn + '_Text_Npc0', 'The boosters work best on young POKéMON. Do not wait too long.'))
N.rewrite(mn, objs, sc, tx)
# ajout au menu de l'apprenti : le dernier "Dest" ne pointe plus vers End mais vers un nouveau Dest
S = 'FuchsiaCity_EventScript_Apprentice'; T = 'FuchsiaCity_Text_Apprentice'
fs = rd('data/maps/FuchsiaCity/scripts.inc'); old = 'goto_if_eq VAR_RESULT, NO, %s_EventScript_End\n\tsetdynamicwarp MAP_FUCHSIA_CITY, 255, 24, 27\n\twarp MAP_BARTER_HOUSE' % S
assert old in fs; fs = fs.replace(old, 'goto_if_eq VAR_RESULT, NO, %s_EventScript_Dest2\n\tsetdynamicwarp MAP_FUCHSIA_CITY, 255, 24, 27\n\twarp MAP_BARTER_HOUSE' % S)
new = '%s_EventScript_Dest2::\n\tmsgbox %s_Ask2, MSGBOX_YESNO\n\tgoto_if_eq VAR_RESULT, NO, %s_EventScript_End\n\tsetdynamicwarp MAP_FUCHSIA_CITY, 255, 24, 27\n\twarp MAP_APOTHECARY, 255, %d, %d\n\twaitstate\n\tend\n%s_EventScript_End::' % (S, T, S, a[0], a[1], S)
assert '%s_EventScript_End::' % S in fs; fs = fs.replace('%s_EventScript_End::' % S, new, 1); wr('data/maps/FuchsiaCity/scripts.inc', fs)
open('data/maps/FuchsiaCity/text.inc', 'a').write(N.text(T + '_Ask2', 'The APOTHECARY: boosters for your whole team. Visit?'))
journal_add(['# ---- LOT 8 (apothicaire)', jl('SIDE QUESTS', 'FLAG_TOPAZE_DEXHALL_350', 'THE APOTHECARY', 'Ferry from AMETHIOLITE: boosters on\nsale.').replace('FLAG_TOPAZE_DEXHALL_350', 'FLAG_TOPAZE_CLOCK_DONE').replace('"THE APOTHECARY"', '"THE APOTHECARY"')] if False else ['# ---- LOT 8']); flush_flags()
