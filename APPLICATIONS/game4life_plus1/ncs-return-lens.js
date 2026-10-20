(function (root, factory) {
  const api = factory();
  if (typeof module === "object" && module.exports) module.exports = api;
  root.NCSReturnLens = api;

  if (typeof root.addEventListener === "function" && root.document) {
    root.addEventListener("lifecrystal:render", event => api.render(event.detail, root.document));
  }
}(typeof globalThis !== "undefined" ? globalThis : this, function () {
  "use strict";

  const SCHEMA = "nexah.game4life.ncs-return-lens.v1";
  const SOURCE_LENS_ID = "NN:MRB_ACR_NCS_Q106_RETURN_CROSSWALK";
  const BINDING_TYPE_CONTROL_ID = "LIFE06D_PQB_CONJUGACY_IDENTIFIABILITY_AUDIT";
  const FIBONACCI_PAIR_ORBIT_MOD4 = Object.freeze([[3, 1], [1, 0], [0, 1], [1, 1], [1, 2], [2, 3]].map(Object.freeze));
  const DISTRIBUTION_40_43 = Object.freeze([
    { value: 40, role: "MEDIATOR", sourceStatus: "X40_CARRIER_BOUNDARY" },
    { value: 41, role: "EULER", sourceStatus: "EXACT_MRB04_EULER_BOUNDARY" },
    { value: 42, role: "MEDIATOR", sourceStatus: "OWNER_DECLARED_TRANSFER_POSITION" },
    { value: 43, role: "FIBONACCI", sourceStatus: "OWNER_DECLARED_RAIL_DISPLAY" }
  ].map(Object.freeze));
  let residualVisible = true;
  let rootAddressesVisible = true;
  let prediction = null;
  let lastSnapshot = null;
  let lastGeneration = null;

  const mod = (value, base) => ((value % base) + base) % base;
  const wrapAddress = (value, base) => mod(value - 1, base) + 1;
  const gcd = (a, b) => {
    let x = Math.abs(a);
    let y = Math.abs(b);
    while (y) [x, y] = [y, x % y];
    return x;
  };
  const lcm = (a, b) => Math.abs(a * b) / gcd(a, b);
  function isPrime(value) {
    if (!Number.isInteger(value) || value < 2) return false;
    for (let divisor = 2; divisor * divisor <= value; divisor += 1) {
      if (value % divisor === 0) return false;
    }
    return true;
  }
  function nthPrime(index) {
    if (!Number.isInteger(index) || index < 1) throw new TypeError("prime index must be a positive integer");
    let found = 0;
    for (let candidate = 2; ; candidate += 1) {
      if (isPrime(candidate) && ++found === index) return candidate;
    }
  }

  function buildReturnTriplet() {
    const left = 6;
    const right = 7;
    const sum = left + right;
    const commonReturn = lcm(left, right);
    const smallMirror = Object.freeze({ left: 17, center: 18, right: 19 });
    const largeMirror = Object.freeze({ left: 41, center: 42, right: 43 });
    return Object.freeze({
      authority: "HUMAN_OWNER_DECLARED_DISPLAY_GRAMMAR_WITH_EXACT_ARITHMETIC_CONTROL",
      small: Object.freeze([
        Object.freeze({ value: 17, symbol: "P", role: "INPUT" }),
        Object.freeze({ value: 18, symbol: "B", role: "BINDER_MEDIATOR" }),
        Object.freeze({ value: 19, symbol: "Q", role: "OUTPUT" })
      ]),
      large: Object.freeze([
        Object.freeze({ value: 41, symbol: "E", role: "EULER" }),
        Object.freeze({ value: 42, symbol: "M", role: "MEDIATOR" }),
        Object.freeze({ value: 43, symbol: "F", role: "FIBONACCI" })
      ]),
      offset: 24,
      doubleMirrorBridge: Object.freeze({
        chain: Object.freeze([7, 17, 24, 42]),
        increments: Object.freeze([10, 7, 18]),
        equations: Object.freeze(["7+17=24", "24+18=42"]),
        smallMirror,
        largeMirror,
        smallReflectionCheck: smallMirror.left + smallMirror.right === 2 * smallMirror.center,
        largeReflectionCheck: largeMirror.left + largeMirror.right === 2 * largeMirror.center,
        offsetChecks: Object.freeze([
          smallMirror.left + 24 === largeMirror.left,
          smallMirror.center + 24 === largeMirror.center,
          smallMirror.right + 24 === largeMirror.right
        ]),
        twinPrimeProduct: smallMirror.left * smallMirror.right,
        interpretation: "7 and 17 form the additive 24 bridge; 18 then lifts the carrier to mediator 42, while +24 transports the three displayed mirror positions",
        boundary: "exact arithmetic and reflection symmetry; no physical mirror mechanism or canonical NCS transport is inferred"
      }),
      mediator42: Object.freeze({
        operands: Object.freeze([left, right]),
        gcd: gcd(left, right),
        product: left * right,
        lcm: commonReturn,
        sum,
        primeIndex: left,
        primeValue: nthPrime(left),
        stateAfterSum: Object.freeze([mod(sum, left), mod(sum, right)]),
        returnState: Object.freeze([mod(commonReturn, left), mod(commonReturn, right)]),
        interpretation: "product/lcm is the joint return period; sum is an additive prime-index readout, not a causal prime selector"
      }),
      boundary: "the +24 crosswalk and role names are display semantics; exact arithmetic does not establish NCS transport or physical causality"
    });
  }

  function quaternionMultiply(a, b) {
    return Object.freeze([
      a[0] * b[0] - a[1] * b[1] - a[2] * b[2] - a[3] * b[3],
      a[0] * b[1] + a[1] * b[0] + a[2] * b[3] - a[3] * b[2],
      a[0] * b[2] - a[1] * b[3] + a[2] * b[0] + a[3] * b[1],
      a[0] * b[3] + a[1] * b[2] - a[2] * b[1] + a[3] * b[0]
    ]);
  }

  function vectorNear(a, b, tolerance = 1e-12) {
    return a.length === b.length && a.every((value, index) => Math.abs(value - b[index]) <= tolerance);
  }

  function buildRootSeedGate() {
    const q = Object.freeze([1, 1, 1, 1]);
    const q2 = quaternionMultiply(q, q);
    const q3 = quaternionMultiply(q2, q);
    const q4 = quaternionMultiply(q3, q);
    const rootI = Object.freeze([Math.SQRT1_2, Math.SQRT1_2, 0, 0]);
    const rootISquared = quaternionMultiply(rootI, rootI);
    const reconstructedPair = Object.freeze(rootI.map(value => value * Math.SQRT2));
    const fibonacci = Object.freeze([1, 1, 2, 3, 5, 8, 13]);
    const checks = Object.freeze({
      quaternionClosure: vectorNear(q3, [-8, 0, 0, 0]) && vectorNear(q4, [-8, -8, -8, -8]),
      rootSplit: vectorNear(rootISquared, [0, 1, 0, 0]) && vectorNear(reconstructedPair, [1, 1, 0, 0]),
      addressedFibonacci: fibonacci[0] === fibonacci[1] && "scalar" !== "i" && fibonacci[2] === fibonacci[0] + fibonacci[1]
    });
    return Object.freeze({
      authority: "FORMAL_LOCAL_DERIVATION_OVER_REUSED_SOURCE_IDENTITIES",
      q, q2, q3, q4,
      normSquared: q.reduce((sum, value) => sum + value * value, 0),
      norm: Math.sqrt(q.reduce((sum, value) => sum + value * value, 0)),
      rootI, rootISquared, reconstructedPair,
      seeds: Object.freeze([{ address: "scalar", value: 1 }, { address: "i", value: 1 }].map(Object.freeze)),
      fibonacci,
      checks,
      passed: Object.values(checks).every(Boolean),
      status: "PASS_FORMAL_IDENTITIES_ADDRESS_SEPARATION_TRANSPORT_OPEN",
      boundary: "1 remains the multiplicative identity, not a prime; Fibonacci-to-X40 transport and historical physical mechanism remain unestablished"
    });
  }

  function buildLens(snapshot) {
    if (!snapshot || !Number.isInteger(snapshot.generation) || snapshot.generation < 0) {
      throw new TypeError("an addressed LIFE snapshot with a non-negative generation is required");
    }
    const generation = snapshot.generation;
    const c6 = mod(generation, 6);
    const audits = snapshot.audit || {};
    const exactEventReturn = Boolean(audits.uniqueEventIds && audits.scalarEqualsChannels && audits.inverseExact);

    const pSlot = wrapAddress(17 + 12 * generation, 30);
    const qSlot = wrapAddress(19 + 18 * generation, 30);
    const p4Phase = mod(generation, 4);
    const returnTriplet = buildReturnTriplet();
    return {
      schema: SCHEMA,
      authority: "non-evidentiary view adapter over an authoritative addressed LIFE snapshot",
      sourceLensId: SOURCE_LENS_ID,
      generation,
      clock: {
        pC5: mod(2 * generation, 5),
        qC5: mod(-2 * generation, 5),
        c6,
        c30: mod(generation, 30),
        fibonacciPairMod4: FIBONACCI_PAIR_ORBIT_MOD4[c6],
        construction: "joint order-five C5 counter-step and six-state Fibonacci pair orbit; no transport to X20 or X40"
      },
      counterRotation: {
        p: { anchor: 17, role: "INPUT", tag: 29, stepC30: 12, stepC5: 2, slot: pSlot },
        q: { anchor: 19, role: "OUTPUT", tag: null, tagStatus: "OPEN_NO_SOURCE_TAG", stepC30: 18, signedStepC30: -12, stepC5: -2, slot: qSlot },
        interpretation: "owner-declared P input / Q output counter-rotation; no LIFE operator identity"
      },
      wobble: {
        phase: p4Phase,
        pulse: generation > 0 && mod(generation, 4) === 0,
        interpretation: "full mod-4 phase retained; every-four pulse alone is insufficient for Return"
      },
      bindingPearl: {
        symbol: "B",
        anchor: 18,
        role: "BINDER_MEDIATOR",
        type: "DERIVED_BOUND_PAIR_RECORD",
        independentGenerator: false,
        pairAddress: Object.freeze([pSlot, qSlot]),
        outputAddress: qSlot,
        legacyDeclaredTag: 36,
        c30Address: mod(generation, 30),
        p4ResidualPhase: p4Phase,
        returnStatus: exactEventReturn ? "RETURN_READY" : "HOLD",
        typeControlId: BINDING_TYPE_CONTROL_ID,
        interpretation: "B is the addressed mediator at 18 and binds P input to Q output; LIFE06D supplies a non-identity type control, not a scale-conjugacy claim"
      },
      returnTriplet,
      distribution4043: {
        authority: "OWNER_DECLARED_DISPLAY_SEMANTICS",
        phase: p4Phase,
        active: DISTRIBUTION_40_43[p4Phase],
        stations: DISTRIBUTION_40_43,
        mediatorValues: Object.freeze([40, 42]),
        railValues: Object.freeze({ euler: 41, fibonacci: 43 }),
        exactSourceBoundary: "41 reuses MRB-04 and the Euler-41 residual-switch audit",
        openTransport: "43/Fibonacci is a display assignment; typed Fibonacci-to-X40 transport remains null"
      },
      returnGate: {
        eventAddress: exactEventReturn ? "EXACT" : "HOLD",
        eventFibreSize: exactEventReturn ? 1 : null,
        p4FibreSize: 4,
        p4ResidualBits: 2,
        p4RoleLabels: "UNASSIGNED",
        boundaryResidualCells: Array.isArray(snapshot.residual) ? snapshot.residual.length : null
      },
      adapterGate: {
        reversibleStaticBijections: 24,
        operatorEquivariantAdapters: 0,
        canonicalAdapter: "NULL",
        q106Binding: "UNAVAILABLE_WITHOUT_X20_ADJACENCY",
        interpretation: "address comparison is available; semantic role fusion is not"
      }
    };
  }

  function buildReturnChallenge(lens, includeResidual, selectedPrediction) {
    const phase = lens.wobble.phase;
    const possiblePhases = includeResidual ? [phase] : [0, 1, 2, 3];
    let status = includeResidual ? "UNIQUE_RETURN" : "AMBIGUOUS_FIBRE_4";
    if (lens.returnGate.eventAddress !== "EXACT") status = "HOLD";
    else if (includeResidual && Number.isInteger(selectedPrediction)) {
      status = selectedPrediction === phase ? "PREDICTION_MATCH" : "PREDICTION_MISMATCH";
    } else if (!includeResidual && Number.isInteger(selectedPrediction)) {
      status = "PREDICTION_RECORDED";
    }
    return Object.freeze({
      includeResidual,
      residualBits: includeResidual ? 2 : 0,
      sourceFibreSize: possiblePhases.length,
      possiblePhases: Object.freeze(possiblePhases),
      resolvedPhase: includeResidual ? phase : null,
      prediction: Number.isInteger(selectedPrediction) ? selectedPrediction : null,
      status
    });
  }

  function setText(document, id, value) {
    const element = document.getElementById(id);
    if (element) element.textContent = String(value);
  }

  function bindControls(document) {
    const toggle = document.getElementById("ncsResidualToggle");
    if (toggle && !toggle.dataset.ncsBound) {
      toggle.dataset.ncsBound = "true";
      toggle.checked = residualVisible;
      toggle.onchange = () => {
        residualVisible = Boolean(toggle.checked);
        if (lastSnapshot) render(lastSnapshot, document);
      };
    }
    const rootToggle = document.getElementById("rootSeedAddressToggle");
    if (rootToggle && !rootToggle.dataset.ncsBound) {
      rootToggle.dataset.ncsBound = "true";
      rootToggle.checked = rootAddressesVisible;
      rootToggle.onchange = () => {
        rootAddressesVisible = Boolean(rootToggle.checked);
        if (lastSnapshot) render(lastSnapshot, document);
      };
    }
    if (typeof document.querySelectorAll === "function") {
      document.querySelectorAll("[data-ncs-candidate]").forEach(button => {
        if (button.dataset.ncsBound) return;
        button.dataset.ncsBound = "true";
        button.onclick = () => {
          prediction = Number(button.dataset.ncsCandidate);
          if (lastSnapshot) render(lastSnapshot, document);
        };
      });
    }
  }

  function renderChallenge(lens, document) {
    const challenge = buildReturnChallenge(lens, residualVisible, prediction);
    setText(document, "ncsChallengeMode", challenge.includeResidual ? "RESIDUAL RETAINED · 2 BITS" : "RESIDUAL HIDDEN · 0 BITS");
    const labels = {
      UNIQUE_RETURN: "UNIQUE RETURN",
      AMBIGUOUS_FIBRE_4: "FOUR SOURCES REMAIN",
      PREDICTION_RECORDED: "PREDICTION STORED",
      PREDICTION_MATCH: "MATCH · SOURCE RECOVERED",
      PREDICTION_MISMATCH: "MISMATCH · DISPLAY WAS INSUFFICIENT",
      HOLD: "HOLD · SNAPSHOT AUDIT INCOMPLETE"
    };
    setText(document, "ncsChallengeStatus", labels[challenge.status]);
    const explanations = {
      UNIQUE_RETURN: "Two retained bits select one source phase from the four-state fibre.",
      AMBIGUOUS_FIBRE_4: "The same visible class admits phases 0, 1, 2 and 3; display alone does not identify the source.",
      PREDICTION_RECORDED: `Phase ${challenge.prediction} is recorded as a guess. Reveal the residual to test it.`,
      PREDICTION_MATCH: `Phase ${challenge.prediction} matches the retained residual.`,
      PREDICTION_MISMATCH: `Phase ${challenge.prediction} does not match phase ${challenge.resolvedPhase}; the hidden residual carried the distinction.`,
      HOLD: "The addressed LIFE snapshot has not passed its inverse audit, so the adapter remains closed."
    };
    setText(document, "ncsChallengeExplanation", explanations[challenge.status]);
    setText(document, "ncsFibre", `${challenge.sourceFibreSize} state${challenge.sourceFibreSize === 1 ? "" : "s"}`);
    if (typeof document.querySelectorAll === "function") {
      document.querySelectorAll("[data-ncs-candidate]").forEach(button => {
        const value = Number(button.dataset.ncsCandidate);
        if (!button.classList) return;
        button.classList.toggle("possible", challenge.possiblePhases.includes(value));
        button.classList.toggle("resolved", challenge.includeResidual && value === challenge.resolvedPhase);
        button.classList.toggle("excluded", challenge.includeResidual && value !== challenge.resolvedPhase);
        button.classList.toggle("predicted", challenge.prediction === value);
        button.setAttribute("aria-pressed", String(challenge.prediction === value));
      });
    }
    return challenge;
  }

  function renderDistribution(lens, document) {
    const distribution = lens.distribution4043;
    setText(document, "ncsDistributionPhase", `phase ${distribution.phase} / 4`);
    setText(document, "ncsDistributionActive", `${distribution.active.value} · ${distribution.active.role}`);
    const explanations = {
      40: "40 is the first mediator: the X40 carrier boundary before the Euler handoff.",
      41: "41 is the sourced Euler boundary: MRB-04 records the exact +1 / residual-switch handoff.",
      42: "42 is the second mediator: a declared transfer position between the two rails.",
      43: "43 is the declared Fibonacci rail display. Its typed transport to X40 remains open."
    };
    setText(document, "ncsDistributionExplanation", explanations[distribution.active.value]);
    const triplet = lens.returnTriplet;
    const mediator = triplet.mediator42;
    const bridge = triplet.doubleMirrorBridge;
    setText(document, "ncsBridgeChain", bridge.chain.join(" → "));
    setText(document, "ncsBridgeEquationA", bridge.equations[0]);
    setText(document, "ncsBridgeEquationB", bridge.equations[1]);
    setText(document, "ncsSmallMirror", `${bridge.smallMirror.left} ← ${bridge.smallMirror.center} → ${bridge.smallMirror.right}`);
    setText(document, "ncsLargeMirror", `${bridge.largeMirror.left} ← ${bridge.largeMirror.center} → ${bridge.largeMirror.right}`);
    setText(document, "ncsMirrorProof", `${bridge.smallMirror.left}+${bridge.smallMirror.right}=2×${bridge.smallMirror.center} · ${bridge.largeMirror.left}+${bridge.largeMirror.right}=2×${bridge.largeMirror.center}`);
    setText(document, "ncsMediatorProduct", `${mediator.operands[0]} × ${mediator.operands[1]} = ${mediator.product} = lcm(${mediator.operands.join(",")})`);
    setText(document, "ncsMediatorSum", `${mediator.operands[0]} + ${mediator.operands[1]} = ${mediator.sum} = p₆`);
    setText(document, "ncsMediatorState", `T¹³(0,0)=(${mediator.stateAfterSum.join(",")}) · T⁴²(0,0)=(${mediator.returnState.join(",")})`);
    if (typeof document.querySelectorAll === "function") {
      document.querySelectorAll("[data-ncs-station]").forEach(station => {
        if (station.classList) station.classList.toggle("active", Number(station.dataset.ncsStation) === distribution.active.value);
      });
    }
    return distribution;
  }

  function renderRootSeedGate(document) {
    const gate = buildRootSeedGate();
    const addressed = ["1₁", "1ᵢ", "1ⱼ", "1ₖ"];
    const collapsed = ["1", "1", "1", "1"];
    const labels = rootAddressesVisible ? addressed : collapsed;
    ["rootSeedScalar", "rootSeedI", "rootSeedJ", "rootSeedK"].forEach((id, index) => setText(document, id, labels[index]));
    setText(document, "rootSeedStatus", rootAddressesVisible ? "3/3 PASS · ADDRESSES RETAINED" : "VALUE VIEW · ADDRESSES HIDDEN");
    setText(document, "rootSeedFibSeeds", rootAddressesVisible ? "1₁, 1ᵢ → 2" : "1, 1 → 2");
    setText(document, "rootSeedExplanation", rootAddressesVisible
      ? "The repeated coefficient is recoverable because its basis address is retained. Fibonacci accepts two equal-valued seeds as distinct ordered inputs."
      : "All four coefficients now look identical. Their values survive, but the source basis cannot be reconstructed from this view alone.");
    const addressRow = document.querySelector && document.querySelector(".root-seed-addresses");
    if (addressRow && addressRow.classList) addressRow.classList.toggle("collapsed", !rootAddressesVisible);
    return Object.freeze({ gate, addressesVisible: rootAddressesVisible });
  }

  function render(snapshot, document) {
    const lens = buildLens(snapshot);
    if (lastGeneration !== null && lastGeneration !== lens.generation) prediction = null;
    lastGeneration = lens.generation;
    lastSnapshot = snapshot;
    bindControls(document);
    setText(document, "ncsGeneration", `g${lens.generation}`);
    setText(document, "ncsC5", `${lens.clock.pC5} / ${lens.clock.qC5}`);
    setText(document, "ncsC6", lens.clock.c6);
    setText(document, "ncsC30", lens.clock.c30);
    setText(document, "ncsFib", `(${lens.clock.fibonacciPairMod4.join(",")})`);
    setText(document, "ncsP", lens.counterRotation.p.slot);
    setText(document, "ncsQ", lens.counterRotation.q.slot);
    setText(document, "ncsB", lens.bindingPearl.anchor);
    setText(document, "ncsBMeta", `P ${lens.bindingPearl.pairAddress[0]} ↔ Q ${lens.bindingPearl.pairAddress[1]} · P4 ${lens.bindingPearl.p4ResidualPhase}`);
    setText(document, "ncsBStatus", lens.bindingPearl.returnStatus === "RETURN_READY" ? "BOUND · RETURN READY" : "BOUND · HOLD");
    setText(document, "ncsWobble", lens.wobble.pulse ? `PULSE · phase ${lens.wobble.phase}` : `phase ${lens.wobble.phase}`);
    setText(document, "ncsResidual", lens.returnGate.boundaryResidualCells == null ? "—" : lens.returnGate.boundaryResidualCells);
    setText(document, "ncsReturn", `${lens.returnGate.eventAddress} · fibre ${lens.returnGate.eventFibreSize ?? "?"}`);
    setText(document, "ncsAdapter", `${lens.adapterGate.operatorEquivariantAdapters} equivariant · ${lens.adapterGate.canonicalAdapter}`);
    const pearl = document.getElementById("ncsPearl");
    if (pearl) pearl.dataset.state = lens.bindingPearl.returnStatus === "RETURN_READY" ? "exact" : "hold";
    const challenge = renderChallenge(lens, document);
    const distribution = renderDistribution(lens, document);
    const rootSeed = renderRootSeedGate(document);
    setText(document, "ncsProof", lens.returnGate.eventAddress === "EXACT"
      ? `P ${lens.counterRotation.p.slot} enters B 18 and returns as Q ${lens.counterRotation.q.slot}. Event inverse is exact; P4 Return is ${challenge.sourceFibreSize === 1 ? "resolved by the retained 2-bit residual" : "ambiguous across four source phases"}.`
      : "Snapshot audit incomplete: adapter remains closed.");
    const p = document.getElementById("ncsPNeedle");
    const q = document.getElementById("ncsQNeedle");
    if (p) p.style.transform = `rotate(${lens.counterRotation.p.slot * 12}deg)`;
    if (q) q.style.transform = `rotate(${-lens.counterRotation.q.slot * 12}deg)`;
    return Object.freeze({ lens, challenge, distribution, rootSeed });
  }

  return Object.freeze({ SCHEMA, SOURCE_LENS_ID, BINDING_TYPE_CONTROL_ID, FIBONACCI_PAIR_ORBIT_MOD4, DISTRIBUTION_40_43, mod, wrapAddress, gcd, lcm, isPrime, nthPrime, buildReturnTriplet, quaternionMultiply, vectorNear, buildRootSeedGate, buildLens, buildReturnChallenge, renderDistribution, renderRootSeedGate, render });
}));
