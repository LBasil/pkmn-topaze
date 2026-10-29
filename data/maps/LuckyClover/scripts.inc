LuckyClover_MapScripts::
	.byte 0

LuckyClover_EventScript_ReturnFerry::
	lock
	faceplayer
	msgbox LuckyClover_Text_ReturnAsk, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, LuckyClover_EventScript_Stay
	warp MAP_FUCHSIA_CITY, 255, 24, 27
	waitstate
	end

LuckyClover_EventScript_Stay::
	msgbox LuckyClover_Text_Stay
	release
	end

LuckyClover_EventScript_Npc0::
	msgbox LuckyClover_Text_Npc0, MSGBOX_NPC
	end

LuckyClover_EventScript_Npc1::
	msgbox LuckyClover_Text_Npc1, MSGBOX_NPC
	end

LuckyClover_EventScript_Quest0::
	lock
	faceplayer
	goto_if_set FLAG_TOPAZE_QUEST_LUCKYCLOVER, LuckyClover_EventScript_Quest0_After
	msgbox LuckyClover_Text_Quest0_Ask
	checkitem ITEM_POKE_BALL, 3
	goto_if_eq VAR_RESULT, FALSE, LuckyClover_EventScript_Quest0_Miss
	checkitemspace ITEM_SILK_SCARF, 1
	goto_if_eq VAR_RESULT, FALSE, LuckyClover_EventScript_Quest0_NoRoom
	removeitem ITEM_POKE_BALL, 3
	giveitem ITEM_SILK_SCARF, 1
	setflag FLAG_TOPAZE_QUEST_LUCKYCLOVER
	msgbox LuckyClover_Text_Quest0_Done
	release
	end

LuckyClover_EventScript_Quest0_After::
	msgbox LuckyClover_Text_Quest0_AfterT
	release
	end

LuckyClover_EventScript_Quest0_Miss::
	msgbox LuckyClover_Text_Quest0_MissT
	release
	end

LuckyClover_EventScript_Quest0_NoRoom::
	msgbox LuckyClover_Text_Quest0_NoRoomT
	release
	end


@ Topaze: objets caches (panneaux a script, drapeaux hors plage moteur)
LuckyClover_EventScript_TopazeFind0::
	lock
	goto_if_set FLAG_TOPAZE_FIND_LUCKYCLOVER_0, LuckyClover_EventScript_TopazeFind0_Done
	checkitemspace ITEM_POKE_BALL, 1
	goto_if_eq VAR_RESULT, FALSE, LuckyClover_EventScript_TopazeFind0_Full
	giveitem ITEM_POKE_BALL, 1
	setflag FLAG_TOPAZE_FIND_LUCKYCLOVER_0
	release
	end

LuckyClover_EventScript_TopazeFind0_Done::
	release
	end

LuckyClover_EventScript_TopazeFind0_Full::
	msgbox LuckyClover_Text_TopazeFindFull
	release
	end

LuckyClover_EventScript_TopazeFind1::
	lock
	goto_if_set FLAG_TOPAZE_FIND_LUCKYCLOVER_1, LuckyClover_EventScript_TopazeFind1_Done
	checkitemspace ITEM_GREAT_BALL, 1
	goto_if_eq VAR_RESULT, FALSE, LuckyClover_EventScript_TopazeFind1_Full
	giveitem ITEM_GREAT_BALL, 1
	setflag FLAG_TOPAZE_FIND_LUCKYCLOVER_1
	release
	end

LuckyClover_EventScript_TopazeFind1_Done::
	release
	end

LuckyClover_EventScript_TopazeFind1_Full::
	msgbox LuckyClover_Text_TopazeFindFull
	release
	end

LuckyClover_EventScript_TopazeFind2::
	lock
	goto_if_set FLAG_TOPAZE_FIND_LUCKYCLOVER_2, LuckyClover_EventScript_TopazeFind2_Done
	checkitemspace ITEM_POTION, 1
	goto_if_eq VAR_RESULT, FALSE, LuckyClover_EventScript_TopazeFind2_Full
	giveitem ITEM_POTION, 1
	setflag FLAG_TOPAZE_FIND_LUCKYCLOVER_2
	release
	end

LuckyClover_EventScript_TopazeFind2_Done::
	release
	end

LuckyClover_EventScript_TopazeFind2_Full::
	msgbox LuckyClover_Text_TopazeFindFull
	release
	end

