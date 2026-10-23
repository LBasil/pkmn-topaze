#!/usr/bin/env python3
"""Rééquilibrage de la difficulté (retours Basil 21/10). Idempotent : repart
toujours des valeurs d'origine stockées dans rebalance21_orig.json.
Usage : python3 docs/topaze/rebalance21.py"""
import re,json,glob,os,sys
ROOT=os.path.abspath(os.path.join(os.path.dirname(__file__),'../..')); os.chdir(ROOT)
ORIGF='docs/topaze/rebalance21_orig.json'
# ---- deltas de niveau par carte (dresseurs) ----
TR={}
def S(names,d):
    for n in names.split(): TR[n]=d
S('RocketHideout_B1F RocketHideout_B2F RocketHideout_B3F RocketHideout_B4F CeladonCity_GameCorner',8)
S('Route12 Route13 Route14 Route15',5)
S('Route16 Route17 Route18 Route19 Route20 Route21_North Route21_South',8)
S('SafariZone_Center SafariZone_East SafariZone_West',7)
S('SafariZone_North',3)
S('FuchsiaCity_Gym',7)
S('SaffronCity_Gym',9)
S('SaffronCity_Dojo',6)
S('SilphCo_2F SilphCo_3F SilphCo_4F SilphCo_5F SilphCo_6F SilphCo_7F SilphCo_8F SilphCo_9F SilphCo_10F SilphCo_11F',11)
S('CinnabarIsland_Gym PokemonMansion_1F PokemonMansion_2F PokemonMansion_3F PokemonMansion_B1F',6)
S('SeafoamIslands_B1F SeafoamIslands_B2F SeafoamIslands_B3F',6)
S('ViridianCity_Gym',4)
S('RockTunnel_1F RockTunnel_B1F',6)
S('PokemonTower_3F PokemonTower_4F PokemonTower_5F PokemonTower_6F',4)
S('VictoryRoad_1F VictoryRoad_2F VictoryRoad_3F VictoryRoadLair_1F VictoryRoadLair_2F',4)
S('OneIsland_KindleRoad ThreeIsland_BondBridge MtEmber_Exterior OneIsland_TreasureBeach',6)
# chefs d'arène / Conseil 4 / champion (parties nommées)
PARTY={'LeaderKoga':4,'LeaderSabrina':8,'LeaderBlaine':6,'LeaderGiovanni':0,
 'EliteFourLorelei':5,'EliteFourBruno':5,'EliteFourAgatha':5,'EliteFourLance':5,
 'ChampionFirstSquirtle':5,'ChampionFirstBulbasaur':5,'ChampionFirstCharmander':5,
 'EliteFourLorelei2':2,'EliteFourBruno2':2,'EliteFourAgatha2':2,'EliteFourLance2':2,
 'ChampionRematchSquirtle':2,'ChampionRematchBulbasaur':2,'ChampionRematchCharmander':2}
# ---- deltas sauvages (terre / surf / casse-roche) ----
WD={}
def W(names,d):
    for n in names.split(): WD[n]=d
W('Route12 Route13 Route14 Route15',5)
W('Route16 Route17 Route18 Route19 Route20 Route21_North Route21_South FuchsiaCity SafariZone_Center SafariZone_East SafariZone_West SafariZone_North',8)
W('SeafoamIslands_1F SeafoamIslands_B1F SeafoamIslands_B2F SeafoamIslands_B3F SeafoamIslands_B4F CinnabarIsland PokemonMansion_1F PokemonMansion_2F PokemonMansion_3F PokemonMansion_B1F',6)
W('PokemonTower_3F PokemonTower_4F PokemonTower_5F PokemonTower_6F PokemonTower_7F',11)
W('RockTunnel_1F RockTunnel_B1F',18)
NOEVO=('Leader','EliteFour','Champion')

S_=''.join(open(f).read() for f in glob.glob('data/scripts/*.inc')+glob.glob('data/maps/*/scripts.inc'))
T=open('src/data/trainers.h').read(); P=open('src/data/trainer_parties.h').read()
def party_of(tid):
    m=re.search(r'\[%s\] = \{(.*?)\n    \},'%tid,T,re.S)
    p=re.search(r'(?:ITEM|NO_ITEM)_(?:CUSTOM|DEFAULT)_MOVES\((\w+)\)',m.group(1)) if m else None
    return p.group(1) if p else None
def scr_trainer(sc):
    m=re.search(r'\n%s::\n(?:\t[^\n]*\n)*?\ttrainerbattle_\w+\s+(TRAINER_\w+)'%re.escape(sc),S_)
    return m.group(1) if m else None
def block(name):
    return re.search(r'(%s\[\] = \{)(.*?)(\n\};)'%re.escape(name),P,re.S)
# evolutions par niveau
EV={}
for m in re.finditer(r'\[(SPECIES_\w+)\]\s*=\s*\{\{EVO_LEVEL,\s*(\d+),\s*(SPECIES_\w+)\}',open('src/data/pokemon/evolution.h').read()):
    EV[m.group(1)]=(int(m.group(2)),m.group(3))
def evolve(sp,lvl):
    while sp in EV and lvl>=EV[sp][0]: sp=EV[sp][1]
    return sp
