# Grenalux — script détaillé (parcours du joueur)
*Généré par `docs/scenario/gen_grenalux.py` à partir des textes du jeu : ce document est toujours à jour avec le code. Les textes sont des placeholders anglais ; seule la structure est figée.*

## 0. Principe : l’attaque se vit en direct
Rien n’est volé avant le début du jeu. Grenalux est d’abord **paisible** (état A) ; l’attaque d’Zircon se déroule sous les yeux du joueur, au ranch du rival, puis le village bascule dans l’état « après » (B) : clôture du ranch coupée, animaux disparus, vitrine de l’école vide, labo fouillé. Le drapeau `FLAG_GRENALUX_ZIRCON_STRIKE` est posé à la fin de la scène du ranch ; tous les PNJ de la ville ont un texte A et un texte B.

`VAR_GRENALUX_OPENING` pilote la séquence : 0 = début ; 1 = scène du ranch en cours ; 2 = école à faire ; 3 = labo à faire ; 4 = séquence terminée (la ville est libre, la sortie nord n’est plus bloquée).

## 1. Chronologie du joueur
1. **Début** : discours de Chêne d’origine → chambre (2F) → rez-de-chaussée. Maman : « Chêne est au ranch d’à côté avec le père du rival, il te cherchait. » Ville **paisible** : les PNJ parlent de la vie du village.
2. **Sortie nord** : le rival arrête le joueur et l’emmène au ranch (maison du rival).
3. **Ranch (scène)** : le père et Chêne accueillent le joueur → les trackers hurlent → un sbire d’Zircon entre : « Nous libérons les POKéMON du ranch ; mes amis sont à l’école et au labo ». Le père court aux enclos. Chêne panique et tend trois POKé BALLS : **le joueur choisit son partenaire en urgence** (menu BULBASAUR / SQUIRTLE / CHARMANDER, confirmation, surnom). Le rival prend celui qui bat le sien. **Combat contre le sbire** (didacticiel de combat de Chêne ; si le joueur perd, la scène continue). Le sbire fuit, Chêne part vérifier son labo. **Maman arrive** en courant, inquiète, puis attendrie par le POKéMON, et lui remet un **PENDENTIF** (sans dire ce que c’est), en lui conseillant d’aller à l’école.
4. **Ville (état B)** : la sortie nord est bloquée (« d’abord l’école, Chêne attend au labo »).
5. **École (scène)** : vitrine vide, la professeure donne le cours sur les types et le **TYPE MEMO**, regarde le pendentif sans rien dire ; le rival surgit et **défie le joueur avec le partenaire opposé** (combat, pas de whiteout).
6. **Labo (scène)** : Chêne annonce que ses fichiers ont été copiés, remet le **POKÉDEX** et 5 POKé BALLS ; le rival part. La ville est libre.
7. **Plus tard** : maman soigne gratuitement quand on rentre. (Le colis de Chêne à Opanihrum a été supprimé.)

## 2. Maison du joueur

**Maman** (8,4 rez-de-chaussée) — *avant la scène du ranch, garçon*

> MOM: …Right.
> All boys leave home someday.
> It said so on TV.
> — — —
> But don't go out in your slippers!
> Put on your sports shoes first.
> — — —
> Oh, and PROF. OAK is at the RANCH
> next door with {RIVAL}'s dad. He was
> looking for you.

**Maman** (8,4) — *avant la scène du ranch, fille*

> MOM: …Right.
> All girls dream of traveling.
> It said so on TV.
> — — —
> But don't go out in your slippers!
> Put on your sports shoes first.
> — — —
> Oh, and PROF. OAK is at the RANCH
> next door with {RIVAL}'s dad. He was
> looking for you.

Après la scène du ranch : soin gratuit, puis :

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

**État A — paisible :**

> The vein under this hill is old.
> Garnet grows like frost in the dark.
> — — —
> We cut only what the mine lets go.

**État B — après l’attaque :**

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

**État A — paisible :**

> My grandfather carried the first
> crystal up from the mine. They say
> the monument hums at night.
> — — —
> Lately, it hums louder.

**État B — après l’attaque :**

