PebbleBeach_MapScripts::
	.byte 0

PebbleBeach_EventScript_ReturnFerry::
	lock
	faceplayer
	msgbox PebbleBeach_Text_ReturnAsk, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, PebbleBeach_EventScript_Stay
	warp MAP_FUCHSIA_CITY, 255, 24, 27
	waitstate
	end

PebbleBeach_EventScript_Stay::
	msgbox PebbleBeach_Text_Stay
	release
	end

PebbleBeach_EventScript_Npc0::
	msgbox PebbleBeach_Text_Npc0, MSGBOX_NPC
	end

PebbleBeach_EventScript_Npc1::
	msgbox PebbleBeach_Text_Npc1, MSGBOX_NPC
	end

PebbleBeach_EventScript_Quest0::
	lock
	faceplayer
	goto_if_set FLAG_TOPAZE_QUEST_PEBBLEBEACH, PebbleBeach_EventScript_Quest0_After
	msgbox PebbleBeach_Text_Quest0_Ask
	checkitem ITEM_POKE_BALL, 1
	goto_if_eq VAR_RESULT, FALSE, PebbleBeach_EventScript_Quest0_Miss
	checkitemspace ITEM_NET_BALL, 1
	goto_if_eq VAR_RESULT, FALSE, PebbleBeach_EventScript_Quest0_NoRoom
	removeitem ITEM_POKE_BALL, 1
	giveitem ITEM_NET_BALL, 1
	setflag FLAG_TOPAZE_QUEST_PEBBLEBEACH
	msgbox PebbleBeach_Text_Quest0_Done
	release
	end

PebbleBeach_EventScript_Quest0_After::
	msgbox PebbleBeach_Text_Quest0_AfterT
	release
	end

PebbleBeach_EventScript_Quest0_Miss::
	msgbox PebbleBeach_Text_Quest0_MissT
	release
	end

PebbleBeach_EventScript_Quest0_NoRoom::
	msgbox PebbleBeach_Text_Quest0_NoRoomT
	release
	end


@ Topaze: objets caches (panneaux a script, drapeaux hors plage moteur)
PebbleBeach_EventScript_TopazeFind0::
	lock
	goto_if_set FLAG_TOPAZE_FIND_PEBBLEBEACH_0, PebbleBeach_EventScript_TopazeFind0_Done
	checkitemspace ITEM_POTION, 1
	goto_if_eq VAR_RESULT, FALSE, PebbleBeach_EventScript_TopazeFind0_Full
	giveitem ITEM_POTION, 1
	setflag FLAG_TOPAZE_FIND_PEBBLEBEACH_0
	release
	end

PebbleBeach_EventScript_TopazeFind0_Done::
	release
	end

PebbleBeach_EventScript_TopazeFind0_Full::
	msgbox PebbleBeach_Text_TopazeFindFull
	release
	end

PebbleBeach_EventScript_TopazeFind1::
	lock
	goto_if_set FLAG_TOPAZE_FIND_PEBBLEBEACH_1, PebbleBeach_EventScript_TopazeFind1_Done
	checkitemspace ITEM_POKE_BALL, 1
	goto_if_eq VAR_RESULT, FALSE, PebbleBeach_EventScript_TopazeFind1_Full
	giveitem ITEM_POKE_BALL, 1
	setflag FLAG_TOPAZE_FIND_PEBBLEBEACH_1
	release
	end

PebbleBeach_EventScript_TopazeFind1_Done::
	release
	end

PebbleBeach_EventScript_TopazeFind1_Full::
	msgbox PebbleBeach_Text_TopazeFindFull
	release
	end

PebbleBeach_EventScript_TopazeFind2::
	lock
	goto_if_set FLAG_TOPAZE_FIND_PEBBLEBEACH_2, PebbleBeach_EventScript_TopazeFind2_Done
	checkitemspace ITEM_ANTIDOTE, 1
	goto_if_eq VAR_RESULT, FALSE, PebbleBeach_EventScript_TopazeFind2_Full
	giveitem ITEM_ANTIDOTE, 1
	setflag FLAG_TOPAZE_FIND_PEBBLEBEACH_2
	release
	end

PebbleBeach_EventScript_TopazeFind2_Done::
	release
	end

PebbleBeach_EventScript_TopazeFind2_Full::
	msgbox PebbleBeach_Text_TopazeFindFull
	release
	end

