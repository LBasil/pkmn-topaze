SevenIsland_Harbor_MapScripts::
	.byte 0

SevenIsland_Harbor_EventScript_Sailor::
	lock
	faceplayer
	message Text_WhereDoYouWantToSail
	waitmessage
	setvar VAR_0x8004, SEAGALLOP_SEVEN_ISLAND
	goto EventScript_ChooseDestFromIsland
	end

SevenIsland_Harbor_EventScript_Guide::
	lock
	faceplayer
	msgbox SevenIsland_Harbor_Text_Guide
	goto_if_eq VAR_ECHO_STAGE, 0, SevenIsland_Harbor_EventScript_GuideEnd
	msgbox SevenIsland_Harbor_Text_GuideCompass
	closemessage
	goto EventScript_EchoCompass
	end

SevenIsland_Harbor_EventScript_GuideEnd::
	release
	end

SevenIsland_Harbor_Text_Guide::
	.string "SEVEN ISLAND, the last one. SEVAULT\n"
	.string "CANYON, the TANOBY RUINS and the\l"
	.string "TRAINER TOWER wait here.\p"
	.string "The strongest travellers end up on\n"
	.string "this island sooner or later.\p"
	.string "Sky, sea and earth all meet in\n"
	.string "the canyon: that is why the legends\l"
	.string "of HOENN end up here.\p"
	.string "I can point you to the next ECHO.$"

SevenIsland_Harbor_Text_GuideCompass::
	.string "Let me check the TIME COMPASS\n"
	.string "with you…$"
