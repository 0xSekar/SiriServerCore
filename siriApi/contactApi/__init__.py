#!/usr/bin/python
# -*- coding: utf-8 -*-

from plugin import *
from siriObjects.baseObjects import *
from siriObjects.contactObjects import *
from siriObjects.systemObjects import DomainObjectUpdate, DomainObjectUpdateCompleted, SendCommands, StartRequest, DomainObjectCommit, DomainObjectCommitCompleted, DomainObjectRetrieve, DomainObjectRetrieveCompleted
from siriObjects.uiObjects import *
import re
import random

text = {
	'numberNotPresent':{
		u'de-DE': u"Ich habe diese {0} von {1} nicht, aber eine andere.",
		u'en-US': u"Sorry, I don't have a {0} number from {1}, but another.",
		u'es-AR': u"Lo lamento, no tengo un número de {0} para {1} sino otro número."
	},
	'selectNumber':{
		u'de-DE': u"Welche Telefonnummer für {0}",
		u'en-US': u"Which phone one for {0}",
		u'es-AR': u"Qué número de teléfono para {0}?"
	},
	'errorNumberTypes':{
		u'de-DE': u"Ich habe dich nicht verstanden, versuch es bitte noch einmal.",
		u'en-US': u"Sorry, I did not understand, please try again.",
		u'es-AR': u"Lo siento, no entiendo, por favor inténtelo nuevamente."
	},
	'selectMail':{
		u'de-DE': u"Welche E-Mail adresse für {0}",
		u'en-US': u"Which E-Mail adress for {0}",
		u'es-AR': u"Qué dirección de E-Mail para {0}?"
	},
	'select':{
		u'de-DE': u"Welchen Kontakt genau?",
		u'en-US': u"What kind of contact exactly?",
		u'es-AR': u"Cuál contacto exactamente?"
	},
	'notFound':{
		u'de-DE':u"Ich konnte {0} nicht finden!",
		u'en-EN':u"I could not find {0}!",
		u'es-AR':u"Lo siento, no puedo encontrar {0} entre sus contactos!"
	},
	'notFoundRelation':{
		u'en-EN':u"Sorry, I don't know who is your {0}!",
		u'es-AR':u"Lo siento, no se quién es su {0}!"
	}
}

speakableDemitter = {
	'en-US': u", or ",
	'de-DE': u', oder ',
	'es-AR': u', o '
}

relationTypes = {
	'de-DE' :{
		u"mutter" : '_$!<Mother>!$_',
		u"vater" : '_$!<Father>!$_',
		u"elternteil" : '_$!<Parent>!$_',
		u"bruder" : '_$!<Brother>!$_',
		u"schwester" : '_$!<Sister>!$_',
		u"kind" : '_$!<Child>!$_',
		u"kontakt" : '_$!<Friend>!$_',
		u"ehepartner" : '_$!<Spouse>!$_',
		u"partner" : '_$!<Partner>!$_',
		u"assistent" : '_$!<Assistant>!$_',
		u"manager" : '_$!<Manager>!$_',
		u"andere" : '_$!<Other>!$_'
	},
	'en-EN' :{
		u"mother" : '_$!<Mother>!$_',
		u"father" : '_$!<Father>!$_',
		u"parent" : '_$!<Parent>!$_',
		u"brother" : '_$!<Brother>!$_',
		u"sister" : '_$!<Sister>!$_',
		u"child" : '_$!<Child>!$_',
		u"friend" : '_$!<Friend>!$_',
		u"spouse" : '_$!<Spouse>!$_',
		u"partner" : '_$!<Partner>!$_',
		u"assistant" : '_$!<Assistant>!$_',
		u"manager" : '_$!<Manager>!$_',
		u"other" : '_$!<Other>!$_'
	},
	'es-AR' :{
		u"madre" : '_$!<Mother>!$_',
		u"padre" : '_$!<Father>!$_',
		u"pariente" : '_$!<Parent>!$_',
		u"hermano" : '_$!<Brother>!$_',
		u"hermana" : '_$!<Sister>!$_',
		u"hijo" : '_$!<Child>!$_',
		u"hija" : '_$!<Child>!$_',
		u"amigo" : '_$!<Friend>!$_',
		u"cónyuge" : '_$!<Spouse>!$_',
		u"esposa" : '_$!<Spouse>!$_',
		u"esposo" : '_$!<Spouse>!$_',
		u"pareja" : '_$!<Partner>!$_',
		u"asistente" : '_$!<Assistant>!$_',
		u"jefe" : '_$!<Manager>!$_',
		u"otro" : '_$!<Other>!$_'
	}
}

