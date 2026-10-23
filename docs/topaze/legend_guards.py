#!/usr/bin/env python3
"""Gardiens des legendaires deja en place : Zapdos (Centrale), Moltres (sommet Mt Brasier), Articuno (clairiere de Celadon).
Des acolytes (Channelers) + un Oracle barrent les derniers pas avant la bete ; ils n'existent que tant que la bete est la (meme flag HIDE).
Idempotent : marqueur '_Guard0' dans le scripts.inc de la carte."""
import json,re,sys,os,collections
sys.path[:0]=['docs/topaze','tools/topaze/maps']
import route_test as R
rd=lambda p:open(p).read(); wr=lambda p,s:open(p,'w').write(s)
def box(label,boxes):
    out=label+'::\n'
    for bi,bx in enumerate(boxes):
        for li,l in enumerate(bx):
            assert len(l)<=35,(len(l),l)
            ll=li==len(bx)-1; lb=bi==len(boxes)-1
            out+='    .string "'+l+('$' if ll and lb else '\\p' if ll else '\\n')+'"\n'
    return out
POOL=['CHANNELER_1','CHANNELER_2','CHANNELER_3','CHANNELER_4','CHANNELER_5','CHANNELER_6','CHANNELER_7','CHANNELER_8','EXPERT_M','EXPERT_F','DRAGON_TAMER','NINJA_BOY','BATTLE_GIRL','PARASOL_LADY','BOARDER_M','BOARDER_F','COLLECTOR','OLD_COUPLE','SUPER_NERD_1','SUPER_NERD_2','SUPER_NERD_3','BURGLAR_1','BURGLAR_2','BURGLAR_3','BURGLAR_4','COOLTRAINER_PAUL','COOLTRAINER_GILBERT','COOLTRAINER_OWEN','COOLTRAINER_BERKE','COOLTRAINER_SHANNON','COOLTRAINER_BROOKE']
CFG=[
 dict(M='PowerPlant',beast='ZAPDOS',hide='FLAG_HIDE_ZAPDOS',warp=3,span=7,
  tr=[('JOLT',[('RAICHU',62),('ELECTABUZZ',62),('MAGNETON',63)],[["The STORM roars in these halls."],["You are not invited."]],["Fried..."],[["The ORACLE feels the thunder."]]),
      ('WATT',[('ELECTRODE',63),('JOLTEON',63),('MANECTRIC',64)],[["We keep the bird's sky safe."]],["Short circuit..."],[["Keep going, if you dare."]]),
      ('STATIC',[('MAGNETON',64),('ELECTABUZZ',64),('RAICHU',65),('MANECTRIC',65)],[["Hear that hum? It is a warning."]],["Power out..."],[["The ORACLE is just ahead."]]),
      ('TEMPEST',[('JOLTEON',66),('ELECTRODE',66),('MAGNETON',66),('RAICHU',67),('MANECTRIC',67),('ELECTABUZZ',68)],
        [["I am the ORACLE of the STORM.","The bird sleeps under my watch."],["Prove that your spark is worth","more than my fear."]],["...Then the storm has chosen you."],[["Go. Do not waste the lightning."]])]),
 dict(M='MtEmber_Summit',beast='MOLTRES',hide='FLAG_HIDE_MOLTRES',warp=0,span=8,
  tr=[('COAL',[('ARCANINE',62),('MAGMAR',62),('RAPIDASH',63)],[["The mountain's fire is ours to","keep."]],["Burnt out..."],[["The ORACLE stands at the peak."]]),
      ('SOOT',[('FLAREON',63),('HOUNDOOM',63),('CAMERUPT',64)],[["Turn back before you scorch."]],["Smothered..."],[["The heat only grows."]]),
      ('FLARE',[('MAGCARGO',64),('TYPHLOSION',64),('ARCANINE',65),('CHARIZARD',65)],[["The bird warms the whole island."]],["Embers..."],[["The ORACLE is waiting."]]),
      ('SOLARA',[('CHARIZARD',66),('ARCANINE',66),('MAGCARGO',66),('TYPHLOSION',67),('CAMERUPT',67),('RAPIDASH',68)],
        [["I am the ORACLE of the FLAME.","The bird sleeps under my watch."],["Prove that your fire is worth","more than my fear."]],["...Then the flame has chosen you."],[["Go. Keep it burning."]])]),
 dict(M='CeladonCity',beast='ARTICUNO',hide='FLAG_HIDE_ARTICUNO',warp=3,span=9,
  tr=[('FROST',[('LAPRAS',62),('JYNX',62),('CLOYSTER',63)],[["This clearing is closed to","outsiders."]],["Thawed..."],[["The ORACLE does not like noise."]]),
      ('HAIL',[('DEWGONG',63),('GLALIE',63),('WALREIN',64)],[["The cold bird chose this place."]],["Melted..."],[["Quiet, now. Walk softly."]]),
      ('SLEET',[('SNEASEL',64),('PILOSWINE',64),('LAPRAS',65),('JYNX',65)],[["You trampled our snow."]],["Cracked..."],[["The ORACLE is just ahead."]]),
      ('BOREAL',[('WALREIN',66),('LAPRAS',66),('CLOYSTER',66),('GLALIE',67),('JYNX',67),('DEWGONG',68)],
        [["I am the ORACLE of the FROST.","The bird sleeps under my watch."],["Prove that your cold is worth","more than my fear."]],["...Then the frost has chosen you."],[["Go. Tread lightly."]])]),
]
trs=rd('src/data/trainers.h'); pa=rd('src/data/trainer_parties.h')
used=set(re.findall(r'TRAINER_(\w+)',' '.join(rd(f) for f in __import__('glob').glob('data/maps/*/*.inc'))))
free=[p for p in POOL if p not in used]
def conv(tid,name,team,last):
    global trs,pa
    bb=re.search(r'\[TRAINER_%s\] = \{.*?\n    \},'%tid,trs,re.S).group(0)
    nb=re.sub(r'trainerClass = \w+','trainerClass = TRAINER_CLASS_CHANNELER',bb)
    nb=re.sub(r'encounterMusic_gender = [\w |]+','encounterMusic_gender = TRAINER_ENCOUNTER_MUSIC_SUSPICIOUS',nb)
    nb=re.sub(r'trainerPic = \w+','trainerPic = TRAINER_PIC_%s'%('PSYCHIC_F' if last else 'CHANNELER'),nb)
    nb=re.sub(r'trainerName = _\("[^"]*"\)','trainerName = _("%s")'%name,nb)
    nb=re.sub(r'doubleBattle = \w+','doubleBattle = FALSE',nb)
    nb=re.sub(r'aiFlags = [\w |]+','aiFlags = '+('AI_SCRIPT_CHECK_BAD_MOVE | AI_SCRIPT_TRY_TO_FAINT | AI_SCRIPT_CHECK_VIABILITY' if last else 'AI_SCRIPT_CHECK_BAD_MOVE | AI_SCRIPT_TRY_TO_FAINT'),nb)
    sym='sParty_Guard_'+tid
    nb=re.sub(r'\.party = \{[^}]*\}|\.party = \w+\(\w+\)|\.party = \{\.\w+ = \w+\}','.party = {.NoItemDefaultMoves = %s}'%sym,nb) if False else nb
    m=re.search(r'\.party\s*=\s*(\w+)\((\w+)\)',nb)
    if m: nb=nb.replace(m.group(0),'.party = NO_ITEM_DEFAULT_MOVES(%s)'%sym)
    else:
        m=re.search(r'\.party\s*=\s*\{[^}]*\}',nb); assert m,nb
        nb=nb.replace(m.group(0),'.party = NO_ITEM_DEFAULT_MOVES(%s)'%sym)
    trs=trs.replace(bb,nb)
    body=''.join('    {\n        .iv = %d,\n        .lvl = %d,\n        .species = SPECIES_%s,\n    },\n'%(60 if last else 40,lv,sp) for sp,lv in team)
    pa+='\nstatic const struct TrainerMonNoItemDefaultMoves %s[] = {\n%s};\n'%(sym,body)
