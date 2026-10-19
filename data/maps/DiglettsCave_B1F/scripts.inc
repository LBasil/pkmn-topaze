DiglettsCave_B1F_MapScripts::
	map_script MAP_SCRIPT_ON_TRANSITION, DiglettsCave_B1F_OnTransition
	.byte 0

DiglettsCave_B1F_OnTransition::
	setworldmapflag FLAG_WORLD_MAP_DIGLETTS_CAVE_B1F
	end

DiglettsCave_B1F_EventScript_ItemNugget::
	finditem ITEM_NUGGET
	end

DiglettsCave_B1F_EventScript_ItemPpUp::
	finditem ITEM_PP_UP
	end

DiglettsCave_B1F_EventScript_ItemMaxRevive::
	finditem ITEM_MAX_REVIVE
	end

DiglettsCave_B1F_EventScript_ItemMaxEther::
	finditem ITEM_MAX_ETHER
	end

DiglettsCave_B1F_EventScript_ItemElixir::
	finditem ITEM_ELIXIR
	end

DiglettsCave_B1F_EventScript_ItemUltraBall::
	finditem ITEM_ULTRA_BALL
	end
