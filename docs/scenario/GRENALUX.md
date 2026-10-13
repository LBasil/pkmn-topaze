# Grenalux — script détaillé (parcours du joueur)
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

**Maman** (8,4 rez-de-chaussée) — *premier passage (avant le combat du rival), garçon*

> MOM: …Right.
> All boys leave home someday.
> It said so on TV.
> — — —
> But don't go out in your slippers!
> Put on your sports shoes first.
> — — —
> Oh, and something happened at the
> RANCH this morning. People in black.
> — — —
> Ask around town before you go
> anywhere, dear.

**Maman** (8,4) — *premier passage, fille*

> MOM: …Right.
> All girls dream of traveling.
> It said so on TV.
> — — —
> But don't go out in your slippers!
> Put on your sports shoes first.
> — — —
> Oh, and something happened at the
> RANCH this morning. People in black.
> — — —
> Ask around town before you go
> anywhere, dear.

Après le combat du rival : soin gratuit (`EventScript_OutOfCenterPartyHeal`), puis :

**Maman** (8,4) — *soin*

> MOM: {PLAYER}!
> You should take a quick rest.

**Maman — rappel** (8,4) — *0 badge(s)*

> MOM: Those people in black stole our
> ranch's trackers. Ask around the next
> towns; someone must have seen them.

**Maman — rappel** (8,4) — *1 badge(s)*

> MOM: One BADGE already! The people in
> black were seen heading east. Keep
> your POKéMON close.

**Maman — rappel** (8,4) — *2 badge(s)*

> MOM: Two BADGES. Every town keeps a gem,
> {PLAYER}. Make sure TEAM ONYBRIS
> doesn't take them all.

**Maman — rappel** (8,4) — *3 badge(s)*

> MOM: Three BADGES! I saw TEAM ONYBRIS on
> the news. They talk about freedom,
> but they only take.

**Maman — rappel** (8,4) — *4 badge(s)*

> MOM: Four BADGES. PROF. OAK wants to see
> you. He sounded worried on the phone.

**Maman — rappel** (8,4) — *5 badge(s)*

> MOM: Five BADGES. You look taller every
> time you come home. Eat something!

**Maman — rappel** (8,4) — *6 badge(s)*

> MOM: Six BADGES. Whatever they are after,
> you're closer to it than they are.

**Maman — rappel** (8,4) — *7 badge(s)*

> MOM: Seven BADGES... One more, and then
> the LEAGUE. I'll keep your room warm.

**Maman — rappel** (8,4) — *8 badge(s)*

> MOM: All eight BADGES! Go to the LEAGUE.
> I'll be watching it on TV.

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

### PNJ — avant / après le coup d’Onybris / après la Ligue

#### Mineur (41,26)

> The ranch alarm woke the whole hill
> at dawn. Folks in black, they say.
> — — —
> The mine is sealed, so it wasn't
> for ore they came.

**Après le coup :**

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

> My grandfather carried the first
> crystal up from the mine. They say
> the monument hums at night.
> — — —
> Lately, it hums louder.

**Après le coup :**

> Every town keeps a stone of its own,
> they say. Garnet is ours.
> — — —
> Take the stones, and a town forgets
> its own name.

#### Fillette (17,30 (se promène))

> The pond turns purple at dusk!
> My teacher says it is the garnet.
> — — —
> She has a real GRENAT at school!

**Après le coup :**

> The school's GRENAT is gone!
> The pond looks sad today.
> — — —
> Don't let them take the monument!

#### Garçon (29,31 (se promène))

> Some POKéMON got new types when the
> AURA changed. Even FAIRY is new!
> — — —
> Teacher gives a TYPE MEMO to every
> new trainer. Go and ask her!

**Après le coup :**

> No school today, because of the
> robbery. But teacher still gives the
> TYPE MEMO to trainers who ask.

#### Scientifique (33,23)

> The lab measures the aura of every
> crystal in town. The readings jumped
> this morning.
> — — —
> As if something answered from far
> away.

**Après le coup :**

> The robbers copied our gem files!
> Now they know where every gem sleeps.
> — — —
> Someone must warn the other towns,
> {PLAYER}!

#### Jardinière (31,8)

> These berries are for ranch animals.
> Not for picking, sorry!
> — — —
> The pens are east, beyond the trees.

**Après le coup :**

> The ranch lost its tracker POKéMON.
> The berries just sit there now.
> — — —
> Whoever took them will have to feed
> them. I hope they know how.

#### Dame (36,23)

> Garnet is the stone of this town.
> Red roofs, red trees, red stone.
> — — —
> The sea road south needs SURF. Come
> back when you can ride the waves.

**Après le coup :**

> Red roofs, red trees, red stone...
> And now an empty case at school.
> — — —
> Tired, {PLAYER}? Go home and let
> MOM tend to your POKéMON.

#### Homme (PC) (19,19 (se promène))

> Technology is incredible!
> You can now store and recall items
> and POKéMON as data via PC.
> — — —
> The PC network was down at dawn.
> Funny, just when the ranch alarm
> went off.

**Après le coup :**

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
> The GRENAT is in our hands, and the
> LAB's files on gems were copied while
> you were busy at the RANCH.
> — — —
> GRENALUX will see us again...

