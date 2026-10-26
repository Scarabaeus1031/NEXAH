(() => {
  "use strict";

  const stages = JSON.parse(document.getElementById("stage-data").textContent);
  const state = { index: 0, timer: null, ui: false, spark: false, compare: false };
  const byId = (id) => document.getElementById(id);
  const els = {
    pipeline: byId("pipeline"), image: byId("stageImage"), compareImage: byId("compareImage"),
    viewport: byId("viewport"), imageWell: document.querySelector(".image-well"),
    number: byId("stageNumber"), class: byId("stageClass"), title: byId("stageTitle"),
    operation: byId("stageOperation"), carrier: byId("stageCarrier"), producer: byId("stageProducer"),
    sources: byId("stageSources"), status: byId("stageStatus"),
    boundary: byId("stageBoundary"), progress: byId("progressBar"), play: byId("play"),
    uiOverlay: byId("uiOverlay"), sparkOverlay: byId("sparkOverlay")
  };

  stages.forEach((stage, index) => {
    const button = document.createElement("button");
    button.type = "button";
    button.innerHTML = `<b>${String(index + 1).padStart(2, "0")} · ${stage.group}</b>${stage.title}`;
    button.addEventListener("click", () => render(index));
    els.pipeline.appendChild(button);
  });

  function render(index) {
    state.index = (index + stages.length) % stages.length;
    const stage = stages[state.index];
    els.image.src = stage.image;
    els.image.alt = `${stage.title}: ${stage.operation}`;
    els.compareImage.src = stage.compare;
    els.number.textContent = `${String(state.index + 1).padStart(2, "0")} / ${stages.length}`;
    els.class.textContent = stage.group;
    els.title.textContent = stage.title;
    els.operation.textContent = stage.operation;
    els.carrier.textContent = stage.carrier;
    els.producer.textContent = stage.producer;
    els.sources.textContent = stage.sources ? stage.sources.join(" · ") : "local source script + generated frame";
    els.status.textContent = stage.status || "existing experimental frame";
    els.boundary.textContent = stage.boundary;
    els.progress.style.width = `${((state.index + 1) / stages.length) * 100}%`;
    [...els.pipeline.children].forEach((button, i) => button.classList.toggle("active", i === state.index));
    els.pipeline.children[state.index].scrollIntoView({ behavior: "smooth", block: "nearest", inline: "center" });
  }

  function toggle(buttonId, key, element) {
    state[key] = !state[key];
    byId(buttonId).classList.toggle("active", state[key]);
    element.classList.toggle("visible", state[key]);
    els.imageWell.classList.toggle("annotated", state.ui || state.spark);
  }

  function stop() {
    if (state.timer) window.clearInterval(state.timer);
    state.timer = null;
    els.play.textContent = "PLAY";
    els.play.classList.add("primary");
  }

  byId("previous").addEventListener("click", () => { stop(); render(state.index - 1); });
  byId("next").addEventListener("click", () => { stop(); render(state.index + 1); });
  els.play.addEventListener("click", () => {
    if (state.timer) return stop();
    els.play.textContent = "PAUSE";
    els.play.classList.remove("primary");
    state.timer = window.setInterval(() => render(state.index + 1), 2600);
  });
  byId("toggleUi").addEventListener("click", () => toggle("toggleUi", "ui", els.uiOverlay));
  byId("toggleSpark").addEventListener("click", () => toggle("toggleSpark", "spark", els.sparkOverlay));
  byId("toggleCompare").addEventListener("click", () => {
    state.compare = !state.compare;
    byId("toggleCompare").classList.toggle("active", state.compare);
    els.imageWell.classList.toggle("compare", state.compare);
  });
  byId("exportReceipt").addEventListener("click", () => {
    const stage = stages[state.index];
    const receipt = {
      instrument: "NEXAH Field Reconstruction Demonstrator",
      source_module: "NEXAH/ARCHITECTURE/CORE/field_reconstruction",
      stage_index: state.index + 1,
      stage,
      view: { ui_annotation: state.ui, orange_spark_annotation: state.spark, comparison: state.compare },
      authority: "display/comparison instrument; source scripts retain implementation authority",
      exported_at: new Date().toISOString()
    };
    const blob = new Blob([JSON.stringify(receipt, null, 2)], { type: "application/json" });
    const link = document.createElement("a");
    link.href = URL.createObjectURL(blob);
    link.download = `nexah-field-reconstruction-${stage.id}-receipt.json`;
    link.click();
    URL.revokeObjectURL(link.href);
  });

  document.addEventListener("keydown", (event) => {
    if (event.key === "ArrowLeft") render(state.index - 1);
    if (event.key === "ArrowRight") render(state.index + 1);
    if (event.key.toLowerCase() === "u") byId("toggleUi").click();
    if (event.key.toLowerCase() === "s") byId("toggleSpark").click();
  });

  render(0);
})();
