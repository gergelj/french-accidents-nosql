from pymongo import MongoClient
from characteristicsLoader import loadCharacteristics
from usersLoader import loadUsers
from vehiclesLoader import loadVehicles
from vehiclesLoader import getVehicleKey


client = MongoClient(host="localhost", port=27017)
db = client.accidents
users = db.users

accidentsMap = loadCharacteristics()
vehiclesMap = loadVehicles()
usersMap = loadUsers()

usersListList = list(usersMap.values())
usersList = [item for uss in usersListList for item in uss]

for usr in usersList:
    vehicle = vehiclesMap.get(getVehicleKey(usr["Num_Acc"], usr["num_veh"]))
    if vehicle is not None:
        usr["vehicle"] = vehicle

    accident = accidentsMap.get(str(usr["Num_Acc"]))
    if accident is not None:
        usr["accident"] = accident
	
users.insert_many(usersList)

client.close()
