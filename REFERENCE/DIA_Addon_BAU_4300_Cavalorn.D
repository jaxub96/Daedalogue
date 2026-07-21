
func int c_bragobanditsdead()
{
	if((Npc_IsDead(ambusher_1013) || (BDT_1013_AWAY == TRUE)) && Npc_IsDead(ambusher_1014) && Npc_IsDead(ambusher_1015))
	{
		return TRUE;
	};
};


instance DIA_ADDON_CAVALORN_EXIT(C_INFO)
{
	npc = bau_4300_addon_cavalorn;
	nr = 999;
	condition = dia_addon_cavalorn_exit_condition;
	information = dia_addon_cavalorn_exit_info;
	permanent = TRUE;
	description = DIALOG_ENDE;
};


func int dia_addon_cavalorn_exit_condition()
{
	return TRUE;
};

func void dia_addon_cavalorn_exit_info()
{
	AI_StopProcessInfos(self);
};


instance DIA_ADDON_CAVALORN_PICKPOCKET(C_INFO)
{
	npc = bau_4300_addon_cavalorn;
	nr = 900;
	condition = dia_addon_cavalorn_pickpocket_condition;
	information = dia_addon_cavalorn_pickpocket_info;
	permanent = TRUE;
	description = "(Kradzież tego kołczanu będzie dość łatwa)";
};


func int dia_addon_cavalorn_pickpocket_condition()
{
	if((Npc_GetTalentSkill(other,NPC_TALENT_PICKPOCKET) == 1) && (self.aivar[AIV_PLAYERHASPICKEDMYPOCKET] == FALSE) && (other.attribute[ATR_DEXTERITY] >= (25 - THEFTDIFF)))
	{
		return TRUE;
	};
};

func void dia_addon_cavalorn_pickpocket_info()
{
	Info_ClearChoices(dia_addon_cavalorn_pickpocket);
	Info_AddChoice(dia_addon_cavalorn_pickpocket,DIALOG_BACK,dia_addon_cavalorn_pickpocket_back);
	Info_AddChoice(dia_addon_cavalorn_pickpocket,DIALOG_PICKPOCKET,dia_addon_cavalorn_pickpocket_doit);
};

func void dia_addon_cavalorn_pickpocket_doit()
{
	if(other.attribute[ATR_DEXTERITY] >= 25)
	{
		b_giveinvitems(self,other,itrw_arrow,44);
		self.aivar[AIV_PLAYERHASPICKEDMYPOCKET] = TRUE;
		b_giveplayerxp(XP_AMBIENT);
		Info_ClearChoices(dia_addon_cavalorn_pickpocket);
	}
	else
	{
		AI_StopProcessInfos(self);
		b_attack(self,other,AR_THEFT,1);
	};
};

func void dia_addon_cavalorn_pickpocket_back()
{
	Info_ClearChoices(dia_addon_cavalorn_pickpocket);
};


instance DIA_ADDON_CAVALORN_MEETINGISRUNNING(C_INFO)
{
	npc = bau_4300_addon_cavalorn;
	nr = 1;
	condition = dia_addon_cavalorn_meetingisrunning_condition;
	information = dia_addon_cavalorn_meetingisrunning_info;
	important = TRUE;
	permanent = TRUE;
};


var int dia_addon_cavalorn_meetingisrunning_onetime;

func int dia_addon_cavalorn_meetingisrunning_condition()
{
	if(Npc_IsInState(self,zs_talk) && (RANGERMEETINGRUNNING == LOG_RUNNING))
	{
		return TRUE;
	};
};

func void dia_addon_cavalorn_meetingisrunning_info()
{
	if(DIA_ADDON_CAVALORN_MEETINGISRUNNING_ONETIME == FALSE)
	{
		AI_Output(self,other,"DIA_Addon_Cavalorn_MeetingIsRunning_08_00");	//Witaj w Kręgu, przyjacielu.
		DIA_ADDON_CAVALORN_MEETINGISRUNNING_ONETIME = TRUE;
	}
	else
	{
		AI_Output(self,other,"DIA_Addon_Gaan_MeetingIsRunning_08_01");	//Vatras da ci kolejne zadanie.
	};
	AI_StopProcessInfos(self);
};


instance DIA_ADDON_CAVALORN_HALLO(C_INFO)
{
	npc = bau_4300_addon_cavalorn;
	nr = 5;
	condition = dia_addon_cavalorn_hallo_condition;
	information = dia_addon_cavalorn_hallo_info;
	description = "Jakieś kłopoty?";
};


func int dia_addon_cavalorn_hallo_condition()
{
	return TRUE;
};

func void dia_addon_cavalorn_hallo_info()
{
	AI_Output(other,self,"DIA_Addon_Cavalorn_HALLO_15_00");	//Jakieś kłopoty?
	AI_Output(self,other,"DIA_Addon_Cavalorn_HALLO_08_01");	//Do diabła. Nie wiem, gdzie się ukrywają. Zabijesz jednego, ale zaraz wracają.
	AI_Output(self,other,"DIA_Addon_Cavalorn_HALLO_08_02");	//Chwila. Ja ciebie znam. To ty ciągle żebrałeś u mnie o strzały, jeszcze w Górniczej Dolinie.
	Info_ClearChoices(dia_addon_cavalorn_hallo);
	Info_AddChoice(dia_addon_cavalorn_hallo,"Nazywasz się Cavalorn, tak?",dia_addon_cavalorn_hallo_ja);
	Info_AddChoice(dia_addon_cavalorn_hallo,"Nie przypominam sobie...",dia_addon_cavalorn_hallo_weissnicht);
};

func void dia_addon_cavalorn_hallo_weissnicht()
{
	AI_Output(other,self,"DIA_Addon_Cavalorn_HALLO_weissNicht_15_00");	//Nie przypominam sobie...
	AI_Output(self,other,"DIA_Addon_Cavalorn_HALLO_weissNicht_08_01");	//Daj spokój! Nauczyłem cię łucznictwa i skradania się w mojej chatce niedaleko Starego Obozu! Przypominasz sobie?
};

func void dia_addon_cavalorn_hallo_ja()
{
	AI_Output(other,self,"DIA_Addon_Cavalorn_HALLO_Ja_15_00");	//Nazywasz się Cavalorn, tak?
	AI_Output(self,other,"DIA_Addon_Cavalorn_HALLO_Ja_08_01");	//Ach, nie zapomniałeś o mnie. Koniec końców obaj przeszliśmy przez tę przeklętą kolonię.
	AI_Output(self,other,"DIA_Addon_Cavalorn_HALLO_Ja_08_02");	//Dokąd idziesz?
	Info_ClearChoices(dia_addon_cavalorn_hallo);
	Info_AddChoice(dia_addon_cavalorn_hallo,"Nie mam określonego celu.",dia_addon_cavalorn_hallo_keinziel);
	Info_AddChoice(dia_addon_cavalorn_hallo,"Z powrotem do Górniczej Doliny.",dia_addon_cavalorn_hallo_bauern);
	if(mil_310_stadtwache.aivar[AIV_PASSGATE] == FALSE)
	{
		Info_AddChoice(dia_addon_cavalorn_hallo,"Do miasta.",dia_addon_cavalorn_hallo_stadt);
	};
};

