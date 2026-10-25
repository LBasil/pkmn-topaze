#!/usr/bin/env python3
"""Echos 2 et 3 : Entei (Cap Brink, ile 2) et Suicune (Pont du Lien, ile 3) vivent dans un repaire cache dans une falaise, garde par des acolytes.
Entei : copie de FourIsland_IcefallCave_B1F (grotte de lave). Suicune : copie de SixIsland_AlteringCave. Idempotent (marqueur : map.json du repaire)."""
import json,re,sys,os,shutil,collections
sys.path[:0]=['docs/topaze','tools/topaze/maps']
import route_test as R, mapkit
rd=lambda p:open(p).read(); wr=lambda p,s:open(p,'w').write(s)
def save(p,m): json.dump(m,open(p,'w'),indent=2); open(p,'a').write('\n')
def box(label,boxes):
    out=label+'::\n'
    for bi,bx in enumerate(boxes):
        for li,l in enumerate(bx):
            assert len(l)<=35,(len(l),l)
            ll=li==len(bx)-1; lb=bi==len(boxes)-1
            out+='    .string "'+l+('$' if ll and lb else '\\p' if ll else '\\n')+'"\n'
    return out
CFG=[dict(
  D='TwoIsland_CapeBrink_EmberDen',P='TwoIsland_CapeBrink',playout='LAYOUT_TWO_ISLAND_CAPE_BRINK',door=(8,24),
  src='MtEmber_RubyPath_B3F',srclay='LAYOUT_MT_EMBER_RUBY_PATH_B3F',srcdir='MtEmber_RubyPath_B3F',mapsec='MAPSEC_TWO_ISLAND',
  need=4,beast='ENTEI',bname='Entei',hide='FLAG_HIDE_ECHO_BEAST2',done='FLAG_ECHO_BEAST2_DONE',after=5,phone='OneIsland_PokemonCenter_1F_EventScript_EchoPhone2',
  locked=[["The rock is warm. Something inside","breathes fire. Not yet."]],
  tr=[('RS_FISHERMAN','EMBER',[('ARCANINE',62),('MAGMAR',62),('RAPIDASH',63)],[["The EMBER hall is closed to","strangers."]],["Burnt out..."],[["Deeper in, the heat is worse."]]),
      ('RS_PICNICKER','BLAZE',[('FLAREON',63),('HOUNDOOM',63),('CAMERUPT',64)],[["Our flame never dies, and neither","do we!"]],["The flame flickers."],[["The ORACLE keeps the last room."]]),
      ('RS_SAILOR','CINDER',[('MAGCARGO',64),('TYPHLOSION',64),('ARCANINE',65),('CHARIZARD',65)],[["The beast gave us warmth when","the sky turned cold."]],["Warmth fades..."],[["Mind the lava. It is hungry."]]),
      ('RS_PKMN_BREEDER_M','ASHE',[('RAPIDASH',65),('MAGMAR',65),('HOUNDOOM',66),('FLAREON',66)],[["You smell of rain. Leave, or","burn!"]],["Only ash remains."],[["The ORACLE is waiting."]]),
      ('RS_PKMN_BREEDER_F','PYRE',[('CHARIZARD',66),('ARCANINE',66),('MAGCARGO',66),('TYPHLOSION',67),('CAMERUPT',67),('RAPIDASH',68)],
        [["I am the ORACLE of the EMBER.","The beast sleeps in my care."],["Prove that your fire is worth","more than my fear."]],["...Then the flame has chosen you."],[["Go. Keep it burning."]])]),
 dict(
  D='ThreeIsland_BondBridge_TideDen',P='ThreeIsland_BondBridge',playout='LAYOUT_THREE_ISLAND_BOND_BRIDGE',door=None,
  src='SixIsland_AlteringCave',srclay='LAYOUT_SIX_ISLAND_ALTERING_CAVE',srcdir='SixIsland_AlteringCave',mapsec='MAPSEC_THREE_ISLAND',
  need=7,beast='SUICUNE',bname='Suicune',hide='FLAG_HIDE_ECHO_BEAST3',done='FLAG_ECHO_BEAST3_DONE',after=8,phone='OneIsland_PokemonCenter_1F_EventScript_EchoPhone3',
  locked=[["Mist rolls out of the cave mouth.","The tide is not ready for you."]],
  tr=[('RS_TWINS','RIPPLE',[('STARMIE',63),('VAPOREON',63),('GYARADOS',64)],[["The TIDE keeps its distance from","strangers."]],["Washed away..."],[["The water runs deeper ahead."]]),
      ('RS_YOUNG_COUPLE','MIST',[('LAPRAS',64),('KINGDRA',64),('POLITOED',65),('SLOWBRO',65)],[["The beast calmed the sea when","the sky broke. We stay for it."]],["The tide turns."],[["The ORACLE will not be so gentle."]]),
      ('RS_SIS_AND_BRO','BROOK',[('BLASTOISE',65),('MILOTIC',66),('STARMIE',66),('LAPRAS',66)],[["You smell of dry land. You do","not belong in the water's hall."]],["Dry as ever..."],[["Almost there. Mind your breath."]]),
      ('RS_CHAMPION','AURORA',[('LAPRAS',66),('MILOTIC',66),('VAPOREON',67),('KINGDRA',67),('BLASTOISE',67),('STARMIE',68)],
        [["I am the ORACLE of the TIDE.","The beast sleeps in my care."],["Prove that your water is worth","more than my fear."]],["...Then the tide has chosen you."],[["Go. Treat the sea kindly."]])]),
 dict(
  D='FiveIsland_Meadow_SteelDen',P='FiveIsland_Meadow',playout='LAYOUT_FIVE_ISLAND_MEADOW',door=(17,28),
  src='MtEmber_RubyPath_B2F',srclay='LAYOUT_MT_EMBER_RUBY_PATH_B2F',srcdir='MtEmber_RubyPath_B2F',mapsec='MAPSEC_FIVE_ISLAND',
  need=13,beast='REGISTEEL',bname='Registeel',hide='FLAG_HIDE_ECHO_BEAST5',done='FLAG_ECHO_BEAST5_DONE',after=14,phone='OneIsland_PokemonCenter_1F_EventScript_EchoPhone5',
  locked=[["The cliff is cold. Something inside","does not rust. Not yet."]],
  tr=[('COOLTRAINER_PAUL','BOLT',[('MAGNETON',66),('SKARMORY',66),('STEELIX',67)],[["Steel does not rust, and neither","does our watch."]],["Rusted through..."],[["The WARDEN is further on."]]),
      ('COOLTRAINER_GILBERT','RIVET',[('SCIZOR',67),('FORRETRESS',67),('AGGRON',68),('MAGNETON',68)],[["The ancient one hums when the","sky cracks. We keep it quiet."]],["Bent out of shape."],[["Keep going. It only gets harder."]]),
      ('COOLTRAINER_OWEN','ALLOY',[('METAGROSS',68),('STEELIX',68),('CLAYDOL',69),('MAWILE',69)],[["No one walks to the shore alone","anymore."]],["The seam gave way."],[["The WARDEN has heard you coming."]]),
      ('COOLTRAINER_BERKE','FORGE',[('AGGRON',69),('SKARMORY',69),('SCIZOR',70),('METAGROSS',70)],[["The beast gave us shelter when","the sky turned. We stay for it."]],["The forge cools."],[["Almost there. Mind your pride."]]),
      ('COOLTRAINER_SHANNON','WARDEN',[('METAGROSS',70),('STEELIX',70),('CLAYDOL',71),('SCIZOR',71),('SKARMORY',72),('AGGRON',72)],
        [["I am the WARDEN of the STEEL.","The beast sleeps in my care."],["Prove that your will is worth","more than my fear."]],["...Then the iron has chosen you."],[["Go. Do not let it rust."]])]),
 dict(
  D='SixIsland_RuinValley_StoneDen',P='SixIsland_RuinValley',playout='LAYOUT_SIX_ISLAND_RUIN_VALLEY',door=None,
  src='MtEmber_RubyPath_B1F',srclay='LAYOUT_MT_EMBER_RUBY_PATH_B1F',srcdir='MtEmber_RubyPath_B1F',mapsec='MAPSEC_SIX_ISLAND',
  need=16,beast='REGIROCK',bname='Regirock',hide='FLAG_HIDE_ECHO_BEAST6',done='FLAG_ECHO_BEAST6_DONE',after=17,phone='OneIsland_PokemonCenter_1F_EventScript_EchoPhone6',
  locked=[["The stone is silent. Inside,","something has waited long."]],
  tr=[('BURGLAR_1','GRAVEL',[('GOLEM',64),('RHYDON',64),('NIDOKING',65)],[["Nothing leaves this valley. Nothing","enters."]],["Crumbled..."],[["Deeper in, the stone is older."]]),
      ('BURGLAR_2','FLINT',[('DONPHAN',65),('ARMALDO',65),('CRADILY',66),('STEELIX',66)],[["The ancient one woke when the sky","cracked. We keep watch."]],["Ground to dust."],[["The WARDEN does not bend."]]),
      ('BURGLAR_3','SLATE',[('TYRANITAR',66),('GOLEM',67),('RHYDON',67),('AGGRON',67)],[["Turn back. Stone remembers","everything."]],["The wall gave way."],[["Mind your footing ahead."]]),
      ('BURGLAR_4','CAIRN',[('NIDOKING',67),('DONPHAN',68),('ARMALDO',68),('CRADILY',68)],[["The beast shelters us from the","broken sky. We stay for it."]],["The cairn falls."],[["Last room. Mind your pride."]]),
      ('SUPER_NERD_1','WARDEN',[('TYRANITAR',68),('GOLEM',69),('RHYDON',69),('STEELIX',70),('AGGRON',70),('ARMALDO',70)],
        [["I am the WARDEN of the STONE.","The beast sleeps in my care."],["Prove that your will is worth","more than my fear."]],["...Then the stone has chosen you."],[["Go. Let it rest after."]])])]