numberTypes = {
	'de-DE' :{
		'_$!<Mobile>!$_': u"Handynummer",
		'iPhone': u"iPhone-Nummer",
		'_$!<Home>!$_': u"Privatnummer",
		'_$!<Work>!$_': u"Geschäftsnummer",
		'_$!<Main>!$_': u"Hauptnummer",
		'_$!<HomeFAX>!$_': u'private Faxnummer',
		'_$!<WorkFAX>!$_': u"geschäftliche Faxnummer",
		'_$!<OtherFAX>!$_': u"anderes Fax",
		'_$!<Pager>!$_': u"Pagernummer",
		'_$!<Other>!$_': u"anderes Telefon"
	},
	'en-EN' :{
		'_$!<Mobile>!$_': u"mobile",
		'iPhone': u"iPhone",
		'_$!<Home>!$_': u"home",
		'_$!<Work>!$_': u"work",
		'_$!<Main>!$_': u"main",
		'_$!<HomeFAX>!$_': u"home fax",
		'_$!<WorkFAX>!$_': u"work fax",
		'_$!<OtherFAX>!$_': u"other fax",
		'_$!<Pager>!$_': u"pager",
		'_$!<Other>!$_': u"other phone",
	},
	'es-AR' :{
		'_$!<Mobile>!$_': u"móvil",
		'iPhone': u"iPhone",
		'_$!<Home>!$_': u"casa",
		'_$!<Work>!$_': u"trabajo",
		'_$!<Main>!$_': u"principal",
		'_$!<HomeFAX>!$_': u"fax casa",
		'_$!<WorkFAX>!$_': u"fax trabajo",
		'_$!<OtherFAX>!$_': u"otro fax",
		'_$!<Pager>!$_': u"busca",
		'_$!<Other>!$_': u"otro teléfono",
	}
}

mailTypes = {
	'de-DE' :{
		'_$!<Home>!$_': u"Privatmail",
		'_$!<Work>!$_': u"Geschäftsmail",
		'_$!<Other>!$_': u"andere Mail"
	},
	'en-EN' :{
		'_$!<Home>!$_': u"home",
		'_$!<Work>!$_': u"work",
		'_$!<Other>!$_': u"other mail",
	},
	'es-AR' :{
		'_$!<Home>!$_': u"casa",
		'_$!<Work>!$_': u"trabajo",
		'_$!<Other>!$_': u"otro mail",
	}
}

