SevenIsland_MapScripts::
	map_script MAP_SCRIPT_ON_TRANSITION, SevenIsland_OnTransition
	.byte 0

SevenIsland_OnTransition::
	setworldmapflag FLAG_WORLD_MAP_SEVEN_ISLAND
	end

SevenIsland_EventScript_IslandSign::
	msgbox SevenIsland_Text_IslandSign, MSGBOX_SIGN
	end

SevenIsland_EventScript_OldWoman::
	msgbox SevenIsland_Text_IslandsMadeInSevenDays, MSGBOX_NPC
	end

SevenIsland_EventScript_Scientist::
	msgbox SevenIsland_Text_IslandVirtuallyUntouched, MSGBOX_NPC
	end

@ Topaze, fin 3 : Seigneur de l'ile (duel avec niveaux gonfles par VAR_TOPAZE_BOOST), apres les Maitres de la Ligue (VAR_REBELS_ROUND >= 8)
SevenIsland_EventScript_Lord::
	lock
	faceplayer
	goto_if_unset FLAG_SYS_GAME_CLEAR, EventScript_ReleaseEnd
	goto_if_ne VAR_TOPAZE_ENDING, 3, SevenIsland_EventScript_LordIdle
	goto_if_set FLAG_LORD_SEVEN, SevenIsland_EventScript_LordDone
	goto_if_lt VAR_REBELS_ROUND, 8, SevenIsland_EventScript_LordEarly
	msgbox SevenIsland_Text_Lord1
	setvar VAR_TOPAZE_BOOST, 12
	trainerbattle_no_intro TRAINER_ELDER_WALLACE, SevenIsland_Text_Lord2
	setvar VAR_TOPAZE_BOOST, 0
	special HealPlayerParty
	setflag FLAG_LORD_SEVEN
	msgbox SevenIsland_Text_Lord3
	giveitem ITEM_MAX_REVIVE, 5
	release
	end

SevenIsland_EventScript_LordEarly::
	msgbox SevenIsland_Text_LordEarly
	release
	end

SevenIsland_EventScript_LordDone::
	msgbox SevenIsland_Text_LordDone
	release
	end

SevenIsland_EventScript_LordIdle::
	msgbox SevenIsland_Text_LordIdle
	release
	end
