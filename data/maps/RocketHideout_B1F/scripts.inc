RocketHideout_B1F_MapScripts::
	map_script MAP_SCRIPT_ON_LOAD, RocketHideout_B1F_OnLoad
	map_script MAP_SCRIPT_ON_TRANSITION, RocketHideout_B1F_OnTransition
	.byte 0

RocketHideout_B1F_OnLoad::
	call_if_not_defeated TRAINER_TEAM_ROCKET_GRUNT_12 RocketHideout_B1F_EventScript_SetBarrier
	end

RocketHideout_B1F_OnTransition::
	setworldmapflag FLAG_WORLD_MAP_ROCKET_HIDEOUT_B1F
	end

RocketHideout_B1F_EventScript_Grunt1::
	trainerbattle_single TRAINER_TEAM_ROCKET_GRUNT_8, RocketHideout_B1F_Text_Grunt1Intro, RocketHideout_B1F_Text_Grunt1Defeat
	msgbox RocketHideout_B1F_Text_Grunt1PostBattle, MSGBOX_AUTOCLOSE
	end

RocketHideout_B1F_EventScript_Grunt2::
	trainerbattle_single TRAINER_TEAM_ROCKET_GRUNT_9, RocketHideout_B1F_Text_Grunt2Intro, RocketHideout_B1F_Text_Grunt2Defeat
	msgbox RocketHideout_B1F_Text_Grunt2PostBattle, MSGBOX_AUTOCLOSE
	end

RocketHideout_B1F_EventScript_Grunt3::
	trainerbattle_single TRAINER_TEAM_ROCKET_GRUNT_10, RocketHideout_B1F_Text_Grunt3Intro, RocketHideout_B1F_Text_Grunt3Defeat
	msgbox RocketHideout_B1F_Text_Grunt3PostBattle, MSGBOX_AUTOCLOSE
	end

RocketHideout_B1F_EventScript_Grunt4::
	trainerbattle_single TRAINER_TEAM_ROCKET_GRUNT_11, RocketHideout_B1F_Text_Grunt4Intro, RocketHideout_B1F_Text_Grunt4Defeat
	msgbox RocketHideout_B1F_Text_Grunt4PostBattle, MSGBOX_AUTOCLOSE
	end

RocketHideout_B1F_EventScript_Grunt5::
	trainerbattle_single TRAINER_TEAM_ROCKET_GRUNT_12, RocketHideout_B1F_Text_Grunt5Intro, RocketHideout_B1F_Text_Grunt5Defeat, RocketHideout_B1F_EventScript_DefeatedGrunt5
	msgbox RocketHideout_B1F_Text_Grunt5PostBattle, MSGBOX_AUTOCLOSE
	end

RocketHideout_B1F_EventScript_DefeatedGrunt5::
	call RocketHideout_B1F_EventScript_RemoveBarrier
	playse SE_UNLOCK
	special DrawWholeMapView
	waitse
	release
	end

RocketHideout_B1F_EventScript_SetBarrier::
	setmetatile 4, 14, METATILE_SilphCo_HideoutBarrier_TopLeft_Floor, 1
	setmetatile 5, 14, METATILE_SilphCo_HideoutBarrier_TopRight_Floor, 1
	setmetatile 4, 15, METATILE_SilphCo_HideoutBarrier_BottomLeft, 1
	setmetatile 5, 15, METATILE_SilphCo_HideoutBarrier_BottomRight, 1
	setmetatile 4, 16, METATILE_SilphCo_HideoutFloor_ShadeFull, 0
	setmetatile 5, 16, METATILE_SilphCo_HideoutFloor_ShadeFull, 0
	return

RocketHideout_B1F_EventScript_RemoveBarrier::
	setmetatile 4, 14, METATILE_SilphCo_HideoutFloor_ShadeFull, 0
	setmetatile 5, 14, METATILE_SilphCo_HideoutFloor, 0
	setmetatile 4, 15, METATILE_SilphCo_HideoutFloor_ShadeFull, 0
	setmetatile 5, 15, METATILE_SilphCo_HideoutFloor, 0
	setmetatile 4, 16, METATILE_SilphCo_HideoutFloor_ShadeFull, 0
	setmetatile 5, 16, METATILE_SilphCo_HideoutFloor, 0
	return

@ Topaze: scene d'entree du repaire de Bourg Quartz (premiere fois)
RocketHideout_B1F_EventScript_Entry::
	lockall
	setvar VAR_TEMP_0, 1
	goto_if_set FLAG_TOPAZE_VAULT_ENTERED, RocketHideout_B1F_EventScript_EntryEnd
	setflag FLAG_TOPAZE_VAULT_ENTERED
	msgbox RocketHideout_B1F_Text_Entry1
	msgbox RocketHideout_B1F_Text_Entry2
RocketHideout_B1F_EventScript_EntryEnd::
	releaseall
	end