def pick_door(c):
    R.SURF=False; nv=R.Nav(c['P']); nv.objs=set(); L=mapkit.Layout(c['playout'])
    mj=json.load(open('data/maps/%s/map.json'%c['P']))
    srcs=[]
    for w in mj['warp_events']:
        for q in [(w['x'],w['y']+1),(w['x'],w['y']-1),(w['x']-1,w['y']),(w['x']+1,w['y'])]:
            if not nv.blocked(*q): srcs.append(q); break
    for x in range(nv.w):
        for y in (0,nv.h-1):
            if not nv.blocked(x,y): srcs.append((x,y))
    seen=set(srcs); q=collections.deque(srcs)
    while q:
        cc=q.popleft()
        for dx,dy in((0,1),(0,-1),(1,0),(-1,0)):
            m=(cc[0]+dx,cc[1]+dy)
            if m in seen or nv.blocked(*m) or not nv.step_ok(cc,m): continue
            seen.add(m); q.append(m)
    occ={(o['x'],o['y']) for o in mj['object_events']}
    cands=[]
    for x in range(2,nv.w-2):
        for y in range(2,nv.h-1):
            v=L.get(x,y)
            if (v&0x3ff) in (0x78,0x79,0x7a) and (v>>10)&3 and (x,y+1) in seen and (x,y+1) not in occ and ((L.get(x-1,y)>>10)&3) and ((L.get(x+1,y)>>10)&3) and ((L.get(x,y-1)>>10)&3):
                cands.append((x,y))
    return cands
