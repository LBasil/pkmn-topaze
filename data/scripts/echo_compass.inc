@ Topaze: boussole des Echos (ITEM_VS_SEEKER en post-game) : indique la prochaine etape selon VAR_ECHO_STAGE
EventScript_EchoCompass::
	lockall
	goto_if_eq VAR_ECHO_STAGE, 1, EchoCompass_1
	goto_if_eq VAR_ECHO_STAGE, 2, EchoCompass_2
	goto_if_eq VAR_ECHO_STAGE, 3, EchoCompass_3
	goto_if_eq VAR_ECHO_STAGE, 4, EchoCompass_4
	goto_if_eq VAR_ECHO_STAGE, 5, EchoCompass_5
	goto_if_eq VAR_ECHO_STAGE, 6, EchoCompass_6
	goto_if_eq VAR_ECHO_STAGE, 7, EchoCompass_7
	goto_if_eq VAR_ECHO_STAGE, 8, EchoCompass_8
	goto_if_eq VAR_ECHO_STAGE, 9, EchoCompass_9
	goto_if_eq VAR_ECHO_STAGE, 10, EchoCompass_10
	goto_if_eq VAR_ECHO_STAGE, 11, EchoCompass_11
	goto_if_eq VAR_ECHO_STAGE, 12, EchoCompass_12
	goto_if_eq VAR_ECHO_STAGE, 13, EchoCompass_13
	goto_if_eq VAR_ECHO_STAGE, 14, EchoCompass_14
	goto_if_eq VAR_ECHO_STAGE, 15, EchoCompass_15
	goto_if_eq VAR_ECHO_STAGE, 16, EchoCompass_16
	goto_if_eq VAR_ECHO_STAGE, 17, EchoCompass_17
	goto_if_eq VAR_ECHO_STAGE, 18, EchoCompass_18
	goto_if_eq VAR_ECHO_STAGE, 19, EchoCompass_19
	goto_if_eq VAR_ECHO_STAGE, 20, EchoCompass_20
	goto_if_eq VAR_ECHO_STAGE, 21, EchoCompass_21
	msgbox EchoCompass_Text_Free
	releaseall
	end

EchoCompass_1::
	msgbox EchoCompass_Text_1
	releaseall
	end

EchoCompass_2::
	msgbox EchoCompass_Text_2
	releaseall
	end

EchoCompass_3::
	msgbox EchoCompass_Text_3
	releaseall
	end

EchoCompass_4::
	msgbox EchoCompass_Text_4
	releaseall
	end

EchoCompass_5::
	msgbox EchoCompass_Text_5
	releaseall
	end

EchoCompass_6::
	msgbox EchoCompass_Text_6
	releaseall
	end

EchoCompass_7::
	msgbox EchoCompass_Text_7
	releaseall
	end

EchoCompass_8::
	msgbox EchoCompass_Text_8
	releaseall
	end

EchoCompass_9::
	msgbox EchoCompass_Text_9
	releaseall
	end

EchoCompass_10::
	msgbox EchoCompass_Text_10
	releaseall
	end

EchoCompass_11::
	msgbox EchoCompass_Text_11
	releaseall
	end

EchoCompass_12::
	msgbox EchoCompass_Text_12
	releaseall
	end

EchoCompass_13::
	msgbox EchoCompass_Text_13
	releaseall
	end

EchoCompass_14::
	msgbox EchoCompass_Text_14
	releaseall
	end

EchoCompass_15::
	msgbox EchoCompass_Text_15
	releaseall
	end

EchoCompass_16::
	msgbox EchoCompass_Text_16
	releaseall
	end

EchoCompass_17::
	msgbox EchoCompass_Text_17
	releaseall
	end

EchoCompass_18::
	msgbox EchoCompass_Text_18
	releaseall
	end

EchoCompass_19::
	msgbox EchoCompass_Text_19
	releaseall
	end

EchoCompass_20::
	msgbox EchoCompass_Text_20
	releaseall
	end

EchoCompass_21::
	msgbox EchoCompass_Text_21
	releaseall
	end

EchoCompass_Text_Free::
    .string "The compass spins freely. The\n"
    .string "ECHOES are all closed.\p"
    .string "Legends now roam the islands.$"

EchoCompass_Text_1::
    .string "RAIKOU. Go north of the town on\n"
    .string "ONE ISLAND: KINDLE ROAD.$"

EchoCompass_Text_2::
    .string "The ECHO is closed. Report to\n"
    .string "CELIO, ONE ISLAND POKéMON CENTER.$"

EchoCompass_Text_3::
    .string "BILL has news for you at the\n"
    .string "ONE ISLAND POKéMON CENTER.$"

EchoCompass_Text_4::
    .string "ENTEI. Go to CAPE BRINK on\n"
    .string "TWO ISLAND.$"

EchoCompass_Text_5::
    .string "The ECHO is closed. Go see BILL\n"
    .string "at the ONE ISLAND POKéMON CENTER.$"

EchoCompass_Text_6::
    .string "CELIO has news for you at the\n"
    .string "ONE ISLAND POKéMON CENTER.$"

EchoCompass_Text_7::
    .string "SUICUNE. Cross the BOND BRIDGE\n"
    .string "on THREE ISLAND.$"

EchoCompass_Text_8::
    .string "The ECHO is closed. Go see CELIO\n"
    .string "at the ONE ISLAND POKéMON CENTER.$"

EchoCompass_Text_9::
    .string "LORELEI waits for you at her\n"
    .string "house on FOUR ISLAND.$"

EchoCompass_Text_10::
    .string "REGICE. Go to the ICEFALL CAVE\n"
    .string "on FOUR ISLAND, to the very back.$"

EchoCompass_Text_11::
    .string "The ECHO is closed. Go see LORELEI\n"
    .string "at her house on FOUR ISLAND.$"

EchoCompass_Text_12::
    .string "BILL has news for you at the\n"
    .string "ONE ISLAND POKéMON CENTER.$"

EchoCompass_Text_13::
    .string "REGISTEEL. Go to the MEADOW on\n"
    .string "FIVE ISLAND.$"

EchoCompass_Text_14::
    .string "The ECHO is closed. Go see BILL\n"
    .string "at the ONE ISLAND POKéMON CENTER.$"

EchoCompass_Text_15::
    .string "CELIO has news for you at the\n"
    .string "ONE ISLAND POKéMON CENTER.$"

EchoCompass_Text_16::
    .string "REGIROCK. Go to RUIN VALLEY on\n"
    .string "SIX ISLAND.$"

EchoCompass_Text_17::
    .string "The ECHO is closed. Go see CELIO\n"
    .string "at the ONE ISLAND POKéMON CENTER.$"

EchoCompass_Text_18::
    .string "BILL has news for you at the\n"
    .string "ONE ISLAND POKéMON CENTER.$"

EchoCompass_Text_19::
    .string "CELEBI. Go to SEVAULT CANYON on\n"
    .string "SEVEN ISLAND.$"

EchoCompass_Text_20::
    .string "The ECHO is closed. Go see BILL\n"
    .string "at the ONE ISLAND POKéMON CENTER.$"

EchoCompass_Text_21::
    .string "A strong signal on SEVEN ISLAND:\n"
    .string "SEVAULT CANYON, high on the cliffs.$"

