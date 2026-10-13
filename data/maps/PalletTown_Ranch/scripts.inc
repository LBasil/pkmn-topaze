PalletTown_Ranch_MapScripts::
	map_script MAP_SCRIPT_ON_TRANSITION, PalletTown_Ranch_OnTransition
	map_script MAP_SCRIPT_ON_LOAD, PalletTown_Ranch_OnLoad
	map_script MAP_SCRIPT_ON_FRAME_TABLE, PalletTown_Ranch_OnFrame
	.byte 0

PalletTown_Ranch_OnTransition::
	call_if_le VAR_GRENALUX_OPENING, 1, PalletTown_Ranch_EventScript_ShowOpeningNpcs
	call_if_gt VAR_GRENALUX_OPENING, 1, PalletTown_Ranch_EventScript_HideOpeningNpcs
	setflag FLAG_HIDE_RANCH_ANIMALS
	goto_if_unset FLAG_GRENALUX_ONYBRIS_STRIKE, PalletTown_Ranch_Peaceful
	goto_if_set FLAG_ONYBRIS_ANIMALS_FOUND, PalletTown_Ranch_ShowAnimals
	clearflag FLAG_HIDE_RANCH_CUT_HAND
	end

PalletTown_Ranch_Peaceful::
	clearflag FLAG_HIDE_RANCH_ANIMALS
	setflag FLAG_HIDE_RANCH_CUT_HAND
	end

PalletTown_Ranch_ShowAnimals::
	clearflag FLAG_HIDE_RANCH_ANIMALS
	clearflag FLAG_HIDE_RANCH_CUT_HAND
	end

PalletTown_Ranch_OnLoad::
	goto_if_set FLAG_GRENALUX_ONYBRIS_STRIKE, PalletTown_Ranch_CutFence
	end

PalletTown_Ranch_CutFence::
	setmetatile 27, 13, 0x001, FALSE
	setmetatile 27, 14, 0x001, FALSE
	end

PalletTown_Ranch_EventScript_Hand1::
	goto_if_set FLAG_GRENALUX_GEM_REWARD, PalletTown_Ranch_EventScript_Hand1Thanks
	goto_if_set FLAG_ONYBRIS_ANIMALS_FOUND, PalletTown_Ranch_EventScript_Hand1Reward
	goto_if_set FLAG_GRENALUX_ONYBRIS_STRIKE, PalletTown_Ranch_EventScript_Hand1Strike
	msgbox PalletTown_Ranch_Text_Hand1, MSGBOX_NPC
	end

PalletTown_Ranch_EventScript_Hand1Reward::
	lock
	faceplayer
	msgbox PalletTown_Ranch_Text_Hand1Reward
	giveitem_msg PalletTown_Ranch_Text_ReceivedPotion, ITEM_POTION
	giveitem_msg PalletTown_Ranch_Text_ReceivedBalls, ITEM_POKE_BALL, 5
	setflag FLAG_GRENALUX_GEM_REWARD
	msgbox PalletTown_Ranch_Text_Hand1Reward2
	release
	end

PalletTown_Ranch_EventScript_Hand1Thanks::
	msgbox PalletTown_Ranch_Text_Hand1Thanks, MSGBOX_NPC
	end

PalletTown_Ranch_EventScript_Hand1Strike::
	msgbox PalletTown_Ranch_Text_Hand1Strike, MSGBOX_NPC
	end

PalletTown_Ranch_EventScript_Hand2::
	goto_if_set FLAG_GRENALUX_ONYBRIS_STRIKE, PalletTown_Ranch_EventScript_Hand2Strike
	msgbox PalletTown_Ranch_Text_Hand2, MSGBOX_NPC
	end

PalletTown_Ranch_EventScript_Hand2Strike::
	msgbox PalletTown_Ranch_Text_Hand2Strike, MSGBOX_NPC
	end

PalletTown_Ranch_EventScript_Girl::
	msgbox PalletTown_Ranch_Text_Girl, MSGBOX_NPC
	end

PalletTown_Ranch_EventScript_Slowpoke::
	msgbox PalletTown_Ranch_Text_Slowpoke, MSGBOX_NPC
	end

PalletTown_Ranch_EventScript_Psyduck::
	msgbox PalletTown_Ranch_Text_Psyduck, MSGBOX_NPC
	end

