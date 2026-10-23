OneIsland_KindleRoad_MapScripts::
	map_script MAP_SCRIPT_ON_TRANSITION, OneIsland_KindleRoad_OnTransition
	.byte 0

OneIsland_KindleRoad_OnTransition::
	@ Topaze: etincelles visibles seulement a l'etape 1 ; Raikou apres les trois
	setflag FLAG_HIDE_ECHO1_SPARK1
	setflag FLAG_HIDE_ECHO1_SPARK2
	setflag FLAG_HIDE_ECHO1_SPARK3
	goto_if_set FLAG_ECHO_BEAST_DONE, OneIsland_KindleRoad_EventScript_HideBeast
	goto_if_ne VAR_ECHO_STAGE, 1, OneIsland_KindleRoad_EventScript_HideBeast
	goto_if_unset FLAG_ECHO1_SPARK_DONE1, OneIsland_KindleRoad_EventScript_ShowSpark1
	goto OneIsland_KindleRoad_EventScript_TransSpark2

OneIsland_KindleRoad_EventScript_ShowSpark1::
	clearflag FLAG_HIDE_ECHO1_SPARK1
	goto OneIsland_KindleRoad_EventScript_TransSpark2

OneIsland_KindleRoad_EventScript_TransSpark2::
	goto_if_unset FLAG_ECHO1_SPARK_DONE2, OneIsland_KindleRoad_EventScript_ShowSpark2
	goto OneIsland_KindleRoad_EventScript_TransSpark3

OneIsland_KindleRoad_EventScript_ShowSpark2::
	clearflag FLAG_HIDE_ECHO1_SPARK2
	goto OneIsland_KindleRoad_EventScript_TransSpark3

OneIsland_KindleRoad_EventScript_TransSpark3::
	goto_if_unset FLAG_ECHO1_SPARK_DONE3, OneIsland_KindleRoad_EventScript_ShowSpark3
	end

OneIsland_KindleRoad_EventScript_ShowSpark3::
	clearflag FLAG_HIDE_ECHO1_SPARK3
	setflag FLAG_HIDE_ECHO_BEAST
	end

OneIsland_KindleRoad_EventScript_HideBeast::
	setflag FLAG_HIDE_ECHO_BEAST
	end

OneIsland_KindleRoad_EventScript_RouteSign::
	msgbox OneIsland_KindleRoad_Text_RouteSign, MSGBOX_SIGN
	end

OneIsland_KindleRoad_EventScript_EmberSpaSign::
	msgbox OneIsland_KindleRoad_Text_EmberSpaSign, MSGBOX_SIGN
	end

@ Topaze: Echo 1 beast (static, stays if fled)
OneIsland_KindleRoad_EventScript_Raikou::
	goto_if_questlog EventScript_ReleaseEnd
	special QuestLog_CutRecording
	lock
	faceplayer
	setwildbattle SPECIES_RAIKOU, 0
	waitse
	playmoncry SPECIES_RAIKOU, CRY_MODE_ENCOUNTER
	delay 40
	waitmoncry
	setflag FLAG_SYS_SPECIAL_WILD_BATTLE
	special StartLegendaryBattle
	waitstate
	clearflag FLAG_SYS_SPECIAL_WILD_BATTLE
	specialvar VAR_RESULT, GetBattleOutcome
	goto_if_eq VAR_RESULT, B_OUTCOME_WON, OneIsland_KindleRoad_EventScript_DefeatedRaikou
	goto_if_eq VAR_RESULT, B_OUTCOME_RAN, OneIsland_KindleRoad_EventScript_RanFromRaikou
	goto_if_eq VAR_RESULT, B_OUTCOME_PLAYER_TELEPORTED, OneIsland_KindleRoad_EventScript_RanFromRaikou
	setflag FLAG_ECHO_BEAST_DONE
	setflag FLAG_HIDE_ECHO_BEAST
	setvar VAR_ECHO_STAGE, 2
	goto OneIsland_PokemonCenter_1F_EventScript_EchoPhone1
	end

OneIsland_KindleRoad_EventScript_DefeatedRaikou::
	setflag FLAG_ECHO_BEAST_DONE
	setvar VAR_ECHO_STAGE, 2
	fadescreen FADE_TO_BLACK
	removeobject VAR_LAST_TALKED
	fadescreen FADE_FROM_BLACK
	goto OneIsland_PokemonCenter_1F_EventScript_EchoPhone1
	end

OneIsland_KindleRoad_EventScript_RanFromRaikou::
	setvar VAR_0x8004, SPECIES_RAIKOU
	goto EventScript_MonFlewAway
	end

@ Topaze: Echo 1, trois etincelles menent a Raikou
OneIsland_KindleRoad_EventScript_EchoSpark1::
	lock
	faceplayer
	setvar VAR_0x8004, SPECIES_VOLTORB
	playmoncry SPECIES_VOLTORB, CRY_MODE_ENCOUNTER
	waitmoncry
	msgbox OneIsland_KindleRoad_Text_EchoSpark1
	setflag FLAG_ECHO1_SPARK_DONE1
	setflag FLAG_HIDE_ECHO1_SPARK1
	fadescreen FADE_TO_BLACK
	removeobject VAR_LAST_TALKED
	fadescreen FADE_FROM_BLACK
	release
	end

OneIsland_KindleRoad_EventScript_EchoSpark2::
	lock
	faceplayer
	playmoncry SPECIES_VOLTORB, CRY_MODE_ENCOUNTER
	waitmoncry
	msgbox OneIsland_KindleRoad_Text_EchoSpark2
	setflag FLAG_ECHO1_SPARK_DONE2
	setflag FLAG_HIDE_ECHO1_SPARK2
	fadescreen FADE_TO_BLACK
	removeobject VAR_LAST_TALKED
	fadescreen FADE_FROM_BLACK
	release
	end

OneIsland_KindleRoad_EventScript_EchoSpark3::
	lock
	faceplayer
	playmoncry SPECIES_VOLTORB, CRY_MODE_ENCOUNTER
	waitmoncry
	msgbox OneIsland_KindleRoad_Text_EchoSpark3
	setflag FLAG_ECHO1_SPARK_DONE3
	setflag FLAG_HIDE_ECHO1_SPARK3
	fadescreen FADE_TO_BLACK
	removeobject VAR_LAST_TALKED
	fadescreen FADE_FROM_BLACK
	playse SE_THUNDER
	delay 30
	playse SE_THUNDER2
	msgbox OneIsland_KindleRoad_Text_EchoSpark3b
	release
	end

@ Topaze: la bouche de grotte du repaire (6,124) reste fermee tant que Bill et les etincelles n'ont pas parle
OneIsland_KindleRoad_EventScript_DenLockedBill::
	lockall
	msgbox OneIsland_KindleRoad_Text_DenLockedBill
	applymovement LOCALID_PLAYER, OneIsland_KindleRoad_Movement_DenBack
	waitmovement 0
	releaseall
	end

OneIsland_KindleRoad_EventScript_DenLockedSparks::
	goto_if_set FLAG_ECHO1_SPARK_DONE3, EventScript_Return
	lockall
	msgbox OneIsland_KindleRoad_Text_DenLockedSparks
	applymovement LOCALID_PLAYER, OneIsland_KindleRoad_Movement_DenBack
	waitmovement 0
	releaseall
	end

OneIsland_KindleRoad_Movement_DenBack::
	walk_down
	step_end
