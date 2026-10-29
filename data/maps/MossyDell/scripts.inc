MossyDell_MapScripts::
	.byte 0

MossyDell_EventScript_ReturnFerry::
	lock
	faceplayer
	msgbox MossyDell_Text_ReturnAsk, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, MossyDell_EventScript_Stay
	warp MAP_FUCHSIA_CITY, 255, 24, 27
	waitstate
	end

MossyDell_EventScript_Stay::
	msgbox MossyDell_Text_Stay
	release
	end

MossyDell_EventScript_Npc0::
	msgbox MossyDell_Text_Npc0, MSGBOX_NPC
	end

MossyDell_EventScript_Npc1::
	msgbox MossyDell_Text_Npc1, MSGBOX_NPC
	end

MossyDell_EventScript_Quest0::
	lock
	faceplayer
	goto_if_set FLAG_TOPAZE_QUEST_MOSSYDELL, MossyDell_EventScript_Quest0_After
	msgbox MossyDell_Text_Quest0_Ask
	checkitem ITEM_ANTIDOTE, 2
	goto_if_eq VAR_RESULT, FALSE, MossyDell_EventScript_Quest0_Miss
	checkitemspace ITEM_SILVER_POWDER, 1
	goto_if_eq VAR_RESULT, FALSE, MossyDell_EventScript_Quest0_NoRoom
	removeitem ITEM_ANTIDOTE, 2
	giveitem ITEM_SILVER_POWDER, 1
	setflag FLAG_TOPAZE_QUEST_MOSSYDELL
	msgbox MossyDell_Text_Quest0_Done
	release
	end

MossyDell_EventScript_Quest0_After::
	msgbox MossyDell_Text_Quest0_AfterT
	release
	end

MossyDell_EventScript_Quest0_Miss::
	msgbox MossyDell_Text_Quest0_MissT
	release
	end

MossyDell_EventScript_Quest0_NoRoom::
	msgbox MossyDell_Text_Quest0_NoRoomT
	release
	end


@ Topaze: objets caches (panneaux a script, drapeaux hors plage moteur)
MossyDell_EventScript_TopazeFind0::
	lock
	goto_if_set FLAG_TOPAZE_FIND_MOSSYDELL_0, MossyDell_EventScript_TopazeFind0_Done
	checkitemspace ITEM_ANTIDOTE, 1
	goto_if_eq VAR_RESULT, FALSE, MossyDell_EventScript_TopazeFind0_Full
	giveitem ITEM_ANTIDOTE, 1
	setflag FLAG_TOPAZE_FIND_MOSSYDELL_0
	release
	end

MossyDell_EventScript_TopazeFind0_Done::
	release
	end

MossyDell_EventScript_TopazeFind0_Full::
	msgbox MossyDell_Text_TopazeFindFull
	release
	end

MossyDell_EventScript_TopazeFind1::
	lock
	goto_if_set FLAG_TOPAZE_FIND_MOSSYDELL_1, MossyDell_EventScript_TopazeFind1_Done
	checkitemspace ITEM_POKE_BALL, 1
	goto_if_eq VAR_RESULT, FALSE, MossyDell_EventScript_TopazeFind1_Full
	giveitem ITEM_POKE_BALL, 1
	setflag FLAG_TOPAZE_FIND_MOSSYDELL_1
	release
	end

MossyDell_EventScript_TopazeFind1_Done::
	release
	end

MossyDell_EventScript_TopazeFind1_Full::
	msgbox MossyDell_Text_TopazeFindFull
	release
	end

MossyDell_EventScript_TopazeFind2::
	lock
	goto_if_set FLAG_TOPAZE_FIND_MOSSYDELL_2, MossyDell_EventScript_TopazeFind2_Done
	checkitemspace ITEM_POTION, 1
	goto_if_eq VAR_RESULT, FALSE, MossyDell_EventScript_TopazeFind2_Full
	giveitem ITEM_POTION, 1
	setflag FLAG_TOPAZE_FIND_MOSSYDELL_2
	release
	end

MossyDell_EventScript_TopazeFind2_Done::
	release
	end

MossyDell_EventScript_TopazeFind2_Full::
	msgbox MossyDell_Text_TopazeFindFull
	release
	end

