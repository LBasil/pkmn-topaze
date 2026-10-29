ShellCoast_MapScripts::
	.byte 0

ShellCoast_EventScript_ReturnFerry::
	lock
	faceplayer
	msgbox ShellCoast_Text_ReturnAsk, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, ShellCoast_EventScript_Stay
	warp MAP_FUCHSIA_CITY, 255, 24, 27
	waitstate
	end

ShellCoast_EventScript_Stay::
	msgbox ShellCoast_Text_Stay
	release
	end

ShellCoast_EventScript_Npc0::
	msgbox ShellCoast_Text_Npc0, MSGBOX_NPC
	end

ShellCoast_EventScript_Npc1::
	msgbox ShellCoast_Text_Npc1, MSGBOX_NPC
	end

ShellCoast_EventScript_Quest0::
	lock
	faceplayer
	goto_if_set FLAG_TOPAZE_QUEST_SHELLCOAST, ShellCoast_EventScript_Quest0_After
	msgbox ShellCoast_Text_Quest0_Ask
	checkitem ITEM_LEMONADE, 1
	goto_if_eq VAR_RESULT, FALSE, ShellCoast_EventScript_Quest0_Miss
	checkitemspace ITEM_DEEP_SEA_TOOTH, 1
	goto_if_eq VAR_RESULT, FALSE, ShellCoast_EventScript_Quest0_NoRoom
	removeitem ITEM_LEMONADE, 1
	giveitem ITEM_DEEP_SEA_TOOTH, 1
	setflag FLAG_TOPAZE_QUEST_SHELLCOAST
	msgbox ShellCoast_Text_Quest0_Done
	release
	end

ShellCoast_EventScript_Quest0_After::
	msgbox ShellCoast_Text_Quest0_AfterT
	release
	end

ShellCoast_EventScript_Quest0_Miss::
	msgbox ShellCoast_Text_Quest0_MissT
	release
	end

ShellCoast_EventScript_Quest0_NoRoom::
	msgbox ShellCoast_Text_Quest0_NoRoomT
	release
	end


@ Topaze: objets caches (panneaux a script, drapeaux hors plage moteur)
ShellCoast_EventScript_TopazeFind0::
	lock
	goto_if_set FLAG_TOPAZE_FIND_SHELLCOAST_0, ShellCoast_EventScript_TopazeFind0_Done
	checkitemspace ITEM_PEARL, 1
	goto_if_eq VAR_RESULT, FALSE, ShellCoast_EventScript_TopazeFind0_Full
	giveitem ITEM_PEARL, 1
	setflag FLAG_TOPAZE_FIND_SHELLCOAST_0
	release
	end

ShellCoast_EventScript_TopazeFind0_Done::
	release
	end

ShellCoast_EventScript_TopazeFind0_Full::
	msgbox ShellCoast_Text_TopazeFindFull
	release
	end

ShellCoast_EventScript_TopazeFind1::
	lock
	goto_if_set FLAG_TOPAZE_FIND_SHELLCOAST_1, ShellCoast_EventScript_TopazeFind1_Done
	checkitemspace ITEM_HEART_SCALE, 1
	goto_if_eq VAR_RESULT, FALSE, ShellCoast_EventScript_TopazeFind1_Full
	giveitem ITEM_HEART_SCALE, 1
	setflag FLAG_TOPAZE_FIND_SHELLCOAST_1
	release
	end

ShellCoast_EventScript_TopazeFind1_Done::
	release
	end

ShellCoast_EventScript_TopazeFind1_Full::
	msgbox ShellCoast_Text_TopazeFindFull
	release
	end

ShellCoast_EventScript_TopazeFind2::
	lock
	goto_if_set FLAG_TOPAZE_FIND_SHELLCOAST_2, ShellCoast_EventScript_TopazeFind2_Done
	checkitemspace ITEM_ELIXIR, 1
	goto_if_eq VAR_RESULT, FALSE, ShellCoast_EventScript_TopazeFind2_Full
	giveitem ITEM_ELIXIR, 1
	setflag FLAG_TOPAZE_FIND_SHELLCOAST_2
	release
	end

ShellCoast_EventScript_TopazeFind2_Done::
	release
	end

ShellCoast_EventScript_TopazeFind2_Full::
	msgbox ShellCoast_Text_TopazeFindFull
	release
	end


ShellCoast_Text_TopazeFindFull::
	.string "Something shines here, but your BAG\n"
	.string "is full.$"
