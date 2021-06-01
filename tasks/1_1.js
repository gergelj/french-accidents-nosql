db.accidents.aggregate([
    {$match: {int: {$in: [2, 3, 4, 5, 6]}, "road.condition.surf": {$exists: true}}} //kružni tokovi i raskrsnice
    ,{$unwind: "$vehicles"}
    ,{$unwind: "$vehicles.users"}
    ,{$group: {_id: {int: "$int", surf: "$road.condition.surf", grav: "$vehicles.users.grav"}, casualtyNum: {$sum: 1}}}
    ,{$group: 
        {
            _id: {int: "$_id.int", surf: "$_id.surf"}, 
            totalCasualties: {$sum: "$casualtyNum"}, 
            severeCasualties: {$sum: {$cond: [{ $in: ["$_id.grav", [2, 3]]}, "$casualtyNum", 0]}}
        }
     }
     ,{$group: 
        {
            _id: {surf: "$_id.surf"}, 
            totalCrossroadCasualties: {$sum: {$cond: [{$in: ["$_id.int", [2, 3, 4, 5]]}, "$totalCasualties", 0]}},
            severeCrossroadCasualties: {$sum: {$cond: [{$in: ["$_id.int", [2, 3, 4, 5]]}, "$severeCasualties", 0]}},
            totalRoundaboutCasualties: {$sum: {$cond: [{$eq: ["$_id.int", 6]}, "$totalCasualties", 0]}},
            severeRoundaboutCasualties: {$sum: {$cond: [{$eq: ["$_id.int", 6]}, "$severeCasualties", 0]}},
        }
     }
     ,{$bucket: {
         groupBy: "$_id.surf",
         boundaries: [1, 2, 10],    //normal road surface conditions = {1}, not normal surface conditions = [2-9]
         output: {
             totalCrossroadCasualties: {$sum: "$totalCrossroadCasualties"},
             severeCrossroadCasualties: {$sum: "$severeCrossroadCasualties"},
             totalRoundaboutCasualties: {$sum: "$totalRoundaboutCasualties"},
             severeRoundaboutCasualties: {$sum: "$severeRoundaboutCasualties"}
         }
     }}
     ,{$addFields:{
         condition: {$cond: [{$eq: ["$_id", 1]}, "normal", "not normal"]},
         severeCrossroadRatio: {$divide: [{$sum: "$severeCrossroadCasualties"}, {$sum: "$totalCrossroadCasualties"}]},
         severeRoundaboutRatio: {$divide: [{$sum: "$severeRoundaboutCasualties"}, {$sum: "$totalRoundaboutCasualties"}]}
     }}
])