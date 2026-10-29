CircusLawn_MapScripts::
	.byte 0

CircusLawn_EventScript_ReturnFerry::
	lock
	faceplayer
	msgbox CircusLawn_Text_ReturnAsk, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, CircusLawn_EventScript_Stay
	warp MAP_FUCHSIA_CITY, 255, 24, 27
	waitstate
	end

CircusLawn_EventScript_Stay::
	msgbox CircusLawn_Text_Stay
	release
	end

CircusLawn_EventScript_Npc0::
	msgbox CircusLawn_Text_Npc0, MSGBOX_NPC
	end

CircusLawn_EventScript_Npc1::
	msgbox CircusLawn_Text_Npc1, MSGBOX_NPC
	end

CircusLawn_EventScript_Quest0::
	lock
	faceplayer
	goto_if_set FLAG_TOPAZE_QUEST_CIRCUSLAWN, CircusLawn_EventScript_Quest0_After
	msgbox CircusLawn_Text_Quest0_Ask
	checkitem ITEM_GREAT_BALL, 2
	goto_if_eq VAR_RESULT, FALSE, CircusLawn_EventScript_Quest0_Miss
	checkitemspace ITEM_TWISTED_SPOON, 1
	goto_if_eq VAR_RESULT, FALSE, CircusLawn_EventScript_Quest0_NoRoom
	removeitem ITEM_GREAT_BALL, 2
	giveitem ITEM_TWISTED_SPOON, 1
	setflag FLAG_TOPAZE_QUEST_CIRCUSLAWN
	msgbox CircusLawn_Text_Quest0_Done
	release
	end

CircusLawn_EventScript_Quest0_After::
	msgbox CircusLawn_Text_Quest0_AfterT
	release
	end

CircusLawn_EventScript_Quest0_Miss::
	msgbox CircusLawn_Text_Quest0_MissT
	release
	end

CircusLawn_EventScript_Quest0_NoRoom::
	msgbox CircusLawn_Text_Quest0_NoRoomT
	release
	end


@ Topaze: objets caches (panneaux a script, drapeaux hors plage moteur)
CircusLawn_EventScript_TopazeFind0::
	lock
	goto_if_set FLAG_TOPAZE_FIND_CIRCUSLAWN_0, CircusLawn_EventScript_TopazeFind0_Done
	checkitemspace ITEM_TWISTED_SPOON, 1
	goto_if_eq VAR_RESULT, FALSE, CircusLawn_EventScript_TopazeFind0_Full
	giveitem ITEM_TWISTED_SPOON, 1
	setflag FLAG_TOPAZE_FIND_CIRCUSLAWN_0
	release
	end

CircusLawn_EventScript_TopazeFind0_Done::
	release
	end

CircusLawn_EventScript_TopazeFind0_Full::
	msgbox CircusLawn_Text_TopazeFindFull
	release
	end

CircusLawn_EventScript_TopazeFind1::
	lock
	goto_if_set FLAG_TOPAZE_FIND_CIRCUSLAWN_1, CircusLawn_EventScript_TopazeFind1_Done
	checkitemspace ITEM_ELIXIR, 1
	goto_if_eq VAR_RESULT, FALSE, CircusLawn_EventScript_TopazeFind1_Full
	giveitem ITEM_ELIXIR, 1
	setflag FLAG_TOPAZE_FIND_CIRCUSLAWN_1
	release
	end

CircusLawn_EventScript_TopazeFind1_Done::
	release
	end

CircusLawn_EventScript_TopazeFind1_Full::
	msgbox CircusLawn_Text_TopazeFindFull
	release
	end

CircusLawn_EventScript_TopazeFind2::
	lock
	goto_if_set FLAG_TOPAZE_FIND_CIRCUSLAWN_2, CircusLawn_EventScript_TopazeFind2_Done
	checkitemspace ITEM_GREAT_BALL, 1
	goto_if_eq VAR_RESULT, FALSE, CircusLawn_EventScript_TopazeFind2_Full
	giveitem ITEM_GREAT_BALL, 1
	setflag FLAG_TOPAZE_FIND_CIRCUSLAWN_2
	release
	end

CircusLawn_EventScript_TopazeFind2_Done::
	release
	end

CircusLawn_EventScript_TopazeFind2_Full::
	msgbox CircusLawn_Text_TopazeFindFull
	release
	end

