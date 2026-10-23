LavenderTown_MapScripts::
	map_script MAP_SCRIPT_ON_TRANSITION, LavenderTown_OnTransition
	.byte 0

LavenderTown_OnTransition::
	setworldmapflag FLAG_WORLD_MAP_LAVENDER_TOWN
	setvar VAR_MAP_SCENE_S_S_ANNE_2F_CORRIDOR, 1
	setflag FLAG_HIDE_SS_ANNE_RIVAL
	call_if_set FLAG_RESCUED_MR_FUJI, LavenderTown_EventScript_PoliceLeave
	end

LavenderTown_EventScript_PoliceLeave::
	setflag FLAG_TEMP_13
	setflag FLAG_TEMP_14
	return

LavenderTown_EventScript_Police::
	lock
	faceplayer
	goto_if_set FLAG_RESCUED_MR_FUJI, LavenderTown_EventScript_PoliceOpen
	msgbox LavenderTown_Text_PoliceClosed
	release
	end

LavenderTown_EventScript_PoliceOpen::
	msgbox LavenderTown_Text_PoliceOpen
	release
	end

LavenderTown_EventScript_LittleGirl::
	lock
	faceplayer
	msgbox LavenderTown_Text_DoYouBelieveInGhosts, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, YES, LavenderTown_EventScript_LittleGirlBelieve
	msgbox LavenderTown_Text_JustImaginingWhiteHand
	release
	end

LavenderTown_EventScript_LittleGirlBelieve::
	msgbox LavenderTown_Text_SoThereAreBelievers
	release
	end

LavenderTown_EventScript_WorkerM::
	msgbox LavenderTown_Text_TownKnownAsMonGraveSite, MSGBOX_NPC
	end

LavenderTown_EventScript_Boy::
	msgbox LavenderTown_Text_GhostsAppearedInTower, MSGBOX_NPC
	end

LavenderTown_EventScript_TownSign::
	msgbox LavenderTown_Text_TownSign, MSGBOX_SIGN
	end

LavenderTown_EventScript_SilphScopeNotice::
	msgbox LavenderTown_Text_SilphScopeNotice, MSGBOX_SIGN
	end

LavenderTown_EventScript_VolunteerHouseSign::
	msgbox LavenderTown_Text_VolunteerPokemonHouse, MSGBOX_SIGN
	end

LavenderTown_EventScript_PokemonTowerSign::
	msgbox LavenderTown_Text_PokemonTowerSign, MSGBOX_SIGN
	end

@ Topaze, fin 2 « Le Refuge » : poste 6/16 (FINN) — duel contre 2 chasseurs, recompense : Porygon
LavenderTown_EventScript_Refuge::
	lock
	faceplayer
	goto_if_ne VAR_TOPAZE_ENDING, 2, LavenderTown_EventScript_RefugeIdle
	goto_if_gt VAR_REFUGE_STAGE, 5, LavenderTown_EventScript_RefugeDone
	goto_if_lt VAR_REFUGE_STAGE, 5, LavenderTown_EventScript_RefugeEarly
	msgbox LavenderTown_Text_RefAsk
	setvar VAR_TOPAZE_BOOST, 44
	trainerbattle_no_intro TRAINER_GENTLEMAN_TUCKER, LavenderTown_Text_RefHunter1
	setvar VAR_TOPAZE_BOOST, 37
	trainerbattle_no_intro TRAINER_JUGGLER_KIRK, LavenderTown_Text_RefHunter2
	setvar VAR_TOPAZE_BOOST, 0
	special HealPlayerParty
	goto LavenderTown_EventScript_RefugeReward
	end

LavenderTown_EventScript_RefugeReward::
	msgbox LavenderTown_Text_RefGives
	givemon SPECIES_PORYGON, 0
	addvar VAR_REFUGE_STAGE, 1
	msgbox LavenderTown_Text_RefAfter
	release
	end

LavenderTown_EventScript_RefugeEarly::
	msgbox LavenderTown_Text_RefEarly
	release
	end

LavenderTown_EventScript_RefugeDone::
	msgbox LavenderTown_Text_RefDone
	release
	end

LavenderTown_EventScript_RefugeIdle::
	msgbox LavenderTown_Text_RefIdle
	release
	end

LavenderTown_EventScript_CellWitness::
	lock
	faceplayer
	goto_if_set FLAG_TOPAZE_CELL_LAVENDER, LavenderTown_EventScript_CellWitnessDone
	goto_if_defeated TRAINER_SCHOOL_KID_M, LavenderTown_EventScript_CellWitnessHalf
	msgbox LavenderTown_Text_CellWitness, MSGBOX_DEFAULT
	release
	end

LavenderTown_EventScript_CellWitnessHalf::
	msgbox LavenderTown_Text_CellWitnessHalf, MSGBOX_DEFAULT
	release
	end

LavenderTown_EventScript_CellWitnessDone::
	msgbox LavenderTown_Text_CellWitnessDone, MSGBOX_DEFAULT
	release
	end

LavenderTown_Text_CellWitness::
	.string "The tower bell rang by itself last"
	.string "night. Nobody climbed it.\p"
	.string "Since then, that house keeps its"
	.string "curtains shut, even at noon.$"

LavenderTown_Text_CellWitnessHalf::
	.string "You went in? Then you saw the set."
	.string "Look behind the crates.$"

LavenderTown_Text_CellWitnessDone::
	.string "The bell is quiet again.\p"
	.string "I think the dead are relieved. Or"
	.string "they are listening to someone else.$"
