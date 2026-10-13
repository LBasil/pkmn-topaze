VictoryRoad_2F_MapScripts::
	map_script MAP_SCRIPT_ON_LOAD, VictoryRoad_2F_OnLoad
	map_script MAP_SCRIPT_ON_TRANSITION, VictoryRoad_2F_OnTransition
	.byte 0

VictoryRoad_2F_OnLoad::
	call_if_ne VAR_MAP_SCENE_VICTORY_ROAD_2F_BOULDER1, 100, VictoryRoad_2F_EventScript_SetRockBarrier1
	call_if_ne VAR_MAP_SCENE_VICTORY_ROAD_2F_BOULDER2, 100, VictoryRoad_2F_EventScript_SetRockBarrier2
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
	goto_if_set FLAG_VR_BOSS_DONE, VictoryRoad_2F_EventScript_FinalDone
	goto_if_unset FLAG_VR_RED_MET, VictoryRoad_2F_EventScript_NoRed
	end

VictoryRoad_2F_EventScript_FinalDone::
	setvar VAR_TEMP_6, 1
	setflag FLAG_TEMP_1
	end

VictoryRoad_2F_EventScript_NoRed::
	setvar VAR_TEMP_6, 1
	setflag FLAG_TEMP_1
	setflag FLAG_TEMP_2
	end

VictoryRoad_2F_EventScript_Stub::
	end

VictoryRoad_2F_EventScript_RedTalk::
	lock
	faceplayer
	goto_if_set FLAG_VR_BOSS_DONE, VictoryRoad_2F_EventScript_RedHeal
	msgbox VictoryRoad_2F_Text_RedSilent
	release
	end

VictoryRoad_2F_EventScript_RedHeal::
	msgbox VictoryRoad_2F_Text_RedHeals
	special HealPlayerParty
	playfanfare MUS_HEAL
	waitfanfare
	msgbox VictoryRoad_2F_Text_RedSilent
	release
	end

VictoryRoad_2F_EventScript_FinalScene::
	lockall
	msgbox VictoryRoad_2F_Text_ShapeA
	closemessage
	setvar VAR_0x8004, 1
	setvar VAR_0x8005, 3
	setvar VAR_0x8006, 8
	setvar VAR_0x8007, 4
	playse SE_THUNDER
	special ShakeScreen
	waitstate
	msgbox VictoryRoad_2F_Text_ShapeB
	closemessage
	fadescreen FADE_TO_BLACK
	delay 40
	fadescreen FADE_FROM_BLACK
	msgbox VictoryRoad_2F_Text_VesperIntro
	closemessage
	setvar VAR_LAST_TALKED, LOCALID_VR_VESPER
	trainerbattle_no_intro TRAINER_MAGMA_ADMIN_TABITHA, VictoryRoad_2F_Text_VesperDefeat
	msgbox VictoryRoad_2F_Text_VesperPost
	closemessage
	fadescreen FADE_TO_BLACK
	removeobject LOCALID_VR_VESPER
	delay 20
	fadescreen FADE_FROM_BLACK
	msgbox VictoryRoad_2F_Text_RedAfter
	closemessage
	setflag FLAG_VR_BOSS_DONE
	setvar VAR_TEMP_6, 1
	releaseall
	end
