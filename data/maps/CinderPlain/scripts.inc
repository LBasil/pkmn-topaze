CinderPlain_MapScripts::
	.byte 0

CinderPlain_EventScript_ReturnFerry::
	lock
	faceplayer
	msgbox CinderPlain_Text_ReturnAsk, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, CinderPlain_EventScript_Stay
	warp MAP_FUCHSIA_CITY, 255, 24, 27
	waitstate
	end

CinderPlain_EventScript_Stay::
	msgbox CinderPlain_Text_Stay
	release
	end

CinderPlain_EventScript_Npc0::
	msgbox CinderPlain_Text_Npc0, MSGBOX_NPC
	end

CinderPlain_EventScript_Npc1::
	msgbox CinderPlain_Text_Npc1, MSGBOX_NPC
	end

CinderPlain_EventScript_Quest0::
	lock
	faceplayer
	goto_if_set FLAG_TOPAZE_QUEST_CINDERPLAIN, CinderPlain_EventScript_Quest0_After
	msgbox CinderPlain_Text_Quest0_Ask
	checkitem ITEM_FIRE_STONE, 1
	goto_if_eq VAR_RESULT, FALSE, CinderPlain_EventScript_Quest0_Miss
	checkitemspace ITEM_CHARCOAL, 1
	goto_if_eq VAR_RESULT, FALSE, CinderPlain_EventScript_Quest0_NoRoom
	removeitem ITEM_FIRE_STONE, 1
	giveitem ITEM_CHARCOAL, 1
	setflag FLAG_TOPAZE_QUEST_CINDERPLAIN
	msgbox CinderPlain_Text_Quest0_Done
	release
	end

CinderPlain_EventScript_Quest0_After::
	msgbox CinderPlain_Text_Quest0_AfterT
	release
	end

CinderPlain_EventScript_Quest0_Miss::
	msgbox CinderPlain_Text_Quest0_MissT
	release
	end

CinderPlain_EventScript_Quest0_NoRoom::
	msgbox CinderPlain_Text_Quest0_NoRoomT
	release
	end


@ Topaze: objets caches (panneaux a script, drapeaux hors plage moteur)
CinderPlain_EventScript_TopazeFind0::
	lock
	goto_if_set FLAG_TOPAZE_FIND_CINDERPLAIN_0, CinderPlain_EventScript_TopazeFind0_Done
	checkitemspace ITEM_FIRE_STONE, 1
	goto_if_eq VAR_RESULT, FALSE, CinderPlain_EventScript_TopazeFind0_Full
	giveitem ITEM_FIRE_STONE, 1
	setflag FLAG_TOPAZE_FIND_CINDERPLAIN_0
	release
	end

CinderPlain_EventScript_TopazeFind0_Done::
	release
	end

CinderPlain_EventScript_TopazeFind0_Full::
	msgbox CinderPlain_Text_TopazeFindFull
	release
	end

CinderPlain_EventScript_TopazeFind1::
	lock
	goto_if_set FLAG_TOPAZE_FIND_CINDERPLAIN_1, CinderPlain_EventScript_TopazeFind1_Done
	checkitemspace ITEM_CHARCOAL, 1
	goto_if_eq VAR_RESULT, FALSE, CinderPlain_EventScript_TopazeFind1_Full
	giveitem ITEM_CHARCOAL, 1
	setflag FLAG_TOPAZE_FIND_CINDERPLAIN_1
	release
	end

CinderPlain_EventScript_TopazeFind1_Done::
	release
	end

CinderPlain_EventScript_TopazeFind1_Full::
	msgbox CinderPlain_Text_TopazeFindFull
	release
	end

CinderPlain_EventScript_TopazeFind2::
	lock
	goto_if_set FLAG_TOPAZE_FIND_CINDERPLAIN_2, CinderPlain_EventScript_TopazeFind2_Done
	checkitemspace ITEM_MAX_POTION, 1
	goto_if_eq VAR_RESULT, FALSE, CinderPlain_EventScript_TopazeFind2_Full
	giveitem ITEM_MAX_POTION, 1
	setflag FLAG_TOPAZE_FIND_CINDERPLAIN_2
	release
	end

CinderPlain_EventScript_TopazeFind2_Done::
	release
	end

CinderPlain_EventScript_TopazeFind2_Full::
	msgbox CinderPlain_Text_TopazeFindFull
	release
	end

