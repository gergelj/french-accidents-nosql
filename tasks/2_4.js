db.users.aggregate([
    {$match: {"catu": {$in: [3,4]}, "accident.agg": 2, "vehicle.manv": {$in: [1,2,13,14,17,18]}}},
    {$bucket: {
        groupBy: "$vehicle.manv",
        boundaries: [1,3,15,19],
        output: {
                totalAccidents: {$sum: 1},
                fatal: {$sum: {$cond: [{ $eq: ["$grav", 2]}, 1, 0]}},
                injured: {$sum: {$cond: [{ $eq: ["$grav", 3]}, 1, 0]}},
            }
    }}
    ])