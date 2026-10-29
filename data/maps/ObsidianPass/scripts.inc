ObsidianPass_MapScripts::
	.byte 0

ObsidianPass_EventScript_ReturnFerry::
	lock
	faceplayer
	msgbox ObsidianPass_Text_ReturnAsk, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, ObsidianPass_EventScript_Stay
	warp MAP_FUCHSIA_CITY, 255, 24, 27
	waitstate
	end

ObsidianPass_EventScript_Stay::
	msgbox ObsidianPass_Text_Stay
	release
	end

ObsidianPass_EventScript_Npc0::
	msgbox ObsidianPass_Text_Npc0, MSGBOX_NPC
	end

ObsidianPass_EventScript_Npc1::
	msgbox ObsidianPass_Text_Npc1, MSGBOX_NPC
	end

ObsidianPass_EventScript_Quest0::
	lock
	faceplayer
	goto_if_set FLAG_TOPAZE_QUEST_OBSIDIANPASS, ObsidianPass_EventScript_Quest0_After
	msgbox ObsidianPass_Text_Quest0_Ask
	checkitem ITEM_MAX_REPEL, 1
	goto_if_eq VAR_RESULT, FALSE, ObsidianPass_EventScript_Quest0_Miss
	checkitemspace ITEM_HARD_STONE, 1
	goto_if_eq VAR_RESULT, FALSE, ObsidianPass_EventScript_Quest0_NoRoom
	removeitem ITEM_MAX_REPEL, 1
	giveitem ITEM_HARD_STONE, 1
	setflag FLAG_TOPAZE_QUEST_OBSIDIANPASS
	msgbox ObsidianPass_Text_Quest0_Done
	release
	end

ObsidianPass_EventScript_Quest0_After::
	msgbox ObsidianPass_Text_Quest0_AfterT
	release
	end

ObsidianPass_EventScript_Quest0_Miss::
	msgbox ObsidianPass_Text_Quest0_MissT
	release
	end

ObsidianPass_EventScript_Quest0_NoRoom::
	msgbox ObsidianPass_Text_Quest0_NoRoomT
	release
	end


@ Topaze: objets caches (panneaux a script, drapeaux hors plage moteur)
ObsidianPass_EventScript_TopazeFind0::
	lock
	goto_if_set FLAG_TOPAZE_FIND_OBSIDIANPASS_0, ObsidianPass_EventScript_TopazeFind0_Done
	checkitemspace ITEM_HARD_STONE, 1
	goto_if_eq VAR_RESULT, FALSE, ObsidianPass_EventScript_TopazeFind0_Full
	giveitem ITEM_HARD_STONE, 1
	setflag FLAG_TOPAZE_FIND_OBSIDIANPASS_0
	release
	end

ObsidianPass_EventScript_TopazeFind0_Done::
	release
	end

ObsidianPass_EventScript_TopazeFind0_Full::
	msgbox ObsidianPass_Text_TopazeFindFull
	release
	end

ObsidianPass_EventScript_TopazeFind1::
	lock
	goto_if_set FLAG_TOPAZE_FIND_OBSIDIANPASS_1, ObsidianPass_EventScript_TopazeFind1_Done
	checkitemspace ITEM_METAL_COAT, 1
	goto_if_eq VAR_RESULT, FALSE, ObsidianPass_EventScript_TopazeFind1_Full
	giveitem ITEM_METAL_COAT, 1
	setflag FLAG_TOPAZE_FIND_OBSIDIANPASS_1
	release
	end

ObsidianPass_EventScript_TopazeFind1_Done::
	release
	end

ObsidianPass_EventScript_TopazeFind1_Full::
	msgbox ObsidianPass_Text_TopazeFindFull
	release
	end

ObsidianPass_EventScript_TopazeFind2::
	lock
	goto_if_set FLAG_TOPAZE_FIND_OBSIDIANPASS_2, ObsidianPass_EventScript_TopazeFind2_Done
	checkitemspace ITEM_MAX_REPEL, 1
	goto_if_eq VAR_RESULT, FALSE, ObsidianPass_EventScript_TopazeFind2_Full
	giveitem ITEM_MAX_REPEL, 1
	setflag FLAG_TOPAZE_FIND_OBSIDIANPASS_2
	release
	end

ObsidianPass_EventScript_TopazeFind2_Done::
	release
	end

ObsidianPass_EventScript_TopazeFind2_Full::
	msgbox ObsidianPass_Text_TopazeFindFull
	release
	end

