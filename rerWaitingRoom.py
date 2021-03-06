#!/usr/bin/python
# TODO
#  -- Parrallelise la recherche sur internet ;

import urllib.request
import re
import sys
import os
import datetime
import time
import optparse

# Dictionnaire donnant la gare de destination du RER en fonction de la premiere lettre de son code mission.
missions_data = {
		"A":"Gare du Nord",
		"C":"Cite universitaire (exceptionnel)",
		"E":"Aeroport Charles-de-Gaulle 2 TGV",
		"G":"Aulnay-sous-Bois",
		"H":"Bourg-la-Reine (exceptionnel)",
		"I":"Mitry - Claye",
		"J":"Denfert-Rochereau",
		"K":"Massy - Palaiseau",
		"L":"Orsay - Ville",
		"M":"Chatelet - Les Halles (exceptionnel)",
		"N":"La Croix de Berny (exceptionnel)",
		"O":"Aeroport Charles-de-Gaulle 1 (exceptionnel)",
		"P":"Saint-Remy-les-Chevreuse",
		"Q":"La Plaine - Stade de France",
		"S":"Robinson",
		"U":"Laplace",
		}

# Dictionnaire donnant la direction du RER en fonction de la premiere lettre de son code mission.
directions_data = {
		"A":"N",
		"C":"N",
		"E":"N",
		"G":"N",
		"H":"S",
		"I":"N",
		"J":"S",
		"K":"S",
		"L":"S",
		"M":"N",
		"N":"S",
		"O":"N",
		"P":"S",
		"Q":"N",
		"S":"S",
		"U":"S",
		}

# Liste des gares du troncons nord du RER B.
gares_data = [
		"Aeroport Charles-de-Gaulle 2 TGV",
		"Aeroport Charles-de-Gaulle 1"    ,
		"Parc des Expositions"            ,
		"Villepinte"                      ,
		"Sevran - Beaudottes"             ,
		"Mitry - Claye"                   ,
		"Villeparisis - Mitry-le-Neuf"    ,
		"Vert-Galant"                     ,
		"Sevran - Livry"                  ,
		"Aulnay-sous-Bois"                ,
		"Le Blanc-Mesnil"                 ,
		"Drancy"                          ,
		"Le Bourget"                      ,
		"La Courneuve - Aubervilliers"    ,
		"La Plaine - Stade de France"     ,
		"Gare du Nord"                    ,
		]

# Code trigramme pour chaque gare
gares_code = {
		"Aeroport Charles-de-Gaulle 2 TGV":"CG2",
		"Aeroport Charles-de-Gaulle 1"    :"CG1",
		"Parc des Expositions"            :"PDE",
		"Villepinte"                      :"VLP",
		"Sevran - Beaudottes"             :"SVB",
		"Mitry - Claye"                   :"MYC",
		"Villeparisis - Mitry-le-Neuf"    :"VMN",
		"Vert-Galant"                     :"VGL",
		"Sevran - Livry"                  :"SLI",
		"Aulnay-sous-Bois"                :"ASB",
		"Le Blanc-Mesnil"                 :"BMN",
		"Drancy"                          :"DRY",
		"Le Bourget"                      :"BRG",
		"La Courneuve - Aubervilliers"    :"CAV",
		"La Plaine - Stade de France"     :"SDF",
		"Gare du Nord"                    :"GDN"
		}

