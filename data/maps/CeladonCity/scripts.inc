CeladonCity_MapScripts::
	map_script MAP_SCRIPT_ON_TRANSITION, CeladonCity_OnTransition
	map_script MAP_SCRIPT_ON_RESUME, CeladonCity_OnResume
	.byte 0

CeladonCity_OnResume::
	call_if_set FLAG_SYS_SPECIAL_WILD_BATTLE, CeladonCity_EventScript_TryRemoveArticuno
	end

CeladonCity_EventScript_TryRemoveArticuno::
	specialvar VAR_RESULT, GetBattleOutcome
	goto_if_ne VAR_RESULT, B_OUTCOME_CAUGHT, EventScript_Return
	removeobject VAR_LAST_TALKED
	return

@ Topaze: ARTICUNO sleeps in the quartz-geode clearing (behind the cuttable tree) once the League is beaten
CeladonCity_EventScript_ShowArticuno::
	goto_if_unset FLAG_TOPAZE_POSTGAME, EventScript_Return
	clearflag FLAG_HIDE_ARTICUNO
	return

CeladonCity_EventScript_Articuno::
	goto_if_questlog EventScript_ReleaseEnd
	special QuestLog_CutRecording
	lock
	faceplayer
	setwildbattle SPECIES_ARTICUNO, 55
	waitse
	playmoncry SPECIES_ARTICUNO, CRY_MODE_ENCOUNTER
	message Text_Gyaoo
	waitmessage
	waitmoncry
	delay 10
	playbgm MUS_ENCOUNTER_GYM_LEADER, 0
	waitbuttonpress
	setflag FLAG_SYS_SPECIAL_WILD_BATTLE
	special StartLegendaryBattle
	waitstate
	clearflag FLAG_SYS_SPECIAL_WILD_BATTLE
	specialvar VAR_RESULT, GetBattleOutcome
	goto_if_eq VAR_RESULT, B_OUTCOME_WON, CeladonCity_EventScript_DefeatedArticuno
	goto_if_eq VAR_RESULT, B_OUTCOME_RAN, CeladonCity_EventScript_RanFromArticuno
	goto_if_eq VAR_RESULT, B_OUTCOME_PLAYER_TELEPORTED, CeladonCity_EventScript_RanFromArticuno
	setflag FLAG_FOUGHT_ARTICUNO
	release
	end

CeladonCity_EventScript_DefeatedArticuno::
	setflag FLAG_FOUGHT_ARTICUNO
	goto EventScript_RemoveStaticMon
	end

CeladonCity_EventScript_RanFromArticuno::
	setvar VAR_0x8004, SPECIES_ARTICUNO
	goto EventScript_MonFlewAway
	end

CeladonCity_OnTransition::
	setworldmapflag FLAG_WORLD_MAP_CELADON_CITY
	call_if_unset FLAG_FOUGHT_ARTICUNO, CeladonCity_EventScript_ShowArticuno
	goto_if_set FLAG_HIDE_CELADON_ROCKETS, CeladonCity_EventScript_WestPoliceLeave
	end

CeladonCity_EventScript_WestPoliceLeave::
	setflag FLAG_TEMP_11
	end

CeladonCity_EventScript_WestPolice::
	lock
	faceplayer
	msgbox CeladonCity_Text_WestBlocked
	release
	end

CeladonCity_EventScript_LittleGirl::
	msgbox CeladonCity_Text_GotMyKoffingInCinnabar, MSGBOX_NPC
	end

CeladonCity_EventScript_OldMan1::
	lock
	msgbox CeladonCity_Text_GymIsGreatFullOfWomen
	release
	end

CeladonCity_EventScript_Woman::
	lock
	faceplayer
	goto_if_set FLAG_TOPAZE_POSTGAME, CeladonCity_EventScript_WomanPostgame
	msgbox CeladonCity_Text_GameCornerIsBadForCitysImage
	release
	end

CeladonCity_EventScript_WomanPostgame::
	msgbox CeladonCity_Text_WhySnowHere
	release
	end

CeladonCity_EventScript_OldMan2::
	msgbox CeladonCity_Text_BlewItAllAtSlots, MSGBOX_NPC
	end

CeladonCity_EventScript_SoftboiledTutor::
	goto EventScript_SoftboiledTutor
	end

CeladonCity_EventScript_FatMan::
	lock
	faceplayer
	msgbox CeladonCity_Text_MyTrustedPalPoliwrath
	closemessage
	applymovement LOCALID_CELADON_FAT_MAN, Common_Movement_FaceOriginalDirection
	waitmovement 0
	release
	end

CeladonCity_EventScript_Poliwrath::
	lock
	faceplayer
	waitse
	playmoncry SPECIES_POLIWRATH, CRY_MODE_NORMAL
	msgbox CeladonCity_Text_Poliwrath
	closemessage
	waitmoncry
	applymovement LOCALID_CELADON_POLIWRATH, Common_Movement_FaceOriginalDirection
	waitmovement 0
	release
	end

CeladonCity_EventScript_RocketGrunt1::
	msgbox CeladonCity_Text_KeepOutOfTeamRocketsWay, MSGBOX_NPC
	end

CeladonCity_EventScript_RocketGrunt2::
	msgbox CeladonCity_Text_GetLostOrIllPunchYou, MSGBOX_NPC
	end

CeladonCity_EventScript_Boy::
	lock
	faceplayer
	goto_if_set FLAG_TOPAZE_POSTGAME, CeladonCity_EventScript_BoyPostgame
	msgbox CeladonCity_Text_ScaldedTongueOnTea
	release
	end

CeladonCity_EventScript_BoyPostgame::
	msgbox CeladonCity_Text_GeodeClearing
	release
	end

CeladonCity_EventScript_SilphCoScientist::
	msgbox CeladonCity_Text_SomeoneStoleSilphScope, MSGBOX_NPC
	end

CeladonCity_EventScript_TrainerTips1::
	msgbox CeladonCity_Text_ExplainXAccuracyDireHit, MSGBOX_SIGN
	end

CeladonCity_EventScript_CitySign::
	msgbox CeladonCity_Text_CitySign, MSGBOX_SIGN
	end

CeladonCity_EventScript_GymSign::
	lockall
	famechecker FAMECHECKER_ERIKA, 0
	msgbox CeladonCity_Text_GymSign
	releaseall
	end

CeladonCity_EventScript_MansionSign::
	msgbox CeladonCity_Text_MansionSign, MSGBOX_SIGN
	end

CeladonCity_EventScript_DeptStoreSign::
	msgbox CeladonCity_Text_DeptStoreSign, MSGBOX_SIGN
	end

CeladonCity_EventScript_TrainerTips2::
	msgbox CeladonCity_Text_GuardSpecProtectsFromStatus, MSGBOX_SIGN
	end

CeladonCity_EventScript_PrizeExchangeSign::
	msgbox CeladonCity_Text_PrizeExchangeSign, MSGBOX_SIGN
	end

CeladonCity_EventScript_GameCornerSign::
	msgbox CeladonCity_Text_GameCornerSign, MSGBOX_SIGN
	end
