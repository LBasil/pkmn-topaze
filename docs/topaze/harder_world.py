"""Topaze: dresseurs et hautes herbes plus difficiles. Usage: python3 harder_world.py <repo>"""
import re,sys,json
repo=sys.argv[1]
# 1) Dresseurs: +12% de niveau (min +1), sauf champions d'arène, Conseil des 4 et Ligue
p=repo+'/src/data/trainer_parties.h'
s=open(p).read()
parts=re.split(r'(static const struct TrainerMon\w+ sParty_\w+\[\] = \{)',s)
out=[parts[0]]; n=0
for i in range(1,len(parts),2):
    head,body=parts[i],parts[i+1]
    name=re.search(r'sParty_(\w+)\[\]',head).group(1)
    if not re.match(r'(Leader|EliteFour|Champion|RSChampion)',name):
        def bump(m):
            global n
            lv=int(m.group(1)); n+=1
            return '.lvl = %d,'%min(100,lv+max(1,round(lv*0.12)))
        body=re.sub(r'\.lvl = (\d+),',bump,body)
    out+= [head,body]
open(p,'w').write(''.join(out)); print('niveaux dresseurs modifiés:',n)
# 2) Hautes herbes: +2 niveaux (<10) ou +3, hors Unown
j=repo+'/src/data/wild_encounters.json'
d=json.load(open(j,encoding='utf-8')); k=0
for g in d['wild_encounter_groups']:
    for e in g['encounters']:
        lm=e.get('land_mons')
        if not lm: continue
        for m in lm['mons']:
            if m['species']=='SPECIES_UNOWN': continue
            add=2 if m['max_level']<10 else 3
            m['min_level']=min(100,m['min_level']+add); m['max_level']=min(100,m['max_level']+add); k+=1
json.dump(d,open(j,'w',encoding='utf-8'),indent=2,ensure_ascii=False)
print('rencontres herbes modifiées:',k)
