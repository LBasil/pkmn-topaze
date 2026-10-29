VictoryRoad_2F_MapScripts::
	map_script MAP_SCRIPT_ON_LOAD, VictoryRoad_2F_OnLoad
	map_script MAP_SCRIPT_ON_TRANSITION, VictoryRoad_2F_OnTransition
	.byte 0

VictoryRoad_2F_OnLoad::
	@ Topaze: les rochers sont déjà tombés sur les interrupteurs (passage ouvert)
	@ Topaze: les rochers sont déjà tombés sur les interrupteurs (passage ouvert)
	end

VictoryRoad_2F_EventScript_SetRockBarrier1::
	setmetatile 13, 10, METATILE_Cave_RockBarrier_Top, 1
	setmetatile 13, 11, METATILE_Cave_RockBarrier_Bottom, 1
	return

VictoryRoad_2F_EventScript_SetRockBarrier2::
	setmetatile 33, 16, METATILE_Cave_RockBarrier_Top, 1
	setmetatile 33, 17, METATILE_Cave_RockBarrier_Bottom, 1
	return

VictoryRoad_2F_EventScript_FloorSwitch1::
	lockall
	goto_if_eq VAR_MAP_SCENE_VICTORY_ROAD_2F_BOULDER1, 100, VictoryRoad_2F_EventScript_FloorSwitch1AlreadyPressed
	setmetatile 13, 10, METATILE_Cave_Floor_Ledge_Top, 0
	setmetatile 13, 11, METATILE_Cave_Floor_Ledge_Bottom, 0
	playse SE_ICE_BREAK
	special DrawWholeMapView
	waitse
	copyobjectxytoperm LOCALID_VICTORY_ROAD_2F_BOULDER1
	setvar VAR_MAP_SCENE_VICTORY_ROAD_2F_BOULDER1, 100
	releaseall
	end

VictoryRoad_2F_EventScript_FloorSwitch1AlreadyPressed::
	releaseall
	end

VictoryRoad_2F_EventScript_FloorSwitch2::
	lockall
	goto_if_eq VAR_MAP_SCENE_VICTORY_ROAD_2F_BOULDER2, 100, VictoryRoad_2F_EventScript_FloorSwitch2AlreadyPressed
	setmetatile 33, 16, METATILE_Cave_Floor_Ledge_Top, 0
	setmetatile 33, 17, METATILE_Cave_Floor_Ledge_Bottom, 0
	playse SE_ICE_BREAK
	special DrawWholeMapView
	waitse
	copyobjectxytoperm LOCALID_VICTORY_ROAD_2F_BOULDER2
	setvar VAR_MAP_SCENE_VICTORY_ROAD_2F_BOULDER2, 100
	releaseall
	end

VictoryRoad_2F_EventScript_FloorSwitch2AlreadyPressed::
	releaseall
	end

VictoryRoad_2F_EventScript_Dawson::
	trainerbattle_single TRAINER_POKEMANIAC_DAWSON, VictoryRoad_2F_Text_DawsonIntro, VictoryRoad_2F_Text_DawsonDefeat
	msgbox VictoryRoad_2F_Text_DawsonPostBattle, MSGBOX_AUTOCLOSE
	end

VictoryRoad_2F_EventScript_Daisuke::
	trainerbattle_single TRAINER_BLACK_BELT_DAISUKE, VictoryRoad_2F_Text_DaisukeIntro, VictoryRoad_2F_Text_DaisukeDefeat
	msgbox VictoryRoad_2F_Text_DaisukePostBattle, MSGBOX_AUTOCLOSE
	end

VictoryRoad_2F_EventScript_Nelson::
	trainerbattle_single TRAINER_JUGGLER_NELSON, VictoryRoad_2F_Text_NelsonIntro, VictoryRoad_2F_Text_NelsonDefeat
	msgbox VictoryRoad_2F_Text_NelsonPostBattle, MSGBOX_AUTOCLOSE
	end

