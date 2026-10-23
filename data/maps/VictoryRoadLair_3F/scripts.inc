VictoryRoadLair_3F_MapScripts::
	map_script MAP_SCRIPT_ON_TRANSITION, VictoryRoadLair_3F_OnTransition
	.byte 0

VictoryRoadLair_3F_OnTransition::
	setflag FLAG_TEMP_2
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

VictoryRoadLair_3F_EventScript_KronosStub::
	end

@ Topaze: scene finale du repaire (refaite le 23/10) : le dernier gardien (KRONOS), le pendentif qui sert de phare,
@ la voix du patron qui explique son but et la suite (la Ligue), puis RED libere.
VictoryRoadLair_3F_EventScript_FinalScene::
	lockall
	msgbox VictoryRoadLair_3F_Text_Cold
	closemessage
	applymovement LOCALID_PLAYER, VictoryRoadLair_3F_Movement_PlayerUp2
	waitmovement 0
	clearflag FLAG_TEMP_2
	addobject LOCALID_LAIR_KRONOS
	playse SE_PIN
	delay 30
	applymovement LOCALID_LAIR_KRONOS, VictoryRoadLair_3F_Movement_KronosDown
	waitmovement 0
	msgbox VictoryRoadLair_3F_Text_KronosIntro
	closemessage
	setvar VAR_LAST_TALKED, LOCALID_LAIR_KRONOS
	trainerbattle_no_intro TRAINER_AQUA_LEADER, VictoryRoadLair_3F_Text_KronosDefeat
	msgbox VictoryRoadLair_3F_Text_KronosLamp
	closemessage
	playse SE_PIN
	delay 20
	msgbox VictoryRoadLair_3F_Text_PendantHeats
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
	msgbox VictoryRoadLair_3F_Text_StonesCall
	closemessage
	fadescreen FADE_TO_WHITE
	delay 40
	fadescreen FADE_FROM_WHITE
	msgbox VictoryRoadLair_3F_Text_BossVoice1
	msgbox VictoryRoadLair_3F_Text_BossVoice2
	closemessage
	special ShakeScreen
	waitstate
	fadescreen FADE_TO_BLACK
	delay 60
	fadescreen FADE_FROM_BLACK
	msgbox VictoryRoadLair_3F_Text_ShapeGone
	closemessage
	msgbox VictoryRoadLair_3F_Text_KronosLeaves
	closemessage
	fadescreen FADE_TO_BLACK
	removeobject LOCALID_LAIR_KRONOS
	delay 30
	fadescreen FADE_FROM_BLACK
	msgbox VictoryRoadLair_3F_Text_RedAfter
	closemessage
	setflag FLAG_VR_BOSS_DONE
	setvar VAR_TEMP_1, 1
	releaseall
	end

VictoryRoadLair_3F_Movement_PlayerUp2::
	walk_up
	walk_up
	step_end

VictoryRoadLair_3F_Movement_KronosDown::
	walk_down
	walk_down
	step_end
