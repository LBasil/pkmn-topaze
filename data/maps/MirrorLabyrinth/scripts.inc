MirrorLabyrinth_MapScripts::
	.byte 0

MirrorLabyrinth_EventScript_ReturnFerry::
	lock
	faceplayer
	msgbox MirrorLabyrinth_Text_ReturnAsk, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, MirrorLabyrinth_EventScript_Stay
	warp MAP_FUCHSIA_CITY, 255, 24, 27
	waitstate
	end

MirrorLabyrinth_EventScript_Stay::
	msgbox MirrorLabyrinth_Text_Stay
	release
	end

MirrorLabyrinth_EventScript_Npc0::
	msgbox MirrorLabyrinth_Text_Npc0, MSGBOX_NPC
	end

MirrorLabyrinth_EventScript_Npc1::
	msgbox MirrorLabyrinth_Text_Npc1, MSGBOX_NPC
	end

MirrorLabyrinth_EventScript_Quest0::
	lock
	faceplayer
	goto_if_set FLAG_TOPAZE_QUEST_MIRRORLABYRINTH, MirrorLabyrinth_EventScript_Quest0_After
	msgbox MirrorLabyrinth_Text_Quest0_Ask
	checkitem ITEM_WATER_STONE, 1
	goto_if_eq VAR_RESULT, FALSE, MirrorLabyrinth_EventScript_Quest0_Miss
	checkitemspace ITEM_MIRACLE_SEED, 1
	goto_if_eq VAR_RESULT, FALSE, MirrorLabyrinth_EventScript_Quest0_NoRoom
	removeitem ITEM_WATER_STONE, 1
	giveitem ITEM_MIRACLE_SEED, 1
	setflag FLAG_TOPAZE_QUEST_MIRRORLABYRINTH
	msgbox MirrorLabyrinth_Text_Quest0_Done
	release
	end

MirrorLabyrinth_EventScript_Quest0_After::
	msgbox MirrorLabyrinth_Text_Quest0_AfterT
	release
	end

MirrorLabyrinth_EventScript_Quest0_Miss::
	msgbox MirrorLabyrinth_Text_Quest0_MissT
	release
	end

MirrorLabyrinth_EventScript_Quest0_NoRoom::
	msgbox MirrorLabyrinth_Text_Quest0_NoRoomT
	release
	end


@ Topaze: objets caches (panneaux a script, drapeaux hors plage moteur)
MirrorLabyrinth_EventScript_TopazeFind0::
	lock
	goto_if_set FLAG_TOPAZE_FIND_MIRRORLABYRINTH_0, MirrorLabyrinth_EventScript_TopazeFind0_Done
	checkitemspace ITEM_MYSTIC_WATER, 1
	goto_if_eq VAR_RESULT, FALSE, MirrorLabyrinth_EventScript_TopazeFind0_Full
	giveitem ITEM_MYSTIC_WATER, 1
	setflag FLAG_TOPAZE_FIND_MIRRORLABYRINTH_0
	release
	end

MirrorLabyrinth_EventScript_TopazeFind0_Done::
	release
	end

MirrorLabyrinth_EventScript_TopazeFind0_Full::
	msgbox MirrorLabyrinth_Text_TopazeFindFull
	release
	end

MirrorLabyrinth_EventScript_TopazeFind1::
	lock
	goto_if_set FLAG_TOPAZE_FIND_MIRRORLABYRINTH_1, MirrorLabyrinth_EventScript_TopazeFind1_Done
	checkitemspace ITEM_WATER_STONE, 1
	goto_if_eq VAR_RESULT, FALSE, MirrorLabyrinth_EventScript_TopazeFind1_Full
	giveitem ITEM_WATER_STONE, 1
	setflag FLAG_TOPAZE_FIND_MIRRORLABYRINTH_1
	release
	end

MirrorLabyrinth_EventScript_TopazeFind1_Done::
	release
	end

MirrorLabyrinth_EventScript_TopazeFind1_Full::
	msgbox MirrorLabyrinth_Text_TopazeFindFull
	release
	end

MirrorLabyrinth_EventScript_TopazeFind2::
	lock
	goto_if_set FLAG_TOPAZE_FIND_MIRRORLABYRINTH_2, MirrorLabyrinth_EventScript_TopazeFind2_Done
	checkitemspace ITEM_HEART_SCALE, 1
	goto_if_eq VAR_RESULT, FALSE, MirrorLabyrinth_EventScript_TopazeFind2_Full
	giveitem ITEM_HEART_SCALE, 1
	setflag FLAG_TOPAZE_FIND_MIRRORLABYRINTH_2
	release
	end

MirrorLabyrinth_EventScript_TopazeFind2_Done::
	release
	end

MirrorLabyrinth_EventScript_TopazeFind2_Full::
	msgbox MirrorLabyrinth_Text_TopazeFindFull
	release
	end

