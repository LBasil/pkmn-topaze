OneIsland_KindleRoad_MapScripts::
	map_script MAP_SCRIPT_ON_TRANSITION, OneIsland_KindleRoad_OnTransition
	map_script MAP_SCRIPT_ON_FRAME_TABLE, OneIsland_KindleRoad_OnFrame
	.byte 0

OneIsland_KindleRoad_OnFrame::
	map_script_2 VAR_TEMP_0, 0, OneIsland_KindleRoad_EventScript_DenExitSurf
	.2byte 0

@ Topaze: la bouche du repaire (6,124) donne sur la mer ; en sortant le joueur faisait un pas a pied sur l'eau (altitude 1) et restait coince
@ (impossible de rejoindre la terre, altitude 3). On le remet en Surf des qu'il touche l'eau a la sortie.
OneIsland_KindleRoad_EventScript_DenExitSurf::
	setvar VAR_TEMP_0, 1
	getplayerxy VAR_0x8008, VAR_0x8009
	goto_if_ne VAR_0x8008, 6, EventScript_Return
	goto_if_ne VAR_0x8009, 125, EventScript_Return
	special ForcePlayerToStartSurfing
	end

OneIsland_KindleRoad_OnTransition::
	end

OneIsland_KindleRoad_EventScript_RouteSign::
	msgbox OneIsland_KindleRoad_Text_RouteSign, MSGBOX_SIGN
	end

OneIsland_KindleRoad_EventScript_EmberSpaSign::
	msgbox OneIsland_KindleRoad_Text_EmberSpaSign, MSGBOX_SIGN
	end


@ Topaze: la bouche de grotte du repaire (6,124) reste fermee tant que Bill et les etincelles n'ont pas parle
OneIsland_KindleRoad_EventScript_DenLockedBill::
	lockall
	msgbox OneIsland_KindleRoad_Text_DenLockedBill
	applymovement LOCALID_PLAYER, OneIsland_KindleRoad_Movement_DenBack
	waitmovement 0
	releaseall
	end

OneIsland_KindleRoad_Movement_DenBack::
	walk_down
	step_end