numberTypesLocalized= {
'_$!<Mobile>!$_': {'en-US': u"mobile", 'de-DE': u"Handynummer", 'es-AR': u"Móvil"},
'iPhone': {'en-US': u"iPhone", 'de-DE': u"iPhone-Nummer", 'es-AR': u"iPhone"},
'_$!<Home>!$_': {'en-US': u"home", 'de-DE': u"Privatnummer", 'es-AR': u"Casa"},
'_$!<Work>!$_': {'en-US': u"work", 'de-DE': u"Geschäftsnummer", 'es-AR': u"Trabajo"},
'_$!<Main>!$_': {'en-US': u"main", 'de-DE': u"Hauptnummer", 'es-AR': u"Principal"},
'_$!<HomeFAX>!$_': {'en-US': u"home fax", 'de-DE': u'private Faxnummer', 'es-AR': u"Fax casa"},
'_$!<WorkFAX>!$_': {'en-US': u"work fax", 'de-DE': u"geschäftliche Faxnummer", 'es-AR': u"Fax trabajo"},
'_$!<OtherFAX>!$_': {'en-US': u"_$!<OtherFAX>!$_", 'de-DE': u"_$!<OtherFAX>!$_", 'es-AR': u"_$!<OtherFAX>!$_"},
'_$!<Pager>!$_': {'en-US': u"pager", 'de-DE': u"Pagernummer", 'es-AR': u"Busca"},
'_$!<Other>!$_':{'en-US': u"other phone", 'de-DE': u"anderes Telefon", 'es-AR': u"Otro teléfono"}
}

namesToNumberTypes = {
'de-DE': {'mobile': "_$!<Mobile>!$_", 'handy': "_$!<Mobile>!$_", 'zuhause': "_$!<Home>!$_", 'privat': "_$!<Home>!$_", 'arbeit': "_$!<Work>!$_"},
'en-US': {'work': "_$!<Work>!$_",'home': "_$!<Home>!$_", 'mobile': "_$!<Mobile>!$_"},
'es-AR': {'trabajo': "_$!<Work>!$_",'casa': "_$!<Home>!$_", u'móvil': "_$!<Mobile>!$_", u'movil': "_$!<Mobile>!$_", 'privado': "_$!<Home>!$_"}
}

identifierRetriever = re.compile("\^phoneCallContactId\^=\^urn:ace:(?P<identifier>.*)")

def replaceNumberType(name, language):
	if language == "de-DE":
		if re.search(r"(?i)iphone(.*)nummer", name):
			return 'iPhone'
		if re.search(r"(?i)handy(.*)nummer", name):
			return '_$!<Mobile>!$_'
		if re.search(r"(?i)privat(.*)nummer", name):
			return '_$!<Home>!$_'
		if re.search(r"(?i)geschäfts(.*)nummer", name):
			return '_$!<Work>!$_'
		if re.search(r"(?i)haupt(.*)nummer", name):
			return '_$!<Main>!$_'
		if name == "private Faxnummer":
			return '_$!<HomeFAX>!$_'
		if name == "geschäftliche Faxnummer":
			return '_$!<WorkFAX>!$_'
		if name == "anderes Fax":
			return '_$!<OtherFAX>!$_'
		if re.search(r"(?i)pager(.*)nummer", name):
			return '_$!<Pager>!$_'
		if name == "anderes Telefon":
			return '_$!<Other>!$_'
	if language == "en-EN":
		if name == "mobile":
			return '_$!<Mobile>!$_'
		if name == "iPhone":
			return 'iPhone'
		if name == "home":
			return '_$!<Home>!$_'
		if name == "work":
			return '_$!<Work>!$_'
		if name == "main":
			return '_$!<Main>!$_'
		if name == "home fax":
			return '_$!<HomeFAX>!$_'
		if name == "work fax":
			return '_$!<WorkFAX>!$_'
		if name == "other fax":
			return '_$!<OtherFAX>!$_'
		if name == "pager":
			return '_$!<Pager>!$_'
		if name == "other phone":
			return '_$!<Other>!$_'
        if language == "es-AR":
                if name == "móvil":
                        return '_$!<Mobile>!$_'
                if name == "movil":
                        return '_$!<Mobile>!$_'
                if name == "iPhone":
                        return 'iPhone'
                if name == "casa":
                        return '_$!<Home>!$_'
                if name == "trabajo":
                        return '_$!<Work>!$_'
                if name == "principal":
                        return '_$!<Main>!$_'
                if name == "fax casa":
                        return '_$!<HomeFAX>!$_'
                if name == "fax trabajo":
                        return '_$!<WorkFAX>!$_'
                if name == "otro fax":
                        return '_$!<OtherFAX>!$_'
                if name == "busca":
                        return '_$!<Pager>!$_'
                if name == "otro teléfono":
                        return '_$!<Other>!$_'

