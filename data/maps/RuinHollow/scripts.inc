RuinHollow_MapScripts::
	.byte 0

RuinHollow_EventScript_ReturnFerry::
	lock
	faceplayer
	msgbox RuinHollow_Text_ReturnAsk, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, RuinHollow_EventScript_Stay
	warp MAP_FUCHSIA_CITY, 255, 24, 27
	waitstate
	end

RuinHollow_EventScript_Stay::
	msgbox RuinHollow_Text_Stay
	release
	end

RuinHollow_EventScript_Npc0::
	msgbox RuinHollow_Text_Npc0, MSGBOX_NPC
	end

RuinHollow_EventScript_Npc1::
	msgbox RuinHollow_Text_Npc1, MSGBOX_NPC
	end

RuinHollow_EventScript_Quest0::
	lock
	faceplayer
	goto_if_set FLAG_TOPAZE_QUEST_RUINHOLLOW, RuinHollow_EventScript_Quest0_After
	msgbox RuinHollow_Text_Quest0_Ask
	checkitem ITEM_ULTRA_BALL, 1
	goto_if_eq VAR_RESULT, FALSE, RuinHollow_EventScript_Quest0_Miss
	checkitemspace ITEM_SPELL_TAG, 1
	goto_if_eq VAR_RESULT, FALSE, RuinHollow_EventScript_Quest0_NoRoom
	removeitem ITEM_ULTRA_BALL, 1
	giveitem ITEM_SPELL_TAG, 1
	setflag FLAG_TOPAZE_QUEST_RUINHOLLOW
	msgbox RuinHollow_Text_Quest0_Done
	release
	end

RuinHollow_EventScript_Quest0_After::
	msgbox RuinHollow_Text_Quest0_AfterT
	release
	end

RuinHollow_EventScript_Quest0_Miss::
	msgbox RuinHollow_Text_Quest0_MissT
	release
	end

RuinHollow_EventScript_Quest0_NoRoom::
	msgbox RuinHollow_Text_Quest0_NoRoomT
	release
	end


@ Topaze: objets caches (panneaux a script, drapeaux hors plage moteur)
RuinHollow_EventScript_TopazeFind0::
	lock
	goto_if_set FLAG_TOPAZE_FIND_RUINHOLLOW_0, RuinHollow_EventScript_TopazeFind0_Done
	checkitemspace ITEM_SPELL_TAG, 1
	goto_if_eq VAR_RESULT, FALSE, RuinHollow_EventScript_TopazeFind0_Full
	giveitem ITEM_SPELL_TAG, 1
	setflag FLAG_TOPAZE_FIND_RUINHOLLOW_0
	release
	end

RuinHollow_EventScript_TopazeFind0_Done::
	release
	end

RuinHollow_EventScript_TopazeFind0_Full::
	msgbox RuinHollow_Text_TopazeFindFull
	release
	end

RuinHollow_EventScript_TopazeFind1::
	lock
	goto_if_set FLAG_TOPAZE_FIND_RUINHOLLOW_1, RuinHollow_EventScript_TopazeFind1_Done
	checkitemspace ITEM_TM30, 1
	goto_if_eq VAR_RESULT, FALSE, RuinHollow_EventScript_TopazeFind1_Full
	giveitem ITEM_TM30, 1
	setflag FLAG_TOPAZE_FIND_RUINHOLLOW_1
	release
	end

RuinHollow_EventScript_TopazeFind1_Done::
	release
	end

RuinHollow_EventScript_TopazeFind1_Full::
	msgbox RuinHollow_Text_TopazeFindFull
	release
	end

RuinHollow_EventScript_TopazeFind2::
	lock
	goto_if_set FLAG_TOPAZE_FIND_RUINHOLLOW_2, RuinHollow_EventScript_TopazeFind2_Done
	checkitemspace ITEM_ULTRA_BALL, 1
	goto_if_eq VAR_RESULT, FALSE, RuinHollow_EventScript_TopazeFind2_Full
	giveitem ITEM_ULTRA_BALL, 1
	setflag FLAG_TOPAZE_FIND_RUINHOLLOW_2
	release
	end

RuinHollow_EventScript_TopazeFind2_Done::
	release
	end

RuinHollow_EventScript_TopazeFind2_Full::
	msgbox RuinHollow_Text_TopazeFindFull
	release
	end

