import pandas as pd
import os.path
import json

csvPath = "../dataset/vehicles.csv"
jsonPath = "json/vehiclesByAccident.json"

def getVehicle(vehicleDf):
	vehicle = {}
	vehicle["Num_Acc"] = int(vehicleDf["Num_Acc"])
	vehicle["num_veh"] = vehicleDf["num_veh"]
	if not pd.isna(vehicleDf["senc"]):
		vehicle["senc"] = int(vehicleDf["senc"])
	if not pd.isna(vehicleDf["catv"]):
		vehicle["catv"] = int(vehicleDf["catv"])
	if not pd.isna(vehicleDf["occutc"]):
		vehicle["occutc"] = int(vehicleDf["occutc"])
	if str(vehicleDf["choc"]) not in ["0", "0.0", "nan"]:
		vehicle["choc"] = int(vehicleDf["choc"])
	if str(vehicleDf["manv"]) not in ["0", "0.0", "nan"]:
		vehicle["manv"] = int(vehicleDf["manv"])
		
	obstacle = {}
	if str(vehicleDf["obs"]) not in ["0", "0.0", "nan"]:
		obstacle["obs"] = int(vehicleDf["obs"])
	if str(vehicleDf["obsm"]) not in ["0", "0.0", "nan"]:
		obstacle["obsm"] = int(vehicleDf["obsm"])
	
	if obstacle:
		vehicle["obstacle"] = obstacle
			
	return vehicle


def loadVehicles():
	vehiclesMap = {}
	print("Started loading vehicles")
	if os.path.isfile(jsonPath):
		with open(jsonPath) as infile:
			vehiclesMap = json.load(infile)
			print("Vehicles loaded from file")
	else:
		vehiclesData = pd.read_csv(csvPath)
		for _, rowVehicle in vehiclesData.iterrows():
			if vehiclesMap.get(rowVehicle["Num_Acc"]) is None:
				vehiclesMap[rowVehicle["Num_Acc"]] = [getVehicle(rowVehicle)]
			else:
				vehiclesMap[rowVehicle["Num_Acc"]].append(getVehicle(rowVehicle))
		with open(jsonPath, 'w') as outfile:
			json.dump(vehiclesMap, outfile)	
		print("Vehicles loaded in memory and saved to file")

	return vehiclesMap
