
instance DIA_XARDAS_FIRSTEXIT(C_INFO)
{
	npc = none_100_xardas;
	nr = 999;
	condition = dia_xardas_firstexit_condition;
	information = dia_xardas_firstexit_info;
	permanent = FALSE;
	description = "Wyruszę w drogę najszybciej, jak się tylko da!";
};


func int dia_xardas_firstexit_condition()
{
	if(Npc_KnowsInfo(other,dia_xardas_todo) && (KAPITEL < 3))
	{
		return TRUE;
	};
};

func void dia_xardas_firstexit_info()
{
	AI_Output(other,self,"DIA_Xardas_FirstEXIT_15_00");	//Wyruszę w drogę najszybciej, jak się da!
	AI_Output(self,other,"DIA_Xardas_FirstEXIT_14_01");	//Świetnie! I jeszcze coś: nie zdradź nikomu, że ze mną rozmawiałeś. A już w żadnym wypadku nie mów o tym żadnemu magowi.
	AI_Output(self,other,"DIA_Xardas_FirstEXIT_14_02");	//Odkąd obrałem własną ścieżkę, Krąg Ognia ma mnie za zmarłego, i niech tak pozostanie.
	AI_StopProcessInfos(self);
	b_kapitelwechsel(1,NEWWORLD_ZEN);
	Npc_ExchangeRoutine(self,"START");
};


instance DIA_XARDAS_EXIT(C_INFO)
{
	npc = none_100_xardas;
	nr = 999;
	condition = dia_xardas_exit_condition;
	information = dia_xardas_exit_info;
	permanent = TRUE;
	description = DIALOG_ENDE;
};


func int dia_xardas_exit_condition()
{
	if(Npc_KnowsInfo(other,dia_xardas_firstexit) && (KAPITEL < 3))
	{
		return TRUE;
	};
};

func void dia_xardas_exit_info()
{
	AI_StopProcessInfos(self);
};


var int addon_zuerst;

instance DIA_XARDAS_HELLO(C_INFO)
{
	npc = none_100_xardas;
	nr = 1;
	condition = dia_xardas_hello_condition;
	information = dia_xardas_hello_info;
	permanent = FALSE;
	important = TRUE;
};


func int dia_xardas_hello_condition()
{
	return TRUE;
};

func void dia_xardas_hello_info()
{
	AI_Output(self,other,"DIA_Addon_Xardas_Hello_14_00");	//Aha! Jesteś już. A ja straciłem nadzieję, że się jeszcze kiedyś spotkamy.
	AI_Output(other,self,"DIA_Addon_Xardas_Hello_15_01");	//Czuję się... Czuję się, jakbym kilka tygodni leżał pod stertą głazów.
	AI_Output(self,other,"DIA_Addon_Xardas_Hello_14_02");	//Hmm... Dokładnie tak było. Życie zawdzięczasz tylko i wyłącznie swemu magicznemu pancerzowi.
	AI_Output(self,other,"DIA_Addon_Xardas_Hello_14_03");	//Bałem się, że nie zdołam cię wydostać z ruin świątyni...
	AI_Output(self,other,"DIA_Addon_Xardas_Hello_14_04");	//Ale dość już o tym.
	AI_Output(self,other,"DIA_Addon_Xardas_Hello_14_05");	//Musimy zająć się nowym niebezpieczeństwem grożącym tej okolicy.
	Info_ClearChoices(dia_xardas_hello);
	Info_AddChoice(dia_xardas_hello,"Mamy na to wystarczająco dużo czasu. Śniący został wygnany.",dia_addon_xardas_hello_dragons);
	Info_AddChoice(dia_xardas_hello,"O jakim NOWYM zagrożeniu mówisz?",dia_addon_xardas_hello_man);
};

func void dia_addon_xardas_hello_man()
{
	PlayVideo("Intro_ADDON");
	AI_Output(self,other,"DIA_Addon_Xardas_AddonIntro_Add_14_10");	//Musisz się z nimi sprzymierzyć! Tylko w ten sposób zdołamy powstrzymać Beliara!
	ADDON_ZUERST = TRUE;
};

func void dia_addon_xardas_hello_dragons()
{
	AI_Output(other,self,"DIA_Xardas_Hello_15_03");	//Mam na to wystarczająco dużo czasu. W końcu zwyciężyłem! Śniący został...
	AI_Output(self,other,"DIA_Xardas_Hello_14_04");	//...wygnany z naszego świata. Przepędziłeś go, to prawda, ale powstrzymanie nadciągającej wojny nie leży już w naszej mocy.
	AI_Output(self,other,"DIA_Xardas_Hello_14_07");	//Swym ostatnim krzykiem rozpaczy Śniący przywołał potężną armię zła.
	AI_Output(self,other,"DIA_Xardas_Hello_14_08");	//Był to wyraźny rozkaz dla wszystkich istot ciemności. Potężne słowo magii, któremu nie mogły odmówić.
	AI_Output(self,other,"DIA_Xardas_Hello_14_09");	//Jego ostatni rozkaz brzmiał 'PRZYBYWAJCIE'. I przybyły wszystkie... nawet smoki.
	AI_Output(other,self,"DIA_Xardas_Hello_15_10");	//Smoki!
	AI_Output(self,other,"DIA_Xardas_Hello_14_11");	//Tak, nawet te potężne, prastare istoty. Wyczuwam ich obecność także tutaj.
	AI_Output(self,other,"DIA_Xardas_Hello_14_12");	//Smoki zebrały wokół siebie liczną armię służących im istot.
	AI_Output(other,self,"DIA_Xardas_Hello_15_13");	//Gdzie jest teraz ta armia?
	AI_Output(self,other,"DIA_Xardas_Hello_14_14");	//Zaległa obozem całkiem blisko stąd, w Górniczej Dolinie, niedaleko Khorinis. Teraz przygotowuje się do ostatecznego ataku.
	if(ADDON_ZUERST == TRUE)
	{
		AI_Output(self,other,"DIA_Xardas_Hello_14_15");	//Zostało nam niewiele czasu.
	}
	else
	{
		AI_Output(self,other,"DIA_Addon_Xardas_Hello_Dragons_14_06");	//Ale to nie wszystko... Niedawno doszły mnie słuchy o jeszcze innym zagrożeniu.
		Info_ClearChoices(dia_xardas_hello);
		Info_AddChoice(dia_xardas_hello,"O jakim INNYM zagrożeniu mówisz?",dia_addon_xardas_hello_man);
	};
};


instance DIA_XARDAS_AWAY(C_INFO)
{
	npc = none_100_xardas;
	nr = 2;
	condition = dia_xardas_away_condition;
	information = dia_xardas_away_info;
	permanent = FALSE;
	description = "Zatem wynośmy się stąd czym prędzej!";
};


func int dia_xardas_away_condition()
{
	if(!Npc_KnowsInfo(other,dia_xardas_todo) && !Npc_KnowsInfo(other,dia_xardas_firstexit) && (KAPITEL < 3))
	{
		return TRUE;
	};
};

func void dia_xardas_away_info()
{
	AI_Output(other,self,"DIA_Xardas_AWAY_15_00");	//Zatem wynośmy się stąd czym prędzej!
	AI_Output(self,other,"DIA_Xardas_AWAY_14_01");	//Jeśli nawet zdołamy teraz uciec, smoki w końcu nas odnajdą.
	AI_Output(self,other,"DIA_Xardas_AWAY_14_02");	//Ale z pomocą tutejszych żołnierzy i magów, możemy je jeszcze powstrzymać, nim zbytnio urosną w siłę.
	AI_Output(self,other,"DIA_Xardas_AWAY_14_03");	//Lepszej szansy chyba już nie dostaniemy.
};


