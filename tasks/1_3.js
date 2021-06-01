db.accidents.aggregate([
    {$unwind: "$vehicles"}
    ,{$match: {"vehicles.obstacle.obsm": {$in: [5, 6]}}}
    ,{$project: {year: {$year: "$date"}, _id: 0, lum: "$condition.lum"}}
    ,{$group: {_id: {year: "$year"}, totalDay: {$sum: {$cond: [{$in: ["$lum", [1, 2]]}, 1, 0]}}, totalNight: {$sum: {$cond: [{$in: ["$lum", [3, 4, 5]]}, 1, 0]}}, total: {$sum: 1}}}
    ,{$project: {_id: 0, year: "$_id.year", totalDay: 1, totalNight: 1, total: 1}}
    ,{$sort: {year: 1}}
])