def replaceMailType(name, language):
	if language == "de-DE":
		if re.search(r"(?i)privat(.*)mail", name):
			return '_$!<Home>!$_'
		if re.search(r"(?i)geschäfts(.*)mail", name):
			return '_$!<Work>!$_'
		if name == "andere E-Mail":
			return '_$!<Other>!$_'
	if language == "en-EN":
		if name == "home":
			return '_$!<Home>!$_'
		if name == "work":
			return '_$!<Work>!$_'
		if name == "other mail":
			return '_$!<Other>!$_'
        if language == "es-AR":
                if name == "casa":
                        return '_$!<Home>!$_'
                if name == "trabajo":
                        return '_$!<Work>!$_'
                if name == "otro mail":
                        return '_$!<Other>!$_'
		
def getNumberTypeForName(name, language):
	# q&d
	if name != None:
		if name.lower() in namesToNumberTypes[language]:
			return namesToNumberTypes[language][name.lower()]
		else:
			for key in numberTypesLocalized.keys():
				if numberTypesLocalized[key][language].lower() == name.lower():
					return numberTypesLocalized[key][language]
	return name

def findPhoneForNumberType(plugin, person, numberType, language):
	number = None
	if numberType != None:
		number = filter(lambda x: x.label == numberType, person.phones)
	        if len(number) == 0:
         		number = None
                else:
                	number = number[0]

	else:
		favPhones = filter(lambda y: y.favoriteVoice if hasattr(y, "favoriteVoice") else False, person.phones)
		if len(favPhones) == 1:
			number = favPhones[0]
	if number == None:
		if len(person.phones) == 1:
			if numberType != None:
				plugin.say(text["numberNotPresent"][language].format(numberTypes[language][numberType], person.fullName))
			number = person.phones[0]
		else:
			while(number == None):
				rootView = UIAddViews(plugin.refId)
				rootView.temporary = False
				rootView.dialogPhase = "Clarification"
				rootView.scrollToTop = False
				rootView.views = []
				sayit = text['selectNumber'][language].format(person.fullName)
				assistant = UIAssistantUtteranceView()
				assistant.text = assistant.speakableText = sayit
				assistant.listenAfterSpeaking = True
				assistant.dialogIdentifier = "ContactDataResolutionDucs#foundAmbiguousPhoneNumberForContact"
				rootView.views.append(assistant)
				lst = UIDisambiguationList()
				lst.items = []
				lst.speakableSelectionResponse = "OK..."
				lst.listenAfterSpeaking = True
				lst.speakableText = ""
				lst.speakableFinalDemitter = speakableDemitter[language]
				lst.speakableDemitter = ", "
				lst.selectionResponse = "OK..."
				rootView.views.append(lst)
				for phone in person.phones:
					numberType = numberTypesLocalized[phone.label][language] if phone.label in numberTypesLocalized else phone.label
					item = UIListItem()
					item.title = ""
					item.text = u"{0}: {1}".format(numberType, phone.number)
					item.selectionText = item.text
					item.speakableText = u"{0}  ".format(numberType)
					item.object = phone
					item.commands = [SendCommands(commands=[StartRequest(handsFree=False, utterance=numberType)])]
					lst.items.append(item)
				answer = plugin.getResponseForRequest(rootView)
				answer = getNumberTypeForName(answer, language)
				numberType = answer
				if numberType != None:
					matches = filter(lambda x: x.label == numberType, person.phones)
					if len(matches) == 1:
						number = matches[0]
					else:
						plugin.say(text['errorNumberTypes'][language])
				else:
					plugin.say(text['errorNumberTypes'][language])
	return number