instance DIA_XARDAS_TODO(C_INFO)
{
	npc = none_100_xardas;
	nr = 1;
	condition = dia_xardas_todo_condition;
	information = dia_xardas_todo_info;
	permanent = FALSE;
	description = "Co możemy zrobić?";
};


func int dia_xardas_todo_condition()
{
	if(KAPITEL < 3)
	{
		return TRUE;
	};
};

func void dia_xardas_todo_info()
{
	AI_Output(other,self,"DIA_Xardas_TODO_15_00");	//Co możemy zrobić?
	AI_Output(self,other,"DIA_Xardas_TODO_14_01");	//Tym razem sami sobie nie poradzimy. W walce ze smokami może nam pomóc tylko moc Innosa.
	AI_Output(self,other,"DIA_Xardas_TODO_14_02");	//W pobliskim mieście Khorinis stacjonuje oddział paladynów.
	AI_Output(self,other,"DIA_Xardas_TODO_14_03");	//W ich posiadaniu znajduje się pewien potężny artefakt, dzięki któremu możemy pokonać paskudne gady.
	AI_Output(self,other,"DIA_Xardas_TODO_14_04");	//Nazywają go 'Okiem Innosa'. Musisz koniecznie zdobyć to Oko.
	AI_Output(self,other,"DIA_Xardas_TODO_14_05");	//Ostrzeż paladynów o smokach i za wszelką cenę przekonaj ich dowódcę, by nam pomógł.
	AI_Output(self,other,"DIA_Addon_Xardas_Add_14_07");	//Gdy tylko z nim porozmawiasz, musisz odszukać artefakt Beliara.
	AI_Output(self,other,"DIA_Addon_Xardas_Add_14_08");	//To odpowiednik Oka Innosa - nie wolno dopuścić, aby wpadł w ręce sług zła.
	Log_CreateTopic(TOPIC_INNOSEYE,LOG_MISSION);
	Log_SetTopicStatus(TOPIC_INNOSEYE,LOG_RUNNING);
	b_logentry(TOPIC_INNOSEYE,"W mieście Khorinis przebywa grupa paladynów. Mają ze sobą potężny artefakt, Oko Innosa, którego moc pomoże nam pokonać smoki. Muszę tylko przekonać paladynów, aby wsparli naszą sprawę.");
};


instance DIA_ADDON_XARDAS_STONEPLATE(C_INFO)
{
	npc = none_100_xardas;
	nr = 5;
	condition = dia_addon_xardas_stoneplate_condition;
	information = dia_addon_xardas_stoneplate_info;
	description = "Co mi możesz powiedzieć o tej kamiennej tablicy?";
};


func int dia_addon_xardas_stoneplate_condition()
{
	if(Npc_HasItems(other,itwr_stoneplatecommon_addon))
	{
		return TRUE;
	};
};

func void dia_addon_xardas_stoneplate_info()
{
	AI_Output(other,self,"DIA_Addon_Xardas_StonePlate_15_00");	//Co mi możesz powiedzieć o tej kamiennej tablicy?
	AI_Output(self,other,"DIA_Addon_Xardas_StonePlate_14_03");	//Sądziłem, że to jakiś magiczny artefakt. Okazało się jednak, że jej znaczenie jest znacznie mniejsze.
	AI_Output(self,other,"DIA_Addon_Xardas_StonePlate_14_04");	//Nie udało mi się do końca rozszyfrować wyrytych na niej znaków, ale wydają się one przekazywać historię prastarej kultury.
	AI_Output(self,other,"DIA_Addon_Xardas_StonePlate_14_05");	//Weź ją, jeśli chcesz, do niczego mi się nie przyda.
	b_giveplayerxp(XP_AMBIENT);
};


instance DIA_ADDON_XARDAS_PORTAL(C_INFO)
{
	npc = none_100_xardas;
	nr = 1;
	condition = dia_addon_xardas_portal_condition;
	information = dia_addon_xardas_portal_info;
	description = "Mag wody odkrył portal prowadzący do nieznanej dotąd części wyspy.";
};


func int dia_addon_xardas_portal_condition()
{
	if(Npc_KnowsInfo(other,dia_addon_saturas_whatsornament) && !c_schasbeliarsweapon() && (SATURAS_KLAUEINSMEER == FALSE))
	{
		return TRUE;
	};
};

func void dia_addon_xardas_portal_info()
{
	AI_Output(other,self,"DIA_Addon_Xardas_AddonSuccess_15_00");	//Mag Wody odkrył portal prowadzący do nieznanej dotąd części wyspy.
	AI_Output(self,other,"DIA_Addon_Xardas_AddonSuccess_14_01");	//To ciekawe...
	AI_Output(self,other,"DIA_Addon_Xardas_AddonSuccess_14_02");	//Zgłoś się do mnie, gdy tylko znajdziesz cokolwiek, co może nam naprawdę pomóc.
	AI_Output(self,other,"DIA_Addon_Xardas_AddonSuccess_14_03");	//Może ukryto tam artefakt Beliara? Odszukaj go!
};


instance DIA_ADDON_XARDAS_PORTALAGAIN(C_INFO)
{
	npc = none_100_xardas;
	nr = 1;
	condition = dia_addon_xardas_portalagain_condition;
	information = dia_addon_xardas_portalagain_info;
	permanent = TRUE;
	description = "Co do niezbadanej dotąd części wyspy...";
};


func int dia_addon_xardas_portalagain_condition()
{
	if(Npc_KnowsInfo(other,dia_addon_xardas_portal) && !c_schasbeliarsweapon() && (SATURAS_KLAUEINSMEER == FALSE))
	{
		return TRUE;
	};
};

func void dia_addon_xardas_portalagain_info()
{
	AI_Output(other,self,"DIA_Addon_Xardas_AddonSuccess_15_17");	//Co do niezbadanej dotąd części wyspy...
	AI_Output(self,other,"DIA_Addon_Xardas_AddonSuccess_14_18");	//Nie męcz mnie zbędnymi szczegółami. Wróć, gdy będziesz mieć coś przydatnego.
};


instance DIA_ADDON_XARDAS_ADDONSUCCESS(C_INFO)
{
	npc = none_100_xardas;
	nr = 1;
	condition = dia_addon_xardas_addonsuccess_condition;
	information = dia_addon_xardas_addonsuccess_info;
	description = "Przeszukałem nieznaną część wyspy.";
};


func int dia_addon_xardas_addonsuccess_condition()
{
	if(c_schasbeliarsweapon() || (SATURAS_KLAUEINSMEER == TRUE))
	{
		return TRUE;
	};
};

