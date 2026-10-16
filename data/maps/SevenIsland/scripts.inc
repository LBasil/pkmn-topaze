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

@ Topaze, fin 2 « Le Refuge » : poste 16/16 (PAXTON) — duel contre 2 chasseurs, recompense : Skarmory
SevenIsland_EventScript_Refuge::
	lock
	faceplayer
	goto_if_ne VAR_TOPAZE_ENDING, 2, SevenIsland_EventScript_RefugeIdle
	goto_if_gt VAR_REFUGE_STAGE, 15, SevenIsland_EventScript_RefugeDone
	goto_if_lt VAR_REFUGE_STAGE, 15, SevenIsland_EventScript_RefugeEarly
	msgbox SevenIsland_Text_RefAsk
	setvar VAR_TOPAZE_BOOST, 25
	trainerbattle_no_intro TRAINER_GENTLEMAN_CLIFFORD, SevenIsland_Text_RefHunter1
	setvar VAR_TOPAZE_BOOST, 44
	trainerbattle_no_intro TRAINER_JUGGLER_NATE, SevenIsland_Text_RefHunter2
	setvar VAR_TOPAZE_BOOST, 0
	special HealPlayerParty
	goto SevenIsland_EventScript_RefugeReward
	end

SevenIsland_EventScript_RefugeReward::
	msgbox SevenIsland_Text_RefGives
	givemon SPECIES_SKARMORY, 0
	addvar VAR_REFUGE_STAGE, 1
	msgbox SevenIsland_Text_RefAfter
	release
	end

SevenIsland_EventScript_RefugeEarly::
	msgbox SevenIsland_Text_RefEarly
	release
	end

SevenIsland_EventScript_RefugeDone::
	msgbox SevenIsland_Text_RefDone
	release
	end

SevenIsland_EventScript_RefugeIdle::
	msgbox SevenIsland_Text_RefIdle
	release
	end
