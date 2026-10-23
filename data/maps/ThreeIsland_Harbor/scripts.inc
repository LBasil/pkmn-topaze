ThreeIsland_Harbor_MapScripts::
	.byte 0

ThreeIsland_Harbor_EventScript_Sailor::
	lock
	faceplayer
	message Text_WhereDoYouWantToSail
	waitmessage
	setvar VAR_0x8004, SEAGALLOP_THREE_ISLAND
	goto EventScript_ChooseDestFromIsland
	end

@ Topaze: guide du port (post-game) : presente l'ile puis lit la boussole des Echos
ThreeIsland_Harbor_EventScript_Guide::
	lock
	faceplayer
	msgbox ThreeIsland_Harbor_Text_Guide
	goto_if_eq VAR_ECHO_STAGE, 0, ThreeIsland_Harbor_EventScript_GuideEnd
	msgbox ThreeIsland_Harbor_Text_GuideCompass
	closemessage
	goto EventScript_EchoCompass
	end

ThreeIsland_Harbor_EventScript_GuideEnd::
	release
	end

ThreeIsland_Harbor_Text_Guide::
	.string "THREE ISLAND. Berry forest, long\n"
	.string "bridge, and old scars: the boss's\l"
	.string "people passed through here.\p"
	.string "The birds he caught were seen\n"
	.string "near this island before they\l"
	.string "vanished. Keep your eyes open.\p"
	.string "It rains here more than anywhere.\n"
	.string "SUICUNE was seen running over the\l"
	.string "water of the bridge.\p"
	.string "I can point you to the next ECHO.$"

ThreeIsland_Harbor_Text_GuideCompass::
	.string "Let me check the TIME COMPASS\n"
	.string "with you…$"
