SunkenBeach_MapScripts::
	.byte 0

SunkenBeach_EventScript_ReturnFerry::
	lock
	faceplayer
	msgbox SunkenBeach_Text_ReturnAsk, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, SunkenBeach_EventScript_Stay
	warp MAP_FUCHSIA_CITY, 255, 24, 27
	waitstate
	end

SunkenBeach_EventScript_Stay::
	msgbox SunkenBeach_Text_Stay
	release
	end

SunkenBeach_EventScript_Npc0::
	msgbox SunkenBeach_Text_Npc0, MSGBOX_NPC
	end

SunkenBeach_EventScript_Npc1::
	msgbox SunkenBeach_Text_Npc1, MSGBOX_NPC
	end

SunkenBeach_EventScript_Quest0::
	lock
	faceplayer
	goto_if_set FLAG_TOPAZE_QUEST_SUNKENBEACH, SunkenBeach_EventScript_Quest0_After
	msgbox SunkenBeach_Text_Quest0_Ask
	checkitem ITEM_HEART_SCALE, 1
	goto_if_eq VAR_RESULT, FALSE, SunkenBeach_EventScript_Quest0_Miss
	checkitemspace ITEM_SHELL_BELL, 1
	goto_if_eq VAR_RESULT, FALSE, SunkenBeach_EventScript_Quest0_NoRoom
	removeitem ITEM_HEART_SCALE, 1
	giveitem ITEM_SHELL_BELL, 1
	setflag FLAG_TOPAZE_QUEST_SUNKENBEACH
	msgbox SunkenBeach_Text_Quest0_Done
	release
	end

SunkenBeach_EventScript_Quest0_After::
	msgbox SunkenBeach_Text_Quest0_AfterT
	release
	end

SunkenBeach_EventScript_Quest0_Miss::
	msgbox SunkenBeach_Text_Quest0_MissT
	release
	end

SunkenBeach_EventScript_Quest0_NoRoom::
	msgbox SunkenBeach_Text_Quest0_NoRoomT
	release
	end


@ Topaze: objets caches (panneaux a script, drapeaux hors plage moteur)
SunkenBeach_EventScript_TopazeFind0::
	lock
	goto_if_set FLAG_TOPAZE_FIND_SUNKENBEACH_0, SunkenBeach_EventScript_TopazeFind0_Done
	checkitemspace ITEM_PEARL, 1
	goto_if_eq VAR_RESULT, FALSE, SunkenBeach_EventScript_TopazeFind0_Full
	giveitem ITEM_PEARL, 1
	setflag FLAG_TOPAZE_FIND_SUNKENBEACH_0
	release
	end

SunkenBeach_EventScript_TopazeFind0_Done::
	release
	end

SunkenBeach_EventScript_TopazeFind0_Full::
	msgbox SunkenBeach_Text_TopazeFindFull
	release
	end

SunkenBeach_EventScript_TopazeFind1::
	lock
	goto_if_set FLAG_TOPAZE_FIND_SUNKENBEACH_1, SunkenBeach_EventScript_TopazeFind1_Done
	checkitemspace ITEM_HEART_SCALE, 1
	goto_if_eq VAR_RESULT, FALSE, SunkenBeach_EventScript_TopazeFind1_Full
	giveitem ITEM_HEART_SCALE, 1
	setflag FLAG_TOPAZE_FIND_SUNKENBEACH_1
	release
	end

SunkenBeach_EventScript_TopazeFind1_Done::
	release
	end

SunkenBeach_EventScript_TopazeFind1_Full::
	msgbox SunkenBeach_Text_TopazeFindFull
	release
	end

SunkenBeach_EventScript_TopazeFind2::
	lock
	goto_if_set FLAG_TOPAZE_FIND_SUNKENBEACH_2, SunkenBeach_EventScript_TopazeFind2_Done
	checkitemspace ITEM_SUPER_POTION, 1
	goto_if_eq VAR_RESULT, FALSE, SunkenBeach_EventScript_TopazeFind2_Full
	giveitem ITEM_SUPER_POTION, 1
	setflag FLAG_TOPAZE_FIND_SUNKENBEACH_2
	release
	end

SunkenBeach_EventScript_TopazeFind2_Done::
	release
	end

SunkenBeach_EventScript_TopazeFind2_Full::
	msgbox SunkenBeach_Text_TopazeFindFull
	release
	end

