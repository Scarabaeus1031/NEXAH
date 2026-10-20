const assert = require("node:assert/strict");
const E = require("./cylinder-engine.js");
const P = require("./crystal-projection.js");

const spec = { id: "GLIDER-X-SEAM", label: "Glider X seam", kind: "explicit", size: 16, cells: [[13,1],[14,2],[12,3],[13,3],[14,3]], horizon: 24 };
const cylinder = E.run(spec, "cylinder-x");
const finite = E.run(spec, "finite-dead");
const snapshot = P.buildSnapshot(cylinder, finite, 12, { fixture: spec.label, historyWindow: 8 });

assert.equal(snapshot.schema, P.SCHEMA);
assert.equal(snapshot.firstGeneration, 5);
assert.equal(snapshot.braid.every(event => event.generation >= 5 && event.generation <= 12), true);
assert.equal(snapshot.register.scalar.length, snapshot.register.births.length + snapshot.register.survivals.length + snapshot.register.deaths.length);
assert.equal(new Set(snapshot.register.scalar).size, snapshot.register.scalar.length);
assert.equal(snapshot.audit.uniqueEventIds, true);
assert.equal(snapshot.audit.scalarEqualsChannels, true);
assert.equal(snapshot.audit.inverseExact, true);
assert.deepEqual(snapshot.rosette.map(event => event.id).sort(), snapshot.register.scalar.slice().sort());
for (const event of snapshot.rosette) {
  const inverse = P.inverseEventId(event.id);
  assert.deepEqual([inverse.generation, inverse.type, inverse.x, inverse.y], [event.generation, event.type, event.x, event.y]);
}
assert.equal(P.CHANNELS.births.symbol, "01");
assert.equal(P.CHANNELS.survivals.symbol, "11");
assert.equal(P.CHANNELS.deaths.symbol, "10");
assert.deepEqual(snapshot.residual.map(({x,y}) => [x,y]), P.symmetricDifference(cylinder.states[12].live, finite.states[12].live));
assert.equal(snapshot.register.controller.rule, "B3/S23");
assert.equal(snapshot.register.controller.boundary, "cylinder-x");
assert.match(snapshot.authority, /projection/i);
assert.equal(snapshot.finiteSource.length, finite.states[12].live.length);
assert.ok(Array.isArray(snapshot.seamCrossings));
const viewSnapshot = P.buildSnapshot(finite, finite, 12, { displayBoundary: "cylinder-x", dynamicsMode: "view" });
assert.equal(viewSnapshot.residual.length, 0);
assert.equal(viewSnapshot.seamCrossings.length, 0);
console.log("PASS LIFE//CRYSTAL 19/19");
