DragonPerch_MapScripts::
	.byte 0

DragonPerch_EventScript_ReturnFerry::
	lock
	faceplayer
	msgbox DragonPerch_Text_ReturnAsk, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, DragonPerch_EventScript_Stay
	warp MAP_FUCHSIA_CITY, 255, 24, 27
	waitstate
	end

DragonPerch_EventScript_Stay::
	msgbox DragonPerch_Text_Stay
	release
	end

DragonPerch_EventScript_Npc0::
	msgbox DragonPerch_Text_Npc0, MSGBOX_NPC
	end

DragonPerch_EventScript_Quest0::
	lock
	faceplayer
	goto_if_set FLAG_TOPAZE_QUEST_DRAGONPERCH, DragonPerch_EventScript_Quest0_After
	msgbox DragonPerch_Text_Quest0_Ask
	checkitem ITEM_DRAGON_SCALE, 1
	goto_if_eq VAR_RESULT, FALSE, DragonPerch_EventScript_Quest0_Miss
	checkitemspace ITEM_DRAGON_FANG, 1
	goto_if_eq VAR_RESULT, FALSE, DragonPerch_EventScript_Quest0_NoRoom
	removeitem ITEM_DRAGON_SCALE, 1
	giveitem ITEM_DRAGON_FANG, 1
	setflag FLAG_TOPAZE_QUEST_DRAGONPERCH
	msgbox DragonPerch_Text_Quest0_Done
	release
	end

DragonPerch_EventScript_Quest0_After::
	msgbox DragonPerch_Text_Quest0_AfterT
	release
	end

DragonPerch_EventScript_Quest0_Miss::
	msgbox DragonPerch_Text_Quest0_MissT
	release
	end

DragonPerch_EventScript_Quest0_NoRoom::
	msgbox DragonPerch_Text_Quest0_NoRoomT
	release
	end