func void dia_addon_cavalorn_hallo_stadt()
{
	AI_Output(other,self,"DIA_Addon_Cavalorn_HALLO_Stadt_15_00");	//Do miasta.
	AI_Output(self,other,"DIA_Addon_Cavalorn_HALLO_Stadt_08_01");	//Ach, też do miasta.
	AI_Output(self,other,"DIA_Addon_Cavalorn_HALLO_Stadt_08_02");	//Miałbyś kłopoty ze strażą. Teraz, gdy aż roi się tu od bandytów, nie każdy może wejść do miasta.
	AI_Output(self,other,"DIA_Addon_Cavalorn_HALLO_Stadt_08_03");	//Kilka dni temu przechodził tędy jeden ze starych Psioników z Górniczej Doliny. Mówił, że może wchodzić i wychodzić z Khorinis, kiedy tylko chce.
	AI_Output(self,other,"DIA_Addon_Cavalorn_HALLO_Stadt_08_04");	//Poszedł do doliny pod tą dużą wieżą. Gdzieś w okolicy wodospadu musi być przejście.
	AI_Output(self,other,"DIA_Addon_Cavalorn_HALLO_Stadt_08_05");	//Może powinieneś z nim porozmawiać.
	Info_ClearChoices(dia_addon_cavalorn_hallo);
};

func void dia_addon_cavalorn_hallo_bauern()
{
	AI_Output(other,self,"DIA_Addon_Cavalorn_HALLO_Bauern_15_00");	//Z powrotem do Górniczej Doliny.
	AI_Output(self,other,"DIA_Addon_Cavalorn_HALLO_Bauern_08_01");	//Naprawdę? Hmm. Szkoda, że nie mogę z tobą iść, ale muszę załatwić kilka spraw.
	AI_Output(self,other,"DIA_Addon_Cavalorn_HALLO_Bauern_08_02");	//Jeżeli dostaniesz się do Górniczej Doliny, sprawdź, czy moja chata jeszcze stoi, dobrze? Pewnego dnia chciałbym tam wrócić.
	MIS_ADDON_CAVALORN_THEHUT = LOG_RUNNING;
	Log_CreateTopic(TOPIC_ADDON_CAVALORNTHEHUT,LOG_MISSION);
	Log_SetTopicStatus(TOPIC_ADDON_CAVALORNTHEHUT,LOG_RUNNING);
	b_logentry(TOPIC_ADDON_CAVALORNTHEHUT,"Cavalorn chce, żebym sprawdził, czy w Górniczej Dolinie wciąż stoi jego stara chata. Z tego, co pamiętam, znajdowała się ona na wzgórzach na zachód od Starego Obozu. Wydaje mi się, że coś tam mogło zostać.");
	Info_ClearChoices(dia_addon_cavalorn_hallo);
};

func void dia_addon_cavalorn_hallo_keinziel()
{
	AI_Output(other,self,"DIA_Addon_Cavalorn_HALLO_keinZiel_15_00");	//Nie mam określonego celu.
	AI_Output(self,other,"DIA_Addon_Cavalorn_HALLO_keinZiel_08_01");	//Nie chcesz powiedzieć, co? Nie ma sprawy.
	Info_ClearChoices(dia_addon_cavalorn_hallo);
};


instance DIA_ADDON_CAVALORN_BEUTEL(C_INFO)
{
	npc = bau_4300_addon_cavalorn;
	nr = 5;
	condition = dia_addon_cavalorn_beutel_condition;
	information = dia_addon_cavalorn_beutel_info;
	description = "Byłem w twojej chacie w Górniczej Dolinie.";
};


func int dia_addon_cavalorn_beutel_condition()
{
	if(Npc_KnowsInfo(other,dia_addon_cavalorn_hallo) && (Npc_HasItems(other,itse_addon_cavalornsbeutel) || (SC_OPENEDCAVALORNSBEUTEL == TRUE)))
	{
		return TRUE;
	};
};

func void dia_addon_cavalorn_beutel_info()
{
	AI_Output(other,self,"DIA_Addon_Cavalorn_Beutel_15_00");	//Byłem w twojej chacie w Górniczej Dolinie.
	AI_Output(self,other,"DIA_Addon_Cavalorn_Beutel_08_01");	//A zatem jeszcze stoi.
	if(MIS_ADDON_CAVALORN_THEHUT == LOG_RUNNING)
	{
		AI_Output(other,self,"DIA_Addon_Cavalorn_Beutel_15_02");	//Tak. I wiem, co stamtąd chciałeś.
	};
	AI_Output(self,other,"DIA_Addon_Cavalorn_Beutel_08_03");	//Udało ci się to znaleźć?
	AI_Output(other,self,"DIA_Addon_Cavalorn_Beutel_15_04");	//Jeżeli mówisz o torbie pełnej rudy... Tak, mam ją.
	AI_Output(self,other,"DIA_Addon_Cavalorn_Beutel_08_05");	//Ale z ciebie spryciula, wiesz o tym?
	if(MIS_ADDON_CAVALORN_THEHUT == LOG_RUNNING)
	{
		AI_Output(other,self,"DIA_Addon_Cavalorn_Beutel_15_06");	//A czego mógłbyś potrzebować z tej starej chaty? Nic tam nie zostało.
	};
	AI_Output(self,other,"DIA_Addon_Cavalorn_Beutel_08_07");	//Masz ją ze sobą? Dam ci za nią 100 sztuk złota.
	TOPIC_END_CAVALORNTHEHUT = TRUE;
	b_giveplayerxp(XP_AMBIENT);
	Info_ClearChoices(dia_addon_cavalorn_beutel);
	if(Npc_HasItems(other,itse_addon_cavalornsbeutel))
	{
		Info_AddChoice(dia_addon_cavalorn_beutel,"Pewnie.",dia_addon_cavalorn_beutel_ja);
	}
	else if(Npc_HasItems(other,itmi_nugget))
	{
		Info_AddChoice(dia_addon_cavalorn_beutel,"Nie, ale mam kawałki rudy.",dia_addon_cavalorn_beutel_jaerz);
	};
	Info_AddChoice(dia_addon_cavalorn_beutel,"Nie.",dia_addon_cavalorn_beutel_no);
};

func void dia_addon_cavalorn_beutel_back()
{
	Info_ClearChoices(dia_addon_cavalorn_beutel);
	AI_Output(self,other,"DIA_Addon_Cavalorn_back_08_00");	//Mam nadzieję, że wkrótce ją odzyskam.
};

func void dia_addon_cavalorn_beutel_jaerz()
{
	AI_Output(other,self,"DIA_Addon_Cavalorn_Beutel_jaerz_15_00");	//Nie, ale mam kawałki rudy.
	AI_Output(self,other,"DIA_Addon_Cavalorn_Beutel_jaerz_08_01");	//Też dobrze.
	Info_ClearChoices(dia_addon_cavalorn_beutel);
	Info_AddChoice(dia_addon_cavalorn_beutel,DIALOG_BACK,dia_addon_cavalorn_beutel_back);
	Info_AddChoice(dia_addon_cavalorn_beutel,"A dlaczego ją zostawiłeś?",dia_addon_cavalorn_beutel_why);
};

