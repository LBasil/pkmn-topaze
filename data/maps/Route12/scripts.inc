Route12_MapScripts::
	map_script MAP_SCRIPT_ON_TRANSITION, Route12_OnTransition
	map_script MAP_SCRIPT_ON_RESUME, Route12_OnResume
	.byte 0

Route12_OnTransition::
	setflag FLAG_TEMP_5
	end

Route12_EventScript_PierKronosTalk::
	end

Route12_EventScript_PierKronosScene::
	lockall
	goto_if_unset FLAG_AMETHYST_STONE_GIVEN, Route12_EventScript_PierKronosSkip
	goto_if_set FLAG_PIER_KRONOS_DONE, Route12_EventScript_PierKronosSkip
	clearflag FLAG_TEMP_5
	addobject LOCALID_PIER_KRONOS
	playse SE_PIN
	applymovement LOCALID_PLAYER, Common_Movement_WalkInPlaceFasterUp
	waitmovement 0
	goto_if_set FLAG_PIER_LORE_DONE, Route12_EventScript_PierKronosKnows
	msgbox Route12_Text_PierKronos1b
	goto Route12_EventScript_PierKronosNext
Route12_EventScript_PierKronosKnows::
	msgbox Route12_Text_PierKronos1
Route12_EventScript_PierKronosNext::
	closemessage
	msgbox Route12_Text_PierKronos2
	closemessage
	applymovement LOCALID_PIER_KRONOS, Route12_Movement_KronosLeaves
	waitmovement 0
	removeobject LOCALID_PIER_KRONOS
	setflag FLAG_PIER_KRONOS_DONE
	releaseall
	end

Route12_EventScript_PierKronosSkip::
	releaseall
	end

Route12_Movement_KronosLeaves::
	walk_up
	walk_up
	walk_up
	walk_up
	walk_up
	step_end

Route12_OnResume::
	call_if_set FLAG_SYS_SPECIAL_WILD_BATTLE, Route12_EventScript_TryRemoveSnorlax
	end

Route12_EventScript_TryRemoveSnorlax::
	removeobject VAR_LAST_TALKED
	return

Route12_EventScript_Snorlax::
	lock
	faceplayer
	goto_if_unset FLAG_GOT_POKE_FLUTE, Route12_EventScript_SnorlaxNoPokeFlute
	goto_if_questlog EventScript_ReleaseEnd
	special QuestLog_CutRecording
	msgbox Text_WantToUsePokeFlute, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, Route12_EventScript_DontUsePokeFlute
	call EventScript_AwakenSnorlax
	setwildbattle SPECIES_SNORLAX, 38
	waitse
	playmoncry SPECIES_SNORLAX, CRY_MODE_ENCOUNTER
	delay 40
	waitmoncry
	setflag FLAG_HIDE_ROUTE_12_SNORLAX
	setflag FLAG_SYS_SPECIAL_WILD_BATTLE
	setflag FLAG_WOKE_UP_ROUTE_12_SNORLAX
	dowildbattle
	clearflag FLAG_SYS_SPECIAL_WILD_BATTLE
	specialvar VAR_RESULT, GetBattleOutcome
	goto_if_eq VAR_RESULT, B_OUTCOME_WON, Route12_EventScript_FoughtSnorlax
	goto_if_eq VAR_RESULT, B_OUTCOME_RAN, Route12_EventScript_FoughtSnorlax
	goto_if_eq VAR_RESULT, B_OUTCOME_PLAYER_TELEPORTED, Route12_EventScript_FoughtSnorlax
	release
	end

Route12_EventScript_DontUsePokeFlute::
	release
	end

Route12_EventScript_FoughtSnorlax::
	msgbox Text_SnorlaxReturnedToMountains
	release
	end

Route12_EventScript_SnorlaxNoPokeFlute::
	msgbox Route12_Text_MonSprawledOutInSlumber
	release
	end

Route12_EventScript_RouteSign::
	msgbox Route12_Text_RouteSign, MSGBOX_SIGN
	end

Route12_EventScript_FishingSign::
	msgbox Route12_Text_SportfishingArea, MSGBOX_SIGN
	end

@ Topaze: PROCHE EMMA (optionnel, fort)
Route12_EventScript_ProcheEmma::
	lock
	faceplayer
	goto_if_unset FLAG_TOPAZE_POSTGAME, Route12_EventScript_ProcheEmma_TooEarly
	goto_if_defeated TRAINER_PROCHE_EMMA, Route12_EventScript_ProcheEmma_After
	msgbox Route12_Text_ProcheEmma_Intro
	checkitemspace ITEM_MIRACLE_SEED
	goto_if_eq VAR_RESULT, FALSE, Route12_EventScript_ProcheEmma_NoRoom
	trainerbattle_no_intro TRAINER_PROCHE_EMMA, Route12_Text_ProcheEmma_Defeat
	msgbox Route12_Text_ProcheEmma_Win
	giveitem ITEM_MIRACLE_SEED
	msgbox Route12_Text_ProcheEmma_After
	release
	end

Route12_EventScript_ProcheEmma_After::
	msgbox Route12_Text_ProcheEmma_After
	release
	end

Route12_EventScript_ProcheEmma_TooEarly::
	msgbox Route12_Text_ProcheEmma_Early
	release
	end

Route12_EventScript_ProcheEmma_NoRoom::
	msgbox Route12_Text_ProcheEmma_NoRoom
	release
	end