def findMailForMailType(plugin, person, mailType, language):
	mail = None
	if mailType != None:
		mailToWrite = filter(lambda x: x.label == mailType, person.emails)
	else:
		favMails = filter(lambda y: y.favoriteVoice if hasattr(y, "favoriteVoice") else False, person.emails)
		if len(favMails) == 1:
			mail = favMails[0]
	if mail == None:
		if len(person.emails) == 1:
			if mailType != None:
				plugin.say(text["numberNotPresent"][language].format(mailTypes[language][mailType], person.fullName))
			mail = person.emails[0]
		else:
			while(mail == None):
				rootView = UIAddViews(plugin.refId)
				rootView.temporary = False
				rootView.dialogPhase = "Clarification"
				rootView.scrollToTop = False
				rootView.views = []
				sayit = text['selectMail'][language].format(person.fullName)
				assistant = UIAssistantUtteranceView()
				assistant.text = assistant.speakableText = sayit
				assistant.listenAfterSpeaking = True
				assistant.dialogIdentifier = "ContactDataResolutionDucs#foundAmbiguousMailForContact"
				rootView.views.append(assistant)
				lst = UIDisambiguationList()
				lst.items = []
				lst.speakableSelectionResponse = "OK..."
				lst.listenAfterSpeaking = True
				lst.speakableText = ""
				lst.speakableFinalDemitter = speakableDemitter[language]
				lst.speakableDemitter = ", "
				lst.selectionResponse = "OK..."
				rootView.views.append(lst)
				for email in person.emails:
					mailType = email.label
					item = UIListItem()
					item.title = ""
					item.text = u"{0}: {1}".format(mailTypes[language][mailType], email.emailAddress)
					item.selectionText = item.text
					item.speakableText = u"{0}  ".format(mailTypes[language][mailType])
					item.object = email
					item.commands = []
					item.commands.append(SendCommands(commands=[StartRequest(handsFree=False, utterance=mailTypes[language][mailType])]))
					lst.items.append(item)
				answer = plugin.getResponseForRequest(rootView)
				answer = replaceMailType(answer, language)
				mailType = answer
				if mailType != None:
					matches = filter(lambda x: x.label == mailType, person.emails)
					if len(matches) == 1:
						mail = matches[0]
					else:
						plugin.say(text['errorNumberTypes'][language])
				else:
					plugin.say(text['errorNumberTypes'][language])
	return mail

def searchPerson(plugin, scope, relatedNames=None, phone=None, name=None, me=None, email=None, company=None, birthday=None, adress=None):
	search = ABPersonSearch(plugin.refId)
	search.scope = scope
	search.relatedNames = relatedNames
	search.phone = phone
	search.name = name
	search.me = me
	search.email = email
	search.company = company
	search.birthday = birthday
	search.address = adress
	answerObj = plugin.getResponseForRequest(search)
	if ObjectIsCommand(answerObj, ABPersonSearchCompleted):
		answer = ABPersonSearchCompleted(answerObj)
		return answer.results if answer.results != None else []
	else:
		raise StopPluginExecution("Unknown response: {0}".format(answerObj))
	return []

def getRelation(plugin, relation, language):
	if relation != None:
		if relation.lower() in relationTypes[language]:
			return relationTypes[language][relation.lower()]
	return relation

