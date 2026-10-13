#!/usr/bin/env python3
"""Génère docs/scenario/OPANIHRUM.md : PNJ, panneaux et scènes d'Opanihrum, textes extraits du code."""
import re,os,sys,json
sys.dont_write_bytecode=True
R=os.path.join(os.path.dirname(__file__),'..','..')
def texts(m):
    s=open(f'{R}/data/maps/{m}/text.inc').read(); out={}
    for lab,body in re.findall(r'^(\w+)::\n((?:\s*\.string[^\n]*\n)+)',s,re.M):
        t=''.join(re.findall(r'"([^"]*)"',body))
        out[lab]=t.replace('\\n','\n').replace('\\l','\n').replace('\\p','\n— — —\n').replace('$','')
    return out
def blocks(m):
    s=open(f'{R}/data/maps/{m}/scripts.inc').read(); b={}
    for lab,body in re.findall(r'^(\w+)::\n(.*?)(?=^\w+::|\Z)',s,re.M|re.S): b[lab]=body
    return b
MAPS=[('ViridianCity','Les rues d’Opanihrum'),('ViridianCity_Mart','Boutique'),('ViridianCity_House','Maison'),('ViridianCity_School','École'),('ViridianCity_PokemonCenter_1F','Centre Pokémon')]
md=['''# Opanihrum — script détaillé (parcours du joueur)
*Généré par `docs/scenario/gen_opanihrum.py` à partir du code : toujours à jour. Textes = placeholders anglais.*

## Chronologie du joueur
1. **Arrivée** par la Route 1 (sud). Ville ordinaire : aucune scène à l’arrivée.
2. **Boutique** : services d’origine (POKé BALL, POTION, ANTIDOTE, PARALYZE HEAL). Plus de colis de Chêne (supprimé le 13/10).
3. **Vieil homme** (18,6) : plus de barrage ni de déclencheur automatique. En lui parlant : « Je te montre comment capturer ? » **OUI/NON** ; OUI = démonstration de capture puis **TEACHY TV** (`FLAG_VIRIDIAN_TUTORIAL_DONE`) ; NON = « reviens quand tu veux ».
4. **Arène (la Fonderie, Hepha, Acier)** : portes verrouillées tant que les badges 1 à 7 ne sont pas tous obtenus ; message + saut en arrière.
5. Centre Pokémon et boutique : services d’origine (boutique : POKé BALL, POTION, ANTIDOTE, PARALYZE HEAL).

''']
for m,title in MAPS:
    T=texts(m); B=blocks(m); d=json.load(open(f'{R}/data/maps/{m}/map.json'))
    md.append(f'## {title} (`{m}`)\n')
    items=[]
    for o in d.get('object_events',[]): items.append((f"PNJ {o['graphics_id'].replace('OBJ_EVENT_GFX_','')} ({o['x']},{o['y']})",o['script']))
    for b in d.get('bg_events',[]):
        if b['type']=='sign': items.append((f"Panneau ({b['x']},{b['y']})",b['script']))
    seen=set()
    for who,sc in items:
        if sc in seen or sc in('0','') : continue
        seen.add(sc)
        body=B.get(sc,'')
        labs=re.findall(r'msgbox (\w+)',body)
        gotos=re.findall(r'goto(?:_if_\w+)? (?:[^,\n]+, )*(\w+)',body)
        for g in gotos:
            if g in B and g!=sc: labs+=re.findall(r'msgbox (\w+)',B[g])
        labs=[l for i,l in enumerate(labs) if l in T and l not in labs[:i]]
        md.append(f'**{who}** — `{sc}`\n')
        if not labs: md.append('> *(texte d’origine FireRed ou service)*\n')
        for l in labs: md.append('\n'.join('> '+x for x in T[l].split('\n'))+'\n')
open(f'{R}/docs/scenario/OPANIHRUM.md','w').write('\n'.join(md))