func void dia_addon_cavalorn_beutel_ja()
{
	AI_Output(other,self,"DIA_Addon_Cavalorn_Beutel_ja_15_00");	//Pewnie.
	AI_Output(self,other,"DIA_Addon_Cavalorn_Beutel_ja_08_01");	//Świetnie.
	Info_ClearChoices(dia_addon_cavalorn_beutel);
	Info_AddChoice(dia_addon_cavalorn_beutel,DIALOG_BACK,dia_addon_cavalorn_beutel_back);
	Info_AddChoice(dia_addon_cavalorn_beutel,"A dlaczego ją zostawiłeś?",dia_addon_cavalorn_beutel_why);
};

func void dia_addon_cavalorn_beutel_no()
{
	AI_Output(other,self,"DIA_Addon_Cavalorn_Beutel_no_15_00");	//Nie.
	AI_Output(self,other,"DIA_Addon_Cavalorn_Beutel_no_08_01");	//Więc przynieś mi to! Koniec końców sam bym chyba poszedł po ten towar do tej przeklętej Górniczej Doliny.
	AI_Output(other,self,"DIA_Addon_Cavalorn_Beutel_no_15_02");	//Jestem wzruszony.
	Info_ClearChoices(dia_addon_cavalorn_beutel);
	Info_AddChoice(dia_addon_cavalorn_beutel,DIALOG_BACK,dia_addon_cavalorn_beutel_back);
	Info_AddChoice(dia_addon_cavalorn_beutel,"A dlaczego ją zostawiłeś?",dia_addon_cavalorn_beutel_why);
};

func void dia_addon_cavalorn_beutel_why()
{
	AI_Output(other,self,"DIA_Addon_Cavalorn_Beutel_why_15_00");	//A dlaczego ją zostawiłeś?
	AI_Output(self,other,"DIA_Addon_Cavalorn_Beutel_why_08_01");	//Kto mógłby przypuszczać, że w Khorinis ruda jest tak cenna.
	AI_Output(self,other,"DIA_Addon_Cavalorn_Beutel_why_08_02");	//W kolonii za głupi kawałek rudy nie dostałbyś nawet miejsca do spania.
	AI_Output(self,other,"DIA_Addon_Cavalorn_Beutel_why_08_03");	//W porcie można dostać po głowie za kawałek rudy.
};


instance DIA_ADDON_CAVALORN_ERZGEBEN(C_INFO)
{
	npc = bau_4300_addon_cavalorn;
	nr = 5;
	condition = dia_addon_cavalorn_erzgeben_condition;
	information = dia_addon_cavalorn_erzgeben_info;
	description = "Daj mi 100 sztuk złota, a przyniosę ci tę rudę.";
};


func int dia_addon_cavalorn_erzgeben_condition()
{
	if(Npc_KnowsInfo(other,dia_addon_cavalorn_beutel) && (Npc_HasItems(other,itse_addon_cavalornsbeutel) || Npc_HasItems(other,itmi_nugget)))
	{
		return TRUE;
	};
};

func void dia_addon_cavalorn_erzgeben_info()
{
	AI_Output(other,self,"DIA_Addon_Cavalorn_ErzGeben_15_00");	//Daj mi 100 sztuk złota, a przyniosę ci tę rudę.
	AI_Output(self,other,"DIA_Addon_Cavalorn_ErzGeben_08_01");	//Zgoda. Masz.
	CreateInvItems(self,itmi_gold,100);
	b_giveinvitems(self,other,itmi_gold,100);
	if(b_giveinvitems(other,self,itse_addon_cavalornsbeutel,1) == FALSE)
	{
		b_giveinvitems(other,self,itmi_nugget,1);
	};
	AI_Output(self,other,"DIA_Addon_Cavalorn_ErzGeben_08_02");	//Prawdziwy z ciebie przyjaciel. Dziękuję.
	MIS_ADDON_CAVALORN_THEHUT = LOG_SUCCESS;
	b_giveplayerxp(XP_ADDON_CAVALORNSBEUTEL);
};


instance DIA_ADDON_CAVALORN_WASMACHSTDU(C_INFO)
{
	npc = bau_4300_addon_cavalorn;
	nr = 5;
	condition = dia_addon_cavalorn_wasmachstdu_condition;
	information = dia_addon_cavalorn_wasmachstdu_info;
	description = "Co tu robisz?";
};


func int dia_addon_cavalorn_wasmachstdu_condition()
{
	if(Npc_KnowsInfo(other,dia_addon_cavalorn_hallo) && (MIS_ADDON_NEFARIUS_BRINGMISSINGORNAMENTS == 0))
	{
		return TRUE;
	};
};

func void dia_addon_cavalorn_wasmachstdu_info()
{
	AI_Output(other,self,"DIA_Addon_Cavalorn_WASMACHSTDU_15_00");	//Co tu robisz?
	AI_Output(self,other,"DIA_Addon_Cavalorn_WASMACHSTDU_08_01");	//Utknąłem. Gdyby nie ci przeklęci bandyci, w ogóle by mnie tu nie było.
};


instance DIA_ADDON_CAVALORN_BANDITEN(C_INFO)
{
	npc = bau_4300_addon_cavalorn;
	nr = 10;
	condition = dia_addon_cavalorn_banditen_condition;
	information = dia_addon_cavalorn_banditen_info;
	description = "O co chodzi z tymi bandytami?";
};


func int dia_addon_cavalorn_banditen_condition()
{
	if(Npc_KnowsInfo(other,dia_addon_cavalorn_wasmachstdu) && (MIS_ADDON_NEFARIUS_BRINGMISSINGORNAMENTS == 0))
	{
		return TRUE;
	};
};

func void dia_addon_cavalorn_banditen_info()
{
	AI_Output(other,self,"DIA_Addon_Cavalorn_Banditen_15_00");	//O co chodzi z tymi bandytami?
	AI_Output(self,other,"DIA_Addon_Cavalorn_Banditen_08_01");	//Przespałeś cały ostatni tydzień?
	AI_Output(other,self,"DIA_Addon_Cavalorn_Banditen_15_02");	//Ech...
	AI_Output(self,other,"DIA_Addon_Cavalorn_Banditen_08_03");	//Mówię o tych szczurach z kolonii karnej - rozleźli się po całej okolicy; łupią i mordują.
	AI_Output(self,other,"DIA_Addon_Cavalorn_Banditen_08_04");	//Cieszę się, że darowali mi życie. Nie uważałem i dostałem w czaszkę.
	if(c_bragobanditsdead() == FALSE)
	{
		AI_Output(self,other,"DIA_Addon_Cavalorn_Banditen_08_05");	//Nie wiem, jak mam teraz odzyskać swoje rzeczy.
	};
};


instance DIA_ADDON_CAVALORN_ARTEFAKT(C_INFO)
{
	npc = bau_4300_addon_cavalorn;
	nr = 5;
	condition = dia_addon_cavalorn_artefakt_condition;
	information = dia_addon_cavalorn_artefakt_info;
	description = "Zostałeś obrabowany przez bandytów?";
};


