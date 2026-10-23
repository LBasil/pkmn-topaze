#!/usr/bin/env python3
"""Les gardiens (repaires 1-3, oiseaux) disparaissent une fois battus : un dresseur battu reste debout sur sa case et bloquerait un couloir d'une case.
Chaque gardien recoit un flag FLAG_0x136+ (cache = vrai), pose apres le combat ; apres victoire : texte, puis removeobject.
Pour les oiseaux : les gardiens sont caches par defaut et reveles avec la bete (OnTransition). Idempotent (marqueur '_Vanish')."""
import json,re,os
rd=lambda p:open(p).read(); wr=lambda p,s:open(p,'w').write(s)
MAPS=[('OneIsland_KindleRoad_StormDen','T',None),('TwoIsland_CapeBrink_EmberDen','T',None),('ThreeIsland_BondBridge_TideDen','T',None),
      ('PowerPlant','Guard','ZAPDOS'),('MtEmber_Summit','Guard','MOLTRES'),('CeladonCity','Guard','ARTICUNO')]
nxt=0x136
def flag(i): return 'FLAG_0x%03X'%i
for M,pre,bird in MAPS:
    sp='data/maps/%s/scripts.inc'%M; s=rd(sp)
    if '_Vanish::' in s: print('deja',M); continue
    mj=json.load(open('data/maps/%s/map.json'%M)); fl=[]
    labs=re.findall(r'^(\w+)::\n\ttrainerbattle_single',s,re.M)
    for lab in labs:
        m=re.search(r'%s::\n\ttrainerbattle_single (TRAINER_\w+), (\w+), (\w+)\n\tmsgbox (\w+), MSGBOX_AUTOCLOSE\n\tend\n'%re.escape(lab),s); assert m,lab
        f=flag(nxt); nxt+=1; fl.append((m.group(1),f))
        s=s.replace(m.group(0),f'{lab}::\n\ttrainerbattle_single {m.group(1)}, {m.group(2)}, {m.group(3)}, {lab}_Vanish\n\tmsgbox {m.group(4)}, MSGBOX_AUTOCLOSE\n\tend\n\n{lab}_Vanish::\n\tmsgbox {m.group(4)}, MSGBOX_DEFAULT\n\tclosemessage\n\tsetflag {f}\n\tremoveobject VAR_LAST_TALKED\n\treleaseall\n\tend\n')
        for o in mj['object_events']:
            if o.get('script')==lab: o['flag']=f
    assert fl,M
    if bird:
        # caches par defaut ; reveles avec la bete
        sets=''.join(f'\tsetflag {f}\n' for _,f in fl)
        rev=''.join(f'\tgoto_if_defeated {t}, {M}_Guards_Skip{i}\n\tclearflag {f}\n{M}_Guards_Skip{i}:\n' for i,(t,f) in enumerate(fl))
        s=s.replace('%s_OnTransition::\n'%M,'%s_OnTransition::\n%s\tgoto_if_set FLAG_FOUGHT_%s, %s_Guards_Done\n\tgoto_if_unset FLAG_TOPAZE_POSTGAME, %s_Guards_Done\n%s%s_Guards_Done:\n'%(M,sets,bird,M,M,rev,M),1)
    wr(sp,s)
    json.dump(mj,open('data/maps/%s/map.json'%M,'w'),indent=2); open('data/maps/%s/map.json'%M,'a').write('\n')
    print(M,fl)
