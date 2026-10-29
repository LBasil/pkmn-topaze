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

@ Topaze: objets caches (panneaux a script, drapeaux hors plage moteur)
DiglettsCave_B1F_EventScript_TopazeFind0::
	lock
	goto_if_set FLAG_TOPAZE_HID_DIGLETTSCAVE_B1F_0, DiglettsCave_B1F_EventScript_TopazeFind0_Done
	checkitemspace ITEM_NUGGET, 1
	goto_if_eq VAR_RESULT, FALSE, DiglettsCave_B1F_EventScript_TopazeFind0_Full
	giveitem ITEM_NUGGET, 1
	setflag FLAG_TOPAZE_HID_DIGLETTSCAVE_B1F_0
	release
	end

DiglettsCave_B1F_EventScript_TopazeFind0_Done::
	release
	end

DiglettsCave_B1F_EventScript_TopazeFind0_Full::
	msgbox DiglettsCave_B1F_Text_TopazeFindFull
	release
	end

DiglettsCave_B1F_EventScript_TopazeFind1::
	lock
	goto_if_set FLAG_TOPAZE_HID_DIGLETTSCAVE_B1F_1, DiglettsCave_B1F_EventScript_TopazeFind1_Done
	checkitemspace ITEM_ULTRA_BALL, 1
	goto_if_eq VAR_RESULT, FALSE, DiglettsCave_B1F_EventScript_TopazeFind1_Full
	giveitem ITEM_ULTRA_BALL, 1
	setflag FLAG_TOPAZE_HID_DIGLETTSCAVE_B1F_1
	release
	end

DiglettsCave_B1F_EventScript_TopazeFind1_Done::
	release
	end

DiglettsCave_B1F_EventScript_TopazeFind1_Full::
	msgbox DiglettsCave_B1F_Text_TopazeFindFull
	release
	end


DiglettsCave_B1F_Text_TopazeFindFull::
	.string "Something shines here, but your BAG\n"
	.string "is full.$"
