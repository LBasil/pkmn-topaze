#!/usr/bin/env python3
"""Courbe de niveaux : Route 22 (avant Route Victoire) +38, Tunnel Roche +10, Tour Pokemon +6. NON idempotent : marqueur dans rebalance21_orig.json."""
import json
F='src/data/wild_encounters.json'; wj=json.load(open(F)); O='docs/topaze/rebalance21_orig.json'; o=json.load(open(O))
if o.get('curvefix'): print('deja applique'); raise SystemExit
EV={'SPECIES_RATTATA':(20,'SPECIES_RATICATE'),'SPECIES_MANKEY':(28,'SPECIES_PRIMEAPE'),'SPECIES_SPEAROW':(20,'SPECIES_FEAROW'),'SPECIES_NIDORAN_F':(16,'SPECIES_NIDORINA'),'SPECIES_NIDORAN_M':(16,'SPECIES_NIDORINO'),
 'SPECIES_GEODUDE':(25,'SPECIES_GRAVELER'),'SPECIES_MACHOP':(28,'SPECIES_MACHOKE'),'SPECIES_ZUBAT':(22,'SPECIES_GOLBAT'),'SPECIES_GASTLY':(25,'SPECIES_HAUNTER'),'SPECIES_CUBONE':(28,'SPECIES_MAROWAK'),
 'SPECIES_POOCHYENA':(18,'SPECIES_MIGHTYENA'),'SPECIES_SHUPPET':(37,'SPECIES_BANETTE'),'SPECIES_DUSKULL':(37,'SPECIES_DUSCLOPS'),'SPECIES_VULPIX':(99,''),'SPECIES_PARAS':(24,'SPECIES_PARASECT'),'SPECIES_MEOWTH':(28,'SPECIES_PERSIAN')}
D={'ROUTE22':38,'ROCK_TUNNEL_1F':10,'ROCK_TUNNEL_B1F':10,'POKEMON_TOWER_3F':6,'POKEMON_TOWER_4F':6,'POKEMON_TOWER_5F':6,'POKEMON_TOWER_6F':6,'POKEMON_TOWER_7F':6}
for g in wj['wild_encounter_groups']:
    for e in g['encounters']:
        mp=e['map'][4:]
        if mp in D and 'FireRed' in e['base_label'] and 'land_mons' in e:
            for m in e['land_mons']['mons']:
                m['min_level']+=D[mp]; m['max_level']+=D[mp]
                s=m['species']
                if s in EV and EV[s][1] and m['min_level']>=EV[s][0]: m['species']=EV[s][1]
json.dump(wj,open(F,'w'),indent=2); o['curvefix']=1; json.dump(o,open(O,'w')); print('ok')
