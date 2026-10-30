CeruleanCity_GlassHall_MapScripts::
	.byte 0


CeruleanCity_GlassHall_EventScript_Guide::
	msgbox CeruleanCity_GlassHall_Text_Guide, MSGBOX_NPC
	end

CeruleanCity_GlassHall_EventScript_Stairs::
	lockall
	goto_if_defeated TRAINER_BIKER_1, CeruleanCity_GlassHall_EventScript_StairsOpen
	releaseall
	end

CeruleanCity_GlassHall_EventScript_StairsOpen::
	warp MAP_CERULEAN_CAVE_1F, 0
	waitstate
	end
