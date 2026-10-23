OneIsland_MapScripts::
	map_script MAP_SCRIPT_ON_TRANSITION, OneIsland_OnTransition
	map_script MAP_SCRIPT_ON_FRAME_TABLE, OneIsland_OnFrame
	.byte 0

OneIsland_OnTransition::
	setworldmapflag FLAG_WORLD_MAP_ONE_ISLAND
	end

OneIsland_OnFrame::
	map_script_2 VAR_MAP_SCENE_ONE_ISLAND_HARBOR, 2, OneIsland_EventScript_EnterOneIslandFirstTime
	.2byte 0

OneIsland_EventScript_EnterOneIslandFirstTime::
	lockall
	textcolor NPC_TEXT_COLOR_MALE
	applymovement LOCALID_PLAYER, OneIsland_Movement_PlayerExitHarbor
	waitmovement 0
	msgbox OneIsland_Text_BillLetsGoSeeCelio
	closemessage
	applymovement LOCALID_ONE_ISLAND_BILL, OneIsland_Movement_BillWalkToPokeCenter
	applymovement LOCALID_PLAYER, OneIsland_Movement_PlayerWalkToPokeCenter
	waitmovement 0
	opendoor 14, 5
	waitdooranim
	applymovement LOCALID_ONE_ISLAND_BILL, OneIsland_Movement_BillEnterPokeCenter
	applymovement LOCALID_PLAYER, OneIsland_Movement_PlayerEnterPokeCenter
	waitmovement 0
	closedoor 14, 5
	waitdooranim
	removeobject LOCALID_ONE_ISLAND_BILL
	setvar VAR_MAP_SCENE_ONE_ISLAND_HARBOR, 3
	warp MAP_ONE_ISLAND_POKEMON_CENTER_1F, 9, 9
	waitstate
	releaseall
	end

	.macro walk_to_pokecenter
	walk_up
	walk_up
	walk_up
	walk_up
	walk_right
	walk_right
	walk_up
	walk_up
	walk_up
	walk_up
	walk_up
	.endm

OneIsland_Movement_PlayerWalkToPokeCenter::
	walk_up
	walk_to_pokecenter
	step_end

OneIsland_Movement_PlayerEnterPokeCenter::
	walk_up
	walk_up
	set_invisible
	step_end

OneIsland_Movement_PlayerExitHarbor::
	walk_up
	step_end

OneIsland_Movement_BillWalkToPokeCenter::
	walk_to_pokecenter
	walk_up
	step_end

OneIsland_Movement_BillEnterPokeCenter::
	walk_up
	set_invisible
	step_end

OneIsland_EventScript_OldMan::
	lock
	faceplayer
	goto_if_set FLAG_SYS_CAN_LINK_WITH_RS, OneIsland_EventScript_OldManLinkHoenn
	goto_if_set FLAG_SEVII_DETOUR_FINISHED, OneIsland_EventScript_OldManLinkKanto
	msgbox OneIsland_Text_LuckyToHaveCelioHere
	release
	end

OneIsland_EventScript_OldManLinkKanto::
	msgbox OneIsland_Text_HavePCLinkageWithKanto
	release
	end

OneIsland_EventScript_OldManLinkHoenn::
	msgbox OneIsland_Text_HavePCLinkageWithHoenn
	release
	end

OneIsland_EventScript_BaldingMan::
	msgbox OneIsland_Text_IsntWarmClimateHereGreat, MSGBOX_NPC
	end

OneIsland_EventScript_IslandSign::
	msgbox OneIsland_Text_IslandSign, MSGBOX_SIGN
	end

OneIsland_EventScript_PokemonNetCenterSign::
	msgbox OneIsland_Text_PokemonNetCenterSign, MSGBOX_SIGN
	end

@ Topaze, fin 3 : Seigneur de l'ile (duel avec niveaux gonfles par VAR_TOPAZE_BOOST), apres les Maitres de la Ligue (VAR_REBELS_ROUND >= 8)
OneIsland_EventScript_Lord::
	lock
	faceplayer
	goto_if_unset FLAG_SYS_GAME_CLEAR, EventScript_ReleaseEnd
	goto_if_ne VAR_TOPAZE_ENDING, 3, OneIsland_EventScript_LordIdle
	goto_if_set FLAG_LORD_ONE, OneIsland_EventScript_LordDone
	goto_if_lt VAR_REBELS_ROUND, 8, OneIsland_EventScript_LordEarly
	msgbox OneIsland_Text_Lord1
	setvar VAR_TOPAZE_BOOST, 17
	trainerbattle_no_intro TRAINER_ELDER_WILL, OneIsland_Text_Lord2
	setvar VAR_TOPAZE_BOOST, 0
	special HealPlayerParty
	setflag FLAG_LORD_ONE
	msgbox OneIsland_Text_Lord3
	giveitem ITEM_RARE_CANDY, 4
	release
	end

OneIsland_EventScript_LordEarly::
	msgbox OneIsland_Text_LordEarly
	release
	end

OneIsland_EventScript_LordDone::
	msgbox OneIsland_Text_LordDone
	release
	end

OneIsland_EventScript_LordIdle::
	msgbox OneIsland_Text_LordIdle
	release
	end

@ Topaze, fin 2 « Le Refuge » : poste 10/16 (JONAH) — duel contre 2 chasseurs, recompense : Kangaskhan
OneIsland_EventScript_Refuge::
	lock
	faceplayer
	goto_if_ne VAR_TOPAZE_ENDING, 2, OneIsland_EventScript_RefugeIdle
	goto_if_gt VAR_REFUGE_STAGE, 9, OneIsland_EventScript_RefugeDone
	goto_if_lt VAR_REFUGE_STAGE, 9, OneIsland_EventScript_RefugeEarly
	msgbox OneIsland_Text_RefAsk
	setvar VAR_TOPAZE_BOOST, 55
	trainerbattle_no_intro TRAINER_GENTLEMAN_WALTER, OneIsland_Text_RefHunter1
	setvar VAR_TOPAZE_BOOST, 23
	trainerbattle_no_intro TRAINER_JUGGLER_GREGORY, OneIsland_Text_RefHunter2
	setvar VAR_TOPAZE_BOOST, 0
	special HealPlayerParty
	goto OneIsland_EventScript_RefugeReward
	end

OneIsland_EventScript_RefugeReward::
	msgbox OneIsland_Text_RefGives
	givemon SPECIES_KANGASKHAN, 0
	addvar VAR_REFUGE_STAGE, 1
	msgbox OneIsland_Text_RefAfter
	release
	end

OneIsland_EventScript_RefugeEarly::
	msgbox OneIsland_Text_RefEarly
	release
	end

OneIsland_EventScript_RefugeDone::
	msgbox OneIsland_Text_RefDone
	release
	end

OneIsland_EventScript_RefugeIdle::
	msgbox OneIsland_Text_RefIdle
	release
	end

@ Topaze: Bill attend à la sortie de la ville ; il renvoie vers le Centre.
OneIsland_EventScript_BillWaiting::
	lock
	faceplayer
	msgbox OneIsland_Text_BillWaiting
	release
	end
