BrightShallows_MapScripts::
	.byte 0

BrightShallows_EventScript_ReturnFerry::
	lock
	faceplayer
	msgbox BrightShallows_Text_ReturnAsk, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, BrightShallows_EventScript_Stay
	warp MAP_FUCHSIA_CITY, 255, 24, 27
	waitstate
	end

BrightShallows_EventScript_Stay::
	msgbox BrightShallows_Text_Stay
	release
	end

BrightShallows_EventScript_Npc0::
	msgbox BrightShallows_Text_Npc0, MSGBOX_NPC
	end

BrightShallows_EventScript_Npc1::
	msgbox BrightShallows_Text_Npc1, MSGBOX_NPC
	end

BrightShallows_EventScript_Quest0::
	lock
	faceplayer
	goto_if_set FLAG_TOPAZE_QUEST_BRIGHTSHALLOWS, BrightShallows_EventScript_Quest0_After
	msgbox BrightShallows_Text_Quest0_Ask
	checkitem ITEM_SUPER_POTION, 1
	goto_if_eq VAR_RESULT, FALSE, BrightShallows_EventScript_Quest0_Miss
	checkitemspace ITEM_MYSTIC_WATER, 1
	goto_if_eq VAR_RESULT, FALSE, BrightShallows_EventScript_Quest0_NoRoom
	removeitem ITEM_SUPER_POTION, 1
	giveitem ITEM_MYSTIC_WATER, 1
	setflag FLAG_TOPAZE_QUEST_BRIGHTSHALLOWS
	msgbox BrightShallows_Text_Quest0_Done
	release
	end

BrightShallows_EventScript_Quest0_After::
	msgbox BrightShallows_Text_Quest0_AfterT
	release
	end

BrightShallows_EventScript_Quest0_Miss::
	msgbox BrightShallows_Text_Quest0_MissT
	release
	end

BrightShallows_EventScript_Quest0_NoRoom::
	msgbox BrightShallows_Text_Quest0_NoRoomT
	release
	end


@ Topaze: objets caches (panneaux a script, drapeaux hors plage moteur)
BrightShallows_EventScript_TopazeFind0::
	lock
	goto_if_set FLAG_TOPAZE_FIND_BRIGHTSHALLOWS_0, BrightShallows_EventScript_TopazeFind0_Done
	checkitemspace ITEM_SUPER_POTION, 1
	goto_if_eq VAR_RESULT, FALSE, BrightShallows_EventScript_TopazeFind0_Full
	giveitem ITEM_SUPER_POTION, 1
	setflag FLAG_TOPAZE_FIND_BRIGHTSHALLOWS_0
	release
	end

BrightShallows_EventScript_TopazeFind0_Done::
	release
	end

BrightShallows_EventScript_TopazeFind0_Full::
	msgbox BrightShallows_Text_TopazeFindFull
	release
	end

BrightShallows_EventScript_TopazeFind1::
	lock
	goto_if_set FLAG_TOPAZE_FIND_BRIGHTSHALLOWS_1, BrightShallows_EventScript_TopazeFind1_Done
	checkitemspace ITEM_PEARL, 1
	goto_if_eq VAR_RESULT, FALSE, BrightShallows_EventScript_TopazeFind1_Full
	giveitem ITEM_PEARL, 1
	setflag FLAG_TOPAZE_FIND_BRIGHTSHALLOWS_1
	release
	end

BrightShallows_EventScript_TopazeFind1_Done::
	release
	end

BrightShallows_EventScript_TopazeFind1_Full::
	msgbox BrightShallows_Text_TopazeFindFull
	release
	end

BrightShallows_EventScript_TopazeFind2::
	lock
	goto_if_set FLAG_TOPAZE_FIND_BRIGHTSHALLOWS_2, BrightShallows_EventScript_TopazeFind2_Done
	checkitemspace ITEM_HEART_SCALE, 1
	goto_if_eq VAR_RESULT, FALSE, BrightShallows_EventScript_TopazeFind2_Full
	giveitem ITEM_HEART_SCALE, 1
	setflag FLAG_TOPAZE_FIND_BRIGHTSHALLOWS_2
	release
	end

BrightShallows_EventScript_TopazeFind2_Done::
	release
	end

BrightShallows_EventScript_TopazeFind2_Full::
	msgbox BrightShallows_Text_TopazeFindFull
	release
	end

