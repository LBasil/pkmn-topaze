#!/usr/bin/env python3
"""Diversite sauvage : remplace des creneaux (par indice) dans les tables a 1-3 especes. Niveaux conserves, idempotent."""
import json
F='src/data/wild_encounters.json'; wj=json.load(open(F))
def fam(*st):
    return lambda l: [s for m,s in st if l>=m][-1]
KR=fam((1,'KRABBY'),(28,'KINGLER')); HO=fam((1,'HORSEA'),(32,'SEADRA')); PW=fam((1,'POLIWAG'),(25,'POLIWHIRL')); ST=fam((1,'STARYU')); MA=fam((1,'WOOPER'),(18,'MARILL'))
GD=fam((1,'PSYDUCK'),(33,'GOLDUCK')); NU=fam((1,'NUMEL'),(33,'CAMERUPT')); MB=fam((1,'MAGBY')); RH=fam((1,'RHYHORN'),(42,'RHYDON')); GL=fam((1,'ODDISH'),(21,'GLOOM'))
SH=fam((1,'SHUPPET'),(37,'BANETTE')); DU=fam((1,'DUSKULL'),(37,'DUSCLOPS')); MI=fam((1,'MISDREAVUS')); SA=fam((1,'SABLEYE'))
def const(s): return lambda l: s
LAND={
 'MT_MOON_B1F':{1:const('ZUBAT'),3:const('CLEFAIRY'),5:const('GEODUDE'),7:const('CLEFAIRY'),9:const('ZUBAT')},
 'POKEMON_TOWER_3F':{3:SH,4:DU},'POKEMON_TOWER_4F':{3:DU,4:MI},'POKEMON_TOWER_5F':{3:MI,4:SH},'POKEMON_TOWER_6F':{3:SH,4:DU,8:MI},'POKEMON_TOWER_7F':{3:DU,4:MI,8:SA},
 'MT_EMBER_SUMMIT_PATH_1F':{2:NU,4:const('SLUGMA'),9:RH},'MT_EMBER_SUMMIT_PATH_2F':{2:NU,3:const('SLUGMA'),5:RH},'MT_EMBER_SUMMIT_PATH_3F':{2:NU,4:const('SLUGMA'),9:RH},
 'MT_EMBER_RUBY_PATH_1F':{2:NU,6:const('SLUGMA'),8:RH},'MT_EMBER_RUBY_PATH_B1F':{1:NU,6:RH,8:MB},'MT_EMBER_RUBY_PATH_B2F':{1:NU,6:RH,8:MB},
 'MT_EMBER_RUBY_PATH_B3F':{1:NU,5:MB,8:RH,10:const('GEODUDE')},'MT_EMBER_RUBY_PATH_B1F_STAIRS':{1:NU,6:RH},'MT_EMBER_RUBY_PATH_B2F_STAIRS':{1:NU,6:RH},
 'THREE_ISLAND_PORT':{1:const('WINGULL'),3:const('MEOWTH'),5:const('SKITTY'),9:const('PIDGEOTTO')},
 'ROUTE7':{8:const('VULPIX'),10:GL}, 'ROUTE8':{3:const('VULPIX'),8:const('SANDSHREW')},
 'ROUTE16':{3:const('FEAROW'),8:const('PIDGEOTTO'),10:const('MURKROW')}, 'ROUTE22':{2:const('NIDORAN_F'),3:const('NIDORAN_M'),10:const('NIDORAN_F')},
}
WATER={}
for m in 'ROUTE10 ROUTE11 PALLET_TOWN CERULEAN_CITY VERMILION_CITY SSANNE_EXTERIOR'.split(): WATER[m]={1:KR,3:HO,4:ST}
for m in 'ROUTE6 ROUTE22 ROUTE23 ROUTE25 VIRIDIAN_CITY'.split(): WATER[m]={1:PW,3:PW,4:GD}
WATER['SIX_ISLAND_RUIN_VALLEY']={1:const('MARILL'),3:const('QUAGSIRE')}
n=0
for g in wj['wild_encounter_groups']:
    for e in g['encounters']:
        if 'FireRed' not in e['base_label']: continue
        mp=e['map'][4:]
        for key,D in (('land_mons',LAND),('water_mons',WATER)):
            if mp in D and key in e:
                for i,f in D[mp].items():
                    m=e[key]['mons'][i]; ns='SPECIES_'+f(m['min_level'])
                    if m['species']!=ns: m['species']=ns; n+=1
json.dump(wj,open(F,'w'),indent=2); print('creneaux modifies',n)