func void dia_addon_xardas_addonsuccess_info()
{
	AI_Output(other,self,"DIA_Addon_Xardas_AddonSuccess_15_03");	//Przeszukałem nieznaną część wyspy.
	AI_Output(self,other,"DIA_Addon_Xardas_AddonSuccess_14_04");	//Z jakim rezultatem?
	AI_Output(other,self,"DIA_Addon_Xardas_AddonSuccess_15_05");	//Wszystko wydaje się obracać wokół potężnego artefaktu znanego jako Szpon Beliara.
	AI_Output(self,other,"DIA_Addon_Xardas_AddonSuccess_14_06");	//Szpon Beliara? Gdzie on jest? Masz go przy sobie?
	if(c_schasbeliarsweapon())
	{
		AI_Output(other,self,"DIA_Addon_Xardas_AddonSuccess_15_07");	//Owszem.
		AI_Output(self,other,"DIA_Addon_Xardas_AddonSuccess_14_08");	//To bardzo ciekawe...
		AI_Output(self,other,"DIA_Addon_Xardas_AddonSuccess_14_09");	//Ta broń może się nam bardzo przydać, jest jednak również niezwykle niebezpieczna.
		AI_Output(self,other,"DIA_Addon_Xardas_AddonSuccess_14_10");	//Zachowaj ostrożność i pod żadnym pozorem jej nie zgub!
		b_giveplayerxp(XP_AMBIENT * 3);
	}
	else
	{
		AI_Output(other,self,"DIA_Addon_Xardas_AddonSuccess_15_11");	//Nie, już nie.
		AI_Output(other,self,"DIA_Addon_Xardas_AddonSuccess_15_12");	//Przekazałem go Magom Wody, aby wrzucili go do morza.
		AI_Output(self,other,"DIA_Addon_Xardas_AddonSuccess_14_13");	//Oszalałeś?! Wiesz chociaż, czego się pozbyłeś lekką ręką?!
		AI_Output(self,other,"DIA_Addon_Xardas_AddonSuccess_14_14");	//Ta broń mogła się nam ogromnie przysłużyć!
		AI_Output(other,self,"DIA_Addon_Xardas_AddonSuccess_15_15");	//Sądzę, że tak będzie lepiej.
		AI_Output(self,other,"DIA_Addon_Xardas_AddonSuccess_14_16");	//Niezbadane są wyroki bogów...
	};
};


instance DIA_XARDAS_WEAPON(C_INFO)
{
	npc = none_100_xardas;
	nr = 5;
	condition = dia_xardas_weapon_condition;
	information = dia_xardas_weapon_info;
	permanent = FALSE;
	description = "Potrzebuję broni.";
};


func int dia_xardas_weapon_condition()
{
	if(KAPITEL < 3)
	{
		return TRUE;
	};
};

func void dia_xardas_weapon_info()
{
	AI_Output(other,self,"DIA_Xardas_WEAPON_15_00");	//Potrzebuję broni.
	AI_Output(self,other,"DIA_Xardas_WEAPON_14_01");	//Mogę ci dać tylko to, co znajdziesz w mojej wieży.
	AI_Output(self,other,"DIA_Xardas_WEAPON_14_02");	//Rozejrzyj się tu trochę. Cokolwiek uznasz za przydatne, należy do ciebie.
};


instance DIA_XARDAS_ARTEFAKT(C_INFO)
{
	npc = none_100_xardas;
	nr = 2;
	condition = dia_xardas_artefakt_condition;
	information = dia_xardas_artefakt_info;
	permanent = FALSE;
	description = "Czym dokładnie jest 'Oko Innosa'?";
};


func int dia_xardas_artefakt_condition()
{
	if(Npc_KnowsInfo(other,dia_xardas_todo) && (KAPITEL < 3))
	{
		return TRUE;
	};
};

func void dia_xardas_artefakt_info()
{
	AI_Output(other,self,"DIA_Xardas_ARTEFAKT_15_00");	//Czym dokładnie jest 'Oko Innosa'?
	AI_Output(self,other,"DIA_Xardas_ARTEFAKT_14_01");	//To magiczny amulet. Legenda głosi, że sam Innos wlał weń część swojej boskiej mocy.
	AI_Output(self,other,"DIA_Xardas_ARTEFAKT_14_02");	//Dzięki niemu odzyskasz część dawnych sił i będziesz mógł stawić czoła smokom.
	AI_Output(self,other,"DIA_Xardas_ARTEFAKT_14_03");	//Oko ma też inne, tajemnicze właściwości, ale o nich opowiem ci, gdy już zdobędziesz amulet.
};


instance DIA_XARDAS_PALADIN(C_INFO)
{
	npc = none_100_xardas;
	nr = 3;
	condition = dia_xardas_paladin_condition;
	information = dia_xardas_paladin_info;
	permanent = FALSE;
	description = "Dlaczego paladyni mieliby mi dać Oko Innosa?";
};


func int dia_xardas_paladin_condition()
{
	if(Npc_KnowsInfo(other,dia_xardas_todo) && (KAPITEL < 3))
	{
		return TRUE;
	};
};

func void dia_xardas_paladin_info()
{
	AI_Output(other,self,"DIA_Xardas_PALADIN_15_00");	//Dlaczego paladyni mieliby mi dać Oko Innosa?
	AI_Output(self,other,"DIA_Xardas_PALADIN_14_01");	//Bo twoim przeznaczeniem jest nosić ten amulet.
	AI_Output(other,self,"DIA_Xardas_PALADIN_15_02");	//Skąd ta pewność?
	AI_Output(self,other,"DIA_Xardas_PALADIN_14_03");	//Jest kilka przesłanek. Najważniejszą z nich jest fakt, że pokonałeś Śniącego. Gdybyś nie był ulubieńcem bogów, już dawno byś nie żył.
	AI_Output(other,self,"DIA_Xardas_PALADIN_15_04");	//Załóżmy, że masz rację i rzeczywiście pisane mi jest posiadanie Oka Innosa. Jak mam o tym przekonać paladynów?
	AI_Output(self,other,"DIA_Xardas_PALADIN_14_05");	//Oko Innosa samo wybiera swojego posiadacza. Jeśli uda ci się je zdobyć i założyć, paladyni będą musieli uznać prawdziwość twoich słów.
};


instance DIA_XARDAS_KHORINIS(C_INFO)
{
	npc = none_100_xardas;
	nr = 4;
	condition = dia_xardas_khorinis_condition;
	information = dia_xardas_khorinis_info;
	permanent = FALSE;
	description = "Jak się dostać do miasta?";
};


func int dia_xardas_khorinis_condition()
{
	if(Npc_KnowsInfo(other,dia_xardas_todo) && (lothar.aivar[AIV_TALKEDTOPLAYER] == FALSE) && (KAPITEL < 3))
	{
		return TRUE;
	};
};

func void dia_xardas_khorinis_info()
{
	AI_Output(other,self,"DIA_Xardas_Khorinis_15_00");	//Jak się dostać do miasta?
	AI_Output(self,other,"DIA_Xardas_Khorinis_14_01");	//Idź po prostu w dół ścieżki prowadzącej od drzwi mojej wieży. Miasto jest duże, z pewnością je zauważysz.
	AI_Output(self,other,"DIA_Xardas_Khorinis_14_02");	//Tylko uważaj! Droga do miasta najeżona jest niebezpieczeństwami, a ty nie jesteś tak silny jak kiedyś.
};


instance DIA_XARDAS_WHEREEX(C_INFO)
{
	npc = none_100_xardas;
	nr = 6;
	condition = dia_xardas_whereex_condition;
	information = dia_xardas_whereex_info;
	permanent = FALSE;
	description = "Gdzie my w ogóle jesteśmy?";
};


func int dia_xardas_whereex_condition()
{
	if(Npc_KnowsInfo(other,dia_xardas_firstexit) && (KAPITEL < 3))
	{
		return TRUE;
	};
};

