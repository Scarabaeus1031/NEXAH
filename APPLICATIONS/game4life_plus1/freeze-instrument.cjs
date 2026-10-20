const fs = require("node:fs");
const path = require("node:path");
const crypto = require("node:crypto");
const cp = require("node:child_process");

const root = __dirname;
const freezeId = "G4L1-POST-CLOSE-INSTRUMENT-FREEZE-2026-10-12";
const jsonName = "FREEZE_MANIFEST_2026-10-12.json";
const checksumName = "FREEZE_SHA256_2026-10-12.txt";
const excluded = new Set([jsonName, checksumName, ".DS_Store"]);

function run(label, command, args) {
  const result = cp.spawnSync(command, args, {
    cwd: root,
    encoding: "utf8",
    maxBuffer: 16 * 1024 * 1024
  });
  const combined = `${result.stdout || ""}\n${result.stderr || ""}`.trim();
  if (result.status !== 0) {
    process.stderr.write(`${combined}\n`);
    throw new Error(`${label} failed with exit code ${result.status}`);
  }
  const summaries = combined
    .split(/\r?\n/)
    .map(line => line.trim())
    .filter(line => /^PASS(?:\s|$)/.test(line));
  return { label, status: "PASS", summaries };
}

function walk(directory) {
  return fs.readdirSync(directory, { withFileTypes: true })
    .sort((a, b) => a.name.localeCompare(b.name))
    .flatMap(entry => {
      if (entry.name === "node_modules" || excluded.has(entry.name)) return [];
      const absolute = path.join(directory, entry.name);
      return entry.isDirectory() ? walk(absolute) : [absolute];
    });
}

function sha256(file) {
  return crypto.createHash("sha256").update(fs.readFileSync(file)).digest("hex");
}

const verification = [
  run("full component suite", "npm", ["test", "--silent"]),
  run("UI smoke suite", "npm", ["run", "test:ui", "--silent"]),
  run("package audit", "npm", ["run", "audit", "--silent"])
];

const files = walk(root).map(file => ({
  path: `./${path.relative(root, file).split(path.sep).join("/")}`,
  sha256: sha256(file),
  bytes: fs.statSync(file).size
}));

const manifest = {
  schema: "nexah.game4life.post-close-freeze.v1",
  freeze_id: freezeId,
  date: "2026-10-12",
  status: "PASS_FROZEN_INTERNAL_INSTRUMENT_SNAPSHOT",
  custody: "10 NEXAH CORE/NEXAH/APPLICATIONS/game4life_plus1",
  scientific_authority: "UNCHANGED_CLOSED_LIFE08_STUDY",
  identity_effect: "REUSE_ONLY_NO_NEW_NAVIGATOR_NODE_OR_RELATION",
  canonical_count_effect: "NONE",
  active_research_cycle: "NONE",
  publication_authorized: false,
  verification,
  open_register: [
    "G4L1-O01_VISUAL_ACCESSIBILITY_REVIEW",
    "G4L1-O02_INDEPENDENT_IMPLEMENTATION_OR_REPLICATION",
    "G4L1-O03_NEW_FIXTURES_OR_BOUNDARY_REQUIRE_NEW_PREREGISTRATION",
    "G4L1-O04_TYPED_TRANSPORT_AND_SOURCE_BINDINGS_REMAIN_OPEN",
    "G4L1-O05_NO_FOURTH_DOMAIN_OR_SHARED_MECHANISM_CLAIM",
    "G4L1-O06_REPOSITORY_VERSIONING_REQUIRES_EXPLICIT_DECISION",
    "G4L1-O07_WORK_PROVENANCE_CLEANUP_REQUIRES_CUSTODY_DECISION"
  ],
  file_count: files.length,
  files
};

fs.writeFileSync(path.join(root, jsonName), `${JSON.stringify(manifest, null, 2)}\n`);
fs.writeFileSync(
  path.join(root, checksumName),
  `${files.map(file => `${file.sha256}  ${file.path}`).join("\n")}\n`
);

console.log(`PASS ${freezeId} ${files.length} files`);
