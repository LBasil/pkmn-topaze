SoundMeadow_MapScripts::
	.byte 0

SoundMeadow_EventScript_ReturnFerry::
	lock
	faceplayer
	msgbox SoundMeadow_Text_ReturnAsk, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, SoundMeadow_EventScript_Stay
	warp MAP_FUCHSIA_CITY, 255, 24, 27
	waitstate
	end

SoundMeadow_EventScript_Stay::
	msgbox SoundMeadow_Text_Stay
	release
	end

SoundMeadow_EventScript_Npc0::
	msgbox SoundMeadow_Text_Npc0, MSGBOX_NPC
	end

SoundMeadow_EventScript_Npc1::
	msgbox SoundMeadow_Text_Npc1, MSGBOX_NPC
	end

SoundMeadow_EventScript_Quest0::
	lock
	faceplayer
	goto_if_set FLAG_TOPAZE_QUEST_SOUNDMEADOW, SoundMeadow_EventScript_Quest0_After
	msgbox SoundMeadow_Text_Quest0_Ask
	checkitem ITEM_LEPPA_BERRY, 1
	goto_if_eq VAR_RESULT, FALSE, SoundMeadow_EventScript_Quest0_Miss
	checkitemspace ITEM_SOFT_SAND, 1
	goto_if_eq VAR_RESULT, FALSE, SoundMeadow_EventScript_Quest0_NoRoom
	removeitem ITEM_LEPPA_BERRY, 1
	giveitem ITEM_SOFT_SAND, 1
	setflag FLAG_TOPAZE_QUEST_SOUNDMEADOW
	msgbox SoundMeadow_Text_Quest0_Done
	release
	end

SoundMeadow_EventScript_Quest0_After::
	msgbox SoundMeadow_Text_Quest0_AfterT
	release
	end

SoundMeadow_EventScript_Quest0_Miss::
	msgbox SoundMeadow_Text_Quest0_MissT
	release
	end

SoundMeadow_EventScript_Quest0_NoRoom::
	msgbox SoundMeadow_Text_Quest0_NoRoomT
	release
	end


@ Topaze: objets caches (panneaux a script, drapeaux hors plage moteur)
SoundMeadow_EventScript_TopazeFind0::
	lock
	goto_if_set FLAG_TOPAZE_FIND_SOUNDMEADOW_0, SoundMeadow_EventScript_TopazeFind0_Done
	checkitemspace ITEM_MOON_STONE, 1
	goto_if_eq VAR_RESULT, FALSE, SoundMeadow_EventScript_TopazeFind0_Full
	giveitem ITEM_MOON_STONE, 1
	setflag FLAG_TOPAZE_FIND_SOUNDMEADOW_0
	release
	end

SoundMeadow_EventScript_TopazeFind0_Done::
	release
	end

SoundMeadow_EventScript_TopazeFind0_Full::
	msgbox SoundMeadow_Text_TopazeFindFull
	release
	end

SoundMeadow_EventScript_TopazeFind1::
	lock
	goto_if_set FLAG_TOPAZE_FIND_SOUNDMEADOW_1, SoundMeadow_EventScript_TopazeFind1_Done
	checkitemspace ITEM_LEPPA_BERRY, 1
	goto_if_eq VAR_RESULT, FALSE, SoundMeadow_EventScript_TopazeFind1_Full
	giveitem ITEM_LEPPA_BERRY, 1
	setflag FLAG_TOPAZE_FIND_SOUNDMEADOW_1
	release
	end

SoundMeadow_EventScript_TopazeFind1_Done::
	release
	end

SoundMeadow_EventScript_TopazeFind1_Full::
	msgbox SoundMeadow_Text_TopazeFindFull
	release
	end

SoundMeadow_EventScript_TopazeFind2::
	lock
	goto_if_set FLAG_TOPAZE_FIND_SOUNDMEADOW_2, SoundMeadow_EventScript_TopazeFind2_Done
	checkitemspace ITEM_ELIXIR, 1
	goto_if_eq VAR_RESULT, FALSE, SoundMeadow_EventScript_TopazeFind2_Full
	giveitem ITEM_ELIXIR, 1
	setflag FLAG_TOPAZE_FIND_SOUNDMEADOW_2
	release
	end

SoundMeadow_EventScript_TopazeFind2_Done::
	release
	end

SoundMeadow_EventScript_TopazeFind2_Full::
	msgbox SoundMeadow_Text_TopazeFindFull
	release
	end

