ThreeIsland_Port_MapScripts::
	map_script MAP_SCRIPT_ON_TRANSITION, ThreeIsland_Port_OnTransition
	.byte 0

ThreeIsland_Port_OnTransition::
	clearflag FLAG_SYS_PC_STORAGE_DISABLED
	setflag FLAG_SEVII_DETOUR_FINISHED
	goto_if_set FLAG_TOPAZE_COUNCIL, ThreeIsland_Port_EventScript_PostgameBikersGone
	end

@ Topaze : la route de Bond Bridge (Echo 3) ne doit pas dependre de la quete vanilla des motards (Joyful Game Corner / Lostelle).
ThreeIsland_Port_EventScript_PostgameBikersGone::
	setflag FLAG_HIDE_THREE_ISLAND_BIKERS
	setflag FLAG_HIDE_THREE_ISLAND_ANTIBIKERS
	setflag FLAG_HIDE_THREE_ISLAND_LONE_BIKER
	call_if_lt VAR_MAP_SCENE_THREE_ISLAND, 4, ThreeIsland_Port_EventScript_SetBikersGone
	end

ThreeIsland_Port_EventScript_SetBikersGone::
	setvar VAR_MAP_SCENE_THREE_ISLAND, 4
	return

ThreeIsland_Port_EventScript_Woman::
	lock
	faceplayer
	goto_if_ge VAR_MAP_SCENE_TWO_ISLAND_JOYFUL_GAME_CORNER, 2, ThreeIsland_Port_EventScript_WomanLostelleFound
	goto_if_ge VAR_MAP_SCENE_THREE_ISLAND, 4, ThreeIsland_Port_EventScript_WomanBikersGone
	msgbox ThreeIsland_Port_Text_IllCallThePolice
	release
	end

ThreeIsland_Port_EventScript_WomanLostelleFound::
	msgbox ThreeIsland_Port_Text_EverythingTurnedOutForBest
	release
	end

ThreeIsland_Port_EventScript_WomanBikersGone::
	msgbox ThreeIsland_Port_Text_ThankGoodnessBikersGone
	release
	end

ThreeIsland_Port_EventScript_Biker1::
	msgbox ThreeIsland_Port_Text_WereKantoRiderFederation, MSGBOX_NPC
	end

ThreeIsland_Port_EventScript_Biker2::
	lock
	msgbox ThreeIsland_Port_Text_ForkOverMoney
	release
	end
