SaffronCity_MapScripts::
	map_script MAP_SCRIPT_ON_TRANSITION, SaffronCity_OnTransition
	.byte 0

SaffronCity_OnTransition::
	setworldmapflag FLAG_WORLD_MAP_SAFFRON_CITY
	setflag FLAG_TEMP_1
	setflag FLAG_TEMP_2
	setflag FLAG_TEMP_3
	call_if_unset FLAG_RESCUED_MR_FUJI, SaffronCity_EventScript_MoveDoorGuardGrunt
	end

SaffronCity_EventScript_MoveDoorGuardGrunt::
	setobjectxyperm LOCALID_SAFFRON_DOOR_GUARD_GRUNT, 33, 31
	return

SaffronCity_EventScript_RocketGrunt1::
	msgbox SaffronCity_Text_WhatDoYouWantGetLost, MSGBOX_NPC
	end

SaffronCity_EventScript_RocketGrunt2::
	msgbox SaffronCity_Text_BossTakeTownForTeamRocket, MSGBOX_NPC
	end

SaffronCity_EventScript_RocketGrunt3::
	msgbox SaffronCity_Text_DontGetDefiantOrIllHurtYou, MSGBOX_NPC
	end

SaffronCity_EventScript_RocketGrunt4::
	msgbox SaffronCity_Text_SaffronBelongsToTeamRocket, MSGBOX_NPC
	end

SaffronCity_EventScript_RocketGrunt5::
	msgbox SaffronCity_Text_CriminalLifeMakesMeFeelAlive, MSGBOX_NPC
	end

SaffronCity_EventScript_RocketGrunt6::
	msgbox SaffronCity_Text_WatchWhereYoureWalking, MSGBOX_NPC
	end

SaffronCity_EventScript_RocketGrunt7::
	msgbox SaffronCity_Text_WeCanExploitMonsAroundWorld, MSGBOX_NPC
	end

SaffronCity_EventScript_AllyStub::
	end

SaffronCity_EventScript_AlliesMeet::
	lockall
	setvar VAR_TEMP_1, 1
	goto_if_set FLAG_HEMATEK_ALLIES_IN, SaffronCity_EventScript_AlliesMeetEnd
	playse SE_PIN
	applymovement LOCALID_PLAYER, Common_Movement_ExclamationMark
	waitmovement 0
	clearflag FLAG_TEMP_1
	clearflag FLAG_TEMP_2
	clearflag FLAG_TEMP_3
	addobject LOCALID_HEMATOWN_BRICE
	addobject LOCALID_HEMATOWN_FLORA
	addobject LOCALID_HEMATOWN_N
	applymovement LOCALID_PLAYER, Common_Movement_WalkInPlaceFasterDown
	applymovement LOCALID_HEMATOWN_BRICE, SaffronCity_Movement_BriceComes
	applymovement LOCALID_HEMATOWN_FLORA, SaffronCity_Movement_FloraComes
	applymovement LOCALID_HEMATOWN_N, SaffronCity_Movement_NComes
	waitmovement 0
	msgbox SaffronCity_Text_AlliesMeet1
	msgbox SaffronCity_Text_AlliesMeet2
	msgbox SaffronCity_Text_AlliesMeet3
	msgbox SaffronCity_Text_AlliesMeet4
	closemessage
	applymovement LOCALID_PLAYER, SaffronCity_Movement_PlayerAside
	waitmovement 0
	applymovement LOCALID_HEMATOWN_BRICE, SaffronCity_Movement_BriceEnters
	waitmovement 0
	removeobject LOCALID_HEMATOWN_BRICE
	applymovement LOCALID_HEMATOWN_FLORA, SaffronCity_Movement_FloraEnters
	waitmovement 0
	removeobject LOCALID_HEMATOWN_FLORA
	applymovement LOCALID_HEMATOWN_N, SaffronCity_Movement_NEnters
	waitmovement 0
	removeobject LOCALID_HEMATOWN_N
	setflag FLAG_HEMATEK_ALLIES_IN
	releaseall
	end

SaffronCity_EventScript_AlliesMeetEnd::
	releaseall
	end

SaffronCity_Movement_BriceComes::
	walk_up
	walk_up
	walk_up
	walk_up
	step_end

SaffronCity_Movement_FloraComes::
	walk_up
	walk_up
	walk_up
	walk_up
	walk_up
	step_end

SaffronCity_Movement_NComes::
	walk_up
	walk_up
	walk_up
	walk_up
	walk_up
	step_end

SaffronCity_Movement_PlayerAside::
	walk_left
	step_end

SaffronCity_Movement_BriceEnters::
	walk_up
	walk_up
	step_end

