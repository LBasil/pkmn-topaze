BlossomCrest_MapScripts::
	.byte 0

BlossomCrest_EventScript_ReturnFerry::
	lock
	faceplayer
	msgbox BlossomCrest_Text_ReturnAsk, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, BlossomCrest_EventScript_Stay
	warp MAP_FUCHSIA_CITY, 255, 24, 27
	waitstate
	end

BlossomCrest_EventScript_Stay::
	msgbox BlossomCrest_Text_Stay
	release
	end

BlossomCrest_EventScript_Npc0::
	msgbox BlossomCrest_Text_Npc0, MSGBOX_NPC
	end

BlossomCrest_EventScript_Npc1::
	msgbox BlossomCrest_Text_Npc1, MSGBOX_NPC
	end

BlossomCrest_EventScript_Quest0::
	lock
	faceplayer
	goto_if_set FLAG_TOPAZE_QUEST_BLOSSOMCREST, BlossomCrest_EventScript_Quest0_After
	msgbox BlossomCrest_Text_Quest0_Ask
	checkitem ITEM_LEAF_STONE, 1
	goto_if_eq VAR_RESULT, FALSE, BlossomCrest_EventScript_Quest0_Miss
	checkitemspace ITEM_MIRACLE_SEED, 1
	goto_if_eq VAR_RESULT, FALSE, BlossomCrest_EventScript_Quest0_NoRoom
	removeitem ITEM_LEAF_STONE, 1
	giveitem ITEM_MIRACLE_SEED, 1
	setflag FLAG_TOPAZE_QUEST_BLOSSOMCREST
	msgbox BlossomCrest_Text_Quest0_Done
	release
	end

BlossomCrest_EventScript_Quest0_After::
	msgbox BlossomCrest_Text_Quest0_AfterT
	release
	end

BlossomCrest_EventScript_Quest0_Miss::
	msgbox BlossomCrest_Text_Quest0_MissT
	release
	end

BlossomCrest_EventScript_Quest0_NoRoom::
	msgbox BlossomCrest_Text_Quest0_NoRoomT
	release
	end


@ Topaze: objets caches (panneaux a script, drapeaux hors plage moteur)
BlossomCrest_EventScript_TopazeFind0::
	lock
	goto_if_set FLAG_TOPAZE_FIND_BLOSSOMCREST_0, BlossomCrest_EventScript_TopazeFind0_Done
	checkitemspace ITEM_MIRACLE_SEED, 1
	goto_if_eq VAR_RESULT, FALSE, BlossomCrest_EventScript_TopazeFind0_Full
	giveitem ITEM_MIRACLE_SEED, 1
	setflag FLAG_TOPAZE_FIND_BLOSSOMCREST_0
	release
	end

BlossomCrest_EventScript_TopazeFind0_Done::
	release
	end

BlossomCrest_EventScript_TopazeFind0_Full::
	msgbox BlossomCrest_Text_TopazeFindFull
	release
	end

BlossomCrest_EventScript_TopazeFind1::
	lock
	goto_if_set FLAG_TOPAZE_FIND_BLOSSOMCREST_1, BlossomCrest_EventScript_TopazeFind1_Done
	checkitemspace ITEM_LEAF_STONE, 1
	goto_if_eq VAR_RESULT, FALSE, BlossomCrest_EventScript_TopazeFind1_Full
	giveitem ITEM_LEAF_STONE, 1
	setflag FLAG_TOPAZE_FIND_BLOSSOMCREST_1
	release
	end

BlossomCrest_EventScript_TopazeFind1_Done::
	release
	end

BlossomCrest_EventScript_TopazeFind1_Full::
	msgbox BlossomCrest_Text_TopazeFindFull
	release
	end

BlossomCrest_EventScript_TopazeFind2::
	lock
	goto_if_set FLAG_TOPAZE_FIND_BLOSSOMCREST_2, BlossomCrest_EventScript_TopazeFind2_Done
	checkitemspace ITEM_SUN_STONE, 1
	goto_if_eq VAR_RESULT, FALSE, BlossomCrest_EventScript_TopazeFind2_Full
	giveitem ITEM_SUN_STONE, 1
	setflag FLAG_TOPAZE_FIND_BLOSSOMCREST_2
	release
	end

BlossomCrest_EventScript_TopazeFind2_Done::
	release
	end

BlossomCrest_EventScript_TopazeFind2_Full::
	msgbox BlossomCrest_Text_TopazeFindFull
	release
	end

