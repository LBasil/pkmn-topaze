FiveIsland_MapScripts::
	map_script MAP_SCRIPT_ON_TRANSITION, FiveIsland_OnTransition
	.byte 0

FiveIsland_OnTransition::
	setworldmapflag FLAG_WORLD_MAP_FIVE_ISLAND
	end

FiveIsland_EventScript_IslandSign::
	msgbox FiveIsland_Text_IslandSign, MSGBOX_SIGN
	end

FiveIsland_EventScript_BugCatcher::
	msgbox FiveIsland_Text_WeirdBuildingInMeadow, MSGBOX_NPC
	end

FiveIsland_EventScript_Fisher::
	msgbox FiveIsland_Text_BeenGettingBusierAroundHere, MSGBOX_NPC
	end

@ Topaze, fin 3 : Seigneur de l'ile (duel avec niveaux gonfles par VAR_TOPAZE_BOOST), apres les Maitres de la Ligue (VAR_REBELS_ROUND >= 8)
FiveIsland_EventScript_Lord::
	lock
	faceplayer
	goto_if_unset FLAG_SYS_GAME_CLEAR, EventScript_ReleaseEnd
	goto_if_ne VAR_TOPAZE_ENDING, 3, FiveIsland_EventScript_LordIdle
	goto_if_set FLAG_LORD_FIVE, FiveIsland_EventScript_LordDone
	goto_if_lt VAR_REBELS_ROUND, 8, FiveIsland_EventScript_LordEarly
	msgbox FiveIsland_Text_Lord1
	setvar VAR_TOPAZE_BOOST, 14
	trainerbattle_no_intro TRAINER_ELDER_PHOEBE, FiveIsland_Text_Lord2
	setvar VAR_TOPAZE_BOOST, 0
	special HealPlayerParty
	setflag FLAG_LORD_FIVE
	msgbox FiveIsland_Text_Lord3
	giveitem ITEM_MAX_ELIXIR, 5
	release
	end

FiveIsland_EventScript_LordEarly::
	msgbox FiveIsland_Text_LordEarly
	release
	end

FiveIsland_EventScript_LordDone::
	msgbox FiveIsland_Text_LordDone
	release
	end

FiveIsland_EventScript_LordIdle::
	msgbox FiveIsland_Text_LordIdle
	release
	end

@ Topaze, fin 2 « Le Refuge » : poste 14/16 (NOEL) — duel contre 2 chasseurs, recompense : Tauros
FiveIsland_EventScript_Refuge::
	lock
	faceplayer
	goto_if_ne VAR_TOPAZE_ENDING, 2, FiveIsland_EventScript_RefugeIdle
	goto_if_gt VAR_REFUGE_STAGE, 13, FiveIsland_EventScript_RefugeDone
	goto_if_lt VAR_REFUGE_STAGE, 13, FiveIsland_EventScript_RefugeEarly
	msgbox FiveIsland_Text_RefAsk
	setvar VAR_TOPAZE_BOOST, 59
	trainerbattle_no_intro TRAINER_GENTLEMAN_LAMAR, FiveIsland_Text_RefHunter1
	setvar VAR_TOPAZE_BOOST, 41
	trainerbattle_no_intro TRAINER_JUGGLER_KAYDEN, FiveIsland_Text_RefHunter2
	setvar VAR_TOPAZE_BOOST, 0
	special HealPlayerParty
	goto FiveIsland_EventScript_RefugeReward
	end

FiveIsland_EventScript_RefugeReward::
	msgbox FiveIsland_Text_RefGives
	givemon SPECIES_TAUROS, 0
	addvar VAR_REFUGE_STAGE, 1
	msgbox FiveIsland_Text_RefAfter
	release
	end

FiveIsland_EventScript_RefugeEarly::
	msgbox FiveIsland_Text_RefEarly
	release
	end

FiveIsland_EventScript_RefugeDone::
	msgbox FiveIsland_Text_RefDone
	release
	end

FiveIsland_EventScript_RefugeIdle::
	msgbox FiveIsland_Text_RefIdle
	release
	end
