PondOfSong_MapScripts::
	.byte 0

PondOfSong_EventScript_ReturnFerry::
	lock
	faceplayer
	msgbox PondOfSong_Text_ReturnAsk, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, PondOfSong_EventScript_Stay
	warp MAP_FUCHSIA_CITY, 255, 24, 27
	waitstate
	end

PondOfSong_EventScript_Stay::
	msgbox PondOfSong_Text_Stay
	release
	end

PondOfSong_EventScript_Npc0::
	msgbox PondOfSong_Text_Npc0, MSGBOX_NPC
	end

PondOfSong_EventScript_Npc1::
	msgbox PondOfSong_Text_Npc1, MSGBOX_NPC
	end

PondOfSong_EventScript_Quest0::
	lock
	faceplayer
	goto_if_set FLAG_TOPAZE_QUEST_PONDOFSONG, PondOfSong_EventScript_Quest0_After
	msgbox PondOfSong_Text_Quest0_Ask
	checkitem ITEM_NET_BALL, 1
	goto_if_eq VAR_RESULT, FALSE, PondOfSong_EventScript_Quest0_Miss
	checkitemspace ITEM_KINGS_ROCK, 1
	goto_if_eq VAR_RESULT, FALSE, PondOfSong_EventScript_Quest0_NoRoom
	removeitem ITEM_NET_BALL, 1
	giveitem ITEM_KINGS_ROCK, 1
	setflag FLAG_TOPAZE_QUEST_PONDOFSONG
	msgbox PondOfSong_Text_Quest0_Done
	release
	end

PondOfSong_EventScript_Quest0_After::
	msgbox PondOfSong_Text_Quest0_AfterT
	release
	end

PondOfSong_EventScript_Quest0_Miss::
	msgbox PondOfSong_Text_Quest0_MissT
	release
	end

PondOfSong_EventScript_Quest0_NoRoom::
	msgbox PondOfSong_Text_Quest0_NoRoomT
	release
	end


@ Topaze: objets caches (panneaux a script, drapeaux hors plage moteur)
PondOfSong_EventScript_TopazeFind0::
	lock
	goto_if_set FLAG_TOPAZE_FIND_PONDOFSONG_0, PondOfSong_EventScript_TopazeFind0_Done
	checkitemspace ITEM_KINGS_ROCK, 1
	goto_if_eq VAR_RESULT, FALSE, PondOfSong_EventScript_TopazeFind0_Full
	giveitem ITEM_KINGS_ROCK, 1
	setflag FLAG_TOPAZE_FIND_PONDOFSONG_0
	release
	end

PondOfSong_EventScript_TopazeFind0_Done::
	release
	end

PondOfSong_EventScript_TopazeFind0_Full::
	msgbox PondOfSong_Text_TopazeFindFull
	release
	end

PondOfSong_EventScript_TopazeFind1::
	lock
	goto_if_set FLAG_TOPAZE_FIND_PONDOFSONG_1, PondOfSong_EventScript_TopazeFind1_Done
	checkitemspace ITEM_MYSTIC_WATER, 1
	goto_if_eq VAR_RESULT, FALSE, PondOfSong_EventScript_TopazeFind1_Full
	giveitem ITEM_MYSTIC_WATER, 1
	setflag FLAG_TOPAZE_FIND_PONDOFSONG_1
	release
	end

PondOfSong_EventScript_TopazeFind1_Done::
	release
	end

PondOfSong_EventScript_TopazeFind1_Full::
	msgbox PondOfSong_Text_TopazeFindFull
	release
	end

PondOfSong_EventScript_TopazeFind2::
	lock
	goto_if_set FLAG_TOPAZE_FIND_PONDOFSONG_2, PondOfSong_EventScript_TopazeFind2_Done
	checkitemspace ITEM_NET_BALL, 1
	goto_if_eq VAR_RESULT, FALSE, PondOfSong_EventScript_TopazeFind2_Full
	giveitem ITEM_NET_BALL, 1
	setflag FLAG_TOPAZE_FIND_PONDOFSONG_2
	release
	end

PondOfSong_EventScript_TopazeFind2_Done::
	release
	end

PondOfSong_EventScript_TopazeFind2_Full::
	msgbox PondOfSong_Text_TopazeFindFull
	release
	end

