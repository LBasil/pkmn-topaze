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

## 0. États du monde (ce qui change les dialogues)
| État | Déclencheur | Ce qui change |
|---|---|---|
| **A — Avant** | nouvelle partie | Le ranch a été visité à l’aube : les trackers sont volés. Le GRENAT de l’école est encore là. |
| **B — Ouverture** | le joueur sort au nord (cases 22/23,1) | Le rival l’arrête, le conduit au ranch (père + Chêne), puis tous vont au labo. |
| **C — Labo** | `VAR_GRENALUX_OPENING`=2 | Choix du partenaire, combat du rival, Chêne explique. |
| **D — Le coup** | combat contre le sbire d’Onybris (22,6) gagné → `FLAG_GRENALUX_ONYBRIS_STRIKE` | Le GRENAT de l’école et les fichiers du labo ont été volés pendant que tout le monde était au ranch. Tous les PNJ passent en texte « après ». La clôture du ranch est coupée, Doduo et les deux Nidoran ont disparu. |
| **E — Arènes** | `FLAG_BADGE01..08_GET` | Maman rappelle l’objectif à chaque badge ; Chêne parle après l’arène 4. |
| **F — Après la Ligue** | `FLAG_SYS_GAME_CLEAR` | La mine peut s’ouvrir (porte non construite : voir « Reste à faire »). |

Objets clés liés à Grenalux : **TYPE MEMO** (école, état C/D), **GRENAT** (ranch, quand `FLAG_ONYBRIS_ANIMALS_FOUND`, posé à Bourg Quartz).

## 1. Chronologie du joueur
1. **Début** : discours de Chêne d’origine (nom, genre) → le joueur se réveille dans sa chambre (2F de la maison, `PalletTown_PlayersHouse_2F`).
2. **Chambre** : PC, console, panneau d’aide (textes d’origine). Escalier (10,2) → rez-de-chaussée.
3. **Rez-de-chaussée** : Maman (8,4) parle la première fois (texte « premier passage » ci-dessous), la télé (6,1) se lit seulement de face.
4. **Dehors** : 8 PNJ d’ambiance + panneaux de lieux + école + labo + maison du rival.
5. **Sortie nord** : le rival (cases 22,1 / 23,1) → ranch → scène du père et de Chêne → labo.
6. **Labo** : choix du partenaire, combat du rival.
7. **Sortie du labo** : sbire d’Onybris sur la route (22,6) → combat → état D.
8. **Route 1** : le joueur peut partir. Maman soigne et rappelle l’objectif à chaque retour.