func void dia_xardas_whereex_info()
{
	AI_Output(other,self,"DIA_Xardas_Add_15_00");	//Gdzie my w ogóle jesteśmy?
	AI_Output(self,other,"DIA_Xardas_Add_14_01");	//Mówiłem ci już - niedaleko miasta Khorinis.
	AI_Output(self,other,"DIA_Xardas_Add_14_02");	//Odbudowałem tutaj moją wieżę.
	AI_Output(other,self,"DIA_Xardas_Add_15_03");	//Przecież nie minął miesiąc, odkąd widzieliśmy się w Górniczej Dolinie!
	AI_Output(self,other,"DIA_Xardas_Add_14_04");	//Słudzy, których wezwałem do budowy mojej wieży, uwinęli się bardzo sprawnie...
	AI_Output(other,self,"DIA_Xardas_Add_15_05");	//Trudno zaprzeczyć.
};


instance DIA_XARDAS_EQUIPMENT(C_INFO)
{
	npc = none_100_xardas;
	nr = 7;
	condition = dia_xardas_equipment_condition;
	information = dia_xardas_equipment_info;
	permanent = FALSE;
	description = "Gdzie mogę znaleźć lepsze wyposażenie?";
};


func int dia_xardas_equipment_condition()
{
	if(Npc_KnowsInfo(other,dia_xardas_weapon) && Npc_KnowsInfo(other,dia_xardas_firstexit) && (KAPITEL < 3))
	{
		return TRUE;
	};
};

func void dia_xardas_equipment_info()
{
	AI_Output(other,self,"DIA_Xardas_EQUIPMENT_15_00");	//Gdzie mogę znaleźć lepsze wyposażenie?
	AI_Output(self,other,"DIA_Xardas_EQUIPMENT_14_01");	//Jeśli chcesz kupić broń i pancerz, musisz pewnie udać się do Khorinis.
	AI_Output(self,other,"DIA_Xardas_EQUIPMENT_14_02");	//Ale w dolinie znajdziesz lecznicze zioła, które przywrócą ci siły utracone w walce.
	AI_Output(self,other,"DIA_Xardas_EQUIPMENT_14_03");	//Wybierz się też nad jezioro, tuż przed moją wieżą. Znajdziesz tam ukryte przejście do doliny.
};


instance DIA_XARDAS_ABOUTLESTER(C_INFO)
{
	npc = none_100_xardas;
	nr = 5;
	condition = dia_xardas_aboutlester_condition;
	information = dia_xardas_aboutlester_info;
	permanent = FALSE;
	description = "Rozmawiałeś już z Lesterem?";
};


func int dia_xardas_aboutlester_condition()
{
	if(Npc_KnowsInfo(other,dia_lester_send_xardas) && (Npc_GetDistToWP(lester,"NW_XARDAS_TOWER_IN1_31") <= 500) && (KAPITEL < 3))
	{
		return TRUE;
	};
};

func void dia_xardas_aboutlester_info()
{
	AI_Output(other,self,"DIA_Xardas_ABOUTLESTER_15_00");	//Rozmawiałeś już z Lesterem?
	AI_Output(self,other,"DIA_Xardas_ABOUTLESTER_14_01");	//Tak, zasypałem go pytaniami. Dużo się od niego dowiedziałem. Jest teraz kompletnie wyczerpany.
	AI_Output(self,other,"DIA_Xardas_ABOUTLESTER_14_02");	//To prawdziwy cud, że w ogóle przeżył tę ucieczkę. Kazałem mu trochę odpocząć.
	AI_Output(other,self,"DIA_Xardas_ABOUTLESTER_15_03");	//Czego się od niego dowiedziałeś?
	AI_Output(self,other,"DIA_Xardas_ABOUTLESTER_14_04");	//Niestety, niczego dobrego. Nie dość, że widział smoka, to spotkał też ludzi w czarnych kapturach.
	AI_Output(other,self,"DIA_Xardas_ABOUTLESTER_15_05");	//To takie ważne?
	AI_Output(self,other,"DIA_Xardas_ABOUTLESTER_14_06");	//Jeśli ci ludzie rzeczywiście istnieją, będą dla nas poważnym zagrożeniem.
	AI_Output(self,other,"DIA_Xardas_ABOUTLESTER_14_07");	//Niepokoi mnie to. Proszę, weź mój pierścień. Będzie cię chronił przed magią.
	b_giveinvitems(self,other,itri_prot_mage_01,1);
	b_giveplayerxp(XP_AMBIENT);
};


instance DIA_XARDAS_FIRSTPAL(C_INFO)
{
	npc = none_100_xardas;
	nr = 10;
	condition = dia_xardas_firstpal_condition;
	information = dia_xardas_firstpal_info;
	permanent = FALSE;
	description = "Byłem w mieście...";
};


func int dia_xardas_firstpal_condition()
{
	if((lothar.aivar[AIV_TALKEDTOPLAYER] == TRUE) && (lordhagen.aivar[AIV_TALKEDTOPLAYER] == FALSE) && (other.guild == GIL_NONE))
	{
		return TRUE;
	};
};

func void dia_xardas_firstpal_info()
{
	AI_Output(other,self,"DIA_Xardas_FirstPal_15_00");	//Byłem w mieście...
	AI_Output(self,other,"DIA_Xardas_FirstPal_14_01");	//Udało ci się porozmawiać z przywódcą paladynów?
	AI_Output(other,self,"DIA_Xardas_FirstPal_15_02");	//Nie. Nie chcą mnie dopuścić przed jego oblicze...
	AI_Output(self,other,"DIA_Xardas_FirstPal_14_03");	//Głupcy! Musi być jakiś sposób, byś do niego dotarł.
	AI_Output(self,other,"DIA_Xardas_FirstPal_14_04");	//Gdyby nie było innego wyjścia, dostań się do klasztoru i zostań magiem.
	AI_Output(self,other,"DIA_Xardas_FirstPal_14_05");	//Może to trochę moralnie dwuznaczne, ale przynajmniej osiągniesz swój cel.
	AI_Output(self,other,"DIA_Xardas_FirstPal_14_06");	//Gdybyś był magiem, przywódca paladynów musiałby się z tobą spotkać.
};


instance DIA_XARDAS_WEITER(C_INFO)
{
	npc = none_100_xardas;
	nr = 99;
	condition = dia_xardas_weiter_condition;
	information = dia_xardas_weiter_info;
	permanent = TRUE;
	description = "Więc co mam teraz robić?";
};


func int dia_xardas_weiter_condition()
{
	if(Npc_KnowsInfo(other,dia_xardas_firstexit) && (KAPITEL < 3))
	{
		return TRUE;
	};
};

func void dia_xardas_weiter_info()
{
	AI_Output(other,self,"DIA_Xardas_Weiter_15_00");	//Więc co mam teraz robić?
	AI_Output(self,other,"DIA_Xardas_Weiter_14_01");	//Postępujmy dalej zgodnie z planem. Chwilowo nie widzę innej drogi.
	AI_Output(self,other,"DIA_Xardas_Weiter_14_02");	//Postaraj się zdobyć Oko Innosa. Ja w tym czasie poszukam odpowiedzi na moje pytania.
};


instance DIA_XARDAS_KDFSECRET(C_INFO)
{
	npc = none_100_xardas;
	nr = 9;
	condition = dia_xardas_kdfsecret_condition;
	information = dia_xardas_kdfsecret_info;
	permanent = FALSE;
	description = "Dlaczego Krąg Ognia nie może się o tobie dowiedzieć?";
};


func int dia_xardas_kdfsecret_condition()
{
	if(Npc_KnowsInfo(other,dia_xardas_firstexit))
	{
		return TRUE;
	};
};