# collecte party -> delta
pd={}
for n,d in TR.items():
    j=json.load(open('data/maps/%s/map.json'%n))
    for o in j.get('object_events',[]):
        if o.get('trainer_type') in ('TRAINER_TYPE_NORMAL','TRAINER_TYPE_SEE_ALL_DIRECTIONS','TRAINER_TYPE_BURIED'):
            t=scr_trainer(o['script']); p=party_of(t) if t else None
            if p: pd[p]=max(pd.get(p,0),d)
for k,d in PARTY.items(): pd['sParty_'+k]=d
orig=json.load(open(ORIGF)) if os.path.exists(ORIGF) else {'parties':{},'wild':{}}
for p in pd:
    if p not in orig['parties']:
        b=block(p); orig['parties'][p]=re.findall(r'\.lvl = (\d+),\s*\n\s*\.species = (SPECIES_\w+)',b.group(2))
P2=P
for p,d in pd.items():
    b=block(p)
    if not b: print('absent',p); continue
    it=iter(orig['parties'][p]); noevo=any(p.startswith('sParty_'+x) for x in NOEVO)
    def f(m):
        l,sp=next(it); nl=min(100,int(l)+d)
        if not noevo: sp=evolve(sp,nl)
        return '.lvl = %d,%s.species = %s'%(nl,m.group(2),sp)
    nb=re.sub(r'\.lvl = (\d+),(\s*\n\s*)\.species = (SPECIES_\w+)',f,b.group(2))
    P2=P2.replace(b.group(0),b.group(1)+nb+b.group(3))
open('src/data/trainer_parties.h','w').write(P2)
# sauvages
wj=json.load(open('src/data/wild_encounters.json'))
for g in wj['wild_encounter_groups']:
    for e in g['encounters']:
        mn=e['map']
        name=[k for k in WD if 'MAP_'+re.sub(r'(?<!^)(?=[A-Z])','_',k).upper().replace('__','_')==mn]
        if not name: continue
        d=WD[name[0]]
        for k in ('land_mons','water_mons','rock_smash_mons'):
            if k in e:
                for i,mo in enumerate(e[k]['mons']):
                    key=mn+k+str(i)
                    o=orig['wild'].setdefault(key,[mo['min_level'],mo['max_level']])
                    mo['min_level']=o[0]+d; mo['max_level']=o[1]+d
json.dump(wj,open('src/data/wild_encounters.json','w'),indent=2)
json.dump(orig,open(ORIGF,'w'))
print('parties',len(pd),'ok')
# ---- portée de vision : on ne doit plus se coller aux dresseurs ----
nch=0
for f in glob.glob('data/maps/*/map.json'):
    n=f.split('/')[2]; j=json.load(open(f)); ch=False
    indoor=bool(re.search(r'Gym|Dojo|SilphCo|SSAnne|Mansion|Tower|House|Center|Mart|GameCorner|Hideout',n))
    mn=3 if indoor else 4
    for o in j.get('object_events',[]):
        if o.get('trainer_type') in ('TRAINER_TYPE_NORMAL','TRAINER_TYPE_SEE_ALL_DIRECTIONS'):
            if 0<int(o['trainer_sight_or_berry_tree_id'])<mn:
                o['trainer_sight_or_berry_tree_id']=str(mn); ch=True; nch+=1
    if ch: json.dump(j,open(f,'w'),indent=2); open(f,'a').write('\n')
print('sight raised on',nch,'trainers')
# ---- équipes thématiques des arènes (absolu) ----
TEAMS={
 # Amethiolite : poison
 'JugglerKayden':[(46,'NIDOKING')],
 'JugglerShawn':[(44,'NIDORINO'),(45,'TENTACRUEL')],
 'JugglerKirk':[(42,'WEEZING'),(42,'MUK'),(43,'WEEZING'),(43,'MUK')],
 'TamerEdgar':[(44,'ARBOK'),(44,'SEVIPER'),(45,'ARBOK')],
 'TamerPhil':[(45,'MUK'),(45,'WEEZING')],
 'JugglerNate':[(45,'VENOMOTH'),(45,'GOLBAT')],
 # Nox : ténèbres / spectre
 'PsychicCameron':[(46,'HOUNDOOM'),(46,'MIGHTYENA'),(47,'HOUNDOOM')],
 'PsychicJohan':[(44,'SNEASEL'),(44,'MURKROW'),(45,'MISDREAVUS'),(46,'UMBREON')],
 'PsychicPreston':[(50,'ABSOL')],
 'ChannelerAmanda':[(47,'HAUNTER'),(47,'BANETTE')],
 'ChannelerStacy':[(50,'GENGAR')],
 'ChannelerTasha':[(46,'HAUNTER'),(46,'SABLEYE'),(47,'DUSCLOPS')],
 'PsychicTyron':[(47,'SABLEYE'),(47,'MURKROW')],
}
P3=open('src/data/trainer_parties.h').read()
for k,team in TEAMS.items():
    b=block('sParty_'+k) if False else re.search(r'(sParty_%s\[\] = \{)(.*?)(\n\};)'%k,P3,re.S)
    body=''.join('\n    {\n        .iv = 20,\n        .lvl = %d,\n        .species = SPECIES_%s,\n    },'%(l,s) for l,s in team)
    P3=P3.replace(b.group(0),b.group(1)+body+b.group(3))
open('src/data/trainer_parties.h','w').write(P3)
print('teams ok')
