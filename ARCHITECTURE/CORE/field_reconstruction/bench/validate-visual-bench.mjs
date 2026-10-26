import fs from "node:fs";
import path from "node:path";
import vm from "node:vm";
import { fileURLToPath } from "node:url";

const benchDir = path.dirname(fileURLToPath(import.meta.url));
const root = path.dirname(benchDir);
const source = fs.readFileSync(path.join(benchDir, "field-visual-bench-data.js"), "utf8");
const context = { window: {} };
vm.createContext(context);
vm.runInContext(source, context);
const assets = context.window.NEXAH_FIELD_BENCH_ASSETS;
const failures = [];
const ids = new Set();
const required = ["id", "family", "version", "title", "image", "producer", "class", "reading", "boundary", "relation", "motifs"];
for (const asset of assets) {
  for (const key of required) if (!(key in asset) || asset[key] === "") failures.push(`${asset.id}: missing ${key}`);
  if (ids.has(asset.id)) failures.push(`duplicate id: ${asset.id}`);
  ids.add(asset.id);
  for (const key of ["image", "producer"]) {
    const target = path.resolve(root, asset[key]);
    if (!fs.existsSync(target)) failures.push(`${asset.id}: missing ${key} ${asset[key]}`);
  }
}
const html = fs.readFileSync(path.join(root, "NEXAH_FIELD_VISUAL_BENCH.html"), "utf8");
if (!html.includes("OWNER MNEMONICS ≠ COMPUTED FEATURES")) failures.push("missing mnemonic boundary");
if (failures.length) {
  console.error(`FAIL:\n- ${failures.join("\n- ")}`);
  process.exit(1);
}
console.log(`PASS: ${assets.length} source-bound frames, ${ids.size} unique IDs, all assets/producers present`);
