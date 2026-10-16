SixIsland_MapScripts::
	map_script MAP_SCRIPT_ON_TRANSITION, SixIsland_OnTransition
	.byte 0

SixIsland_OnTransition::
	setworldmapflag FLAG_WORLD_MAP_SIX_ISLAND
	end

SixIsland_EventScript_Hiker::
	msgbox SixIsland_Text_ThatWayToWaterPathRuinValley, MSGBOX_NPC
	end

SixIsland_EventScript_Boy::
	msgbox SixIsland_Text_SkyAtNightIsFantastic, MSGBOX_NPC
	end

SixIsland_EventScript_IslandSign::
	msgbox SixIsland_Text_IslandSign, MSGBOX_SIGN
	end

@ Topaze, fin 3 : Seigneur de l'ile (duel avec niveaux gonfles par VAR_TOPAZE_BOOST), apres les Maitres de la Ligue (VAR_REBELS_ROUND >= 8)
SixIsland_EventScript_Lord::
	lock
	faceplayer
	goto_if_unset FLAG_SYS_GAME_CLEAR, EventScript_ReleaseEnd
	goto_if_ne VAR_TOPAZE_ENDING, 3, SixIsland_EventScript_LordIdle
	goto_if_set FLAG_LORD_SIX, SixIsland_EventScript_LordDone
	goto_if_lt VAR_REBELS_ROUND, 8, SixIsland_EventScript_LordEarly
	msgbox SixIsland_Text_Lord1
	setvar VAR_TOPAZE_BOOST, 13
	trainerbattle_no_intro TRAINER_ELDER_DRAKE, SixIsland_Text_Lord2
	setvar VAR_TOPAZE_BOOST, 0
	special HealPlayerParty
	setflag FLAG_LORD_SIX
	msgbox SixIsland_Text_Lord3
	giveitem ITEM_PP_MAX, 4
	release
	end

SixIsland_EventScript_LordEarly::
	msgbox SixIsland_Text_LordEarly
	release
	end

SixIsland_EventScript_LordDone::
	msgbox SixIsland_Text_LordDone
	release
	end

SixIsland_EventScript_LordIdle::
	msgbox SixIsland_Text_LordIdle
	release
	end
