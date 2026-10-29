AshenMine_MapScripts::
	.byte 0

AshenMine_EventScript_ReturnFerry::
	lock
	faceplayer
	msgbox AshenMine_Text_ReturnAsk, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, AshenMine_EventScript_Stay
	warp MAP_FUCHSIA_CITY, 255, 24, 27
	waitstate
	end

AshenMine_EventScript_Stay::
	msgbox AshenMine_Text_Stay
	release
	end

AshenMine_EventScript_Npc0::
	msgbox AshenMine_Text_Npc0, MSGBOX_NPC
	end

AshenMine_EventScript_Quest0::
	lock
	faceplayer
	goto_if_set FLAG_TOPAZE_QUEST_MINE, AshenMine_EventScript_Quest0_After
	msgbox AshenMine_Text_Quest0_Ask
	checkitem ITEM_STARDUST, 2
	goto_if_eq VAR_RESULT, FALSE, AshenMine_EventScript_Quest0_Miss
	checkitemspace ITEM_DRAGON_SCALE, 1
	goto_if_eq VAR_RESULT, FALSE, AshenMine_EventScript_Quest0_NoRoom
	removeitem ITEM_STARDUST, 2
	giveitem ITEM_DRAGON_SCALE, 1
	setflag FLAG_TOPAZE_QUEST_MINE
	msgbox AshenMine_Text_Quest0_Done
	release
	end

AshenMine_EventScript_Quest0_After::
	msgbox AshenMine_Text_Quest0_AfterT
	release
	end

AshenMine_EventScript_Quest0_Miss::
	msgbox AshenMine_Text_Quest0_MissT
	release
	end

AshenMine_EventScript_Quest0_NoRoom::
	msgbox AshenMine_Text_Quest0_NoRoomT
	release
	end


@ Topaze: objets caches (panneaux a script, drapeaux hors plage moteur)
AshenMine_EventScript_TopazeFind0::
	lock
	goto_if_set FLAG_TOPAZE_FIND_MINE_0, AshenMine_EventScript_TopazeFind0_Done
	checkitemspace ITEM_STAR_PIECE, 1
	goto_if_eq VAR_RESULT, FALSE, AshenMine_EventScript_TopazeFind0_Full
	giveitem ITEM_STAR_PIECE, 1
	setflag FLAG_TOPAZE_FIND_MINE_0
	release
	end

AshenMine_EventScript_TopazeFind0_Done::
	release
	end

AshenMine_EventScript_TopazeFind0_Full::
	msgbox AshenMine_Text_TopazeFindFull
	release
	end

AshenMine_EventScript_TopazeFind1::
	lock
	goto_if_set FLAG_TOPAZE_FIND_MINE_1, AshenMine_EventScript_TopazeFind1_Done
	checkitemspace ITEM_STAR_PIECE, 1
	goto_if_eq VAR_RESULT, FALSE, AshenMine_EventScript_TopazeFind1_Full
	giveitem ITEM_STAR_PIECE, 1
	setflag FLAG_TOPAZE_FIND_MINE_1
	release
	end

AshenMine_EventScript_TopazeFind1_Done::
	release
	end

AshenMine_EventScript_TopazeFind1_Full::
	msgbox AshenMine_Text_TopazeFindFull
	release
	end

AshenMine_EventScript_TopazeFind2::
	lock
	goto_if_set FLAG_TOPAZE_FIND_MINE_2, AshenMine_EventScript_TopazeFind2_Done
	checkitemspace ITEM_STARDUST, 1
	goto_if_eq VAR_RESULT, FALSE, AshenMine_EventScript_TopazeFind2_Full
	giveitem ITEM_STARDUST, 1
	setflag FLAG_TOPAZE_FIND_MINE_2
	release
	end

AshenMine_EventScript_TopazeFind2_Done::
	release
	end

AshenMine_EventScript_TopazeFind2_Full::
	msgbox AshenMine_Text_TopazeFindFull
	release
	end

AshenMine_EventScript_TopazeFind3::
	lock
	goto_if_set FLAG_TOPAZE_FIND_MINE_3, AshenMine_EventScript_TopazeFind3_Done
	checkitemspace ITEM_STARDUST, 1
	goto_if_eq VAR_RESULT, FALSE, AshenMine_EventScript_TopazeFind3_Full
	giveitem ITEM_STARDUST, 1
	setflag FLAG_TOPAZE_FIND_MINE_3
	release
	end

AshenMine_EventScript_TopazeFind3_Done::
	release
	end

AshenMine_EventScript_TopazeFind3_Full::
	msgbox AshenMine_Text_TopazeFindFull
	release
	end

AshenMine_EventScript_TopazeFind4::
	lock
	goto_if_set FLAG_TOPAZE_FIND_MINE_4, AshenMine_EventScript_TopazeFind4_Done
	checkitemspace ITEM_SUN_STONE, 1
	goto_if_eq VAR_RESULT, FALSE, AshenMine_EventScript_TopazeFind4_Full
	giveitem ITEM_SUN_STONE, 1
	setflag FLAG_TOPAZE_FIND_MINE_4
	release
	end

AshenMine_EventScript_TopazeFind4_Done::
	release
	end

AshenMine_EventScript_TopazeFind4_Full::
	msgbox AshenMine_Text_TopazeFindFull
	release
	end

AshenMine_EventScript_TopazeFind5::
	lock
	goto_if_set FLAG_TOPAZE_FIND_MINE_5, AshenMine_EventScript_TopazeFind5_Done
	checkitemspace ITEM_MOON_STONE, 1
	goto_if_eq VAR_RESULT, FALSE, AshenMine_EventScript_TopazeFind5_Full
	giveitem ITEM_MOON_STONE, 1
	setflag FLAG_TOPAZE_FIND_MINE_5
	release
	end

AshenMine_EventScript_TopazeFind5_Done::
	release
	end

AshenMine_EventScript_TopazeFind5_Full::
	msgbox AshenMine_Text_TopazeFindFull
	release
	end


AshenMine_Text_TopazeFindFull::
	.string "Something shines here, but your BAG\n"
	.string "is full.$"
