db.users.aggregate([
    {$match: {"place": {$in: [1, 2]}, "vehicle.catv": {$in: [5, 7]}}},
    {$group: {_id: {vehicleCategory: "$vehicle.catv", victimPlace: "$place"},
        severeInjuries: {$sum: {$cond: [{$in: ["$grav",[2,3]]}, 1, 0]}},        
        totalinjuries: {$sum: 1},
    }},
    {$project: {severeInjuryRatio: {$divide: ["$totalinjuries", "$severeInjuries"]}}}
    ])