SaffronCity_Movement_FloraEnters::
	walk_right
	walk_up
	walk_up
	step_end

SaffronCity_Movement_NEnters::
	walk_left
	walk_left
	walk_up
	walk_up
	step_end

SaffronCity_EventScript_DoorGuardGrunt::
	lock
	goto_if_set FLAG_HEMATEK_BOSS_DONE, SaffronCity_EventScript_DoorGuardGone
	goto_if_set FLAG_HEMATEK_ALLIES_IN, SaffronCity_EventScript_DoorGuardScared
	goto_if_set FLAG_RESCUED_MR_FUJI, SaffronCity_EventScript_DoorGuardAsleep
	applymovement LOCALID_SAFFRON_DOOR_GUARD_GRUNT, Common_Movement_FacePlayer
	waitmovement 0
	msgbox SaffronCity_Text_ImASecurityGuard
	release
	end

SaffronCity_EventScript_DoorGuardScared::
	msgbox SaffronCity_Text_GuardScared
	release
	end

SaffronCity_EventScript_DoorGuardGone::
	msgbox SaffronCity_Text_GuardGone
	release
	end

SaffronCity_EventScript_DoorGuardAsleep::
	textcolor NPC_TEXT_COLOR_NEUTRAL
	msgbox SaffronCity_Text_HesTakingASnooze
	release
	end

SaffronCity_EventScript_WorkerM::
	msgbox SaffronCity_Text_YouBeatTeamRocket, MSGBOX_NPC
	end

SaffronCity_EventScript_Youngster::
	msgbox SaffronCity_Text_SafeToGoOutAgain, MSGBOX_NPC
	end

SaffronCity_EventScript_Lass::
	msgbox SaffronCity_Text_PeopleComingBackToSaffron, MSGBOX_NPC
	end

SaffronCity_EventScript_Boy::
	msgbox SaffronCity_Text_FlewHereOnPidgeot, MSGBOX_NPC
	end

SaffronCity_EventScript_Pidgeot::
	lock
	faceplayer
	waitse
	playmoncry SPECIES_PIDGEOT, CRY_MODE_NORMAL
	msgbox SaffronCity_Text_Pidgeot
	waitmoncry
	release
	end

SaffronCity_EventScript_Man::
	msgbox SaffronCity_Text_SawRocketBossEscaping, MSGBOX_NPC
	end

SaffronCity_EventScript_CitySign::
	msgbox SaffronCity_Text_CitySign, MSGBOX_SIGN
	end

SaffronCity_EventScript_DojoSign::
	msgbox SaffronCity_Text_FightingDojo, MSGBOX_SIGN
	end

SaffronCity_EventScript_GymSign::
	lockall
	famechecker FAMECHECKER_SABRINA, 0
	msgbox SaffronCity_Text_GymSign
	releaseall
	end

SaffronCity_EventScript_TrainerTips1::
	msgbox SaffronCity_Text_FullHealCuresStatus, MSGBOX_SIGN
	end

SaffronCity_EventScript_TrainerTips2::
	msgbox SaffronCity_Text_GreatBallImprovedCatchRate, MSGBOX_SIGN
	end

SaffronCity_EventScript_SilphCoSign::
	msgbox SaffronCity_Text_SilphCoSign, MSGBOX_SIGN
	end

SaffronCity_EventScript_MrPsychicsHouseSign::
	msgbox SaffronCity_Text_MrPsychicsHouse, MSGBOX_SIGN
	end

SaffronCity_EventScript_SilphProductSign::
	msgbox SaffronCity_Text_SilphsLatestProduct, MSGBOX_SIGN
	end

SaffronCity_EventScript_TrainerFanClubSign::
	msgbox SaffronCity_Text_TrainerFanClubSign, MSGBOX_SIGN
	end

@ Topaze, fin 2 « Le Refuge » : poste 8/16 (HUGO) — duel contre 2 chasseurs, recompense : Snorlax
SaffronCity_EventScript_Refuge::
	lock
	faceplayer
	goto_if_ne VAR_TOPAZE_ENDING, 2, SaffronCity_EventScript_RefugeIdle
	goto_if_gt VAR_REFUGE_STAGE, 7, SaffronCity_EventScript_RefugeDone
	goto_if_lt VAR_REFUGE_STAGE, 7, SaffronCity_EventScript_RefugeEarly
	msgbox SaffronCity_Text_RefAsk
	setvar VAR_TOPAZE_BOOST, 18
	trainerbattle_no_intro TRAINER_GENTLEMAN_NORTON, SaffronCity_Text_RefHunter1
	setvar VAR_TOPAZE_BOOST, 36
	trainerbattle_no_intro TRAINER_JUGGLER_SHAWN, SaffronCity_Text_RefHunter2
	setvar VAR_TOPAZE_BOOST, 0
	special HealPlayerParty
	goto SaffronCity_EventScript_RefugeReward
	end

