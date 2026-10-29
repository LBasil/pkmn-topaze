ThunderRidge_MapScripts::
	.byte 0

ThunderRidge_EventScript_ReturnFerry::
	lock
	faceplayer
	msgbox ThunderRidge_Text_ReturnAsk, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, ThunderRidge_EventScript_Stay
	warp MAP_FUCHSIA_CITY, 255, 24, 27
	waitstate
	end

ThunderRidge_EventScript_Stay::
	msgbox ThunderRidge_Text_Stay
	release
	end

ThunderRidge_EventScript_Npc0::
	msgbox ThunderRidge_Text_Npc0, MSGBOX_NPC
	end

ThunderRidge_EventScript_Npc1::
	msgbox ThunderRidge_Text_Npc1, MSGBOX_NPC
	end

ThunderRidge_EventScript_Quest0::
	lock
	faceplayer
	goto_if_set FLAG_TOPAZE_QUEST_THUNDERRIDGE, ThunderRidge_EventScript_Quest0_After
	msgbox ThunderRidge_Text_Quest0_Ask
	checkitem ITEM_THUNDER_STONE, 1
	goto_if_eq VAR_RESULT, FALSE, ThunderRidge_EventScript_Quest0_Miss
	checkitemspace ITEM_MAGNET, 1
	goto_if_eq VAR_RESULT, FALSE, ThunderRidge_EventScript_Quest0_NoRoom
	removeitem ITEM_THUNDER_STONE, 1
	giveitem ITEM_MAGNET, 1
	setflag FLAG_TOPAZE_QUEST_THUNDERRIDGE
	msgbox ThunderRidge_Text_Quest0_Done
	release
	end

ThunderRidge_EventScript_Quest0_After::
	msgbox ThunderRidge_Text_Quest0_AfterT
	release
	end

ThunderRidge_EventScript_Quest0_Miss::
	msgbox ThunderRidge_Text_Quest0_MissT
	release
	end

ThunderRidge_EventScript_Quest0_NoRoom::
	msgbox ThunderRidge_Text_Quest0_NoRoomT
	release
	end


@ Topaze: objets caches (panneaux a script, drapeaux hors plage moteur)
ThunderRidge_EventScript_TopazeFind0::
	lock
	goto_if_set FLAG_TOPAZE_FIND_THUNDERRIDGE_0, ThunderRidge_EventScript_TopazeFind0_Done
	checkitemspace ITEM_MAGNET, 1
	goto_if_eq VAR_RESULT, FALSE, ThunderRidge_EventScript_TopazeFind0_Full
	giveitem ITEM_MAGNET, 1
	setflag FLAG_TOPAZE_FIND_THUNDERRIDGE_0
	release
	end

ThunderRidge_EventScript_TopazeFind0_Done::
	release
	end

ThunderRidge_EventScript_TopazeFind0_Full::
	msgbox ThunderRidge_Text_TopazeFindFull
	release
	end

ThunderRidge_EventScript_TopazeFind1::
	lock
	goto_if_set FLAG_TOPAZE_FIND_THUNDERRIDGE_1, ThunderRidge_EventScript_TopazeFind1_Done
	checkitemspace ITEM_THUNDER_STONE, 1
	goto_if_eq VAR_RESULT, FALSE, ThunderRidge_EventScript_TopazeFind1_Full
	giveitem ITEM_THUNDER_STONE, 1
	setflag FLAG_TOPAZE_FIND_THUNDERRIDGE_1
	release
	end

ThunderRidge_EventScript_TopazeFind1_Done::
	release
	end

ThunderRidge_EventScript_TopazeFind1_Full::
	msgbox ThunderRidge_Text_TopazeFindFull
	release
	end

ThunderRidge_EventScript_TopazeFind2::
	lock
	goto_if_set FLAG_TOPAZE_FIND_THUNDERRIDGE_2, ThunderRidge_EventScript_TopazeFind2_Done
	checkitemspace ITEM_ELIXIR, 1
	goto_if_eq VAR_RESULT, FALSE, ThunderRidge_EventScript_TopazeFind2_Full
	giveitem ITEM_ELIXIR, 1
	setflag FLAG_TOPAZE_FIND_THUNDERRIDGE_2
	release
	end

ThunderRidge_EventScript_TopazeFind2_Done::
	release
	end

ThunderRidge_EventScript_TopazeFind2_Full::
	msgbox ThunderRidge_Text_TopazeFindFull
	release
	end

