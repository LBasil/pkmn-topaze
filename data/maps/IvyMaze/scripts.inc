IvyMaze_MapScripts::
	.byte 0

IvyMaze_EventScript_ReturnFerry::
	lock
	faceplayer
	msgbox IvyMaze_Text_ReturnAsk, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, IvyMaze_EventScript_Stay
	warp MAP_FUCHSIA_CITY, 255, 24, 27
	waitstate
	end

IvyMaze_EventScript_Stay::
	msgbox IvyMaze_Text_Stay
	release
	end

IvyMaze_EventScript_Npc0::
	msgbox IvyMaze_Text_Npc0, MSGBOX_NPC
	end

IvyMaze_EventScript_Npc1::
	msgbox IvyMaze_Text_Npc1, MSGBOX_NPC
	end

