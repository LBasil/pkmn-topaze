ThornThicket_MapScripts::
	.byte 0

ThornThicket_EventScript_ReturnFerry::
	lock
	faceplayer
	msgbox ThornThicket_Text_ReturnAsk, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, ThornThicket_EventScript_Stay
	warp MAP_FUCHSIA_CITY, 255, 24, 27
	waitstate
	end

ThornThicket_EventScript_Stay::
	msgbox ThornThicket_Text_Stay
	release
	end

ThornThicket_EventScript_Npc0::
	msgbox ThornThicket_Text_Npc0, MSGBOX_NPC
	end

ThornThicket_EventScript_Npc1::
	msgbox ThornThicket_Text_Npc1, MSGBOX_NPC
	end

ThornThicket_EventScript_Quest0::
	lock
	faceplayer
	goto_if_set FLAG_TOPAZE_QUEST_THORNTHICKET, ThornThicket_EventScript_Quest0_After
	msgbox ThornThicket_Text_Quest0_Ask
	checkitem ITEM_REPEL, 2
	goto_if_eq VAR_RESULT, FALSE, ThornThicket_EventScript_Quest0_Miss
	checkitemspace ITEM_SILVER_POWDER, 1
	goto_if_eq VAR_RESULT, FALSE, ThornThicket_EventScript_Quest0_NoRoom
	removeitem ITEM_REPEL, 2
	giveitem ITEM_SILVER_POWDER, 1
	setflag FLAG_TOPAZE_QUEST_THORNTHICKET
	msgbox ThornThicket_Text_Quest0_Done
	release
	end

ThornThicket_EventScript_Quest0_After::
	msgbox ThornThicket_Text_Quest0_AfterT
	release
	end

ThornThicket_EventScript_Quest0_Miss::
	msgbox ThornThicket_Text_Quest0_MissT
	release
	end

ThornThicket_EventScript_Quest0_NoRoom::
	msgbox ThornThicket_Text_Quest0_NoRoomT
	release
	end


@ Topaze: objets caches (panneaux a script, drapeaux hors plage moteur)
ThornThicket_EventScript_TopazeFind0::
	lock
	goto_if_set FLAG_TOPAZE_FIND_THORNTHICKET_0, ThornThicket_EventScript_TopazeFind0_Done
	checkitemspace ITEM_SILVER_POWDER, 1
	goto_if_eq VAR_RESULT, FALSE, ThornThicket_EventScript_TopazeFind0_Full
	giveitem ITEM_SILVER_POWDER, 1
	setflag FLAG_TOPAZE_FIND_THORNTHICKET_0
	release
	end

ThornThicket_EventScript_TopazeFind0_Done::
	release
	end

ThornThicket_EventScript_TopazeFind0_Full::
	msgbox ThornThicket_Text_TopazeFindFull
	release
	end

ThornThicket_EventScript_TopazeFind1::
	lock
	goto_if_set FLAG_TOPAZE_FIND_THORNTHICKET_1, ThornThicket_EventScript_TopazeFind1_Done
	checkitemspace ITEM_GREAT_BALL, 1
	goto_if_eq VAR_RESULT, FALSE, ThornThicket_EventScript_TopazeFind1_Full
	giveitem ITEM_GREAT_BALL, 1
	setflag FLAG_TOPAZE_FIND_THORNTHICKET_1
	release
	end

ThornThicket_EventScript_TopazeFind1_Done::
	release
	end

ThornThicket_EventScript_TopazeFind1_Full::
	msgbox ThornThicket_Text_TopazeFindFull
	release
	end

ThornThicket_EventScript_TopazeFind2::
	lock
	goto_if_set FLAG_TOPAZE_FIND_THORNTHICKET_2, ThornThicket_EventScript_TopazeFind2_Done
	checkitemspace ITEM_REPEL, 1
	goto_if_eq VAR_RESULT, FALSE, ThornThicket_EventScript_TopazeFind2_Full
	giveitem ITEM_REPEL, 1
	setflag FLAG_TOPAZE_FIND_THORNTHICKET_2
	release
	end

ThornThicket_EventScript_TopazeFind2_Done::
	release
	end

ThornThicket_EventScript_TopazeFind2_Full::
	msgbox ThornThicket_Text_TopazeFindFull
	release
	end

