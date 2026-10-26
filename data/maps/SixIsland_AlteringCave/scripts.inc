SixIsland_AlteringCave_MapScripts::
	map_script MAP_SCRIPT_ON_TRANSITION, SixIsland_AlteringCave_OnTransition
	.byte 0

SixIsland_AlteringCave_OnTransition::
	setworldmapflag FLAG_WORLD_MAP_SIX_ISLAND_ALTERING_CAVE
	random 9
	copyvar VAR_ALTERING_CAVE_WILD_SET, VAR_RESULT
	end

SixIsland_AlteringCave_EventScript_Item1::
	finditem ITEM_RARE_CANDY
	end

SixIsland_AlteringCave_EventScript_Item2::
	finditem ITEM_PP_UP
	end

SixIsland_AlteringCave_EventScript_Item3::
	finditem ITEM_MAX_ELIXIR
	end