# Dictionnaire donnant un code d'ordre de precedence en fonction du nom de la gare.
# Le premier nombre du code indique la branche (0 : branche commune, 1 : branche mitry, 2 : branche CDG).
# Le second nombre du code indique la position de la station dans la branche.
# Ainsi, pour etre comparer, les stations doivent avoir le meme premier nombre, ou l'une des deux doit avoir un premier nombre nul.
garesOrder_data = {
      "Aeroport Charles-de-Gaulle 2 TGV": (2,11),
		"Aeroport Charles-de-Gaulle 1"    : (2,10),
		"Parc des Expositions"            : (2,9),
		"Villepinte"                      : (2,8),
		"Sevran - Beaudottes"             : (2,7),
		"Mitry - Claye"                   : (1,10),
		"Villeparisis - Mitry-le-Neuf"    : (1,9),
		"Vert-Galant"                     : (1,8),
		"Sevran - Livry"                  : (1,7),
		"Aulnay-sous-Bois"                : (0,6),
		"Le Blanc-Mesnil"                 : (0,5),
		"Drancy"                          : (0,4),
		"Le Bourget"                      : (0,3),
		"La Courneuve - Aubervilliers"    : (0,2),
		"La Plaine - Stade de France"     : (0,1),
		"Gare du Nord"                    : (0,0),
        }

# Dictionnaire donnant la requete a faire sur le site transilien pour avoir la liste des missions desservant la gare.
requests_data = {
		"Aeroport Charles-de-Gaulle 2 TGV": "http://www.transilien.com/gare/pagegare/filterListeTrains?codeTR3A=RYR&destination=PARIS+NORD&ligne=&nomGare=AEROPORT+CHARLES+DE+GAULLE+2+TGV+-+Roissy&x=28&y=10",
		"Aeroport Charles-de-Gaulle 1"    : "http://www.transilien.com/gare/pagegare/filterListeTrains?codeTR3A=RSY&destination=PARIS+NORD&ligne=&nomGare=AEROPORT+CHARLES+DE+GAULLE++1+-+Roissy&x=45&y=12",
		"Parc des Expositions"            : "http://www.transilien.com/gare/pagegare/filterListeTrains?codeTR3A=PEX&destination=PARIS+NORD&ligne=&nomGare=PARC+DES+EXPOSITIONS&x=18&y=16",
		"Villepinte"                      : "http://www.transilien.com/gare/pagegare/filterListeTrains?codeTR3A=VPN&destination=PARIS+NORD&ligne=&nomGare=VILLEPINTE&x=26&y=13",
		"Sevran - Beaudottes"             : "http://www.transilien.com/gare/pagegare/filterListeTrains?codeTR3A=BDE&destination=PARIS+NORD&ligne=&nomGare=SEVRAN+BEAUDOTTES&x=44&y=10",
		"Mitry - Claye"                   : "http://www.transilien.com/gare/pagegare/filterListeTrains?codeTR3A=MY&destination=PARIS+NORD&ligne=&nomGare=MITRY+CLAYE&x=17&y=17",
		"Villeparisis - Mitry-le-Neuf"    : "http://www.transilien.com/gare/pagegare/filterListeTrains?codeTR3A=VII&destination=PARIS+NORD&ligne=&nomGare=VILLEPARISIS+MITRY+LE+NEUF&x=16&y=23",
		"Vert-Galant"                     : "http://www.transilien.com/gare/pagegare/filterListeTrains?codeTR3A=VGL&destination=PARIS+NORD&ligne=&nomGare=VERT+GALANT&x=24&y=12",
		"Sevran - Livry"                  : "http://www.transilien.com/gare/pagegare/filterListeTrains?codeTR3A=SEV&destination=PARIS+NORD&ligne=&nomGare=SEVRAN+LIVRY&x=22&y=14",
		"Aulnay-sous-Bois"                : "http://www.transilien.com/gare/pagegare/filterListeTrains?codeTR3A=AB&destination=PARIS+NORD&ligne=&nomGare=AULNAY+SOUS+BOIS&x=40&y=18",
		"Le Blanc-Mesnil"                 : "http://www.transilien.com/gare/pagegare/filterListeTrains?codeTR3A=BAM&destination=PARIS+NORD&ligne=&nomGare=LE+BLANC+MESNIL&x=14&y=20",
		"Drancy"                          : "http://www.transilien.com/gare/pagegare/filterListeTrains?codeTR3A=DRN&destination=PARIS+NORD&ligne=&nomGare=DRANCY&x=19&y=13",
		"Le Bourget"                      : "http://www.transilien.com/gare/pagegare/filterListeTrains?codeTR3A=LBT&destination=PARIS+NORD&ligne=&nomGare=LE+BOURGET&x=43&y=6",
		"La Courneuve - Aubervilliers"    : "http://www.transilien.com/gare/pagegare/filterListeTrains?codeTR3A=ALC&destination=PARIS+NORD&ligne=&nomGare=LA+COURNEUVE+AUBERVILLIERS&x=47&y=13",
		"La Plaine - Stade de France"     : "http://www.transilien.com/gare/pagegare/filterListeTrains?codeTR3A=LPN&destination=PARIS+NORD&ligne=&nomGare=LA+PLAINE+STADE+DE+FRANCE+-+Saint-Denis+Aubervilliers&x=29&y=16",
		"Gare du Nord"                    : "http://www.transilien.com/gare/pagegare/filterListeTrains?codeTR3A=GDS&destination=SAINT-MICHEL+NOTRE+DAME&ligne=&nomGare=PARIS+NORD+%28GARE+DU+NORD%29&x=39&y=14",
		}