func void dia_xardas_kdfsecret_info()
{
	AI_Output(other,self,"DIA_Xardas_KdfSecret_15_00");	//Dlaczego Krąg Ognia nie może się o tobie dowiedzieć?
	AI_Output(self,other,"DIA_Xardas_KdfSecret_14_01");	//Kiedyś byłem wysoko w hierarchii kręgu. Jednak już wtedy podejrzewałem, że kluczem do Bariery jest magia demonów.
	AI_Output(self,other,"DIA_Xardas_KdfSecret_14_02");	//Oczywiście nigdy nie udało mi się przekonać o tym pozostałych magów.
	AI_Output(self,other,"DIA_Xardas_KdfSecret_14_03");	//Dlatego opuściłem Krąg i oddałem się badaniu tajemnic mrocznych sztuk.
	AI_Output(self,other,"DIA_Xardas_KdfSecret_14_04");	//To zbrodnia, której 'Bogobojni Wyznawcy Innosa', 'Dobrzy' i 'Cnotliwi' Magowie Ognia nigdy mi nie wybaczą.
	AI_Output(self,other,"DIA_Xardas_KdfSecret_14_05");	//Zapewne wiedzą, że wciąż żyję, ale nie mają pojęcia, gdzie mnie szukać. I niech tak pozostanie.
};


instance DIA_XARDAS_KAP3_EXIT(C_INFO)
{
	npc = none_100_xardas;
	nr = 999;
	condition = dia_xardas_kap3_exit_condition;
	information = dia_xardas_kap3_exit_info;
	permanent = TRUE;
	description = DIALOG_ENDE;
};


func int dia_xardas_kap3_exit_condition()
{
	if(KAPITEL == 3)
	{
		return TRUE;
	};
};

func void dia_xardas_kap3_exit_info()
{
	AI_StopProcessInfos(self);
};


instance DIA_XARDAS_BACKFROMOW(C_INFO)
{
	npc = none_100_xardas;
	nr = 31;
	condition = dia_xardas_backfromow_condition;
	information = dia_xardas_backfromow_info;
	description = "Wracam z Górniczej Doliny.";
};


func int dia_xardas_backfromow_condition()
{
	if(KAPITEL == 3)
	{
		return TRUE;
	};
};

func void dia_xardas_backfromow_info()
{
	AI_Output(other,self,"DIA_Xardas_BACKFROMOW_15_00");	//Wracam z Górniczej Doliny.
	AI_Output(self,other,"DIA_Xardas_BACKFROMOW_14_01");	//Najwyższy czas. Co tam widziałeś?
	AI_Output(other,self,"DIA_Xardas_BACKFROMOW_15_02");	//Miałeś rację. W dolinie stacjonuje potężna armia nieprzyjaciela.
	AI_Output(other,self,"DIA_Xardas_BACKFROMOW_15_03");	//Orkowie oblegają zamek, a smoki pustoszą okoliczne tereny.
	AI_Output(other,self,"DIA_Xardas_BACKFROMOW_15_04");	//Jeśli się nie mylę, wkrótce cała armia ruszy na Khorinis.
	b_giveplayerxp(XP_AMBIENT);
};


instance DIA_XARDAS_DMTSINDDA(C_INFO)
{
	npc = none_100_xardas;
	nr = 32;
	condition = dia_xardas_dmtsindda_condition;
	information = dia_xardas_dmtsindda_info;
	description = "Co się tu do diabła działo pod moją nieobecność?";
};


func int dia_xardas_dmtsindda_condition()
{
	if((KAPITEL == 3) && Npc_KnowsInfo(other,dia_xardas_backfromow))
	{
		return TRUE;
	};
};

func void dia_xardas_dmtsindda_info()
{
	if(Npc_KnowsInfo(other,dia_lester_backintown))
	{
		AI_Output(other,self,"DIA_Xardas_DMTSINDDA_15_00");	//Lester powiedział, że chcesz się ze mną widzieć.
	};
	AI_Output(other,self,"DIA_Xardas_DMTSINDDA_15_01");	//Co się tu do diabła działo pod moją nieobecność?
	AI_Output(self,other,"DIA_Xardas_DMTSINDDA_14_02");	//Nasz przeciwnik dowiedział się, kim jesteś naprawdę, i że zamierzasz zdobyć Oko Innosa.
	AI_Output(self,other,"DIA_Xardas_DMTSINDDA_14_03");	//Zdał sobie sprawę z zagrożenia, więc postanowił wyjść z ukrycia i zaatakować otwarcie.
	AI_Output(self,other,"DIA_Xardas_DMTSINDDA_14_04");	//Zabawa w chowanego już się skończyła. Jeszcze wczoraj nikt nie wiedział, z której strony nadejdzie cios. Dziś nie ma co do tego żadnych wątpliwości.
	b_logentry(TOPIC_INNOSEYE,"Wróg dowiedział się, że szukam Oka Innosa. Muszę je jak najszybciej znaleźć, zanim będzie za późno.");
	Info_ClearChoices(dia_xardas_dmtsindda);
	Info_AddChoice(dia_xardas_dmtsindda,"Zaatakowali mnie magowie w czarnych szatach.",dia_xardas_dmtsindda_dmt);
	Info_AddChoice(dia_xardas_dmtsindda,"Wreszcie udało mi się zdobyć dowód dla Lorda Hagena.",dia_xardas_dmtsindda_beweis);
};

func void dia_xardas_dmtsindda_dmt()
{
	AI_Output(other,self,"DIA_Xardas_DMTSINDDA_DMT_15_00");	//Zaatakowali mnie magowie w czarnych szatach.
	AI_Output(self,other,"DIA_Xardas_DMTSINDDA_DMT_14_01");	//Wróg ma wiele twarzy. Poszukiwacze to właśnie jedna z nich. Ale oni tylko przygotowują teren na przybycie prawdziwego przeciwnika.
	AI_Output(self,other,"DIA_Xardas_DMTSINDDA_DMT_14_02");	//Zajęli już pozycje w strategicznych miejscach. Teraz czekają tylko na dogodną okazję, by zacisnąć pętlę sideł.
	AI_Output(self,other,"DIA_Xardas_DMTSINDDA_DMT_14_03");	//Trzymaj się od nich z dala. To potężne, magiczne istoty, które za wszelką cenę spróbują cię powstrzymać.
	if(hero.guild == GIL_KDF)
	{
		Log_CreateTopic(TOPIC_DEMENTOREN,LOG_MISSION);
		Log_SetTopicStatus(TOPIC_DEMENTOREN,LOG_RUNNING);
		b_logentry(TOPIC_DEMENTOREN,"Xardas wie o odzianych na czarno mężczyznach. Wygląda na to, że tak naprawdę to Poszukiwacze pociągają za sznurki, i są bardzo niebezpiecznymi przeciwnikami.");
	};
};

func void dia_xardas_dmtsindda_beweis()
{
	AI_Output(other,self,"DIA_Xardas_DMTSINDDA_Beweis_15_00");	//Znalazłem wreszcie dowód, którego domagał się Lord Hagen.
	AI_Output(self,other,"DIA_Xardas_DMTSINDDA_Beweis_14_01");	//Co to za dowód?
	AI_Output(other,self,"DIA_Xardas_DMTSINDDA_Beweis_15_02");	//Otrzymałem list od Garonda, dowódcy paladynów w Górniczej Dolinie. Prosi w nim o posiłki.
	AI_Output(self,other,"DIA_Xardas_DMTSINDDA_Beweis_14_03");	//To powinno wystarczyć, by przekonać Hagena. Dobra robota.
	Info_AddChoice(dia_xardas_dmtsindda,"Co mam teraz robić?",dia_xardas_dmtsindda_dmt_whattodo);
	b_giveplayerxp(XP_AMBIENT);
};