> Every town keeps a stone of its own,
> they say. Garnet is ours.
> — — —
> Take the stones, and a town forgets
> its own name.

#### Fillette (17,30 (se promène))

**État A — paisible :**

> The pond turns purple at dusk!
> My teacher says it is the garnet.
> — — —
> She has a real GRENAT at school!

**État B — après l’attaque :**

> The school's GRENAT is gone!
> The pond looks sad today.
> — — —
> Don't let them take the monument!

#### Garçon (29,31 (se promène))

**État A — paisible :**

> Some POKéMON got new types when the
> AURA changed. Even FAIRY is new!
> — — —
> Teacher knows everything about it.
> Go to the school and ask!

**État B — après l’attaque :**

> No school today, because of the
> robbery. But teacher still gives the
> TYPE MEMO to trainers who ask.

#### Scientifique (33,23)

**État A — paisible :**

> The lab measures the aura of every
> crystal in town. The readings jumped
> this morning.
> — — —
> As if something answered from far
> away.

**État B — après l’attaque :**

> The robbers copied our gem files!
> Now they know where every gem sleeps.
> — — —
> Someone must warn the other towns,
> {PLAYER}!

#### Jardinière (31,8)

**État A — paisible :**

> These berries are for ranch animals.
> Not for picking, sorry!
> — — —
> The pens are east, beyond the trees.

**État B — après l’attaque :**

> The ranch lost its tracker POKéMON.
> The berries just sit there now.
> — — —
> Whoever took them will have to feed
> them. I hope they know how.

#### Dame (36,23)

**État A — paisible :**

> Garnet is the stone of this town.
> Red roofs, red trees, red stone.
> — — —
> The sea road south needs SURF. Come
> back when you can ride the waves.

**État B — après l’attaque :**

> Red roofs, red trees, red stone...
> And now an empty case at school.
> — — —
> Tired, {PLAYER}? Go home and let
> MOM tend to your POKéMON.

#### Homme (PC) (19,19 (se promène))

**État A — paisible :**

> Technology is incredible!
> You can now store and recall items
> and POKéMON as data via PC.

**État B — après l’attaque :**

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

### Blocage de la sortie nord (après le ranch, avant la fin du labo)

> {PLAYER}: Not yet. MOM said to see
> the SCHOOL first, and PROF. OAK is
> waiting at the LAB.


## 4. La scène du ranch (`PalletTown_RivalsHouse`) — l’attaque

**Père du rival**

> {RIVAL}'s DAD: So you're {PLAYER}.
> {RIVAL} never stops talking about you.

**Chêne**

> OAK: Good, we're all here.
> — — —
> Ten years ago the AURA changed every
> POKéMON. Lately my trackers have been
> restless, as if they felt something.
> — — —
> That is why I brought three POKé
> BALLS with me today. {PLAYER}, {RIVAL},
> you have both waited long enough, and--

**Chêne**

> ...Do you hear that?
> The trackers are howling.

**Sbire d’Zircon (entre par la porte)**

> Nobody move!
> TEAM ZIRCON is freeing the POKéMON
> of this ranch!
> — — —
> My friends are at the SCHOOL and the
> LAB right now. Today, we take it all!

**Père du rival (sort en courant)**

> {RIVAL}'s DAD: My pens! Stay here!

**Chêne (panique, tend les POKé BALLS)**

> OAK: Oh no, oh no, oh no!
> What do we do?!
> — — —
> There is no time to be polite!
> {PLAYER}, take one of these, quick!

**Chêne (menu du choix du partenaire)**

> OAK: Which one?
> Hurry, hurry!

**Rival (prend le partenaire opposé)**

> {RIVAL}: Then I'll take the one that
> beats yours! Gramps, give it here!

**Sbire (avant le combat)**

> Hah! A kid with a brand new partner?
> — — —
> Let's see if it fights for you, or
> just obeys!

**Sbire (battu)**

> Tch... it fights for you by
> choice? That's... not what the
> boss told us.

**Sbire (si le joueur perd)**

> Hah! Too easy.
> But we don't need you anyway.

**Sbire (fuit)**

