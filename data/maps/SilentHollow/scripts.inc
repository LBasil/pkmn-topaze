SilentHollow_MapScripts::
	.byte 0

SilentHollow_EventScript_ReturnFerry::
	lock
	faceplayer
	msgbox SilentHollow_Text_ReturnAsk, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, SilentHollow_EventScript_Stay
	warp MAP_FUCHSIA_CITY, 255, 24, 27
	waitstate
	end

SilentHollow_EventScript_Stay::
	msgbox SilentHollow_Text_Stay
	release
	end

SilentHollow_EventScript_Npc0::
	msgbox SilentHollow_Text_Npc0, MSGBOX_NPC
	end

SilentHollow_EventScript_Npc1::
	msgbox SilentHollow_Text_Npc1, MSGBOX_NPC
	end

SilentHollow_EventScript_Quest0::
	lock
	faceplayer
	goto_if_set FLAG_TOPAZE_QUEST_SILENTHOLLOW, SilentHollow_EventScript_Quest0_After
	msgbox SilentHollow_Text_Quest0_Ask
	checkitem ITEM_MAX_ELIXIR, 1
	goto_if_eq VAR_RESULT, FALSE, SilentHollow_EventScript_Quest0_Miss
	checkitemspace ITEM_SPELL_TAG, 1
	goto_if_eq VAR_RESULT, FALSE, SilentHollow_EventScript_Quest0_NoRoom
	removeitem ITEM_MAX_ELIXIR, 1
	giveitem ITEM_SPELL_TAG, 1
	setflag FLAG_TOPAZE_QUEST_SILENTHOLLOW
	msgbox SilentHollow_Text_Quest0_Done
	release
	end

SilentHollow_EventScript_Quest0_After::
	msgbox SilentHollow_Text_Quest0_AfterT
	release
	end

SilentHollow_EventScript_Quest0_Miss::
	msgbox SilentHollow_Text_Quest0_MissT
	release
	end

SilentHollow_EventScript_Quest0_NoRoom::
	msgbox SilentHollow_Text_Quest0_NoRoomT
	release
	end


@ Topaze: objets caches (panneaux a script, drapeaux hors plage moteur)
SilentHollow_EventScript_TopazeFind0::
	lock
	goto_if_set FLAG_TOPAZE_FIND_SILENTHOLLOW_0, SilentHollow_EventScript_TopazeFind0_Done
	checkitemspace ITEM_SPELL_TAG, 1
	goto_if_eq VAR_RESULT, FALSE, SilentHollow_EventScript_TopazeFind0_Full
	giveitem ITEM_SPELL_TAG, 1
	setflag FLAG_TOPAZE_FIND_SILENTHOLLOW_0
	release
	end

SilentHollow_EventScript_TopazeFind0_Done::
	release
	end

SilentHollow_EventScript_TopazeFind0_Full::
	msgbox SilentHollow_Text_TopazeFindFull
	release
	end

SilentHollow_EventScript_TopazeFind1::
	lock
	goto_if_set FLAG_TOPAZE_FIND_SILENTHOLLOW_1, SilentHollow_EventScript_TopazeFind1_Done
	checkitemspace ITEM_BLACK_GLASSES, 1
	goto_if_eq VAR_RESULT, FALSE, SilentHollow_EventScript_TopazeFind1_Full
	giveitem ITEM_BLACK_GLASSES, 1
	setflag FLAG_TOPAZE_FIND_SILENTHOLLOW_1
	release
	end

SilentHollow_EventScript_TopazeFind1_Done::
	release
	end

SilentHollow_EventScript_TopazeFind1_Full::
	msgbox SilentHollow_Text_TopazeFindFull
	release
	end

SilentHollow_EventScript_TopazeFind2::
	lock
	goto_if_set FLAG_TOPAZE_FIND_SILENTHOLLOW_2, SilentHollow_EventScript_TopazeFind2_Done
	checkitemspace ITEM_MAX_ELIXIR, 1
	goto_if_eq VAR_RESULT, FALSE, SilentHollow_EventScript_TopazeFind2_Full
	giveitem ITEM_MAX_ELIXIR, 1
	setflag FLAG_TOPAZE_FIND_SILENTHOLLOW_2
	release
	end

SilentHollow_EventScript_TopazeFind2_Done::
	release
	end

SilentHollow_EventScript_TopazeFind2_Full::
	msgbox SilentHollow_Text_TopazeFindFull
	release
	end

