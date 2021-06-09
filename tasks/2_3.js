db.accidents.aggregate([
    {$match: {"agg": 1,"condition.lum": {$in: [3, 4, 5]}}},
    {$unwind: "$vehicles"},
    {$match: {"vehicles.catv": 7, "vehicles.users":{$ne:null}}},
    { $group: { _id: { number:{$gt: [{$size: "$vehicles.users"}, 1]}, lum: {$gt: ["$condition.lum", 4]}}, count: { $sum: 1 } } },
    {$project: {passengerNumber: "$_id.number", lightingCondition: "$_id.lum", accidentCount: "$count"}}
    ])
  