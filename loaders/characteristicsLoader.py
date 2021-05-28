import threading
import pandas as pd
import os.path
import json
from json import JSONDecoder
from json import JSONEncoder
from datetime import datetime
import dateutil.parser

characteristicsData = None
inseePostCodeData = None
holidaysData = None
placesData = None

characteristicsMap = {}
holidaysMap = {}
placesMap = {}
inseeMap = {}

class DateTimeDecoder(JSONDecoder):

    def __init__(self, *args, **kargs):
        JSONDecoder.__init__(self, object_hook=self.dict_to_object,
                             *args, **kargs)
    
    def dict_to_object(self, d): 
        if '__type__' not in d:
            return d

        type = d.pop('__type__')
        try:
            dateobj = datetime(**d)
            return dateobj
        except:
            d['__type__'] = type
            return d


class DateTimeEncoder(JSONEncoder):
    """ Instead of letting the default encoder convert datetime to string,
        convert datetime objects into a dict, which can be decoded by the
        DateTimeDecoder
    """
        
    def default(self, obj):
        if isinstance(obj, datetime):
            return {
                '__type__' : 'datetime',
                'year' : obj.year,
                'month' : obj.month,
                'day' : obj.day,
                'hour' : obj.hour,
                'minute' : obj.minute,
                'second' : obj.second,
                'microsecond' : obj.microsecond,
            }   
        else:
            return JSONEncoder.default(self, obj)


def getInsee(inseeDf):
	insee = {}
	insee["insee"] = inseeDf["INSEE_COM"]
	insee["com"] = inseeDf["NOM_COM"]
	insee["dep"] = inseeDf["NOM_DEPT"]
	insee["population"] = int(inseeDf["POPULATION"])
	latlong = inseeDf["Geo Point"].split(',')
	insee["lat"] = float(latlong[0])
	insee["long"] = float(latlong[1])
		
	return insee


def getInseeCode(dep, com):
	if com == 'nan' or dep == 'nan':
		return None
	
	if dep == '201':
		insee_dep = '2A'
	elif dep == '202':
		insee_dep = '2B'
	elif dep in ['971', '972', '973', '974', '975', '976']:
		insee_dep = '97'
	else:
		insee_dep = dep[:-1].zfill(2)
	
	insee_com = com.zfill(3)
	return insee_dep + insee_com


def getPlace(placeDf):
	place = {}
	# place["Num_Acc"] = int(placeDf["Num_Acc"])
	if not pd.isna(placeDf["catr"]):
		place["catr"] = int(placeDf["catr"])
	if not pd.isna(placeDf["voie"]):
		place["voie"] = placeDf["voie"]
	#if not pd.isna(placeDf["v1"]):
	#	place["v1"] = int(placeDf["v1"])
	if str(placeDf["circ"]) not in ["0", "0.0", "nan"]:
		place["circ"] = int(placeDf["circ"])
	if not pd.isna(placeDf["nbv"]):
		place["nbv"] = int(placeDf["nbv"])
	#if not pd.isna(placeDf["pr"]):
	#	place["pr"] = float(placeDf["pr"])
	#if not pd.isna(placeDf["pr1"]):
	#	place["pr1"] = int(placeDf["pr1"])
	#if str(placeDf["vosp"]) not in ["0", "0.0", "nan"]:
	#	place["vosp"] = int(placeDf["vosp"])
	#if not pd.isna(placeDf["lartpc"]):
	#	place["lartpc"] = int(placeDf["lartpc"])
	#if not pd.isna(placeDf["larrout"]):
	#	place["larrout"] = int(placeDf["larrout"])
	if str(placeDf["infra"]) not in ["0", "0.0", "nan"]:
		place["infra"] = int(placeDf["infra"])
	if str(placeDf["situ"]) not in ["0", "0.0", "nan"]:
		place["situ"] = int(placeDf["situ"])
	#if not pd.isna(placeDf["env1"]):
	#	place["env1"] = int(placeDf["env1"])
	
	condition = {}
	if str(placeDf["prof"]) not in ["0", "0.0", "nan"]:
		condition["prof"] = int(placeDf["prof"])
	if str(placeDf["plan"]) not in ["0", "0.0", "nan"]:
		condition["plan"] = int(placeDf["plan"])
	if str(placeDf["surf"]) not in ["0", "0.0", "nan"]:
		condition["surf"] = int(placeDf["surf"])
		
	if condition:
		place["condition"] = condition
	
	return place


