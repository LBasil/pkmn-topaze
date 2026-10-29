CrownField_MapScripts::
	.byte 0

CrownField_EventScript_ReturnFerry::
	lock
	faceplayer
	msgbox CrownField_Text_ReturnAsk, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, CrownField_EventScript_Stay
	warp MAP_FUCHSIA_CITY, 255, 24, 27
	waitstate
	end

CrownField_EventScript_Stay::
	msgbox CrownField_Text_Stay
	release
	end

CrownField_EventScript_Npc0::
	msgbox CrownField_Text_Npc0, MSGBOX_NPC
	end

CrownField_EventScript_Npc1::
	msgbox CrownField_Text_Npc1, MSGBOX_NPC
	end

CrownField_EventScript_Quest0::
	lock
	faceplayer
	goto_if_set FLAG_TOPAZE_QUEST_CROWNFIELD, CrownField_EventScript_Quest0_After
	msgbox CrownField_Text_Quest0_Ask
	checkitem ITEM_RARE_CANDY, 1
	goto_if_eq VAR_RESULT, FALSE, CrownField_EventScript_Quest0_Miss
	checkitemspace ITEM_PP_MAX, 1
	goto_if_eq VAR_RESULT, FALSE, CrownField_EventScript_Quest0_NoRoom
	removeitem ITEM_RARE_CANDY, 1
	giveitem ITEM_PP_MAX, 1
	setflag FLAG_TOPAZE_QUEST_CROWNFIELD
	msgbox CrownField_Text_Quest0_Done
	release
	end

CrownField_EventScript_Quest0_After::
	msgbox CrownField_Text_Quest0_AfterT
	release
	end

CrownField_EventScript_Quest0_Miss::
	msgbox CrownField_Text_Quest0_MissT
	release
	end

CrownField_EventScript_Quest0_NoRoom::
	msgbox CrownField_Text_Quest0_NoRoomT
	release
	end


@ Topaze: objets caches (panneaux a script, drapeaux hors plage moteur)
CrownField_EventScript_TopazeFind0::
	lock
	goto_if_set FLAG_TOPAZE_FIND_CROWNFIELD_0, CrownField_EventScript_TopazeFind0_Done
	checkitemspace ITEM_RARE_CANDY, 1
	goto_if_eq VAR_RESULT, FALSE, CrownField_EventScript_TopazeFind0_Full
	giveitem ITEM_RARE_CANDY, 1
	setflag FLAG_TOPAZE_FIND_CROWNFIELD_0
	release
	end

CrownField_EventScript_TopazeFind0_Done::
	release
	end

CrownField_EventScript_TopazeFind0_Full::
	msgbox CrownField_Text_TopazeFindFull
	release
	end

CrownField_EventScript_TopazeFind1::
	lock
	goto_if_set FLAG_TOPAZE_FIND_CROWNFIELD_1, CrownField_EventScript_TopazeFind1_Done
	checkitemspace ITEM_MAX_REVIVE, 1
	goto_if_eq VAR_RESULT, FALSE, CrownField_EventScript_TopazeFind1_Full
	giveitem ITEM_MAX_REVIVE, 1
	setflag FLAG_TOPAZE_FIND_CROWNFIELD_1
	release
	end

CrownField_EventScript_TopazeFind1_Done::
	release
	end

CrownField_EventScript_TopazeFind1_Full::
	msgbox CrownField_Text_TopazeFindFull
	release
	end

CrownField_EventScript_TopazeFind2::
	lock
	goto_if_set FLAG_TOPAZE_FIND_CROWNFIELD_2, CrownField_EventScript_TopazeFind2_Done
	checkitemspace ITEM_PP_UP, 1
	goto_if_eq VAR_RESULT, FALSE, CrownField_EventScript_TopazeFind2_Full
	giveitem ITEM_PP_UP, 1
	setflag FLAG_TOPAZE_FIND_CROWNFIELD_2
	release
	end

CrownField_EventScript_TopazeFind2_Done::
	release
	end

CrownField_EventScript_TopazeFind2_Full::
	msgbox CrownField_Text_TopazeFindFull
	release
	end

