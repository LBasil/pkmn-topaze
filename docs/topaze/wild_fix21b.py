#!/usr/bin/env python3
"""Retours Basil 21/10 (soir) : routes 21 vides (que des Saquedeneu) et Pokémon d'eau trop faibles. A lancer APRES rebalance21.py (idempotent).
- Route 21 N/S : table de terre variee, niv. 40-48.
- Eau (surf) : tables refaites sur les routes marines apres Parmanie (especes variees, niveaux resserres) ; Sevii : plancher de niveau ; peche +12."""
import json, re
import os
F = 'src/data/wild_encounters.json'; j = json.load(open(F)); OF = 'docs/topaze/wild_fix21b_orig.json'; ORIG = json.load(open(OF)) if os.path.exists(OF) else {}
def mons(spec): return [{'min_level': a, 'max_level': b, 'species': 'SPECIES_' + s} for s, a, b in spec]
LAND21 = mons([('TANGELA',42,45),('MR_MIME',41,44),('PIDGEOTTO',40,44),('PONYTA',42,45),('TANGELA',44,47),('RAPIDASH',45,48),('FEAROW',42,46),('PIDGEOTTO',44,47),('KANGASKHAN',44,47),('SCYTHER',45,48),('PINSIR',45,48),('CHANSEY',46,48)])
def water(a, b, sp): return mons([(sp[0],a,a+4),(sp[1],a+1,a+5),(sp[2],a+2,a+6),(sp[3],a+3,a+7),(sp[4],a+4,b)])
SEA = {'MAP_ROUTE19':44,'MAP_ROUTE20':45,'MAP_ROUTE21_NORTH':46,'MAP_ROUTE21_SOUTH':46,'MAP_CINNABAR_ISLAND':44,'MAP_ROUTE12':38,'MAP_ROUTE13':38}
SEASP = ['TENTACOOL','TENTACRUEL','STARYU','SEADRA','GYARADOS']
FRESH = {'MAP_FUCHSIA_CITY':40,'MAP_SAFARI_ZONE_CENTER':42,'MAP_SAFARI_ZONE_EAST':42,'MAP_SAFARI_ZONE_NORTH':42,'MAP_SAFARI_ZONE_WEST':42,'MAP_CELADON_CITY':36}
FRSP = ['PSYDUCK','GOLDUCK','SLOWPOKE','POLIWHIRL','SEAKING']
SEVII = [k for k in ('SSANNE_EXTERIOR','ONE_ISLAND','ONE_ISLAND_KINDLE_ROAD','ONE_ISLAND_TREASURE_BEACH','TWO_ISLAND_CAPE_BRINK','THREE_ISLAND_BOND_BRIDGE','THREE_ISLAND_BERRY_FOREST','FOUR_ISLAND','FIVE_ISLAND','FIVE_ISLAND_RESORT_GORGEOUS','FIVE_ISLAND_WATER_LABYRINTH','FIVE_ISLAND_MEADOW','FIVE_ISLAND_MEMORIAL_PILLAR','SIX_ISLAND_OUTCAST_ISLAND','SIX_ISLAND_GREEN_PATH','SIX_ISLAND_WATER_PATH','SEVEN_ISLAND_TRAINER_TOWER','SEVEN_ISLAND_TANOBY_RUINS','FOUR_ISLAND_ICEFALL_CAVE_ENTRANCE')]
SEVII = ['MAP_' + k for k in SEVII]
for g in j['wild_encounter_groups']:
    for e in g['encounters']:
        m = e['map']
        if m in ('MAP_ROUTE21_NORTH', 'MAP_ROUTE21_SOUTH') and 'land_mons' in e: e['land_mons']['mons'] = json.loads(json.dumps(LAND21))
        if 'water_mons' in e:
            if m in SEA: e['water_mons']['mons'] = water(SEA[m], SEA[m] + 8, SEASP)
            elif m in FRESH: e['water_mons']['mons'] = water(FRESH[m], FRESH[m] + 8, FRSP)
            elif m in SEVII:
                for mo in e['water_mons']['mons']:
                    mo['min_level'] = max(mo['min_level'], 38); mo['max_level'] = max(mo['max_level'], mo['min_level'] + 6)
        if 'fishing_mons' in e and m in SEA:
            ms = e['fishing_mons']['mons']; key = m + e['base_label']
            if key not in ORIG: ORIG[key] = [[x['min_level'], x['max_level']] for x in ms]
            for x, (a, b) in zip(ms, ORIG[key]): x['min_level'] = a + 12; x['max_level'] = b + 12
open(OF, 'w').write(json.dumps(ORIG))
json.dump(j, open(F, 'w'), indent=2)
print('ok')