func int dia_addon_cavalorn_artefakt_condition()
{
	if(Npc_KnowsInfo(other,dia_addon_cavalorn_banditen) && (MIS_ADDON_CAVALORN_KILLBRAGO != LOG_SUCCESS) && (MIS_ADDON_NEFARIUS_BRINGMISSINGORNAMENTS == 0) && (MIS_ADDON_CAVALORN_LETTER2VATRAS != LOG_SUCCESS))
	{
		return TRUE;
	};
};

func void dia_addon_cavalorn_artefakt_info()
{
	AI_Output(other,self,"DIA_Addon_Cavalorn_ARTEFAKT_15_00");	//Zostałeś obrabowany przez bandytów?
	AI_Output(self,other,"DIA_Addon_Cavalorn_ARTEFAKT_08_01");	//Tak. Ogłuszyli mnie i zostawili jako żarcie dla goblinów.
	AI_Output(self,other,"DIA_Addon_Cavalorn_ARTEFAKT_08_02");	//To były piekielnie ważne rzeczy. List i cała moja gotówka. Muszę je odzyskać.
	AI_Output(self,other,"DIA_Addon_Cavalorn_ARTEFAKT_08_03");	//Nie pójdę tam jednak bez wsparcia. Ta tchórzliwa hałastra bandytów...
};


instance DIA_ADDON_CAVALORN_HELFEN(C_INFO)
{
	npc = bau_4300_addon_cavalorn;
	nr = 5;
	condition = dia_addon_cavalorn_helfen_condition;
	information = dia_addon_cavalorn_helfen_info;
	description = "Mogę ci pomóc z tymi bandytami?";
};


func int dia_addon_cavalorn_helfen_condition()
{
	if(Npc_KnowsInfo(other,dia_addon_cavalorn_artefakt) && (MIS_ADDON_NEFARIUS_BRINGMISSINGORNAMENTS == 0) && (MIS_ADDON_CAVALORN_LETTER2VATRAS != LOG_SUCCESS) && (c_bragobanditsdead() == FALSE))
	{
		return TRUE;
	};
};

func void dia_addon_cavalorn_helfen_info()
{
	AI_Output(other,self,"DIA_Addon_Cavalorn_HELFEN_15_00");	//Mogę ci pomóc z tymi bandytami?
	if((Npc_HasEquippedArmor(other) == FALSE) && (hero.guild == GIL_NONE))
	{
		AI_Output(self,other,"DIA_Addon_Cavalorn_HELFEN_08_01");	//Może. Ale sądząc po twoim mizernym wyglądzie, mogę powiedzieć, że od tygodni nie miałeś w rękach prawdziwego miecza.
	};
	AI_Output(self,other,"DIA_Addon_Cavalorn_HELFEN_08_02");	//No cóż. Muszę chyba przyjąć twoją ofertę. Nie mam zbyt wiele czasu.
	AI_Output(self,other,"DIA_Addon_Cavalorn_HELFEN_08_03");	//Dobra, słuchaj. W dole tej ścieżki jest jedna z tych brudnych dziur, w których ukrywają się bandyci.
	AI_Output(self,other,"DIA_Addon_Cavalorn_HELFEN_08_04");	//To te łotry ukradły moje rzeczy.
	AI_Output(self,other,"DIA_Addon_Cavalorn_HELFEN_08_05");	//Daj znać, gdy będziesz gotów. Ruszymy za tymi szczurami!
	MIS_ADDON_CAVALORN_KILLBRAGO = LOG_RUNNING;
	Log_CreateTopic(TOPIC_ADDON_KILLBRAGO,LOG_MISSION);
	Log_SetTopicStatus(TOPIC_ADDON_KILLBRAGO,LOG_RUNNING);
	b_logentry(TOPIC_ADDON_KILLBRAGO,"Bandyci ukradli coś cennego Cavalornowi. Chce, żebyśmy razem ich zabili.");
	self.aivar[AIV_PARTYMEMBER] = TRUE;
};


instance DIA_ADDON_CAVALORN_AUSRUESTUNG(C_INFO)
{
	npc = bau_4300_addon_cavalorn;
	nr = 5;
	condition = dia_addon_cavalorn_ausruestung_condition;
	information = dia_addon_cavalorn_ausruestung_info;
	description = "Potrzebuję lepszego sprzętu.";
};


func int dia_addon_cavalorn_ausruestung_condition()
{
	if((MIS_ADDON_CAVALORN_KILLBRAGO != 0) && (MIS_ADDON_NEFARIUS_BRINGMISSINGORNAMENTS == 0))
	{
		return TRUE;
	};
};

func void dia_addon_cavalorn_ausruestung_info()
{
	AI_Output(other,self,"DIA_Addon_Cavalorn_AUSRUESTUNG_15_00");	//Potrzebuję lepszego sprzętu.
	if(c_bragobanditsdead() == FALSE)
	{
		AI_Output(self,other,"DIA_Addon_Cavalorn_AUSRUESTUNG_08_01");	//Te świnie nie zostawiły mi zbyt wiele.
	};
	AI_Output(self,other,"DIA_Addon_Cavalorn_AUSRUESTUNG_08_02");	//Mogę ci dać nóż na wilki. Wystarczy?
	AI_Output(other,self,"DIA_Addon_Cavalorn_AUSRUESTUNG_15_03");	//Tak, nóż będzie dobry.
	CreateInvItems(self,itmw_addon_knife01,1);
	b_giveinvitems(self,other,itmw_addon_knife01,1);
	AI_Output(other,self,"DIA_Addon_Cavalorn_AUSRUESTUNG_15_04");	//A co z leczeniem?
	AI_Output(self,other,"DIA_Addon_Cavalorn_AUSRUESTUNG_08_05");	//Zostały mi dwie mikstury uzdrawiające. Chcesz?
	AI_Output(other,self,"DIA_Addon_Cavalorn_AUSRUESTUNG_15_06");	//Pewnie. Wezmę je.
	CreateInvItems(self,itpo_health_01,2);
	b_giveinvitems(self,other,itpo_health_01,2);
};


instance DIA_ADDON_CAVALORN_LETSKILLBANDITS(C_INFO)
{
	npc = bau_4300_addon_cavalorn;
	nr = 5;
	condition = dia_addon_cavalorn_letskillbandits_condition;
	information = dia_addon_cavalorn_letskillbandits_info;
	description = "Chodźmy zabić tych gnojków.";
};


func int dia_addon_cavalorn_letskillbandits_condition()
{
	if((MIS_ADDON_CAVALORN_KILLBRAGO == LOG_RUNNING) && (MIS_ADDON_NEFARIUS_BRINGMISSINGORNAMENTS == 0) && (MIS_ADDON_CAVALORN_LETTER2VATRAS != LOG_SUCCESS) && (c_bragobanditsdead() == FALSE))
	{
		return TRUE;
	};
};