> Forget it. We got what we came for.
> — — —
> The trackers are already on the road.
> GRENALUX will see us again...

**Chêne (part au labo)**

> OAK: ...Well! That was a real battle,
> {PLAYER}. Your partner trusts you.
> — — —
> I must see what they did to my LAB.
> Stay safe, both of you!

**Maman (arrive, donne le pendentif)**

> MOM: {PLAYER}!!
> Are you hurt? The whole town heard
> the alarm!
> — — —
> ...Is that a POKéMON? Your first one?
> Oh, look at you. You look so proud.
> — — —
> Listen, the SCHOOL was broken into
> too. Your teacher is waiting for you.
> — — —
> If you're going to travel with that
> little one, you should learn what has
> changed first.
> — — —
> And take this with you. It has been in
> our family a long time.

**Objet reçu**

> {PLAYER} received the PENDANT!

**Maman (au revoir)**

> MOM: Keep it close, and don't lose it.
> — — —
> Come home whenever you need a rest.
> I'll be waiting.

**Daisy** (10,6) — *après l’attaque*

> DAISY: Dad is mending the fence,
> and Grandpa is not himself.
> — — —
> Please be careful out there,
> {PLAYER}. And take care of {RIVAL}.

Autres états de Daisy (carte du monde, toilettage après la Ligue) : textes d’origine.


## 5. L’école (`PalletTown_School`)
### Avant l’attaque

**Professeure** (6,2) — *état A*

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

**Élève** (4,5) — *état A*

> My grandpa says FIRE POKéMON were
> only FIRE once. Now look at them...
> — — —
> He says the world turned upside down,
> and all he did was grow old.

**Vitrine du GRENAT** (8-9,2) — *état A*

> A glass case on the science shelf.
> It holds the GRENAT, a deep red gem
> that glows when POKéMON gather near.

### Scène d’arrivée (après la scène du ranch)

**Professeure** () — *scène*

> TEACHER: {PLAYER}! Thank goodness you
> are safe.
> — — —
> Your MOM called. A first partner, at
> last. Good.
> — — —
> But look at that case... They emptied
> it while the town ran to the RANCH.
> The GRENAT is gone.
> — — —
> Still, nobody learns anything by
> crying over a stone.

**Professeure** () — *cours*

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

**Objet reçu** () — **

> {PLAYER} received the TYPE MEMO!

**Professeure** () — *le pendentif*

> TEACHER: ...That pendant around your
> neck. May I?
> — — —
> ...No. Forget it. It is none of my
> business. Keep it close, {PLAYER}.

**Rival** (entre à 3,7) — *défi (combat avec le partenaire opposé)*

> {RIVAL}: There you are!
> — — —
> I took the other POKé BALL Gramps
> had, and mine beats yours!
> — — —
> Let's see which of us is stronger.
> Come on, I'll take you on!

**Rival** () — *après le combat*

> {RIVAL}: Tch... lucky.
> — — —
> Gramps wants us at the LAB, doesn't
> he? Race you there!

### Après

**Professeure** (6,2) — *état B*

> They came while the town ran to the
> RANCH, all in black. They took the
> GRENAT before I could reach the alarm.
> — — —
> They said it was for the POKéMON,
> for their freedom... What does a
> gem have to do with freedom?
> — — —
> There is no class today.

**Élève** (4,5) — *état B*

> Grandpa says thieves used to hide
> their faces. These ones were proud
> of it.
> — — —
> We got the day off, but nobody feels
> like playing.

**Vitrine** (8-9,2) — *état B*

> The glass case is empty. A note is
> left behind: POKéMON were never
> meant to be owned. - TEAM ZIRCON

**Tableau de l’aura** (4-5,1) — *toujours*

> The AURA of ten years ago.
> Records show every POKéMON's type
> changed in a single night.


## 6. Le laboratoire (`PalletTown_ProfessorOaksLab`)
Le choix du partenaire n’a plus lieu ici (il se fait au ranch). Scène d’arrivée après l’école :

**Chêne** (6,3) — *scène du POKÉDEX*

