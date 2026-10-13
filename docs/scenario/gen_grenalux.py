#!/usr/bin/env python3
"""Génère docs/scenario/GRENALUX.md : le script détaillé de Grenalux, textes extraits du code."""
import re,os,sys
sys.dont_write_bytecode=True
R=os.path.join(os.path.dirname(__file__),'..','..')
def texts(m):
    s=open(f'{R}/data/maps/{m}/text.inc').read()
    out={}
    for lab,body in re.findall(r'^(\w+)::\n((?:\s*\.string[^\n]*\n)+)',s,re.M):
        t=''.join(re.findall(r'"([^"]*)"',body))
        t=t.replace('\\n','\n').replace('\\l','\n').replace('\\p','\n— — —\n').replace('$','')
        out[lab]=t
    return out
TX={m:texts(m) for m in ['PalletTown','PalletTown_PlayersHouse_1F','PalletTown_PlayersHouse_2F','PalletTown_ProfessorOaksLab','PalletTown_Ranch','PalletTown_RivalsHouse','PalletTown_School']}
def T(m,lab):
    t=TX[m].get(lab)
    if t is None: return f'> *(texte d’origine FireRed : `{lab}`)*'
    return '\n'.join('> '+l for l in t.split('\n'))
def row(m,who,where,cond,lab):
    return f'**{who}** ({where}) — *{cond}*\n\n{T(m,lab)}\n'
P='PalletTown'
md=[]
A=md.append
A('''# Grenalux — script détaillé (parcours du joueur)
*Généré par `docs/scenario/gen_grenalux.py` à partir des textes du jeu : ce document est toujours à jour avec le code. Les textes sont des placeholders anglais ; seule la structure est figée.*

## 0. Principe : un seul raid, à l’aube
Avant que le jeu commence, TEAM ONYBRIS a frappé **trois lieux d’un coup, à l’aube** : le ranch (trackers volés, clôture coupée), l’école (le GRENAT) et le labo (fichiers sur les gemmes copiés à 4h12). Toute la ville le sait dès la première minute : il n’y a donc **pas** de « avant / après » dans les dialogues de Grenalux. Le drapeau `FLAG_GRENALUX_ONYBRIS_STRIKE` est posé au premier chargement de la ville.

| Moment | Ce qui change |
|---|---|
| Début de partie | Tout le raid est déjà fait : école et ranch en désordre, PNJ au courant. |
| Après le combat du rival au labo | Le sbire d’Onybris apparaît sur la route (22,6) : il surveille la sortie. |
| Après chaque arène | Rien ne change à Grenalux (maman soigne seulement). Chêne a un passage après l’arène 4. |
| Après la Ligue (`FLAG_SYS_GAME_CLEAR`) | Mineur et scène finale de Chêne ; la mine pourra s’ouvrir (intérieur à construire). |

Objets liés à Grenalux : **TYPE MEMO** (professeure) et **GRENAT** (ouvrier du ranch, quand `FLAG_ONYBRIS_ANIMALS_FOUND`, posé à Bourg Quartz).

## 1. Chronologie du joueur
1. **Début** : discours de Chêne d’origine (nom, genre) → le joueur se réveille dans sa chambre (2F).
2. **Chambre** : PC, console, panneau d’aide (textes d’origine). Escalier → rez-de-chaussée.
3. **Rez-de-chaussée** : maman annonce le raid de l’aube et conseille d’interroger les gens. La télé se lit de face.
4. **Dehors** : PNJ et panneaux commentent le raid ; école (vitrine vide, TYPE MEMO) ; labo ; maison du rival.
5. **Sortie nord** : le rival l’arrête → ranch (père + Chêne) → labo.
6. **Labo** : choix du partenaire, combat du rival, Chêne explique.
7. **Sortie du labo** : sbire d’Onybris (22,6) → combat → route 1.
8. **Retours** : maman soigne gratuitement (sans parler des badges).

## 2. Maison du joueur
''')
A(row('PalletTown_PlayersHouse_1F','Maman','8,4 rez-de-chaussée','premier passage, garçon','PalletTown_PlayersHouse_1F_Text_AllBoysLeaveOakLookingForYou'))
A(row('PalletTown_PlayersHouse_1F','Maman','8,4','premier passage, fille','PalletTown_PlayersHouse_1F_Text_AllGirlsLeaveOakLookingForYou'))
A('Après le combat du rival : soin gratuit, puis :\n')
A(row('PalletTown_PlayersHouse_1F','Maman','8,4','soin','PalletTown_PlayersHouse_1F_Text_YouShouldTakeQuickRest'))
A(row('PalletTown_PlayersHouse_1F','Maman','8,4','après le soin','PalletTown_PlayersHouse_1F_Text_LookingGreatTakeCare'))
A('**Panneaux** : télé (6,1), PC/console/panneau de la chambre : textes d’origine.\n')
A('\n## 3. Les rues de Grenalux (carte `PalletTown`, 46×36)\n### Panneaux\n')
for lab,where,desc in [('PalletTown_Text_PlayersHouse','10,9','maison du joueur'),('PalletTown_Text_RivalsHouse','37,9','ranch du rival'),('PalletTown_Text_TownSign','21,10','entrée de ville'),('PalletTown_Text_SchoolSign','11,21','école'),('PalletTown_Text_OakPokemonResearchLab','36,22','laboratoire'),('PalletTown_Text_SceneryMonument','22,23','monument de grenat'),('PalletTown_Text_SceneryGuardian','19,10 / 26,10','cristaux gardiens'),('PalletTown_Text_SceneryMine','39,24','mine scellée'),('PalletTown_Text_SceneryBerries','29..32 × 5 et 7','buissons de baies du ranch')]:
    A(f'**{desc}** ({where})\n\n{T(P,lab)}\n')