func void dia_addon_cavalorn_letskillbandits_info()
{
	AI_Output(other,self,"DIA_Addon_Cavalorn_LETSKILLBANDITS_15_00");	//Chodźmy zabić tych gnojków.
	AI_Output(self,other,"DIA_Addon_Cavalorn_LETSKILLBANDITS_08_01");	//Dobra. Tylko mnie osłaniaj, jasne?
	AI_Output(self,other,"DIA_Addon_Cavalorn_LETSKILLBANDITS_08_02");	//A teraz czeka ich paskudna niespodzianka.
	AI_StopProcessInfos(self);
	Npc_ExchangeRoutine(self,"KillBandits");
	if(BDT_1013_AWAY == FALSE)
	{
		ambusher_1013.aivar[AIV_ENEMYOVERRIDE] = FALSE;
	};
	ambusher_1014.aivar[AIV_ENEMYOVERRIDE] = FALSE;
	ambusher_1015.aivar[AIV_ENEMYOVERRIDE] = FALSE;
};

func void b_addon_cavalorn_vatrasbrief()
{
	if(MIS_ADDON_CAVALORN_LETTER2VATRAS != LOG_SUCCESS)
	{
		AI_Output(self,other,"DIA_Addon_Cavalorn_VatrasBrief_08_00");	//Przynajmniej mogę wykonać zadanie. I tak zmarnowałem już zbyt wiele czasu.
		AI_Output(other,self,"DIA_Addon_Cavalorn_VatrasBrief_15_01");	//Jakie zadanie...?
		AI_Output(self,other,"DIA_Addon_Cavalorn_VatrasBrief_08_02");	//Ech. Muszę się dostać do miasta, a później...
		AI_Output(self,other,"DIA_Addon_Cavalorn_VatrasBrief_08_03");	//Nie wiem tylko, jak mam zdążyć.
		AI_Output(other,self,"DIA_Addon_Cavalorn_VatrasBrief_15_04");	//A co ze mną?
		AI_Output(self,other,"DIA_Addon_Cavalorn_VatrasBrief_08_05");	//Hmm. Czemu nie. Mógłbyś zanieść list do miasta.
	};
	AI_Output(self,other,"DIA_Addon_Cavalorn_VatrasBrief_08_06");	//Dzięki temu będę miał czas, żeby pozbierać sprzęt.
	if(MIS_ADDON_CAVALORN_LETTER2VATRAS != LOG_SUCCESS)
	{
		AI_Output(self,other,"DIA_Addon_Cavalorn_VatrasBrief_08_07");	//Jeden z tych bandytów powinien mieć list w kieszeni.
		AI_Output(self,other,"DIA_Addon_Cavalorn_VatrasBrief_08_08");	//Zanieś go do miasta i oddaj magowi Kręgu Wody, Vatrasowi. Znajdziesz go w świątyni Adanosa. Naucza tam całymi dniami.
		AI_Output(self,other,"DIA_Addon_Cavalorn_VatrasBrief_08_09");	//Powiedz mu, że nie zdążyłem na czas.
		AI_Output(self,other,"DIA_Addon_Cavalorn_VatrasBrief_08_10");	//A gdyby cię zapytał, gdzie jestem, powiedz, że w drodze na miejsce spotkania, dobrze?
		b_logentry(TOPIC_ADDON_KDW,"Maga Wody, Vatrasa, można znaleźć w portowym mieście Khorinis. Głosi tam kazania w świątyni Adanosa.");
	};
	if((Npc_HasEquippedArmor(other) == FALSE) && (hero.guild == GIL_NONE) && (MIL_310_SCHONMALREINGELASSEN == FALSE) && (MIL_333_SCHONMALREINGELASSEN == FALSE))
	{
		AI_Output(self,other,"DIA_Addon_Cavalorn_VatrasBrief_08_11");	//Aha, jeszcze jedno: kup sobie od jakiegoś wieśniaka porządne ubranie.
		AI_Output(self,other,"DIA_Addon_Cavalorn_VatrasBrief_08_12");	//Inaczej wezmą cię za bandytę. Masz, tu jest parę monet.
		CreateInvItems(self,itmi_gold,50);
		b_giveinvitems(self,other,itmi_gold,50);
	};
	MIS_ADDON_CAVALORN_KILLBRAGO = LOG_SUCCESS;
	if(MIS_ADDON_CAVALORN_LETTER2VATRAS == 0)
	{
		MIS_ADDON_CAVALORN_LETTER2VATRAS = LOG_RUNNING;
	};
	Npc_ExchangeRoutine(self,"Start");
	b_giveplayerxp(XP_ADDON_CAVALORN_KILLBRAGO);
	Log_CreateTopic(TOPIC_ADDON_KDW,LOG_MISSION);
	Log_SetTopicStatus(TOPIC_ADDON_KDW,LOG_RUNNING);
	self.aivar[AIV_PARTYMEMBER] = FALSE;
};


instance DIA_ADDON_CAVALORN_BRAGOKILLED(C_INFO)
{
	npc = bau_4300_addon_cavalorn;
	nr = 5;
	condition = dia_addon_cavalorn_bragokilled_condition;
	information = dia_addon_cavalorn_bragokilled_info;
	important = TRUE;
};


func int dia_addon_cavalorn_bragokilled_condition()
{
	if((Npc_GetDistToWP(self,"NW_XARDAS_BANDITS_LEFT") < 500) && (MIS_ADDON_CAVALORN_KILLBRAGO == LOG_RUNNING) && (c_bragobanditsdead() == TRUE))
	{
		return TRUE;
	};
};

func void dia_addon_cavalorn_bragokilled_info()
{
	AI_Output(self,other,"DIA_Addon_Cavalorn_BragoKilled_08_00");	//No to załatwione. Ech. Mogli ze mną nie zaczynać.
	b_addon_cavalorn_vatrasbrief();
};


instance DIA_ADDON_CAVALORN_PCKILLEDBRAGO(C_INFO)
{
	npc = bau_4300_addon_cavalorn;
	nr = 5;
	condition = dia_addon_cavalorn_pckilledbrago_condition;
	information = dia_addon_cavalorn_pckilledbrago_info;
	description = "Bandyci są już martwi.";
};


func int dia_addon_cavalorn_pckilledbrago_condition()
{
	if((MIS_ADDON_CAVALORN_KILLBRAGO == 0) && Npc_KnowsInfo(other,dia_addon_cavalorn_banditen) && (c_bragobanditsdead() == TRUE))
	{
		return TRUE;
	};
};

func void dia_addon_cavalorn_pckilledbrago_info()
{
	AI_Output(other,self,"DIA_Addon_Cavalorn_PCKilledBrago_15_00");	//Bandyci są już martwi.
	b_addon_cavalorn_vatrasbrief();
};


instance DIA_ADDON_CAVALORN_JUNGS(C_INFO)
{
	npc = bau_4300_addon_cavalorn;
	nr = 2;
	condition = dia_addon_cavalorn_jungs_condition;
	information = dia_addon_cavalorn_jungs_info;
	description = "Masz na sobie interesujący pancerz.";
};


func int dia_addon_cavalorn_jungs_condition()
{
	if(Npc_KnowsInfo(other,dia_addon_cavalorn_hallo))
	{
		return TRUE;
	};
};

