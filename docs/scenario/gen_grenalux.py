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

## 0. Principe : l’attaque se vit en direct
Rien n’est volé avant le début du jeu. Grenalux est d’abord **paisible** (état A) ; l’attaque d’Onybris se déroule sous les yeux du joueur, au ranch du rival, puis le village bascule dans l’état « après » (B) : clôture du ranch coupée, animaux disparus, vitrine de l’école vide, labo fouillé. Le drapeau `FLAG_GRENALUX_ONYBRIS_STRIKE` est posé à la fin de la scène du ranch ; tous les PNJ de la ville ont un texte A et un texte B.

`VAR_GRENALUX_OPENING` pilote la séquence : 0 = début ; 1 = scène du ranch en cours ; 2 = école à faire ; 3 = labo à faire ; 4 = séquence terminée (la ville est libre, la sortie nord n’est plus bloquée).

## 1. Chronologie du joueur
1. **Début** : discours de Chêne d’origine → chambre (2F) → rez-de-chaussée. Maman : « Chêne est au ranch d’à côté avec le père du rival, il te cherchait. » Ville **paisible** : les PNJ parlent de la vie du village.
2. **Sortie nord** : le rival arrête le joueur et l’emmène au ranch (maison du rival).
3. **Ranch (scène)** : le père et Chêne accueillent le joueur → les trackers hurlent → un sbire d’Onybris entre : « Nous libérons les POKéMON du ranch ; mes amis sont à l’école et au labo ». Le père court aux enclos. Chêne panique et tend trois POKé BALLS : **le joueur choisit son partenaire en urgence** (menu BULBASAUR / SQUIRTLE / CHARMANDER, confirmation, surnom). Le rival prend celui qui bat le sien. **Combat contre le sbire** (didacticiel de combat de Chêne ; si le joueur perd, la scène continue). Le sbire fuit, Chêne part vérifier son labo. **Maman arrive** en courant, inquiète, puis attendrie par le POKéMON, et lui remet un **PENDENTIF** (sans dire ce que c’est), en lui conseillant d’aller à l’école.
4. **Ville (état B)** : la sortie nord est bloquée (« d’abord l’école, Chêne attend au labo »).
5. **École (scène)** : vitrine vide, la professeure donne le cours sur les types et le **TYPE MEMO**, regarde le pendentif sans rien dire ; le rival surgit et **défie le joueur avec le partenaire opposé** (combat, pas de whiteout).
6. **Labo (scène)** : Chêne annonce que ses fichiers ont été copiés, remet le **POKÉDEX** et 5 POKé BALLS ; le rival part. La ville est libre.
7. **Plus tard** : le colis d’Opanihrum est livré à Chêne (plus de Pokédex à ce moment-là, uniquement la livraison). Maman soigne gratuitement quand on rentre.

