SparkGlade_MapScripts::
	.byte 0

SparkGlade_EventScript_ReturnFerry::
	lock
	faceplayer
	msgbox SparkGlade_Text_ReturnAsk, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, SparkGlade_EventScript_Stay
	warp MAP_FUCHSIA_CITY, 255, 24, 27
	waitstate
	end

SparkGlade_EventScript_Stay::
	msgbox SparkGlade_Text_Stay
	release
	end

SparkGlade_EventScript_Npc0::
	msgbox SparkGlade_Text_Npc0, MSGBOX_NPC
	end

SparkGlade_EventScript_Npc1::
	msgbox SparkGlade_Text_Npc1, MSGBOX_NPC
	end

SparkGlade_EventScript_Quest0::
	lock
	faceplayer
	goto_if_set FLAG_TOPAZE_QUEST_SPARKGLADE, SparkGlade_EventScript_Quest0_After
	msgbox SparkGlade_Text_Quest0_Ask
	checkitem ITEM_ELIXIR, 2
	goto_if_eq VAR_RESULT, FALSE, SparkGlade_EventScript_Quest0_Miss
	checkitemspace ITEM_MAGNET, 1
	goto_if_eq VAR_RESULT, FALSE, SparkGlade_EventScript_Quest0_NoRoom
	removeitem ITEM_ELIXIR, 2
	giveitem ITEM_MAGNET, 1
	setflag FLAG_TOPAZE_QUEST_SPARKGLADE
	msgbox SparkGlade_Text_Quest0_Done
	release
	end

SparkGlade_EventScript_Quest0_After::
	msgbox SparkGlade_Text_Quest0_AfterT
	release
	end

SparkGlade_EventScript_Quest0_Miss::
	msgbox SparkGlade_Text_Quest0_MissT
	release
	end

SparkGlade_EventScript_Quest0_NoRoom::
	msgbox SparkGlade_Text_Quest0_NoRoomT
	release
	end

