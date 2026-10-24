@ Journal televise d'Onybris (ecran des Centres Pokemon). 5 paliers selon la progression,
@ 2 reportages par palier tires au hasard.

Topaze_EventScript_NewsTV::
	lockall
	msgbox Topaze_News_Text_TurnOn, MSGBOX_DEFAULT
	goto_if_set FLAG_SYS_GAME_CLEAR, Topaze_News_Quiet
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

@ --- Recruteur d'Onybris (Centres Pokemon) : visible de 4 badges jusqu'a la victoire sur le Champion.
Topaze_EventScript_RecruiterCheck::
	setflag FLAG_TOPAZE_HIDE_RECRUITER
	goto_if_set FLAG_SYS_GAME_CLEAR, Topaze_Recruiter_CheckEnd
	goto_if_unset FLAG_BADGE04_GET, Topaze_Recruiter_CheckEnd
	clearflag FLAG_TOPAZE_HIDE_RECRUITER
Topaze_Recruiter_CheckEnd::
	return

Topaze_EventScript_Recruiter::
	lock
	faceplayer
	goto_if_set FLAG_VR_BOSS_DONE, Topaze_Recruiter_T3
	goto_if_set FLAG_BADGE06_GET, Topaze_Recruiter_T2
	random 2
	goto_if_eq VAR_RESULT, 0, Topaze_Recruiter_T1A
	msgbox Topaze_Recruiter_Text_T1B, MSGBOX_DEFAULT
	goto Topaze_Recruiter_End

Topaze_Recruiter_T1A::
	msgbox Topaze_Recruiter_Text_T1A, MSGBOX_DEFAULT
	goto Topaze_Recruiter_End

Topaze_Recruiter_T2::
	random 2
	goto_if_eq VAR_RESULT, 0, Topaze_Recruiter_T2A
	msgbox Topaze_Recruiter_Text_T2B, MSGBOX_DEFAULT
	goto Topaze_Recruiter_End

Topaze_Recruiter_T2A::
	msgbox Topaze_Recruiter_Text_T2A, MSGBOX_DEFAULT
	goto Topaze_Recruiter_End

Topaze_Recruiter_T3::
	random 2
	goto_if_eq VAR_RESULT, 0, Topaze_Recruiter_T3A
	msgbox Topaze_Recruiter_Text_T3B, MSGBOX_DEFAULT
	goto Topaze_Recruiter_End

Topaze_Recruiter_T3A::
	msgbox Topaze_Recruiter_Text_T3A, MSGBOX_DEFAULT
	goto Topaze_Recruiter_End

Topaze_Recruiter_End::
	release
	end

Topaze_Recruiter_Text_T1A::
	.string "RECRUIT: Relax. I am not here to\n"
	.string "fight, only to talk.\p"
	.string "I used to run a delivery route.\n"
	.string "My POKéMON hauled crates fourteen\l"
	.string "hours a day for nothing.\p"
	.string "Then someone gave me a black\n"
	.string "uniform and a reason.$"

Topaze_Recruiter_Text_T1B::
	.string "RECRUIT: There are people like me\n"
	.string "in every town now. Quiet ones.\p"
	.string "We do not steal. We listen, sign\n"
	.string "people up, carry messages.\p"
	.string "The ones who fight are GRUNTS.\n"
	.string "Above them, EXECUTIVES. Above them,\l"
	.string "someone nobody names.$"

Topaze_Recruiter_Text_T2A::
	.string "RECRUIT: Did you hear? HEMATOWN\n"
	.string "fell without a single shout.\p"
	.string "The guards clocked out and never\n"
	.string "came back. That is how it works:\l"
	.string "we do not break doors, we rewrite\l"
	.string "the rules.\p"
	.string "There are thousands of us.$"

Topaze_Recruiter_Text_T2B::
	.string "RECRUIT: Join us or do not. The\n"
	.string "stones are leaving this region and\l"
	.string "nobody can stop it.\p"
	.string "I am not paid. I simply stopped\n"
	.string "being afraid of the dark.$"

