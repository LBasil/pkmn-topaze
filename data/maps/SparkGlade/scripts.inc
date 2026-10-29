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


@ Topaze: objets caches (panneaux a script, drapeaux hors plage moteur)
SparkGlade_EventScript_TopazeFind0::
	lock
	goto_if_set FLAG_TOPAZE_FIND_SPARKGLADE_0, SparkGlade_EventScript_TopazeFind0_Done
	checkitemspace ITEM_MAX_ETHER, 1
	goto_if_eq VAR_RESULT, FALSE, SparkGlade_EventScript_TopazeFind0_Full
	giveitem ITEM_MAX_ETHER, 1
	setflag FLAG_TOPAZE_FIND_SPARKGLADE_0
	release
	end

SparkGlade_EventScript_TopazeFind0_Done::
	release
	end

SparkGlade_EventScript_TopazeFind0_Full::
	msgbox SparkGlade_Text_TopazeFindFull
	release
	end

SparkGlade_EventScript_TopazeFind1::
	lock
	goto_if_set FLAG_TOPAZE_FIND_SPARKGLADE_1, SparkGlade_EventScript_TopazeFind1_Done
	checkitemspace ITEM_ELIXIR, 1
	goto_if_eq VAR_RESULT, FALSE, SparkGlade_EventScript_TopazeFind1_Full
	giveitem ITEM_ELIXIR, 1
	setflag FLAG_TOPAZE_FIND_SPARKGLADE_1
	release
	end

SparkGlade_EventScript_TopazeFind1_Done::
	release
	end

SparkGlade_EventScript_TopazeFind1_Full::
	msgbox SparkGlade_Text_TopazeFindFull
	release
	end

SparkGlade_EventScript_TopazeFind2::
	lock
	goto_if_set FLAG_TOPAZE_FIND_SPARKGLADE_2, SparkGlade_EventScript_TopazeFind2_Done
	checkitemspace ITEM_REVIVE, 1
	goto_if_eq VAR_RESULT, FALSE, SparkGlade_EventScript_TopazeFind2_Full
	giveitem ITEM_REVIVE, 1
	setflag FLAG_TOPAZE_FIND_SPARKGLADE_2
	release
	end

SparkGlade_EventScript_TopazeFind2_Done::
	release
	end

SparkGlade_EventScript_TopazeFind2_Full::
	msgbox SparkGlade_Text_TopazeFindFull
	release
	end


SparkGlade_Text_TopazeFindFull::
	.string "Something shines here, but your BAG\n"
	.string "is full.$"
