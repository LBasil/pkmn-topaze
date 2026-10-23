SixIsland_Harbor_MapScripts::
	.byte 0

SixIsland_Harbor_EventScript_Sailor::
	lock
	faceplayer
	message Text_WhereDoYouWantToSail
	waitmessage
	setvar VAR_0x8004, SEAGALLOP_SIX_ISLAND
	goto EventScript_ChooseDestFromIsland
	end

@ Topaze: guide du port (post-game) : presente l'ile puis lit la boussole des Echos
SixIsland_Harbor_EventScript_Guide::
	lock
	faceplayer
	msgbox SixIsland_Harbor_Text_Guide
	goto_if_eq VAR_ECHO_STAGE, 0, SixIsland_Harbor_EventScript_GuideEnd
	msgbox SixIsland_Harbor_Text_GuideCompass
	closemessage
	goto EventScript_EchoCompass
	end

SixIsland_Harbor_EventScript_GuideEnd::
	release
	end

SixIsland_Harbor_Text_Guide::
	.string "SIX ISLAND. RUIN VALLEY hides the\n"
	.string "oldest stones of the world, and\l"
	.string "ALTERING CAVE hides odd visitors.\p"
	.string "They say the AURA first woke up\n"
	.string "somewhere around here.\p"
	.string "I can point you to the next ECHO.$"

SixIsland_Harbor_Text_GuideCompass::
	.string "Let me check the TIME COMPASS\n"
	.string "with you…$"
