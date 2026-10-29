FrozenMarsh_MapScripts::
	.byte 0

FrozenMarsh_EventScript_ReturnFerry::
	lock
	faceplayer
	msgbox FrozenMarsh_Text_ReturnAsk, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, FrozenMarsh_EventScript_Stay
	warp MAP_FUCHSIA_CITY, 255, 24, 27
	waitstate
	end

FrozenMarsh_EventScript_Stay::
	msgbox FrozenMarsh_Text_Stay
	release
	end

FrozenMarsh_EventScript_Npc0::
	msgbox FrozenMarsh_Text_Npc0, MSGBOX_NPC
	end

FrozenMarsh_EventScript_Npc1::
	msgbox FrozenMarsh_Text_Npc1, MSGBOX_NPC
	end

FrozenMarsh_EventScript_Quest0::
	lock
	faceplayer
	goto_if_set FLAG_TOPAZE_QUEST_FROZENMARSH, FrozenMarsh_EventScript_Quest0_After
	msgbox FrozenMarsh_Text_Quest0_Ask
	checkitem ITEM_PEARL, 1
	goto_if_eq VAR_RESULT, FALSE, FrozenMarsh_EventScript_Quest0_Miss
	checkitemspace ITEM_NEVER_MELT_ICE, 1
	goto_if_eq VAR_RESULT, FALSE, FrozenMarsh_EventScript_Quest0_NoRoom
	removeitem ITEM_PEARL, 1
	giveitem ITEM_NEVER_MELT_ICE, 1
	setflag FLAG_TOPAZE_QUEST_FROZENMARSH
	msgbox FrozenMarsh_Text_Quest0_Done
	release
	end

FrozenMarsh_EventScript_Quest0_After::
	msgbox FrozenMarsh_Text_Quest0_AfterT
	release
	end

FrozenMarsh_EventScript_Quest0_Miss::
	msgbox FrozenMarsh_Text_Quest0_MissT
	release
	end

FrozenMarsh_EventScript_Quest0_NoRoom::
	msgbox FrozenMarsh_Text_Quest0_NoRoomT
	release
	end


@ Topaze: objets caches (panneaux a script, drapeaux hors plage moteur)
FrozenMarsh_EventScript_TopazeFind0::
	lock
	goto_if_set FLAG_TOPAZE_FIND_FROZENMARSH_0, FrozenMarsh_EventScript_TopazeFind0_Done
	checkitemspace ITEM_NEVER_MELT_ICE, 1
	goto_if_eq VAR_RESULT, FALSE, FrozenMarsh_EventScript_TopazeFind0_Full
	giveitem ITEM_NEVER_MELT_ICE, 1
	setflag FLAG_TOPAZE_FIND_FROZENMARSH_0
	release
	end

FrozenMarsh_EventScript_TopazeFind0_Done::
	release
	end

FrozenMarsh_EventScript_TopazeFind0_Full::
	msgbox FrozenMarsh_Text_TopazeFindFull
	release
	end

FrozenMarsh_EventScript_TopazeFind1::
	lock
	goto_if_set FLAG_TOPAZE_FIND_FROZENMARSH_1, FrozenMarsh_EventScript_TopazeFind1_Done
	checkitemspace ITEM_PEARL, 1
	goto_if_eq VAR_RESULT, FALSE, FrozenMarsh_EventScript_TopazeFind1_Full
	giveitem ITEM_PEARL, 1
	setflag FLAG_TOPAZE_FIND_FROZENMARSH_1
	release
	end

FrozenMarsh_EventScript_TopazeFind1_Done::
	release
	end

FrozenMarsh_EventScript_TopazeFind1_Full::
	msgbox FrozenMarsh_Text_TopazeFindFull
	release
	end

FrozenMarsh_EventScript_TopazeFind2::
	lock
	goto_if_set FLAG_TOPAZE_FIND_FROZENMARSH_2, FrozenMarsh_EventScript_TopazeFind2_Done
	checkitemspace ITEM_MAX_ELIXIR, 1
	goto_if_eq VAR_RESULT, FALSE, FrozenMarsh_EventScript_TopazeFind2_Full
	giveitem ITEM_MAX_ELIXIR, 1
	setflag FLAG_TOPAZE_FIND_FROZENMARSH_2
	release
	end

FrozenMarsh_EventScript_TopazeFind2_Done::
	release
	end

FrozenMarsh_EventScript_TopazeFind2_Full::
	msgbox FrozenMarsh_Text_TopazeFindFull
	release
	end