## 2. Maison du joueur
''')
A(row('PalletTown_PlayersHouse_1F','Maman','8,4 rez-de-chaussée','avant la scène du ranch, garçon','PalletTown_PlayersHouse_1F_Text_AllBoysLeaveOakLookingForYou'))
A(row('PalletTown_PlayersHouse_1F','Maman','8,4','avant la scène du ranch, fille','PalletTown_PlayersHouse_1F_Text_AllGirlsLeaveOakLookingForYou'))
A('Après la scène du ranch : soin gratuit, puis :\n')
A(row('PalletTown_PlayersHouse_1F','Maman','8,4','soin','PalletTown_PlayersHouse_1F_Text_YouShouldTakeQuickRest'))
A(row('PalletTown_PlayersHouse_1F','Maman','8,4','après le soin','PalletTown_PlayersHouse_1F_Text_LookingGreatTakeCare'))
A('**Panneaux** : télé (6,1), PC/console/panneau de la chambre : textes d’origine.\n')
A('\n## 3. Les rues de Grenalux (carte `PalletTown`, 46×36)\n### Panneaux\n')
for lab,where,desc in [('PalletTown_Text_PlayersHouse','10,9','maison du joueur'),('PalletTown_Text_RivalsHouse','37,9','ranch du rival'),('PalletTown_Text_TownSign','21,10','entrée de ville'),('PalletTown_Text_SchoolSign','11,21','école'),('PalletTown_Text_OakPokemonResearchLab','36,22','laboratoire'),('PalletTown_Text_SceneryMonument','22,23','monument de grenat'),('PalletTown_Text_SceneryGuardian','19,10 / 26,10','cristaux gardiens'),('PalletTown_Text_SceneryMine','39,24','mine scellée'),('PalletTown_Text_SceneryBerries','29..32 × 5 et 7','buissons de baies du ranch')]:
    A(f'**{desc}** ({where})\n\n{T(P,lab)}\n')
A('### PNJ\n')
for k,name,where in [('AmbMiner','Mineur','41,26'),('AmbOldman','Vieil homme','19,22'),('AmbGirl','Fillette','17,30 (se promène)'),('AmbBoy','Garçon','29,31 (se promène)'),('AmbScientist','Scientifique','33,23'),('AmbGardener','Jardinière','31,8'),('AmbLady','Dame','36,23'),('FatMan','Homme (PC)','19,19 (se promène)')]:
    A(f'#### {name} ({where})\n')
    A('**État A — paisible :**\n\n'+T(P,f'PalletTown_Text_{k}A')+'\n')
    A('**État B — après l’attaque :**\n\n'+T(P,f'PalletTown_Text_{k}B')+'\n')
    d=TX[P].get(f'PalletTown_Text_{k}D')
    if d: A('**Après la Ligue :**\n\n'+T(P,f'PalletTown_Text_{k}D')+'\n')
A('#### Dame au panneau (10,16) — textes d’origine (tutoriel du menu Start), déplacée vers la sortie nord après le tutoriel\n')
A('### Scène du rival (sortie nord)\n')
A(row(P,'Rival','22/23,1','déclencheur','PalletTown_Text_RivalDontGoOut'))
A(row(P,'Rival','','dialogue','PalletTown_Text_RivalGrassUnsafeNeedMon'))
A('### Blocage de la sortie nord (après le ranch, avant la fin du labo)\n')
A(T(P,'PalletTown_Text_ExitGate')+'\n')
A('\n## 4. La scène du ranch (`PalletTown_RivalsHouse`) — l’attaque\n')
for lab,who in [('RanchDadHello','Père du rival'),('RanchOakIntro','Chêne'),('RanchTrackersHowl','Chêne'),('RanchGruntEnter','Sbire d’Onybris (entre par la porte)'),('RanchDadFlees','Père du rival (sort en courant)'),('RanchOakPanic','Chêne (panique, tend les POKé BALLS)'),('RanchOakChoose','Chêne (menu du choix du partenaire)'),('RanchRivalTakes','Rival (prend le partenaire opposé)'),('RanchGruntChallenge','Sbire (avant le combat)'),('OnybrisGruntDefeat','Sbire (battu)'),('OnybrisGruntVictory','Sbire (si le joueur perd)'),('RanchGruntRetreat','Sbire (fuit)'),('RanchOakAfter','Chêne (part au labo)'),('RanchMom1','Maman (arrive, donne le pendentif)'),('ReceivedPendant','Objet reçu'),('RanchMom2','Maman (au revoir)')]:
    A(f'**{who}**\n\n'+T(P,f'PalletTown_Text_{lab}')+'\n')
A(row('PalletTown_RivalsHouse','Daisy','10,6','après l’attaque','PalletTown_RivalsHouse_Text_DaisyStrike'))
A('Autres états de Daisy (carte du monde, toilettage après la Ligue) : textes d’origine.\n')
A('\n## 5. L’école (`PalletTown_School`)\n### Avant l’attaque\n')
A(row('PalletTown_School','Professeure','6,2','état A','PalletTown_School_Text_Teacher'))
A(row('PalletTown_School','Élève','4,5','état A','PalletTown_School_Text_Student'))
A(row('PalletTown_School','Vitrine du GRENAT','8-9,2','état A','PalletTown_School_Text_GarnetCase'))
A('### Scène d’arrivée (après la scène du ranch)\n')
A(row('PalletTown_School','Professeure','','scène','PalletTown_School_Text_SceneTeacher1'))
A(row('PalletTown_School','Professeure','','cours','PalletTown_School_Text_TeacherCourse'))
A(row('PalletTown_School','Objet reçu','','','PalletTown_School_Text_ReceivedTypeMemo'))
A(row('PalletTown_School','Professeure','','le pendentif','PalletTown_School_Text_SceneTeacherPendant'))
A(row('PalletTown_School','Rival','entre à 3,7','défi (combat avec le partenaire opposé)','PalletTown_School_Text_SceneRivalChallenge'))
A(row('PalletTown_School','Rival','','après le combat','PalletTown_School_Text_SceneRivalAfter'))
A('### Après\n')
A(row('PalletTown_School','Professeure','6,2','état B','PalletTown_School_Text_TeacherStrike'))
A(row('PalletTown_School','Élève','4,5','état B','PalletTown_School_Text_StudentStrike'))
A(row('PalletTown_School','Vitrine','8-9,2','état B','PalletTown_School_Text_GarnetCaseStrike'))
A(row('PalletTown_School','Tableau de l’aura','4-5,1','toujours','PalletTown_School_Text_AuraCase'))
A('\n## 6. Le laboratoire (`PalletTown_ProfessorOaksLab`)\nLe choix du partenaire n’a plus lieu ici (il se fait au ranch). Scène d’arrivée après l’école :\n')
A(row('PalletTown_ProfessorOaksLab','Chêne','6,3','scène du POKÉDEX','PalletTown_ProfessorOaksLab_Text_OakAfterRaid'))
A('Puis, d’origine : demande, POKÉDEX, 5 POKé BALLS, explications, rêve de Chêne, le rival part. Aides et ordinateur (état B) :\n')
A(row('PalletTown_ProfessorOaksLab','Assistant 1','3,11','état B','PalletTown_ProfessorOaksLab_Text_AideStrike1'))
A(row('PalletTown_ProfessorOaksLab','Assistant 2','11,10','état B','PalletTown_ProfessorOaksLab_Text_AideStrike2'))
A(row('PalletTown_ProfessorOaksLab','Ordinateur','2-3,1','état B','PalletTown_ProfessorOaksLab_Text_ComputerStrike'))
A(row('PalletTown_ProfessorOaksLab','Chêne','6,3','après 4 badges (une fois)','PalletTown_ProfessorOaksLab_Text_OakReturn2'))
A('Chêne : retour 1 = livraison du colis d’Opanihrum (le Pokédex est déjà donné), retour final = scène du Pokédex national d’origine après la Ligue.\n')
A('\n## 7. Le ranch (`PalletTown_Ranch`, zone extérieure)\n')
for who,w,a,b in [('Ouvrier 1','9,7','Hand1','Hand1Strike'),('Ouvrier 2','14,12','Hand2','Hand2Strike')]:
    A(row('PalletTown_Ranch',who,w,'état A',f'PalletTown_Ranch_Text_{a}'))
    A(row('PalletTown_Ranch',who,w,'état B',f'PalletTown_Ranch_Text_{b}'))
A(row('PalletTown_Ranch','Ouvrier 1','9,7','Doduo + 2 Nidoran retrouvés','PalletTown_Ranch_Text_Hand1Reward'))
A(row('PalletTown_Ranch','Ouvrier 1','','récompense : 1 POTION + 5 POKé BALLS','PalletTown_Ranch_Text_Hand1Reward2'))
A(row('PalletTown_Ranch','Ouvrier 1','','après','PalletTown_Ranch_Text_Hand1Thanks'))
A(row('PalletTown_Ranch','Ouvrier 3','28,13 (clôture coupée)','état B','PalletTown_Ranch_Text_Hand3'))
A('Animaux (Slowpoke, Psyduck, Meowth, Jigglypuff, Doduo, Nidoran) : cris et phrases d’ambiance ; Doduo et les deux Nidoran disparaissent à l’état B (volés pendant l’attaque).\n')
A('''
## 8. Reste à faire sur Grenalux
- Quête du ranch **terminée sur la Route 1** : après l’attaque, DODUO + 2 NIDORAN errent sur la route (x11–17, y25–27) ; leur parler (n’importe lequel) les renvoie au ranch (`FLAG_ONYBRIS_ANIMALS_FOUND`), ils réapparaissent dans les enclos, l’ouvrier près de la clôture donne 1 POTION + 5 POKé BALLS (`FLAG_GRENALUX_GEM_REWARD`).
- Route 1 : aucun dresseur ; PNJ = vendeur (Potion), garçon (herbe qui change de couleur), panneau ; herbe : Pidgey / Rattata niv. 3–7, Spearow rare niv. 6–7.
- Faire réapparaître Doduo et les deux Nidoran dans les enclos quand la quête est rendue.
- Mine : seule la grille scellée existe ; son ouverture après la Ligue demande un intérieur (à décider).
- Le PENDENTIF (ancien `ITEM_RUBY`) est le « vrai » GRENAT, mais son importance n’est révélée que plus tard : à décider avec la quête des gemmes.
''')
open(os.path.join(os.path.dirname(__file__),'GRENALUX.md'),'w').write('\n'.join(md))
