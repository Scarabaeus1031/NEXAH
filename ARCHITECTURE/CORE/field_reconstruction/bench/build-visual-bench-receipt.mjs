import crypto from "node:crypto";
import fs from "node:fs";
import path from "node:path";
import vm from "node:vm";
import { fileURLToPath } from "node:url";

const benchDir = path.dirname(fileURLToPath(import.meta.url));
const root = path.dirname(benchDir);
const context = { window: {} };
vm.createContext(context);
vm.runInContext(fs.readFileSync(path.join(benchDir, "field-visual-bench-data.js"), "utf8"), context);
const hash = (file) => crypto.createHash("sha256").update(fs.readFileSync(file)).digest("hex");
const assets = context.window.NEXAH_FIELD_BENCH_ASSETS.map((asset) => ({
  ...asset,
  imageSha256: hash(path.resolve(root, asset.image)),
  producerSha256: hash(path.resolve(root, asset.producer))
}));
const receipt = {
  instrument: "NEXAH_FIELD_VISUAL_BENCH",
  identity: "ARCHITECTURE/CORE/field_reconstruction",
  generatedOn: "2026-10-26",
  authority: "Source-bound display lens. Original assets and producers retain content and evidence authority.",
  graphEffect: "No new Source Graph identity, relation, Study, Family or canonical count.",
  claimBoundary: "Owner mnemonic tags are navigation vocabulary, not computed variables or evidence of one mechanism.",
  assetCount: assets.length,
  assets
};
fs.writeFileSync(path.join(benchDir, "FIELD_VISUAL_BENCH_RECEIPT_2026-10-26.json"), `${JSON.stringify(receipt, null, 2)}\n`);
console.log(`WROTE: ${assets.length} hashed source bindings`);
