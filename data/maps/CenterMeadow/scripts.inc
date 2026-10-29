CenterMeadow_MapScripts::
	.byte 0

CenterMeadow_EventScript_ReturnFerry::
	lock
	faceplayer
	msgbox CenterMeadow_Text_ReturnAsk, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, CenterMeadow_EventScript_Stay
	warp MAP_FUCHSIA_CITY, 255, 24, 27
	waitstate
	end

CenterMeadow_EventScript_Stay::
	msgbox CenterMeadow_Text_Stay
	release
	end

CenterMeadow_EventScript_Npc0::
	msgbox CenterMeadow_Text_Npc0, MSGBOX_NPC
	end

CenterMeadow_EventScript_Npc1::
	msgbox CenterMeadow_Text_Npc1, MSGBOX_NPC
	end

CenterMeadow_EventScript_Quest0::
	lock
	faceplayer
	goto_if_set FLAG_TOPAZE_QUEST_CENTERMEADOW, CenterMeadow_EventScript_Quest0_After
	msgbox CenterMeadow_Text_Quest0_Ask
	checkitem ITEM_ULTRA_BALL, 2
	goto_if_eq VAR_RESULT, FALSE, CenterMeadow_EventScript_Quest0_Miss
	checkitemspace ITEM_LUCKY_EGG, 1
	goto_if_eq VAR_RESULT, FALSE, CenterMeadow_EventScript_Quest0_NoRoom
	removeitem ITEM_ULTRA_BALL, 2
	giveitem ITEM_LUCKY_EGG, 1
	setflag FLAG_TOPAZE_QUEST_CENTERMEADOW
	msgbox CenterMeadow_Text_Quest0_Done
	release
	end

CenterMeadow_EventScript_Quest0_After::
	msgbox CenterMeadow_Text_Quest0_AfterT
	release
	end

CenterMeadow_EventScript_Quest0_Miss::
	msgbox CenterMeadow_Text_Quest0_MissT
	release
	end

CenterMeadow_EventScript_Quest0_NoRoom::
	msgbox CenterMeadow_Text_Quest0_NoRoomT
	release
	end


@ Topaze: objets caches (panneaux a script, drapeaux hors plage moteur)
CenterMeadow_EventScript_TopazeFind0::
	lock
	goto_if_set FLAG_TOPAZE_FIND_CENTERMEADOW_0, CenterMeadow_EventScript_TopazeFind0_Done
	checkitemspace ITEM_LUCKY_EGG, 1
	goto_if_eq VAR_RESULT, FALSE, CenterMeadow_EventScript_TopazeFind0_Full
	giveitem ITEM_LUCKY_EGG, 1
	setflag FLAG_TOPAZE_FIND_CENTERMEADOW_0
	release
	end

CenterMeadow_EventScript_TopazeFind0_Done::
	release
	end

CenterMeadow_EventScript_TopazeFind0_Full::
	msgbox CenterMeadow_Text_TopazeFindFull
	release
	end

CenterMeadow_EventScript_TopazeFind1::
	lock
	goto_if_set FLAG_TOPAZE_FIND_CENTERMEADOW_1, CenterMeadow_EventScript_TopazeFind1_Done
	checkitemspace ITEM_ULTRA_BALL, 1
	goto_if_eq VAR_RESULT, FALSE, CenterMeadow_EventScript_TopazeFind1_Full
	giveitem ITEM_ULTRA_BALL, 1
	setflag FLAG_TOPAZE_FIND_CENTERMEADOW_1
	release
	end

CenterMeadow_EventScript_TopazeFind1_Done::
	release
	end

CenterMeadow_EventScript_TopazeFind1_Full::
	msgbox CenterMeadow_Text_TopazeFindFull
	release
	end

CenterMeadow_EventScript_TopazeFind2::
	lock
	goto_if_set FLAG_TOPAZE_FIND_CENTERMEADOW_2, CenterMeadow_EventScript_TopazeFind2_Done
	checkitemspace ITEM_REVIVE, 1
	goto_if_eq VAR_RESULT, FALSE, CenterMeadow_EventScript_TopazeFind2_Full
	giveitem ITEM_REVIVE, 1
	setflag FLAG_TOPAZE_FIND_CENTERMEADOW_2
	release
	end

CenterMeadow_EventScript_TopazeFind2_Done::
	release
	end

CenterMeadow_EventScript_TopazeFind2_Full::
	msgbox CenterMeadow_Text_TopazeFindFull
	release
	end