func void dia_xardas_dmtsindda_dmt_whattodo()
{
	AI_Output(other,self,"DIA_Xardas_DMTSINDDA_DMT_WhatToDo_15_00");	//Co mam teraz robić?
	AI_Output(self,other,"DIA_Xardas_DMTSINDDA_DMT_WhatToDo_14_01");	//Zanieś Hagenowi list od Garonda. Z takim dowodem w ręku zostaniesz dopuszczony do Oka Innosa.
	AI_Output(self,other,"DIA_Xardas_DMTSINDDA_DMT_WhatToDo_14_02");	//Potem udaj się do Pyrokara. To on da ci Oko.
	AI_Output(self,other,"DIA_Xardas_DMTSINDDA_DMT_WhatToDo_14_03");	//Musisz koniecznie zabrać ten artefakt w bezpieczne miejsce.
	AI_Output(self,other,"DIA_Xardas_DMTSINDDA_DMT_WhatToDo_14_04");	//Idź już, zanim będzie za późno. Wróg też spróbuje zdobyć amulet dla siebie.
	b_logentry(TOPIC_INNOSEYE,"Oko znajduje się w klasztorze Magów Ognia. Mam nadzieję, że Lord Hagen pozwoli mi się do niego dostać, kiedy dostarczę mu wiadomość od Lorda Garonda. Mag Ognia Pyrokar nie dopuści mnie w pobliże amuletu, jeśli nie będę miał poparcia Hagena.");
};


instance DIA_XARDAS_INNOSEYEBROKEN(C_INFO)
{
	npc = none_100_xardas;
	nr = 33;
	condition = dia_xardas_innoseyebroken_condition;
	information = dia_xardas_innoseyebroken_info;
	description = "Oko Innosa zostało zniszczone.";
};


func int dia_xardas_innoseyebroken_condition()
{
	if((KAPITEL == 3) && Npc_KnowsInfo(other,dia_xardas_dmtsindda) && (Npc_HasItems(other,itmi_innoseye_broken_mis) || (MIS_SCKNOWSINNOSEYEISBROKEN == TRUE)))
	{
		return TRUE;
	};
};

func void dia_xardas_innoseyebroken_info()
{
	AI_Output(other,self,"DIA_Xardas_INNOSEYEBROKEN_15_00");	//Oko Innosa zostało zniszczone.
	AI_Output(self,other,"DIA_Xardas_INNOSEYEBROKEN_14_01");	//Jak to możliwe? Zniszczone?!
	AI_Output(other,self,"DIA_Xardas_INNOSEYEBROKEN_15_02");	//Znalazłem je w północnych lasach. Niestety, udało mi się odzyskać tylko kawałki.
	AI_Output(self,other,"DIA_Xardas_INNOSEYEBROKEN_14_03");	//To była nasza jedyna szansa na pokonanie tych smoków! Wszystko stracone.
	MIS_SCKNOWSINNOSEYEISBROKEN = TRUE;
	b_giveplayerxp(XP_AMBIENT);
	Info_ClearChoices(dia_xardas_innoseyebroken);
	Info_AddChoice(dia_xardas_innoseyebroken,"Co teraz?",dia_xardas_innoseyebroken_wasnun);
};

func void dia_xardas_innoseyebroken_wasnun()
{
	AI_Output(other,self,"DIA_Xardas_INNOSEYEBROKEN_wasnun_15_00");	//Co teraz?
	AI_Output(self,other,"DIA_Xardas_INNOSEYEBROKEN_wasnun_14_01");	//To straszliwy cios. Nieprędko się po nim podniesiemy. Muszę przemyśleć całą sprawę w spokoju.
	AI_Output(self,other,"DIA_Xardas_INNOSEYEBROKEN_wasnun_14_02");	//W międzyczasie powinieneś udać się do miasta i porozmawiać z Magiem Wody imieniem Vatras. Może on będzie wiedział, co wypada czynić dalej.
	b_logentry(TOPIC_INNOSEYE,"Xardas nie był zachwycony, kiedy dowiedział się, że Oko Innosa zostało zniszczone. Jedyną naszą nadzieją jest Vatras, Mag Wody z miasta Khorinis.");
	MIS_XARDAS_GOTOVATRASINNOSEYE = LOG_RUNNING;
};


instance DIA_XARDAS_RITUALREQUEST(C_INFO)
{
	npc = none_100_xardas;
	nr = 34;
	condition = dia_xardas_ritualrequest_condition;
	information = dia_xardas_ritualrequest_info;
	description = "Vatras przysłał mnie do ciebie.";
};


func int dia_xardas_ritualrequest_condition()
{
	if((MIS_RITUALINNOSEYEREPAIR == LOG_RUNNING) && Npc_KnowsInfo(other,dia_xardas_innoseyebroken) && (KAPITEL == 3))
	{
		return TRUE;
	};
};

func void dia_xardas_ritualrequest_info()
{
	AI_Output(other,self,"DIA_Xardas_RITUALREQUEST_15_00");	//Vatras przysłał mnie do ciebie.
	AI_Output(self,other,"DIA_Xardas_RITUALREQUEST_14_01");	//To dobrze. Co ci powiedział?
	AI_Output(other,self,"DIA_Xardas_RITUALREQUEST_15_02");	//Wspomniał coś o rytuale odwrócenia, który należy odprawić w Słonecznym Kręgu.
	AI_Output(self,other,"DIA_Xardas_RITUALREQUEST_14_03");	//Ten stary wyga! Chyba wiem, co planuje. Przybywasz, by przekazać mi jego zaproszenie?
	AI_Output(other,self,"DIA_Xardas_RITUALREQUEST_15_04");	//Na to wygląda. Kiedy wyruszysz?
	if((hero.guild == GIL_KDF) || (hero.guild == GIL_DJG) || (hero.guild == GIL_PAL))
	{
		AI_Output(self,other,"DIA_Xardas_RITUALREQUEST_14_05");	//Bezzwłocznie. Ty musisz jeszcze wypełnić swoje zadania. Potem znów się spotkamy.
		AI_StopProcessInfos(self);
		b_logentry(TOPIC_INNOSEYE,"Xardas zgodził się przyjść do Słonecznego Kręgu na rytuał.");
		b_giveplayerxp(XP_AMBIENT);
		Npc_ExchangeRoutine(self,"RitualInnosEyeRepair");
		XARDAS_GOESTORITUALINNOSEYE = TRUE;
	}
	else
	{
		AI_Output(self,other,"DIA_Xardas_RITUALREQUEST_14_06");	//Pomogę przy odprawianiu rytuału, dopiero gdy będę miał pewność, że jesteś gotów stawić czoła smokom.
	};
	b_giveplayerxp(XP_AMBIENT);
};


instance DIA_XARDAS_WARUMNICHTJETZT(C_INFO)
{
	npc = none_100_xardas;
	nr = 34;
	condition = dia_xardas_warumnichtjetzt_condition;
	information = dia_xardas_warumnichtjetzt_info;
	description = "Dlaczego nie pójdziesz do Vatrasa od razu?";
};


