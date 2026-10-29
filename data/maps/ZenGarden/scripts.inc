ZenGarden_MapScripts::
	.byte 0

ZenGarden_EventScript_ReturnFerry::
	lock
	faceplayer
	msgbox ZenGarden_Text_ReturnAsk, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, ZenGarden_EventScript_Stay
	warp MAP_FUCHSIA_CITY, 255, 24, 27
	waitstate
	end

ZenGarden_EventScript_Stay::
	msgbox ZenGarden_Text_Stay
	release
	end

ZenGarden_EventScript_Npc0::
	msgbox ZenGarden_Text_Npc0, MSGBOX_NPC
	end

ZenGarden_EventScript_Npc1::
	msgbox ZenGarden_Text_Npc1, MSGBOX_NPC
	end

ZenGarden_EventScript_Quest0::
	lock
	faceplayer
	goto_if_set FLAG_TOPAZE_QUEST_ZENGARDEN, ZenGarden_EventScript_Quest0_After
	msgbox ZenGarden_Text_Quest0_Ask
	checkitem ITEM_LEMONADE, 2
	goto_if_eq VAR_RESULT, FALSE, ZenGarden_EventScript_Quest0_Miss
	checkitemspace ITEM_TWISTED_SPOON, 1
	goto_if_eq VAR_RESULT, FALSE, ZenGarden_EventScript_Quest0_NoRoom
	removeitem ITEM_LEMONADE, 2
	giveitem ITEM_TWISTED_SPOON, 1
	setflag FLAG_TOPAZE_QUEST_ZENGARDEN
	msgbox ZenGarden_Text_Quest0_Done
	release
	end

ZenGarden_EventScript_Quest0_After::
	msgbox ZenGarden_Text_Quest0_AfterT
	release
	end

ZenGarden_EventScript_Quest0_Miss::
	msgbox ZenGarden_Text_Quest0_MissT
	release
	end

ZenGarden_EventScript_Quest0_NoRoom::
	msgbox ZenGarden_Text_Quest0_NoRoomT
	release
	end