VictoryRoad_2F_EventScript_Gregory::
	trainerbattle_single TRAINER_JUGGLER_GREGORY, VictoryRoad_2F_Text_GregoryIntro, VictoryRoad_2F_Text_GregoryDefeat
	msgbox VictoryRoad_2F_Text_GregoryPostBattle, MSGBOX_AUTOCLOSE
	end

VictoryRoad_2F_EventScript_Vincent::
	trainerbattle_single TRAINER_TAMER_VINCENT, VictoryRoad_2F_Text_VincentIntro, VictoryRoad_2F_Text_VincentDefeat
	msgbox VictoryRoad_2F_Text_VincentPostBattle, MSGBOX_AUTOCLOSE
	end

VictoryRoad_2F_OnTransition::
	goto_if_set FLAG_VR_BOSS_DONE, VictoryRoad_2F_EventScript_ExitOpen
	end

VictoryRoad_2F_EventScript_ExitOpen::
	setvar VAR_TEMP_6, 1
	end

VictoryRoad_2F_EventScript_ExitBlockedN::
	lockall
	msgbox VictoryRoad_2F_Text_ExitBlocked
	applymovement LOCALID_PLAYER, VictoryRoad_2F_Movement_PushUp
	waitmovement 0
	releaseall
	end

VictoryRoad_2F_EventScript_ExitBlockedS::
	lockall
	msgbox VictoryRoad_2F_Text_ExitBlocked
	applymovement LOCALID_PLAYER, VictoryRoad_2F_Movement_PushDown
	waitmovement 0
	releaseall
	end

VictoryRoad_2F_Movement_PushUp::
	walk_up
	step_end

VictoryRoad_2F_Movement_PushDown::
	walk_down
	step_end

@ Topaze: l'infirmiere de la route (deplacee de la 1F), pres de l'echelle cachee du repaire
VictoryRoad_2F_EventScript_Nurse::
	lock
	faceplayer
	msgbox VictoryRoad_2F_Text_NurseHeal
	fadescreen FADE_TO_BLACK
	playfanfare MUS_HEAL
	waitfanfare
	special HealPlayerParty
	fadescreen FADE_FROM_BLACK
	msgbox VictoryRoad_2F_Text_NurseHealed
	release
	end

@ Topaze: objets caches (panneaux a script, drapeaux hors plage moteur)
VictoryRoad_2F_EventScript_TopazeFind0::
	lock
	goto_if_set FLAG_TOPAZE_HID_VICTORYROAD_2F_0, VictoryRoad_2F_EventScript_TopazeFind0_Done
	checkitemspace ITEM_MAX_REVIVE, 1
	goto_if_eq VAR_RESULT, FALSE, VictoryRoad_2F_EventScript_TopazeFind0_Full
	giveitem ITEM_MAX_REVIVE, 1
	setflag FLAG_TOPAZE_HID_VICTORYROAD_2F_0
	release
	end

VictoryRoad_2F_EventScript_TopazeFind0_Done::
	release
	end

VictoryRoad_2F_EventScript_TopazeFind0_Full::
	msgbox VictoryRoad_2F_Text_TopazeFindFull
	release
	end

VictoryRoad_2F_EventScript_TopazeFind1::
	lock
	goto_if_set FLAG_TOPAZE_HID_VICTORYROAD_2F_1, VictoryRoad_2F_EventScript_TopazeFind1_Done
	checkitemspace ITEM_ELIXIR, 1
	goto_if_eq VAR_RESULT, FALSE, VictoryRoad_2F_EventScript_TopazeFind1_Full
	giveitem ITEM_ELIXIR, 1
	setflag FLAG_TOPAZE_HID_VICTORYROAD_2F_1
	release
	end

VictoryRoad_2F_EventScript_TopazeFind1_Done::
	release
	end

VictoryRoad_2F_EventScript_TopazeFind1_Full::
	msgbox VictoryRoad_2F_Text_TopazeFindFull
	release
	end


VictoryRoad_2F_Text_TopazeFindFull::
	.string "Something shines here, but your BAG\n"
	.string "is full.$"