def relatedNamesAction(plugin, personsData, relation, language):
	root = UIAddViews(plugin.refId)
	root.scrollToTop = False
	root.temporary = False
	root.dialogPhase = "Clarification"
	root.views = []
	root.callbacks = []
	assistant = UIAssistantUtteranceView()
	assistant.text = assistant.speakableText = text["select"][language]
	assistant.dialogIdentifier = "ContactDataResolutionDucs#disambiguateContact"
	assistant.listenAfterSpeaking = True
	root.views.append(assistant)
	lst = UIDisambiguationList()
	lst.items = []
	lst.speakableSelectionResponse = "OK!"
	lst.listenAfterSpeaking = True
	lst.speakableText = ""
	lst.speakableFinalDemitter = speakableDemitter
	lst.speakableDemitter = ", "
	lst.selectionResponse = "OK!"
	root.views.append(lst)
	i = 0
	returnData = None
	for person in personsData:
		if person.label == relation:
			i += 1
	if i > 0:
		if i == 1:
			for person in personsData:
				if person.label == relation:
					returnData = person.name
		else:
			for person in personsData:
				if person.label == relation:
					item = UIListItem()
					item.title = person.name
					item.selectionText = person.name
					item.commands = []
					item.speakableText = person.name
					item.object = person
					#
					#
					#
					#
					# should we not better use the identifier here? name is not really unique
					item.commands.append(SendCommands([StartRequest(False, person.name)]))
					lst.items.append(item)
			returnData = plugin.getResponseForRequest(root)
	return returnData

def presentPossibleUsers(plugin, persons, language):
	root = UIAddViews(plugin.refId)
	root.scrollToTop = False
	root.temporary = False
	root.dialogPhase = "Clarification"
	root.views = []
	root.callbacks = []
	assistant = UIAssistantUtteranceView()
	assistant.text = assistant.speakableText = text["select"][language]
	assistant.dialogIdentifier = "ContactDataResolutionDucs#disambiguateContact"
	assistant.listenAfterSpeaking = True
	root.views.append(assistant)
	lst = UIDisambiguationList()
	lst.items = []
	lst.speakableSelectionResponse = "OK!"
	lst.listenAfterSpeaking = True
	lst.speakableText = ""
	lst.speakableFinalDemitter = speakableDemitter
	lst.speakableDemitter = ", "
	lst.selectionResponse = "OK!"
	root.views.append(lst)
	for person in persons:
		item = UIListItem()
		item.title = person.fullName
		item.selectionText = person.fullName
		item.speakableText = person.fullName
		item.object = person
		#use the identifier here, it can distinquish better between users
		item.commands = [SendCommands([StartRequest(False, "^phoneCallContactId^=^urn:ace:{0}".format(person.identifier))])]
		lst.items.append(item)
	return root

def personAction(plugin, personsData, language):
	person = None
	if len(personsData) > 0:
		if len(personsData) == 1:
			person = personsData[0]
		else:
			while(person == None):
				choosenPerson = plugin.getResponseForRequest(presentPossibleUsers(plugin, personsData, language))
				choosenPersonIdentifier = identifierRetriever.match(choosenPerson)
				if choosenPersonIdentifier:
					choosenPersonIdentifier = choosenPersonIdentifier.group("identifier")
				for personData in personsData:
					if choosenPersonIdentifier == personData.identifier or choosenPerson == personData.fullName:
						person = personData
				if person == None:
                        		plugin.say(text['errorNumberTypes'][language].format(choosenPersonIdentifier))

	if person != None:
			return person
	else:
		return None

def definePerson(plugin, scope, name, relation, me, language):
	if relation != None:
		relationEnc = getRelation(plugin, relation, language)
		if me == True or name == None:
			relationPerson = searchPerson(plugin, scope="Local", me=True)[0]
		else:
			relationPerson = searchPerson(plugin, scope="Local", name=name)[0]
		name = relatedNamesAction(plugin, relationPerson.relatedNames, relationEnc, language)
	if name == None:
		plugin.say(text['notFoundRelation'][language].format(relation))
		plugin.complete_request()
		return None
	else :
		for person in relationPerson.relatedNames:
			if person.label == relationEnc:
				if name in person.name:
					name = person.name
		personsData = searchPerson(plugin, scope=scope, name=name)
		if personsData == [] and name[-1] == "s":
			name = name[:-1]
			personsData = searchPerson(plugin, scope=scope, name=name)

		personData = personAction(plugin, personsData, language)
		if personData != None:
			return personData
		else:
			plugin.say(text['notFound'][language].format(name))
			plugin.complete_request()
			return None
