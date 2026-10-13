# Opanihrum — script détaillé (parcours du joueur)
*Généré par `docs/scenario/gen_opanihrum.py` à partir du code : toujours à jour. Textes = placeholders anglais.*

## Chronologie du joueur
1. **Arrivée** par la Route 1 (sud). Ville ordinaire : aucune scène à l’arrivée.
2. **Boutique** : à la première entrée, le vendeur reconnaît le joueur (« Tu viens de Grenalux ? ») et lui confie le **COLIS de CHÊNE** (objet clé). Le colis n’affecte plus le Pokédex (déjà donné) : seule la livraison compte.
3. **Vieil homme au barrage** (porte nord, Route 2) : tant que le colis n’est pas livré, il bloque la route (« propriété privée »). Livraison à Chêne (Grenalux, labo) → il a pris son café, fait la **démonstration de capture** et donne la **TEACHY TV**.
4. **Arène (la Fonderie, Hepha, Acier)** : portes verrouillées tant que les badges 1 à 7 ne sont pas tous obtenus ; message + saut en arrière.
5. Centre Pokémon et boutique : services d’origine (boutique : POKé BALL, POTION, ANTIDOTE, PARALYZE HEAL).


## Les rues d’Opanihrum (`ViridianCity`)

**PNJ FAT_MAN (14,25)** — `ViridianCity_EventScript_DreamEaterTutor`

> *(texte d’origine FireRed ou service)*

**PNJ OLD_MAN_1 (11,14)** — `ViridianCity_EventScript_OldMan`

> This GYM has been closed ever since
> the LEADER left on a long trip.
> — — —
> Rumor says HEPHA forges her own
> steel. I'd love to see it.

> OPANIHRUM GYM's LEADER returned!

**PNJ VAR_0 (18,6)** — `ViridianCity_EventScript_TutorialOldMan`

> Well, now, I've had my coffee, and
> that's what I need to get going!
> — — —
> But I made it too strong.
> It gave me a headache…
> — — —
> Incidentally, is my old TEACHY TV
> helping you?

> Wahaha!
> It's my grandson on the show!
> — — —
> Since he's the one doing the
> teaching, you're bound to learn.

> Well, now, I've had my coffee, and
> that's what I need to get going!
> — — —
> But I made it too strong.
> It gave me a headache…
> — — —
> Incidentally, are you filling your
> POKéDEX?
> — — —
> At first, focus on weakening the
> POKéMON before trying to catch it.

> I absolutely forbid you from
> going through here!
> — — —
> This is private property!

**PNJ WOMAN_3 (17,12)** — `ViridianCity_EventScript_Woman`

> I go shopping in PYROPIA
> occasionally.
> — — —
> I have to take the winding trail in
> CINDER FOREST when I go.

> Oh, Grandpa!
> Don't be so mean!
> — — —
> I'm so sorry. Since the TEAM ONYBRIS
> news, he doesn't trust strangers.

**PNJ YOUNGSTER (31,21)** — `ViridianCity_EventScript_Youngster`

> You want to know about the two
> kinds of caterpillar POKéMON?

> They look alike, but since the
> AURA they are not the same.
> — — —
> CATERPIE has a PSYCHIC side.
> WEEDLE has an ELECTRIC one.
> — — —
> Mind WEEDLE's sting. It shocks!

> Oh, okay then!

**PNJ BOY (26,24)** — `ViridianCity_EventScript_Boy`

> Ten years ago, the AURA changed
> every POKéMON's TYPE overnight.
> — — —
> My dad still can't believe his
> GROWLITHE is part ICE now.

**PNJ ITEM_BALL (15,5)** — `ViridianCity_EventScript_ItemPotion`

> *(texte d’origine FireRed ou service)*

**Panneau (23,3)** — `ViridianCity_EventScript_TrainerTips1`

> TRAINER TIPS
> — — —
> Catch POKéMON and expand your
> collection.
> — — —
> The more you have, the easier it
> is to battle.

**Panneau (11,13)** — `ViridianCity_EventScript_GymSign`

> OPANIHRUM POKéMON GYM
> THE FOUNDRY - LEADER: HEPHA

**Panneau (23,31)** — `ViridianCity_EventScript_TrainerTips2`

> TRAINER TIPS
> — — —
> The battle moves of POKéMON are
> limited by their POWER POINTS, PP.
> — — —
> To replenish PP, rest your tired
> POKéMON at a POKéMON CENTER.

