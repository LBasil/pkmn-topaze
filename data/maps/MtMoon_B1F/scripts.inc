MtMoon_B1F_MapScripts::
	.byte 0

@ Topaze: objets caches (panneaux a script, drapeaux hors plage moteur)
MtMoon_B1F_EventScript_TopazeFind0::
	lock
	goto_if_set FLAG_TOPAZE_HID_MTMOON_B1F_0, MtMoon_B1F_EventScript_TopazeFind0_Done
	checkitemspace ITEM_REVIVE, 1
	goto_if_eq VAR_RESULT, FALSE, MtMoon_B1F_EventScript_TopazeFind0_Full
	giveitem ITEM_REVIVE, 1
	setflag FLAG_TOPAZE_HID_MTMOON_B1F_0
	release
	end

MtMoon_B1F_EventScript_TopazeFind0_Done::
	release
	end

MtMoon_B1F_EventScript_TopazeFind0_Full::
	msgbox MtMoon_B1F_Text_TopazeFindFull
	release
	end

MtMoon_B1F_EventScript_TopazeFind1::
	lock
	goto_if_set FLAG_TOPAZE_HID_MTMOON_B1F_1, MtMoon_B1F_EventScript_TopazeFind1_Done
	checkitemspace ITEM_ETHER, 1
	goto_if_eq VAR_RESULT, FALSE, MtMoon_B1F_EventScript_TopazeFind1_Full
	giveitem ITEM_ETHER, 1
	setflag FLAG_TOPAZE_HID_MTMOON_B1F_1
	release
	end

MtMoon_B1F_EventScript_TopazeFind1_Done::
	release
	end

MtMoon_B1F_EventScript_TopazeFind1_Full::
	msgbox MtMoon_B1F_Text_TopazeFindFull
	release
	end


MtMoon_B1F_Text_TopazeFindFull::
	.string "Something shines here, but your BAG\n"
	.string "is full.$"
