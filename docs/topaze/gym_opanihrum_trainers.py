#!/usr/bin/env python3
"""Fonderie d'Opanihrum : equipes ACIER (Hepha + 8 forgerons), textes, sprite de Hepha. Idempotent (marqueur dans trainer_parties)."""
import re,json,sys
rd=lambda p:open(p).read(); wr=lambda p,s:open(p,'w').write(s)
tr=rd('src/data/trainers.h'); pa=rd('src/data/trainer_parties.h')
if 'SPECIES_AGGRON' in pa and 'sParty_LeaderGiovanni' in pa and re.search(r'sParty_LeaderGiovanni\[\][^;]*AGGRON',pa,re.S): print('already'); sys.exit(0)
T={'LEADER_GIOVANNI':[('MAGNETON',52),('FORRETRESS',53),('SKARMORY',54),('SCIZOR',55),('STEELIX',56),('AGGRON',58)],
 'TAMER_JASON':[('MAGNETON',48),('FORRETRESS',48)],
 'TAMER_COLE':[('SKARMORY',47),('SCIZOR',47)],
 'BLACK_BELT_ATSUSHI':[('ONIX',47),('STEELIX',49)],
 'BLACK_BELT_KIYO':[('LAIRON',47),('LAIRON',47)],
 'BLACK_BELT_TAKASHI':[('MAGNEMITE',43),('MAGNETON',45),('MAGNETON',45)],
 'COOLTRAINER_SAMUEL':[('AGGRON',47),('FORRETRESS',46),('MAGNETON',46),('STEELIX',47),('SCIZOR',47)],
 'COOLTRAINER_YUJI':[('STEELIX',46),('GOLEM',45),('MAGNETON',46),('SKARMORY',47),('SANDSLASH',45)],
 'COOLTRAINER_WARREN':[('FORRETRESS',45),('SKARMORY',46),('AGGRON',46),('SCIZOR',46)]}
for t,team in T.items():
    b=re.search(r'\[TRAINER_%s\] = \{.*?\n    \},'%t,tr,re.S).group(0)
    sym=re.search(r'MOVES\((\w+)\)',b).group(1)
    nb=re.sub(r'NO_ITEM_(?:DEFAULT|CUSTOM)_MOVES\(','NO_ITEM_DEFAULT_MOVES(',b)
    if t=='LEADER_GIOVANNI': nb=re.sub(r'trainerPic = \w+','trainerPic = TRAINER_PIC_LEADER_WINONA',nb)
    tr=tr.replace(b,nb)
    m=re.search(r'static const struct TrainerMon\w+ %s\[\] = \{.*?\};'%sym,pa,re.S); assert m,sym
    iv=60 if t=='LEADER_GIOVANNI' else 40
    body=''.join('    {\n        .iv = %d,\n        .lvl = %d,\n        .species = SPECIES_%s,\n    },\n'%(iv,lv,sp) for sp,lv in team)
    pa=pa.replace(m.group(0),'static const struct TrainerMonNoItemDefaultMoves %s[] = {\n%s};'%(sym,body))
wr('src/data/trainers.h',tr); wr('src/data/trainer_parties.h',pa)
# Hepha overworld sprite
p='data/maps/ViridianCity_Gym/map.json'; m=json.load(open(p))
for o in m['object_events']:
    if o['script'].endswith('_Giovanni'): o['graphics_id']='OBJ_EVENT_GFX_CRUSH_GIRL'
json.dump(m,open(p,'w'),indent=2); open(p,'a').write('\n')
# texts
def mk(label,*lines):
    for l in lines: assert len(l)<=35,(l)
    out=label+'::\n'
    for i,l in enumerate(lines):
        last=i==len(lines)-1
        out+='    .string "'+l+('$' if last else ('\\p' if l.endswith('\\p') else '\\n'))+'"\n'
    return out
def box(label,boxes):
    out=label+'::\n'
    for bi,b in enumerate(boxes):
        for li,l in enumerate(b):
            assert len(l)<=35,l
            ll=li==len(b)-1; lb=bi==len(boxes)-1
            out+='    .string "'+l+('$' if ll and lb else '\\p' if ll else '\\n')+'"\n'
    return out
N={'Yuji':([["Hot metal does not wait for you!"]],[["Quenched…"]],[["HEPHA tempers every one of us","in the opal furnace."]]),
   'Atsushi':([["I hammer ore for a living.","You are next on the anvil!"]],[["My hammer slipped!"]],[["The black opal glows when HEPHA","is angry. Do not make her angry."]]),
   'Jason':([["Clang, clang! My POKéMON and I","make the best forge music!"]],[["Out of tune…"]],[["Wonder who taught HEPHA to","smith? Not me. Not anyone."]]),
   'Kiyo':([["Steel is patient. So am I."]],[["I bent…"]],[["Patience, kid. You'll need it","against HEPHA."]]),
   'Warren':([["Only the best alloy makes it","through this door."]],[["Cracked under pressure!"]],[["HEPHA will melt me down for","this loss…"]]),
   'Takashi':([["I guard the furnace! No one","passes my magnets!"]],[["My magnets failed!"]],[["Eight badges and the LEAGUE.","Then the VICTORY ROAD."]]),
   'Cole':([["Wings of steel cut through","anything. Even you."]],[["Dulled!"]],[["Not all steel is for show.","Some is for the war ahead."]]),
   'Samuel':([["OPANIHRUM's FOUNDRY forged the","LEAGUE's gate. Impressed?"]],[["Too much heat…"]],[["Beyond the gate is the VICTORY","ROAD. Strange men went in."]])}
tp='data/maps/ViridianCity_Gym/text.inc'; t=rd(tp)
for k,(a,b,c) in N.items():
    for suf,bx in (('Intro',a),('Defeat',b),('PostBattle',c)):
        lab=f'ViridianCity_Gym_Text_{k}{suf}'
        s=t.index(lab+'::'); e=t.index('\n\n',s) if '\n\n' in t[s:] else len(t)
        t=t[:s]+box(lab,bx)+t[e:]
# gym guy + statue
s=t.index('ViridianCity_Gym_Text_GymGuyAdvice::'); e=t.index('\n\n',s)
t=t[:s]+box('ViridianCity_Gym_Text_GymGuyAdvice',[["Yo! Champ in the making!"],["This is the FOUNDRY, the last","GYM before the LEAGUE."],["Every TRAINER here uses STEEL-","types. Bring FIRE or GROUND."],["And watch the spinner tiles.","They send you straight to the","furnace!"]])+t[e:]
s=t.index('ViridianCity_Gym_Text_GymGuyPostVictory::'); e=t.index('\n\n',s)
t=t[:s]+box('ViridianCity_Gym_Text_GymGuyPostVictory',[["Eight badges! Go to the VICTORY","ROAD. But mind the men in black."]])+t[e:]
wr(tp,t)
print('ok')
