const fs = require("node:fs");
const path = require("node:path");
const crypto = require("node:crypto");
const E = require("./cylinder-engine.js");
const protocol = require("./PREREGISTRATION.json");
const lock = require("./PREREGISTRATION_LOCK.json");
const root = __dirname;
const out = path.join(root, "results");
fs.mkdirSync(out, { recursive: true });

const canonical = value => JSON.stringify(value, Object.keys(value).sort());
const stateKey = s => s.live.map(c => c.join(",")).join(";");
const sameCells = (a, b) => stateKey(a) === stateKey(b);

function summarizeRun(run, dead) {
  let first = null, agree = 0;
  for (let i = 0; i < run.states.length; i++) {
    const ok = sameCells(run.states[i], dead.states[i]);
    if (ok) agree++; else if (first === null) first = i;
  }
  return {
    fixture: run.id,
    boundary: run.boundary,
    firstDivergence: first,
    exactStateAgreementRate: agree / run.states.length,
    seamBirths: run.rows.reduce((a, r) => a + r.seamBirths, 0),
    lag2CountReturn: Object.fromEntries(E.CHANNELS.map((k, i) => [k, E.countReturn(run.rows, i)])),
    lag2SpatialReturn: Object.fromEntries(E.CHANNELS.map((k, i) => [k, E.spatialReturn(run.rows, i)])),
    finalLive: run.states.at(-1).live.length
  };
}
function evaluate() {
  const runs = [];
  for (const spec of protocol.fixtures) for (const boundary of protocol.boundary_modes) runs.push(E.run(spec, boundary));
  const get = (id, boundary) => runs.find(r => r.id === id && r.boundary === boundary);
  const summaries = [];
  for (const spec of protocol.fixtures) {
    const dead = get(spec.id, "finite-dead");
    for (const boundary of protocol.boundary_modes) summaries.push(summarizeRun(get(spec.id, boundary), dead));
  }
  const negativeControlsStable = ["BLOCK-C", "BLINKER-C"].every(id => ["cylinder-x", "cylinder-y"].every(b => get(id, b).states.every((s, i) => sameCells(s, get(id, "finite-dead").states[i]))));
  const x = E.initial({ id: "EQX", kind: "explicit", size: 32, cells: [[0, 1], [31, 1], [0, 2], [1, 2], [31, 3]], horizon: 1 }, "cylinder-x");
  const y = E.initial({ id: "EQY", kind: "explicit", size: 32, cells: [[1, 0], [1, 31], [2, 0], [2, 1], [3, 31]], horizon: 1 }, "cylinder-y");
  const cylinderXEquivariant = E.equal(E.step(E.translate(x, 1, 0)), E.translate(E.step(x), 1, 0));
  const cylinderYEquivariant = E.equal(E.step(E.translate(y, 0, 1)), E.translate(E.step(y), 0, 1));
  const boundaryEffectDetected = summaries.some(s => s.boundary !== "finite-dead" && s.firstDivergence !== null);
  const quaternionRegisterExact = runs.every(r => r.rows.every(row => {
    const back = E.quaternionInverse(row.quaternion);
    return back.every((v, i) => v === row.counts[i]) && row.quaternion.scalar === row.counts.reduce((a, n) => a + n, 0);
  }));
  const gates = { negativeControlsStable, cylinderXEquivariant, cylinderYEquivariant, boundaryEffectDetected, quaternionRegisterExact };
  const corePass = Object.values(gates).every(Boolean);
  return {
    id: "LIFE08-BOUNDARY-CYLINDER-RESULT",
    date: "2026-10-11",
    protocolSha256: lock.sha256,
    rule: protocol.rule,
    schedule: protocol.schedule,
    summaries,
    gates,
    boundaryEffectFixtures: summaries.filter(s => s.boundary !== "finite-dead" && s.firstDivergence !== null).map(s => ({ fixture: s.fixture, boundary: s.boundary, firstDivergence: s.firstDivergence })),
    decisionBeforeReplay: corePass ? "BOUNDARY_RELATION_READY_FOR_REPLAY" : "INVALID_STUDY",
    claimCeiling: protocol.claim_ceiling
  };
}
function stable(value) {
  if (Array.isArray(value)) return value.map(stable);
  if (value && typeof value === "object") return Object.fromEntries(Object.keys(value).sort().map(k => [k, stable(value[k])]));
  return value;
}
const primaryCore = stable(evaluate());
const replayCore = stable(evaluate());
const pBytes = JSON.stringify(primaryCore, null, 2) + "\n";
const rBytes = JSON.stringify(replayCore, null, 2) + "\n";
const deterministicReplay = pBytes === rBytes;
const finalDecision = Object.values(primaryCore.gates).every(Boolean) && deterministicReplay ? "BOUNDED_CYLINDER_RELATION_PASS" : primaryCore.gates.boundaryEffectDetected ? "INVALID_STUDY" : "BOUNDARY_EFFECT_NOT_DETECTED";
const finish = core => stable({ ...core, gates: { ...core.gates, deterministicReplay }, decision: finalDecision });
const primary = finish(primaryCore), replay = finish(replayCore);
const primaryBytes = JSON.stringify(primary, null, 2) + "\n";
const replayBytes = JSON.stringify(replay, null, 2) + "\n";
fs.writeFileSync(path.join(out, "PRIMARY_RESULT.json"), primaryBytes);
fs.writeFileSync(path.join(out, "REPLAY_RESULT.json"), replayBytes);
fs.writeFileSync(path.join(out, "study-results.js"), `window.LIFE08_RESULT=${JSON.stringify(primary)};\n`);
const validation = {
  id: "LIFE08-VALIDATION",
  status: finalDecision === "BOUNDED_CYLINDER_RELATION_PASS" && primaryBytes === replayBytes ? "PASS" : "FAIL",
  gates: primary.gates,
  primarySha256: crypto.createHash("sha256").update(primaryBytes).digest("hex"),
  replaySha256: crypto.createHash("sha256").update(replayBytes).digest("hex")
};
fs.writeFileSync(path.join(out, "LIFE08_VALIDATION_REPORT.json"), JSON.stringify(validation, null, 2) + "\n");
console.log(`${validation.status} ${Object.values(validation.gates).filter(Boolean).length}/6 ${finalDecision}`);
if (validation.status !== "PASS") process.exit(1);
