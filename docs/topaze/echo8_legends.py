#!/usr/bin/env python3
"""Echo 7 finale : vrais sprites (Pokedex reduit) pour Kyogre/Groudon/Rayquaza/Latias/Latios/Jirachi (GFX 156-161, tags 0x1125-0x112A)
+ 4 gardiens qui bouchent les 2 escaliers du plateau a l'etape >=22 (flags TEMP 11,14,1E,1F). Idempotent."""
import re,json,sys
sys.path.insert(0,'docs/topaze')
import beast_sprites as B
rd=lambda p:open(p).read(); wr=lambda p,s:open(p,'w').write(s)
N=['kyogre','groudon','rayquaza','latias','latios','jirachi']
C=['Kyogre','Groudon','Rayquaza','Latias','Latios','Jirachi']
if 'OBJ_EVENT_GFX_KYOGRE' in rd('include/constants/event_objects.h'): print('deja'); raise SystemExit
for n in N:
    im,cols=B.build_dex(n); im.save(B.R+f'graphics/object_events/pics/pokemon/{n}.png')
    open(B.R+f'graphics/object_events/palettes/{n}.pal','w',newline='').write('JASC-PAL\r\n0100\r\n16\r\n'+''.join('%d %d %d\r\n'%c for c in cols))
p='include/constants/event_objects.h'; s=rd(p)
s=s.replace('#define NUM_OBJ_EVENT_GFX     156',''.join(f'#define OBJ_EVENT_GFX_{n.upper()} {156+i}\n' for i,n in enumerate(N))+'\n#define NUM_OBJ_EVENT_GFX     162'); wr(p,s)
p='src/data/object_events/object_event_graphics.h'; s=rd(p)
a='const u16 gObjectEventPic_Registeel[]'; i=s.index(a); i=s.index('\n',i)+1
s=s[:i]+''.join(f'const u16 gObjectEventPic_{c}[] = INCBIN_U16("graphics/object_events/pics/pokemon/{n}.4bpp");\n' for c,n in zip(C,N))+s[i:]
a='const u16 gObjectEventPal_TopazeRegisteel[]'; i=s.index(a); i=s.index('\n',i)+1
s=s[:i]+''.join(f'const u16 gObjectEventPal_Topaze{c}[] = INCBIN_U16("graphics/object_events/palettes/{n}.gbapal");\n' for c,n in zip(C,N))+s[i:]; wr(p,s)
p='src/event_object_movement.c'; s=rd(p)
a='#define OBJ_EVENT_PAL_TAG_TOPAZE_REGISTEEL            0x1124\n'
s=s.replace(a,a+''.join(f'#define OBJ_EVENT_PAL_TAG_TOPAZE_{c.upper()}'.ljust(60)+f'0x{0x1125+i:04X}\n' for i,c in enumerate(C)))
a='    {gObjectEventPal_TopazeRegisteel,         OBJ_EVENT_PAL_TAG_TOPAZE_REGISTEEL},\n'
s=s.replace(a,a+''.join(f'    {{gObjectEventPal_Topaze{c},'.ljust(46)+f'OBJ_EVENT_PAL_TAG_TOPAZE_{c.upper()}}},\n' for c in C)); wr(p,s)
p='src/data/object_events/object_event_pic_tables.h'; s=rd(p)
s+=''.join(f'\nstatic const struct SpriteFrameImage sPicTable_{c}[] = {{\n'+''.join(f'    overworld_frame(gObjectEventPic_{c}, 4, 4, 0),\n' for _ in range(9))+'};\n' for c in C); wr(p,s)
p='src/data/object_events/object_event_graphics_info.h'; s=rd(p)
for c in C:
    s+=f'''
const struct ObjectEventGraphicsInfo gObjectEventGraphicsInfo_{c} = {{
    .tileTag = TAG_NONE,
    .paletteTag = OBJ_EVENT_PAL_TAG_TOPAZE_{c.upper()},
    .reflectionPaletteTag = OBJ_EVENT_PAL_TAG_NONE,
    .size = 512,
    .width = 32,
    .height = 32,
    .paletteSlot = PALSLOT_NPC_SPECIAL,
    .shadowSize = SHADOW_SIZE_M,
    .inanimate = FALSE,
    .disableReflectionPaletteLoad = FALSE,
    .tracks = TRACKS_FOOT,
    .oam = &gObjectEventBaseOam_32x32,
    .subspriteTables = gObjectEventSpriteOamTables_32x32,
    .anims = sAnimTable_Standard,
    .images = sPicTable_{c},
    .affineAnims = gDummySpriteAffineAnimTable,
}};
'''
wr(p,s)
p='src/data/object_events/object_event_graphics_info_pointers.h'; s=rd(p)
a='const struct ObjectEventGraphicsInfo gObjectEventGraphicsInfo_Regice;\n'
s=s.replace(a,a+''.join(f'const struct ObjectEventGraphicsInfo gObjectEventGraphicsInfo_{c};\n' for c in C))
a='    [OBJ_EVENT_GFX_REGISTEEL]'; i=s.index(a); i=s.index('\n',i)+1
s=s[:i]+''.join(f'    [OBJ_EVENT_GFX_{c.upper()}]'.ljust(45)+f'= &gObjectEventGraphicsInfo_{c},\n' for c in C)+s[i:]; wr(p,s)
# map : sprites + gardiens
M='SevenIsland_SevaultCanyon'
mp=f'data/maps/{M}/map.json'; mj=json.load(open(mp))
for o in mj['object_events']:
    for c in C:
        if o['script']==f'{M}_EventScript_{c}': o['graphics_id']='OBJ_EVENT_GFX_'+c.upper()