# Pattern (generique puis plus precis)
patternListTrain = re.compile(b"gare/pagegare/detailDesserteTrain.*>")
patternTrain = re.compile(b"numeroTrain=\w\w\w\w\d\d")
patternHeureProbable = re.compile(b"heureProbable=\d\d:\d\d")
patternHeureTheorique = re.compile(b"heureTheorique=\d\d:\d\d")


def getGareOrder(gare1,gare2):
	"""return 1 sur gare 1 avant gare 2, -1 si gare 2 avant gare 1, 0 si incomparable."""
	positionGare1 = garesOrder_data[gare1]
	positionGare2 = garesOrder_data[gare2]
	# meme sous branche
	if positionGare1[0] == positionGare2[0]:
		return 1 if positionGare1[1] >= positionGare2[1] else -1
	# sous branche differente.
	else:
		if positionGare1[0] != 0 and positionGare2[0] != 0:
			# Les branches sont incomparables
			return 0
		else:
			return 1 if positionGare1[0] >= positionGare2[0] else -1


def getTrainFromRequest(request):
	"""
		Effectue la requete sur le site transilien pour renvoier la liste des missions avec leur horaires theorique et probable.
		nbTry (100) tentatives sont lance, si aucune ne fonctionne une liste vide est renvoye.
	"""
	# Requete.
	success = False
	nbTry = 100
	for i in range(0,nbTry):
		try:
			page = urllib.request.urlopen(request)
			success = True
		except(KeyboardInterrupt, SystemExit):
			sys.exit(0)
		except:
			continue
		break
	if not success:
		print("Echec apres %d tentatives" % nbTry)
		return []

	# Exploitation du resultat de la requete/
	content = page.read()
	res = patternListTrain.findall(content)
	trainRoissyVersParisNord = []
	for r in res:
		nameTrain = patternTrain.findall(r)
		probableHourTrain = patternHeureProbable.findall(r)
		theoricalHourTrain = patternHeureTheorique.findall(r)
		
		name = ""
		theoricalHour = ""
		probableHour = ""

		if len(nameTrain):
			name = nameTrain[0].decode("utf-8")[-6:]
		if len(probableHourTrain):
			probableHour = probableHourTrain[0].decode("utf-8")[-5:]
		if len(theoricalHourTrain):
			theoricalHour = theoricalHourTrain[0].decode("utf-8")[-5:]

		if len(name) and len(probableHour) and len (theoricalHour):
			if name[0] in directions_data.keys() and directions_data[name[0]] == "S":
				trainRoissyVersParisNord.append((name,probableHour,theoricalHour))
	return trainRoissyVersParisNord


def getTrainFromStation(gare):
	"""Renvoie la liste des missions avec leur horaires theorique et probable de la gare."""
	return getTrainFromRequest(requests_data[gare])
	

