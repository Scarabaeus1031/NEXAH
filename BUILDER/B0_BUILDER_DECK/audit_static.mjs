import assert from "node:assert/strict";
import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";

const root = path.dirname(fileURLToPath(import.meta.url));
const pageNames = ["index.html", "systems-desk.html", "build-desk.html", "public-field.html", "a0-tools.html", "archive.html", "project-a0-pentagon-body-return.html", "public-nexahedron-human-reading.html"];
const pages = Object.fromEntries(pageNames.map((name) => [name, fs.readFileSync(path.join(root, name), "utf8")]));
const architect = pages["index.html"];
const systems = pages["systems-desk.html"];
const build = pages["build-desk.html"];
const publicHtml = pages["public-field.html"];
const a0Html = pages["a0-tools.html"];
const archive = pages["archive.html"];
const css = fs.readFileSync(path.join(root, "styles.css"), "utf8");
const js = fs.readFileSync(path.join(root, "app.js"), "utf8");

for (const [name, html] of Object.entries(pages)) {
  assert.match(html, /class="desk-nav"/, `${name}: shared desk navigation missing`);
  assert.match(html, /index\.html/, `${name}: Architect link missing`);
  assert.match(html, /systems-desk\.html/, `${name}: Systems link missing`);
  assert.match(html, /build-desk\.html/, `${name}: Build link missing`);
  assert.match(html, /public-field\.html/, `${name}: Public link missing`);
  assert.match(html, /a0-tools\.html/, `${name}: A0 link missing`);
  assert.match(html, /archive\.html/, `${name}: Archive link missing`);
}

assert.match(architect, /B0 · Architect Desk/);
assert.match(architect, /00 · ARCHITECT DESK/);
assert.match(architect, /Bauplan &amp; Arbeitsstand/);
assert.match(architect, /A0 \+ Currentness/);
assert.match(architect, /466 Quellen · 0 Fehler/);
assert.match(architect, /NEXAH \+ Scarabæus Receipts/);
assert.match(architect, /CH-007\/009\/010/);
assert.match(architect, /Building ist aktuell der dominante Modus/);
assert.match(architect, /Jede Arbeit hat ihren eigenen Desk/);
assert.doesNotMatch(architect, /BUILDER ARCHIVE · SOURCE-BOUND/);
assert.doesNotMatch(architect, /Ein System\. Sieben klar getrennte Rollen/);

assert.match(systems, /01 · SYSTEMS DESK/);
assert.match(systems, /Systemarchitektur/);
assert.match(systems, /Bauräume &amp; Übergaben/);
assert.match(systems, /Carrier &amp; Formate/);
assert.match(systems, /Baupläne &amp; Systemkarten/);
for (const label of ["A0", "OLS", "Kernel", "ORION", "Navigator", "THE EYE", "NEXAHEDRON"]) assert.match(systems, new RegExp(label));
for (const sectionId of ["big-picture", "build-rooms", "projects", "inventory", "carriers", "maturity", "blueprints", "laws", "sources"]) assert.match(systems, new RegExp(`id="${sectionId}"`));
assert.match(systems, /keine technische Kopplung/);
assert.match(systems, /Builder Laws/);
assert.match(systems, /GOAL → SOURCE → SMALL CUT → CHECK → RETURN → CLOSE/);
assert.match(systems, /BUILDER_POLICY\.md/);
assert.match(systems, /A0 \/ THE MACHINA/);
assert.match(systems, /PROJECT_THE_MACHINA_EXHIBITION_2026-10-26\.md/);
assert.match(systems, /Exhibition, Machine Series, Parts Shelf und Bench/);
assert.match(systems, /NEXAH \+ NEXAHEDRON/);
assert.match(systems, /BUILDER_TOOL_INVENTORY\.csv/);
assert.equal([...systems.matchAll(/data-build-item/g)].length, 44);

