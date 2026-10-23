TwoIsland_Harbor_MapScripts::
	.byte 0

TwoIsland_Harbor_EventScript_Sailor::
	lock
	faceplayer
	message Text_WhereDoYouWantToSail
	waitmessage
	setvar VAR_0x8004, SEAGALLOP_TWO_ISLAND
	goto EventScript_ChooseDestFromTwoIsland
	end

@ Topaze: guide du port (post-game) : presente l'ile puis lit la boussole des Echos
TwoIsland_Harbor_EventScript_Guide::
	lock
	faceplayer
	msgbox TwoIsland_Harbor_Text_Guide
	goto_if_eq VAR_ECHO_STAGE, 0, TwoIsland_Harbor_EventScript_GuideEnd
	msgbox TwoIsland_Harbor_Text_GuideCompass
	closemessage
	goto EventScript_EchoCompass
	end

TwoIsland_Harbor_EventScript_GuideEnd::
	release
	end

TwoIsland_Harbor_Text_Guide::
	.string "TWO ISLAND! Game corner by day,\n"
	.string "training cliffs at CAPE BRINK.\p"
	.string "The old League veterans still come\n"
	.string "here to walk the cliffs and think.\p"
	.string "You can sail to any island you\n"
	.string "like, in any order. I'll point\l"
	.string "you to the next ECHO.$"

TwoIsland_Harbor_Text_GuideCompass::
	.string "Let me check the TIME COMPASS\n"
	.string "with you…$"
