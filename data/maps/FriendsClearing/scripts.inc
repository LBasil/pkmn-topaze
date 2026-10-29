FriendsClearing_MapScripts::
	.byte 0

FriendsClearing_EventScript_ReturnFerry::
	lock
	faceplayer
	msgbox FriendsClearing_Text_ReturnAsk, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, FriendsClearing_EventScript_Stay
	warp MAP_FUCHSIA_CITY, 255, 24, 27
	waitstate
	end

FriendsClearing_EventScript_Stay::
	msgbox FriendsClearing_Text_Stay
	release
	end

FriendsClearing_EventScript_Boss::
	lock
	faceplayer
	goto_if_defeated TRAINER_ZONE_CLEARING, FriendsClearing_EventScript_Boss_After
	msgbox FriendsClearing_Text_Boss_Intro
	checkitemspace ITEM_PP_MAX, 3
	goto_if_eq VAR_RESULT, FALSE, FriendsClearing_EventScript_Boss_NoRoom
	trainerbattle_no_intro TRAINER_ZONE_CLEARING, FriendsClearing_Text_Boss_Defeat
	giveitem ITEM_PP_MAX, 3
	msgbox FriendsClearing_Text_Boss_After
	release
	end

FriendsClearing_EventScript_Boss_After::
	msgbox FriendsClearing_Text_Boss_After
	release
	end

FriendsClearing_EventScript_Boss_NoRoom::
	msgbox FriendsClearing_Text_Boss_NoRoom
	release
	end

FriendsClearing_EventScript_Npc0::
	msgbox FriendsClearing_Text_Npc0, MSGBOX_NPC
	end

FriendsClearing_EventScript_Npc1::
	msgbox FriendsClearing_Text_Npc1, MSGBOX_NPC
	end

