MirrorPond_MapScripts::
	.byte 0

MirrorPond_EventScript_ReturnFerry::
	lock
	faceplayer
	msgbox MirrorPond_Text_ReturnAsk, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, MirrorPond_EventScript_Stay
	warp MAP_FUCHSIA_CITY, 255, 24, 27
	waitstate
	end

MirrorPond_EventScript_Stay::
	msgbox MirrorPond_Text_Stay
	release
	end

MirrorPond_EventScript_Npc0::
	msgbox MirrorPond_Text_Npc0, MSGBOX_NPC
	end

MirrorPond_EventScript_Npc1::
	msgbox MirrorPond_Text_Npc1, MSGBOX_NPC
	end

MirrorPond_EventScript_Quest0::
	lock
	faceplayer
	goto_if_set FLAG_TOPAZE_QUEST_MIRRORPOND, MirrorPond_EventScript_Quest0_After
	msgbox MirrorPond_Text_Quest0_Ask
	checkitem ITEM_WATER_STONE, 1
	goto_if_eq VAR_RESULT, FALSE, MirrorPond_EventScript_Quest0_Miss
	checkitemspace ITEM_MYSTIC_WATER, 1
	goto_if_eq VAR_RESULT, FALSE, MirrorPond_EventScript_Quest0_NoRoom
	removeitem ITEM_WATER_STONE, 1
	giveitem ITEM_MYSTIC_WATER, 1
	setflag FLAG_TOPAZE_QUEST_MIRRORPOND
	msgbox MirrorPond_Text_Quest0_Done
	release
	end

MirrorPond_EventScript_Quest0_After::
	msgbox MirrorPond_Text_Quest0_AfterT
	release
	end

MirrorPond_EventScript_Quest0_Miss::
	msgbox MirrorPond_Text_Quest0_MissT
	release
	end

MirrorPond_EventScript_Quest0_NoRoom::
	msgbox MirrorPond_Text_Quest0_NoRoomT
	release
	end


@ Topaze: objets caches (panneaux a script, drapeaux hors plage moteur)
MirrorPond_EventScript_TopazeFind0::
	lock
	goto_if_set FLAG_TOPAZE_FIND_MIRRORPOND_0, MirrorPond_EventScript_TopazeFind0_Done
	checkitemspace ITEM_WATER_STONE, 1
	goto_if_eq VAR_RESULT, FALSE, MirrorPond_EventScript_TopazeFind0_Full
	giveitem ITEM_WATER_STONE, 1
	setflag FLAG_TOPAZE_FIND_MIRRORPOND_0
	release
	end

MirrorPond_EventScript_TopazeFind0_Done::
	release
	end

MirrorPond_EventScript_TopazeFind0_Full::
	msgbox MirrorPond_Text_TopazeFindFull
	release
	end

MirrorPond_EventScript_TopazeFind1::
	lock
	goto_if_set FLAG_TOPAZE_FIND_MIRRORPOND_1, MirrorPond_EventScript_TopazeFind1_Done
	checkitemspace ITEM_MYSTIC_WATER, 1
	goto_if_eq VAR_RESULT, FALSE, MirrorPond_EventScript_TopazeFind1_Full
	giveitem ITEM_MYSTIC_WATER, 1
	setflag FLAG_TOPAZE_FIND_MIRRORPOND_1
	release
	end

MirrorPond_EventScript_TopazeFind1_Done::
	release
	end

MirrorPond_EventScript_TopazeFind1_Full::
	msgbox MirrorPond_Text_TopazeFindFull
	release
	end

MirrorPond_EventScript_TopazeFind2::
	lock
	goto_if_set FLAG_TOPAZE_FIND_MIRRORPOND_2, MirrorPond_EventScript_TopazeFind2_Done
	checkitemspace ITEM_MAX_POTION, 1
	goto_if_eq VAR_RESULT, FALSE, MirrorPond_EventScript_TopazeFind2_Full
	giveitem ITEM_MAX_POTION, 1
	setflag FLAG_TOPAZE_FIND_MIRRORPOND_2
	release
	end

MirrorPond_EventScript_TopazeFind2_Done::
	release
	end

MirrorPond_EventScript_TopazeFind2_Full::
	msgbox MirrorPond_Text_TopazeFindFull
	release
	end