assert.match(build, /02 · BUILD DESK/);
assert.match(build, /BUILDER NOTES · LETZTER STAND · 26\.10\.2026/);
assert.match(build, /B0 Plateau 01/);
assert.match(build, /71 \/ 71/);
assert.match(build, /253 \/ 253/);
assert.match(build, /466 Quellen · 0 Fehler/);
assert.equal([...build.matchAll(/class="priority-project /g)].length, 3);
assert.match(build, /M-PUB01/);
assert.match(build, /NEXAH × NEXAHEDRON/);
assert.match(build, /A0 \/ THE MACHINA/);
assert.match(build, /PROJECT RECORDED · NO BUILD/);
assert.match(build, /PROJECT_THE_MACHINA_EXHIBITION_2026-10-26\.md/);
assert.match(build, /public-nexahedron-human-reading\.html/);
assert.match(build, /Pentagon Body · Guided v2 \+ Exhibition/);
assert.match(build, /A0_PENTAGON_BODY_RETURN_GUIDED\.html/);
assert.match(build, /A0_PENTAGON_BODY_EXHIBITION\.html/);
assert.match(build, /Inventar vollständig · ein Staging-Paket reproduzierbar/);
assert.match(build, /Orientieren\. Verbinden\. Benutzen/);
assert.match(build, /BUILD REGISTER · SOURCE-BOUND/);
assert.match(build, /Zwei Fenster\. Vierzehn Builds\./);
assert.match(build, /A0_BUILDER_TOY_STORE\.html#instrument-atlas/);
assert.match(build, /A0_RESEARCH_DESK\.html#instrument-atlas-return-20261025/);
assert.equal([...build.matchAll(/data-build-log-item/g)].length, 14);
assert.match(build, /Crown → Shadow Contact Bench/);
assert.match(build, /A0_CROWN_SHADOW_CONTACT_BENCH\.html/);
assert.match(build, /110\/110 Hashes und 88\/88 Engineering-Checks/);
assert.match(build, /Field Reconstruction Package/);
assert.match(build, /61-frame bench und 122 Source-Hashes/);
assert.match(build, /NEXAH_FIELD_RECONSTRUCTION_PACKAGE\.html/);
assert.match(build, /Body\/Pole\/Lantern-Kopplung bleibt UNDEFINED_CONTRACT/);

const pentagonProject = pages["project-a0-pentagon-body-return.html"];
assert.match(pentagonProject, /Pentagon \/ <em>Body Return/);
assert.match(pentagonProject, /GUIDED ACCEPTED · BODY WIRING OPEN/);
assert.match(pentagonProject, /SOURCE BODY → MOVE → PROJECT → COMPARE → RETURN \/ CANNOT RETURN/);
assert.match(pentagonProject, /114/);
assert.match(pentagonProject, /PROJECT_A0_PENTAGON_BODY_RETURN_2026-10-25\.md/);
assert.match(pentagonProject, /A0_PENTAGON_BODY_RETURN_GUIDED\.html/);
assert.match(pentagonProject, /17 STAGES · 61 FRAMES · 122 HASHES/);
assert.match(pentagonProject, /OPEN · GATE → BRIDGE/);
assert.match(pentagonProject, /OPEN · BODY → POLE → LANTERN/);
assert.match(pentagonProject, /keine Shared Clock/);
assert.match(pentagonProject, /BODY SYNTHESIS UNDEFINED_CONTRACT/);

const humanReadingProject = pages["public-nexahedron-human-reading.html"];
assert.match(humanReadingProject, /Der Unterschied <em>wird lesbar/);
assert.match(humanReadingProject, /CONCEPT FREEZE · LOCAL ONLY/);
assert.match(humanReadingProject, /Dark Room/);
assert.match(humanReadingProject, /Diamond Lens/);
assert.match(humanReadingProject, /One Pulse/);
assert.match(humanReadingProject, /PUBLIC_NEXAHEDRON_HUMAN_READING_2026-10-25\.md/);

assert.match(publicHtml, /ONE FIELD/);
assert.match(publicHtml, /THREE HOUSES/);
assert.match(publicHtml, /NO HIDDEN COUPLING/);
assert.match(publicHtml, /LOCAL DESIGN \/ NO DEPLOY/);
assert.match(publicHtml, /How NEXAH Works — From Representation to Human Return/);
assert.match(publicHtml, /M-PUB01_NEXAH_PUBLIC_FIELD\.md/);
assert.match(publicHtml, /CURRENT LOCAL WEBSITE PROJECT/);
assert.match(publicHtml, /public-nexahedron-human-reading\.html/);
assert.match(publicHtml, /https:\/\/www\.scarabaeus1033\.net/);

assert.match(a0Html, /04 · A0 BUILDER DESK/);
assert.match(a0Html, /A0 Builder Log/);
assert.match(a0Html, /A0 Science Desk/);
assert.match(a0Html, /A0_RESEARCH_DESK\.html#desk-cabinet/);
assert.match(a0Html, /NEXAHEDRON_BUILDER_BACKLOG\.md/);
assert.match(a0Html, /12 CURRENT BUILDS/);
assert.match(a0Html, /build-desk\.html#latest-builds/);

assert.match(archive, /05 · ARCHIVE DESK/);
assert.match(archive, /BUILDER ARCHIVE · SOURCE-BOUND/);
assert.equal([...archive.matchAll(/data-archive-item/g)].length, 16);
assert.match(archive, /CURRENT\/ENGINEERING_ASSEMBLY\.csv/);
assert.match(archive, /A0_RESEARCH_BACKLOG\.html/);

assert.match(css, /\.desk-nav/);
assert.match(css, /\.workspace-grid/);
assert.match(css, /\.architecture-map/);
assert.match(css, /\.build-room-table/);
assert.match(css, /\.builder-laws/);
assert.match(css, /\.project-wall/);
assert.match(css, /\.build-inventory-list/);
assert.match(css, /\.build-board/);
assert.match(css, /\.recent-build-list/);
assert.match(css, /\.build-register-window/);
assert.match(css, /\.build-log-return/);
assert.match(css, /@media \(max-width: 760px\)/);
assert.match(css, /prefers-reduced-motion/);
assert.match(js, /dataset\.filter/);
assert.match(js, /archiveSearch/);
assert.match(js, /data-archive-item/);
assert.match(js, /buildInventorySearch/);
assert.match(js, /buildRegisterGroups/);
assert.equal([...build.matchAll(/data-build-log-group/g)].length, 2);
assert.equal([...build.matchAll(/data-build-log-item/g)].length, 14);
assert.match(build, /BUILD \/ MACHINE/);
assert.match(build, /SCIENCE \/ INSTRUMENT/);
assert.match(build, /5 BUILDS/);
assert.match(build, /9 INSTRUMENTS/);

const localLinks = Object.entries(pages).flatMap(([name, source]) =>
  [...source.matchAll(/href="([^"]+)"/g)]
    .map((match) => ({ name, href: match[1] }))
    .filter(({ href }) => !href.startsWith("#") && !href.startsWith("http"))
);
const missing = localLinks.filter(({ href }) => {
  const target = decodeURIComponent(href.split(/[?#]/)[0]);
  return !fs.existsSync(path.resolve(root, target));
});
assert.deepEqual(missing, []);

console.log(`PASS · B0 six-desk architecture, source-bound workspaces, searchable 16-entry archive and ${localLinks.length} local links verified.`);
