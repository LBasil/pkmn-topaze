OutcastShore_MapScripts::
	.byte 0

OutcastShore_EventScript_ReturnFerry::
	lock
	faceplayer
	msgbox OutcastShore_Text_ReturnAsk, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, OutcastShore_EventScript_Stay
	warp MAP_FUCHSIA_CITY, 255, 24, 27
	waitstate
	end

OutcastShore_EventScript_Stay::
	msgbox OutcastShore_Text_Stay
	release
	end

OutcastShore_EventScript_Npc0::
	msgbox OutcastShore_Text_Npc0, MSGBOX_NPC
	end

OutcastShore_EventScript_Npc1::
	msgbox OutcastShore_Text_Npc1, MSGBOX_NPC
	end

OutcastShore_EventScript_Quest0::
	lock
	faceplayer
	goto_if_set FLAG_TOPAZE_QUEST_OUTCASTSHORE, OutcastShore_EventScript_Quest0_After
	msgbox OutcastShore_Text_Quest0_Ask
	checkitem ITEM_MAX_REPEL, 1
	goto_if_eq VAR_RESULT, FALSE, OutcastShore_EventScript_Quest0_Miss
	checkitemspace ITEM_SOUL_DEW, 1
	goto_if_eq VAR_RESULT, FALSE, OutcastShore_EventScript_Quest0_NoRoom
	removeitem ITEM_MAX_REPEL, 1
	giveitem ITEM_SOUL_DEW, 1
	setflag FLAG_TOPAZE_QUEST_OUTCASTSHORE
	msgbox OutcastShore_Text_Quest0_Done
	release
	end

OutcastShore_EventScript_Quest0_After::
	msgbox OutcastShore_Text_Quest0_AfterT
	release
	end

OutcastShore_EventScript_Quest0_Miss::
	msgbox OutcastShore_Text_Quest0_MissT
	release
	end

OutcastShore_EventScript_Quest0_NoRoom::
	msgbox OutcastShore_Text_Quest0_NoRoomT
	release
	end


@ Topaze: objets caches (panneaux a script, drapeaux hors plage moteur)
OutcastShore_EventScript_TopazeFind0::
	lock
	goto_if_set FLAG_TOPAZE_FIND_OUTCASTSHORE_0, OutcastShore_EventScript_TopazeFind0_Done
	checkitemspace ITEM_SOUL_DEW, 1
	goto_if_eq VAR_RESULT, FALSE, OutcastShore_EventScript_TopazeFind0_Full
	giveitem ITEM_SOUL_DEW, 1
	setflag FLAG_TOPAZE_FIND_OUTCASTSHORE_0
	release
	end

OutcastShore_EventScript_TopazeFind0_Done::
	release
	end

OutcastShore_EventScript_TopazeFind0_Full::
	msgbox OutcastShore_Text_TopazeFindFull
	release
	end

OutcastShore_EventScript_TopazeFind1::
	lock
	goto_if_set FLAG_TOPAZE_FIND_OUTCASTSHORE_1, OutcastShore_EventScript_TopazeFind1_Done
	checkitemspace ITEM_MAX_REPEL, 1
	goto_if_eq VAR_RESULT, FALSE, OutcastShore_EventScript_TopazeFind1_Full
	giveitem ITEM_MAX_REPEL, 1
	setflag FLAG_TOPAZE_FIND_OUTCASTSHORE_1
	release
	end

OutcastShore_EventScript_TopazeFind1_Done::
	release
	end

OutcastShore_EventScript_TopazeFind1_Full::
	msgbox OutcastShore_Text_TopazeFindFull
	release
	end

OutcastShore_EventScript_TopazeFind2::
	lock
	goto_if_set FLAG_TOPAZE_FIND_OUTCASTSHORE_2, OutcastShore_EventScript_TopazeFind2_Done
	checkitemspace ITEM_MAX_ELIXIR, 1
	goto_if_eq VAR_RESULT, FALSE, OutcastShore_EventScript_TopazeFind2_Full
	giveitem ITEM_MAX_ELIXIR, 1
	setflag FLAG_TOPAZE_FIND_OUTCASTSHORE_2
	release
	end

OutcastShore_EventScript_TopazeFind2_Done::
	release
	end

OutcastShore_EventScript_TopazeFind2_Full::
	msgbox OutcastShore_Text_TopazeFindFull
	release
	end

