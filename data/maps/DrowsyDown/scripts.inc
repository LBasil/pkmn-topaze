DrowsyDown_MapScripts::
	.byte 0

DrowsyDown_EventScript_ReturnFerry::
	lock
	faceplayer
	msgbox DrowsyDown_Text_ReturnAsk, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, DrowsyDown_EventScript_Stay
	warp MAP_FUCHSIA_CITY, 255, 24, 27
	waitstate
	end

DrowsyDown_EventScript_Stay::
	msgbox DrowsyDown_Text_Stay
	release
	end

DrowsyDown_EventScript_Npc0::
	msgbox DrowsyDown_Text_Npc0, MSGBOX_NPC
	end

DrowsyDown_EventScript_Npc1::
	msgbox DrowsyDown_Text_Npc1, MSGBOX_NPC
	end

DrowsyDown_EventScript_Quest0::
	lock
	faceplayer
	goto_if_set FLAG_TOPAZE_QUEST_DROWSYDOWN, DrowsyDown_EventScript_Quest0_After
	msgbox DrowsyDown_Text_Quest0_Ask
	checkitem ITEM_CHESTO_BERRY, 1
	goto_if_eq VAR_RESULT, FALSE, DrowsyDown_EventScript_Quest0_Miss
	checkitemspace ITEM_LEFTOVERS, 1
	goto_if_eq VAR_RESULT, FALSE, DrowsyDown_EventScript_Quest0_NoRoom
	removeitem ITEM_CHESTO_BERRY, 1
	giveitem ITEM_LEFTOVERS, 1
	setflag FLAG_TOPAZE_QUEST_DROWSYDOWN
	msgbox DrowsyDown_Text_Quest0_Done
	release
	end

DrowsyDown_EventScript_Quest0_After::
	msgbox DrowsyDown_Text_Quest0_AfterT
	release
	end

DrowsyDown_EventScript_Quest0_Miss::
	msgbox DrowsyDown_Text_Quest0_MissT
	release
	end

DrowsyDown_EventScript_Quest0_NoRoom::
	msgbox DrowsyDown_Text_Quest0_NoRoomT
	release
	end


@ Topaze: objets caches (panneaux a script, drapeaux hors plage moteur)
DrowsyDown_EventScript_TopazeFind0::
	lock
	goto_if_set FLAG_TOPAZE_FIND_DROWSYDOWN_0, DrowsyDown_EventScript_TopazeFind0_Done
	checkitemspace ITEM_LEFTOVERS, 1
	goto_if_eq VAR_RESULT, FALSE, DrowsyDown_EventScript_TopazeFind0_Full
	giveitem ITEM_LEFTOVERS, 1
	setflag FLAG_TOPAZE_FIND_DROWSYDOWN_0
	release
	end

DrowsyDown_EventScript_TopazeFind0_Done::
	release
	end

DrowsyDown_EventScript_TopazeFind0_Full::
	msgbox DrowsyDown_Text_TopazeFindFull
	release
	end

DrowsyDown_EventScript_TopazeFind1::
	lock
	goto_if_set FLAG_TOPAZE_FIND_DROWSYDOWN_1, DrowsyDown_EventScript_TopazeFind1_Done
	checkitemspace ITEM_CHESTO_BERRY, 1
	goto_if_eq VAR_RESULT, FALSE, DrowsyDown_EventScript_TopazeFind1_Full
	giveitem ITEM_CHESTO_BERRY, 1
	setflag FLAG_TOPAZE_FIND_DROWSYDOWN_1
	release
	end

DrowsyDown_EventScript_TopazeFind1_Done::
	release
	end

DrowsyDown_EventScript_TopazeFind1_Full::
	msgbox DrowsyDown_Text_TopazeFindFull
	release
	end

DrowsyDown_EventScript_TopazeFind2::
	lock
	goto_if_set FLAG_TOPAZE_FIND_DROWSYDOWN_2, DrowsyDown_EventScript_TopazeFind2_Done
	checkitemspace ITEM_SUPER_POTION, 1
	goto_if_eq VAR_RESULT, FALSE, DrowsyDown_EventScript_TopazeFind2_Full
	giveitem ITEM_SUPER_POTION, 1
	setflag FLAG_TOPAZE_FIND_DROWSYDOWN_2
	release
	end

DrowsyDown_EventScript_TopazeFind2_Done::
	release
	end

DrowsyDown_EventScript_TopazeFind2_Full::
	msgbox DrowsyDown_Text_TopazeFindFull
	release
	end

