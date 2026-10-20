const fs = require("node:fs");
const path = require("node:path");

const crystal = fs.readFileSync(path.join(__dirname, "crystal-scene.js"), "utf8");
const cylinder = fs.readFileSync(path.join(__dirname, "cylinder-comparison.js"), "utf8");
const checks = [
  ["crystal-camera-state", /cameraReady\s*=\s*false/.test(crystal)],
  ["crystal-build-preserves-camera", /applyLayout\(!cameraReady\);cameraReady=true/.test(crystal)],
  ["crystal-orbit-remains-live", /controls\.autoRotate=autoRotate/.test(crystal)],
  ["cylinder-camera-state", /cameraReady=false/.test(cylinder)],
  ["cylinder-build-preserves-camera", /if\(!cameraReady\)\{fit\(\);cameraReady=true\}/.test(cylinder)],
  ["cylinder-orbit-remains-live", /controls\.autoRotate=auto/.test(cylinder)]
];

for (const [id, pass] of checks) console.log(`${pass ? "PASS" : "FAIL"} ${id}`);
const passed = checks.filter(([, pass]) => pass).length;
console.log(`${passed === checks.length ? "PASS" : "FAIL"} ${passed}/${checks.length}`);
if (passed !== checks.length) process.exit(1);
