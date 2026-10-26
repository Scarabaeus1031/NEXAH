import fs from "node:fs";
import path from "node:path";
import { execFileSync } from "node:child_process";
import { fileURLToPath } from "node:url";

const deck = path.dirname(fileURLToPath(import.meta.url));
const ecosystem = path.resolve(deck, "../../../..");
const missionControl = path.join(ecosystem, "00 EXECUTIVE", "NEXAH-Mission-Control");

const ignoredDirectories = new Set([".git", ".work", "node_modules", "__pycache__", ".venv", "tmp"]);
const ignoredFiles = new Set([".DS_Store"]);
const extensionGroups = {
  code: new Set([".html", ".htm", ".css", ".js", ".mjs", ".cjs", ".ts", ".tsx", ".jsx", ".py", ".rs", ".sh", ".zsh"]),
  documents: new Set([".md", ".txt", ".pdf", ".doc", ".docx", ".rtf", ".tex"]),
  data: new Set([".json", ".csv", ".tsv", ".yaml", ".yml", ".xml", ".toml"]),
  images: new Set([".png", ".jpg", ".jpeg", ".webp", ".gif", ".svg", ".tif", ".tiff"]),
  models3d: new Set([".glb", ".gltf", ".obj", ".fbx", ".stl", ".ply"]),
  media: new Set([".mp4", ".mov", ".webm", ".mp3", ".wav", ".m4a", ".aac"]),
};

const repositoryPaths = [
  "00 EXECUTIVE/NEXAH-Mission-Control",
  "10 NEXAH CORE/NEXAH",
  "20 ORION/NEXAH-ORION-V1-CERTIFIED-d34fbb2f",
  "20 ORION/NEXAH-ORION",
  "20 ORION/NEXAH-ORION/.workspace/repositories/NEXAH-framework-ci",
  "20 ORION/NEXAH-ORION/.workspace/repositories/nexah-experience",
  "30 SCIENCE LAB/NEXAH-Science-Lab",
  "40 EXPERIENCE PRODUCTION/NEXAH-Experience",
  "40 EXPERIENCE PRODUCTION/NEXAHEDRON",
  "70 SCARABAEUS1033 WORKBENCH/Scarabaeus-1033",
];

function parseCsv(source) {
  const rows = [];
  let row = [];
  let field = "";
  let quoted = false;
  for (let index = 0; index < source.length; index += 1) {
    const char = source[index];
    if (char === '"') {
      if (quoted && source[index + 1] === '"') {
        field += '"';
        index += 1;
      } else {
        quoted = !quoted;
      }
    } else if (char === "," && !quoted) {
      row.push(field);
      field = "";
    } else if ((char === "\n" || char === "\r") && !quoted) {
      if (char === "\r" && source[index + 1] === "\n") index += 1;
      row.push(field);
      if (row.some((value) => value !== "")) rows.push(row);
      row = [];
      field = "";
    } else {
      field += char;
    }
  }
  if (field || row.length) {
    row.push(field);
    rows.push(row);
  }
  const [headers = [], ...records] = rows;
  return records.map((values) => Object.fromEntries(headers.map((header, index) => [header, values[index] ?? ""])));
}

function readCsv(relativePath) {
  return parseCsv(fs.readFileSync(path.join(missionControl, relativePath), "utf8"));
}

function git(relativePath, args) {
  return execFileSync("git", ["-C", path.join(ecosystem, relativePath), ...args], { encoding: "utf8" }).trim();
}

function scanFiles() {
  const totals = { files: 0, bytes: 0, html: 0, models3d: 0 };
  const groups = Object.fromEntries([...Object.keys(extensionGroups), "other"].map((key) => [key, { files: 0, bytes: 0 }]));
  const topLevels = new Map();
  const stack = [ecosystem];
  while (stack.length) {
    const directory = stack.pop();
    for (const entry of fs.readdirSync(directory, { withFileTypes: true })) {
      if (entry.isDirectory() && ignoredDirectories.has(entry.name)) continue;
      const fullPath = path.join(directory, entry.name);
      if (entry.isDirectory()) {
        stack.push(fullPath);
        continue;
      }
      if (!entry.isFile() || ignoredFiles.has(entry.name)) continue;
      const bytes = fs.statSync(fullPath).size;
      const relative = path.relative(ecosystem, fullPath);
      const topLevel = relative.split(path.sep)[0] || "ROOT";
      const top = topLevels.get(topLevel) || { files: 0, bytes: 0 };
      top.files += 1;
      top.bytes += bytes;
      topLevels.set(topLevel, top);
      const extension = path.extname(entry.name).toLowerCase();
      const group = Object.entries(extensionGroups).find(([, extensions]) => extensions.has(extension))?.[0] || "other";
      totals.files += 1;
      totals.bytes += bytes;
      groups[group].files += 1;
      groups[group].bytes += bytes;
      if (extension === ".html" || extension === ".htm") totals.html += 1;
      if (extensionGroups.models3d.has(extension)) totals.models3d += 1;
    }
  }
  return {
    totals,
    groups,
    topLevels: [...topLevels.entries()]
      .map(([name, value]) => ({ name, ...value }))
      .sort((a, b) => b.bytes - a.bytes),
  };
}

