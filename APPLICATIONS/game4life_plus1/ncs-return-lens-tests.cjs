const assert = require("node:assert/strict");
const N = require("./ncs-return-lens.js");

const snapshot = generation => ({
  generation,
  residual: Array.from({ length: generation % 3 }, (_, index) => ({ x: index, y: 0 })),
  audit: { uniqueEventIds: true, scalarEqualsChannels: true, inverseExact: true }
});

const zero = N.buildLens(snapshot(0));
const rootSeed = N.buildRootSeedGate();
const triplet = N.buildReturnTriplet();
assert.equal(N.gcd(6, 7), 1);
assert.equal(N.lcm(6, 7), 42);
assert.equal(N.isPrime(13), true);
assert.equal(N.nthPrime(6), 13);
assert.deepEqual(triplet.small.map(item => item.value), [17, 18, 19]);
assert.deepEqual(triplet.small.map(item => item.role), ["INPUT", "BINDER_MEDIATOR", "OUTPUT"]);
assert.deepEqual(triplet.large.map(item => item.value), [41, 42, 43]);
assert.deepEqual(triplet.large.map((item, index) => item.value - triplet.small[index].value), [24, 24, 24]);
assert.equal(triplet.offset, 24);
assert.deepEqual(triplet.doubleMirrorBridge.chain, [7, 17, 24, 42]);
assert.deepEqual(triplet.doubleMirrorBridge.increments, [10, 7, 18]);
assert.deepEqual(triplet.doubleMirrorBridge.equations, ["7+17=24", "24+18=42"]);
assert.deepEqual(triplet.doubleMirrorBridge.smallMirror, { left: 17, center: 18, right: 19 });
assert.deepEqual(triplet.doubleMirrorBridge.largeMirror, { left: 41, center: 42, right: 43 });
assert.equal(triplet.doubleMirrorBridge.smallReflectionCheck, true);
assert.equal(triplet.doubleMirrorBridge.largeReflectionCheck, true);
assert.deepEqual(triplet.doubleMirrorBridge.offsetChecks, [true, true, true]);
assert.equal(triplet.doubleMirrorBridge.twinPrimeProduct, 323);
assert.match(triplet.doubleMirrorBridge.boundary, /no physical mirror mechanism/);
assert.deepEqual(triplet.mediator42.operands, [6, 7]);
assert.equal(triplet.mediator42.gcd, 1);
assert.equal(triplet.mediator42.product, 42);
assert.equal(triplet.mediator42.lcm, 42);
assert.equal(triplet.mediator42.sum, 13);
assert.equal(triplet.mediator42.primeIndex, 6);
assert.equal(triplet.mediator42.primeValue, 13);
assert.deepEqual(triplet.mediator42.stateAfterSum, [1, 6]);
assert.deepEqual(triplet.mediator42.returnState, [0, 0]);
assert.deepEqual(rootSeed.q2, [-2, 2, 2, 2]);
assert.deepEqual(rootSeed.q3, [-8, 0, 0, 0]);
assert.deepEqual(rootSeed.q4, [-8, -8, -8, -8]);
assert.equal(rootSeed.normSquared, 4);
assert.equal(rootSeed.norm, 2);
assert.equal(N.vectorNear(rootSeed.rootISquared, [0, 1, 0, 0]), true);
assert.equal(N.vectorNear(rootSeed.reconstructedPair, [1, 1, 0, 0]), true);
assert.deepEqual(rootSeed.seeds, [{ address: "scalar", value: 1 }, { address: "i", value: 1 }]);
assert.deepEqual(rootSeed.fibonacci, [1, 1, 2, 3, 5, 8, 13]);
assert.deepEqual(rootSeed.checks, { quaternionClosure: true, rootSplit: true, addressedFibonacci: true });
assert.equal(rootSeed.passed, true);
assert.match(rootSeed.boundary, /not a prime/);
assert.equal(zero.schema, N.SCHEMA);
assert.equal(zero.sourceLensId, "NN:MRB_ACR_NCS_Q106_RETURN_CROSSWALK");
assert.deepEqual([zero.clock.pC5, zero.clock.qC5, zero.clock.c6, zero.clock.c30], [0, 0, 0, 0]);
assert.deepEqual(zero.clock.fibonacciPairMod4, [3, 1]);
assert.deepEqual([zero.counterRotation.p.slot, zero.counterRotation.q.slot], [17, 19]);
assert.deepEqual([zero.counterRotation.p.role, zero.counterRotation.q.role], ["INPUT", "OUTPUT"]);
assert.equal(zero.counterRotation.q.anchor, 19);
assert.equal(zero.counterRotation.q.tag, null);
assert.equal(zero.counterRotation.q.tagStatus, "OPEN_NO_SOURCE_TAG");
assert.equal(zero.wobble.pulse, false);
assert.equal(zero.bindingPearl.symbol, "B");
assert.equal(zero.bindingPearl.anchor, 18);
assert.equal(zero.bindingPearl.role, "BINDER_MEDIATOR");
assert.equal(zero.bindingPearl.type, "DERIVED_BOUND_PAIR_RECORD");
assert.equal(zero.bindingPearl.independentGenerator, false);
assert.deepEqual(zero.bindingPearl.pairAddress, [17, 19]);
assert.equal(zero.bindingPearl.outputAddress, 19);
assert.equal(zero.bindingPearl.legacyDeclaredTag, 36);
assert.equal(zero.bindingPearl.returnStatus, "RETURN_READY");
assert.equal(zero.bindingPearl.typeControlId, "LIFE06D_PQB_CONJUGACY_IDENTIFIABILITY_AUDIT");
assert.equal(zero.distribution4043.active.value, 40);
assert.equal(zero.distribution4043.active.role, "MEDIATOR");
assert.deepEqual(zero.distribution4043.mediatorValues, [40, 42]);
assert.deepEqual(zero.distribution4043.railValues, { euler: 41, fibonacci: 43 });

