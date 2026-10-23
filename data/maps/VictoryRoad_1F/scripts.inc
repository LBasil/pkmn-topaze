VictoryRoad_1F_MapScripts::
	map_script MAP_SCRIPT_ON_LOAD, VictoryRoad_1F_OnLoad
	map_script MAP_SCRIPT_ON_TRANSITION, VictoryRoad_1F_OnTransition
	.byte 0

VictoryRoad_1F_OnLoad::
	@ Topaze: les rochers sont déjà tombés sur les interrupteurs (passage ouvert)
	@ Topaze: éboulis ONYBRIS sur le couloir de l'échelle tant que le repaire n'est pas nettoyé
	goto_if_set FLAG_VR_BOSS_DONE, VictoryRoad_1F_OnLoad_Open
	setmetatile 4, 8, METATILE_Cave_RockBarrier_Top, 1
	setmetatile 5, 8, METATILE_Cave_RockBarrier_Top, 1
	setmetatile 4, 9, METATILE_Cave_RockBarrier_Bottom, 1
	setmetatile 5, 9, METATILE_Cave_RockBarrier_Bottom, 1
VictoryRoad_1F_OnLoad_Open::
	end

VictoryRoad_1F_EventScript_Rubble::
	lockall
	setvar VAR_TEMP_0, 1
	goto_if_set FLAG_VR_BOSS_DONE, VictoryRoad_1F_EventScript_RubbleEnd
	msgbox VictoryRoad_1F_Text_Rubble
VictoryRoad_1F_EventScript_RubbleEnd::
	releaseall
	end

@ Topaze: l'infirmiere de la route, a cote de l'echelle du repaire
VictoryRoad_1F_EventScript_Nurse::
	lock
	faceplayer
	msgbox VictoryRoad_1F_Text_NurseHeal
	fadescreen FADE_TO_BLACK
	playfanfare MUS_HEAL
	waitfanfare
	special HealPlayerParty
	fadescreen FADE_FROM_BLACK
	msgbox VictoryRoad_1F_Text_NurseHealed
	release
	end

VictoryRoad_1F_EventScript_SetRockBarrier::
	setmetatile 12, 14, METATILE_Cave_RockBarrier_Top, 1
	setmetatile 12, 15, METATILE_Cave_RockBarrier_Bottom, 1
	return

VictoryRoad_1F_OnTransition::
	setworldmapflag FLAG_WORLD_MAP_VICTORY_ROAD_1F
	end

VictoryRoad_1F_EventScript_FloorSwitch::
	lockall
	goto_if_eq VAR_MAP_SCENE_VICTORY_ROAD_1F, 100, VictoryRoad_1F_EventScript_FloorSwitchAlreadyPressed
	setmetatile 12, 14, METATILE_Cave_Floor_Ledge_Top, 0
	setmetatile 12, 15, METATILE_Cave_Floor_Ledge_Bottom, 0
	playse SE_ICE_BREAK
	special DrawWholeMapView
	waitse
	copyobjectxytoperm LOCALID_VICTORY_ROAD_1F_BOULDER
	setvar VAR_MAP_SCENE_VICTORY_ROAD_1F, 100
	releaseall
	end

VictoryRoad_1F_EventScript_FloorSwitchAlreadyPressed::
	releaseall
	end

VictoryRoad_1F_EventScript_Naomi::
	trainerbattle_single TRAINER_COOLTRAINER_NAOMI, VictoryRoad_1F_Text_NaomiIntro, VictoryRoad_1F_Text_NaomiDefeat
	msgbox VictoryRoad_1F_Text_NaomiPostBattle, MSGBOX_AUTOCLOSE
	end

VictoryRoad_1F_EventScript_Rolando::
	trainerbattle_single TRAINER_COOLTRAINER_ROLANDO, VictoryRoad_1F_Text_RolandoIntro, VictoryRoad_1F_Text_RolandoDefeat
	msgbox VictoryRoad_1F_Text_RolandoPostBattle, MSGBOX_AUTOCLOSE
	end
