db.accidents.aggregate([
    {$match: {"col": 1}},
    {$unwind: "$vehicles"},
    {$match: {  $and: [{"vehicles.catv": 7},{"vehicles.users.1":{$exists: true}}, {"vehicles.users.2":{$exists: false}},
                            {"vehicles.users.0.place":1}, {"vehicles.users.1.place":2}]}},
    {$project: { u1: {$arrayElemAt: [ "$vehicles.users", 0 ]}, u2: {$arrayElemAt: [ "$vehicles.users", 1 ]}
    }},
    {$project: {driverDied: {$eq: ["$u1.grav", 2]}, passengerDied: {$eq: ["$u2.grav", 2]}}},
    {$group: {_id: {driverDied: "$driverDied", passengerDied: "$passengerDied"}, count: {$sum: 1}}}
    ])
    