PalletTown_Ranch_EventScript_Hand3::
	msgbox PalletTown_Ranch_Text_Hand3, MSGBOX_NPC
	end

PalletTown_Ranch_EventScript_Doduo::
	msgbox PalletTown_Ranch_Text_Doduo, MSGBOX_NPC
	end

PalletTown_Ranch_EventScript_Nidoranm::
	msgbox PalletTown_Ranch_Text_Nidoranm, MSGBOX_NPC
	end

PalletTown_Ranch_EventScript_Nidoranf::
	msgbox PalletTown_Ranch_Text_Nidoranf, MSGBOX_NPC
	end

PalletTown_Ranch_EventScript_Meowth::
	msgbox PalletTown_Ranch_Text_Meowth, MSGBOX_NPC
	end

PalletTown_Ranch_EventScript_Jigglypuff::
	msgbox PalletTown_Ranch_Text_Jigglypuff, MSGBOX_NPC
	end

PalletTown_Ranch_EventScript_BarnDoor::
	msgbox PalletTown_Ranch_Text_BarnDoor, MSGBOX_SIGN
	end

@ Topaze: opening scene at the outdoor RANCH. Calm talk -> ONYBRIS raid (2 grunts) -> urgent starter choice -> battles -> MOM and the pendant
PalletTown_Ranch_OnFrame::
	map_script_2 VAR_GRENALUX_OPENING, 0, PalletTown_Ranch_EventScript_OpeningScene
	map_script_2 VAR_GRENALUX_OPENING, 1, PalletTown_Ranch_EventScript_OpeningScene
	.2byte 0

PalletTown_Ranch_EventScript_OpeningScene::
	lockall
	textcolor NPC_TEXT_COLOR_MALE
	getplayerxy VAR_0x8004, VAR_0x8005
	call_if_eq VAR_0x8005, 6, PalletTown_Ranch_EventScript_WalkInRow6
	call_if_ne VAR_0x8005, 6, PalletTown_Ranch_EventScript_WalkInRow7
	applymovement LOCALID_RANCH_RIVAL, Common_Movement_WalkInPlaceFasterUp
	waitmovement 0
	msgbox PalletTown_Text_RanchDadHello
	applymovement LOCALID_RANCH_OAK, Common_Movement_WalkInPlaceFasterRight
	waitmovement 0
	msgbox PalletTown_Text_RanchOakIntro
	closemessage
	playse SE_PIN
	delay 40
	msgbox PalletTown_Text_RanchTrackersHowl
	closemessage
	clearflag FLAG_HIDE_RANCH_GRUNT
	clearflag FLAG_HIDE_RANCH_GRUNT2
	addobject LOCALID_RANCH_GRUNT
	addobject LOCALID_RANCH_GRUNT2
	playse SE_EXIT
	applymovement LOCALID_RANCH_GRUNT, PalletTown_Ranch_Movement_GruntsArrive
	applymovement LOCALID_RANCH_GRUNT2, PalletTown_Ranch_Movement_GruntsArrive
	waitmovement 0
	msgbox PalletTown_Text_RanchGruntEnter
	closemessage
	msgbox PalletTown_Text_RanchDadFlees
	closemessage
	applymovement LOCALID_RANCH_FATHER, PalletTown_Ranch_Movement_FatherRunsOut
	waitmovement 0
	removeobject LOCALID_RANCH_FATHER
	applymovement LOCALID_RANCH_GRUNT, PalletTown_Ranch_Movement_GruntsStep
	applymovement LOCALID_RANCH_GRUNT2, PalletTown_Ranch_Movement_GruntsStep
	waitmovement 0
	applymovement LOCALID_RANCH_OAK, Common_Movement_ExclamationMark
	waitmovement 0
	msgbox PalletTown_Text_RanchOakPanic
	closemessage
PalletTown_Ranch_EventScript_ChooseStarter::
	message PalletTown_Text_RanchOakChoose
	waitmessage
	multichoice 0, 0, MULTICHOICE_TOPAZE_STARTER, FALSE
	goto_if_ge VAR_RESULT, 3, PalletTown_Ranch_EventScript_ChooseStarter
	copyvar VAR_TEMP_2, VAR_RESULT
	goto_if_eq VAR_TEMP_2, 0, PalletTown_Ranch_EventScript_StarterIsBulbasaur
	goto_if_eq VAR_TEMP_2, 1, PalletTown_Ranch_EventScript_StarterIsSquirtle
	goto PalletTown_Ranch_EventScript_StarterIsCharmander
	end

