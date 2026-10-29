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


@ Topaze: objets caches (panneaux a script, drapeaux hors plage moteur)
ZenGarden_EventScript_TopazeFind0::
	lock
	goto_if_set FLAG_TOPAZE_FIND_ZENGARDEN_0, ZenGarden_EventScript_TopazeFind0_Done
	checkitemspace ITEM_ELIXIR, 1
	goto_if_eq VAR_RESULT, FALSE, ZenGarden_EventScript_TopazeFind0_Full
	giveitem ITEM_ELIXIR, 1
	setflag FLAG_TOPAZE_FIND_ZENGARDEN_0
	release
	end

ZenGarden_EventScript_TopazeFind0_Done::
	release
	end

ZenGarden_EventScript_TopazeFind0_Full::
	msgbox ZenGarden_Text_TopazeFindFull
	release
	end

ZenGarden_EventScript_TopazeFind1::
	lock
	goto_if_set FLAG_TOPAZE_FIND_ZENGARDEN_1, ZenGarden_EventScript_TopazeFind1_Done
	checkitemspace ITEM_REVIVAL_HERB, 1
	goto_if_eq VAR_RESULT, FALSE, ZenGarden_EventScript_TopazeFind1_Full
	giveitem ITEM_REVIVAL_HERB, 1
	setflag FLAG_TOPAZE_FIND_ZENGARDEN_1
	release
	end

ZenGarden_EventScript_TopazeFind1_Done::
	release
	end

ZenGarden_EventScript_TopazeFind1_Full::
	msgbox ZenGarden_Text_TopazeFindFull
	release
	end

ZenGarden_EventScript_TopazeFind2::
	lock
	goto_if_set FLAG_TOPAZE_FIND_ZENGARDEN_2, ZenGarden_EventScript_TopazeFind2_Done
	checkitemspace ITEM_MENTAL_HERB, 1
	goto_if_eq VAR_RESULT, FALSE, ZenGarden_EventScript_TopazeFind2_Full
	giveitem ITEM_MENTAL_HERB, 1
	setflag FLAG_TOPAZE_FIND_ZENGARDEN_2
	release
	end

ZenGarden_EventScript_TopazeFind2_Done::
	release
	end

ZenGarden_EventScript_TopazeFind2_Full::
	msgbox ZenGarden_Text_TopazeFindFull
	release
	end


ZenGarden_Text_TopazeFindFull::
	.string "Something shines here, but your BAG\n"
	.string "is full.$"
