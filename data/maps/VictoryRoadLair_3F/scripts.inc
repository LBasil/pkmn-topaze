VictoryRoadLair_3F_MapScripts::
	map_script MAP_SCRIPT_ON_TRANSITION, VictoryRoadLair_3F_OnTransition
	.byte 0

VictoryRoadLair_3F_OnTransition::
	goto_if_set FLAG_VR_BOSS_DONE, VictoryRoadLair_3F_EventScript_Done
	end

VictoryRoadLair_3F_EventScript_Done::
	setvar VAR_TEMP_1, 1
	end

VictoryRoadLair_3F_EventScript_Red::
	lock
	faceplayer
	goto_if_set FLAG_VR_BOSS_DONE, VictoryRoadLair_3F_EventScript_RedHeal
	msgbox VictoryRoadLair_3F_Text_RedSilent
	release
	end

VictoryRoadLair_3F_EventScript_RedHeal::
	msgbox VictoryRoadLair_3F_Text_RedHeals
	special HealPlayerParty
	playfanfare MUS_HEAL
	waitfanfare
	msgbox VictoryRoadLair_3F_Text_RedSilent
	release
	end

VictoryRoadLair_3F_EventScript_FinalScene::
	lockall
	msgbox VictoryRoadLair_3F_Text_ShapeA
	closemessage
	setvar VAR_0x8004, 1
	setvar VAR_0x8005, 3
	setvar VAR_0x8006, 8
	setvar VAR_0x8007, 4
	playse SE_THUNDER
	special ShakeScreen
	waitstate
	playmoncry SPECIES_MEWTWO, CRY_MODE_ENCOUNTER
	waitmoncry
	msgbox VictoryRoadLair_3F_Text_ShapeB
	closemessage
	fadescreen FADE_TO_BLACK
	delay 60
	fadescreen FADE_FROM_BLACK
	msgbox VictoryRoadLair_3F_Text_ShapeC
	msgbox VictoryRoadLair_3F_Text_RedAfter
	closemessage
	setflag FLAG_VR_BOSS_DONE
	setvar VAR_TEMP_1, 1
	releaseall
	end