PalletTown_Ranch_EventScript_StarterIsBulbasaur::
	setvar VAR_TEMP_3, SPECIES_BULBASAUR
	showmonpic SPECIES_BULBASAUR, 10, 3
	msgbox PalletTown_ProfessorOaksLab_Text_OakChoosingBulbasaur, MSGBOX_YESNO
	goto PalletTown_Ranch_EventScript_ConfirmStarter
	end

PalletTown_Ranch_EventScript_StarterIsSquirtle::
	setvar VAR_TEMP_3, SPECIES_SQUIRTLE
	showmonpic SPECIES_SQUIRTLE, 10, 3
	msgbox PalletTown_ProfessorOaksLab_Text_OakChoosingSquirtle, MSGBOX_YESNO
	goto PalletTown_Ranch_EventScript_ConfirmStarter
	end

PalletTown_Ranch_EventScript_StarterIsCharmander::
	setvar VAR_TEMP_3, SPECIES_CHARMANDER
	showmonpic SPECIES_CHARMANDER, 10, 3
	msgbox PalletTown_ProfessorOaksLab_Text_OakChoosingCharmander, MSGBOX_YESNO
	goto PalletTown_Ranch_EventScript_ConfirmStarter
	end

PalletTown_Ranch_EventScript_ConfirmStarter::
	goto_if_eq VAR_RESULT, NO, PalletTown_Ranch_EventScript_DeclinedStarter
	hidemonpic
	msgbox PalletTown_ProfessorOaksLab_Text_OakThisMonIsEnergetic
	call EventScript_RestorePrevTextColor
	setflag FLAG_SYS_POKEMON_GET
	setflag FLAG_PALLET_LADY_NOT_BLOCKING_SIGN
	givemon VAR_TEMP_3, 5
	copyvar VAR_STARTER_MON, VAR_TEMP_2
	bufferspeciesname STR_VAR_1, VAR_TEMP_3
	message PalletTown_ProfessorOaksLab_Text_ReceivedMonFromOak
	waitmessage
	playfanfare MUS_OBTAIN_KEY_ITEM
	waitfanfare
	msgbox Text_GiveNicknameToThisMon, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, PalletTown_Ranch_EventScript_AfterStarter
	setvar VAR_0x8004, 0
	call EventScript_ChangePokemonNickname
	goto PalletTown_Ranch_EventScript_AfterStarter
	end

PalletTown_Ranch_EventScript_DeclinedStarter::
	hidemonpic
	goto PalletTown_Ranch_EventScript_ChooseStarter
	end

