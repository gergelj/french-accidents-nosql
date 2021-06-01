db.users.aggregate([
    {$match: {"catu": 1, "an_nais": {$exists: true}, "vehicle.obstacle": {$exists: true}}} //vozaci
    ,{$project: {"obsm": {$cond: [{$in: ["$vehicle.obstacle.obsm", [1,2,4,5,6,9]]}, "$vehicle.obstacle.obsm", {$multiply: ["$vehicle.obstacle.obs", 10]}]}, "age": {$subtract: [{$year: "$accident.date"}, "$an_nais"]}, _id: 0}}
    ,{$group: {_id: {age: "$age", obsm: "$obsm"}, cnt: {$sum: 1}}}
    ,{$group: {_id: {age: "$_id.age"}, totalAccidents: {$sum: "$cnt"}, pedestrianAccidents: {$sum: {$cond: [{$eq: ["$_id.obsm", 1]}, "$cnt", 0]}}}}
    ,{$project: {_id: 0, age: "$_id.age", pedestrianRatio: {$divide: ["$pedestrianAccidents", "$totalAccidents"]}}}
    ,{$sort: {age: 1}}
    ,{$match: {"age": {$gt: 15}}}
])