const four = N.buildLens(snapshot(4));
assert.equal(four.wobble.pulse, true);
assert.equal(four.wobble.phase, 0);
assert.equal(four.returnGate.p4FibreSize, 4);
assert.equal(four.returnGate.p4ResidualBits, 2);
assert.equal(four.returnGate.p4RoleLabels, "UNASSIGNED");
assert.equal(four.bindingPearl.p4ResidualPhase, 0);

const one = N.buildLens(snapshot(1));
assert.deepEqual([one.counterRotation.p.slot, one.counterRotation.q.slot], [29, 7]);
assert.deepEqual([one.clock.pC5, one.clock.qC5], [2, 3]);
assert.deepEqual(one.clock.fibonacciPairMod4, [1, 0]);
assert.deepEqual(one.bindingPearl.pairAddress, [29, 7]);
assert.deepEqual([one.distribution4043.active.value, one.distribution4043.active.role], [41, "EULER"]);
assert.deepEqual([N.buildLens(snapshot(2)).distribution4043.active.value, N.buildLens(snapshot(2)).distribution4043.active.role], [42, "MEDIATOR"]);
assert.deepEqual([N.buildLens(snapshot(3)).distribution4043.active.value, N.buildLens(snapshot(3)).distribution4043.active.role], [43, "FIBONACCI"]);

const hidden = N.buildReturnChallenge(one, false, null);
assert.equal(hidden.residualBits, 0);
assert.equal(hidden.sourceFibreSize, 4);
assert.deepEqual(hidden.possiblePhases, [0, 1, 2, 3]);
assert.equal(hidden.resolvedPhase, null);
assert.equal(hidden.status, "AMBIGUOUS_FIBRE_4");
const guessed = N.buildReturnChallenge(one, false, 1);
assert.equal(guessed.status, "PREDICTION_RECORDED");
const revealedMatch = N.buildReturnChallenge(one, true, 1);
assert.equal(revealedMatch.sourceFibreSize, 1);
assert.deepEqual(revealedMatch.possiblePhases, [1]);
assert.equal(revealedMatch.status, "PREDICTION_MATCH");
assert.equal(N.buildReturnChallenge(one, true, 3).status, "PREDICTION_MISMATCH");

const thirty = N.buildLens(snapshot(30));
assert.deepEqual([thirty.clock.pC5, thirty.clock.qC5, thirty.clock.c6, thirty.clock.c30], [0, 0, 0, 0]);
assert.deepEqual([thirty.counterRotation.p.slot, thirty.counterRotation.q.slot], [17, 19]);
assert.equal(thirty.returnGate.eventAddress, "EXACT");
assert.equal(thirty.returnGate.eventFibreSize, 1);
assert.equal(thirty.adapterGate.reversibleStaticBijections, 24);
assert.equal(thirty.adapterGate.operatorEquivariantAdapters, 0);
assert.equal(thirty.adapterGate.canonicalAdapter, "NULL");

const held = N.buildLens({ generation: 1, residual: [], audit: { uniqueEventIds: true } });
assert.equal(held.returnGate.eventAddress, "HOLD");
assert.equal(held.returnGate.eventFibreSize, null);
assert.equal(held.bindingPearl.returnStatus, "HOLD");
assert.equal(N.buildReturnChallenge(held, true, null).status, "HOLD");
assert.throws(() => N.buildLens({ generation: -1 }), /required/);

console.log("PASS NCS Return Lens 95/95");