for c in CFG:
    M=c['M']; sp='data/maps/%s/scripts.inc'%M
    if '%s_Guard0'%M in rd(sp): print('deja',M); continue
    R.SURF=False; nv=R.Nav(M); nv.objs=set()
    mj=json.load(open('data/maps/%s/map.json'%M))
    b=[o for o in mj['object_events'] if o['graphics_id'].endswith('_'+c['beast'])][0]
    w=mj['warp_events'][c['warp']]
    st=None
    for q in [(w['x'],w['y']+1),(w['x'],w['y']-1),(w['x']-1,w['y']),(w['x']+1,w['y'])]:
        if not nv.blocked(*q): st=q;break
    goal=[(b['x']+a,b['y']+d) for a,d in((0,1),(0,-1),(1,0),(-1,0)) if not nv.blocked(b['x']+a,b['y']+d)]
    par={st:None}; qq=collections.deque([st])
    while qq:
        cc=qq.popleft()
        for dx,dy in((0,1),(0,-1),(1,0),(-1,0)):
            m=(cc[0]+dx,cc[1]+dy)
            if m in par or nv.blocked(*m) or not nv.step_ok(cc,m): continue
            par[m]=cc; qq.append(m)
    g=[x for x in goal if x in par][0]
    path=[];cc=g
    while cc: path.append(cc);cc=par[cc]
    path.reverse(); n=len(path); k=len(c['tr'])
    print(M,'chemin',n,'bete',(b['x'],b['y']))
    def reach(blocked):
        seen={st};qq=collections.deque([st])
        while qq:
            cc=qq.popleft()
            for dx,dy in((0,1),(0,-1),(1,0),(-1,0)):
                m=(cc[0]+dx,cc[1]+dy)
                if m in seen or nv.blocked(*m) or not nv.step_ok(cc,m) or m in blocked: continue
                seen.add(m);qq.append(m)
        return any(t in seen for t in goal)
    occ0={(o['x'],o['y']) for o in mj['object_events']}
    # places voulues : de la bete vers l'entree, sur 'span' cases ; oracle le plus pres de la bete
    span=min(c['span'],n-1)
    want=[n-2-int(round((span-1)*j/max(1,k-1))) for j in range(k)]  # j=0 oracle
    placed=[]  # (tile, facing_tile)
    taken=set(occ0)
    def cands(i):
        yield path[i],path[i-1]
        for dx,dy in((0,1),(0,-1),(1,0),(-1,0)):
            t=(path[i][0]+dx,path[i][1]+dy)
            if t not in path and not nv.blocked(*t): yield t,path[i]
    for j,i0_ in enumerate(want):
        done=False
        for d in range(0,n):
            for i in (i0_-d,i0_+d):
                if not 1<=i<n-0 or done: continue
                for t,f in cands(i):
                    if t in taken or t in goal and False: continue
                    if reach({p for p,_ in placed}|{t}):
                        placed.append((t,f)); taken.add(t); done=True; break
            if done: break
    placed=placed[::-1]  # entree -> bete
    k=len(placed); c['tr']=c['tr'][:k-1]+[c['tr'][-1]] if k<len(c['tr']) else c['tr']
    print(' places',placed)
    def face(i):
        a_,b_=placed[i]; b_,a_=a_,b_ ; return None
    occ={(o['x'],o['y']) for o in mj['object_events']}
    gfx=['OBJ_EVENT_GFX_CHANNELER','OBJ_EVENT_GFX_CHANNELER','OBJ_EVENT_GFX_BLACK_BELT','OBJ_EVENT_GFX_OLD_WOMAN']
    scr=rd(sp); txt=''
    tx='data/maps/%s/text.inc'%M
    for j,(name,team,a_,b_,c_) in enumerate(c['tr']):
        tid=free.pop(0); last=j==k-1; conv(tid,name,team,last)
        (x,y),(fx,fy)=placed[j]
        mj['object_events'].append({"type":"object","graphics_id":gfx[j] if j<len(gfx) else gfx[-1],"x":x,"y":y,"elevation":3,"movement_type":"MOVEMENT_TYPE_FACE_"+{(0,1):"DOWN",(0,-1):"UP",(1,0):"RIGHT",(-1,0):"LEFT"}[(fx-x,fy-y)],"movement_range_x":0,"movement_range_y":0,
            "trainer_type":"TRAINER_TYPE_NORMAL","trainer_sight_or_berry_tree_id":"4","script":'%s_Guard%d'%(M,j),"flag":c['hide']})
        scr+=f'\n{M}_Guard{j}::\n\ttrainerbattle_single TRAINER_{tid}, {M}_Text_Guard{j}Intro, {M}_Text_Guard{j}Defeat\n\tmsgbox {M}_Text_Guard{j}Post, MSGBOX_AUTOCLOSE\n\tend\n'
        txt+='\n'+box(f'{M}_Text_Guard{j}Intro',a_)+'\n'+box(f'{M}_Text_Guard{j}Defeat',[b_])+'\n'+box(f'{M}_Text_Guard{j}Post',c_)
    wr(sp,scr)
    new=not os.path.exists(tx)
    wr(tx,(rd(tx) if not new else '')+txt)
    if new:
        f='data/event_scripts.s'; s=rd(f); a='\t.include "data/maps/%s/scripts.inc"\n'%M; assert a in s
        s=s.replace(a,a+'\t.include "data/maps/%s/text.inc"\n'%M,1); wr(f,s)
    json.dump(mj,open('data/maps/%s/map.json'%M,'w'),indent=2); open('data/maps/%s/map.json'%M,'a').write('\n')
    print(' gardes',k)
wr('src/data/trainers.h',trs); wr('src/data/trainer_parties.h',pa)
