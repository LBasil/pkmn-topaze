#!/usr/bin/env python3
"""Echo 5 (Registeel, Five Island Meadow) : 4 gardiens + 1 gardienne sur le chemin du Pokemon.
Trainers reaffectes (slots vanille inutilises COOLTRAINER_*). Idempotent (marqueur : EventScript_G0 dans scripts.inc)."""
import re,json,sys,collections
sys.path[:0]=['docs/topaze','tools/topaze/maps']
import route_test as R
rd=lambda p:open(p).read(); wr=lambda p,s:open(p,'w').write(s)
M='FiveIsland_Meadow'; HIDE='FLAG_HIDE_ECHO_BEAST5'
def box(label,boxes):
    out=label+'::\n'
    for bi,bx in enumerate(boxes):
        for li,l in enumerate(bx):
            assert len(l)<=35,(len(l),l)
            ll=li==len(bx)-1; lb=bi==len(boxes)-1
            out+='    .string "'+l+('$' if ll and lb else '\\p' if ll else '\\n')+'"\n'
    return out
TR=[('COOLTRAINER_PAUL','BOLT',[('MAGNETON',66),('SKARMORY',66),('STEELIX',67)],[["Steel does not rust, and neither","does our watch."]],["Rusted through..."],[["Our WARDEN is further on."]],4),
    ('COOLTRAINER_GILBERT','RIVET',[('SCIZOR',67),('FORRETRESS',67),('AGGRON',68),('MAGNETON',68)],[["The ancient one hums when the","sky cracks. We keep it quiet."]],["Bent out of shape."],[["Keep going. It only gets harder."]],4),
    ('COOLTRAINER_OWEN','ALLOY',[('METAGROSS',68),('STEELIX',68),('CLAYDOL',69),('MAWILE',69)],[["No one walks to the shore alone","anymore."]],["The seam gave way."],[["The WARDEN has heard you coming."]],4),
    ('COOLTRAINER_BERKE','FORGE',[('AGGRON',69),('SKARMORY',69),('SCIZOR',70),('METAGROSS',70)],[["The beast gave us shelter when","the sky turned. We stay for it."]],["The forge cools."],[["Almost there. Mind your pride."]],4),
    ('COOLTRAINER_SHANNON','WARDEN',[('METAGROSS',70),('STEELIX',70),('CLAYDOL',71),('SCIZOR',71),('SKARMORY',72),('AGGRON',72)],
        [["I am the WARDEN of the STEEL.","The beast sleeps in my care."],["Prove that your will is worth","more than my fear."]],["...Then the iron has chosen you."],[["Go. Do not let it rust."]],4)]
GF=['OBJ_EVENT_GFX_CHANNELER','OBJ_EVENT_GFX_BLACK_BELT','OBJ_EVENT_GFX_CHANNELER','OBJ_EVENT_GFX_FAT_MAN','OBJ_EVENT_GFX_OLD_WOMAN']
s=rd(f'data/maps/{M}/scripts.inc')
if f'{M}_EventScript_G0::' in s: print('already'); sys.exit()
R.SURF=False; nv=R.Nav(M); nv.objs=set()
path=[(12,29),(12,28),(12,27),(12,26),(12,25),(12,24),(12,23),(12,22),(13,22),(14,22)]  # cour fermee sous l'entrepot, seule entree : escalier (12,30)
idx=[1,3,5,6,8]
def face(i):
    a,b=path[i],path[i-1]; return {(0,1):'DOWN',(0,-1):'UP',(1,0):'RIGHT',(-1,0):'LEFT'}[(b[0]-a[0],b[1]-a[1])]
trs=rd('src/data/trainers.h'); pa=rd('src/data/trainer_parties.h'); objs=[]; k=len(TR)
for j,(tid,name,team,a_,b_,c_,_) in enumerate(TR):
    last=j==k-1
    bb=re.search(r'\[TRAINER_%s\] = \{.*?\n    \},'%tid,trs,re.S).group(0)
    nb=re.sub(r'trainerClass = \w+','trainerClass = TRAINER_CLASS_CHANNELER',bb)
    nb=re.sub(r'encounterMusic_gender = [\w |]+','encounterMusic_gender = TRAINER_ENCOUNTER_MUSIC_SUSPICIOUS',nb)
    nb=re.sub(r'trainerPic = \w+','trainerPic = TRAINER_PIC_%s'%('PSYCHIC_F' if last else 'CHANNELER'),nb)
    nb=re.sub(r'trainerName = _\("[^"]*"\)','trainerName = _("%s")'%name,nb)
    nb=re.sub(r'doubleBattle = \w+','doubleBattle = FALSE',nb)
    nb=re.sub(r'aiFlags = [\w |]+','aiFlags = '+('AI_SCRIPT_CHECK_BAD_MOVE | AI_SCRIPT_TRY_TO_FAINT | AI_SCRIPT_CHECK_VIABILITY' if last else 'AI_SCRIPT_CHECK_BAD_MOVE | AI_SCRIPT_TRY_TO_FAINT'),nb)
    sym=re.search(r'MOVES\((\w+)\)',nb).group(1)
    nb=re.sub(r'(?:NO_)?ITEM_(?:DEFAULT|CUSTOM)_MOVES\(','NO_ITEM_DEFAULT_MOVES(',nb)
    trs=trs.replace(bb,nb)
    m=re.search(r'static const struct TrainerMon\w+ %s\[\] = \{.*?\};'%sym,pa,re.S); assert m,sym
    body=''.join('    {\n        .iv = %d,\n        .lvl = %d,\n        .species = SPECIES_%s,\n    },\n'%(60 if last else 40,lv,sp) for sp,lv in team)
    pa=pa.replace(m.group(0),'static const struct TrainerMonNoItemDefaultMoves %s[] = {\n%s};'%(sym,body))
    x,y=path[idx[j]]
    objs.append({"type":"object","graphics_id":GF[j],"x":x,"y":y,"elevation":3,"movement_type":"MOVEMENT_TYPE_FACE_"+face(idx[j]),"movement_range_x":0,"movement_range_y":0,
      "trainer_type":"TRAINER_TYPE_NORMAL","trainer_sight_or_berry_tree_id":"4","script":f'{M}_EventScript_G{j}',"flag":HIDE})
wr('src/data/trainers.h',trs); wr('src/data/trainer_parties.h',pa)
mj=json.load(open(f'data/maps/{M}/map.json')); mj['object_events']+=objs
json.dump(mj,open(f'data/maps/{M}/map.json','w'),indent=2); open(f'data/maps/{M}/map.json','a').write('\n')
txt=''
for j,(tid,name,team,a_,b_,c_,_) in enumerate(TR):
    s+=f'\n{M}_EventScript_G{j}::\n\ttrainerbattle_single TRAINER_{tid}, {M}_Text_G{j}Intro, {M}_Text_G{j}Defeat\n\tmsgbox {M}_Text_G{j}Post, MSGBOX_AUTOCLOSE\n\tend\n'
    txt+=box(f'{M}_Text_G{j}Intro',a_)+'\n'+box(f'{M}_Text_G{j}Defeat',[b_])+'\n'+box(f'{M}_Text_G{j}Post',c_)+'\n'
wr(f'data/maps/{M}/scripts.inc',s)
tp=f'data/maps/{M}/text.inc'; wr(tp,rd(tp)+'\n'+txt)
print('ok')
