CottonField_MapScripts::
	.byte 0

CottonField_EventScript_ReturnFerry::
	lock
	faceplayer
	msgbox CottonField_Text_ReturnAsk, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, CottonField_EventScript_Stay
	warp MAP_FUCHSIA_CITY, 255, 24, 27
	waitstate
	end

CottonField_EventScript_Stay::
	msgbox CottonField_Text_Stay
	release
	end

CottonField_EventScript_Npc0::
	msgbox CottonField_Text_Npc0, MSGBOX_NPC
	end

CottonField_EventScript_Npc1::
	msgbox CottonField_Text_Npc1, MSGBOX_NPC
	end

CottonField_EventScript_Quest0::
	lock
	faceplayer
	goto_if_set FLAG_TOPAZE_QUEST_COTTONFIELD, CottonField_EventScript_Quest0_After
	msgbox CottonField_Text_Quest0_Ask
	checkitem ITEM_SUPER_POTION, 1
	goto_if_eq VAR_RESULT, FALSE, CottonField_EventScript_Quest0_Miss
	checkitemspace ITEM_LEFTOVERS, 1
	goto_if_eq VAR_RESULT, FALSE, CottonField_EventScript_Quest0_NoRoom
	removeitem ITEM_SUPER_POTION, 1
	giveitem ITEM_LEFTOVERS, 1
	setflag FLAG_TOPAZE_QUEST_COTTONFIELD
	msgbox CottonField_Text_Quest0_Done
	release
	end

CottonField_EventScript_Quest0_After::
	msgbox CottonField_Text_Quest0_AfterT
	release
	end

CottonField_EventScript_Quest0_Miss::
	msgbox CottonField_Text_Quest0_MissT
	release
	end

CottonField_EventScript_Quest0_NoRoom::
	msgbox CottonField_Text_Quest0_NoRoomT
	release
	end


@ Topaze: objets caches (panneaux a script, drapeaux hors plage moteur)
CottonField_EventScript_TopazeFind0::
	lock
	goto_if_set FLAG_TOPAZE_FIND_COTTONFIELD_0, CottonField_EventScript_TopazeFind0_Done
	checkitemspace ITEM_SUPER_POTION, 1
	goto_if_eq VAR_RESULT, FALSE, CottonField_EventScript_TopazeFind0_Full
	giveitem ITEM_SUPER_POTION, 1
	setflag FLAG_TOPAZE_FIND_COTTONFIELD_0
	release
	end

CottonField_EventScript_TopazeFind0_Done::
	release
	end

CottonField_EventScript_TopazeFind0_Full::
	msgbox CottonField_Text_TopazeFindFull
	release
	end

CottonField_EventScript_TopazeFind1::
	lock
	goto_if_set FLAG_TOPAZE_FIND_COTTONFIELD_1, CottonField_EventScript_TopazeFind1_Done
	checkitemspace ITEM_ELIXIR, 1
	goto_if_eq VAR_RESULT, FALSE, CottonField_EventScript_TopazeFind1_Full
	giveitem ITEM_ELIXIR, 1
	setflag FLAG_TOPAZE_FIND_COTTONFIELD_1
	release
	end

CottonField_EventScript_TopazeFind1_Done::
	release
	end

CottonField_EventScript_TopazeFind1_Full::
	msgbox CottonField_Text_TopazeFindFull
	release
	end

CottonField_EventScript_TopazeFind2::
	lock
	goto_if_set FLAG_TOPAZE_FIND_COTTONFIELD_2, CottonField_EventScript_TopazeFind2_Done
	checkitemspace ITEM_LEFTOVERS, 1
	goto_if_eq VAR_RESULT, FALSE, CottonField_EventScript_TopazeFind2_Full
	giveitem ITEM_LEFTOVERS, 1
	setflag FLAG_TOPAZE_FIND_COTTONFIELD_2
	release
	end

CottonField_EventScript_TopazeFind2_Done::
	release
	end

CottonField_EventScript_TopazeFind2_Full::
	msgbox CottonField_Text_TopazeFindFull
	release
	end

