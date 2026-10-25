#!/usr/bin/env python3
"""Echo 4 (Regice, Icefall Cave Back) : 4 gardiens + la gardienne dans le couloir, visibles seulement a l'etape 10 (flags TEMP 11-15),
disparaissent une fois battus ; Regice refuse tant qu'un gardien reste debout. Idempotent (marqueur : EventScript_G0)."""
import re,json
rd=lambda p:open(p).read(); wr=lambda p,s:open(p,'w').write(s)
M='FourIsland_IcefallCave_Back'
def box(label,boxes):
    out=label+'::\n'
    for bi,bx in enumerate(boxes):
        for li,l in enumerate(bx):
            assert len(l)<=35,(len(l),l)
            ll=li==len(bx)-1; lb=bi==len(boxes)-1
            out+='    .string "'+l+('$' if ll and lb else '\\p' if ll else '\\n')+'"\n'
    return out
TR=[('BIRD_KEEPER_REED','FROST',[('GLALIE',62),('DEWGONG',62),('CLOYSTER',63)],[["The cold keeps what it is given."]],["Thawed..."],[["The WARDEN is further on."]],(11,22),'RIGHT','OBJ_EVENT_GFX_CHANNELER'),
    ('BIRD_KEEPER_KEITH','RIME',[('LAPRAS',63),('JYNX',63),('WALREIN',64),('PILOSWINE',64)],[["The ancient one chills the air when","the sky cracks. We keep it calm."]],["Cracked."],[["Keep going. It only gets colder."]],(13,20),'LEFT','OBJ_EVENT_GFX_BLACK_BELT'),
    ('TAMER_JOHN','SLEET',[('GLALIE',64),('LAPRAS',65),('SNEASEL',65),('WALREIN',65)],[["No one walks in alone anymore."]],["Melted away."],[["The WARDEN has felt you coming."]],(11,19),'RIGHT','OBJ_EVENT_GFX_CHANNELER'),
    ('ROCKER_RANDALL','HAIL',[('WALREIN',66),('JYNX',66),('PILOSWINE',66),('CLOYSTER',66)],[["The beast gave us shelter when","the sky turned. We stay for it."]],["The hail stops."],[["Almost there. Mind your pride."]],(13,18),'LEFT','OBJ_EVENT_GFX_FAT_MAN'),
    ('BEAUTY_LAUREN','WARDEN',[('LAPRAS',67),('GLALIE',67),('WALREIN',68),('JYNX',68),('DEWGONG',68),('CLOYSTER',69)],
        [["I am the WARDEN of the ICE.","The beast sleeps in my care."],["Prove that your will is worth","more than my fear."]],["...Then the ice has chosen you."],[["Go. Do not let it melt."]],(12,16),'DOWN','OBJ_EVENT_GFX_OLD_WOMAN')]
sp=f'data/maps/{M}/scripts.inc'; s=rd(sp)
if f'{M}_EventScript_G0::' in s: print('deja'); raise SystemExit
trs=rd('src/data/trainers.h'); pa=rd('src/data/trainer_parties.h'); k=len(TR); objs=[]
for j,(tid,name,team,a_,b_,c_,pos,face,gfx) in enumerate(TR):
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
    body=''.join('    {\n        .iv = %d,\n        .lvl = %d,\n        .species = SPECIES_%s,\n    },\n'%(60 if last else 40,lv,sp_) for sp_,lv in team)
    pa=pa.replace(m.group(0),'static const struct TrainerMonNoItemDefaultMoves %s[] = {\n%s};'%(sym,body))
    objs.append({"type":"object","graphics_id":gfx,"x":pos[0],"y":pos[1],"elevation":3,"movement_type":"MOVEMENT_TYPE_FACE_"+face,"movement_range_x":0,"movement_range_y":0,
      "trainer_type":"TRAINER_TYPE_NORMAL","trainer_sight_or_berry_tree_id":"4","script":f'{M}_EventScript_G{j}',"flag":"FLAG_TEMP_%d"%(11+j)})
wr('src/data/trainers.h',trs); wr('src/data/trainer_parties.h',pa)
mp=f'data/maps/{M}/map.json'; mj=json.load(open(mp)); mj['object_events']+=objs; json.dump(mj,open(mp,'w'),indent=2); open(mp,'a').write('\n')
# EchoSetup : gardiens caches par defaut, reveles a l'etape 10 si non battus
old="FourIsland_IcefallCave_Back_EventScript_EchoSetup::\n\tsetflag FLAG_HIDE_ECHO_BEAST4\n"
assert old in s
s=s.replace(old,old+''.join(f'\tsetflag FLAG_TEMP_{11+j}\n' for j in range(k)),1)
old2="\tclearflag FLAG_HIDE_ECHO_BEAST4\n\treturn\n"
assert s.count(old2)==1
s=s.replace(old2,''.join(f'\tgoto_if_defeated TRAINER_{t[0]}, {M}_Guard{j}_Skip\n\tclearflag FLAG_TEMP_{11+j}\n{M}_Guard{j}_Skip:\n' for j,t in enumerate(TR))+old2,1)
# Regice refuse tant qu'un gardien reste
lab=f'{M}_EventScript_Regice::\n\tgoto_if_questlog EventScript_ReleaseEnd\n\tspecial QuestLog_CutRecording\n\tlock\n\tfaceplayer\n'
assert lab in s
s=s.replace(lab,lab+''.join(f'\tgoto_if_not_defeated TRAINER_{t[0]}, {M}_EventScript_GuardsLeft\n' for t in TR),1)
txt=''
for j,(tid,name,team,a_,b_,c_,pos,face,gfx) in enumerate(TR):
    s+=f'\n{M}_EventScript_G{j}::\n\ttrainerbattle_single TRAINER_{tid}, {M}_Text_G{j}Intro, {M}_Text_G{j}Defeat, {M}_EventScript_G{j}_Vanish\n\tmsgbox {M}_Text_G{j}Post, MSGBOX_AUTOCLOSE\n\tend\n\n{M}_EventScript_G{j}_Vanish::\n\tmsgbox {M}_Text_G{j}Post, MSGBOX_DEFAULT\n\tclosemessage\n\tremoveobject VAR_LAST_TALKED\n\treleaseall\n\tend\n'
    txt+=box(f'{M}_Text_G{j}Intro',a_)+'\n'+box(f'{M}_Text_G{j}Defeat',[b_])+'\n'+box(f'{M}_Text_G{j}Post',c_)+'\n'
s+=f'\n{M}_EventScript_GuardsLeft::\n\tmsgbox {M}_Text_GuardsLeft, MSGBOX_DEFAULT\n\trelease\n\tend\n'
txt+=f'{M}_Text_GuardsLeft::\n    .string "The beast does not stir.\\n"\n    .string "Its guardians still stand watch.$"\n'
wr(sp,s); tp=f'data/maps/{M}/text.inc'; wr(tp,rd(tp)+'\n'+txt); print('ok')
