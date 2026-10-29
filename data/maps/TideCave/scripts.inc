TideCave_MapScripts::
	.byte 0

TideCave_EventScript_ReturnFerry::
	lock
	faceplayer
	msgbox TideCave_Text_ReturnAsk, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, TideCave_EventScript_Stay
	warp MAP_FUCHSIA_CITY, 255, 24, 27
	waitstate
	end

TideCave_EventScript_Stay::
	msgbox TideCave_Text_Stay
	release
	end

TideCave_EventScript_Npc0::
	msgbox TideCave_Text_Npc0, MSGBOX_NPC
	end

TideCave_EventScript_Npc1::
	msgbox TideCave_Text_Npc1, MSGBOX_NPC
	end

TideCave_EventScript_Quest0::
	lock
	faceplayer
	goto_if_set FLAG_TOPAZE_QUEST_TIDECAVE, TideCave_EventScript_Quest0_After
	msgbox TideCave_Text_Quest0_Ask
	checkitem ITEM_PEARL, 1
	goto_if_eq VAR_RESULT, FALSE, TideCave_EventScript_Quest0_Miss
	checkitemspace ITEM_MYSTIC_WATER, 1
	goto_if_eq VAR_RESULT, FALSE, TideCave_EventScript_Quest0_NoRoom
	removeitem ITEM_PEARL, 1
	giveitem ITEM_MYSTIC_WATER, 1
	setflag FLAG_TOPAZE_QUEST_TIDECAVE
	msgbox TideCave_Text_Quest0_Done
	release
	end

TideCave_EventScript_Quest0_After::
	msgbox TideCave_Text_Quest0_AfterT
	release
	end

TideCave_EventScript_Quest0_Miss::
	msgbox TideCave_Text_Quest0_MissT
	release
	end

TideCave_EventScript_Quest0_NoRoom::
	msgbox TideCave_Text_Quest0_NoRoomT
	release
	end


@ Topaze: objets caches (panneaux a script, drapeaux hors plage moteur)
TideCave_EventScript_TopazeFind0::
	lock
	goto_if_set FLAG_TOPAZE_FIND_TIDECAVE_0, TideCave_EventScript_TopazeFind0_Done
	checkitemspace ITEM_DEEP_SEA_TOOTH, 1
	goto_if_eq VAR_RESULT, FALSE, TideCave_EventScript_TopazeFind0_Full
	giveitem ITEM_DEEP_SEA_TOOTH, 1
	setflag FLAG_TOPAZE_FIND_TIDECAVE_0
	release
	end

TideCave_EventScript_TopazeFind0_Done::
	release
	end

TideCave_EventScript_TopazeFind0_Full::
	msgbox TideCave_Text_TopazeFindFull
	release
	end

TideCave_EventScript_TopazeFind1::
	lock
	goto_if_set FLAG_TOPAZE_FIND_TIDECAVE_1, TideCave_EventScript_TopazeFind1_Done
	checkitemspace ITEM_DEEP_SEA_SCALE, 1
	goto_if_eq VAR_RESULT, FALSE, TideCave_EventScript_TopazeFind1_Full
	giveitem ITEM_DEEP_SEA_SCALE, 1
	setflag FLAG_TOPAZE_FIND_TIDECAVE_1
	release
	end

TideCave_EventScript_TopazeFind1_Done::
	release
	end

TideCave_EventScript_TopazeFind1_Full::
	msgbox TideCave_Text_TopazeFindFull
	release
	end

TideCave_EventScript_TopazeFind2::
	lock
	goto_if_set FLAG_TOPAZE_FIND_TIDECAVE_2, TideCave_EventScript_TopazeFind2_Done
	checkitemspace ITEM_PEARL, 1
	goto_if_eq VAR_RESULT, FALSE, TideCave_EventScript_TopazeFind2_Full
	giveitem ITEM_PEARL, 1
	setflag FLAG_TOPAZE_FIND_TIDECAVE_2
	release
	end

TideCave_EventScript_TopazeFind2_Done::
	release
	end

TideCave_EventScript_TopazeFind2_Full::
	msgbox TideCave_Text_TopazeFindFull
	release
	end

