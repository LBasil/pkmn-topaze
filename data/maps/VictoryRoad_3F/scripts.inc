VictoryRoad_3F_MapScripts::
	map_script MAP_SCRIPT_ON_LOAD, VictoryRoad_3F_OnLoad
	.byte 0

VictoryRoad_3F_OnLoad::
	@ Topaze: les rochers sont déjà tombés sur les interrupteurs (passage ouvert)
	end

VictoryRoad_3F_EventScript_SetRockBarrier::
	setmetatile 12, 12, METATILE_Cave_RockBarrier_Top, 1
	setmetatile 12, 13, METATILE_Cave_RockBarrier_Bottom, 1
	return

VictoryRoad_3F_EventScript_FloorSwitch::
	lockall
	goto_if_eq VAR_MAP_SCENE_VICTORY_ROAD_3F, 100, VictoryRoad_3F_EventScript_FloorSwitchAlreadyPressed
	setmetatile 12, 12, METATILE_Cave_Floor_Ledge_Top, 0
	setmetatile 12, 13, METATILE_Cave_Floor_Ledge_Bottom, 0
	playse SE_ICE_BREAK
	special DrawWholeMapView
	waitse
	copyobjectxytoperm LOCALID_VICTORY_ROAD_3F_BOULDER1
	copyobjectxytoperm LOCALID_VICTORY_ROAD_3F_BOULDER2
	setvar VAR_MAP_SCENE_VICTORY_ROAD_3F, 100
	releaseall
	end

VictoryRoad_3F_EventScript_FloorSwitchAlreadyPressed::
	releaseall
	end

VictoryRoad_3F_EventScript_George::
	trainerbattle_single TRAINER_COOLTRAINER_GEORGE, VictoryRoad_3F_Text_GeorgeIntro, VictoryRoad_3F_Text_GeorgeDefeat
	msgbox VictoryRoad_3F_Text_GeorgePostBattle, MSGBOX_AUTOCLOSE
	end

VictoryRoad_3F_EventScript_Colby::
	trainerbattle_single TRAINER_COOLTRAINER_COLBY, VictoryRoad_3F_Text_ColbyIntro, VictoryRoad_3F_Text_ColbyDefeat
	msgbox VictoryRoad_3F_Text_ColbyPostBattle, MSGBOX_AUTOCLOSE
	end

VictoryRoad_3F_EventScript_Caroline::
	trainerbattle_single TRAINER_COOLTRAINER_CAROLINE, VictoryRoad_3F_Text_CarolineIntro, VictoryRoad_3F_Text_CarolineDefeat
	msgbox VictoryRoad_3F_Text_CarolinePostBattle, MSGBOX_AUTOCLOSE
	end

VictoryRoad_3F_EventScript_Alexa::
	trainerbattle_single TRAINER_COOLTRAINER_ALEXA, VictoryRoad_3F_Text_AlexaIntro, VictoryRoad_3F_Text_AlexaDefeat
	msgbox VictoryRoad_3F_Text_AlexaPostBattle, MSGBOX_AUTOCLOSE
	end

VictoryRoad_3F_EventScript_Ray::
	trainerbattle_double TRAINER_COOL_COUPLE_RAY_TYRA, VictoryRoad_3F_Text_RayIntro, VictoryRoad_3F_Text_RayDefeat, VictoryRoad_3F_Text_RayNotEnoughMons
	msgbox VictoryRoad_3F_Text_RayPostBattle, MSGBOX_AUTOCLOSE
	end

VictoryRoad_3F_EventScript_Tyra::
	trainerbattle_double TRAINER_COOL_COUPLE_RAY_TYRA, VictoryRoad_3F_Text_TyraIntro, VictoryRoad_3F_Text_TyraDefeat, VictoryRoad_3F_Text_TyraNotEnoughMons
	msgbox VictoryRoad_3F_Text_TyraPostBattle, MSGBOX_AUTOCLOSE
	end

@ Topaze: objets caches (panneaux a script, drapeaux hors plage moteur)
VictoryRoad_3F_EventScript_TopazeFind0::
	lock
	goto_if_set FLAG_TOPAZE_HID_VICTORYROAD_3F_0, VictoryRoad_3F_EventScript_TopazeFind0_Done
	checkitemspace ITEM_RARE_CANDY, 1
	goto_if_eq VAR_RESULT, FALSE, VictoryRoad_3F_EventScript_TopazeFind0_Full
	giveitem ITEM_RARE_CANDY, 1
	setflag FLAG_TOPAZE_HID_VICTORYROAD_3F_0
	release
	end

VictoryRoad_3F_EventScript_TopazeFind0_Done::
	release
	end

VictoryRoad_3F_EventScript_TopazeFind0_Full::
	msgbox VictoryRoad_3F_Text_TopazeFindFull
	release
	end

VictoryRoad_3F_EventScript_TopazeFind1::
	lock
	goto_if_set FLAG_TOPAZE_HID_VICTORYROAD_3F_1, VictoryRoad_3F_EventScript_TopazeFind1_Done
	checkitemspace ITEM_PP_UP, 1
	goto_if_eq VAR_RESULT, FALSE, VictoryRoad_3F_EventScript_TopazeFind1_Full
	giveitem ITEM_PP_UP, 1
	setflag FLAG_TOPAZE_HID_VICTORYROAD_3F_1
	release
	end

VictoryRoad_3F_EventScript_TopazeFind1_Done::
	release
	end

VictoryRoad_3F_EventScript_TopazeFind1_Full::
	msgbox VictoryRoad_3F_Text_TopazeFindFull
	release
	end


VictoryRoad_3F_Text_TopazeFindFull::
	.string "Something shines here, but your BAG\n"
	.string "is full.$"