for c in CFG:
    D,P=c['D'],c['P']
    if os.path.exists('data/maps/%s/map.json'%D): print('already',D); continue
    if c['door'] is None:
        cd=pick_door(c); print('candidats porte',P,cd[:12]); c['door']=cd[len(cd)//2]
    dx,dy=c['door']
    # layout copie
    os.makedirs('data/layouts/'+D,exist_ok=True)
    for f in ('map.bin','border.bin'): shutil.copy('data/layouts/%s/%s'%(c['srcdir'],f),'data/layouts/%s/%s'%(D,f))
    lj=json.load(open('data/layouts/layouts.json')); src=[l for l in lj['layouts'] if l.get('id')==c['srclay']][0]
    lid='LAYOUT_'+re.sub(r'(?<!^)(?=[A-Z0-9])','_',D).upper().replace('__','_')
    new=dict(src); new['id']=lid; new['name']=D+'_Layout'; new['border_filepath']='data/layouts/%s/border.bin'%D; new['blockdata_filepath']='data/layouts/%s/map.bin'%D
    lj['layouts'].append(new); save('data/layouts/layouts.json',lj)
    # bouche de grotte dans le parent
    L=mapkit.Layout(c['playout']); i=dy*L.w+dx; L.g[i]=(L.g[i]&~0x3ff&~(3<<10))|0xa9; L.save()
    pj=json.load(open('data/maps/%s/map.json'%P))
    pj['warp_events'].append({"x":dx,"y":dy,"elevation":0,"dest_map":"MAP_"+lid[7:],"dest_warp_id":"0"})
    pw=len(pj['warp_events'])-1
    for o in pj['object_events']:
        if c['beast'] in o['graphics_id']: pj['object_events'].remove(o); break
    pj.setdefault('coord_events',[])
    for v in range(c['need']):
        pj['coord_events'].append({"type":"trigger","x":dx,"y":dy+1,"elevation":0,"var":"VAR_ECHO_STAGE","var_value":str(v),"script":P+"_EventScript_DenLocked"})
    save('data/maps/%s/map.json'%P,pj)
    s=rd('data/maps/%s/scripts.inc'%P)
    s+=f"\n@ Topaze: la bouche de grotte ({dx},{dy}) reste fermee tant que l'Echo n'est pas ouvert\n{P}_EventScript_DenLocked::\n\tlockall\n\tmsgbox {P}_Text_DenLocked\n\tapplymovement LOCALID_PLAYER, {P}_Movement_DenBack\n\twaitmovement 0\n\treleaseall\n\tend\n\n{P}_Movement_DenBack::\n\twalk_down\n\tstep_end\n"
    # plus de bete dehors : OnTransition neutre
    wr('data/maps/%s/scripts.inc'%P,s)
    tp='data/maps/%s/text.inc'%P
    t=(rd(tp) if os.path.exists(tp) else '')+'\n'+box(P+'_Text_DenLocked',c['locked'])
    wr(tp,t)
    # carte du repaire
    sm=json.load(open('data/maps/%s/map.json'%c['src']))
    mj=dict(sm); mj['id']='MAP_'+lid[7:]; mj['name']=D; mj['layout']=lid; mj['region_map_section']=c['mapsec']; mj['weather']='WEATHER_NONE'; mj['connections']=None
    nw=len(sm['warp_events'])
    mj['warp_events']=[{"x":w['x'],"y":w['y'],"elevation":0,"dest_map":"MAP_"+P.upper() if False else "MAP_"+re.sub(r'(?<!^)(?=[A-Z0-9])','_',P).upper().replace('__','_'),"dest_warp_id":str(pw)} for w in sm['warp_events']]
    mj['coord_events']=[]; mj['bg_events']=[]
    R.SURF=False; nv=R.Nav(c['src']); nv.objs=set()
    wp=sm['warp_events'][0]; st=None
    for q in [(wp['x'],wp['y']+1),(wp['x'],wp['y']-1),(wp['x']-1,wp['y']),(wp['x']+1,wp['y'])]:
        if not nv.blocked(*q): st=q; break
    par={st:None}; dist={st:0}; qq=collections.deque([st])
    while qq:
        cc=qq.popleft()
        for ddx,ddy in((0,1),(0,-1),(1,0),(-1,0)):
            m=(cc[0]+ddx,cc[1]+ddy)
            if m in par or nv.blocked(*m) or not nv.step_ok(cc,m): continue
            par[m]=cc; dist[m]=dist[cc]+1; qq.append(m)
    warps={(w['x'],w['y']) for w in sm['warp_events']}
    far=max([p for p in dist if p not in warps and all(abs(p[0]-w[0])+abs(p[1]-w[1])>2 for w in warps)],key=lambda p:dist[p])
    path=[]; cc=far
    while cc: path.append(cc); cc=par[cc]
    path.reverse(); n=len(path); print(D,'chemin',n,'bete',far)
    def face(i):
        a_,b_=path[i],path[i-1]; return {(0,1):'DOWN',(0,-1):'UP',(1,0):'RIGHT',(-1,0):'LEFT'}[(b_[0]-a_[0],b_[1]-a_[1])]
    def trn(gfx,i,script):
        x,y=path[i]; return {"type":"object","graphics_id":gfx,"x":x,"y":y,"elevation":3,"movement_type":"MOVEMENT_TYPE_FACE_"+face(i),"movement_range_x":0,"movement_range_y":0,
          "trainer_type":"TRAINER_TYPE_NORMAL","trainer_sight_or_berry_tree_id":"4","script":script,"flag":"0"}
    k=len(c['tr']); idx=[max(3,int((n-3)*(j+1)/(k+0.4))) for j in range(k)]
    # trainers
    trs=rd('src/data/trainers.h'); pa=rd('src/data/trainer_parties.h'); objs=[]
    gfxs=['OBJ_EVENT_GFX_CHANNELER','OBJ_EVENT_GFX_CHANNELER','OBJ_EVENT_GFX_BLACK_BELT','OBJ_EVENT_GFX_FAT_MAN','OBJ_EVENT_GFX_OLD_WOMAN']
    for j,(tid,name,team,a_,b_,c_) in enumerate(c['tr']):
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
        objs.append(trn(gfxs[j] if not last else gfxs[4],idx[j],'%s_EventScript_T%d'%(D,j)))
    wr('src/data/trainers.h',trs); wr('src/data/trainer_parties.h',pa)
    bx,by=far
    objs.append({"local_id":"LOCALID_DEN_BEAST","type":"object","graphics_id":"OBJ_EVENT_GFX_"+c['beast'],"x":bx,"y":by,"elevation":3,"movement_type":"MOVEMENT_TYPE_FACE_DOWN","movement_range_x":0,"movement_range_y":0,
       "trainer_type":"TRAINER_TYPE_NONE","trainer_sight_or_berry_tree_id":"0","script":D+"_EventScript_Beast","flag":c['hide']})
    mj['object_events']=objs; os.makedirs('data/maps/'+D,exist_ok=True); save('data/maps/%s/map.json'%D,mj)
    # scripts / textes
    scr=f"""{D}_MapScripts::
	map_script MAP_SCRIPT_ON_TRANSITION, {D}_OnTransition
	.byte 0

{D}_OnTransition::
	goto_if_set {c['done']}, {D}_EventScript_HideBeast
	goto_if_ne VAR_ECHO_STAGE, {c['need']}, {D}_EventScript_HideBeast
	clearflag {c['hide']}
	end

{D}_EventScript_HideBeast::
	setflag {c['hide']}
	end
"""
    txt=''
    for j,(tid,name,team,a_,b_,c_) in enumerate(c['tr']):
        scr+=f'\n{D}_EventScript_T{j}::\n\ttrainerbattle_single TRAINER_{tid}, {D}_Text_T{j}Intro, {D}_Text_T{j}Defeat\n\tmsgbox {D}_Text_T{j}Post, MSGBOX_AUTOCLOSE\n\tend\n'
        txt+=box(f'{D}_Text_T{j}Intro',a_)+'\n'+box(f'{D}_Text_T{j}Defeat',[b_])+'\n'+box(f'{D}_Text_T{j}Post',c_)+'\n'
    B=c['beast']
    scr+=f"""
{D}_EventScript_Beast::
	goto_if_questlog EventScript_ReleaseEnd
	special QuestLog_CutRecording
	lock
	faceplayer
	setwildbattle SPECIES_{B}, 0
	waitse
	playmoncry SPECIES_{B}, CRY_MODE_ENCOUNTER
	delay 40
	waitmoncry
	setflag FLAG_SYS_SPECIAL_WILD_BATTLE
	special StartLegendaryBattle
	waitstate
	clearflag FLAG_SYS_SPECIAL_WILD_BATTLE
	specialvar VAR_RESULT, GetBattleOutcome
	goto_if_eq VAR_RESULT, B_OUTCOME_WON, {D}_EventScript_DefeatedBeast
	goto_if_eq VAR_RESULT, B_OUTCOME_RAN, {D}_EventScript_RanFromBeast
	goto_if_eq VAR_RESULT, B_OUTCOME_PLAYER_TELEPORTED, {D}_EventScript_RanFromBeast
	setflag {c['done']}
	setflag {c['hide']}
	fadescreen FADE_TO_BLACK
	removeobject VAR_LAST_TALKED
	fadescreen FADE_FROM_BLACK
	setvar VAR_ECHO_STAGE, {c['after']}
	goto {c['phone']}
	end

{D}_EventScript_DefeatedBeast::
	setflag {c['done']}
	setvar VAR_ECHO_STAGE, {c['after']}
	fadescreen FADE_TO_BLACK
	removeobject VAR_LAST_TALKED
	fadescreen FADE_FROM_BLACK
	goto {c['phone']}
	end

{D}_EventScript_RanFromBeast::
	setvar VAR_0x8004, SPECIES_{B}
	goto EventScript_MonFlewAway
	end
"""
    wr(f'data/maps/{D}/scripts.inc',scr); wr(f'data/maps/{D}/text.inc',txt.rstrip('\n')+'\n')
    j2=json.load(open('data/maps/map_groups.json'))
    if D not in j2['gMapGroup_SpecialArea']: j2['gMapGroup_SpecialArea'].append(D)
    save('data/maps/map_groups.json',j2)
    f='data/event_scripts.s'; s=rd(f); anchor='\t.include "data/maps/%s/scripts.inc"\n'%P; assert anchor in s
    s=s.replace(anchor,anchor+'\t.include "data/maps/%s/scripts.inc"\n'%D,1)
    anchor='\t.include "data/maps/%s/text.inc"\n'%P
    if anchor not in s:
        a2='\t.include "data/maps/%s/scripts.inc"\n'%P+'\t.include "data/maps/%s/scripts.inc"\n'%D
        s=s.replace(a2,a2+anchor,1)
    s=s.replace(anchor,anchor+'\t.include "data/maps/%s/text.inc"\n'%D,1); wr(f,s)
    print('ok',D,'porte',(dx,dy),'idx',idx)
