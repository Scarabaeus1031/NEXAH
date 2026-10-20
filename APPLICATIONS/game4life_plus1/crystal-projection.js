(function (root, factory) {
  const api = factory();
  if (typeof module === "object" && module.exports) module.exports = api;
  root.LifeCrystalProjection = api;
}(typeof globalThis !== "undefined" ? globalThis : this, function () {
  "use strict";

  const SCHEMA = "nexah.life-crystal.observatory-projection.v1";
  const CHANNELS = Object.freeze({
    births: Object.freeze({ symbol: "01", slot: "i", phase: 90, label: "BIRTH" }),
    survivals: Object.freeze({ symbol: "11", slot: "j", phase: 0, label: "SURVIVE" }),
    deaths: Object.freeze({ symbol: "10", slot: "k", phase: -90, label: "DEATH" })
  });
  const pad = (value, width) => String(value).padStart(width, "0");
  const cellKey = cell => `${cell[0]},${cell[1]}`;

  function eventId(runId, boundary, generation, type, x, y) {
    const channel = CHANNELS[type];
    if (!channel) throw new TypeError(`unknown event type ${type}`);
    return `${runId}|${boundary}|g${pad(generation, 4)}|${channel.symbol}|x${pad(x, 3)}|y${pad(y, 3)}`;
  }

  function inverseEventId(id) {
    const match = /^(.*)\|([^|]+)\|g(\d+)\|(01|11|10)\|x(\d+)\|y(\d+)$/.exec(id);
    if (!match) throw new TypeError(`invalid event id ${id}`);
    const type = Object.keys(CHANNELS).find(key => CHANNELS[key].symbol === match[4]);
    return { runId: match[1], boundary: match[2], generation: Number(match[3]), type, symbol: match[4], x: Number(match[5]), y: Number(match[6]) };
  }

  function eventsForRow(run, generation) {
    if (!generation) return [];
    const row = run.rows[generation - 1], events = [];
    for (const [type, channel] of Object.entries(CHANNELS)) {
      for (const [x, y] of row.sets[type]) events.push({
        id: eventId(run.id, run.boundary, generation, type, x, y),
        type, symbol: channel.symbol, slot: channel.slot, phase: channel.phase,
        generation, x, y
      });
    }
    return events;
  }

  function symmetricDifference(a, b) {
    const A = new Set(a.map(cellKey)), B = new Set(b.map(cellKey)), out = [];
    for (const cell of a) if (!B.has(cellKey(cell))) out.push(cell);
    for (const cell of b) if (!A.has(cellKey(cell))) out.push(cell);
    return out;
  }

  function seamCrossingBirths(run, generation) {
    if (!generation || run.boundary === "finite-dead") return [];
    const previous = new Set(run.states[generation - 1].live.map(cellKey)), births = run.rows[generation - 1].sets.births, size = run.size, out = [];
    const mod = value => ((value % size) + size) % size;
    for (const [x, y] of births) {
      const atSeam = run.boundary === "cylinder-x" ? x === 0 || x === size - 1 : y === 0 || y === size - 1;
      if (!atSeam) continue;
      let across = false;
      for (let dy = -1; dy <= 1; dy++) for (let dx = -1; dx <= 1; dx++) {
        if (!dx && !dy) continue;
        const rawAcross = run.boundary === "cylinder-x" ? x + dx < 0 || x + dx >= size : y + dy < 0 || y + dy >= size;
        const mapped = run.boundary === "cylinder-x" ? [mod(x + dx), y + dy] : [x + dx, mod(y + dy)];
        if (rawAcross && mapped[0] >= 0 && mapped[1] >= 0 && mapped[0] < size && mapped[1] < size && previous.has(cellKey(mapped))) across = true;
      }
      if (across) out.push({ x, y, generation, id: eventId(run.id, run.boundary, generation, "births", x, y) });
    }
    return out;
  }

  function buildSnapshot(run, finiteRun, generation, options = {}) {
    if (!run || !finiteRun || run.size !== finiteRun.size) throw new TypeError("comparable runs required");
    if (!Number.isInteger(generation) || generation < 0 || generation > run.horizon) throw new RangeError("generation outside run");
    const historyWindow = options.historyWindow === "all" ? generation : Math.max(1, Number(options.historyWindow) || 60);
    const firstGeneration = Math.max(1, generation - historyWindow + 1);
    const events = eventsForRow(run, generation);
    const history = [];
    for (let g = firstGeneration; g <= generation; g++) history.push(...eventsForRow(run, g));
    const byType = Object.fromEntries(Object.keys(CHANNELS).map(type => [type, events.filter(event => event.type === type)]));
    const residual = symmetricDifference(run.states[generation].live, finiteRun.states[generation].live).map(([x, y]) => ({ x, y, generation }));
    const ids = new Set(events.map(event => event.id));
    return {
      schema: SCHEMA,
      authority: "registered Life run; observatory and GLB are reversible projections",
      runId: run.id,
      fixture: options.fixture || run.id,
      rule: "B3/S23",
      boundary: run.boundary,
      generation,
      size: run.size,
      historyWindow,
      firstGeneration,
      source: run.states[generation].live.map(([x, y]) => ({ x, y, generation })),
      finiteSource: finiteRun.states[generation].live.map(([x, y]) => ({ x, y, generation })),
      register: {
        scalar: events.map(event => event.id),
        births: byType.births,
        survivals: byType.survivals,
        deaths: byType.deaths,
        controller: { rule: "B3/S23", boundary: run.boundary, generation, fixture: options.fixture || run.id }
      },
      rosette: events,
      braid: history,
      residual,
      seamCrossings: seamCrossingBirths(run, generation),
      displayBoundary: options.displayBoundary || run.boundary,
      dynamicsMode: options.dynamicsMode || (run.boundary === "finite-dead" ? "view" : "dynamics"),
      audit: {
        uniqueEventIds: ids.size === events.length,
        scalarEqualsChannels: events.length === byType.births.length + byType.survivals.length + byType.deaths.length,
        inverseExact: events.every(event => {
          const inverse = inverseEventId(event.id);
          return inverse.generation === event.generation && inverse.type === event.type && inverse.x === event.x && inverse.y === event.y;
        })
      }
    };
  }

  return Object.freeze({ SCHEMA, CHANNELS, eventId, inverseEventId, eventsForRow, symmetricDifference, seamCrossingBirths, buildSnapshot });
}));