def box(label,bx):
    out=label+'::\n'
    for li,l in enumerate(bx):
        assert len(l)<=35,l; out+='    .string "'+l+('$' if li==len(bx)-1 else '\\n')+'"\n'
    return out
G=[('COOLTRAINER_BROOKE','TIDE',[('KINGDRA',72),('GYARADOS',72),('LAPRAS',73),('MILOTIC',73)],["The tide keeps this canyon.","Turn back, or be washed away."],"Ebbed...","Left stair is open. Mind the top.",(9,6),'OBJ_EVENT_GFX_CHANNELER','FLAG_TEMP_11'),
   ('COOLTRAINER_AUSTINA','MAGMA',[('CAMERUPT',72),('TYPHLOSION',73),('FLAREON',73),('MAGCARGO',74)],["Fire and earth sleep above.","None wake them on my watch."],"Burnt out...","The way is open.",(10,6),'OBJ_EVENT_GFX_BLACK_BELT','FLAG_TEMP_14'),
   ('COOLTRAINER_JULIE','GALE',[('SALAMENCE',73),('DRAGONITE',73),('ALTARIA',74),('FLYGON',74)],["The sky dragon dreams up there.","You must earn the wind first."],"Grounded...","Go on. The wind allows it.",(17,6),'OBJ_EVENT_GFX_CHANNELER','FLAG_TEMP_1E'),
   ('SUPER_NERD_2','DREAM',[('ALAKAZAM',74),('GARDEVOIR',74),('ESPEON',75),('STARMIE',75),('SLOWKING',75),('MEWTWO',76)],["I am the last guardian of the","dreamers. The eon twins and the","wish star rest behind me."],"Awake at last...","Go. Be gentle with them.",(18,6),'OBJ_EVENT_GFX_OLD_WOMAN','FLAG_TEMP_1F')]
