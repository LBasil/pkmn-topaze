#!/usr/bin/env python3
"""Routes 13-15 : des dresseurs motards deviennent des sbires Onybris (classe, sprite, textes). Idempotent."""
import re, json
R = '/home/claude/pkmn-topaze'
# (route, nom script, trainer id, texte intro, defeat, post)  ; '|' = saut de ligne, '||' = \p
T = [
 ('Route13','Jared','TRAINER_BIKER_JARED','M',
  'Route 13 is under new|management.','Management will not|like this.','I just keep the road quiet. Others|do the loud work in the towns.'),
 ('Route14','Gerald','TRAINER_BIKER_GERALD','M',
  'Nice bike, kid? No? Then walk|back the way you came.','Wipeout.','We came from every town on this|road. We are not a gang.||We are a union.'),
 ('Route14','Malik','TRAINER_BIKER_MALIK','M',
  'The boss pays better than the|gym ever did.','I still get paid, right?','Ask any of us. We signed up of our|own will. Mostly.'),
 ('Route14','Isaac','TRAINER_BIKER_ISAAC','M',
  'Pedals, crates, orders.|That is my week.','Crate dropped.','Some of us carry stones. I only|carry the bad news.'),
 ('Route15','Ernest','TRAINER_BIKER_ERNEST','M',
  'Stop. This road is closed for|BRANCH business.','...Closed until you win, I guess.','Closed means closed. Next time,|ask before you walk through.'),
 ('Route15','Alex','TRAINER_BIKER_ALEX','M',
  'I used to race for fun. Now I|race for orders.','Out of the race.','The finish line is past the LEAGUE.|That is what they say.'),
]
def fmt(s):
    out=[]
    for para in s.split('||'):
        lines=para.split('|')
        for l in lines: assert len(l)<=35,l
        out.append(lines)
    parts=[]
    for pi,lines in enumerate(out):
        for li,l in enumerate(lines):
            end='\\p' if (pi<len(out)-1 and li==len(lines)-1) else ('\\n' if li<len(lines)-1 else '')
            parts.append(f'    .string "{l}{end}"')
    parts[-1]=parts[-1][:-1]+'$"'
    return '\n'.join(parts)
for route,name,tid,g,i,d,p in T:
    f=f'{R}/data/maps/{route}/text.inc'; t=open(f).read()
    for suf,txt in (('Intro',i),('Defeat',d),('PostBattle',p)):
        pat=re.compile(r'(%s_Text_%s%s::\n)(?:    \.string .*\n)+' % (route,name,suf))
        assert pat.search(t),(route,name,suf)
        t=pat.sub(lambda m:m.group(1)+fmt(txt)+'\n',t)
    open(f,'w').write(t)
    # sprite
    mp=f'{R}/data/maps/{route}/map.json'; j=json.load(open(mp))
    for o in j['object_events']:
        if o['script'].endswith('EventScript_'+name): o['graphics_id']='OBJ_EVENT_GFX_ROCKET_M'
    json.dump(j,open(mp,'w'),indent=2); open(mp,'a').write('\n')
    # classe/pic/musique/nom
    tf=f'{R}/src/data/trainers.h'; s=open(tf).read()
    m=re.search(r'    \[%s\] = \{\n.*?\n    \},\n'%tid,s,re.S); b=m.group(0)
    b2=re.sub(r'\.trainerClass = \w+','.trainerClass = TRAINER_CLASS_TEAM_ROCKET',b)
    b2=re.sub(r'\.encounterMusic_gender = \w+','.encounterMusic_gender = TRAINER_ENCOUNTER_MUSIC_AQUA',b2)
    b2=re.sub(r'\.trainerPic = \w+','.trainerPic = TRAINER_PIC_ROCKET_GRUNT_M',b2)
    b2=re.sub(r'\.trainerName = _\("\w*"\)','.trainerName = _("GRUNT")',b2)
    open(tf,'w').write(s.replace(b,b2))
print('ok')