> OAK: {PLAYER}! {RIVAL}! Both of you
> in one piece. Good.
> — — —
> They got into my LAB too. Nothing
> was broken, but every file on gems,
> AURA and JIRACHI was copied.
> — — —
> Whoever leads them is looking for
> something, and I can't chase it
> alone. That is why I need you two.

Puis, d’origine : demande, POKÉDEX, 5 POKé BALLS, explications, rêve de Chêne, le rival part. Aides et ordinateur (état B) :

**Assistant 1** (3,11) — *état B*

> Someone got into the archive room
> this morning and copied every file
> on gemstones.
> — — —
> Nothing else was touched. That's
> what scares me.

**Assistant 2** (11,10) — *état B*

> The PROF. says the GRENAT in the
> museum and the files here are two
> halves of the same puzzle.
> — — —
> Whoever hit both knows exactly what
> they're after.

**Ordinateur** (2-3,1) — *état B*

> ACCESS LOG: archive opened at 9:41.
> Files copied: GEMSTONES, AURA
> RECORDS, JIRACHI.

**Chêne** (6,3) — *après 4 badges (une fois)*

> OAK: Four BADGES! I hear that each
> town you visit keeps a gem, and that
> someone is collecting them.
> — — —
> TEAM ZIRCON believes they can tear
> POKéMON away from people for good.
> — — —
> Their leader fights the AURA with
> every step. Be careful, {PLAYER}.

Chêne : plus de colis (supprimé) ; retour final = scène du Pokédex national d’origine après la Ligue.


## 7. Le ranch (`PalletTown_Ranch`, zone extérieure)

**Ouvrier 1** (9,7) — *état A*

> This ranch runs from the town wall
> to the far fences. It takes ten of
> us to look after it all.

**Ouvrier 1** (9,7) — *état B*

> The east fence was cut this morning.
> On a ranch this big, no one saw.

**Ouvrier 2** (14,12) — *état A*

> The east pasture is so far out, we
> only check it twice a day.

**Ouvrier 2** (14,12) — *état B*

> They took the tracker POKéMON from
> the pens. The fence was cut open.

**Ouvrier 1** (9,7) — *Doduo + 2 Nidoran retrouvés*

> DODUO and both NIDORAN just trotted
> back into the pens, safe!
> — — —
> The boss says you found them on the
> road. Please, take these.

**Ouvrier 1** () — *récompense : 1 POTION + 5 POKé BALLS*

> The boss says it is the least we can
> do. Take care of them out there.

**Ouvrier 1** () — *après*

> The animals are calm again.
> Thank you for everything.

**Ouvrier 3** (28,13 (clôture coupée)) — *état B*

> The pens were shut tight this morning.
> Now look at this fence...

Animaux (Slowpoke, Psyduck, Meowth, Jigglypuff, Doduo, Nidoran) : cris et phrases d’ambiance ; Doduo et les deux Nidoran disparaissent à l’état B (volés pendant l’attaque).


## 8. Reste à faire sur Grenalux
- Quête du ranch **terminée sur la Route 1** : après l’attaque, DODUO + 2 NIDORAN errent sur la route (x11–17, y25–27) ; il faut parler **aux trois** (`FLAG_ROUTE1_TALKED_DODUO/NIDORANM/NIDORANF`) pour les renvoyer au ranch (`FLAG_ZIRCON_ANIMALS_FOUND`), ils réapparaissent dans les enclos, l’ouvrier près de la clôture donne 1 POTION + 5 POKé BALLS (`FLAG_GRENALUX_GEM_REWARD`).
- Route 1 : aucun dresseur ; PNJ = vendeur (Potion), garçon (herbe qui change de couleur), panneau ; herbe : Pidgey / Rattata niv. 3–7, Spearow rare niv. 6–7.
- Faire réapparaître Doduo et les deux Nidoran dans les enclos quand la quête est rendue.
- Mine : seule la grille scellée existe ; son ouverture après la Ligue demande un intérieur (à décider).
- Le PENDENTIF (ancien `ITEM_RUBY`) est le « vrai » GRENAT, mais son importance n’est révélée que plus tard : à décider avec la quête des gemmes.