SaffronCity_EventScript_RefugeReward::
	msgbox SaffronCity_Text_RefGives
	givemon SPECIES_SNORLAX, 0
	addvar VAR_REFUGE_STAGE, 1
	msgbox SaffronCity_Text_RefAfter
	release
	end

SaffronCity_EventScript_RefugeEarly::
	msgbox SaffronCity_Text_RefEarly
	release
	end

SaffronCity_EventScript_RefugeDone::
	msgbox SaffronCity_Text_RefDone
	release
	end

SaffronCity_EventScript_RefugeIdle::
	msgbox SaffronCity_Text_RefIdle
	release
	end

@ Topaze: PROCHE VIOLETTE (optionnel, fort)
SaffronCity_EventScript_ProcheViolette::
	lock
	faceplayer
	goto_if_unset FLAG_TOPAZE_POSTGAME, SaffronCity_EventScript_ProcheViolette_TooEarly
	goto_if_defeated TRAINER_PROCHE_VIOLETTE, SaffronCity_EventScript_ProcheViolette_After
	msgbox SaffronCity_Text_ProcheViolette_Intro
	checkitemspace ITEM_TWISTED_SPOON
	goto_if_eq VAR_RESULT, FALSE, SaffronCity_EventScript_ProcheViolette_NoRoom
	trainerbattle_no_intro TRAINER_PROCHE_VIOLETTE, SaffronCity_Text_ProcheViolette_Defeat
	msgbox SaffronCity_Text_ProcheViolette_Win
	giveitem ITEM_TWISTED_SPOON
	msgbox SaffronCity_Text_ProcheViolette_After
	release
	end

SaffronCity_EventScript_ProcheViolette_After::
	msgbox SaffronCity_Text_ProcheViolette_After
	release
	end

SaffronCity_EventScript_ProcheViolette_TooEarly::
	msgbox SaffronCity_Text_ProcheViolette_Early
	release
	end

SaffronCity_EventScript_ProcheViolette_NoRoom::
	msgbox SaffronCity_Text_ProcheViolette_NoRoom
	release
	end

@ Topaze: HORLOGE DE SAFRANIA (quete des 3 indices : R1, R11, R22)
SaffronCity_EventScript_ClockKeeper::
	lock
	faceplayer
	goto_if_set FLAG_TOPAZE_CLOCK_DONE, SaffronCity_EventScript_ClockKeeper_Done
	goto_if_unset FLAG_TOPAZE_CLOCK_1, SaffronCity_EventScript_ClockKeeper_Ask
	goto_if_unset FLAG_TOPAZE_CLOCK_2, SaffronCity_EventScript_ClockKeeper_Ask
	goto_if_unset FLAG_TOPAZE_CLOCK_3, SaffronCity_EventScript_ClockKeeper_Ask
	checkitemspace ITEM_EXP_SHARE, 1
	goto_if_eq VAR_RESULT, FALSE, SaffronCity_EventScript_ClockKeeper_NoRoom
	setflag FLAG_TOPAZE_CLOCK_DONE
	msgbox SaffronCity_Text_Clock_Solved
	giveitem ITEM_EXP_SHARE, 1
	release
	end

SaffronCity_EventScript_ClockKeeper_Ask::
	msgbox SaffronCity_Text_Clock_Ask
	release
	end

SaffronCity_EventScript_ClockKeeper_Done::
	msgbox SaffronCity_Text_Clock_Done
	release
	end

SaffronCity_EventScript_ClockKeeper_NoRoom::
	msgbox SaffronCity_Text_Clock_NoRoom
	release
	end

@ Topaze: MARCHE NOCTURNE (post-game)
SaffronCity_EventScript_NightMarket::
	lock
	faceplayer
	goto_if_unset FLAG_TOPAZE_POSTGAME, SaffronCity_EventScript_NightMarket_Closed
	msgbox SaffronCity_Text_Market_Open
	pokemart SaffronCity_NightMarketItems
	msgbox SaffronCity_Text_Market_Bye
	release
	end

SaffronCity_EventScript_NightMarket_Closed::
	msgbox SaffronCity_Text_Market_Closed
	release
	end

	.align 2
SaffronCity_NightMarketItems::
	.2byte ITEM_RARE_CANDY
	.2byte ITEM_PP_MAX
	.2byte ITEM_MAX_REVIVE
	.2byte ITEM_FULL_RESTORE
	.2byte ITEM_LUCKY_EGG
	.2byte ITEM_NONE
