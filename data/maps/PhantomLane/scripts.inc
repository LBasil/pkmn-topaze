PhantomLane_MapScripts::
	.byte 0

PhantomLane_EventScript_ReturnFerry::
	lock
	faceplayer
	msgbox PhantomLane_Text_ReturnAsk, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, PhantomLane_EventScript_Stay
	warp MAP_FUCHSIA_CITY, 255, 24, 27
	waitstate
	end

PhantomLane_EventScript_Stay::
	msgbox PhantomLane_Text_Stay
	release
	end

PhantomLane_EventScript_Npc0::
	msgbox PhantomLane_Text_Npc0, MSGBOX_NPC
	end

PhantomLane_EventScript_Npc1::
	msgbox PhantomLane_Text_Npc1, MSGBOX_NPC
	end

PhantomLane_EventScript_Quest0::
	lock
	faceplayer
	goto_if_set FLAG_TOPAZE_QUEST_PHANTOMLANE, PhantomLane_EventScript_Quest0_After
	msgbox PhantomLane_Text_Quest0_Ask
	checkitem ITEM_MAX_REVIVE, 1
	goto_if_eq VAR_RESULT, FALSE, PhantomLane_EventScript_Quest0_Miss
	checkitemspace ITEM_SPELL_TAG, 1
	goto_if_eq VAR_RESULT, FALSE, PhantomLane_EventScript_Quest0_NoRoom
	removeitem ITEM_MAX_REVIVE, 1
	giveitem ITEM_SPELL_TAG, 1
	setflag FLAG_TOPAZE_QUEST_PHANTOMLANE
	msgbox PhantomLane_Text_Quest0_Done
	release
	end

PhantomLane_EventScript_Quest0_After::
	msgbox PhantomLane_Text_Quest0_AfterT
	release
	end

PhantomLane_EventScript_Quest0_Miss::
	msgbox PhantomLane_Text_Quest0_MissT
	release
	end

PhantomLane_EventScript_Quest0_NoRoom::
	msgbox PhantomLane_Text_Quest0_NoRoomT
	release
	end


@ Topaze: objets caches (panneaux a script, drapeaux hors plage moteur)
PhantomLane_EventScript_TopazeFind0::
	lock
	goto_if_set FLAG_TOPAZE_FIND_PHANTOMLANE_0, PhantomLane_EventScript_TopazeFind0_Done
	checkitemspace ITEM_SPELL_TAG, 1
	goto_if_eq VAR_RESULT, FALSE, PhantomLane_EventScript_TopazeFind0_Full
	giveitem ITEM_SPELL_TAG, 1
	setflag FLAG_TOPAZE_FIND_PHANTOMLANE_0
	release
	end

PhantomLane_EventScript_TopazeFind0_Done::
	release
	end

PhantomLane_EventScript_TopazeFind0_Full::
	msgbox PhantomLane_Text_TopazeFindFull
	release
	end

PhantomLane_EventScript_TopazeFind1::
	lock
	goto_if_set FLAG_TOPAZE_FIND_PHANTOMLANE_1, PhantomLane_EventScript_TopazeFind1_Done
	checkitemspace ITEM_BLACK_GLASSES, 1
	goto_if_eq VAR_RESULT, FALSE, PhantomLane_EventScript_TopazeFind1_Full
	giveitem ITEM_BLACK_GLASSES, 1
	setflag FLAG_TOPAZE_FIND_PHANTOMLANE_1
	release
	end

PhantomLane_EventScript_TopazeFind1_Done::
	release
	end

PhantomLane_EventScript_TopazeFind1_Full::
	msgbox PhantomLane_Text_TopazeFindFull
	release
	end

PhantomLane_EventScript_TopazeFind2::
	lock
	goto_if_set FLAG_TOPAZE_FIND_PHANTOMLANE_2, PhantomLane_EventScript_TopazeFind2_Done
	checkitemspace ITEM_MAX_REVIVE, 1
	goto_if_eq VAR_RESULT, FALSE, PhantomLane_EventScript_TopazeFind2_Full
	giveitem ITEM_MAX_REVIVE, 1
	setflag FLAG_TOPAZE_FIND_PHANTOMLANE_2
	release
	end

PhantomLane_EventScript_TopazeFind2_Done::
	release
	end

PhantomLane_EventScript_TopazeFind2_Full::
	msgbox PhantomLane_Text_TopazeFindFull
	release
	end

