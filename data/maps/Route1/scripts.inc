Route1_MapScripts::
	map_script MAP_SCRIPT_ON_TRANSITION, Route1_OnTransition
	.byte 0

Route1_OnTransition::
	goto_if_unset FLAG_GRENALUX_ONYBRIS_STRIKE, Route1_HideAnimals
	goto_if_set FLAG_ONYBRIS_ANIMALS_FOUND, Route1_HideAnimals
	clearflag FLAG_HIDE_ROUTE1_DODUO
	clearflag FLAG_HIDE_ROUTE1_NIDORANM
	clearflag FLAG_HIDE_ROUTE1_NIDORANF
	goto_if_set FLAG_ROUTE1_TALKED_DODUO, Route1_HideDoduo
Route1_OnTransition_Nm::
	goto_if_set FLAG_ROUTE1_TALKED_NIDORANM, Route1_HideNidoranm
Route1_OnTransition_Nf::
	goto_if_set FLAG_ROUTE1_TALKED_NIDORANF, Route1_HideNidoranf
	end

Route1_HideDoduo::
	setflag FLAG_HIDE_ROUTE1_DODUO
	goto Route1_OnTransition_Nm

Route1_HideNidoranm::
	setflag FLAG_HIDE_ROUTE1_NIDORANM
	goto Route1_OnTransition_Nf

Route1_HideNidoranf::
	setflag FLAG_HIDE_ROUTE1_NIDORANF
	end

Route1_HideAnimals::
	setflag FLAG_HIDE_ROUTE1_DODUO
	setflag FLAG_HIDE_ROUTE1_NIDORANM
	setflag FLAG_HIDE_ROUTE1_NIDORANF
	end


Route1_EventScript_MartClerk::
	lock
	faceplayer
	goto_if_set FLAG_GOT_POTION_ON_ROUTE_1, Route1_EventScript_AlreadyGotPotion
	msgbox Route1_Text_WorkAtPokeMartTakeSample
	textcolor NPC_TEXT_COLOR_NEUTRAL
	checkitemspace ITEM_POTION
	goto_if_eq VAR_RESULT, FALSE, EventScript_BagIsFull
	bufferitemname STR_VAR_2, ITEM_POTION
	playfanfare MUS_LEVEL_UP
	message Text_ObtainedTheX
	waitmessage
	waitfanfare
	additem ITEM_POTION
	msgbox Route1_Text_PutPotionAway
	call EventScript_RestorePrevTextColor
	setflag FLAG_GOT_POTION_ON_ROUTE_1
	release
	end

Route1_EventScript_AlreadyGotPotion::
	msgbox Route1_Text_ComeSeeUsIfYouNeedPokeBalls
	release
	end

Route1_EventScript_Boy::
	msgbox Route1_Text_CanJumpFromLedges, MSGBOX_NPC
	end

Route1_EventScript_RouteSign::
	msgbox Route1_Text_RouteSign, MSGBOX_SIGN
	end

Route1_EventScript_Doduo::
	lock
	faceplayer
	waitse
	playmoncry SPECIES_DODUO, CRY_MODE_NORMAL
	msgbox Route1_Text_Doduo
	waitmoncry
	setflag FLAG_ROUTE1_TALKED_DODUO
	msgbox Route1_Text_AnimalLeaves
	fadescreen FADE_TO_BLACK
	removeobject LOCALID_ROUTE1_DODUO
	setflag FLAG_HIDE_ROUTE1_DODUO
	fadescreen FADE_FROM_BLACK
	goto Route1_EventScript_AnimalCheck
	end

Route1_EventScript_Nidoranm::
	lock
	faceplayer
	waitse
	playmoncry SPECIES_NIDORAN_M, CRY_MODE_NORMAL
	msgbox Route1_Text_Nidoranm
	waitmoncry
	setflag FLAG_ROUTE1_TALKED_NIDORANM
	msgbox Route1_Text_AnimalLeaves
	fadescreen FADE_TO_BLACK
	removeobject LOCALID_ROUTE1_NIDORANM
	setflag FLAG_HIDE_ROUTE1_NIDORANM
	fadescreen FADE_FROM_BLACK
	goto Route1_EventScript_AnimalCheck
	end

Route1_EventScript_Nidoranf::
	lock
	faceplayer
	waitse
	playmoncry SPECIES_NIDORAN_F, CRY_MODE_NORMAL
	msgbox Route1_Text_Nidoranf
	waitmoncry
	setflag FLAG_ROUTE1_TALKED_NIDORANF
	msgbox Route1_Text_AnimalLeaves
	fadescreen FADE_TO_BLACK
	removeobject LOCALID_ROUTE1_NIDORANF
	setflag FLAG_HIDE_ROUTE1_NIDORANF
	fadescreen FADE_FROM_BLACK
	goto Route1_EventScript_AnimalCheck
	end

Route1_EventScript_AnimalCheck::
	goto_if_unset FLAG_ROUTE1_TALKED_DODUO, Route1_EventScript_AnimalMore
	goto_if_unset FLAG_ROUTE1_TALKED_NIDORANM, Route1_EventScript_AnimalMore
	goto_if_unset FLAG_ROUTE1_TALKED_NIDORANF, Route1_EventScript_AnimalMore
	goto Route1_EventScript_AnimalsHome
	end

Route1_EventScript_AnimalMore::
	msgbox Route1_Text_AnimalMore
	release
	end

@ The last stray went home: the quest is done.
Route1_EventScript_AnimalsHome::
	setflag FLAG_ONYBRIS_ANIMALS_FOUND
	msgbox Route1_Text_AnimalsHome
	release
	end

Route1_EventScript_Walker::
	msgbox Route1_Text_Walker, MSGBOX_NPC
	end

@ Topaze: indice du temps deregle
Route1_EventScript_TimeHint::
	setflag FLAG_TOPAZE_CLOCK_1
	msgbox Route1_Text_TimeHint, MSGBOX_SIGN
	end
