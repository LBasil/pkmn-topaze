ThornyTrail_MapScripts::
	.byte 0

ThornyTrail_EventScript_ReturnFerry::
	lock
	faceplayer
	msgbox ThornyTrail_Text_ReturnAsk, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, ThornyTrail_EventScript_Stay
	warp MAP_FUCHSIA_CITY, 255, 24, 27
	waitstate
	end

ThornyTrail_EventScript_Stay::
	msgbox ThornyTrail_Text_Stay
	release
	end

ThornyTrail_EventScript_Npc0::
	msgbox ThornyTrail_Text_Npc0, MSGBOX_NPC
	end

ThornyTrail_EventScript_Npc1::
	msgbox ThornyTrail_Text_Npc1, MSGBOX_NPC
	end

ThornyTrail_EventScript_Quest0::
	lock
	faceplayer
	goto_if_set FLAG_TOPAZE_QUEST_THORNYTRAIL, ThornyTrail_EventScript_Quest0_After
	msgbox ThornyTrail_Text_Quest0_Ask
	checkitem ITEM_REVIVE, 1
	goto_if_eq VAR_RESULT, FALSE, ThornyTrail_EventScript_Quest0_Miss
	checkitemspace ITEM_POISON_BARB, 1
	goto_if_eq VAR_RESULT, FALSE, ThornyTrail_EventScript_Quest0_NoRoom
	removeitem ITEM_REVIVE, 1
	giveitem ITEM_POISON_BARB, 1
	setflag FLAG_TOPAZE_QUEST_THORNYTRAIL
	msgbox ThornyTrail_Text_Quest0_Done
	release
	end

ThornyTrail_EventScript_Quest0_After::
	msgbox ThornyTrail_Text_Quest0_AfterT
	release
	end

ThornyTrail_EventScript_Quest0_Miss::
	msgbox ThornyTrail_Text_Quest0_MissT
	release
	end

ThornyTrail_EventScript_Quest0_NoRoom::
	msgbox ThornyTrail_Text_Quest0_NoRoomT
	release
	end


@ Topaze: objets caches (panneaux a script, drapeaux hors plage moteur)
ThornyTrail_EventScript_TopazeFind0::
	lock
	goto_if_set FLAG_TOPAZE_FIND_THORNYTRAIL_0, ThornyTrail_EventScript_TopazeFind0_Done
	checkitemspace ITEM_MOON_STONE, 1
	goto_if_eq VAR_RESULT, FALSE, ThornyTrail_EventScript_TopazeFind0_Full
	giveitem ITEM_MOON_STONE, 1
	setflag FLAG_TOPAZE_FIND_THORNYTRAIL_0
	release
	end

ThornyTrail_EventScript_TopazeFind0_Done::
	release
	end

ThornyTrail_EventScript_TopazeFind0_Full::
	msgbox ThornyTrail_Text_TopazeFindFull
	release
	end

ThornyTrail_EventScript_TopazeFind1::
	lock
	goto_if_set FLAG_TOPAZE_FIND_THORNYTRAIL_1, ThornyTrail_EventScript_TopazeFind1_Done
	checkitemspace ITEM_POISON_BARB, 1
	goto_if_eq VAR_RESULT, FALSE, ThornyTrail_EventScript_TopazeFind1_Full
	giveitem ITEM_POISON_BARB, 1
	setflag FLAG_TOPAZE_FIND_THORNYTRAIL_1
	release
	end

ThornyTrail_EventScript_TopazeFind1_Done::
	release
	end

ThornyTrail_EventScript_TopazeFind1_Full::
	msgbox ThornyTrail_Text_TopazeFindFull
	release
	end

ThornyTrail_EventScript_TopazeFind2::
	lock
	goto_if_set FLAG_TOPAZE_FIND_THORNYTRAIL_2, ThornyTrail_EventScript_TopazeFind2_Done
	checkitemspace ITEM_REVIVE, 1
	goto_if_eq VAR_RESULT, FALSE, ThornyTrail_EventScript_TopazeFind2_Full
	giveitem ITEM_REVIVE, 1
	setflag FLAG_TOPAZE_FIND_THORNYTRAIL_2
	release
	end

ThornyTrail_EventScript_TopazeFind2_Done::
	release
	end

ThornyTrail_EventScript_TopazeFind2_Full::
	msgbox ThornyTrail_Text_TopazeFindFull
	release
	end