func int dia_xardas_warumnichtjetzt_condition()
{
	if(Npc_KnowsInfo(other,dia_xardas_ritualrequest) && (XARDAS_GOESTORITUALINNOSEYE == FALSE) && ((hero.guild == GIL_MIL) || (hero.guild == GIL_SLD)))
	{
		return TRUE;
	};
};

func void dia_xardas_warumnichtjetzt_info()
{
	AI_Output(other,self,"DIA_Xardas_WARUMNICHTJETZT_15_00");	//Dlaczego od razu nie pójdziesz do Vatrasa?
	AI_Output(other,self,"DIA_Xardas_WARUMNICHTJETZT_15_01");	//Czasem cię po prostu nie rozumiem.
	AI_Output(self,other,"DIA_Xardas_WARUMNICHTJETZT_14_02");	//Nigdy nie zwracaj się do mnie tym tonem! Gdyby nie JA, twoje szczątki gniłyby teraz w świątyni Śniącego!
	Info_AddChoice(dia_xardas_warumnichtjetzt,"Mniejsza z tym. Powiedz tylko, co mam zrobić.",dia_xardas_warumnichtjetzt_wastun);
	Info_AddChoice(dia_xardas_warumnichtjetzt,"Więc wyjaśnij mi chociaż, dlaczego się wahasz.",dia_xardas_warumnichtjetzt_grund);
};

func void dia_xardas_warumnichtjetzt_grund()
{
	AI_Output(other,self,"DIA_Xardas_WARUMNICHTJETZT_grund_15_00");	//Więc wyjaśnij mi chociaż, dlaczego się wahasz.
	AI_Output(self,other,"DIA_Xardas_WARUMNICHTJETZT_grund_14_01");	//Odkąd opuściłem Magów Ognia, starałem się trzymać od nich możliwie daleko.
	AI_Output(self,other,"DIA_Xardas_WARUMNICHTJETZT_grund_14_02");	//I nie zamierzam tego zmieniać, tak długo, jak to możliwe.
	AI_Output(self,other,"DIA_Xardas_WARUMNICHTJETZT_grund_14_03");	//Więc zanim znów stanę przed mymi dawnymi towarzyszami, chcę mieć absolutną pewność, że nie robię tego na darmo. Musisz być gotów do walki ze smokami!
	AI_Output(self,other,"DIA_Xardas_WARUMNICHTJETZT_grund_14_04");	//Z takim wyposażeniem daleko jednak nie zajdziesz. Wróć do mnie, gdy będziesz wystarczająco silny.
	AI_StopProcessInfos(self);
};

func void dia_xardas_warumnichtjetzt_wastun()
{
	AI_Output(other,self,"DIA_Xardas_WARUMNICHTJETZT_wastun_15_00");	//Mniejsza z tym. Powiedz tylko, co mam zrobić.
	AI_Output(self,other,"DIA_Xardas_WARUMNICHTJETZT_wastun_14_01");	//Jesteś jeszcze zbyt słaby, by zmierzyć się ze smokiem.
	AI_Output(self,other,"DIA_Xardas_WARUMNICHTJETZT_wastun_14_02");	//Wróć, gdy będziesz odpowiednio przygotowany. Wtedy udam się na spotkanie z Vatrasem.
	AI_StopProcessInfos(self);
};


instance DIA_XARDAS_BEREIT(C_INFO)
{
	npc = none_100_xardas;
	condition = dia_xardas_bereit_condition;
	information = dia_xardas_bereit_info;
	description = "Jestem gotów, by zmierzyć się ze smokami.";
};


func int dia_xardas_bereit_condition()
{
	if((XARDAS_GOESTORITUALINNOSEYE == FALSE) && Npc_KnowsInfo(other,dia_xardas_ritualrequest) && ((hero.guild == GIL_DJG) || (hero.guild == GIL_PAL)))
	{
		return TRUE;
	};
};

func void dia_xardas_bereit_info()
{
	AI_Output(other,self,"DIA_Xardas_BEREIT_15_00");	//Jestem gotów, by zmierzyć się ze smokami.
	AI_Output(self,other,"DIA_Xardas_BEREIT_14_01");	//Zatem nie ma czasu do stracenia. Natychmiast wyruszam w drogę do Słonecznego Kręgu. Wypełnij swoje zadania. Spotkamy się na miejscu.
	AI_StopProcessInfos(self);
	b_logentry(TOPIC_INNOSEYE,"Xardas zgodził się przyjść do Słonecznego Kręgu na rytuał.");
	b_giveplayerxp(XP_AMBIENT);
	Npc_ExchangeRoutine(self,"RitualInnosEyeRepair");
	XARDAS_GOESTORITUALINNOSEYE = TRUE;
};


instance DIA_XARDAS_BINGESPANNT(C_INFO)
{
	npc = none_100_xardas;
	nr = 35;
	condition = dia_xardas_bingespannt_condition;
	information = dia_xardas_bingespannt_info;
	permanent = TRUE;
	description = "Czy ten rytuał odwrócenia ma szansę się powieść?";
};


func int dia_xardas_bingespannt_condition()
{
	if((MIS_RITUALINNOSEYEREPAIR == LOG_RUNNING) && (KAPITEL == 3) && (XARDAS_GOESTORITUALINNOSEYE == TRUE))
	{
		return TRUE;
	};
};

func void dia_xardas_bingespannt_info()
{
	AI_Output(other,self,"DIA_Xardas_BINGESPANNT_15_00");	//Czy ten rytuał odwrócenia ma szansę się powieść?
	AI_Output(self,other,"DIA_Xardas_BINGESPANNT_14_01");	//Nie możemy mieć pewności. Wszystko zależy od szczegółów planu Vatrasa.
};


instance DIA_XARDAS_PYROWILLNICHT(C_INFO)
{
	npc = none_100_xardas;
	nr = 37;
	condition = dia_xardas_pyrowillnicht_condition;
	information = dia_xardas_pyrowillnicht_info;
	description = "Pyrokar nie chce się stawić na spotkanie.";
};


func int dia_xardas_pyrowillnicht_condition()
{
	if((PYROKAR_DENIESINNOSEYERITUAL == TRUE) && Npc_KnowsInfo(other,dia_xardas_ritualrequest) && (KAPITEL == 3))
	{
		return TRUE;
	};
};