def getWaitingQueue(passageInGare):
	"""
		Return un dictionnaire avec en cle le nom des mission de passageInGare avec 
		en valeur leur position dans la file d'attente pour gare du Nord.
		passageInGare est un dictionnaire associant pour chaque gare (en cle) les prochaines missions desservant cette gare.
	"""
	# Initialisation
	waitingQueue = {}
	waitingQueue[passageInGare[gares_data[-1]][0][0]] = 0
	pos = 0
	currentPosition = pos
	# Recuperation de l'ordre de passage par methode naive. 
	for gare in reversed(gares_data):
		for mission in passageInGare[gare]:
			if mission[0] in waitingQueue:
				currentPosition = max(pos, waitingQueue[mission[0]])
			else:
				currentPosition = currentPosition + 1
				waitingQueue[mission[0]] = currentPosition
				pos = currentPosition

	# Correction de la methode naive par des swaps jusqu'a obtention d'une solution coherente.
	# Fonctionnement des swap : pour chaque gare si on trouve une mission A passant avant une mission B alors que
	# leur position courante dans la queue indique le contraire alors on change leur position dans la queue pour
	# obtenir un resultat plus coherent.
	doContinue = True
	nbIter = 0
	while doContinue:
		nbIter = nbIter + 1
		doContinue = False
		for gare in reversed(gares_data):
			for i in range(0,len(passageInGare[gare])-1):
					mission1Name = passageInGare[gare][i][0]
					mission2Name = passageInGare[gare][i+1][0]
					pos1 = waitingQueue[mission1Name]
					pos2 = waitingQueue[mission2Name]
					if pos1 > pos2:
						waitingQueue[mission1Name] = pos2
						waitingQueue[mission2Name] = pos1
						doContinue = True
						break
			if doContinue:
				break
		if nbIter > 1000:
			break
	return waitingQueue


def getNewLine(gare):
	return "| "
	alignIdx = garesOrder_data[gare][0]
	alignValue = 1 
	if alignIdx == 1 : 
		alignValue = 2
	elif alignIdx == 2:
		alignValue = 0
	else:
		alignValue = 1
	return " " * 35 * alignValue + "| "

def getAllTrainForAllStation():
	"""
		Renvoie un dictionnaire associant a chaque gare les futurs missions.
	"""
	return dict(zip(gares_data, map(getTrainFromStation,gares_data)))


def getNextStationForMissionStrict(passageGare):
	"""
		Renvoie un dictionnaire associant pour chaque mission la prochaine gare strictement desservie par la mission
		Entree. Dictionnaire associant a chaque gare les prochaines missions desservant la gare.
		La notion de "strict" signifie ici que la station est vraiment desservie (le train s'y arrete)
	"""
	nextStationForMission = {}
	for gare in reversed(gares_data):
		for mission in passageGare[gare]:
			nextStationForMission[mission[0]] = gare
	return nextStationForMission

def getNextStationForMissionHeuristic(passageGare, positionByMission):
	"""
		Renvoie un dictionnaire associant pour chaque mission la prochaine gare desservie par la mission (methode heuristique)
		Entree. Dictionnaire associant a chaque gare les prochaines missions desservant la gare.
		La notion de "heuristique" signifie ici que la station n'est pas necessairement desservie mais on "imagine" que c'est la prochaine desservie.
	"""
	nextStationForMission = getNextStationForMissionStrict(passageGare)

	changeDone = True
	nbIter = 0
	while changeDone and nbIter < 1000:
		nbIter += 1
		changeDone = False
		for missionA in positionByMission.keys():
			for missionB in positionByMission.keys():
				if missionA == missionB:
					continue
				nextStationA = nextStationForMission[missionA]
				nextStationB = nextStationForMission[missionB]
				if nextStationA == nextStationB:
					continue
				if garesOrder_data[nextStationA][0] != garesOrder_data[nextStationB][0]:
					continue
				# Temporel : A est avant B (son numero de mission est avant)
				# Spatial : la prochaine station desservie par A est avant la prochaine station desservie par B
				if positionByMission[missionA] < positionByMission[missionB] and getGareOrder(nextStationA,nextStationB) == 1:
					nextStationForMission[missionB] = nextStationA
					changeDone = True
					break
			if changeDone:
				break

	return nextStationForMission