func void dia_addon_cavalorn_jungs_info()
{
	AI_Output(other,self,"DIA_Addon_Cavalorn_JUNGS_15_00");	//Masz na sobie interesujący pancerz. Nie należysz już do Cieni?
	AI_Output(self,other,"DIA_Addon_Cavalorn_JUNGS_08_01");	//Cieni? Od upadku bariery już nie istnieją.
	AI_Output(self,other,"DIA_Addon_Cavalorn_JUNGS_08_02");	//Gdy tylko mogliśmy opuścić Górniczą Dolinę, nie było powodu, żeby tam dłużej zostawać.
	AI_Output(self,other,"DIA_Addon_Cavalorn_JUNGS_08_03");	//Teraz pracuję dla magów wody. Jestem członkiem Wodnego Kręgu.
	SC_KNOWSRANGER = TRUE;
	Log_CreateTopic(TOPIC_ADDON_RINGOFWATER,LOG_MISSION);
	Log_SetTopicStatus(TOPIC_ADDON_RINGOFWATER,LOG_RUNNING);
	b_logentry(TOPIC_ADDON_RINGOFWATER,"Cavalorn powiedział mi, że należy do grupy zwącej się Wodny Krąg.");
	CAVALORN_RANGERHINT = TRUE;
};


instance DIA_ADDON_CAVALORN_RING(C_INFO)
{
	npc = bau_4300_addon_cavalorn;
	nr = 5;
	condition = dia_addon_cavalorn_ring_condition;
	information = dia_addon_cavalorn_ring_info;
	permanent = FALSE;
	description = "Powiedz mi coś więcej o Wodnym Kręgu!";
};


func int dia_addon_cavalorn_ring_condition()
{
	if(Npc_KnowsInfo(other,dia_addon_cavalorn_jungs))
	{
		return TRUE;
	};
};

func void dia_addon_cavalorn_ring_info()
{
	AI_Output(other,self,"DIA_Addon_Cavalorn_Ring_15_00");	//Powiedz mi coś więcej o Wodnym Kręgu!
	AI_Output(self,other,"DIA_Addon_Cavalorn_Ring_08_01");	//Nie wolno mi o tym mówić.
	AI_Output(self,other,"DIA_Addon_Cavalorn_Ring_08_02");	//Mogę cię jedynie wysłać do Vartasa. On reprezentuje Magów Wody w Khorinis.
	AI_Output(self,other,"DIA_Addon_Cavalorn_Ring_08_03");	//Najlepiej będzie, jak z nim porozmawiasz. Powiedz, że ja cię przysłałem.
	AI_Output(self,other,"DIA_Addon_Cavalorn_Ring_08_04");	//Może pozwoli ci wstąpić do Kręgu. Bardzo potrzeba nam dobrych ludzi...
	b_logentry(TOPIC_ADDON_RINGOFWATER,"Vatras, Mag Wody, może powiedzieć mi więcej o Wodnym Kręgu.");
};


instance DIA_ADDON_CAVALORN_FEINDE(C_INFO)
{
	npc = bau_4300_addon_cavalorn;
	nr = 6;
	condition = dia_addon_cavalorn_feinde_condition;
	information = dia_addon_cavalorn_feinde_info;
	permanent = FALSE;
	description = "Czy ty i twoi ludzie nie byliście czasem przeciwnikami Magów Wody?";
};


func int dia_addon_cavalorn_feinde_condition()
{
	if(Npc_KnowsInfo(other,dia_addon_cavalorn_jungs))
	{
		return TRUE;
	};
};

func void dia_addon_cavalorn_feinde_info()
{
	AI_Output(other,self,"DIA_Addon_Cavalorn_Feinde_15_00");	//Czy ty i twoi ludzie nie byliście czasem przeciwnikami Magów Wody?
	AI_Output(self,other,"DIA_Addon_Cavalorn_Feinde_08_01");	//Szalona przeszłość jest już za nami. Nie ma już Nowego ani Starego Obozu.
	AI_Output(self,other,"DIA_Addon_Cavalorn_Feinde_08_02");	//A teraz, gdy nie ma już kolonii karnej, każdy odpowiada za siebie.
	AI_Output(self,other,"DIA_Addon_Cavalorn_Feinde_08_03");	//Większość z nas - byłych więźniów - nie została uniewinniona.
	AI_Output(self,other,"DIA_Addon_Cavalorn_Feinde_08_04");	//Magowie Wody zdołali uzyskać dla mnie ułaskawienie i mogę teraz poruszać się swobodnie.
};


instance DIA_ADDON_CAVALORN_KDWTASK(C_INFO)
{
	npc = bau_4300_addon_cavalorn;
	nr = 6;
	condition = dia_addon_cavalorn_kdwtask_condition;
	information = dia_addon_cavalorn_kdwtask_info;
	permanent = FALSE;
	description = "Co porabiają teraz Magowie Wody?";
};


func int dia_addon_cavalorn_kdwtask_condition()
{
	if(Npc_KnowsInfo(other,dia_addon_cavalorn_jungs) && (MIS_ADDON_NEFARIUS_BRINGMISSINGORNAMENTS == 0))
	{
		return TRUE;
	};
};

func void dia_addon_cavalorn_kdwtask_info()
{
	AI_Output(other,self,"DIA_Addon_Cavalorn_KdWTask_15_00");	//Co porabiają teraz Magowie Wody?
	AI_Output(self,other,"DIA_Addon_Cavalorn_KdWTask_08_01");	//Mają wielki plan. Chodzi o niezbadaną część wyspy.
	AI_Output(other,self,"DIA_Addon_Cavalorn_KdWTask_15_02");	//Niezbadaną część? Gdzie ona jest?
	AI_Output(self,other,"DIA_Addon_Cavalorn_KdWTask_08_03");	//Nie mogę ci powiedzieć nic więcej. Porozmawiaj z Vatrasem w Khorinis.
};


instance DIA_ADDON_CAVALORN_BROUGHTLETTER(C_INFO)
{
	npc = bau_4300_addon_cavalorn;
	nr = 5;
	condition = dia_addon_cavalorn_broughtletter_condition;
	information = dia_addon_cavalorn_broughtletter_info;
	description = "Dałem Vatrasowi twój list.";
};


func int dia_addon_cavalorn_broughtletter_condition()
{
	if((MIS_ADDON_CAVALORN_LETTER2VATRAS == LOG_SUCCESS) && Npc_KnowsInfo(other,dia_addon_cavalorn_jungs))
	{
		return TRUE;
	};
};

func void dia_addon_cavalorn_broughtletter_info()
{
	AI_Output(other,self,"DIA_Addon_Cavalorn_BroughtLetter_15_00");	//Dałem Vatrasowi twój list.
	AI_Output(self,other,"DIA_Addon_Cavalorn_BroughtLetter_08_01");	//Nie oczekiwałem od ciebie niczego innego. Dziękuję.
	b_giveplayerxp(XP_AMBIENT);
};