const files = scanFiles();
const uniqueCommits = new Set();
const repositories = repositoryPaths.map((relativePath) => {
  const commitHashes = git(relativePath, ["rev-list", "--all"]).split("\n").filter(Boolean);
  commitHashes.forEach((hash) => uniqueCommits.add(hash));
  const dirtyEntries = git(relativePath, ["status", "--porcelain"]).split("\n").filter(Boolean).length;
  return {
    name: path.basename(relativePath),
    path: relativePath,
    commits: commitHashes.length,
    trackedFiles: Number(git(relativePath, ["ls-files"]).split("\n").filter(Boolean).length),
    dirtyEntries,
  };
});

const builderTools = readCsv("CURRENT/BUILDER_TOOL_INVENTORY.csv");
const researchResults = readCsv("CURRENT/RESEARCH_RESULTS.csv");
const works = readCsv("CURRENT/WORKS_REGISTER.csv");
const controllingSources = readCsv("CURRENT/CONTROLLING_SOURCES.csv");
const outreachChannels = readCsv("CURRENT/OUTREACH_CHANNELS.csv");
const portfolioTruth = JSON.parse(fs.readFileSync(path.join(missionControl, "CURRENT/PORTFOLIO_TRUTH.json"), "utf8"));
const navigatorControl = JSON.parse(fs.readFileSync(path.join(missionControl, "CURRENT/NAVIGATOR_SOURCE_GRAPH_CONTROL.json"), "utf8"));

const snapshot = {
  schema: "nexah.builder.ecosystem-achievements-snapshot/1.0.0",
  asOf: portfolioTruth.as_of,
  generatedAt: new Date().toISOString(),
  scope: "Local NEXAH ECOSYSTEM workspace; excludes Git object stores, node_modules, .work, tmp, Python caches and virtual environments.",
  caution: "Footprint and commit counts measure corpus scale, not unique authorship, scientific validity, publication state or product readiness.",
  filesystem: files,
  git: {
    repositoryCount: repositories.length,
    commitSum: repositories.reduce((sum, repository) => sum + repository.commits, 0),
    uniqueCommits: uniqueCommits.size,
    trackedFilesSum: repositories.reduce((sum, repository) => sum + repository.trackedFiles, 0),
    repositories,
  },
  registers: {
    builderObjects: builderTools.length,
    runnableBuilderObjects: builderTools.filter((row) => row.runnable_now === "YES").length,
    partialBuilderObjects: builderTools.filter((row) => row.runnable_now === "PARTIAL").length,
    nonRunnableBuilderObjects: builderTools.filter((row) => row.runnable_now === "NO").length,
    researchResults: researchResults.length,
    works: works.length,
    controllingSources: controllingSources.length,
    publicSurfaces: outreachChannels.filter((row) => row.channel_class === "PUBLIC_SURFACE").length,
    htmlArtifactsCovered: portfolioTruth.currentness.science_lab_html_artifacts_covered,
    sourceGraphEntities: navigatorControl.canonical_counts.composed_entities,
    sourceGraphRelations: navigatorControl.canonical_counts.composed_relations,
    sourceGraphComponents: navigatorControl.component_count,
  },
};

const jsonOutput = path.join(deck, "ecosystem-achievements.snapshot.json");
const jsOutput = path.join(deck, "ecosystem-achievements.snapshot.js");
fs.writeFileSync(jsonOutput, `${JSON.stringify(snapshot, null, 2)}\n`);
fs.writeFileSync(jsOutput, `globalThis.NEXAH_ECOSYSTEM_ACHIEVEMENTS = ${JSON.stringify(snapshot)};\n`);
console.log(JSON.stringify({ jsonOutput, jsOutput, ...snapshot.git, filesystem: snapshot.filesystem.totals, registers: snapshot.registers }, null, 2));