def getNextStationForMission(passageGare, positionByMission=[]):
	"""
		Renvoie un dictionnaire associant pour chaque mission la prochaine gare desservie par la mission
		Entree. Dictionnaire associant a chaque gare les prochaines missions desservant la gare.
	"""
	#return getNextStationForMissionStrict(passageGare)
	return getNextStationForMissionHeuristic(passageGare,positionByMission)

def makeOutputString(dataToPrintByStation, highLightedStation=""):
	outputString = ""
	linesToPrint = []
	linesToPrintLeft = []
	linesToPrintRight = []
	linesToPrintCenter = []
	for gare in gares_data:
		printer = linesToPrintCenter
		if garesOrder_data[gare][0] == 1 :
			printer = linesToPrintRight
		elif garesOrder_data[gare][0] == 2:
			printer = linesToPrintLeft
		for dataChunkToPrint in dataToPrintByStation[gare]:
			thisLine = getNewLine(gare)
			thisLine += dataChunkToPrint
			printer.append(thisLine)
		thisLine = getNewLine(gare)
		thisLine += ("* " if gare == highLightedStation else "") + gare
		printer.append(thisLine)

	nbLinesToComplete = len(linesToPrintRight) - len(linesToPrintLeft)
	linesToPrintToComplete = linesToPrintLeft
	if nbLinesToComplete < 0:
		nbLinesToComplete = -nbLinesToComplete
		linesToPrintToComplete = linesToPrintRight
		
	for i in range(0,nbLinesToComplete):
		linesToPrintToComplete.insert(0,"")


	for i in range(0, max(len(linesToPrintRight), len(linesToPrintLeft))):
		s = ""
		if i < len(linesToPrintLeft):
			s += linesToPrintLeft[i]
		else:
			s += getNewLine(gare)
		if i < len(linesToPrintRight):
			s += " " * (60 - len(s)) + linesToPrintRight[i]
		else:
			s += " " * (60 - len(s)) + getNewLine(gare)
		linesToPrint.append(s)

	linesToPrint.append("\ " + " " * 58 + "/") 
	linesToPrint.append("  " + "-" * 27 + " " * 3 + "-" * 28  + " ") 
	linesToPrint.append("  " + " " * 27 + "\ /"  + " " * 28  + " ") 
	for line in linesToPrintCenter:
		linesToPrint.append(" " * 30 + line)

	for line in linesToPrint:
		outputString += line + "\n"
	
	return outputString

def getNextStationsAndDelay(passageInGare):
	# Pour chaque mission association de la liste des gare desservie avec l'horaire.
	stationsByMission = {}
	for gare in reversed(gares_data):
		for mission in passageInGare[gare]:
			key = mission[0]
			if not key in stationsByMission:
				stationsByMission[key] = []
			FMT = '%H:%M'
			forecastTime = datetime.datetime.strptime(mission[1], FMT)
			theoricTime = datetime.datetime.strptime(mission[2], FMT)
			delay = forecastTime - theoricTime
			stationsByMission[key].append((gare,forecastTime,theoricTime,delay))
	return stationsByMission

