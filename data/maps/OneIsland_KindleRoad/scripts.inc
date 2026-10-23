OneIsland_KindleRoad_MapScripts::
	map_script MAP_SCRIPT_ON_TRANSITION, OneIsland_KindleRoad_OnTransition
	.byte 0

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
