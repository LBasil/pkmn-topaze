import re,sys
repo=sys.argv[1]
# slot: (nom, iv, [(espèce, niveau, [4 capacités])])
L={
'BROCK':('KAY',40,[('VULPIX',15,['EMBER','CONFUSION','QUICK_ATTACK','CONFUSE_RAY']),
  ('GROWLITHE',16,['EMBER','BITE','WATER_PULSE','LEER']),
  ('PONYTA',17,['EMBER','SPARK','STOMP','QUICK_ATTACK']),
  ('MAGMAR',20,['EMBER','SMOG','FIRE_SPIN','LEER'])]),
'MISTY':('SYLVESTRE',50,[('BUTTERFREE',19,['CONFUSION','SLEEP_POWDER','STUN_SPORE','SILVER_WIND']),
  ('PARASECT',20,['SPORE','SLASH','LEECH_LIFE','STUN_SPORE']),
  ('BEEDRILL',20,['SPARK','POISON_POWDER','FURY_CUTTER','LEECH_LIFE']),
  ('WEEPINBELL',21,['RAZOR_LEAF','ACID','SLEEP_POWDER','POISON_POWDER']),
  ('SCYTHER',23,['WING_ATTACK','SLASH','LEECH_LIFE','SWORDS_DANCE'])]),
'LT_SURGE':('HERA',60,[('FEAROW',25,['DRILL_PECK','AERIAL_ACE','SAND_ATTACK','SCREECH']),
  ('DODRIO',26,['DRILL_PECK','CROSS_CHOP','TRI_ATTACK','DOUBLE_TEAM']),
  ('PIDGEOT',27,['WING_ATTACK','FAINT_ATTACK','QUICK_ATTACK','SAND_ATTACK']),
  ('DRAGONAIR',29,['DRAGON_BREATH','SLAM','TWISTER','THUNDER_WAVE']),
  ('AERODACTYL',31,['ANCIENT_POWER','WING_ATTACK','DRAGON_BREATH','BITE'])]),
'ERIKA':('GRIM',70,[('DEWGONG',32,['AURORA_BEAM','SURF','ICE_BEAM','HEADBUTT']),
  ('CLOYSTER',33,['ICE_BEAM','SURF','SUPERSONIC','CLAMP']),
  ('JYNX',34,['ICE_PUNCH','PSYCHIC','HYPNOSIS','DREAM_EATER']),
  ('ONIX',34,['ROCK_SLIDE','ICE_BEAM','EARTHQUAKE','IRON_TAIL']),
  ('LAPRAS',36,['BLIZZARD','SURF','PSYCHIC','HYDRO_PUMP'])]),
'KOGA':('ACHLYS',80,[('TENTACRUEL',38,['SLUDGE_BOMB','SURF','SUPERSONIC','SWIFT']),
  ('ARBOK',38,['SLUDGE_BOMB','IRON_TAIL','SCREECH','BITE']),
  ('MUK',39,['SLUDGE_BOMB','FLAMETHROWER','SHADOW_PUNCH','TOXIC']),
  ('NIDOQUEEN',40,['SLUDGE_BOMB','EARTHQUAKE','BODY_SLAM','TOXIC']),
  ('VILEPLUME',41,['GIGA_DRAIN','SLUDGE_BOMB','STUN_SPORE','SLEEP_POWDER'])]),
'SABRINA':('NOX',90,[('PERSIAN',41,['FAINT_ATTACK','SLASH','SWIFT','SCREECH']),
  ('GOLBAT',42,['SLUDGE_BOMB','CRUNCH','WING_ATTACK','CONFUSE_RAY']),
  ('HAUNTER',42,['SHADOW_BALL','CRUNCH','HYPNOSIS','DREAM_EATER']),
  ('GENGAR',44,['SHADOW_BALL','CRUNCH','THUNDERBOLT','HYPNOSIS']),
  ('PIDGEOT',44,['WING_ATTACK','FAINT_ATTACK','AERIAL_ACE','SAND_ATTACK'])]),
'BLAINE':('EDDIE',100,[('MAGNETON',45,['THUNDERBOLT','TRI_ATTACK','SWIFT','THUNDER_WAVE']),
  ('RAICHU',46,['THUNDERBOLT','SHADOW_BALL','QUICK_ATTACK','THUNDER_WAVE']),
  ('RAPIDASH',46,['THUNDER','FLAMETHROWER','STOMP','QUICK_ATTACK']),
  ('ELECTABUZZ',47,['THUNDER_PUNCH','THUNDERBOLT','SWIFT','SCREECH']),
  ('JOLTEON',48,['THUNDERBOLT','QUICK_ATTACK','DOUBLE_TEAM','SHADOW_BALL'])]),
'GIOVANNI':('HEPHA',120,[('ARBOK',49,['SLUDGE_BOMB','IRON_TAIL','CRUNCH','SCREECH']),
  ('GRAVELER',49,['EARTHQUAKE','ROCK_SLIDE','IRON_TAIL','ROLLOUT']),
  ('MACHAMP',50,['CROSS_CHOP','IRON_TAIL','ROCK_SLIDE','BRICK_BREAK']),
  ('GOLEM',51,['EARTHQUAKE','FLAMETHROWER','ROCK_SLIDE','IRON_TAIL']),
  ('BLASTOISE',53,['SURF','ICE_BEAM','IRON_TAIL','HYDRO_PUMP'])]),
}
pp=repo+'/src/data/trainer_parties.h'; tt=repo+'/src/data/trainers.h'
P=open(pp).read(); T=open(tt).read()
for slot,(name,iv,mons) in L.items():
    arr='sParty_Leader'+{'LT_SURGE':'LtSurge'}.get(slot,slot.title())
    body='\n'.join('    {\n        .iv = %d,\n        .lvl = %d,\n        .species = SPECIES_%s,\n        .moves = {%s},\n    },'%(iv,lv,sp,', '.join('MOVE_'+m for m in (mv+['NONE']*4)[:4])) for sp,lv,mv in mons)
    pat=re.compile(r'(static const struct TrainerMonNoItemCustomMoves '+arr+r'\[\] = \{\n).*?(\n\};)',re.S)
    P,k=pat.subn(lambda m:m.group(1)+body+m.group(2),P,count=1)
    assert k==1,arr
    pat=re.compile(r'(\[TRAINER_LEADER_'+slot+r'\] = \{.*?\.trainerName = _\(")[^"]*("\))',re.S)
    T,k=pat.subn(lambda m:m.group(1)+name+m.group(2),T,count=1)
    assert k==1,slot
open(pp,'w').write(P); open(tt,'w').write(T)
print('ok')
