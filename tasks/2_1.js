db.users.aggregate([
        {$match: {"vehicle.obstacle.obsm": {$in: [5, 6]}}},
        {$group: {_id: {obstacle: "$vehicle.obstacle.obsm"}, 
         uninjured: {$sum: {$cond: [{ $eq: ["$grav", 1]}, 1, 0]}},
         fatal: {$sum: {$cond: [{ $eq: ["$grav", 2]}, 1, 0]}},
         injured: {$sum: {$cond: [{ $eq: ["$grav", 3]}, 1, 0]}},
         minorinjury: {$sum: {$cond: [{ $eq: ["$grav", 4]}, 1, 0]}},
         totalinjured: {$sum: 1}
         }}
    ])