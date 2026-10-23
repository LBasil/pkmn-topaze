FiveIsland_Harbor_MapScripts::
	.byte 0

FiveIsland_Harbor_EventScript_Sailor::
	lock
	faceplayer
	message Text_WhereDoYouWantToSail
	waitmessage
	setvar VAR_0x8004, SEAGALLOP_FIVE_ISLAND
	goto EventScript_ChooseDestFromIsland
	end

@ Topaze: guide du port (post-game) : presente l'ile puis lit la boussole des Echos
FiveIsland_Harbor_EventScript_Guide::
	lock
	faceplayer
	msgbox FiveIsland_Harbor_Text_Guide
	goto_if_eq VAR_ECHO_STAGE, 0, FiveIsland_Harbor_EventScript_GuideEnd
	msgbox FiveIsland_Harbor_Text_GuideCompass
	closemessage
	goto EventScript_EchoCompass
	end

FiveIsland_Harbor_EventScript_GuideEnd::
	release
	end

FiveIsland_Harbor_Text_Guide::
	.string "FIVE ISLAND. The MEMORIAL PILLAR\n"
	.string "stands for every POKéMON that\l"
	.string "never came home.\p"
	.string "LOST CAVE is full of voices. Don't\n"
	.string "go in without a full team.\p"
	.string "I can point you to the next ECHO.$"

FiveIsland_Harbor_Text_GuideCompass::
	.string "Let me check the TIME COMPASS\n"
	.string "with you…$"
