#!/usr/bin/env python3
"""Echo 7 (Celebi, Sevault Canyon) : 4 gardiens + la gardienne dans le couloir, visibles seulement a l'etape 19 (flags TEMP 18,19,1A,1C,1D),
disparaissent une fois battus ; Celebi refuse tant qu'un gardien reste debout. Idempotent (marqueur : EventScript_G0)."""
import re,json
rd=lambda p:open(p).read(); wr=lambda p,s:open(p,'w').write(s)
M='SevenIsland_SevaultCanyon'
def box(label,boxes):
    out=label+'::\n'
    for bi,bx in enumerate(boxes):
        for li,l in enumerate(bx):
            assert len(l)<=35,(len(l),l)
            ll=li==len(bx)-1; lb=bi==len(boxes)-1
            out+='    .string "'+l+('$' if ll and lb else '\\p' if ll else '\\n')+'"\n'
    return out
TR=[('BUG_CATCHER_2','MOSS',[('VILEPLUME',68),('ARIADOS',68),('HERACROSS',69)],[["The little guardian sleeps in the","grove. Not one step further."]],["Wilted..."],[["The WARDEN waits at the top."]],(10,4),'DOWN','OBJ_EVENT_GFX_CHANNELER'),
    ('BUG_CATCHER_5','FERN',[('SCIZOR',69),('EXEGGUTOR',69),('NINJASK',70),('MEGANIUM',70)],[["Time folds around it. We keep the","grove from folding with it."]],["Pruned."],[["Keep climbing. It gets greener."]],(12,4),'DOWN','OBJ_EVENT_GFX_BLACK_BELT'),
    ('BUG_CATCHER_6','BRIAR',[('SCEPTILE',70),('SHEDINJA',70),('TANGELA',71),('BEAUTIFLY',71)],[["No one should reach the top alone."]],["Snapped."],[["The WARDEN has felt you coming."]],(14,4),'DOWN','OBJ_EVENT_GFX_CHANNELER'),
    ('BUG_CATCHER_7','THORN',[('HERACROSS',71),('VENUSAUR',71),('ARIADOS',72),('SCIZOR',72)],[["The forest spirit gave us shelter","when the sky turned. We stay."]],["Uprooted."],[["Almost there. Mind your pride."]],(16,4),'DOWN','OBJ_EVENT_GFX_FAT_MAN'),
    ('BUG_CATCHER_8','WARDEN',[('VENUSAUR',72),('SCEPTILE',72),('HERACROSS',73),('MEGANIUM',73),('SCIZOR',74),('SHEDINJA',74)],
        [["I am the WARDEN of the GROVE.","The little one sleeps in my care."],["Prove that your will is worth","more than my fear."]],["...Then the grove has chosen you."],[["Go. Let it sleep after."]],(13,4),'DOWN','OBJ_EVENT_GFX_OLD_WOMAN')]
TF=['FLAG_TEMP_18','FLAG_TEMP_19','FLAG_TEMP_1A','FLAG_TEMP_1C','FLAG_TEMP_1D']
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
      "trainer_type":"TRAINER_TYPE_NORMAL","trainer_sight_or_berry_tree_id":"4","script":f'{M}_EventScript_G{j}',"flag":TF[j]})
wr('src/data/trainers.h',trs); wr('src/data/trainer_parties.h',pa)
mp=f'data/maps/{M}/map.json'; mj=json.load(open(mp)); mj['object_events']+=objs; json.dump(mj,open(mp,'w'),indent=2); open(mp,'a').write('\n')
# EchoSetup : gardiens caches par defaut, reveles a l'etape 10 si non battus
old="SevenIsland_SevaultCanyon_OnTransition::\n\tsetflag FLAG_HIDE_ECHO_SCENE\n"
assert old in s
s=s.replace(old,old+''.join(f'\tsetflag {TF[j]}\n' for j in range(k)),1)
old2="\tclearflag FLAG_HIDE_ECHO_CELEBI\n\treturn\n"
assert s.count(old2)==1
s=s.replace(old2,''.join(f'\tgoto_if_defeated TRAINER_{t[0]}, {M}_Guard{j}_Skip\n\tclearflag {TF[j]}\n{M}_Guard{j}_Skip:\n' for j,t in enumerate(TR))+old2,1)
# Celebi refuse tant qu'un gardien reste
lab=f'{M}_EventScript_Celebi::\n\tgoto_if_questlog EventScript_ReleaseEnd\n\tspecial QuestLog_CutRecording\n\tlock\n\tfaceplayer\n'
assert lab in s
s=s.replace(lab,lab+''.join(f'\tgoto_if_not_defeated TRAINER_{t[0]}, {M}_EventScript_GuardsLeft\n' for t in TR),1)
txt=''
for j,(tid,name,team,a_,b_,c_,pos,face,gfx) in enumerate(TR):
    s+=f'\n{M}_EventScript_G{j}::\n\ttrainerbattle_single TRAINER_{tid}, {M}_Text_G{j}Intro, {M}_Text_G{j}Defeat, {M}_EventScript_G{j}_Vanish\n\tmsgbox {M}_Text_G{j}Post, MSGBOX_AUTOCLOSE\n\tend\n\n{M}_EventScript_G{j}_Vanish::\n\tmsgbox {M}_Text_G{j}Post, MSGBOX_DEFAULT\n\tclosemessage\n\tremoveobject VAR_LAST_TALKED\n\treleaseall\n\tend\n'
    txt+=box(f'{M}_Text_G{j}Intro',a_)+'\n'+box(f'{M}_Text_G{j}Defeat',[b_])+'\n'+box(f'{M}_Text_G{j}Post',c_)+'\n'
s+=f'\n{M}_EventScript_GuardsLeft::\n\tmsgbox {M}_Text_GuardsLeft, MSGBOX_DEFAULT\n\trelease\n\tend\n'
txt+=f'{M}_Text_GuardsLeft::\n    .string "The beast does not stir.\\n"\n    .string "Its guardians still stand watch.$"\n'
wr(sp,s); tp=f'data/maps/{M}/text.inc'; wr(tp,rd(tp)+'\n'+txt); print('ok')
