.equ REQUIRED_SEEN_MONS, 10

Route2_EastBuilding_MapScripts::
	.byte 0

Route2_EastBuilding_EventScript_Aide::
	lock
	faceplayer
	call Route2_EastBuilding_EventScript_GetAideRequestInfo
	goto_if_set FLAG_GOT_HM05, Route2_EastBuilding_EventScript_AlreadyGotHM05
	msgbox Route2_EastBuilding_Text_GiveHM05IfSeen10Mons, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, Aide_EventScript_DeclineCheckMons
	setvar VAR_0x8004, 0
	specialvar VAR_RESULT, GetPokedexCount
	buffernumberstring STR_VAR_3, VAR_0x8006
	call Route2_EastBuilding_EventScript_GetAideRequestInfo
	goto_if_lt VAR_0x8006, REQUIRED_SEEN_MONS, Aide_EventScript_HaventCaughtEnough
	msgbox Route2_EastBuilding_Text_GreatHereYouGo
	checkitemspace ITEM_HM05
	goto_if_eq VAR_RESULT, FALSE, Aide_EventScript_NoRoomForItem
	giveitem_msg Route2_EastBuilding_Text_ReceivedHM05FromAide, ITEM_HM05
	setflag FLAG_GOT_HM05
	msgbox Route2_EastBuilding_Text_ExplainHM05
	goto Route2_EastBuilding_EventScript_GivePokeRadar
	end

Route2_EastBuilding_EventScript_AlreadyGotHM05::
	msgbox Route2_EastBuilding_Text_ExplainHM05
	goto Route2_EastBuilding_EventScript_GivePokeRadar
	end

Route2_EastBuilding_EventScript_GivePokeRadar::
	checkitem ITEM_10B
	goto_if_eq VAR_RESULT, TRUE, Route2_EastBuilding_EventScript_RadarDone
	checkitemspace ITEM_10B
	goto_if_eq VAR_RESULT, FALSE, Aide_EventScript_NoRoomForItem
	msgbox Route2_EastBuilding_Text_RadarIntro
	giveitem_msg Route2_EastBuilding_Text_ReceivedRadar, ITEM_10B
	msgbox Route2_EastBuilding_Text_RadarExplain
Route2_EastBuilding_EventScript_RadarDone::
	release
	end

Route2_EastBuilding_EventScript_GetAideRequestInfo::
	buffernumberstring STR_VAR_1, REQUIRED_SEEN_MONS
	bufferitemname STR_VAR_2, ITEM_HM05
	return

Route2_EastBuilding_EventScript_Rocker::
	msgbox Route2_EastBuilding_Text_CanGetThroughRockTunnel, MSGBOX_NPC
	end

Route2_EastBuilding_Text_RadarIntro:
	.string "Oh, and take this too! A prototype\n"
	.string "I built for tracking POKéMON.$"

Route2_EastBuilding_Text_ReceivedRadar:
	.string "{PLAYER} received a POKé RADAR!$"

Route2_EastBuilding_Text_RadarExplain:
	.string "Open it from the START menu and\n"
	.string "pick a POKéMON you have seen here.\n"
	.string "Walk up to the rustling grass, but\n"
	.string "don't run or it will flee!\p"
	.string "Beat or catch the same species in\n"
	.string "a row to chain it: shinies get\n"
	.string "much more likely!$"
