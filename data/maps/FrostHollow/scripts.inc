FrostHollow_MapScripts::
	.byte 0

FrostHollow_EventScript_ReturnFerry::
	lock
	faceplayer
	msgbox FrostHollow_Text_ReturnAsk, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, FrostHollow_EventScript_Stay
	warp MAP_FUCHSIA_CITY, 255, 24, 27
	waitstate
	end

FrostHollow_EventScript_Stay::
	msgbox FrostHollow_Text_Stay
	release
	end

FrostHollow_EventScript_Npc0::
	msgbox FrostHollow_Text_Npc0, MSGBOX_NPC
	end

FrostHollow_EventScript_Npc1::
	msgbox FrostHollow_Text_Npc1, MSGBOX_NPC
	end

FrostHollow_EventScript_Quest0::
	lock
	faceplayer
	goto_if_set FLAG_TOPAZE_QUEST_FROSTHOLLOW, FrostHollow_EventScript_Quest0_After
	msgbox FrostHollow_Text_Quest0_Ask
	checkitem ITEM_BURN_HEAL, 2
	goto_if_eq VAR_RESULT, FALSE, FrostHollow_EventScript_Quest0_Miss
	checkitemspace ITEM_NEVER_MELT_ICE, 1
	goto_if_eq VAR_RESULT, FALSE, FrostHollow_EventScript_Quest0_NoRoom
	removeitem ITEM_BURN_HEAL, 2
	giveitem ITEM_NEVER_MELT_ICE, 1
	setflag FLAG_TOPAZE_QUEST_FROSTHOLLOW
	msgbox FrostHollow_Text_Quest0_Done
	release
	end

FrostHollow_EventScript_Quest0_After::
	msgbox FrostHollow_Text_Quest0_AfterT
	release
	end

FrostHollow_EventScript_Quest0_Miss::
	msgbox FrostHollow_Text_Quest0_MissT
	release
	end

FrostHollow_EventScript_Quest0_NoRoom::
	msgbox FrostHollow_Text_Quest0_NoRoomT
	release
	end


@ Topaze: objets caches (panneaux a script, drapeaux hors plage moteur)
FrostHollow_EventScript_TopazeFind0::
	lock
	goto_if_set FLAG_TOPAZE_FIND_FROSTHOLLOW_0, FrostHollow_EventScript_TopazeFind0_Done
	checkitemspace ITEM_ELIXIR, 1
	goto_if_eq VAR_RESULT, FALSE, FrostHollow_EventScript_TopazeFind0_Full
	giveitem ITEM_ELIXIR, 1
	setflag FLAG_TOPAZE_FIND_FROSTHOLLOW_0
	release
	end

FrostHollow_EventScript_TopazeFind0_Done::
	release
	end

FrostHollow_EventScript_TopazeFind0_Full::
	msgbox FrostHollow_Text_TopazeFindFull
	release
	end

FrostHollow_EventScript_TopazeFind1::
	lock
	goto_if_set FLAG_TOPAZE_FIND_FROSTHOLLOW_1, FrostHollow_EventScript_TopazeFind1_Done
	checkitemspace ITEM_MAX_ETHER, 1
	goto_if_eq VAR_RESULT, FALSE, FrostHollow_EventScript_TopazeFind1_Full
	giveitem ITEM_MAX_ETHER, 1
	setflag FLAG_TOPAZE_FIND_FROSTHOLLOW_1
	release
	end

FrostHollow_EventScript_TopazeFind1_Done::
	release
	end

FrostHollow_EventScript_TopazeFind1_Full::
	msgbox FrostHollow_Text_TopazeFindFull
	release
	end

FrostHollow_EventScript_TopazeFind2::
	lock
	goto_if_set FLAG_TOPAZE_FIND_FROSTHOLLOW_2, FrostHollow_EventScript_TopazeFind2_Done
	checkitemspace ITEM_REVIVE, 1
	goto_if_eq VAR_RESULT, FALSE, FrostHollow_EventScript_TopazeFind2_Full
	giveitem ITEM_REVIVE, 1
	setflag FLAG_TOPAZE_FIND_FROSTHOLLOW_2
	release
	end

FrostHollow_EventScript_TopazeFind2_Done::
	release
	end

FrostHollow_EventScript_TopazeFind2_Full::
	msgbox FrostHollow_Text_TopazeFindFull
	release
	end


FrostHollow_Text_TopazeFindFull::
	.string "Something shines here, but your BAG\n"
	.string "is full.$"