instance DIA_ADDON_CAVALORN_ORNAMENT(C_INFO)
{
	npc = bau_4300_addon_cavalorn;
	nr = 2;
	condition = dia_addon_cavalorn_ornament_condition;
	information = dia_addon_cavalorn_ornament_info;
	description = "Szukasz czegoś?";
};


func int dia_addon_cavalorn_ornament_condition()
{
	if((MIS_ADDON_NEFARIUS_BRINGMISSINGORNAMENTS == LOG_RUNNING) && Npc_KnowsInfo(other,dia_addon_cavalorn_hallo))
	{
		return TRUE;
	};
};

func void dia_addon_cavalorn_ornament_info()
{
	AI_Output(other,self,"DIA_Addon_Cavalorn_Ornament_15_00");	//Szukasz czegoś?
	AI_Output(self,other,"DIA_Addon_Cavalorn_Ornament_08_01");	//To takie oczywiste? Tak, Magowie Wody kazali mi szukać zgubionych ornamentów.
	AI_Output(other,self,"DIA_Addon_Cavalorn_Ornament_15_02");	//Interesujący zbieg okoliczności. Otrzymałem taki sam rozkaz od Nefariusa.
	if(SC_KNOWSRANGER == TRUE)
	{
		AI_Output(self,other,"DIA_Addon_Cavalorn_Ornament_08_03");	//Należysz więc do Wodnego Kręgu?
		if(SC_ISRANGER == TRUE)
		{
			AI_Output(other,self,"DIA_Addon_Cavalorn_Ornament_15_04");	//Tak.
		}
		else
		{
			AI_Output(other,self,"DIA_Addon_Cavalorn_Ornament_15_05");	//Jeszcze nie, ale pracuję nad tym.
		};
	};
	AI_Output(self,other,"DIA_Addon_Cavalorn_Ornament_08_06");	//To dobrze. W takim razie nie muszę tego robić sam.
	AI_Output(other,self,"DIA_Addon_Cavalorn_Ornament_15_07");	//Znalazłeś już jakiś ornament?
	AI_Output(self,other,"DIA_Addon_Cavalorn_Ornament_08_08");	//Znam miejsce, w którym powinniśmy coś znaleźć.
	AI_Output(self,other,"DIA_Addon_Cavalorn_Ornament_08_09");	//Ten kamienny krąg może być jedną z tych budowli, które opisał Nefarius.
	AI_Output(self,other,"DIA_Addon_Cavalorn_Ornament_08_10");	//Teraz musimy tylko znaleźć mechanizm.
};


instance DIA_ADDON_CAVALORN_TRIGGERED(C_INFO)
{
	npc = bau_4300_addon_cavalorn;
	nr = 5;
	condition = dia_addon_cavalorn_triggered_condition;
	information = dia_addon_cavalorn_triggered_info;
	description = "Uruchomiłem mechanizm. Nic się nie stało.";
};


func int dia_addon_cavalorn_triggered_condition()
{
	if((MIS_ADDON_NEFARIUS_BRINGMISSINGORNAMENTS == LOG_RUNNING) && Npc_KnowsInfo(other,dia_addon_cavalorn_ornament) && (ORNAMENT_SWITCHED_FARM == TRUE))
	{
		return TRUE;
	};
};

func void dia_addon_cavalorn_triggered_info()
{
	AI_Output(other,self,"DIA_Addon_Cavalorn_Triggered_15_00");	//Uruchomiłem mechanizm. Nic się nie stało.
	AI_Output(self,other,"DIA_Addon_Cavalorn_Triggered_08_01");	//W takim razie wieśniacy Lobarta mieli rację.
	AI_Output(self,other,"DIA_Addon_Cavalorn_Triggered_08_02");	//Powiedzieli, że ktoś już kręcił się przy tych kamieniach.
	AI_Output(self,other,"DIA_Addon_Cavalorn_Triggered_08_03");	//Nagle znikąd pojawił się kamienny strażnik i ich zaatakował.
	AI_Output(self,other,"DIA_Addon_Cavalorn_Triggered_08_04");	//Farmerzy wezwali straż, żołnierze paladynów, a ci przyszli i zniszczyli potwora.
	AI_Output(self,other,"DIA_Addon_Cavalorn_Triggered_08_05");	//Przeszukałem już cały teren. Jeżeli był tu jakiś ornament, mają go teraz paladyni.
	Info_ClearChoices(dia_addon_cavalorn_triggered);
	Info_AddChoice(dia_addon_cavalorn_triggered,"Jeden z nas musi pójść do górnego miasta.",dia_addon_cavalorn_triggered_pal);
	Info_AddChoice(dia_addon_cavalorn_triggered,"W takim razie pójdę do nich i odzyskam ornament.",dia_addon_cavalorn_triggered_oback);
};

func void b_cavalorn_triggered_wohin()
{
	AI_Output(self,other,"DIA_Addon_Cavalorn_Triggered_Wohin_08_00");	//Pójdę do miasta. Spotkamy się u Vatrasa.
	AI_StopProcessInfos(self);
	Npc_ExchangeRoutine(self,"Stadt");
	Log_CreateTopic(TOPIC_ADDON_ORNAMENT,LOG_MISSION);
	Log_SetTopicStatus(TOPIC_ADDON_ORNAMENT,LOG_RUNNING);
	b_logentry(TOPIC_ADDON_ORNAMENT,"Jeden z brakujących fragmentów ornamentu jest w posiadaniu paladynów w górnym mieście.");
	MIS_ADDON_CAVALORN_GETORNAMENTFROMPAL = LOG_RUNNING;
	self.flags = 0;
};

func void dia_addon_cavalorn_triggered_oback()
{
	AI_UnequipArmor(self);
	CreateInvItems(self,itar_bau_l,1);
	Npc_RemoveInvItems(self,itar_ranger_addon,Npc_HasItems(self,itar_ranger_addon));
	Npc_RemoveInvItems(self,itar_fake_ranger,Npc_HasItems(self,itar_fake_ranger));
	AI_EquipBestArmor(self);
	AI_Output(other,self,"DIA_Addon_Cavalorn_Triggered_OBack_15_00");	//W takim razie pójdę do nich i odzyskam ornament.
	AI_Output(self,other,"DIA_Addon_Cavalorn_Triggered_OBack_08_01");	//Dobrze.
	b_cavalorn_triggered_wohin();
};

func void dia_addon_cavalorn_triggered_pal()
{
	AI_UnequipArmor(self);
	CreateInvItems(self,itar_bau_l,1);
	Npc_RemoveInvItems(self,itar_ranger_addon,Npc_HasItems(self,itar_ranger_addon));
	Npc_RemoveInvItems(self,itar_fake_ranger,Npc_HasItems(self,itar_fake_ranger));
	AI_EquipBestArmor(self);
	AI_Output(other,self,"DIA_Addon_Cavalorn_Triggered_Pal_15_00");	//Jeden z nas musi pójść do górnego miasta.
	AI_Output(self,other,"DIA_Addon_Cavalorn_Triggered_Pal_08_01");	//Nie mam na to czasu. Ty musisz to zrobić.
	b_cavalorn_triggered_wohin();
};


