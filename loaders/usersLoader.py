import os.path
import json
import pandas as pd

csvPath = "../dataset/users.csv"
jsonPath = "json/users.json"

def getUserKey(num_acc, num_veh):
	return str(num_acc) + "-" + num_veh


def getUser(userDf):
	user = {}
	user["Num_Acc"] = int(userDf["Num_Acc"])
	user["num_veh"] = userDf["num_veh"]
	if not pd.isna(userDf["place"]):
		user["place"] = int(userDf["place"])
	user["catu"] = int(userDf["catu"])
	user["grav"] = int(userDf["grav"])
	user["sexe"] = int(userDf["sexe"])
	if str(userDf["trajet"]) not in ["0", "0.0", "nan"]:
		user["trajet"] = int(userDf["trajet"])
	
	if not pd.isna(userDf["secu"]):
		secu = str(int(userDf["secu"]))
		if len(secu) == 2:
			user["sec"] = secu[0]
			if secu[1] == '1':
				user["secutil"] = True
			elif secu[1] == '2':
				user["secutil"] = False
	
	if not pd.isna(userDf["an_nais"]):
		user["an_nais"] = int(userDf["an_nais"])
	if str(userDf["locp"]) not in ["0", "0.0", "nan"]:
		user["locp"] = int(userDf["locp"])
	if not pd.isna(userDf["actp"]):
		user["actp"] = int(userDf["actp"])
	if str(userDf["etatp"]) not in ["0", "0.0", "nan"]:
		user["etatp"] = int(userDf["etatp"])
	
	return user


def loadUsers():
	usersMap = {}
	print("Started loading users")
	if os.path.isfile(jsonPath):
		with open(jsonPath) as infile:
			usersMap = json.load(infile)
			print("Users loaded from file")
	else:
		usersData = pd.read_csv(csvPath)
		for _, rowUser in usersData.iterrows():
			if usersMap.get(getUserKey(rowUser["Num_Acc"], rowUser["num_veh"])) is None:
				usersMap[getUserKey(rowUser["Num_Acc"], rowUser["num_veh"])] = [getUser(rowUser)]
			else:
				usersMap[getUserKey(rowUser["Num_Acc"], rowUser["num_veh"])].append(getUser(rowUser))
		with open(jsonPath, 'w') as outfile:
			json.dump(usersMap, outfile)	
		print("Users loaded in memory and saved to file")

	return usersMap
	
loadUsers()
