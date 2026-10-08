PewterCity_Gym_Text_BrockIntro::
    .string "So, you made it through OPANIHRUM\n"
    .string "and the forest. I'm KAY, LEADER\p"
    .string "of PYROPIA GYM.\p"
    .string "This town sleeps on a volcano.\n"
    .string "Heat, pressure, patience... that\p"
    .string "is how we live, and that is how\n"
    .string "my POKéMON fight.\p"
    .string "They are all FIRE-type! Since the\n"
    .string "AURA changed everything ten years\p"
    .string "ago, even ordinary flames burn\n"
    .string "differently.\p"
    .string "If you think you can take the\n"
    .string "heat, come on. Show me your\p"
    .string "best!{PLAY_BGM}{MUS_ENCOUNTER_GYM_LEADER}$"

@ NOTE: This defeat text actually causes a buffer overflow. It's too long for the gDisplayedStringBattle
@ buffer that it's put into, and it stomps all over the gBattleTextBuffs after, as well as the otherwise
@ unused array after that, sFlickerArray. Perhaps that's the reason why said array exists.
PewterCity_Gym_Text_BrockDefeat::
    .string "Hah... I was burning too bright\n"
    .string "and you stayed calm. Fair enough.\p"
    .string "Take the PYROPE BADGE.\p"
    .string "{FONT_NORMAL}{PLAYER} received the PYROPE BADGE\n"
    .string "from KAY!{PAUSE_MUSIC}{PLAY_BGM}{MUS_OBTAIN_BADGE}{PAUSE 0xFE}{PAUSE 0x56}{RESUME_MUSIC}\p"
    .string "{FONT_MALE}The PYROPE BADGE makes your\n"
    .string "POKéMON more powerful.\p"
    .string "It also lets you use FLASH outside\n"
    .string "of battle, if you carry the HM.$"

PewterCity_Gym_Text_TakeThisWithYou::
    .string "Wait!\n"
    .string "Take this with you.$"

PewterCity_Gym_Text_ReceivedTM39FromBrock::
    .string "{PLAYER} received TM35\n"
    .string "from KAY.$"

PewterCity_Gym_Text_ExplainTM39::
    .string "TM35 contains FLAMETHROWER.\p"
    .string "A reliable stream of fire that\n"
    .string "may burn the target. Keep it for\p"
    .string "a POKéMON that can really use it.$"

PewterCity_Gym_Text_BrockPostBattle::
    .string "Someone broke into the GRENALUX\n"
    .string "MUSEUM and took the GRENAT gem, I\p"
    .string "heard. TEAM ONYBRIS, they call\n"
    .string "themselves.\p"
    .string "They say POKé BALLS are chains.\n"
    .string "Maybe so. But a chain you choose\p"
    .string "and a chain someone forces on you\n"
    .string "are not the same thing.\p"
    .string "Go on to TOURMALIA. SYLVESTRE\n"
    .string "will not go easy on you.$"

PewterCity_Gym_Text_DontHaveRoomForThis::
    .string "You don't have room for this.$"

PewterCity_Gym_Text_LiamIntro::
    .string "Stop right there, kid!\p"
    .string "You are ten thousand light-years\n"
    .string "from facing KAY!$"

PewterCity_Gym_Text_LiamDefeat::
    .string "Darn!\p"
    .string "Light-years isn't time…\n"
    .string "It measures distance!$"

PewterCity_Gym_Text_LiamPostBattle::
    .string "You're pretty hot. ...But not as\n"
    .string "hot as KAY!$"

PewterCity_Gym_Text_LetMeTakeYouToTheTop::
    .string "Hiya!\n"
    .string "Do you want to dream big?\p"
    .string "Do you dare to dream of becoming\n"
    .string "the POKéMON champ?\p"
    .string "I'm no TRAINER, but I can advise\n"
    .string "you on how to win.\p"
    .string "Let me take you to the top!$"

PewterCity_Gym_Text_LetsGetHappening::
    .string "All right!\n"
    .string "Let's get happening!$"

PewterCity_Gym_Text_TryDifferentPartyOrders::
    .string "The first POKéMON out in a match is\n"
    .string "at the left of the POKéMON LIST.\p"
    .string "By changing the order of POKéMON,\n"
    .string "you may gain an advantage.\p"
    .string "Try different orders to suit your\n"
    .string "opponent's party.$"

PewterCity_Gym_Text_ItsFreeLetsGetHappening::
    .string "It's a free service!\n"
    .string "Let's get happening!$"

PewterCity_Gym_Text_YoureChampMaterial::
    .string "Just as I thought!\n"
    .string "You're POKéMON champ material!$"

PewterCity_Gym_Text_GymStatue::
    .string "PYROPIA POKéMON GYM\n"
    .string "LEADER: KAY\p"
    .string "WINNING TRAINERS:\n"
    .string "{RIVAL}$"

PewterCity_Gym_Text_GymStatuePlayerWon::
    .string "PYROPIA POKéMON GYM\n"
    .string "LEADER: KAY\p"
    .string "WINNING TRAINERS:\n"
    .string "{RIVAL}, {PLAYER}$"

