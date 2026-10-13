Route1_MapScripts::
	map_script MAP_SCRIPT_ON_TRANSITION, Route1_OnTransition
	.byte 0

Route1_OnTransition::
	goto_if_unset FLAG_GRENALUX_ONYBRIS_STRIKE, Route1_HideAnimals
	goto_if_set FLAG_ONYBRIS_ANIMALS_FOUND, Route1_HideAnimals
	clearflag FLAG_HIDE_ROUTE1_ANIMALS
	end

Route1_HideAnimals::
	setflag FLAG_HIDE_ROUTE1_ANIMALS
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
	goto Route1_EventScript_AnimalsHome
	end

Route1_EventScript_Nidoranm::
	lock
	faceplayer
	waitse
	playmoncry SPECIES_NIDORAN_M, CRY_MODE_NORMAL
	msgbox Route1_Text_Nidoranm
	waitmoncry
	goto Route1_EventScript_AnimalsHome
	end

Route1_EventScript_Nidoranf::
	lock
	faceplayer
	waitse
	playmoncry SPECIES_NIDORAN_F, CRY_MODE_NORMAL
	msgbox Route1_Text_Nidoranf
	waitmoncry
	goto Route1_EventScript_AnimalsHome
	end

@ The three ranch animals gather and head home together.
Route1_EventScript_AnimalsHome::
	fadescreen FADE_TO_BLACK
	removeobject LOCALID_ROUTE1_DODUO
	removeobject LOCALID_ROUTE1_NIDORANM
	removeobject LOCALID_ROUTE1_NIDORANF
	setflag FLAG_HIDE_ROUTE1_ANIMALS
	setflag FLAG_ONYBRIS_ANIMALS_FOUND
	fadescreen FADE_FROM_BLACK
	msgbox Route1_Text_AnimalsHome
	release
	end
