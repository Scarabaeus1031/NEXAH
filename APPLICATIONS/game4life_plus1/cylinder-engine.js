(function (root, factory) {
  const api = factory();
  if (typeof module === "object" && module.exports) module.exports = api;
  root.LifeCylinder = api;
}(typeof globalThis !== "undefined" ? globalThis : this, function () {
  "use strict";
  const RULE = "B3/S23";
  const MODES = Object.freeze(["finite-dead", "cylinder-x", "cylinder-y"]);
  const CHANNELS = Object.freeze(["births", "survivals", "deaths"]);
  const PATTERNS = Object.freeze({
    block: "2o$2o!",
    blinker: "3o!",
    glider: "bob$2bo$3o!",
    toad: "b3o$3o!",
    beehive: "b2o$o2bo$b2o!",
    beehiveBloom: "b2o$ob2o$b2o!",
    rPentomino: "b2o$2ob$bo!",
    acorn: "bo$3bo$2o2b3o!",
    lwss: "bo2bo$o4b$o3bo$4o!"
  });
  const key = ([x, y]) => `${x},${y}`;
  const mod = (n, m) => ((n % m) + m) % m;
  const sortCells = cells => Array.from(new Set(cells.map(key)), s => s.split(",").map(Number)).sort((a, b) => a[1] - b[1] || a[0] - b[0]);

  function makeState(size, cells, boundary = "finite-dead") {
    if (!MODES.includes(boundary)) throw new TypeError(`unknown boundary ${boundary}`);
    for (const [x, y] of cells) if (!Number.isInteger(x) || !Number.isInteger(y) || x < 0 || y < 0 || x >= size || y >= size) throw new TypeError("cell outside carrier");
    return { size, boundary, live: sortCells(cells) };
  }
  function mapCoord(x, y, size, boundary) {
    if (boundary === "cylinder-x") {
      if (y < 0 || y >= size) return null;
      return [mod(x, size), y];
    }
    if (boundary === "cylinder-y") {
      if (x < 0 || x >= size) return null;
      return [x, mod(y, size)];
    }
    if (x < 0 || y < 0 || x >= size || y >= size) return null;
    return [x, y];
  }
  function step(state) {
    const live = new Set(state.live.map(key));
    const counts = new Map();
    for (const [x, y] of state.live) for (let dy = -1; dy <= 1; dy++) for (let dx = -1; dx <= 1; dx++) {
      if (!dx && !dy) continue;
      const c = mapCoord(x + dx, y + dy, state.size, state.boundary);
      if (!c) continue;
      const k = key(c);
      counts.set(k, (counts.get(k) || 0) + 1);
    }
    const next = [];
    for (const [k, n] of counts) if (n === 3 || (n === 2 && live.has(k))) next.push(k.split(",").map(Number));
    return makeState(state.size, next, state.boundary);
  }
  function parseRLE(source) {
    const cells = []; let x = 0; let y = 0; let digits = "";
    for (const token of source) {
      if (/\d/.test(token)) { digits += token; continue; }
      const n = digits ? Number(digits) : 1; digits = "";
      if (token === "o") { for (let i = 0; i < n; i++) cells.push([x + i, y]); x += n; }
      else if (token === "b") x += n;
      else if (token === "$") { y += n; x = 0; }
      else if (token === "!") break;
    }
    return cells;
  }
  function center(cells, size) {
    const w = Math.max(...cells.map(c => c[0])) + 1, h = Math.max(...cells.map(c => c[1])) + 1;
    const ox = Math.floor((size - w) / 2), oy = Math.floor((size - h) / 2);
    return cells.map(([x, y]) => [x + ox, y + oy]);
  }
  function rng(seed) { let s = seed >>> 0; return () => ((s = (1664525 * s + 1013904223) >>> 0) + .5) / 4294967296; }
  function initial(spec, boundary) {
    if (spec.kind === "explicit") return makeState(spec.size, spec.cells, boundary);
    if (spec.kind === "pattern") return makeState(spec.size, center(parseRLE(PATTERNS[spec.pattern]), spec.size), boundary);
    const R = rng(spec.seed), cells = [];
    for (let y = 0; y < spec.size; y++) for (let x = 0; x < spec.size; x++) if (R() < spec.density) cells.push([x, y]);
    return makeState(spec.size, cells, boundary);
  }
  function eventSets(a, b) {
    const A = new Set(a.live.map(key)), B = new Set(b.live.map(key));
    return {
      births: sortCells(b.live.filter(c => !A.has(key(c)))),
      survivals: sortCells(b.live.filter(c => A.has(key(c)))),
      deaths: sortCells(a.live.filter(c => !B.has(key(c))))
    };
  }
  function components(cells, size, boundary) {
    const live = new Set(cells.map(key)), seen = new Set(); let count = 0;
    for (const start of live) {
      if (seen.has(start)) continue;
      count++; seen.add(start); const q = [start];
      while (q.length) {
        const [x, y] = q.pop().split(",").map(Number);
        for (let dy = -1; dy <= 1; dy++) for (let dx = -1; dx <= 1; dx++) {
          if (!dx && !dy) continue;
          const c = mapCoord(x + dx, y + dy, size, boundary); if (!c) continue;
          const k = key(c); if (live.has(k) && !seen.has(k)) { seen.add(k); q.push(k); }
        }
      }
    }
    return count;
  }
  function jaccard(a, b) {
    const A = new Set(a.map(key)), B = new Set(b.map(key)), U = new Set([...A, ...B]);
    if (!U.size) return 1;
    let n = 0; for (const k of A) if (B.has(k)) n++;
    return n / U.size;
  }
  function prime(n) { if (n < 2) return false; for (let d = 2; d * d <= n; d++) if (n % d === 0) return false; return true; }
  function quaternionRegister(counts) { const [b, s, d] = counts; return { scalar: b + s + d, i: b, j: s, k: d }; }
  function quaternionInverse(q) { return [q.i, q.j, q.k]; }
  function seamBirths(previous, births, boundary) {
    if (boundary === "finite-dead") return 0;
    const live = new Set(previous.live.map(key)), n = previous.size; let total = 0;
    for (const [x, y] of births) {
      const atSeam = boundary === "cylinder-x" ? (x === 0 || x === n - 1) : (y === 0 || y === n - 1);
      if (!atSeam) continue;
      let across = false;
      for (let dy = -1; dy <= 1; dy++) for (let dx = -1; dx <= 1; dx++) {
        if (!dx && !dy) continue;
        const rawAcross = boundary === "cylinder-x" ? (x + dx < 0 || x + dx >= n) : (y + dy < 0 || y + dy >= n);
        const c = mapCoord(x + dx, y + dy, n, boundary);
        if (rawAcross && c && live.has(key(c))) across = true;
      }
      if (across) total++;
    }
    return total;
  }
  function run(spec, boundary) {
    let state = initial(spec, boundary); const states = [state], rows = [];
    for (let generation = 1; generation <= spec.horizon; generation++) {
      const next = step(state), sets = eventSets(state, next), counts = CHANNELS.map(k => sets[k].length), q = quaternionRegister(counts);
      rows.push({ generation, live: next.live.length, counts, quaternion: q, components: CHANNELS.map(k => components(sets[k], spec.size, boundary)), seamBirths: seamBirths(state, sets.births, boundary), sets });
      state = next; states.push(state);
    }
    return { id: spec.id, boundary, size: spec.size, horizon: spec.horizon, states, rows };
  }
  function countReturn(rows, channel, lag = 2) {
    let hits = 0, trials = 0;
    for (let i = lag; i < rows.length; i++) { trials++; if (rows[i].counts[channel] === rows[i - lag].counts[channel]) hits++; }
    return { hits, trials, rate: trials ? hits / trials : 0 };
  }
  function spatialReturn(rows, channel, lag = 2) {
    const values = [];
    for (let i = lag; i < rows.length; i++) if (rows[i].counts[channel] === rows[i - lag].counts[channel]) values.push(jaccard(rows[i].sets[CHANNELS[channel]], rows[i - lag].sets[CHANNELS[channel]]));
    return { n: values.length, mean: values.length ? values.reduce((a, x) => a + x, 0) / values.length : null };
  }
  function translate(state, dx, dy) {
    const cells = state.live.map(([x, y]) => {
      const c = mapCoord(x + dx, y + dy, state.size, state.boundary);
      if (!c) throw new TypeError("translation left carrier"); return c;
    });
    return makeState(state.size, cells, state.boundary);
  }
  function equal(a, b) { return a.size === b.size && a.boundary === b.boundary && a.live.map(key).join(";") === b.live.map(key).join(";"); }
  return Object.freeze({ RULE, MODES, CHANNELS, PATTERNS, makeState, mapCoord, step, initial, eventSets, components, jaccard, prime, quaternionRegister, quaternionInverse, seamBirths, run, countReturn, spatialReturn, translate, equal });
}));
