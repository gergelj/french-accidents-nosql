db.users.aggregate([
    {$group: {_id:{accident: "$Num_Acc", holiday: "$accident.holiday"}, severities: {$sum: {$cond: [{$in: ["$grav", [2, 3]]}, 1, 0]}}}}
    ,{$group: {_id: {$gt: ["$_id.holiday", null]}, totalAccidents: {$sum: 1}, severeAccidents: {$sum: {$cond: [{$gt: ["$severities", 0]}, 1, 0]}}}}
    ,{$project: {_id: 0, holiday: "$_id", totalAccidents: 1, severeAccidents: 1}}
    ,{$addFields: {avgSevereAccidents: {$divide: ["$severeAccidents", "$totalAccidents"]}}}
], {allowDiskUse: true})
