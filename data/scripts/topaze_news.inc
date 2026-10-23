@ Journal televise d'Onybris (ecran des Centres Pokemon). 5 paliers selon la progression,
@ 2 reportages par palier tires au hasard.

Topaze_EventScript_NewsTV::
	lockall
	msgbox Topaze_News_Text_TurnOn, MSGBOX_DEFAULT
	goto_if_set FLAG_DEFEATED_CHAMP, Topaze_News_Quiet
	goto_if_set FLAG_VR_BOSS_DONE, Topaze_News_T5
	goto_if_set FLAG_BADGE07_GET, Topaze_News_T4
	goto_if_set FLAG_BADGE05_GET, Topaze_News_T3
	goto_if_set FLAG_BADGE03_GET, Topaze_News_T2
	goto Topaze_News_T1

Topaze_News_T1::
	random 2
	goto_if_eq VAR_RESULT, 0, Topaze_News_T1A
	msgbox Topaze_News_Text_T1B, MSGBOX_DEFAULT
	goto Topaze_News_End

Topaze_News_T1A::
	msgbox Topaze_News_Text_T1A, MSGBOX_DEFAULT
	goto Topaze_News_End

Topaze_News_T2::
	random 2
	goto_if_eq VAR_RESULT, 0, Topaze_News_T2A
	msgbox Topaze_News_Text_T2B, MSGBOX_DEFAULT
	goto Topaze_News_End

Topaze_News_T2A::
	msgbox Topaze_News_Text_T2A, MSGBOX_DEFAULT
	goto Topaze_News_End

Topaze_News_T3::
	random 2
	goto_if_eq VAR_RESULT, 0, Topaze_News_T3A
	msgbox Topaze_News_Text_T3B, MSGBOX_DEFAULT
	goto Topaze_News_End

Topaze_News_T3A::
	msgbox Topaze_News_Text_T3A, MSGBOX_DEFAULT
	goto Topaze_News_End

Topaze_News_T4::
	random 2
	goto_if_eq VAR_RESULT, 0, Topaze_News_T4A
	msgbox Topaze_News_Text_T4B, MSGBOX_DEFAULT
	goto Topaze_News_End

Topaze_News_T4A::
	msgbox Topaze_News_Text_T4A, MSGBOX_DEFAULT
	goto Topaze_News_End

Topaze_News_T5::
	random 2
	goto_if_eq VAR_RESULT, 0, Topaze_News_T5A
	msgbox Topaze_News_Text_T5B, MSGBOX_DEFAULT
	goto Topaze_News_End

Topaze_News_T5A::
	msgbox Topaze_News_Text_T5A, MSGBOX_DEFAULT
	goto Topaze_News_End

Topaze_News_Quiet::
	msgbox Topaze_News_Text_Quiet, MSGBOX_DEFAULT
	goto Topaze_News_End

Topaze_News_End::
	releaseall
	end

Topaze_News_Text_TurnOn::
	.string "The screen is tuned to the news.$"

Topaze_News_Text_T1A::
	.string "NEWS: A string of thefts shakes\n"
	.string "the region. Gems vanish from\l"
	.string "museums, schools and ranches.\p"
	.string "Police blame isolated gangs.\n"
	.string "Every witness describes the same\l"
	.string "black uniforms.$"

Topaze_News_Text_T1B::
	.string "NEWS: A group calling itself TEAM\n"
	.string "ONYBRIS posted a message today.\p"
	.string "POKéMON were never meant to be\n"
	.string "owned. We are the ones who listen.\p"
	.string "Its followers are already counted\n"
	.string "in the hundreds.$"

Topaze_News_Text_T2A::
	.string "NEWS: TEAM ONYBRIS is no longer\n"
	.string "called a gang. Officials admit it\l"
	.string "has ranks, bases and funding.\p"
	.string "Reports speak of GRUNTS in the\n"
	.string "field, EXECUTIVES giving orders,\l"
	.string "and someone above them all.$"

Topaze_News_Text_T2B::
	.string "NEWS: The stolen stones are not\n"
	.string "being sold. Experts say the thefts\l"
	.string "follow a single plan.\p"
	.string "The gems are being gathered,\n"
	.string "somewhere, by someone patient.$"

Topaze_News_Text_T3A::
	.string "NEWS: A city has gone silent.\n"
	.string "Tower lights burn all night under\l"
	.string "a black banner, and no one comes\l"
	.string "out to talk.\p"
	.string "Locals say ONYBRIS recruits will\n"
	.string "not leave their posts.$"

Topaze_News_Text_T3B::
	.string "NEWS: ONYBRIS recruiters now work\n"
	.string "openly in many towns, handing out\l"
	.string "leaflets: Free the POKéMON.\p"
	.string "The group claims thousands of\n"
	.string "members. Police cannot confirm it,\l"
	.string "and cannot deny it.$"

Topaze_News_Text_T4A::
	.string "NEWS: Most of the stones are gone.\n"
	.string "The last ones sit under guard, and\l"
	.string "the sea itself has been closed by\l"
	.string "fire.\p"
	.string "The LEAGUE called an urgent session.\n"
	.string "Its answer: wait.$"

Topaze_News_Text_T4B::
	.string "NEWS: A voice cut into every radio\n"
	.string "at noon.\p"
	.string "The ten stones. Soon, all of them.\n"
	.string "Do not be afraid.\p"
	.string "No one has seen the speaker. His\n"
	.string "followers call him THE BOSS.$"

Topaze_News_Text_T5A::
	.string "NEWS: Black-clad figures were seen\n"
	.string "gathering on the road to the\l"
	.string "PLATEAU, in silence, in rows.\p"
	.string "The tournament will go on. No one\n"
	.string "dares say it should not.$"

Topaze_News_Text_T5B::
	.string "NEWS: Rumor says ten stones now\n"
	.string "lie in a single hand.\p"
	.string "The sky above the PLATEAU has\n"
	.string "turned strange. Trainers are\l"
	.string "advised to stay indoors.\p"
	.string "Few listen.$"

Topaze_News_Text_Quiet::
	.string "NEWS: TEAM ONYBRIS has fallen\n"
	.string "silent. Followers gather in small\l"
	.string "groups, unsure what to believe.\p"
	.string "The world waits to see what comes\n"
	.string "next.$"
