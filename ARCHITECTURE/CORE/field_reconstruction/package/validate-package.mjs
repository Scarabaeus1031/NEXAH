import fs from "node:fs";
import path from "node:path";
import vm from "node:vm";
import { fileURLToPath } from "node:url";

const packageDir = path.dirname(fileURLToPath(import.meta.url));
const root = path.dirname(packageDir);
const failures = [];
const requiredFiles = [
  "NEXAH_FIELD_RECONSTRUCTION_PACKAGE.html",
  "NEXAH_FIELD_RECONSTRUCTION_DEMONSTRATOR.html",
  "NEXAH_FIELD_VISUAL_BENCH.html",
  "package/field-reconstruction-package.css",
  "demonstrator/field-reconstruction-demonstrator.js",
  "demonstrator/field-reconstruction-demonstrator.css",
  "bench/field-visual-bench.js",
  "bench/field-visual-bench.css",
  "bench/field-visual-bench-final.css",
  "bench/FIELD_VISUAL_BENCH_RECEIPT_2026-10-26.json",
  "package/PACKAGE_MANIFEST_2026-10-26.json",
  "FIELD_RECONSTRUCTION_PACKAGE_CLOSEOUT_2026-10-26.md"
];

for (const file of requiredFiles) {
  if (!fs.existsSync(path.join(root, file))) failures.push(`missing ${file}`);
}

const context = { window: {} };
vm.createContext(context);
vm.runInContext(fs.readFileSync(path.join(root, "bench/field-visual-bench-data.js"), "utf8"), context);
const assets = context.window.NEXAH_FIELD_BENCH_ASSETS;
const receipt = JSON.parse(fs.readFileSync(path.join(root, "bench/FIELD_VISUAL_BENCH_RECEIPT_2026-10-26.json"), "utf8"));
const manifest = JSON.parse(fs.readFileSync(path.join(packageDir, "PACKAGE_MANIFEST_2026-10-26.json"), "utf8"));

if (assets.length !== 61) failures.push(`catalog count ${assets.length} != 61`);
if (receipt.assetCount !== assets.length) failures.push(`receipt count ${receipt.assetCount} != catalog count ${assets.length}`);
if (manifest.counts.visualFrames !== assets.length) failures.push("manifest visual-frame count mismatch");
if (receipt.assets.some((asset) => !asset.imageSha256 || !asset.producerSha256)) failures.push("receipt has unhashed bindings");

for (const entrypoint of Object.values(manifest.entrypoints)) {
  if (!fs.existsSync(path.join(root, entrypoint))) failures.push(`broken entrypoint ${entrypoint}`);
}

const home = fs.readFileSync(path.join(root, manifest.entrypoints.home), "utf8");
const pipeline = fs.readFileSync(path.join(root, manifest.entrypoints.pipeline), "utf8");
const bench = fs.readFileSync(path.join(root, manifest.entrypoints.visualBench), "utf8");
for (const phrase of ["NEXAH CORE · BUILDER PATH", "SYSTEMS DESK", "WIRING RETURN", "61-FRAME BENCH", "PACKAGE COMPLETE · VERIFY EXISTING · STOP"]) {
  if (!home.includes(phrase)) failures.push(`home missing ${phrase}`);
}
if (!pipeline.includes("PACKAGE HOME")) failures.push("pipeline missing package link");
if (!bench.includes("PACKAGE HOME")) failures.push("bench missing package link");

if (failures.length) {
  console.error(`FAIL:\n- ${failures.join("\n- ")}`);
  process.exit(1);
}
console.log(`PASS: ${requiredFiles.length} package artifacts, ${assets.length} frames, ${assets.length * 2} hashes, all entrypoints linked`);