Topaze_Recruiter_Text_T3A::
	.string "RECRUIT: Ten stones, one hand.\n"
	.string "We said it would happen.\p"
	.string "Whatever the LEAGUE planned, it is\n"
	.string "too late. I am only here to see\l"
	.string "that the road stays clear for him.$"

Topaze_Recruiter_Text_T3B::
	.string "RECRUIT: I came to heal a POKéMON\n"
	.string "that was never mine to begin with.\p"
	.string "They told me: you will understand\n"
	.string "in a few days.\p"
	.string "I think I already do.$"

@ --- Cameos des cadres (sans combat) dans trois Centres : ils obeissent a quelqu'un, ils sont nombreux.
Topaze_EventScript_VesperCheck::
	setflag FLAG_TOPAZE_HIDE_VESPER
	goto_if_unset FLAG_BADGE05_GET, Topaze_Cameo_VesperEnd
	goto_if_set FLAG_BADGE07_GET, Topaze_Cameo_VesperEnd
	clearflag FLAG_TOPAZE_HIDE_VESPER
Topaze_Cameo_VesperEnd::
	return

Topaze_EventScript_SeleneCheck::
	setflag FLAG_TOPAZE_HIDE_SELENE
	goto_if_unset FLAG_BADGE03_GET, Topaze_Cameo_SeleneEnd
	goto_if_set FLAG_BADGE04_GET, Topaze_Cameo_SeleneEnd
	clearflag FLAG_TOPAZE_HIDE_SELENE
Topaze_Cameo_SeleneEnd::
	return

Topaze_EventScript_KronosCheck::
	setflag FLAG_TOPAZE_HIDE_KRONOS
	goto_if_unset FLAG_BADGE04_GET, Topaze_Cameo_KronosEnd
	goto_if_set FLAG_BADGE06_GET, Topaze_Cameo_KronosEnd
	clearflag FLAG_TOPAZE_HIDE_KRONOS
Topaze_Cameo_KronosEnd::
	return

Topaze_EventScript_VesperCameo::
	lock
	faceplayer
	msgbox Topaze_Cameo_Text_Vesper, MSGBOX_DEFAULT
	release
	end

Topaze_EventScript_SeleneCameo::
	lock
	faceplayer
	msgbox Topaze_Cameo_Text_Selene, MSGBOX_DEFAULT
	release
	end

Topaze_EventScript_KronosCameo::
	lock
	faceplayer
	msgbox Topaze_Cameo_Text_Kronos, MSGBOX_DEFAULT
	release
	end

Topaze_Cameo_Text_Vesper::
	.string "VESPER: ...Yes. Understood. HEMATEK\n"
	.string "is on schedule. No, the child is\l"
	.string "not a problem. Yet.\p"
	.string "...Oh. The pendant.\p"
	.string "Relax, I am off duty. The BOSS\n"
	.string "forbids brawls in a POKéMON CENTER.\l"
	.string "Even we have rules.\p"
	.string "Seven branches, one per corner of\n"
	.string "the map. I only run the quiet one.\l"
	.string "Try to keep up.$"

Topaze_Cameo_Text_Selene::
	.string "SELENE: Yes. The tower is quiet\n"
	.string "again. The stone left with KRONOS.\p"
	.string "...You. The one who walks on while\n"
	.string "his hands shake. I like that.\p"
	.string "Do not mistake us for thieves. A\n"
	.string "thief needs hiding. We have\l"
	.string "thousands of mouths that agree.\p"
	.string "Go on. We will meet again.$"

Topaze_Cameo_Text_Kronos::
	.string "KRONOS: ...Understood. All branches\n"
	.string "report in. The road is clear.\p"
	.string "A courtesy, child. We never needed\n"
	.string "to hurry. You are the one running.\p"
	.string "We are not behind you. We are\n"
	.string "waiting where you are going.$"
