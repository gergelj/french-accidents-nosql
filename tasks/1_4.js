db.users.aggregate([
    {$match: {secutil: {$exists: true}}}
    ,{$project: {_id: 0, Num_Acc: 1, grav: 1, secutil: 1}}
    ,{$group: {_id: {secutil: "$secutil", accident: "$Num_Acc"}, severities: {$sum: {$cond: [{$in: ["$grav", [2, 3]]}, 1, 0]}}}}
    ,{$group: {_id: {secutil: "$_id.secutil"}, totalSeverities: {$sum: "$severities"}, totalAccidents: {$sum: 1}}}
    ,{$project: {_id: 0, secutil: "$_id.secutil", totalSeverities: 1, totalAccidents: 1}}
    ,{$addFields: {averageSeverities: {$divide: ["$totalSeverities", "$totalAccidents"]}}}
], {allowDiskUse: true})