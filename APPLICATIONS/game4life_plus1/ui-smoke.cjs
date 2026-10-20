const assert = require("node:assert/strict");
const fs = require("node:fs");
const vm = require("node:vm");
const LifeCylinder = require("./cylinder-engine.js");
const LifeCrystalProjection = require("./crystal-projection.js");
const LIFE08_RESULT = require("./results/PRIMARY_RESULT.json");
const html = fs.readFileSync("index.html", "utf8");

const context2d = {
  clearRect() {}, fillRect() {}, beginPath() {}, moveTo() {}, lineTo() {},
  stroke() {}, strokeRect() {}, setLineDash() {}, ellipse() {}, arc() {},
  fill() {}, closePath() {}, fillText() {}
};
const ids = ["fixture", "boundary", "channel", "generation", "projectionMode",
  "componentOutlines", "playPause", "speed", "runLength", "loopPlayback", "observeMode", "stepForward", "reset", "playbackStatus", "flat",
  "cylinder", "projectionTitle", "generationValue", "flatLabel", "cylinderLabel",
  "live", "eventCount", "seamBirths", "residual", "quaternion", "modeNote",
  "decision", "gates", "crystalHistory"];
const elements = Object.fromEntries(ids.map(id => [id, {
  id, value: "", textContent: "", innerHTML: "", style: {}, max: 0,
  width: id === "flat" || id === "cylinder" ? 760 : undefined,
  height: id === "flat" || id === "cylinder" ? 620 : undefined,
  options: [], add(option) { this.options.push(option); },
  getContext() { context2d.canvas = this; return context2d; }
}]));
elements.boundary.value = "cylinder-x";
elements.channel.value = "all";
elements.projectionMode.value = "cylinder";
elements.speed.value = "420";
elements.runLength.value = "520";
elements.loopPlayback.checked = true;
elements.generation.value = "0";
elements.componentOutlines.checked = true;
elements.crystalHistory.value = "60";
const radios = [{ value: "view", onchange: null }, { value: "dynamics", onchange: null }];
let activeRadio = radios[0];
let intervalCallback = null;
const sandbox = {
  window: { LifeCylinder, LIFE08_RESULT, LifeCrystalProjection, dispatchEvent(event) { sandbox.lastEvent = event; } },
  document: {
    getElementById: id => elements[id],
    querySelector: () => activeRadio,
    querySelectorAll: () => radios
  },
  Option: function Option(text, value) { return { text, value }; },
  setInterval(fn) { intervalCallback = fn; return 1; },
  clearInterval() { intervalCallback = null; },
  CustomEvent: function CustomEvent(type, init) { this.type = type; this.detail = init.detail; },
  console
};
vm.runInNewContext(fs.readFileSync("app.js", "utf8"), sandbox, { filename: "app.js" });

assert.equal(Number(elements.generation.value), 120);
assert.equal(Number(elements.generation.max), 520);
assert.equal(elements.channel.value, "all");
assert.match(elements.cylinderLabel.textContent, /4 components/);
assert.match(elements.playbackStatus.textContent, /Paused/);
elements.reset.onclick();
assert.equal(Number(elements.generation.value), 0);
elements.playPause.onclick();
assert.equal(elements.playPause.textContent, "Pause");
assert.equal(typeof intervalCallback, "function");
intervalCallback();
assert.equal(Number(elements.generation.value), 1);
elements.playPause.onclick();
assert.equal(elements.playPause.textContent, "Start");
elements.generation.value = elements.generation.max;
elements.playPause.onclick();
intervalCallback();
assert.equal(Number(elements.generation.value), 0);
assert.equal(elements.playPause.textContent, "Pause");
elements.playPause.onclick();
elements.projectionMode.value = "four-plus-one";
elements.projectionMode.onchange();
assert.equal(elements.projectionTitle.textContent, "4+1 event register");
elements.projectionMode.value = "phase-register";
elements.projectionMode.onchange();
assert.equal(elements.projectionTitle.textContent, "Temporal phase register");
elements.projectionMode.value = "transition-rosette";
elements.projectionMode.onchange();
assert.equal(elements.projectionTitle.textContent, "Transition rosette");
assert.equal(sandbox.lastEvent.type, "lifecrystal:render");
assert.equal(sandbox.lastEvent.detail.audit.inverseExact, true);
assert.match(html, /id="gearLifeSync"/);
assert.match(html, /id="gearCoupler"/);
assert.match(html, /life-clock-coupler\.css/);
elements.componentOutlines.checked = false;
elements.componentOutlines.onchange();
elements.channel.value = "residual";
elements.channel.onchange();
assert.match(elements.residual.textContent, /same state|cells/);
activeRadio = radios[1];
activeRadio.onchange();
assert.match(elements.modeNote.innerHTML, /DYNAMICS WRAP/);
console.log("PASS UI smoke 18/18");
