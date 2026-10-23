FourIsland_Harbor_MapScripts::
	.byte 0

FourIsland_Harbor_EventScript_Sailor::
	lock
	faceplayer
	message Text_WhereDoYouWantToSail
	waitmessage
	setvar VAR_0x8004, SEAGALLOP_FOUR_ISLAND
	goto EventScript_ChooseDestFromIsland
	end

@ Topaze: guide du port (post-game) : presente l'ile puis lit la boussole des Echos
FourIsland_Harbor_EventScript_Guide::
	lock
	faceplayer
	msgbox FourIsland_Harbor_Text_Guide
	goto_if_eq VAR_ECHO_STAGE, 0, FourIsland_Harbor_EventScript_GuideEnd
	msgbox FourIsland_Harbor_Text_GuideCompass
	closemessage
	goto EventScript_EchoCompass
	end

FourIsland_Harbor_EventScript_GuideEnd::
	release
	end

FourIsland_Harbor_Text_Guide::
	.string "FOUR ISLAND! Snow, ice, and ICEFALL\n"
	.string "CAVE. LORELEI's old house is just\l"
	.string "up the path.\p"
	.string "The cold here is older than the\n"
	.string "island itself, they say.\p"
	.string "REGICE sleeps deep in ICEFALL CAVE,\n"
	.string "made of ice that never melted.\p"
	.string "I can point you to the next ECHO.$"

FourIsland_Harbor_Text_GuideCompass::
	.string "Let me check the TIME COMPASS\n"
	.string "with you…$"
