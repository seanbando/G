// All stills, keyed by script line id (S001 ...). Split across files to keep them readable.
module.exports = Object.assign({}, ...["a", "b", "c", "d"].map((k) => { try { return require("./scenes-" + k + ".js").S; } catch (e) { if (e.code !== "MODULE_NOT_FOUND") throw e; return {}; } }));
