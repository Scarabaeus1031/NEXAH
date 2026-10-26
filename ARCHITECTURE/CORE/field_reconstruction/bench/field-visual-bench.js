(function () {
  "use strict";
  const assets = window.NEXAH_FIELD_BENCH_ASSETS;
  const order = ["ALL", "CORE", "V2–V5", "V6", "V7", "V8", "V9", "V10", "NOISE", "ZETA", "MOTIF"];
  const notes = { ALL: "complete atlas", CORE: "reconstruction", "V2–V5": "field emergence", V6: "structure", V7: "navigation", V8: "stability", V9: "transport", V10: "boundary + time", NOISE: "robustness", ZETA: "coherence bridge", MOTIF: "owner mnemonics" };
  const state = { family: "ALL", mode: "atlas", selectedId: assets[0].id, compareId: assets[1].id, query: "", motif: null };
  const $ = (id) => document.getElementById(id);
  const el = {
    phase: $("phaseRail"), rail: $("assetRail"), count: $("visibleCount"), family: $("frameFamily"), title: $("frameTitle"), index: $("frameIndex"),
    primary: $("primaryImage"), secondary: $("secondaryImage"), layer: $("compareLayer"), seam: $("compareSeam"), range: $("compareRange"), value: $("compareValue"),
    stage: $("imageStage"), flag: $("stateFlag"), motifs: $("motifStrip"), reading: $("frameReading"), source: $("frameSource"), producer: $("frameProducer"),
    klass: $("frameClass"), boundary: $("frameBoundary"), relation: $("frameRelation"), search: $("search"), receipt: $("receiptPanel"), receiptGrid: $("receiptGrid"),
    receiptSummary: $("receiptSummary"), wall: $("wallPanel"), wallGrid: $("wallGrid"), tour: $("playTour")
  };
  let tourTimer = null;

  function visible() {
    const q = state.query.trim().toLowerCase();
    return assets.filter((a) => (state.family === "ALL" || a.family === state.family) && (!state.motif || a.motifs.includes(state.motif)) && (!q || [a.version, a.title, a.family, a.reading, a.class, ...a.motifs].join(" ").toLowerCase().includes(q)));
  }
  function selected() { return assets.find((a) => a.id === state.selectedId) || visible()[0] || assets[0]; }
  function compared() { return assets.find((a) => a.id === state.compareId) || assets[1]; }
  function renderFamilies() {
    el.phase.innerHTML = "";
    order.forEach((family) => {
      const count = family === "ALL" ? assets.length : assets.filter((a) => a.family === family).length;
      const button = document.createElement("button"); button.type = "button"; button.className = family === state.family ? "active" : "";
      button.innerHTML = `<span>${family}</span><small>${count} · ${notes[family]}</small>`;
      button.onclick = () => { state.family = family; state.motif = null; const first = visible()[0]; if (first) state.selectedId = first.id; render(); };
      el.phase.append(button);
    });
  }
  function renderRail() {
    const list = visible(); el.count.textContent = list.length; el.rail.innerHTML = "";
    list.forEach((a) => {
      const button = document.createElement("button"); button.type = "button"; button.className = `asset-button${a.id === state.selectedId ? " active" : ""}`;
      button.innerHTML = `<img src="${a.image}" alt=""><span><strong>${a.version} · ${a.title}</strong><small>${a.class}</small></span>`;
      button.onclick = () => { if (state.mode === "compare" && state.selectedId !== a.id) state.compareId = a.id; else state.selectedId = a.id; render(); };
      el.rail.append(button);
    });
  }
  function renderViewer() {
    const a = selected(), c = compared(), list = visible(), index = Math.max(0, list.findIndex((x) => x.id === a.id));
    el.family.textContent = `${a.family} · ${a.version}`; el.title.textContent = a.title; el.index.textContent = `${String(index + 1).padStart(2, "0")} / ${String(list.length).padStart(2, "0")}`;
    el.primary.src = a.image; el.primary.alt = `${a.version} — ${a.title}`; el.secondary.src = c.image; el.secondary.alt = `Comparison: ${c.version} — ${c.title}`;
    el.flag.textContent = state.mode === "compare" ? `${a.version} ↔ ${c.version}` : a.class; el.reading.textContent = a.reading; el.source.textContent = a.image;
    el.producer.textContent = a.producer; el.klass.textContent = a.class; el.boundary.textContent = a.boundary; el.relation.textContent = a.relation; el.motifs.innerHTML = "";
    a.motifs.forEach((motif) => {
      const button = document.createElement("button"); button.type = "button"; button.className = `motif-chip${state.motif === motif ? " active" : ""}`;
      button.textContent = `OWNER MNEMONIC · ${motif.toUpperCase()}`;
      button.onclick = () => { state.motif = state.motif === motif ? null : motif; state.family = "ALL"; const first = visible()[0]; if (first) state.selectedId = first.id; render(); };
      el.motifs.append(button);
    });
    requestAnimationFrame(syncCompare);
  }
  function renderReceipt() {
    el.receiptSummary.textContent = `${assets.length} frames · ${new Set(assets.map((a) => a.producer)).size} source bindings · ${new Set(assets.map((a) => a.family)).size} families`;
    el.receiptGrid.innerHTML = assets.map((a) => `<div class="receipt-item"><span>${a.version} · ${a.title}</span><code>${a.image}</code><code>← ${a.producer}</code></div>`).join("");
  }
  function renderWall() {
    el.wallGrid.innerHTML = visible().map((a) => `<button type="button" class="wall-item" data-id="${a.id}"><img src="${a.image}" alt=""><span>${a.version} · ${a.title}</span><small>${a.class}</small></button>`).join("");
    el.wallGrid.querySelectorAll(".wall-item").forEach((button) => { button.onclick = () => { state.selectedId = button.dataset.id; state.mode = "atlas"; render(); }; });
  }
  function renderMode() {
    document.body.className = `mode-${state.mode}`;
    document.querySelectorAll("[data-mode]").forEach((button) => button.classList.toggle("active", button.dataset.mode === state.mode));
    el.receipt.hidden = state.mode !== "receipt"; el.wall.hidden = state.mode !== "wall";
  }
  function render() {
    const list = visible(); if (list.length && !list.some((a) => a.id === state.selectedId)) state.selectedId = list[0].id;
    renderMode(); renderFamilies(); renderRail(); renderViewer(); renderReceipt(); renderWall();
  }
  function move(delta) { const list = visible(); if (!list.length) return; const current = Math.max(0, list.findIndex((a) => a.id === state.selectedId)); state.selectedId = list[(current + delta + list.length) % list.length].id; render(); }
  function syncCompare() { el.secondary.style.width = `${el.stage.getBoundingClientRect().width}px`; }
  function setSeam(value) { el.layer.style.width = `${value}%`; el.seam.style.left = `${value}%`; el.value.value = `${value}%`; }
  function toggleTour() {
    if (tourTimer) { clearInterval(tourTimer); tourTimer = null; el.tour.textContent = "▶ TOUR"; el.tour.classList.remove("active"); return; }
    state.mode = "atlas"; state.family = "ALL"; state.motif = null; el.tour.textContent = "■ STOP"; el.tour.classList.add("active"); render();
    tourTimer = setInterval(() => move(1), 2400);
  }
  function exportReceipt() {
    const data = { instrument: "NEXAH_FIELD_VISUAL_BENCH", identity: "ARCHITECTURE/CORE/field_reconstruction", authority: "source-bound display lens; original files remain authoritative", generatedAt: new Date().toISOString(), selected: selected().id, comparison: state.mode === "compare" ? compared().id : null, filters: { family: state.family, query: state.query, motif: state.motif }, assets };
    const blob = new Blob([JSON.stringify(data, null, 2)], { type: "application/json" }), url = URL.createObjectURL(blob), link = document.createElement("a"); link.href = url; link.download = "nexah-field-visual-bench-receipt.json"; link.click(); URL.revokeObjectURL(url);
  }

  document.querySelectorAll("[data-mode]").forEach((button) => { button.onclick = () => { state.mode = button.dataset.mode; render(); }; });
  el.tour.onclick = toggleTour; $("previous").onclick = () => move(-1); $("next").onclick = () => move(1); $("exportReceipt").onclick = exportReceipt;
  el.search.oninput = (event) => { state.query = event.target.value; render(); }; el.range.oninput = (event) => setSeam(event.target.value); window.onresize = syncCompare;
  window.addEventListener("keydown", (event) => { if (event.target.matches("input")) return; if (event.key === "ArrowLeft") move(-1); if (event.key === "ArrowRight") move(1); if (event.key === " ") { event.preventDefault(); toggleTour(); } });
  setSeam(50); render();
}());