trs=rd('src/data/trainers.h'); pa=rd('src/data/trainer_parties.h'); objs=[]
for j,(tid,name,team,a_,b_,c_,pos,gfx,fl) in enumerate(G):
    last=j==3
    bb=re.search(r'\[TRAINER_%s\] = \{.*?\n    \},'%tid,trs,re.S).group(0)
    nb=re.sub(r'trainerClass = \w+','trainerClass = TRAINER_CLASS_CHANNELER',bb)
    nb=re.sub(r'encounterMusic_gender = [\w |]+','encounterMusic_gender = TRAINER_ENCOUNTER_MUSIC_SUSPICIOUS',nb)
    nb=re.sub(r'trainerPic = \w+','trainerPic = TRAINER_PIC_%s'%('PSYCHIC_F' if last else 'CHANNELER'),nb)
    nb=re.sub(r'trainerName = _\("[^"]*"\)','trainerName = _("%s")'%name,nb)
    nb=re.sub(r'doubleBattle = \w+','doubleBattle = FALSE',nb)
    nb=re.sub(r'aiFlags = [\w |]+','aiFlags = AI_SCRIPT_CHECK_BAD_MOVE | AI_SCRIPT_TRY_TO_FAINT | AI_SCRIPT_CHECK_VIABILITY',nb)
    sym=re.search(r'MOVES\((\w+)\)',nb).group(1)
    nb=re.sub(r'(?:NO_)?ITEM_(?:DEFAULT|CUSTOM)_MOVES\(','NO_ITEM_DEFAULT_MOVES(',nb)
    trs=trs.replace(bb,nb)
    m=re.search(r'static const struct TrainerMon\w+ %s\[\] = \{.*?\};'%sym,pa,re.S); assert m,sym
    body=''.join('    {\n        .iv = 60,\n        .lvl = %d,\n        .species = SPECIES_%s,\n    },\n'%(lv,sp_) for sp_,lv in team)
    pa=pa.replace(m.group(0),'static const struct TrainerMonNoItemDefaultMoves %s[] = {\n%s};'%(sym,body))
    objs.append({"type":"object","graphics_id":gfx,"x":pos[0],"y":pos[1],"elevation":3,"movement_type":"MOVEMENT_TYPE_FACE_DOWN","movement_range_x":0,"movement_range_y":0,
      "trainer_type":"TRAINER_TYPE_NORMAL","trainer_sight_or_berry_tree_id":"3","script":f'{M}_EventScript_W{j}',"flag":fl})
wr('src/data/trainers.h',trs); wr('src/data/trainer_parties.h',pa)
mj['object_events']+=objs; json.dump(mj,open(mp,'w'),indent=2); open(mp,'a').write('\n')
sp=f'data/maps/{M}/scripts.inc'; s=rd(sp)
old="SevenIsland_SevaultCanyon_OnTransition::\n\tsetflag FLAG_HIDE_ECHO_SCENE\n"; assert old in s
s=s.replace(old,old+''.join(f'\tsetflag {g[8]}\n' for g in G)+f'\tcall_if_eq VAR_ECHO_STAGE, 22, {M}_EventScript_ShowWardens\n',1)
txt=''
for j,(tid,name,team,a_,b_,c_,pos,gfx,fl) in enumerate(G):
    s+=f'\n{M}_EventScript_W{j}::\n\ttrainerbattle_single TRAINER_{tid}, {M}_Text_W{j}Intro, {M}_Text_W{j}Defeat, {M}_EventScript_W{j}_Vanish\n\tmsgbox {M}_Text_W{j}Post, MSGBOX_AUTOCLOSE\n\tend\n\n{M}_EventScript_W{j}_Vanish::\n\tmsgbox {M}_Text_W{j}Post, MSGBOX_DEFAULT\n\tclosemessage\n\tremoveobject VAR_LAST_TALKED\n\treleaseall\n\tend\n'
    txt+=box(f'{M}_Text_W{j}Intro',a_)+'\n'+box(f'{M}_Text_W{j}Defeat',[b_])+'\n'+box(f'{M}_Text_W{j}Post',[c_])+'\n'
s+=f'\n{M}_EventScript_ShowWardens::\n'+''.join(f'\tgoto_if_defeated TRAINER_{g[0]}, {M}_Warden{j}_Skip\n\tclearflag {g[8]}\n{M}_Warden{j}_Skip:\n' for j,g in enumerate(G))+'\treturn\n'
wr(sp,s); tp=f'data/maps/{M}/text.inc'; wr(tp,rd(tp)+'\n'+txt); print('ok')