PalletTown_Ranch_EventScript_AfterStarter::
	closemessage
	msgbox PalletTown_Text_RanchRivalTakes
	closemessage
	applymovement LOCALID_RANCH_RIVAL, Common_Movement_WalkInPlaceFasterRight
	waitmovement 0
	msgbox PalletTown_Text_RanchRivalChallenge
	closemessage
	msgbox PalletTown_Text_RanchGrunt2Taunt
	closemessage
	msgbox PalletTown_Text_RanchGruntChallenge
	closemessage
	trainerbattle_earlyrival TRAINER_TEAM_ROCKET_GRUNT_22, RIVAL_BATTLE_TUTORIAL, PalletTown_Text_OnybrisGruntDefeat, PalletTown_Text_OnybrisGruntVictory
	special HealPlayerParty
	msgbox PalletTown_Text_RanchRivalWin
	closemessage
	msgbox PalletTown_Text_RanchGruntRetreat
	closemessage
	applymovement LOCALID_RANCH_GRUNT, PalletTown_Ranch_Movement_GruntsLeave
	applymovement LOCALID_RANCH_GRUNT2, PalletTown_Ranch_Movement_GruntsLeave
	waitmovement 0
	removeobject LOCALID_RANCH_GRUNT
	removeobject LOCALID_RANCH_GRUNT2
	setflag FLAG_HIDE_RANCH_GRUNT
	setflag FLAG_HIDE_RANCH_GRUNT2
	msgbox PalletTown_Text_RanchOakAfter
	closemessage
	fadescreen FADE_TO_BLACK
	removeobject LOCALID_RANCH_OAK
	removeobject LOCALID_RANCH_RIVAL
	setflag FLAG_HIDE_RANCH_SCENE
	delay 30
	clearflag FLAG_HIDE_RANCH_MOM
	addobject LOCALID_RANCH_MOM
	fadescreen FADE_FROM_BLACK
	applymovement LOCALID_RANCH_MOM, PalletTown_Ranch_Movement_MomRunsIn
	applymovement LOCALID_PLAYER, Common_Movement_WalkInPlaceFasterLeft
	waitmovement 0
	msgbox PalletTown_Text_RanchMom1
	closemessage
	giveitem_msg PalletTown_Text_ReceivedPendant, ITEM_RUBY, 1, MUS_OBTAIN_KEY_ITEM
	msgbox PalletTown_Text_RanchMom2
	closemessage
	fadescreen FADE_TO_BLACK
	removeobject LOCALID_RANCH_MOM
	setflag FLAG_HIDE_RANCH_MOM
	@ the raid hits the whole town: ranch, school and lab
	setflag FLAG_GRENALUX_ONYBRIS_STRIKE
	setflag FLAG_HIDE_BULBASAUR_BALL
	setflag FLAG_HIDE_SQUIRTLE_BALL
	setflag FLAG_HIDE_CHARMANDER_BALL
	setflag FLAG_HIDE_RIVAL_IN_LAB
	setvar VAR_GRENALUX_OPENING, 2
	fadescreen FADE_FROM_BLACK
	releaseall
	end

PalletTown_Ranch_EventScript_WalkInRow6::
	applymovement LOCALID_PLAYER, PalletTown_Ranch_Movement_PlayerWalkInRow6
	waitmovement 0
	return

PalletTown_Ranch_EventScript_WalkInRow7::
	applymovement LOCALID_PLAYER, PalletTown_Ranch_Movement_PlayerWalkInRow7
	waitmovement 0
	return

PalletTown_Ranch_Movement_PlayerWalkInRow6::
	walk_right
	walk_right
	walk_right
	walk_right
	walk_right
	walk_right
	walk_right
	walk_right
	walk_right
	walk_right
	walk_right
	walk_in_place_faster_right
	step_end

PalletTown_Ranch_Movement_PlayerWalkInRow7::
	walk_up
	walk_right
	walk_right
	walk_right
	walk_right
	walk_right
	walk_right
	walk_right
	walk_right
	walk_right
	walk_right
	walk_right
	walk_in_place_faster_right
	step_end

PalletTown_Ranch_Movement_GruntsArrive::
	walk_left
	walk_left
	walk_left
	walk_left
	walk_left
	step_end

PalletTown_Ranch_Movement_GruntsStep::
	walk_left
	walk_left
	step_end

PalletTown_Ranch_Movement_FatherRunsOut::
	walk_down
	walk_down
	walk_down
	step_end

PalletTown_Ranch_Movement_GruntsLeave::
	walk_right
	walk_right
	walk_right
	walk_right
	walk_right
	walk_right
	walk_right
	walk_right
	step_end

PalletTown_Ranch_Movement_MomRunsIn::
	walk_right
	walk_right
	walk_right
	walk_right
	walk_right
	walk_right
	walk_right
	walk_right
	walk_right
	walk_in_place_faster_right
	step_end

PalletTown_Ranch_EventScript_ShowOpeningNpcs::
	setobjectxyperm LOCALID_PALLET_RANCH_HAND1, 6, 9
	clearflag FLAG_HIDE_RANCH_SCENE
	setflag FLAG_HIDE_RANCH_GRUNT
	setflag FLAG_HIDE_RANCH_GRUNT2
	setflag FLAG_HIDE_RANCH_MOM
	return

PalletTown_Ranch_EventScript_HideOpeningNpcs::
	setobjectxyperm LOCALID_PALLET_RANCH_HAND1, 9, 7
	setflag FLAG_HIDE_RANCH_SCENE
	setflag FLAG_HIDE_RANCH_GRUNT
	setflag FLAG_HIDE_RANCH_GRUNT2
	setflag FLAG_HIDE_RANCH_MOM
	return