Effets : le sbire disparaît, `FLAG_GRENALUX_ONYBRIS_STRIKE` est posé (état D).


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

**Daisy** (10,6) — *après le coup (après le combat du rival)*

> DAISY: Dad is mending the fence,
> and Grandpa is not himself.
> — — —
> Please be careful out there,
> {PLAYER}. And take care of {RIVAL}.

Autres états de Daisy (carte du monde, toilettage après la Ligue) : textes d’origine.


## 5. L’école (`PalletTown_School`)

**Professeure** (6,2) — *avant le coup, 1re visite*

> Welcome to the GRENALUX SCHOOL!
> — — —
> Our pride is the GRENAT in the science
> case, a gem that hums when a POKéMON's
> AURA is near.
> — — —
> Legend says the GRENAT is tied to
> JIRACHI's wish. Ten years ago, the
> AURA changed every POKéMON's type...
> — — —
> Funny how nobody knows why.

**Professeure** () — *suite : cours*

> Since you are here, a short lesson.
> — — —
> Ten years ago the AURA changed the
> types of many POKéMON. FIRE ones may
> now be ICE, and WATER ones STEEL.
> — — —
> A new type also appeared: FAIRY.
> It beats DRAGON, FIGHTING and DARK,
> but POISON and STEEL beat it.
> — — —
> Never trust a POKéMON's old type.
> Check it in the SUMMARY first!

**Professeure** () — *fin du cours*

> I wrote it all down for you.
> Read it whenever you doubt.

**Professeure** () — *visites suivantes*

> Remember: check a POKéMON's type in
> the SUMMARY. The old ones lie.

**Professeure** () — *après le coup*

> They came this morning, all in black.
> They took the GRENAT before I could
> even reach the alarm.
> — — —
> They said it was for the POKéMON,
> for their freedom... What does a
> gem have to do with freedom?
> — — —
> There is no class today.

**Professeure** () — *après le coup, si pas de mémo*

> Still, a teacher teaches. Types changed
> ten years ago, and FAIRY now beats
> DRAGON, FIGHTING and DARK.
> — — —
> I wrote it down for you.

**Élève** (4,5) — *avant*

> My grandpa says FIRE POKéMON were
> only FIRE once. Now look at them...
> — — —
> He says the world turned upside down,
> and all he did was grow old.

**Élève** () — *après*

> Grandpa says thieves used to hide
> their faces. These ones were proud
> of it.
> — — —
> We got the day off, but nobody feels
> like playing.

**Vitrine du GRENAT** (8-9,2) — *avant*

> A glass case on the science shelf.
> It holds the GRENAT, a deep red gem
> that glows when POKéMON gather near.

**Vitrine** () — *après*

> The glass case is empty. A note is
> left behind: POKéMON were never
> meant to be owned. - TEAM ONYBRIS

**Tableau de l’aura** (4-5,1) — *toujours*

> The AURA of ten years ago.
> Records show every POKéMON's type
> changed in a single night.


## 6. Le laboratoire (`PalletTown_ProfessorOaksLab`)
Choix du partenaire et combat du rival : scènes d’origine (adaptées au rival de Topaze). Après le coup :

**Assistant 1** (3,11) — *après le coup*

> Someone got into the archive room
> last night and copied every file
> on gemstones.
> — — —
> Nothing else was touched. That's
> what scares me.

**Assistant 2** (11,10) — *après le coup*

> The PROF. says the GRENAT in the
> museum and the files here are two
> halves of the same puzzle.
> — — —
> Whoever hit both knows exactly what
> they're after.

**Ordinateur** (2-3,1) — *après le coup*

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

**Ouvrier 1** (9,7) — *avant*

> This ranch runs from the town wall
> to the far fences. It takes ten of
> us to look after it all.

**Ouvrier 1** (9,7) — *après le coup*

> The east fence was cut last night.
> On a ranch this big, no one saw.

**Ouvrier 2** (14,12) — *avant*

> The east pasture is so far out, we
> only check it twice a day.

**Ouvrier 2** (14,12) — *après le coup*

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

**Ouvrier 3** (28,13 (apparaît après le coup, clôture coupée)) — *après le coup*

> The pens were shut tight last night.
> Now look at this fence...

Animaux (Slowpoke, Psyduck, Meowth, Jigglypuff, Doduo, Nidoran) : cris et phrases d’ambiance ; Doduo et les deux Nidoran disparaissent après le coup.


## 8. Reste à faire sur Grenalux
- Poser `FLAG_ONYBRIS_ANIMALS_FOUND` au QG d’Onybris de Bourg Quartz (étape 6 du parcours) : la quête du ranch est alors terminable.
- Faire réapparaître Doduo et les deux Nidoran dans les enclos quand la quête est rendue.
- Mine : seule la grille scellée existe (panneau 39,24). L’ouverture après la Ligue demande un intérieur (à décider).
- Lore à trancher : le GRENAT de l’école est-il la vraie gemme ou un leurre ? (Le plan actuel : l’école a l’exemplaire de vitrine ; le « vrai » GRENAT est offert par l’ouvrier du ranch.)
