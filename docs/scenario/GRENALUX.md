# Grenalux — script détaillé (parcours du joueur)
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

**Maman** (8,4 rez-de-chaussée) — *premier passage, garçon*

> MOM: …Right.
> All boys leave home someday.
> It said so on TV.
> — — —
> But don't go out in your slippers!
> Put on your sports shoes first.
> — — —
> Oh, and the whole town is talking
> about a raid at dawn. The RANCH, the
> SCHOOL, even the LAB. People in black.
> — — —
> Ask around before you go anywhere,
> dear.

**Maman** (8,4) — *premier passage, fille*

> MOM: …Right.
> All girls dream of traveling.
> It said so on TV.
> — — —
> But don't go out in your slippers!
> Put on your sports shoes first.
> — — —
> Oh, and the whole town is talking
> about a raid at dawn. The RANCH, the
> SCHOOL, even the LAB. People in black.
> — — —
> Ask around before you go anywhere,
> dear.

Après le combat du rival : soin gratuit, puis :

**Maman** (8,4) — *soin*

> MOM: {PLAYER}!
> You should take a quick rest.

**Maman** (8,4) — *après le soin*

> MOM: Oh, good! You and your
> POKéMON are looking great.
> Take care now!

**Panneaux** : télé (6,1), PC/console/panneau de la chambre : textes d’origine.


## 3. Les rues de Grenalux (carte `PalletTown`, 46×36)
### Panneaux

**maison du joueur** (10,9)

> {PLAYER}'s house

**ranch du rival** (37,9)

> {RIVAL}'s family RANCH

**entrée de ville** (21,10)

> GRENALUX
> Where every journey begins!

**école** (11,21)

> GRENALUX SCHOOL
> Where every trainer begins.

**laboratoire** (36,22)

> OAK POKéMON RESEARCH LAB

**monument de grenat** (22,23)

> A giant garnet crystal.
> It hums softly, as if alive.

**cristaux gardiens** (19,10 / 26,10)

> A garnet crystal, tall as a house.
> It watches over the road north.

**mine scellée** (39,24)

> The old mine, sealed for safety.
> Something glints deep inside...

**buissons de baies du ranch** (29..32 × 5 et 7)

> Berry bushes for the ranch animals.
> They are not for picking!

### PNJ

#### Mineur (41,26)

> They took the GRENAT from the school.
> The mine is sealed, but I can feel
> the vein humming under my boots.
> — — —
> Only the LEAGUE can open that gate.
> Beat it, and maybe it lets go.

**Après la Ligue :**

> The LEAGUE sent word, CHAMPION.
> The mine gate may open again.
> — — —
> The vein hums for you now. Mind the
> dark down there.

#### Vieil homme (19,22)

> Every town keeps a stone of its own,
> they say. Garnet is ours.
> — — —
> Take the stones, and a town forgets
> its own name.

#### Fillette (17,30 (se promène))

> The school's GRENAT is gone!
> The pond looks sad today.
> — — —
> Don't let them take the monument!

#### Garçon (29,31 (se promène))

> No school today, because of the
> robbery. But teacher still gives the
> TYPE MEMO to trainers who ask.

#### Scientifique (33,23)

> The robbers copied our gem files!
> Now they know where every gem sleeps.
> — — —
> Someone must warn the other towns,
> {PLAYER}!

#### Jardinière (31,8)

> The ranch lost its tracker POKéMON.
> The berries just sit there now.
> — — —
> Whoever took them will have to feed
> them. I hope they know how.

#### Dame (36,23)

> Red roofs, red trees, red stone...
> And now an empty case at school.
> — — —
> Tired, {PLAYER}? Go home and let
> MOM tend to your POKéMON.

#### Homme (PC) (19,19 (se promène))

> Did you hear? Robbers hit the school
> and the LAB! They even copied files
> from the PC network.
> — — —
> Don't leave anything precious in the
> PC today.

#### Dame au panneau (10,16) — textes d’origine (tutoriel du menu Start), déplacée vers la sortie nord après le tutoriel

### Scène du rival (sortie nord)

**Rival** (22/23,1) — *déclencheur*

> {RIVAL}: Hey, {PLAYER}! Wait!
> Don't go out there!

**Rival** () — *dialogue*

> {RIVAL}: The tall grass is full of
> wild POKéMON, and you've got
> nothing to fight with!
> — — —
> {PLAYER}: But I've waited all my life
> to start my journey!
> — — —
> {RIVAL}: Then come to our RANCH.
> My dad and PROF. OAK are there.
> — — —
> They'll know what to do.
> Follow me!

### Sbire d’Onybris (22,6) — après le combat du rival

**Sbire** (22,6) — *avant le combat*

> Hold it, kid!
> TEAM ONYBRIS has business here.
> — — —
> POKé BALLS are chains.
> We set POKéMON free, as equals!
> — — —
> That starter of yours is a prisoner
> who doesn't know it yet.
> — — —
> Let's see how it feels about that!

**Sbire** () — *défaite*

> Tch... it fights for you by
> choice? That's... not what the
> boss told us.

**Sbire** () — *après*

> Forget it. You're too late anyway.
> — — —
> The GRENAT and the LAB's gem files
> left GRENALUX before sunrise.
> — — —
> We only stayed to watch the road.
> GRENALUX will see us again...

Effet : le sbire disparaît (il ne révèle plus le vol : il dit seulement que tout est déjà loin).