func void dia_xardas_pyrowillnicht_info()
{
	AI_Output(other,self,"DIA_Xardas_PYROWILLNICHT_15_00");	//Pyrokar nie chce się stawić na spotkanie.
	AI_Output(other,self,"DIA_Xardas_PYROWILLNICHT_15_01");	//Domaga się dowodu, że można ci zaufać.
	AI_Output(self,other,"DIA_Xardas_PYROWILLNICHT_14_02");	//Czyżby? Pyrokar, tak? To ciekawe.
	AI_Output(self,other,"DIA_Xardas_PYROWILLNICHT_14_03");	//Ten stary cap zaczyna mnie irytować. Ale chyba mam tu coś, co może go przekonać.
	AI_Output(self,other,"DIA_Xardas_PYROWILLNICHT_14_04");	//Opuszczając Zakon Magów Ognia, zabrałem ze sobą kilka drobiazgów.
	AI_Output(self,other,"DIA_Xardas_PYROWILLNICHT_14_06");	//Nie chcę, by oddział paladynów i magów przetrząsnął moją wieżę i znalazł te rzeczy.
	AI_Output(self,other,"DIA_Xardas_PYROWILLNICHT_14_07");	//Dlatego ukryłem je w bezpiecznym miejscu, w którym magowie nigdy nie będą ich szukać.
	AI_Output(other,self,"DIA_Xardas_PYROWILLNICHT_15_08");	//Gdzie dokładnie?
	AI_Output(self,other,"DIA_Xardas_PYROWILLNICHT_14_09");	//Część z nich leży zamknięta w skrzyni na farmie Sekoba.
	SEKOB_ROOMFREE = TRUE;
	AI_Output(other,self,"DIA_Xardas_PYROWILLNICHT_15_10");	//Ufasz temu Sekobowi?
	AI_Output(self,other,"DIA_Xardas_PYROWILLNICHT_14_11");	//Nie, ale można go kupić, a wtedy nie zadaje niewygodnych pytań. Poza tym - skrzynia jest zamknięta. Oto klucz.
	CreateInvItems(self,itke_chest_sekob_xardasbook_mis,1);
	b_giveinvitems(self,other,itke_chest_sekob_xardasbook_mis,1);
	AI_Output(self,other,"DIA_Xardas_PYROWILLNICHT_14_12");	//Znajdziesz tam między innymi pewną starą księgę. Gdy Pyrokar ją zobaczy, będzie wiedział, że to prezent ode mnie.
	AI_Output(self,other,"DIA_Xardas_PYROWILLNICHT_14_13");	//Ja już nie będę miał z niej pożytku, więc przynajmniej tobie na coś się przyda.
	b_logentry(TOPIC_INNOSEYE,"Xardas dał mi klucz do kufra na farmie Sekoba. W środku znajdę książkę, którą mam wręczyć Pyrokarowi.");
};


instance DIA_XARDAS_RITUALINNOSEYEREPAIRIMPORTANT(C_INFO)
{
	npc = none_100_xardas;
	nr = 36;
	condition = dia_xardas_ritualinnoseyerepairimportant_condition;
	information = dia_xardas_ritualinnoseyerepairimportant_info;
	important = TRUE;
};


func int dia_xardas_ritualinnoseyerepairimportant_condition()
{
	if((MIS_RITUALINNOSEYEREPAIR == LOG_SUCCESS) && (KAPITEL == 3))
	{
		return TRUE;
	};
};

func void dia_xardas_ritualinnoseyerepairimportant_info()
{
	AI_Output(self,other,"DIA_Xardas_Add_14_06");	//Teraz, gdy Oko Innosa zostało naprawione, musisz stawić czoła smokom.
	AI_Output(self,other,"DIA_Xardas_Add_14_07");	//Wszystkie one są sługami Beliara, boga ciemności.
	AI_Output(self,other,"DIA_Xardas_Add_14_08");	//Ale bezpośrednie rozkazy muszą otrzymywać z tego świata. Tyle udało mi się do tej pory ustalić.
	AI_Output(self,other,"DIA_Xardas_Add_14_09");	//Dowiedz się, co jest źródłem ich potęgi.
	AI_Output(self,other,"DIA_Xardas_Add_14_10");	//Potem wracaj czym prędzej do mnie.
	Info_ClearChoices(dia_xardas_ritualinnoseyerepairimportant);
	Info_AddChoice(dia_xardas_ritualinnoseyerepairimportant,DIALOG_ENDE,dia_xardas_ritualinnoseyerepairimportant_weiter);
};

func void dia_xardas_ritualinnoseyerepairimportant_weiter()
{
	AI_StopProcessInfos(self);
	b_startotherroutine(xardas,"Start");
	b_startotherroutine(vatras,"Start");
};


instance DIA_XARDAS_WASNUN(C_INFO)
{
	npc = none_100_xardas;
	nr = 36;
	condition = dia_xardas_wasnun_condition;
	information = dia_xardas_wasnun_info;
	permanent = TRUE;
	description = "Oko Innosa zostało naprawione. Co teraz?";
};


func int dia_xardas_wasnun_condition()
{
	if((MIS_RITUALINNOSEYEREPAIR == LOG_SUCCESS) && (KAPITEL == 3))
	{
		return TRUE;
	};
};

func void dia_xardas_wasnun_info()
{
	AI_Output(other,self,"DIA_Xardas_WASNUN_15_00");	//Oko Innosa zostało naprawione. Co teraz?
	AI_Output(self,other,"DIA_Xardas_WASNUN_14_01");	//Pamiętaj, by zakładać je za każdym razem, gdy przyjdzie ci walczyć ze smokiem.
	if(MIS_READYFORCHAPTER4 == TRUE)
	{
		AI_Output(self,other,"DIA_Xardas_WASNUN_14_02");	//Nie trać czasu. Zejdź teraz do Górniczej Doliny i rozpraw się ze smokami.
	}
	else
	{
		AI_Output(self,other,"DIA_Xardas_WASNUN_14_03");	//Idź do Pyrokara. Niech ci wyjaśni, jak posługiwać się Okiem.
	};
};


instance DIA_XARDAS_KAP4_EXIT(C_INFO)
{
	npc = none_100_xardas;
	nr = 999;
	condition = dia_xardas_kap4_exit_condition;
	information = dia_xardas_kap4_exit_info;
	permanent = TRUE;
	description = DIALOG_ENDE;
};


func int dia_xardas_kap4_exit_condition()
{
	if(KAPITEL == 4)
	{
		return TRUE;
	};
};

func void dia_xardas_kap4_exit_info()
{
	AI_StopProcessInfos(self);
};


instance DIA_XARDAS_PERM4(C_INFO)
{
	npc = none_100_xardas;
	nr = 40;
	condition = dia_xardas_perm4_condition;
	information = dia_xardas_perm4_info;
	permanent = TRUE;
	description = "Co nowego?";
};


func int dia_xardas_perm4_condition()
{
	if(KAPITEL == 4)
	{
		return TRUE;
	};
};

func void dia_xardas_perm4_info()
{
	AI_Output(other,self,"DIA_Xardas_PERM4_15_00");	//Co nowego?
	AI_Output(self,other,"DIA_Xardas_PERM4_14_01");	//Poszukiwacze nadal kręcą się w pobliżu. Nie spoczną, póki nie przeciągną cię na swoją stronę.
	AI_Output(self,other,"DIA_Xardas_PERM4_14_02");	//Zabij smoki z Górniczej Doliny i dowiedz się, kto stoi za tymi atakami. W przeciwnym wypadku ich siła jeszcze wzrośnie!
};


instance DIA_XARDAS_KAP5_EXIT(C_INFO)
{
	npc = none_100_xardas;
	nr = 999;
	condition = dia_xardas_kap5_exit_condition;
	information = dia_xardas_kap5_exit_info;
	permanent = TRUE;
	description = DIALOG_ENDE;
};


func int dia_xardas_kap5_exit_condition()
{
	if(KAPITEL == 5)
	{
		return TRUE;
	};
};

func void dia_xardas_kap5_exit_info()
{
	AI_StopProcessInfos(self);
};


instance DIA_XARDAS_KAP6_EXIT(C_INFO)
{
	npc = none_100_xardas;
	nr = 999;
	condition = dia_xardas_kap6_exit_condition;
	information = dia_xardas_kap6_exit_info;
	permanent = TRUE;
	description = DIALOG_ENDE;
};


func int dia_xardas_kap6_exit_condition()
{
	if(KAPITEL == 6)
	{
		return TRUE;
	};
};

func void dia_xardas_kap6_exit_info()
{
	AI_StopProcessInfos(self);
};