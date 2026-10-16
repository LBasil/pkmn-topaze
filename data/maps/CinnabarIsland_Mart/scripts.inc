CinnabarIsland_Mart_MapScripts::
	.byte 0

CinnabarIsland_Mart_EventScript_Woman::
	msgbox CinnabarIsland_Mart_Text_DontTheyHaveXAttack, MSGBOX_NPC
	end

CinnabarIsland_Mart_EventScript_Scientist::
	lock
	faceplayer
	goto_if_set FLAG_QUEST_CINNABAR_REPEL, CinnabarIsland_Mart_EventScript_ScientistDone
	checkitem ITEM_REPEL, 3
	goto_if_eq VAR_RESULT, TRUE, CinnabarIsland_Mart_EventScript_ScientistOffer
	msgbox CinnabarIsland_Mart_Text_ScientistAsk
	release
	end

CinnabarIsland_Mart_EventScript_ScientistOffer::
	msgbox CinnabarIsland_Mart_Text_ScientistOffer, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, CinnabarIsland_Mart_EventScript_ScientistRefuse
	removeitem ITEM_REPEL, 3
	setflag FLAG_QUEST_CINNABAR_REPEL
	msgbox CinnabarIsland_Mart_Text_ScientistGives
	giveitem ITEM_CALCIUM
	release
	end

CinnabarIsland_Mart_EventScript_ScientistRefuse::
	msgbox CinnabarIsland_Mart_Text_ScientistNo
	release
	end

CinnabarIsland_Mart_EventScript_ScientistDone::
	msgbox CinnabarIsland_Mart_Text_ExtraItemsNeverHurt
	release
	end

CinnabarIsland_Mart_EventScript_Clerk::
	goto_if_questlog EventScript_ReleaseEnd
	lock
	faceplayer
	message Text_MayIHelpYou
	waitmessage
	pokemart CinnabarIsland_Mart_Items
	msgbox Text_PleaseComeAgain
	release
	end

	.align 2
CinnabarIsland_Mart_Items::
	.2byte ITEM_ULTRA_BALL
	.2byte ITEM_GREAT_BALL
	.2byte ITEM_HYPER_POTION
	.2byte ITEM_REVIVE
	.2byte ITEM_FULL_HEAL
	.2byte ITEM_ESCAPE_ROPE
	.2byte ITEM_MAX_REPEL
	.2byte ITEM_NONE
	release
	end
