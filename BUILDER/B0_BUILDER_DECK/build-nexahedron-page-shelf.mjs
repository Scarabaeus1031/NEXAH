import { existsSync, readdirSync, readFileSync, writeFileSync } from "node:fs";
import { dirname, join, relative, resolve, sep } from "node:path";
import { fileURLToPath } from "node:url";

const deskRoot = dirname(fileURLToPath(import.meta.url));
const ecosystemRoot = resolve(deskRoot, "../../../..");
const ownerRoot = join(ecosystemRoot, "40 EXPERIENCE PRODUCTION", "NEXAHEDRON");
const publicRoot = join(ownerRoot, "public");
const startRoot = join(publicRoot, "a0-human", "start");
const journeyPath = join(startRoot, "A0_NEXAH_APERTURE_JOURNEY.html");
const outputPath = join(deskRoot, "public-nexahedron-page-shelf.html");

function walkHtml(directory) {
  return readdirSync(directory, { withFileTypes: true }).flatMap((entry) => {
    const absolute = join(directory, entry.name);
    if (entry.isDirectory()) return walkHtml(absolute);
    return entry.isFile() && entry.name.endsWith(".html") ? [absolute] : [];
  });
}

function decodeText(value = "") {
  return value
    .replace(/<[^>]*>/g, " ")
    .replace(/&amp;/g, "&")
    .replace(/&quot;/g, '"')
    .replace(/&#39;|&apos;/g, "'")
    .replace(/&nbsp;/g, " ")
    .replace(/\s+/g, " ")
    .trim();
}

function escapeHtml(value = "") {
  return value
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;")
    .replaceAll('"', "&quot;");
}

function extractTitle(source, fallback) {
  const title = source.match(/<title[^>]*>([\s\S]*?)<\/title>/i)?.[1];
  const h1 = source.match(/<h1[^>]*>([\s\S]*?)<\/h1>/i)?.[1];
  return decodeText(title || h1 || fallback.replace(/\.html$/i, "").replaceAll("_", " "));
}

function extractHrefs(source) {
  return [...source.matchAll(/\bhref\s*=\s*(["'])(.*?)\1/gi)].map((match) => match[2]);
}

function resolveLocalHtml(sourcePath, href) {
  if (!href || /^(?:#|[a-z][a-z\d+.-]*:|\/\/)/i.test(href)) return null;
  const clean = href.split("#", 1)[0].split("?", 1)[0];
  if (!clean) return null;

  let target;
  try {
    const decoded = decodeURIComponent(clean);
    target = decoded.startsWith("/")
      ? join(publicRoot, decoded.replace(/^\/+/, ""))
      : resolve(dirname(sourcePath), decoded);
  } catch {
    return null;
  }

  if (target.endsWith(sep) || !target.endsWith(".html")) target = join(target, "index.html");
  return existsSync(target) && target.startsWith(startRoot) ? target : null;
}

function sourceUrl(absolutePath) {
  const ownerRelative = relative(ownerRoot, absolutePath).split(sep).map(encodeURIComponent).join("/");
  return `../../../../40%20EXPERIENCE%20PRODUCTION/NEXAHEDRON/${ownerRelative}`;
}

const files = walkHtml(startRoot).sort();
const sources = new Map(files.map((file) => [file, readFileSync(file, "utf8")]));
const inbound = new Map(files.map((file) => [file, new Set()]));
const outbound = new Map(files.map((file) => [file, new Set()]));
const titleByFile = new Map(files.map((file) => {
  const path = relative(startRoot, file).split(sep).join("/");
  return [file, extractTitle(sources.get(file), path.split("/").at(-1))];
}));

for (const [sourcePath, source] of sources) {
  for (const href of extractHrefs(source)) {
    const target = resolveLocalHtml(sourcePath, href);
    if (target && inbound.has(target) && target !== sourcePath) {
      inbound.get(target).add(sourcePath);
      outbound.get(sourcePath).add(target);
    }
  }
}

const journeyTargets = new Set(
  extractHrefs(sources.get(journeyPath) || "")
    .map((href) => resolveLocalHtml(journeyPath, href))
    .filter(Boolean),
);

const pages = files.map((file) => {
  const path = relative(startRoot, file).split(sep).join("/");
  const isJourney = file === journeyPath;
  const isDirect = journeyTargets.has(file);
  const inboundSources = [...inbound.get(file)].sort((a, b) => titleByFile.get(a).localeCompare(titleByFile.get(b), "de"));
  const inboundCount = inboundSources.length;
  const outboundCount = outbound.get(file).size;
  const status = isJourney ? "journey" : isDirect ? "direct" : inboundCount ? "referenced" : "unlinked";
  const surface = path.startsWith("assets/") ? "runtime" : "page";
  return {
    file,
    path,
    title: titleByFile.get(file),
    status,
    surface,
    inboundCount,
    outboundCount,
    inboundSources,
  };
}).sort((a, b) => {
  const rank = { journey: 0, direct: 1, referenced: 2, unlinked: 3 };
  return rank[a.status] - rank[b.status] || a.title.localeCompare(b.title, "de");
});

const counts = Object.fromEntries(["journey", "direct", "referenced", "unlinked"].map((key) => [key, pages.filter((page) => page.status === key).length]));
const statusLabel = {
  journey: "Journey",
  direct: "Journey-Link",
  referenced: "anders referenziert",
  unlinked: "kein statischer Eingang",
};

const rows = pages.map((page, index) => {
  const parents = page.inboundSources.map((source) => {
    const path = relative(startRoot, source).split(sep).join("/");
    return `<li><a href="${sourceUrl(source)}"><strong>${escapeHtml(titleByFile.get(source))}</strong><small>${escapeHtml(path)}</small></a></li>`;
  }).join("");
  const relationDetail = page.inboundCount
    ? `<details class="page-shelf-parents"><summary>Hängt an ${page.inboundCount} Seite${page.inboundCount === 1 ? "" : "n"}</summary><ul>${parents}</ul></details>`
    : `<p class="page-shelf-orphan">Nirgends statisch eingehängt</p>`;
  const searchText = `${page.title} ${page.path} ${page.inboundSources.map((source) => `${titleByFile.get(source)} ${relative(startRoot, source)}`).join(" ")}`.toLowerCase();
  return `
        <article class="page-shelf-item" data-page-item data-order="${index}" data-status="${page.status}" data-surface="${page.surface}" data-title="${escapeHtml(page.title.toLowerCase())}" data-path="${escapeHtml(page.path.toLowerCase())}" data-inbound="${page.inboundCount}" data-outbound="${page.outboundCount}" data-search="${escapeHtml(searchText)}">
          <span class="page-shelf-index">${String(index + 1).padStart(2, "0")}</span>
          <div class="page-shelf-copy"><strong>${escapeHtml(page.title)}</strong><small>${escapeHtml(page.path)}</small>${relationDetail}</div>
          <span class="page-shelf-status page-shelf-status--${page.status}">${statusLabel[page.status]}</span>
          <span class="page-shelf-degree"><b>${page.inboundCount}</b> rein · <b>${page.outboundCount}</b> raus</span>
          <a href="${sourceUrl(page.file)}">Öffnen ↗</a>
        </article>`;
}).join("");

const html = `<!doctype html>
<html lang="de">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <meta name="description" content="Vollständiges source-bound Seitenregal der NEXAHEDRON A0 Human View.">
  <title>B0 Public · NEXAHEDRON Page Shelf</title>
  <link rel="stylesheet" href="styles.css">
</head>
<body class="area-page area-page-public page-shelf-page">
  <a class="skip-link" href="#main">Zum Inhalt</a>
  <header class="topbar">
    <a class="wordmark" href="index.html"><span class="mark">B0</span><span>BUILDER DECK</span></a>
    <nav class="desk-nav" aria-label="B0 Arbeitsbereiche">
      <a href="index.html"><span>00</span>Architect</a><a href="systems-desk.html"><span>01</span>Systems</a><a href="build-desk.html"><span>02</span>Build</a><a class="is-current" href="public-field.html" aria-current="page"><span>03</span>Public</a><a href="a0-tools.html"><span>04</span>A0</a><a href="archive.html"><span>05</span>Archive</a>
    </nav>
    <a class="mc-link" href="public-nexahedron-human-reading.html#page-shelf">Bauplan ↩</a>
  </header>

  <main id="main">
    <section class="area-hero page-shelf-hero">
      <div><p class="eyebrow">PUBLIC SOURCE SHELF · NEXAHEDRON</p><h1>Alle Türen.<br><em>Eine Quelle.</em></h1><p>Die Aperture Journey bleibt die geführte Route. Dieses Builder-Regal hält sämtliche HTML-Flächen auffindbar — auch jene, die die Journey derzeit nicht direkt benutzt.</p></div>
      <aside><span>SOURCE</span><strong>75 HTML SURFACES · LOCAL POINTERS</strong><p>Keine Datei wurde verschoben oder kopiert. Jeder Link öffnet die bestehende Fläche in ihrem owning repository.</p></aside>
    </section>

    <section class="section page-shelf-summary" aria-labelledby="summary-title">
      <header class="section-head"><div><p class="eyebrow">APERTURE JOURNEY · SOURCE MAP</p><h2 id="summary-title">Geführt vorne. Vollständig dahinter.</h2></div><p>„Nicht in der Journey“ bedeutet nur: kein direkter Link aus der aktuellen Aperture-Journey-Datei. Es ist keine Lösch-, Qualitäts- oder Release-Aussage.</p></header>
      <div class="page-shelf-counts">
        <article><span>J</span><strong>${counts.journey}</strong><small>Aperture Journey</small></article>
        <article><span>→</span><strong>${counts.direct}</strong><small>direkte Journey-Links</small></article>
        <article><span>↗</span><strong>${counts.referenced}</strong><small>anders statisch referenziert</small></article>
        <article><span>○</span><strong>${counts.unlinked}</strong><small>kein statischer Eingang gefunden</small></article>
      </div>
      <div class="inventory-authority"><strong>OWNER</strong><span>NEXAHEDRON/public/a0-human/start · aus dem aktuellen Source Tree generiert</span><a href="${sourceUrl(journeyPath)}">Aperture Journey öffnen ↗</a></div>
    </section>

    <section class="section" id="page-shelf" aria-labelledby="shelf-title">
      <header class="section-head"><div><p class="eyebrow">COMPLETE HTML INVENTORY</p><h2 id="shelf-title">Seiten &amp; Runtimes.</h2></div><p>75 direkte Source-Links. Filter dienen nur der Auffindbarkeit; sie verändern keine Route und keinen Status im Quellsystem.</p></header>
      <div class="page-shelf-toolbar" role="search">
        <label for="page-search">Suchen</label>
        <input id="page-search" type="search" placeholder="Titel oder Dateiname" autocomplete="off">
        <label for="page-status">Journey-Bezug</label>
        <select id="page-status"><option value="all">Alle</option><option value="journey">Journey</option><option value="direct">Direkt verlinkt</option><option value="referenced">Anders referenziert</option><option value="unlinked">Kein statischer Eingang</option><option value="not-direct">Nicht direkt in Journey</option></select>
        <label for="page-surface">Fläche</label>
        <select id="page-surface"><option value="all">Alle</option><option value="page">Public Page</option><option value="runtime">Runtime / Asset</option></select>
        <label for="page-sort">Sortieren</label>
        <select id="page-sort"><option value="route">Journey / Beziehung</option><option value="inbound-desc">Stark verbunden zuerst</option><option value="inbound-asc">Lose verbunden zuerst</option><option value="orphans-first">Nirgends eingehängt zuerst</option><option value="outbound-desc">Viele Ziele zuerst</option><option value="title">Titel A–Z</option><option value="path">Dateipfad A–Z</option></select>
        <strong id="page-result-count" aria-live="polite">75 / 75</strong>
      </div>
      <div class="page-shelf-list" aria-label="NEXAHEDRON Seiteninventar">${rows}
      </div>
      <div class="boundary"><strong>Boundary:</strong> Das Regal ist ein Builder-Pointer. Inhalt, Identität, wissenschaftliche Bedeutung, Veröffentlichung und Lifecycle bleiben vollständig bei der jeweiligen NEXAHEDRON-Quelle.</div>
    </section>
  </main>
  <footer class="footer"><div><span class="mark">B0</span><p><strong>Public · NEXAHEDRON Page Shelf</strong><br>find · inspect · choose · return</p></div><p>Generierte lokale Auffindbarkeit, keine Aktivierung.</p><a href="public-nexahedron-human-reading.html">Bauplan →</a></footer>
  <script>
    const search = document.querySelector("#page-search");
    const status = document.querySelector("#page-status");
    const surface = document.querySelector("#page-surface");
    const sorter = document.querySelector("#page-sort");
    const list = document.querySelector(".page-shelf-list");
    const items = [...document.querySelectorAll("[data-page-item]")];
    const count = document.querySelector("#page-result-count");
    const compareItems = (a, b) => {
      const number = (item, key) => Number(item.dataset[key]);
      if (sorter.value === "inbound-desc") return number(b, "inbound") - number(a, "inbound") || a.dataset.title.localeCompare(b.dataset.title, "de");
      if (sorter.value === "inbound-asc") return number(a, "inbound") - number(b, "inbound") || a.dataset.title.localeCompare(b.dataset.title, "de");
      if (sorter.value === "orphans-first") return (number(a, "inbound") > 0) - (number(b, "inbound") > 0) || number(a, "inbound") - number(b, "inbound") || a.dataset.title.localeCompare(b.dataset.title, "de");
      if (sorter.value === "outbound-desc") return number(b, "outbound") - number(a, "outbound") || a.dataset.title.localeCompare(b.dataset.title, "de");
      if (sorter.value === "title") return a.dataset.title.localeCompare(b.dataset.title, "de");
      if (sorter.value === "path") return a.dataset.path.localeCompare(b.dataset.path, "de");
      return number(a, "order") - number(b, "order");
    };
    const applyFilters = () => {
      const query = search.value.trim().toLowerCase();
      let visible = 0;
      const ordered = [...items].sort(compareItems);
      for (const item of ordered) list.append(item);
      for (const item of ordered) {
        const statusMatch = status.value === "all" || item.dataset.status === status.value || (status.value === "not-direct" && item.dataset.status !== "journey" && item.dataset.status !== "direct");
        const surfaceMatch = surface.value === "all" || item.dataset.surface === surface.value;
        const searchMatch = !query || item.dataset.search.includes(query);
        item.hidden = !(statusMatch && surfaceMatch && searchMatch);
        if (!item.hidden) {
          visible += 1;
          item.querySelector(".page-shelf-index").textContent = String(visible).padStart(2, "0");
        }
      }
      count.textContent = visible + " / " + items.length;
    };
    search.addEventListener("input", applyFilters);
    status.addEventListener("change", applyFilters);
    surface.addEventListener("change", applyFilters);
    sorter.addEventListener("change", applyFilters);
  </script>
</body>
</html>`;

writeFileSync(outputPath, html);
console.log(`Wrote ${relative(deskRoot, outputPath)} with ${pages.length} HTML surfaces.`);