instance DIA_ADDON_CAVALORN_GOTORNAFROMHAGEN(C_INFO)
{
	npc = bau_4300_addon_cavalorn;
	nr = 5;
	condition = dia_addon_cavalorn_gotornafromhagen_condition;
	information = dia_addon_cavalorn_gotornafromhagen_info;
	description = "Dostałem brakujący ornament od Lorda Hagena.";
};


func int dia_addon_cavalorn_gotornafromhagen_condition()
{
	if(LORD_HAGEN_GOTORNAMENT == TRUE)
	{
		return TRUE;
	};
};

func void dia_addon_cavalorn_gotornafromhagen_info()
{
	AI_Output(other,self,"DIA_Addon_Cavalorn_GotOrnaFromHagen_15_00");	//Dostałem brakujący ornament od Lorda Hagena.
	AI_Output(self,other,"DIA_Addon_Cavalorn_GotOrnaFromHagen_08_01");	//Widzisz? Wiedziałem, że mieli go paladyni.
	b_giveplayerxp(XP_AMBIENT);
	MIS_ADDON_CAVALORN_GETORNAMENTFROMPAL = LOG_SUCCESS;
};


instance DIA_ADDON_CAVALORN_WANNALEARN(C_INFO)
{
	npc = bau_4300_addon_cavalorn;
	nr = 7;
	condition = dia_addon_cavalorn_wannalearn_condition;
	information = dia_addon_cavalorn_wannalearn_info;
	permanent = FALSE;
	description = "Możesz mnie czegoś nauczyć?";
};


func int dia_addon_cavalorn_wannalearn_condition()
{
	if(Npc_KnowsInfo(other,dia_addon_cavalorn_hallo) && (c_bragobanditsdead() == TRUE))
	{
		return TRUE;
	};
};

func void dia_addon_cavalorn_wannalearn_info()
{
	AI_Output(other,self,"DIA_Addon_Cavalorn_WannaLearn_15_00");	//Możesz mnie czegoś nauczyć?
	AI_Output(self,other,"DIA_Addon_Cavalorn_WannaLearn_08_01");	//Pewnie. Przecież wiesz. Oj, chłopie, nieźle cię przegonili.
	AI_Output(self,other,"DIA_Addon_Cavalorn_WannaLearn_08_02");	//Niczego nie pamiętasz, prawda?
	CAVALORN_ADDON_TEACHPLAYER = TRUE;
	Log_CreateTopic(TOPIC_OUTTEACHER,LOG_NOTE);
	b_logentry(TOPIC_OUTTEACHER,LOGTEXT_ADDON_CAVALORN_TEACH);
};


var int addon_cavalorn_merke_bow;
var int addon_cavalorn_merke_1h;

instance DIA_ADDON_CAVALORN_TEACH(C_INFO)
{
	npc = bau_4300_addon_cavalorn;
	nr = 8;
	condition = dia_addon_cavalorn_teach_condition;
	information = dia_addon_cavalorn_teach_info;
	permanent = TRUE;
	description = "Chcę się czegoś od ciebie nauczyć.";
};


func int dia_addon_cavalorn_teach_condition()
{
	if(CAVALORN_ADDON_TEACHPLAYER == TRUE)
	{
		return TRUE;
	};
};

func void dia_addon_cavalorn_teach_choices()
{
	Info_ClearChoices(dia_addon_cavalorn_teach);
	Info_AddChoice(dia_addon_cavalorn_teach,DIALOG_BACK,dia_addon_cavalorn_teach_back);
	if(Npc_GetTalentSkill(other,NPC_TALENT_SNEAK) == FALSE)
	{
		Info_AddChoice(dia_addon_cavalorn_teach,b_buildlearnstring("Skradanie się",b_getlearncosttalent(other,NPC_TALENT_SNEAK,1)),dia_addon_cavalorn_teach_sneak);
	};
	Info_AddChoice(dia_addon_cavalorn_teach,b_buildlearnstring(PRINT_LEARNBOW1,b_getlearncosttalent(other,NPC_TALENT_BOW,1)),dia_addon_cavalorn_teach_bow_1);
	Info_AddChoice(dia_addon_cavalorn_teach,b_buildlearnstring(PRINT_LEARNBOW5,b_getlearncosttalent(other,NPC_TALENT_BOW,1) * 5),dia_addon_cavalorn_teach_bow_5);
	Info_AddChoice(dia_addon_cavalorn_teach,b_buildlearnstring(PRINT_LEARN1H1,b_getlearncosttalent(other,NPC_TALENT_1H,1)),dia_addon_cavalorn_teach_1h_1);
	Info_AddChoice(dia_addon_cavalorn_teach,b_buildlearnstring(PRINT_LEARN1H5,b_getlearncosttalent(other,NPC_TALENT_1H,1) * 5),dia_addon_cavalorn_teach_1h_5);
};

func void dia_addon_cavalorn_teach_info()
{
	AI_Output(other,self,"DIA_Addon_Cavalorn_TEACH_15_00");	//Chcę się czegoś od ciebie nauczyć.
	AI_Output(self,other,"DIA_Addon_Cavalorn_TEACH_08_01");	//Pewnie. Co chcesz wiedzieć?
	ADDON_CAVALORN_MERKE_BOW = other.hitchance[NPC_TALENT_BOW];
	ADDON_CAVALORN_MERKE_1H = other.hitchance[NPC_TALENT_1H];
	dia_addon_cavalorn_teach_choices();
};

func void dia_addon_cavalorn_teach_sneak()
{
	if(b_teachthieftalent(self,other,NPC_TALENT_SNEAK))
	{
		AI_Output(self,other,"DIA_Addon_Cavalorn_Teach_Sneak_08_00");	//Na miękkich podeszwach mamy większe szanse podkraść się niezauważenie do przeciwnika.
	};
	dia_addon_cavalorn_teach_choices();
};

func void dia_addon_cavalorn_teach_bow_1()
{
	b_teachfighttalentpercent(self,other,NPC_TALENT_BOW,1,90);
	dia_addon_cavalorn_teach_choices();
};

func void dia_addon_cavalorn_teach_bow_5()
{
	b_teachfighttalentpercent(self,other,NPC_TALENT_BOW,5,90);
	dia_addon_cavalorn_teach_choices();
};

func void dia_addon_cavalorn_teach_1h_1()
{
	b_teachfighttalentpercent(self,other,NPC_TALENT_1H,1,30);
	dia_addon_cavalorn_teach_choices();
};

func void dia_addon_cavalorn_teach_1h_5()
{
	b_teachfighttalentpercent(self,other,NPC_TALENT_1H,5,30);
	dia_addon_cavalorn_teach_choices();
};

func void dia_addon_cavalorn_teach_back()
{
	if((ADDON_CAVALORN_MERKE_BOW < other.hitchance[NPC_TALENT_BOW]) || (ADDON_CAVALORN_MERKE_1H < other.hitchance[NPC_TALENT_1H]))
	{
		AI_Output(self,other,"DIA_Addon_Cavalorn_Teach_BACK_08_00");	//Od razu lepiej. Wiele zapomniałeś, ale doprowadzimy cię do formy.
	};
	Info_ClearChoices(dia_addon_cavalorn_teach);
};