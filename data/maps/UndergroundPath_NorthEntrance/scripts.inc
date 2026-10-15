UndergroundPath_NorthEntrance_MapScripts::
	.byte 0

UndergroundPath_NorthEntrance_EventScript_Saige::
	lock
	faceplayer
	goto_if_set FLAG_DID_MS_NIDO_TRADE, UndergroundPath_NorthEntrance_EventScript_Saige_Done
	msgbox UndergroundPath_NorthEntrance_Text_QuestAsk
	setvar VAR_0x8004, 1
	specialvar VAR_RESULT, GetPokedexCount
	buffernumberstring STR_VAR_1, VAR_0x8006
	goto_if_lt VAR_0x8006, 40, UndergroundPath_NorthEntrance_EventScript_Saige_No
	checkitemspace ITEM_SUN_STONE
	goto_if_eq VAR_RESULT, FALSE, UndergroundPath_NorthEntrance_EventScript_Saige_NoRoom
	msgbox UndergroundPath_NorthEntrance_Text_QuestOk
	giveitem_msg UndergroundPath_NorthEntrance_Text_QuestGot, ITEM_SUN_STONE
	setflag FLAG_DID_MS_NIDO_TRADE
	release
	end

UndergroundPath_NorthEntrance_EventScript_Saige_No::
	msgbox UndergroundPath_NorthEntrance_Text_QuestNo
	release
	end

UndergroundPath_NorthEntrance_EventScript_Saige_NoRoom::
	msgbox UndergroundPath_NorthEntrance_Text_QuestNoRoom
	release
	end

UndergroundPath_NorthEntrance_EventScript_Saige_Done::
	msgbox UndergroundPath_NorthEntrance_Text_QuestDone
	release
	end

UndergroundPath_NorthEntrance_Text_QuestAsk::
    .string "I collect POKéMON data, and I\nlove people who do too!\pCatch 40 kinds of POKéMON and I\nwill give you something warm.$"

UndergroundPath_NorthEntrance_Text_QuestOk::
    .string "Wow, you caught {STR_VAR_1} kinds!\pHere, a SUN STONE for you!$"

UndergroundPath_NorthEntrance_Text_QuestGot::
    .string "{PLAYER} received a SUN STONE!$"

UndergroundPath_NorthEntrance_Text_QuestNo::
    .string "You've caught only {STR_VAR_1} kinds.\nKeep going until you reach 40!$"

UndergroundPath_NorthEntrance_Text_QuestNoRoom::
    .string "Your BAG is full. Make some\nroom first!$"

UndergroundPath_NorthEntrance_Text_QuestDone::
    .string "Do you use the SUN STONE\nwell?$"