## 4. Le ranch du rival (maison, `PalletTown_RivalsHouse`) — scène d’ouverture

**Père du rival** (4,5) — *scène*

> {RIVAL}'s DAD: So you're {PLAYER}.
> {RIVAL} never stops talking about you.
> — — —
> Bad timing, I'm afraid. At dawn,
> people in black took our tracker
> POKéMON right out of the pens.
> — — —
> They called themselves TEAM ONYBRIS.

**Chêne** (10,5) — *scène*

> OAK: Trackers were the best at
> sensing the AURA. Someone is
> searching for something.
> — — —
> Ten years ago the AURA changed every
> POKéMON. I never thought the trouble
> would reach our doorstep.
> — — —
> {PLAYER}, {RIVAL}, come to my LAB.
> You're each getting a partner.

Fondu → labo (6,12).

**Daisy** (10,6) — *toujours (après le combat du rival)*

> DAISY: Dad is mending the fence,
> and Grandpa is not himself.
> — — —
> Please be careful out there,
> {PLAYER}. And take care of {RIVAL}.

Autres états de Daisy (carte du monde, toilettage après la Ligue) : textes d’origine.


## 5. L’école (`PalletTown_School`)

**Professeure** () — *visites suivantes*

> Remember: check a POKéMON's type in
> the SUMMARY. The old ones lie.

**Professeure** () — *1re visite*

> They came at dawn, all in black.
> They took the GRENAT before I could
> even reach the alarm.
> — — —
> They said it was for the POKéMON,
> for their freedom... What does a
> gem have to do with freedom?
> — — —
> There is no class today.

**Professeure** () — *puis : remise du mémo*

> Still, a teacher teaches. Types changed
> ten years ago, and FAIRY now beats
> DRAGON, FIGHTING and DARK.
> — — —
> I wrote it down for you.

**Élève** () — *toujours*

> Grandpa says thieves used to hide
> their faces. These ones were proud
> of it.
> — — —
> We got the day off, but nobody feels
> like playing.

**Vitrine du GRENAT** (8-9,2) — *toujours*

> The glass case is empty. A note is
> left behind: POKéMON were never
> meant to be owned. - TEAM ONYBRIS

**Tableau de l’aura** (4-5,1) — *toujours*

> The AURA of ten years ago.
> Records show every POKéMON's type
> changed in a single night.


## 6. Le laboratoire (`PalletTown_ProfessorOaksLab`)
Choix du partenaire et combat du rival : scènes d’origine (adaptées au rival de Topaze). Dès le début :

**Assistant 1** (3,11) — *toujours*

> Someone got into the archive room
> last night and copied every file
> on gemstones.
> — — —
> Nothing else was touched. That's
> what scares me.

**Assistant 2** (11,10) — *toujours*

> The PROF. says the GRENAT in the
> museum and the files here are two
> halves of the same puzzle.
> — — —
> Whoever hit both knows exactly what
> they're after.

**Ordinateur** (2-3,1) — *toujours*

> ACCESS LOG: archive opened at 4:12.
> Files copied: GEMSTONES, AURA
> RECORDS, JIRACHI.

**Chêne** (6,3) — *après 4 badges (une fois)*

> OAK: Four BADGES! I hear that each
> town you visit keeps a gem, and that
> someone is collecting them.
> — — —
> TEAM ONYBRIS believes they can tear
> POKéMON away from people for good.
> — — —
> Their leader fights the AURA with
> every step. Be careful, {PLAYER}.

Chêne : retour 1 = scène du colis (Pokédex), retour final = scène du Pokédex national d’origine après la Ligue.


## 7. Le ranch (`PalletTown_Ranch`, zone extérieure)

**Ouvrier 1** (9,7) — *toujours*

> The east fence was cut last night.
> On a ranch this big, no one saw.

**Ouvrier 2** (14,12) — *toujours*

> They took the tracker POKéMON from
> the pens. The fence was cut open.

**Ouvrier 1** (9,7) — *Doduo + 2 Nidoran retrouvés*

> You found DODUO and both NIDORAN?
> They are back in the pens, safe!
> — — —
> The boss kept this in the barn for
> years. Please, take it.

**Ouvrier 1** () — *remise du GRENAT*

> It was found in the old mine. It
> hums when you hold it. I don't know
> why, but it likes you.

**Ouvrier 1** () — *après*

> The animals are calm again.
> Thank you for everything.

**Ouvrier 3** (28,13 (clôture coupée)) — *toujours*

> The pens were shut tight last night.
> Now look at this fence...

Animaux (Slowpoke, Psyduck, Meowth, Jigglypuff, Doduo, Nidoran) : cris et phrases d’ambiance ; Doduo et les deux Nidoran ont été volés à l’aube (absents).


## 8. Reste à faire sur Grenalux
- Poser `FLAG_ONYBRIS_ANIMALS_FOUND` au QG d’Onybris de Bourg Quartz (étape 6 du parcours) : la quête du ranch est alors terminable.
- Faire réapparaître Doduo et les deux Nidoran dans les enclos quand la quête est rendue.
- Mine : seule la grille scellée existe (panneau 39,24). L’ouverture après la Ligue demande un intérieur (à décider).
- Lore à trancher : le GRENAT de l’école est-il la vraie gemme ou un leurre ? (Le plan actuel : l’école a l’exemplaire de vitrine ; le « vrai » GRENAT est offert par l’ouvrier du ranch.)