**Panneau (23,16)** — `ViridianCity_EventScript_CitySign`

> OPANIHRUM 
> City of the Black Opal

**Panneau (8,11)** — `ViridianCity_EventScript_GymDoor`

> OPANIHRUM GYM's doors are locked…

## Boutique (`ViridianCity_Mart`)

**PNJ CLERK (2,3)** — `ViridianCity_Mart_EventScript_Clerk`

> Okay, thanks! Please say hi to
> PROF. OAK for me, too.

**PNJ YOUNGSTER (6,2)** — `ViridianCity_Mart_EventScript_Youngster`

> I've got to buy some POTIONS.
> — — —
> You never know when your POKéMON
> will need quick healing.

**PNJ WOMAN_1 (9,5)** — `ViridianCity_Mart_EventScript_Woman`

> This shop does good business in
> ANTIDOTES, I've heard.

## Maison (`ViridianCity_House`)

**PNJ BALDING_MAN (7,4)** — `ViridianCity_House_EventScript_BaldingMan`

> Coming up with nicknames is fun,
> but it's not so easy to do.
> — — —
> Clever names are nice, but simple
> names are easier to remember.

**PNJ LITTLE_GIRL (2,5)** — `ViridianCity_House_EventScript_LittleGirl`

> My daddy loves POKéMON, too.

**PNJ SPEAROW (6,6)** — `ViridianCity_House_EventScript_Speary`

> SPEARY: Tetweet!

**Panneau (7,1)** — `ViridianCity_House_EventScript_NicknameSign`

> SPEAROW
> Name: SPEARY

## École (`ViridianCity_School`)

**PNJ WOMAN_2 (6,2)** — `ViridianCity_School_EventScript_Woman`

> Okay!
> — — —
> Be sure to read what's on the
> blackboard carefully!

**PNJ LASS (4,5)** — `ViridianCity_School_EventScript_Lass`

> Whew! I'm trying to memorize all my
> notes.

**Panneau (4,4)** — `ViridianCity_School_EventScript_Notebook`

> Let's check out the notebook.
> — — —
> First page…
> — — —
> POKé BALLS are used to catch
> POKéMON.
> — — —
> Up to six POKéMON can be carried
> in your party.
> — — —
> People who raise and battle
> with POKéMON are called TRAINERS.

> Turn the page?

> Second page…
> — — —
> A healthy POKéMON may be hard to
> catch, so weaken it first.
> — — —
> Poison, burn, or cause another
> status problem to weaken it.

> Third page…
> — — —
> POKéMON TRAINERS seek others to
> engage in POKéMON battles.
> — — —
> To TRAINERS, the taste of victory
> is sweet, indeed.
> — — —
> Battles are constantly waged at
> POKéMON GYMS everywhere.

> Fourth page…
> — — —
> The ultimate goal for all POKéMON
> TRAINERS is simple.
> — — —
> It is to defeat the top eight
> POKéMON GYM LEADERS.
> — — —
> Do so to earn the right to face…
> — — —
> The ELITE FOUR of the POKéMON
> LEAGUE!

> GIRL: Hey!
> Don't look at my notes!

**Panneau (5,1)** — `ViridianCity_School_EventScript_Blackboard`

> The blackboard lists POKéMON
> STATUS problems during battles.

**Panneau (9,2)** — `ViridianCity_School_EventScript_PokemonJournal`

> *(texte d’origine FireRed ou service)*

## Centre Pokémon (`ViridianCity_PokemonCenter_1F`)

**PNJ NURSE (7,2)** — `ViridianCity_PokemonCenter_1F_EventScript_Nurse`

> *(texte d’origine FireRed ou service)*

**PNJ GENTLEMAN (12,5)** — `ViridianCity_PokemonCenter_1F_EventScript_Gentleman`

> Please feel free to use that PC in
> the corner.
> — — —
> The receptionist told me so.
> It's so kind of her!

**PNJ BOY (4,7)** — `ViridianCity_PokemonCenter_1F_EventScript_Boy`

> There's a POKéMON CENTER in every
> town ahead.
> — — —
> They charge no money, so don't
> be shy about healing POKéMON.

**PNJ YOUNGSTER (2,3)** — `ViridianCity_PokemonCenter_1F_EventScript_Youngster`

> POKéMON CENTERS heal your tired,
> hurt, or fainted POKéMON.
> — — —
> They make all POKéMON completely
> healthy.
