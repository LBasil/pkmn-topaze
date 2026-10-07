"""Topaze: donne des attaques STAB aux 151 pour leurs NOUVEAUX types (niveaux selon le stade d'évolution).
Usage: python3 learnsets_stab.py <repo>   (nécessite que species_info.h ait déjà les nouveaux types)"""
import re,subprocess,sys
repo=sys.argv[1]
def read(p): return open(repo+'/'+p).read()
cur=read('src/data/pokemon/species_info.h')
orig=subprocess.check_output(['git','-C',repo,'show','037335f4:src/data/pokemon/species_info.h']).decode()
sp=read('include/constants/species.h')
const={int(v):k for k,v in re.findall(r'#define (SPECIES_\w+)\s+(\d+)\s*$',sp,re.M)}
def types(src,name):
    m=re.search(r'\['+name+r'\] =\s*\{.*?\.types = \{(\w+), (\w+)\}',src,re.S)
    return {m.group(1),m.group(2)}
TIER={'TYPE_FIGHTING':['KARATE_CHOP','BRICK_BREAK','CROSS_CHOP'],'TYPE_FLYING':['WING_ATTACK','AERIAL_ACE','DRILL_PECK'],
'TYPE_POISON':['POISON_STING','SLUDGE','SLUDGE_BOMB'],'TYPE_GROUND':['MUD_SLAP','DIG','EARTHQUAKE'],
'TYPE_ROCK':['ROCK_THROW','ROCK_TOMB','ROCK_SLIDE'],'TYPE_BUG':['LEECH_LIFE','FURY_CUTTER','SIGNAL_BEAM'],
'TYPE_GHOST':['LICK','SHADOW_PUNCH','SHADOW_BALL'],'TYPE_STEEL':['METAL_CLAW','STEEL_WING','IRON_TAIL'],
'TYPE_FIRE':['EMBER','FLAME_WHEEL','FLAMETHROWER'],'TYPE_WATER':['WATER_GUN','WATER_PULSE','SURF'],
'TYPE_GRASS':['ABSORB','MEGA_DRAIN','GIGA_DRAIN'],'TYPE_ELECTRIC':['THUNDER_SHOCK','SPARK','THUNDERBOLT'],
'TYPE_PSYCHIC':['CONFUSION','PSYBEAM','PSYCHIC'],'TYPE_ICE':['ICY_WIND','ICE_PUNCH','ICE_BEAM'],
'TYPE_DRAGON':['DRAGON_RAGE','DRAGON_BREATH','DRAGON_CLAW'],'TYPE_DARK':['BITE','FAINT_ATTACK','CRUNCH'],
'TYPE_FAIRY':['SWEET_KISS','COVET','HYPER_VOICE'],'TYPE_NORMAL':['TACKLE','SWIFT','BODY_SLAM']}
# stade d'évolution
evo=read('src/data/pokemon/evolution.h')
child={}
for a,b in re.findall(r'\[(SPECIES_\w+)\]\s*=\s*\{(.*?)\},?\n',evo):
    for t in re.findall(r'(SPECIES_\w+)',b): child[t]=a
def stage(n):
    s=0
    while n in child: n=child[n]; s+=1
    return s
LV={0:(13,31),1:(20,38),2:(28,44)}
ptrs=dict(re.findall(r'\[(SPECIES_\w+)\] = (s\w+LevelUpLearnset)',read('src/data/pokemon/level_up_learnset_pointers.h')))
path='src/data/pokemon/level_up_learnsets.h'; L=read(path); added=0; capped=0
for dex in range(1,152):
    n=const[dex]; new=types(cur,n)-types(orig,n)
    if not new: continue
    arr=ptrs[n]
    m=re.search(r'(static const u16 '+arr+r'\[\] = \{\n)(.*?)(    LEVEL_UP_END\n\};)',L,re.S)
    entries=re.findall(r'LEVEL_UP_MOVE\(\s*(\d+),\s*(MOVE_\w+)\)',m.group(2))
    ents=[(int(a),b) for a,b in entries]; have={b for _,b in ents}
    lv1,lv2=LV[min(stage(n),2)]
    for t in sorted(new):
        if t not in TIER: continue
        for mv,lv in ((TIER[t][0],lv1),(TIER[t][2] if stage(n)>=1 else TIER[t][1],lv2)):
            mv='MOVE_'+mv
            if mv in have: continue
            if len(ents)>=19: capped+=1; continue
            ents.append((lv,mv)); have.add(mv); added+=1
    ents.sort(key=lambda e:e[0])
    body=''.join('    LEVEL_UP_MOVE(%2d, %s),\n'%e for e in ents)
    L=L[:m.start(2)]+body+L[m.end(2):]
open(repo+'/'+path,'w').write(L)
print('attaques ajoutées',added,'ignorées (learnset plein)',capped)
# retype des attaques Fée
b=read('src/data/battle_moves.h')
for mv in ('COVET','HYPER_VOICE','SWEET_KISS'):
    i=b.index('[MOVE_%s] ='%mv); j=b.index('},',i)
    b=b[:i]+b[i:j].replace('TYPE_NORMAL','TYPE_FAIRY')+b[j:]
open(repo+'/src/data/battle_moves.h','w').write(b)
