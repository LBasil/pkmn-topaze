GaleCliff_MapScripts::
	.byte 0

GaleCliff_EventScript_ReturnFerry::
	lock
	faceplayer
	msgbox GaleCliff_Text_ReturnAsk, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, GaleCliff_EventScript_Stay
	warp MAP_FUCHSIA_CITY, 255, 24, 27
	waitstate
	end

GaleCliff_EventScript_Stay::
	msgbox GaleCliff_Text_Stay
	release
	end

GaleCliff_EventScript_Npc0::
	msgbox GaleCliff_Text_Npc0, MSGBOX_NPC
	end

GaleCliff_EventScript_Npc1::
	msgbox GaleCliff_Text_Npc1, MSGBOX_NPC
	end

GaleCliff_EventScript_Quest0::
	lock
	faceplayer
	goto_if_set FLAG_TOPAZE_QUEST_GALECLIFF, GaleCliff_EventScript_Quest0_After
	msgbox GaleCliff_Text_Quest0_Ask
	checkitem ITEM_GREAT_BALL, 2
	goto_if_eq VAR_RESULT, FALSE, GaleCliff_EventScript_Quest0_Miss
	checkitemspace ITEM_SHARP_BEAK, 1
	goto_if_eq VAR_RESULT, FALSE, GaleCliff_EventScript_Quest0_NoRoom
	removeitem ITEM_GREAT_BALL, 2
	giveitem ITEM_SHARP_BEAK, 1
	setflag FLAG_TOPAZE_QUEST_GALECLIFF
	msgbox GaleCliff_Text_Quest0_Done
	release
	end

GaleCliff_EventScript_Quest0_After::
	msgbox GaleCliff_Text_Quest0_AfterT
	release
	end

GaleCliff_EventScript_Quest0_Miss::
	msgbox GaleCliff_Text_Quest0_MissT
	release
	end

GaleCliff_EventScript_Quest0_NoRoom::
	msgbox GaleCliff_Text_Quest0_NoRoomT
	release
	end


@ Topaze: objets caches (panneaux a script, drapeaux hors plage moteur)
GaleCliff_EventScript_TopazeFind0::
	lock
	goto_if_set FLAG_TOPAZE_FIND_GALECLIFF_0, GaleCliff_EventScript_TopazeFind0_Done
	checkitemspace ITEM_SHARP_BEAK, 1
	goto_if_eq VAR_RESULT, FALSE, GaleCliff_EventScript_TopazeFind0_Full
	giveitem ITEM_SHARP_BEAK, 1
	setflag FLAG_TOPAZE_FIND_GALECLIFF_0
	release
	end

GaleCliff_EventScript_TopazeFind0_Done::
	release
	end

GaleCliff_EventScript_TopazeFind0_Full::
	msgbox GaleCliff_Text_TopazeFindFull
	release
	end

GaleCliff_EventScript_TopazeFind1::
	lock
	goto_if_set FLAG_TOPAZE_FIND_GALECLIFF_1, GaleCliff_EventScript_TopazeFind1_Done
	checkitemspace ITEM_GREAT_BALL, 1
	goto_if_eq VAR_RESULT, FALSE, GaleCliff_EventScript_TopazeFind1_Full
	giveitem ITEM_GREAT_BALL, 1
	setflag FLAG_TOPAZE_FIND_GALECLIFF_1
	release
	end

GaleCliff_EventScript_TopazeFind1_Done::
	release
	end

GaleCliff_EventScript_TopazeFind1_Full::
	msgbox GaleCliff_Text_TopazeFindFull
	release
	end

GaleCliff_EventScript_TopazeFind2::
	lock
	goto_if_set FLAG_TOPAZE_FIND_GALECLIFF_2, GaleCliff_EventScript_TopazeFind2_Done
	checkitemspace ITEM_REVIVE, 1
	goto_if_eq VAR_RESULT, FALSE, GaleCliff_EventScript_TopazeFind2_Full
	giveitem ITEM_REVIVE, 1
	setflag FLAG_TOPAZE_FIND_GALECLIFF_2
	release
	end

GaleCliff_EventScript_TopazeFind2_Done::
	release
	end

GaleCliff_EventScript_TopazeFind2_Full::
	msgbox GaleCliff_Text_TopazeFindFull
	release
	end

