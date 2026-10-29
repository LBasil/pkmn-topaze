QuarryHeights_MapScripts::
	.byte 0

QuarryHeights_EventScript_ReturnFerry::
	lock
	faceplayer
	msgbox QuarryHeights_Text_ReturnAsk, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, QuarryHeights_EventScript_Stay
	warp MAP_FUCHSIA_CITY, 255, 24, 27
	waitstate
	end

QuarryHeights_EventScript_Stay::
	msgbox QuarryHeights_Text_Stay
	release
	end

QuarryHeights_EventScript_Npc0::
	msgbox QuarryHeights_Text_Npc0, MSGBOX_NPC
	end

QuarryHeights_EventScript_Npc1::
	msgbox QuarryHeights_Text_Npc1, MSGBOX_NPC
	end

QuarryHeights_EventScript_Quest0::
	lock
	faceplayer
	goto_if_set FLAG_TOPAZE_QUEST_QUARRYHEIGHTS, QuarryHeights_EventScript_Quest0_After
	msgbox QuarryHeights_Text_Quest0_Ask
	checkitem ITEM_IRON, 1
	goto_if_eq VAR_RESULT, FALSE, QuarryHeights_EventScript_Quest0_Miss
	checkitemspace ITEM_METAL_COAT, 1
	goto_if_eq VAR_RESULT, FALSE, QuarryHeights_EventScript_Quest0_NoRoom
	removeitem ITEM_IRON, 1
	giveitem ITEM_METAL_COAT, 1
	setflag FLAG_TOPAZE_QUEST_QUARRYHEIGHTS
	msgbox QuarryHeights_Text_Quest0_Done
	release
	end

QuarryHeights_EventScript_Quest0_After::
	msgbox QuarryHeights_Text_Quest0_AfterT
	release
	end

QuarryHeights_EventScript_Quest0_Miss::
	msgbox QuarryHeights_Text_Quest0_MissT
	release
	end

QuarryHeights_EventScript_Quest0_NoRoom::
	msgbox QuarryHeights_Text_Quest0_NoRoomT
	release
	end


@ Topaze: objets caches (panneaux a script, drapeaux hors plage moteur)
QuarryHeights_EventScript_TopazeFind0::
	lock
	goto_if_set FLAG_TOPAZE_FIND_QUARRYHEIGHTS_0, QuarryHeights_EventScript_TopazeFind0_Done
	checkitemspace ITEM_METAL_COAT, 1
	goto_if_eq VAR_RESULT, FALSE, QuarryHeights_EventScript_TopazeFind0_Full
	giveitem ITEM_METAL_COAT, 1
	setflag FLAG_TOPAZE_FIND_QUARRYHEIGHTS_0
	release
	end

QuarryHeights_EventScript_TopazeFind0_Done::
	release
	end

QuarryHeights_EventScript_TopazeFind0_Full::
	msgbox QuarryHeights_Text_TopazeFindFull
	release
	end

QuarryHeights_EventScript_TopazeFind1::
	lock
	goto_if_set FLAG_TOPAZE_FIND_QUARRYHEIGHTS_1, QuarryHeights_EventScript_TopazeFind1_Done
	checkitemspace ITEM_HARD_STONE, 1
	goto_if_eq VAR_RESULT, FALSE, QuarryHeights_EventScript_TopazeFind1_Full
	giveitem ITEM_HARD_STONE, 1
	setflag FLAG_TOPAZE_FIND_QUARRYHEIGHTS_1
	release
	end

QuarryHeights_EventScript_TopazeFind1_Done::
	release
	end

QuarryHeights_EventScript_TopazeFind1_Full::
	msgbox QuarryHeights_Text_TopazeFindFull
	release
	end

QuarryHeights_EventScript_TopazeFind2::
	lock
	goto_if_set FLAG_TOPAZE_FIND_QUARRYHEIGHTS_2, QuarryHeights_EventScript_TopazeFind2_Done
	checkitemspace ITEM_IRON, 1
	goto_if_eq VAR_RESULT, FALSE, QuarryHeights_EventScript_TopazeFind2_Full
	giveitem ITEM_IRON, 1
	setflag FLAG_TOPAZE_FIND_QUARRYHEIGHTS_2
	release
	end

QuarryHeights_EventScript_TopazeFind2_Done::
	release
	end

QuarryHeights_EventScript_TopazeFind2_Full::
	msgbox QuarryHeights_Text_TopazeFindFull
	release
	end

