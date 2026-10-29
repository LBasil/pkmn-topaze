SoulPillar_MapScripts::
	.byte 0

SoulPillar_EventScript_ReturnFerry::
	lock
	faceplayer
	msgbox SoulPillar_Text_ReturnAsk, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, SoulPillar_EventScript_Stay
	warp MAP_FUCHSIA_CITY, 255, 24, 27
	waitstate
	end

SoulPillar_EventScript_Stay::
	msgbox SoulPillar_Text_Stay
	release
	end

SoulPillar_EventScript_Npc0::
	msgbox SoulPillar_Text_Npc0, MSGBOX_NPC
	end

SoulPillar_EventScript_Npc1::
	msgbox SoulPillar_Text_Npc1, MSGBOX_NPC
	end

SoulPillar_EventScript_Quest0::
	lock
	faceplayer
	goto_if_set FLAG_TOPAZE_QUEST_SOULPILLAR, SoulPillar_EventScript_Quest0_After
	msgbox SoulPillar_Text_Quest0_Ask
	checkitem ITEM_ZINC, 1
	goto_if_eq VAR_RESULT, FALSE, SoulPillar_EventScript_Quest0_Miss
	checkitemspace ITEM_LUCKY_EGG, 1
	goto_if_eq VAR_RESULT, FALSE, SoulPillar_EventScript_Quest0_NoRoom
	removeitem ITEM_ZINC, 1
	giveitem ITEM_LUCKY_EGG, 1
	setflag FLAG_TOPAZE_QUEST_SOULPILLAR
	msgbox SoulPillar_Text_Quest0_Done
	release
	end

SoulPillar_EventScript_Quest0_After::
	msgbox SoulPillar_Text_Quest0_AfterT
	release
	end

SoulPillar_EventScript_Quest0_Miss::
	msgbox SoulPillar_Text_Quest0_MissT
	release
	end

SoulPillar_EventScript_Quest0_NoRoom::
	msgbox SoulPillar_Text_Quest0_NoRoomT
	release
	end


@ Topaze: objets caches (panneaux a script, drapeaux hors plage moteur)
SoulPillar_EventScript_TopazeFind0::
	lock
	goto_if_set FLAG_TOPAZE_FIND_SOULPILLAR_0, SoulPillar_EventScript_TopazeFind0_Done
	checkitemspace ITEM_SPELL_TAG, 1
	goto_if_eq VAR_RESULT, FALSE, SoulPillar_EventScript_TopazeFind0_Full
	giveitem ITEM_SPELL_TAG, 1
	setflag FLAG_TOPAZE_FIND_SOULPILLAR_0
	release
	end

SoulPillar_EventScript_TopazeFind0_Done::
	release
	end

SoulPillar_EventScript_TopazeFind0_Full::
	msgbox SoulPillar_Text_TopazeFindFull
	release
	end

SoulPillar_EventScript_TopazeFind1::
	lock
	goto_if_set FLAG_TOPAZE_FIND_SOULPILLAR_1, SoulPillar_EventScript_TopazeFind1_Done
	checkitemspace ITEM_ZINC, 1
	goto_if_eq VAR_RESULT, FALSE, SoulPillar_EventScript_TopazeFind1_Full
	giveitem ITEM_ZINC, 1
	setflag FLAG_TOPAZE_FIND_SOULPILLAR_1
	release
	end

SoulPillar_EventScript_TopazeFind1_Done::
	release
	end

SoulPillar_EventScript_TopazeFind1_Full::
	msgbox SoulPillar_Text_TopazeFindFull
	release
	end

SoulPillar_EventScript_TopazeFind2::
	lock
	goto_if_set FLAG_TOPAZE_FIND_SOULPILLAR_2, SoulPillar_EventScript_TopazeFind2_Done
	checkitemspace ITEM_ULTRA_BALL, 1
	goto_if_eq VAR_RESULT, FALSE, SoulPillar_EventScript_TopazeFind2_Full
	giveitem ITEM_ULTRA_BALL, 1
	setflag FLAG_TOPAZE_FIND_SOULPILLAR_2
	release
	end

SoulPillar_EventScript_TopazeFind2_Done::
	release
	end

SoulPillar_EventScript_TopazeFind2_Full::
	msgbox SoulPillar_Text_TopazeFindFull
	release
	end

