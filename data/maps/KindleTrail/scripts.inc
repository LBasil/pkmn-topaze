KindleTrail_MapScripts::
	.byte 0

KindleTrail_EventScript_ReturnFerry::
	lock
	faceplayer
	msgbox KindleTrail_Text_ReturnAsk, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, KindleTrail_EventScript_Stay
	warp MAP_FUCHSIA_CITY, 255, 24, 27
	waitstate
	end

KindleTrail_EventScript_Stay::
	msgbox KindleTrail_Text_Stay
	release
	end

KindleTrail_EventScript_Npc0::
	msgbox KindleTrail_Text_Npc0, MSGBOX_NPC
	end

KindleTrail_EventScript_Npc1::
	msgbox KindleTrail_Text_Npc1, MSGBOX_NPC
	end

KindleTrail_EventScript_Quest0::
	lock
	faceplayer
	goto_if_set FLAG_TOPAZE_QUEST_KINDLETRAIL, KindleTrail_EventScript_Quest0_After
	msgbox KindleTrail_Text_Quest0_Ask
	checkitem ITEM_PROTEIN, 1
	goto_if_eq VAR_RESULT, FALSE, KindleTrail_EventScript_Quest0_Miss
	checkitemspace ITEM_FOCUS_BAND, 1
	goto_if_eq VAR_RESULT, FALSE, KindleTrail_EventScript_Quest0_NoRoom
	removeitem ITEM_PROTEIN, 1
	giveitem ITEM_FOCUS_BAND, 1
	setflag FLAG_TOPAZE_QUEST_KINDLETRAIL
	msgbox KindleTrail_Text_Quest0_Done
	release
	end

KindleTrail_EventScript_Quest0_After::
	msgbox KindleTrail_Text_Quest0_AfterT
	release
	end

KindleTrail_EventScript_Quest0_Miss::
	msgbox KindleTrail_Text_Quest0_MissT
	release
	end

KindleTrail_EventScript_Quest0_NoRoom::
	msgbox KindleTrail_Text_Quest0_NoRoomT
	release
	end


@ Topaze: objets caches (panneaux a script, drapeaux hors plage moteur)
KindleTrail_EventScript_TopazeFind0::
	lock
	goto_if_set FLAG_TOPAZE_FIND_KINDLETRAIL_0, KindleTrail_EventScript_TopazeFind0_Done
	checkitemspace ITEM_BLACK_BELT, 1
	goto_if_eq VAR_RESULT, FALSE, KindleTrail_EventScript_TopazeFind0_Full
	giveitem ITEM_BLACK_BELT, 1
	setflag FLAG_TOPAZE_FIND_KINDLETRAIL_0
	release
	end

KindleTrail_EventScript_TopazeFind0_Done::
	release
	end

KindleTrail_EventScript_TopazeFind0_Full::
	msgbox KindleTrail_Text_TopazeFindFull
	release
	end

KindleTrail_EventScript_TopazeFind1::
	lock
	goto_if_set FLAG_TOPAZE_FIND_KINDLETRAIL_1, KindleTrail_EventScript_TopazeFind1_Done
	checkitemspace ITEM_PROTEIN, 1
	goto_if_eq VAR_RESULT, FALSE, KindleTrail_EventScript_TopazeFind1_Full
	giveitem ITEM_PROTEIN, 1
	setflag FLAG_TOPAZE_FIND_KINDLETRAIL_1
	release
	end

KindleTrail_EventScript_TopazeFind1_Done::
	release
	end

KindleTrail_EventScript_TopazeFind1_Full::
	msgbox KindleTrail_Text_TopazeFindFull
	release
	end

KindleTrail_EventScript_TopazeFind2::
	lock
	goto_if_set FLAG_TOPAZE_FIND_KINDLETRAIL_2, KindleTrail_EventScript_TopazeFind2_Done
	checkitemspace ITEM_X_ATTACK, 1
	goto_if_eq VAR_RESULT, FALSE, KindleTrail_EventScript_TopazeFind2_Full
	giveitem ITEM_X_ATTACK, 1
	setflag FLAG_TOPAZE_FIND_KINDLETRAIL_2
	release
	end

KindleTrail_EventScript_TopazeFind2_Done::
	release
	end

KindleTrail_EventScript_TopazeFind2_Full::
	msgbox KindleTrail_Text_TopazeFindFull
	release
	end