## 2. Maison du joueur
''')
A(row('PalletTown_PlayersHouse_1F','Maman','8,4 rez-de-chaussée','premier passage (avant le combat du rival), garçon','PalletTown_PlayersHouse_1F_Text_AllBoysLeaveOakLookingForYou'))
A(row('PalletTown_PlayersHouse_1F','Maman','8,4','premier passage, fille','PalletTown_PlayersHouse_1F_Text_AllGirlsLeaveOakLookingForYou'))
A('Après le combat du rival : soin gratuit (`EventScript_OutOfCenterPartyHeal`), puis :\n')
A(row('PalletTown_PlayersHouse_1F','Maman','8,4','soin','PalletTown_PlayersHouse_1F_Text_YouShouldTakeQuickRest'))
for i in range(9):
    A(row('PalletTown_PlayersHouse_1F','Maman — rappel','8,4',f'{i} badge(s)',f'PalletTown_PlayersHouse_1F_Text_MomB{i}'))
A('**Panneaux** : télé (6,1), PC/console/panneau de la chambre : textes d’origine.\n')
A('\n## 3. Les rues de Grenalux (carte `PalletTown`, 46×36)\n### Panneaux\n')
for lab,where,desc in [('PalletTown_Text_PlayersHouse','10,9','maison du joueur'),('PalletTown_Text_RivalsHouse','37,9','ranch du rival'),('PalletTown_Text_TownSign','21,10','entrée de ville'),('PalletTown_Text_SchoolSign','11,21','école'),('PalletTown_Text_OakPokemonResearchLab','36,22','laboratoire'),('PalletTown_Text_SceneryMonument','22,23','monument de grenat'),('PalletTown_Text_SceneryGuardian','19,10 / 26,10','cristaux gardiens'),('PalletTown_Text_SceneryMine','39,24','mine scellée'),('PalletTown_Text_SceneryBerries','29..32 × 5 et 7','buissons de baies du ranch')]:
    A(f'**{desc}** ({where})\n\n{T(P,lab)}\n')
A('### PNJ — avant / après le coup d’Onybris / après la Ligue\n')
for k,name,where in [('AmbMiner','Mineur','41,26'),('AmbOldman','Vieil homme','19,22'),('AmbGirl','Fillette','17,30 (se promène)'),('AmbBoy','Garçon','29,31 (se promène)'),('AmbScientist','Scientifique','33,23'),('AmbGardener','Jardinière','31,8'),('AmbLady','Dame','36,23'),('FatMan','Homme (PC)','19,19 (se promène)')]:
    A(f'#### {name} ({where})\n')
    A(row(P,'État A — avant','',' ',f'PalletTown_Text_{k}A').replace('**État A — avant** () — * *\n\n',''))
    A(row(P,'État D — après le coup','',' ',f'PalletTown_Text_{k}B').replace('**État D — après le coup** () — * *\n\n','**Après le coup :**\n\n'))
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
A('Effets : le sbire disparaît, `FLAG_GRENALUX_ONYBRIS_STRIKE` est posé (état D).\n')
A('\n## 4. Le ranch du rival (maison, `PalletTown_RivalsHouse`) — scène d’ouverture\n')
A(row('PalletTown','Père du rival','4,5','scène','PalletTown_Text_RanchDadStolenTrackers'))
A(row('PalletTown','Chêne','10,5','scène','PalletTown_Text_RanchOakGoToLab'))
A('Fondu → labo (6,12).\n')
A(row('PalletTown_RivalsHouse','Daisy','10,6','après le coup (après le combat du rival)','PalletTown_RivalsHouse_Text_DaisyStrike'))
A('Autres états de Daisy (carte du monde, toilettage après la Ligue) : textes d’origine.\n')
A('\n## 5. L’école (`PalletTown_School`)\n')
A(row('PalletTown_School','Professeure','6,2','avant le coup, 1re visite','PalletTown_School_Text_Teacher'))
A(row('PalletTown_School','Professeure','','suite : cours','PalletTown_School_Text_TeacherCourse'))
A(row('PalletTown_School','Professeure','','fin du cours','PalletTown_School_Text_TeacherCourseEnd'))
A(row('PalletTown_School','Professeure','','visites suivantes','PalletTown_School_Text_TeacherCourseDone'))
A(row('PalletTown_School','Professeure','','après le coup','PalletTown_School_Text_TeacherStrike'))
A(row('PalletTown_School','Professeure','','après le coup, si pas de mémo','PalletTown_School_Text_TeacherCourseShort'))
A(row('PalletTown_School','Élève','4,5','avant','PalletTown_School_Text_Student'))
A(row('PalletTown_School','Élève','','après','PalletTown_School_Text_StudentStrike'))
A(row('PalletTown_School','Vitrine du GRENAT','8-9,2','avant','PalletTown_School_Text_GarnetCase'))
A(row('PalletTown_School','Vitrine','','après','PalletTown_School_Text_GarnetCaseStrike'))
A(row('PalletTown_School','Tableau de l’aura','4-5,1','toujours','PalletTown_School_Text_AuraCase'))
A('\n## 6. Le laboratoire (`PalletTown_ProfessorOaksLab`)\nChoix du partenaire et combat du rival : scènes d’origine (adaptées au rival de Topaze). Après le coup :\n')
A(row('PalletTown_ProfessorOaksLab','Assistant 1','3,11','après le coup','PalletTown_ProfessorOaksLab_Text_AideStrike1'))
A(row('PalletTown_ProfessorOaksLab','Assistant 2','11,10','après le coup','PalletTown_ProfessorOaksLab_Text_AideStrike2'))
A(row('PalletTown_ProfessorOaksLab','Ordinateur','2-3,1','après le coup','PalletTown_ProfessorOaksLab_Text_ComputerStrike'))
A(row('PalletTown_ProfessorOaksLab','Chêne','6,3','après 4 badges (une fois)','PalletTown_ProfessorOaksLab_Text_OakReturn2'))
A('Chêne : retour 1 = scène du colis (Pokédex), retour final = scène du Pokédex national d’origine après la Ligue.\n')
A('\n## 7. Le ranch (`PalletTown_Ranch`, zone extérieure)\n')
for who,w,a,b in [('Ouvrier 1','9,7','Hand1','Hand1Strike'),('Ouvrier 2','14,12','Hand2','Hand2Strike')]:
    A(row('PalletTown_Ranch',who,w,'avant',f'PalletTown_Ranch_Text_{a}'))
    A(row('PalletTown_Ranch',who,w,'après le coup',f'PalletTown_Ranch_Text_{b}'))
A(row('PalletTown_Ranch','Ouvrier 1','9,7','Doduo + 2 Nidoran retrouvés','PalletTown_Ranch_Text_Hand1Reward'))
A(row('PalletTown_Ranch','Ouvrier 1','','remise du GRENAT','PalletTown_Ranch_Text_Hand1Reward2'))
A(row('PalletTown_Ranch','Ouvrier 1','','après','PalletTown_Ranch_Text_Hand1Thanks'))
A(row('PalletTown_Ranch','Ouvrier 3','28,13 (apparaît après le coup, clôture coupée)','après le coup','PalletTown_Ranch_Text_Hand3'))
A('Animaux (Slowpoke, Psyduck, Meowth, Jigglypuff, Doduo, Nidoran) : cris et phrases d’ambiance ; Doduo et les deux Nidoran disparaissent après le coup.\n')
A('''
## 8. Reste à faire sur Grenalux
- Poser `FLAG_ONYBRIS_ANIMALS_FOUND` au QG d’Onybris de Bourg Quartz (étape 6 du parcours) : la quête du ranch est alors terminable.
- Faire réapparaître Doduo et les deux Nidoran dans les enclos quand la quête est rendue.
- Mine : seule la grille scellée existe (panneau 39,24). L’ouverture après la Ligue demande un intérieur (à décider).
- Lore à trancher : le GRENAT de l’école est-il la vraie gemme ou un leurre ? (Le plan actuel : l’école a l’exemplaire de vitrine ; le « vrai » GRENAT est offert par l’ouvrier du ranch.)
''')
open(os.path.join(os.path.dirname(__file__),'GRENALUX.md'),'w').write('\n'.join(md))