A('### PNJ\n')
for k,name,where in [('AmbMiner','Mineur','41,26'),('AmbOldman','Vieil homme','19,22'),('AmbGirl','Fillette','17,30 (se promène)'),('AmbBoy','Garçon','29,31 (se promène)'),('AmbScientist','Scientifique','33,23'),('AmbGardener','Jardinière','31,8'),('AmbLady','Dame','36,23'),('FatMan','Homme (PC)','19,19 (se promène)')]:
    A(f'#### {name} ({where})\n')
    A(T(P,f'PalletTown_Text_{k}')+'\n')
    d=TX[P].get(f'PalletTown_Text_{k}D')
    if d: A('**Après la Ligue :**\n\n'+T(P,f'PalletTown_Text_{k}D')+'\n')
A('#### Dame au panneau (10,16) — textes d’origine (tutoriel du menu Start), déplacée vers la sortie nord après le tutoriel\n')
A('### Scène du rival (sortie nord)\n')
A(row(P,'Rival','22/23,1','déclencheur','PalletTown_Text_RivalDontGoOut'))
A(row(P,'Rival','','dialogue','PalletTown_Text_RivalGrassUnsafeNeedMon'))
A('### Sbire d’Onybris (22,6) — après le combat du rival\n')
A(row(P,'Sbire','22,6','avant le combat','PalletTown_Text_OnybrisGruntIntro'))
A(row(P,'Sbire','','défaite','PalletTown_Text_OnybrisGruntDefeat'))
A(row(P,'Sbire','','après','PalletTown_Text_OnybrisGruntPostBattle'))
A('Effet : le sbire disparaît (il ne révèle plus le vol : il dit seulement que tout est déjà loin).\n')
A('\n## 4. Le ranch du rival (maison, `PalletTown_RivalsHouse`) — scène d’ouverture\n')
A(row('PalletTown','Père du rival','4,5','scène','PalletTown_Text_RanchDadStolenTrackers'))
A(row('PalletTown','Chêne','10,5','scène','PalletTown_Text_RanchOakGoToLab'))
A('Fondu → labo (6,12).\n')
A(row('PalletTown_RivalsHouse','Daisy','10,6','toujours (après le combat du rival)','PalletTown_RivalsHouse_Text_DaisyStrike'))
A('Autres états de Daisy (carte du monde, toilettage après la Ligue) : textes d’origine.\n')
A('\n## 5. L’école (`PalletTown_School`)\n')



