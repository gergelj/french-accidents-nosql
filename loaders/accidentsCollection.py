from pymongo import MongoClient
from characteristicsLoader import loadCharacteristics
from usersLoader import loadUsers
from vehiclesByAccidentLoader import loadVehicles
from usersLoader import getUserKey


client = MongoClient(host="localhost", port=27017)
db = client.accidents
accidents = db.accidents

accidentsMap = loadCharacteristics()
vehiclesMap = loadVehicles()
usersMap = loadUsers()

for v_key, v_val in vehiclesMap.items():
	for veh in v_val:
		users = usersMap.get(getUserKey(veh["Num_Acc"], veh["num_veh"]))
		veh["users"] = users

for c_key, c_val in accidentsMap.items():
	vehicles = vehiclesMap.get(c_key)
	c_val["vehicles"] = vehicles
	
accidents.insert_many(accidentsMap.values())

client.close()
