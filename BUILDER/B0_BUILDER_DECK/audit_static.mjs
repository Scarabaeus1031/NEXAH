import assert from "node:assert/strict";
import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";

const root = path.dirname(fileURLToPath(import.meta.url));
const pageNames = ["index.html", "systems-desk.html", "build-desk.html", "public-field.html", "a0-tools.html", "archive.html"];
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
assert.match(architect, /M-PUB01 · Gate 0 abschließen/);
assert.match(architect, /CH-007 · CH-009 · CH-010/);
assert.match(architect, /Building ist aktuell der dominante Modus/);
assert.match(architect, /Jede Arbeit hat ihren eigenen Desk/);
assert.doesNotMatch(architect, /BUILDER ARCHIVE · SOURCE-BOUND/);
assert.doesNotMatch(architect, /Ein System\. Sieben klar getrennte Rollen/);

assert.match(systems, /01 · SYSTEMS DESK/);
assert.match(systems, /Sieben Rollen\. Ein prüfbarer Rückweg/);
for (const label of ["A0", "OLS", "Kernel", "ORION", "Navigator", "THE EYE", "NEXAHEDRON"]) assert.match(systems, new RegExp(label));
assert.match(systems, /BOUNDED COMPONENTS · NO UNIFIED RUNTIME/);

assert.match(build, /02 · BUILD DESK/);
assert.match(build, /To-dos nach Entscheidungstyp/);
assert.match(build, /CH-014 · Book Identity/);
assert.match(build, /CH-008 · CH-016/);
assert.match(build, /Orientieren\. Verbinden\. Benutzen/);

assert.match(publicHtml, /ONE FIELD/);
assert.match(publicHtml, /THREE HOUSES/);
assert.match(publicHtml, /NO HIDDEN COUPLING/);
assert.match(publicHtml, /LOCAL DESIGN \/ NO DEPLOY/);
assert.match(publicHtml, /How NEXAH Works — From Representation to Human Return/);
assert.match(publicHtml, /M-PUB01_NEXAH_PUBLIC_FIELD\.md/);
assert.match(publicHtml, /https:\/\/www\.scarabaeus1033\.net/);

assert.match(a0Html, /04 · A0 BUILDER DESK/);
assert.match(a0Html, /A0 Builder Log/);
assert.match(a0Html, /A0 Science Desk/);
assert.match(a0Html, /A0_RESEARCH_DESK\.html#desk-cabinet/);
assert.match(a0Html, /NEXAHEDRON_BUILDER_BACKLOG\.md/);

assert.match(archive, /05 · ARCHIVE DESK/);
assert.match(archive, /BUILDER ARCHIVE · SOURCE-BOUND/);
assert.equal([...archive.matchAll(/data-archive-item/g)].length, 16);
assert.match(archive, /CURRENT\/ENGINEERING_ASSEMBLY\.csv/);
assert.match(archive, /A0_RESEARCH_BACKLOG\.html/);

assert.match(css, /\.desk-nav/);
assert.match(css, /\.workspace-grid/);
assert.match(css, /\.system-blueprint/);
assert.match(css, /\.build-board/);
assert.match(css, /@media \(max-width: 760px\)/);
assert.match(css, /prefers-reduced-motion/);
assert.match(js, /dataset\.filter/);
assert.match(js, /archiveSearch/);
assert.match(js, /data-archive-item/);

const localLinks = Object.entries(pages).flatMap(([name, source]) =>
  [...source.matchAll(/href="([^"]+)"/g)]
    .map((match) => ({ name, href: match[1] }))
    .filter(({ href }) => !href.startsWith("#") && !href.startsWith("http"))
);
const missing = localLinks.filter(({ href }) => {
  const target = decodeURIComponent(href.split("#")[0]);
  return !fs.existsSync(path.resolve(root, target));
});
assert.deepEqual(missing, []);

console.log(`PASS · B0 six-desk architecture, source-bound workspaces, searchable 16-entry archive and ${localLinks.length} local links verified.`);
