const fs = require("node:fs");
const crypto = require("node:crypto");
const path = require("node:path");
const file = path.join(__dirname, "PREREGISTRATION.json");
const sha256 = crypto.createHash("sha256").update(fs.readFileSync(file)).digest("hex");
const lock = { id: "LIFE08-PROTOCOL-LOCK", status: "FROZEN_BEFORE_EXECUTION", file: "PREREGISTRATION.json", sha256, date: "2026-10-11" };
fs.writeFileSync(path.join(__dirname, "PREREGISTRATION_LOCK.json"), JSON.stringify(lock, null, 2) + "\n");
console.log(sha256);
