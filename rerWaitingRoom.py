#!/usr/bin/python
# TODO
#  -- Parrallelise la recherche sur internet ;
#  -- rendu graphique plan de ligne format texte ; 
#  -- algorithme de numerotation de l'ordre de passage de chaque train a Paris Nord

import urllib.request
import re
import sys


missions_data = {
		"A":"Gare du Nord",
		"C":"Cité universitaire (exceptionnel)",
		"E":"Aéroport Charles-de-Gaulle 2 TGV",
		"G":"Aulnay-sous-Bois",
		"H":"Bourg-la-Reine (exceptionnel)",
		"I":"Mitry - Claye",
		"J":"Denfert-Rochereau",
		"K":"Massy - Palaiseau",
		"L":"Orsay - Ville",
		"M":"Châtelet - Les Halles (exceptionnel)",
		"N":"La Croix de Berny (exceptionnel)",
		"O":"Aéroport Charles-de-Gaulle 1 (exceptionnel)",
		"P":"Saint-Rémy-lès-Chevreuse",
		"Q":"La Plaine - Stade de France",
		"S":"Robinson",
		"U":"Laplace",
		}

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

gares_data = [
		"Aéroport Charles-de-Gaulle 2 TGV",
		"Aéroport Charles-de-Gaulle 1"    ,
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
garesOrder_data = {
        	"Aéroport Charles-de-Gaulle 2 TGV": (2,4),
		"Aéroport Charles-de-Gaulle 1"    : (2,3),
		"Parc des Expositions"            : (2,2),
		"Villepinte"                      : (2,1),
		"Sevran - Beaudottes"             : (2,0),
		"Mitry - Claye"                   : (1,3),
		"Villeparisis - Mitry-le-Neuf"    : (1,2),
		"Vert-Galant"                     : (1,1),
		"Sevran - Livry"                  : (1,0),
		"Aulnay-sous-Bois"                : (0,6),
		"Le Blanc-Mesnil"                 : (0,5),
		"Drancy"                          : (0,4),
		"Le Bourget"                      : (0,3),
		"La Courneuve - Aubervilliers"    : (0,2),
		"La Plaine - Stade de France"     : (0,1),
		"Gare du Nord"                    : (0,0),
        }
requests_data = {
		"Aéroport Charles-de-Gaulle 2 TGV": "http://www.transilien.com/gare/pagegare/filterListeTrains?codeTR3A=RYR&destination=PARIS+NORD&ligne=&nomGare=AEROPORT+CHARLES+DE+GAULLE+2+TGV+-+Roissy&x=28&y=10",
		"Aéroport Charles-de-Gaulle 1"    : "http://www.transilien.com/gare/pagegare/filterListeTrains?codeTR3A=RSY&destination=PARIS+NORD&ligne=&nomGare=AEROPORT+CHARLES+DE+GAULLE++1+-+Roissy&x=45&y=12",
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


# return 1 sur gare 1 avant gare 2, -1 si gare 2 avant gare 1, 0 si incomparable.
def getGareOrder(gare1,gare2):
        positionGare1 = garesOrder_data[gare1]
        positionGare2 = garesOrder_data[gare2]
        # meme sous branche
        if positionGare1[0] == positionGare2[0]:
                return 1 if positionGare1[1] >= positionGare2[1] else -1
        else:
                if positionGare1[0] != 0 and positionGare2[0] != 0:
                        # Les branches sont incomparables
                        return 0
                else:
                        return 1 if positionGare1[0] >= positionGare2[0] else -1


def getTrainFrom(request):
	success = False
	nbTry = 100
	for i in range(0,nbTry):
		try:
			page = urllib.request.urlopen(request)
			success = True
		except:
			continue
		break
	if not success:
		print("Echec apres %d tentatives" % nbTry)
		return []
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
	
passageGare = {}
for gare in gares_data:
	passageGare[gare] = getTrainFrom(requests_data[gare])

for gare in gares_data:
        print(gare)
        print(passageGare[gare])

missions = {}
for gare in reversed(gares_data):
        for mission in passageGare[gare]:
                missions[mission[0]] = gare

nextTrainsToStation = {}
for mission in missions.keys():
        if not missions[mission] in nextTrainsToStation:
                nextTrainsToStation[missions[mission]] = []
        nextTrainsToStation[missions[mission]].append(mission)

for gare in gares_data:        
        if gare in nextTrainsToStation:
                print(nextTrainsToStation[gare])
        print(gare)

waitingQueue = {}
pos = 0
waitingQueue[passageGare[-1][0]] = 0
print(waitingQueue)

sys.exit(0)


# Request (pour l'instant les requetes vont toujour vers le sud)
request_CDG1 = "http://www.transilien.com/gare/pagegare/filterListeTrains?codeTR3A=RSY&destination=PARIS+NORD&ligne=&nomGare=AEROPORT+CHARLES+DE+GAULLE++1+-+Roissy&x=41&y=11"
request_Aulnay = "http://www.transilien.com/gare/pagegare/filterListeTrains?codeTR3A=AB&destination=PARIS+NORD&ligne=&nomGare=AULNAY+SOUS+BOIS&x=44&y=11" 
request_ParisNord = "http://www.transilien.com/gare/pagegare/filterListeTrains?codeTR3A=GDS&destination=SAINT-MICHEL+NOTRE+DAME&ligne=&nomGare=PARIS+NORD+%28GARE+DU+NORD%29&x=39&y=14"
#request_CDG1 = "http://www.transilien.com/gare/AEROPORT-CHARLES-DE-GAULLE-1-Roissy-8727146"
#request_Aulnay = "http://www.transilien.com/gare/AULNAY-SOUS-BOIS-8727141" 
#request_ParisNord = "http://www.transilien.com/gare/pagegare/filterListeTrains?codeTR3A=GDS&destination=&ligne=RER+B&nomGare=PARIS+NORD+%28GARE+DU+NORD%29&x=35&y=6" 

trainARoissy = getTrainFrom(request_CDG1)
#trainAAulnay = getTrainFrom(request_Aulnay)
trainAParis = getTrainFrom(request_ParisNord)

print(trainARoissy)
print(trainAParis)

myTrain = trainARoissy[0][0]

pos = 0
sol = ""
for train in trainAParis:
	if train[0] == myTrain:
		sol = "Il y a %d train avant le votre" % pos
		break
	pos = pos + 1

if len(sol):
	print(sol)
else:
	print("Pas de solution trouve!")