def computeResult(passageGare):
	# Calcul de l'ordre de passage a Gare du Nord  pour chaque mission.
	positionByMission = getWaitingQueue(passageGare)
	# "Inversion" du dictionnaire suivant pour recuperer la mission en fonction de l'ordre de passage a Gare du Nord.
	missionByPosition = dict(zip(positionByMission.values(),positionByMission.keys()))
	# Recuperation de la position de la mission (on associe a chaque mission sa prochaine gare).
	nextStationForMission = getNextStationForMission(passageGare, positionByMission)

	# Recuperation des prochaines missions a passer par la gare G lorsque la gare G est la prochaine gare desservie par la mission pour chaque gare G.
	#   Initialisation du dictionnaire.
	nextMissionsToStation = dict((gare, []) for gare in gares_data)
	#   Calcul
	for mission in nextStationForMission.keys():
		nextMissionsToStation[nextStationForMission[mission]].append(mission)

	# Pour chaque mission association de la liste des gare desservie avec l'horaire.
	stationsByMission = getNextStationsAndDelay(passageGare)

	dataToPrintByStation = dict((gare,[]) for gare in gares_data)
	for gare in gares_data:        
		if gare in nextMissionsToStation:
			for number in reversed(sorted(missionByPosition.keys())):
				if missionByPosition[number] in nextMissionsToStation[gare]:
					mission = missionByPosition[number]
					dataToPrintByStation[gare].append(missionByPosition[number] + "  (" + str(number + 1) + ") " + stationsByMission[mission][0][0] + " " + stationsByMission[mission][0][1].strftime("%H:%M") + " " + str(stationsByMission[mission][0][3])[:-3]  )
	return dataToPrintByStation

def printJustStation(code,passageGare={}):
	stationByCode = dict(zip(gares_code.values(),gares_code.keys()))
	nextMissions=[]
	if len(passageGare):
		nextMissions = passageGare[stationByCode[code]]
	else:
		nextMissions = getTrainFromStation(stationByCode[code])

	print(stationByCode[code])
	for mission in nextMissions:
		print("%s  %s  (%s)" % (mission[0],mission[1],mission[2]))

def stateLessMode(printAllStation = False):
	# Recuperation pour chaque gare des prochains train desservant la gare.
	passageGare = getAllTrainForAllStation()

	dataToPrintByStation = computeResult(passageGare)

	# Affichage
	print(makeOutputString(dataToPrintByStation))

	if printAllStation:
		for pos in range(2,-1,-1):
			resToPrint=""
			for station in gares_data:
				if garesOrder_data[station][0] != pos:
					continue
				resToPrint += "%-35s" % (station)
			resToPrint += "\n"
			for numMission in range(0,6):
				for station in gares_data:
					if garesOrder_data[station][0] != pos:
						continue
					if len(passageGare[station]) <= numMission:
						resToPrint += " " * 35
					else:
						mission = passageGare[station][numMission]
						resToPrint += ("%-35s" % ("%s  %s  (%s)" % (mission[0],mission[1],mission[2])))
				resToPrint += "\n"
			print(resToPrint)


def stateFullMode(printAllStation = False):
	# Recuperation initial pour chaque gare des prochains train desservant la gare.
	passageGare = getAllTrainForAllStation()

	snapshot=0
	while True:
		# Gare a mettre a jour (mise a jour succesive)
		for currentStation in reversed(gares_data):
			snapshot += 1
			beginSnapshot = datetime.datetime.now() 

			# Mise a jour des prochains passages a cette gare
			passageGare[currentStation] = getTrainFromStation(currentStation)
			
			dataToPrintByStation = computeResult(passageGare)

			# Affichage
			os.system("clear")
			print("%4d -- %s -- %s" % (snapshot, beginSnapshot.strftime("%Y/%m/%d %H:%M:%S"),currentStation))
			print(makeOutputString(dataToPrintByStation, currentStation))
			#print(passageGare[gares_data[-1]])

	return 0


if __name__ == "__main__":
	parser = optparse.OptionParser()
	parser.add_option("--statefull", help='Mode state full (se met a jour en continue)', dest='statefull',default=False, action='store_true')
	parser.add_option("--allstations", help='Affichage des horaires de passage pour chaque station', dest='allstations',default=False, action='store_true')
	parser.add_option("--station", help='Prochain passage pour une station', dest='stationCode')
	(opts,args) = parser.parse_args()
	if(opts.stationCode):
		printJustStation(opts.stationCode)
		sys.exit(0)
	if opts.statefull:
		stateFullMode(opts.allstations)
	else:
		stateLessMode(opts.allstations)
	sys.exit(0)


