SevenIsland_SevaultCanyon_Grove_MapScripts::
	map_script MAP_SCRIPT_ON_TRANSITION, SevenIsland_SevaultCanyon_Grove_OnTransition
	.byte 0

SevenIsland_SevaultCanyon_Grove_OnTransition::
	setflag FLAG_TEMP_11
	setflag FLAG_TEMP_14
	setflag FLAG_TEMP_1E
	setflag FLAG_TEMP_1F
	call_if_eq VAR_ECHO_STAGE, 22, SevenIsland_SevaultCanyon_EventScript_ShowWardens
	end