def getCharacteristic(dataFrame):
	c = {}
	c["Num_Acc"] = int(dataFrame["Num_Acc"])
	hrmn = str(dataFrame["hrmn"]).zfill(4)
	years = "20" + str(dataFrame["an"]).zfill(2)
	hours = int(hrmn[0:-2])
	minutes = int(hrmn[-2:])
	date = datetime.strptime(years + '-' + str(dataFrame['mois']) + '-' + str(dataFrame["jour"]) + ' ' + str(hours) + ":" + str(minutes), '%Y-%m-%d %H:%M')
	c["date"] = date
	
	holiday = holidaysMap.get(date.strftime("%Y-%m-%d"))
	if holiday is not None:
		c["holiday"] = holiday
		
	if not pd.isna(dataFrame["col"]):
		c["col"] = int(dataFrame["col"])
	if str(dataFrame["int"]) not in ['0', '0.0']:
		c["int"] = int(dataFrame["int"])
		
	condition = {}
	condition["lum"] = int(dataFrame["lum"])
	if not pd.isna(dataFrame["atm"]):
		condition["atm"] = int(dataFrame["atm"])
	c["condition"] = condition
	
	# c["agg"] = int(dataFrame["agg"])
	# c["adr"] = str(dataFrame["adr"])
	
	location = None
	insee_code = getInseeCode(str(dataFrame["dep"]), str(dataFrame["com"]))
	if insee_code is not None:
		location = inseeMap.get(insee_code)
	#location = getLocation(str(int(dataFrame["dep"])), str(int(dataFrame["com"])))
	if location is None:
		location = {}
		
	if str(dataFrame["gps"]) not in ['0', '0.0', '']:
		location["gps"] = str(dataFrame["gps"])
	#if str(dataFrame["lat"]) not in ['0', '', '0.0', 'nan']:
	#	location["lat"] = float(dataFrame["lat"] / 100000)
	#if str(dataFrame["long"]) not in ['0', '0.0', '', 'nan']:
	#	location["long"] = float(dataFrame["long"] / 100000)

	if location:
		c["location"] = location

	road = placesMap.get(dataFrame["Num_Acc"])
	if road is not None:
		c["road"] = road
		
	#vehicles = vehiclesMap.get(dataFrame["Num_Acc"])
	#if vehicles is not None:
    #	c["vehicles"] = vehicles
	
	return c

def loadHolidays():
	global holidaysMap
	global holidaysData
	print("Started loading holidays")
	if os.path.isfile('holidays.json'):
		with open('holidays.json') as infile:
			holidaysMap = json.load(infile)
			print("Holidays loaded from file")
	else:
		holidaysData = pd.read_csv("../holidays.csv")
		for _, rowHoliday in holidaysData.iterrows():
			if holidaysMap.get(rowHoliday["ds"]) is None:
				holidaysMap[rowHoliday["ds"]] = rowHoliday["holiday"]
				
		with open('holidays.json', 'w') as outfile:
			json.dump(holidaysMap, outfile)	
		print("Holidays loaded in memory and saved to file")


def loadPlaces():
	global placesMap
	global placesData
	print("Started loading places")
	if os.path.isfile('places.json'):
		with open('places.json') as infile:
			placesMap = json.load(infile)
			print("Places loaded from file")
	else:
		placesData = pd.read_csv("../places.csv")
		for _, rowPlace in placesData.iterrows():
			if placesMap.get(rowPlace["Num_Acc"]) is None:
				placesMap[rowPlace["Num_Acc"]] = getPlace(rowPlace)
		with open('places.json', 'w') as outfile:
			json.dump(placesMap, outfile)	
		print("Places loaded in memory and saved to file")


def loadInsee():
	global inseeMap
	global inseePostCodeData
	print("Started loading insee")
	if os.path.isfile('insee.json'):
		with open('insee.json') as infile:
			inseeMap = json.load(infile)
			print("Insee loaded from file")
	else:
		inseePostCodeData = pd.read_csv("../code-postal-code-insee-2015.csv", sep=";")
		for _, rowInsee in inseePostCodeData.iterrows():
			if inseeMap.get(rowInsee["INSEE_COM"]) is None:
				inseeMap[rowInsee["INSEE_COM"]] = getInsee(rowInsee)
		with open('insee.json', 'w') as outfile:
			json.dump(inseeMap, outfile)
		print("Insee loaded in memory and saved to file")


def loadCharacteristics():
	global characteristicsMap
	global characteristicsData
	print("Started loading characteristics")
	if os.path.isfile('characteristics.json'):
		with open('characteristics.json') as infile:
			characteristicsMap = json.load(infile, cls=DateTimeDecoder)
			print("Characteristics loaded from file")
	else:
		characteristicsData = pd.read_csv("../characteristics.csv")
		holidaysT = threading.Thread(target=loadHolidays)
		inseeT = threading.Thread(target=loadInsee)
		placesT = threading.Thread(target=loadPlaces)
		holidaysT.start()
		placesT.start()
		inseeT.start()
		holidaysT.join()
		placesT.join()
		inseeT.join()
		for _, rowCharacteristic in characteristicsData.iterrows():
			if characteristicsMap.get(rowCharacteristic["Num_Acc"]) is None:
				characteristicsMap[rowCharacteristic["Num_Acc"]] = getCharacteristic(rowCharacteristic)
		with open('characteristics.json', 'w') as outfile:
			json.dump(characteristicsMap, outfile, cls=DateTimeEncoder)
		print("Characteristics loaded in memory and saved to file")


loadCharacteristics()