A(row('PalletTown_School','Professeure','','visites suivantes','PalletTown_School_Text_TeacherCourseDone'))
A(row('PalletTown_School','Professeure','','1re visite','PalletTown_School_Text_TeacherStrike'))
A(row('PalletTown_School','Professeure','','puis : remise du mémo','PalletTown_School_Text_TeacherCourseShort'))

A(row('PalletTown_School','Élève','','toujours','PalletTown_School_Text_StudentStrike'))

A(row('PalletTown_School','Vitrine du GRENAT','8-9,2','toujours','PalletTown_School_Text_GarnetCaseStrike'))
A(row('PalletTown_School','Tableau de l’aura','4-5,1','toujours','PalletTown_School_Text_AuraCase'))
A('\n## 6. Le laboratoire (`PalletTown_ProfessorOaksLab`)\nChoix du partenaire et combat du rival : scènes d’origine (adaptées au rival de Topaze). Dès le début :\n')
A(row('PalletTown_ProfessorOaksLab','Assistant 1','3,11','toujours','PalletTown_ProfessorOaksLab_Text_AideStrike1'))
A(row('PalletTown_ProfessorOaksLab','Assistant 2','11,10','toujours','PalletTown_ProfessorOaksLab_Text_AideStrike2'))
A(row('PalletTown_ProfessorOaksLab','Ordinateur','2-3,1','toujours','PalletTown_ProfessorOaksLab_Text_ComputerStrike'))
A(row('PalletTown_ProfessorOaksLab','Chêne','6,3','après 4 badges (une fois)','PalletTown_ProfessorOaksLab_Text_OakReturn2'))
A('Chêne : retour 1 = scène du colis (Pokédex), retour final = scène du Pokédex national d’origine après la Ligue.\n')
A('\n## 7. Le ranch (`PalletTown_Ranch`, zone extérieure)\n')
for who,w,a,b in [('Ouvrier 1','9,7','Hand1','Hand1Strike'),('Ouvrier 2','14,12','Hand2','Hand2Strike')]:
    A(row('PalletTown_Ranch',who,w,'toujours',f'PalletTown_Ranch_Text_{b}'))
A(row('PalletTown_Ranch','Ouvrier 1','9,7','Doduo + 2 Nidoran retrouvés','PalletTown_Ranch_Text_Hand1Reward'))
A(row('PalletTown_Ranch','Ouvrier 1','','remise du GRENAT','PalletTown_Ranch_Text_Hand1Reward2'))
A(row('PalletTown_Ranch','Ouvrier 1','','après','PalletTown_Ranch_Text_Hand1Thanks'))
A(row('PalletTown_Ranch','Ouvrier 3','28,13 (clôture coupée)','toujours','PalletTown_Ranch_Text_Hand3'))
A('Animaux (Slowpoke, Psyduck, Meowth, Jigglypuff, Doduo, Nidoran) : cris et phrases d’ambiance ; Doduo et les deux Nidoran ont été volés à l’aube (absents).\n')
A('''
## 8. Reste à faire sur Grenalux
- Poser `FLAG_ONYBRIS_ANIMALS_FOUND` au QG d’Onybris de Bourg Quartz (étape 6 du parcours) : la quête du ranch est alors terminable.
- Faire réapparaître Doduo et les deux Nidoran dans les enclos quand la quête est rendue.
- Mine : seule la grille scellée existe (panneau 39,24). L’ouverture après la Ligue demande un intérieur (à décider).
- Lore à trancher : le GRENAT de l’école est-il la vraie gemme ou un leurre ? (Le plan actuel : l’école a l’exemplaire de vitrine ; le « vrai » GRENAT est offert par l’ouvrier du ranch.)
''')
open(os.path.join(os.path.dirname(__file__),'GRENALUX.md'),'w').write('\n'.join(md))
