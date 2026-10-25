SixIsland_DottedHole_1F_MapScripts::
	map_script MAP_SCRIPT_ON_TRANSITION, SixIsland_DottedHole_1F_OnTransition
	map_script MAP_SCRIPT_ON_FRAME_TABLE, SixIsland_DottedHole_1F_OnFrame
	.byte 0

SixIsland_DottedHole_1F_OnFrame::
	map_script_2 VAR_ECHO_STAGE, 16, SixIsland_DottedHole_1F_EventScript_ToStoneDen
	.2byte 0

@ Topaze: a l'etape de l'Echo 6, la porte de la VALLEE DES RUINES mene au repaire de REGIROCK
SixIsland_DottedHole_1F_EventScript_ToStoneDen::
	warp MAP_SIX_ISLAND_RUIN_VALLEY_STONE_DEN, 0, 9, 21
	waitstate
	end

SixIsland_DottedHole_1F_OnTransition::
	setworldmapflag FLAG_WORLD_MAP_SIX_ISLAND_DOTTED_HOLE_1F
	end

SixIsland_DottedHole_B1F_EventScript_BrailleUp::
	lockall
	braillemessage Braille_Text_Up
	waitbuttonpress
	releaseall
	end

SixIsland_DottedHole_B4F_EventScript_BrailleDown::
	lockall
	braillemessage Braille_Text_Down
	waitbuttonpress
	releaseall
	end

SixIsland_DottedHole_B3F_EventScript_BrailleRight::
	lockall
	braillemessage Braille_Text_Right
	waitbuttonpress
	releaseall
	end

SixIsland_DottedHole_B2F_EventScript_BrailleLeft::
	lockall
	braillemessage Braille_Text_Left
	waitbuttonpress
	releaseall
	end
