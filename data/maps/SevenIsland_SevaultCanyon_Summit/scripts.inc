SevenIsland_SevaultCanyon_Summit_MapScripts::
	map_script MAP_SCRIPT_ON_TRANSITION, SevenIsland_SevaultCanyon_Summit_OnTransition
	map_script MAP_SCRIPT_ON_FRAME_TABLE, SevenIsland_SevaultCanyon_Summit_OnWarp
	.byte 0

SevenIsland_SevaultCanyon_Summit_OnTransition::
	setflag FLAG_HIDE_ECHO_SCENE
	setflag FLAG_TEMP_11
	call_if_eq VAR_ECHO_STAGE, 22, SevenIsland_SevaultCanyon_Summit_EventScript_ShowRed
	end

SevenIsland_SevaultCanyon_Summit_EventScript_ShowRed::
	clearflag FLAG_TEMP_11
	return

SevenIsland_SevaultCanyon_Summit_EventScript_Red::
	trainerbattle_single TRAINER_BIKER_1, SevenIsland_SevaultCanyon_Summit_Text_RedIntro, SevenIsland_SevaultCanyon_Summit_Text_RedDefeat, SevenIsland_SevaultCanyon_Summit_EventScript_RedWon
	msgbox SevenIsland_SevaultCanyon_Summit_Text_RedPost, MSGBOX_AUTOCLOSE
	end

SevenIsland_SevaultCanyon_Summit_EventScript_RedWon::
	special HealPlayerParty
	msgbox SevenIsland_SevaultCanyon_Summit_Text_RedPost, MSGBOX_DEFAULT
	releaseall
	end

SevenIsland_SevaultCanyon_Summit_OnWarp::
	map_script_2 VAR_TEMP_0, 0, SevenIsland_SevaultCanyon_Summit_Arrive
	.2byte 0

@ arrival on the exit-warp tile: step one tile inward (ON_FRAME, never ON_WARP: waitmovement hangs in an immediate script)
SevenIsland_SevaultCanyon_Summit_Arrive::
	setvar VAR_TEMP_0, 1
	getplayerxy VAR_0x8004, VAR_0x8005
	goto_if_ne VAR_0x8004, 8, SevenIsland_SevaultCanyon_Summit_ArriveEnd
	goto_if_eq VAR_0x8005, 42, SevenIsland_SevaultCanyon_Summit_StepUp
	goto_if_eq VAR_0x8005, 4, SevenIsland_SevaultCanyon_Summit_StepDown
SevenIsland_SevaultCanyon_Summit_ArriveEnd::
	end

SevenIsland_SevaultCanyon_Summit_StepUp::
	applymovement OBJ_EVENT_ID_PLAYER, SevenIsland_SevaultCanyon_Summit_Movement_In
	waitmovement 0
	end

SevenIsland_SevaultCanyon_Summit_StepDown::
	applymovement OBJ_EVENT_ID_PLAYER, SevenIsland_SevaultCanyon_Summit_Movement_InDown
	waitmovement 0
	end

SevenIsland_SevaultCanyon_Summit_Movement_In::
	walk_up
	step_end

SevenIsland_SevaultCanyon_Summit_Movement_InDown::
	walk_down
	step_end
