AshenHeights_MapScripts::
	.byte 0

AshenHeights_EventScript_ReturnFerry::
	lock
	faceplayer
	msgbox AshenHeights_Text_ReturnAsk, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, AshenHeights_EventScript_Stay
	warp MAP_FUCHSIA_CITY, 255, 24, 27
	waitstate
	end

AshenHeights_EventScript_Stay::
	msgbox AshenHeights_Text_Stay
	release
	end

AshenHeights_EventScript_Npc0::
	msgbox AshenHeights_Text_Npc0, MSGBOX_NPC
	end

AshenHeights_EventScript_Npc1::
	msgbox AshenHeights_Text_Npc1, MSGBOX_NPC
	end

AshenHeights_EventScript_Quest0::
	lock
	faceplayer
	goto_if_set FLAG_TOPAZE_QUEST_ASHENHEIGHTS, AshenHeights_EventScript_Quest0_After
	msgbox AshenHeights_Text_Quest0_Ask
	checkitem ITEM_BURN_HEAL, 2
	goto_if_eq VAR_RESULT, FALSE, AshenHeights_EventScript_Quest0_Miss
	checkitemspace ITEM_CHARCOAL, 1
	goto_if_eq VAR_RESULT, FALSE, AshenHeights_EventScript_Quest0_NoRoom
	removeitem ITEM_BURN_HEAL, 2
	giveitem ITEM_CHARCOAL, 1
	setflag FLAG_TOPAZE_QUEST_ASHENHEIGHTS
	msgbox AshenHeights_Text_Quest0_Done
	release
	end

AshenHeights_EventScript_Quest0_After::
	msgbox AshenHeights_Text_Quest0_AfterT
	release
	end

AshenHeights_EventScript_Quest0_Miss::
	msgbox AshenHeights_Text_Quest0_MissT
	release
	end

AshenHeights_EventScript_Quest0_NoRoom::
	msgbox AshenHeights_Text_Quest0_NoRoomT
	release
	end


@ Topaze: objets caches (panneaux a script, drapeaux hors plage moteur)
AshenHeights_EventScript_TopazeFind0::
	lock
	goto_if_set FLAG_TOPAZE_FIND_ASHENHEIGHTS_0, AshenHeights_EventScript_TopazeFind0_Done
	checkitemspace ITEM_FIRE_STONE, 1
	goto_if_eq VAR_RESULT, FALSE, AshenHeights_EventScript_TopazeFind0_Full
	giveitem ITEM_FIRE_STONE, 1
	setflag FLAG_TOPAZE_FIND_ASHENHEIGHTS_0
	release
	end

AshenHeights_EventScript_TopazeFind0_Done::
	release
	end

AshenHeights_EventScript_TopazeFind0_Full::
	msgbox AshenHeights_Text_TopazeFindFull
	release
	end

AshenHeights_EventScript_TopazeFind1::
	lock
	goto_if_set FLAG_TOPAZE_FIND_ASHENHEIGHTS_1, AshenHeights_EventScript_TopazeFind1_Done
	checkitemspace ITEM_HARD_STONE, 1
	goto_if_eq VAR_RESULT, FALSE, AshenHeights_EventScript_TopazeFind1_Full
	giveitem ITEM_HARD_STONE, 1
	setflag FLAG_TOPAZE_FIND_ASHENHEIGHTS_1
	release
	end

AshenHeights_EventScript_TopazeFind1_Done::
	release
	end

AshenHeights_EventScript_TopazeFind1_Full::
	msgbox AshenHeights_Text_TopazeFindFull
	release
	end

AshenHeights_EventScript_TopazeFind2::
	lock
	goto_if_set FLAG_TOPAZE_FIND_ASHENHEIGHTS_2, AshenHeights_EventScript_TopazeFind2_Done
	checkitemspace ITEM_BURN_HEAL, 1
	goto_if_eq VAR_RESULT, FALSE, AshenHeights_EventScript_TopazeFind2_Full
	giveitem ITEM_BURN_HEAL, 1
	setflag FLAG_TOPAZE_FIND_ASHENHEIGHTS_2
	release
	end

AshenHeights_EventScript_TopazeFind2_Done::
	release
	end

AshenHeights_EventScript_TopazeFind2_Full::
	msgbox AshenHeights_Text_TopazeFindFull
	release
	end

