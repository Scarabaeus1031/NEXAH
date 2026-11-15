const fs = require('node:fs');
const path = require('node:path');

const here = __dirname;
const ecosystem = path.resolve(here, '../../../..');
const mission = path.join(ecosystem, '00 EXECUTIVE/NEXAH-Mission-Control');
const science = path.join(
  ecosystem,
  '30 SCIENCE LAB/NEXAH-Science-Lab/RESEARCH_PROGRAM_B_MATHEMATICAL_FOUNDATIONS/AXIOM0_QMODE_ORIENTATION_TO_MEASUREMENT_FOUNDATION_PACKAGE_2026-10-01/A0_BOOK'
);

let checks = 0;
function read(file) {
  checks += 1;
  if (!fs.existsSync(file)) throw new Error(`missing file: ${file}`);
  return fs.readFileSync(file, 'utf8');
}
function has(text, pattern, label) {
  checks += 1;
  if (!pattern.test(text)) throw new Error(`missing ${label}`);
}

const result = JSON.parse(read(path.join(science, 'results/a0-ullinium-methods-1-5-result-2026-11-11.json')));
checks += 1;
if (result.conclusion !== 'EQUIVALENT_RECOVERY_WITH_EXPLICIT_GOVERNANCE_OVERHEAD') {
  throw new Error('unexpected benchmark conclusion');
}

const b0Return = read(path.join(here, 'PROJECT_A0_ULLINIUM_METHODS_1_5_ENGINEERING_RETURN_2026-11-11.md'));
has(b0Return, /10,000\s*\/\s*10,000/, 'exact-run receipt');
has(b0Return, /2\.0363×/, 'payload overhead');
has(b0Return, /new graph algorithm/i, 'algorithmic non-capability');
has(b0Return, /New nodes `0`; relations `0`;\s*aliases `0`/, 'zero graph delta');

const vision = read(path.join(mission, 'CURRENT/BUILDER_VISION.md'));
has(vision, /Engineering-Prinzip · austauschbarer Kern, explizite Governance/, 'Builder Vision principle');
has(vision, /REPLACEABLE STANDARD CORE/, 'replaceable-core architecture');

const builderView = read(path.join(mission, '00_OVERVIEW/BUILDER_VIEW.md'));
has(builderView, /Methods 1–5 · Engineering-Capability und Grenze/, 'Builder View return');
has(builderView, /NO NEW CAPABILITY ID/, 'capability-id boundary');

const capabilities = read(path.join(mission, 'CURRENT/CAPABILITY_TRUTH.csv'));
has(capabilities, /bounded A0 governance-envelope return/, 'capability truth');
has(capabilities, /no reconstruction or robustness advantage over standard cospan/, 'capability limit');

const assembly = read(path.join(mission, 'CURRENT/ENGINEERING_ASSEMBLY.csv'));
has(assembly, /A0 Methods 1-5 governance envelope/, 'engineering assembly row');
has(assembly, /REUSE_AS_EXPLICIT_GOVERNANCE_ENVELOPE_NOT_AS_PRIVILEGED_CORE/, 'assembly disposition');

const architect = read(path.join(here, 'index.html'));
has(architect, /Austauschbarer Standardkern, expliziter Governance Envelope/, 'Architect vision');

const systems = read(path.join(here, 'systems-desk.html'));
has(systems, /Methods 1–5 consequence/, 'Systems consequence');
has(systems, /20 Integrationszeilen/, 'assembly count');

const build = read(path.join(here, 'build-desk.html'));
has(build, /ENGINEERING RETURN · NOT BUILD 24/, 'Build Desk boundary');

const a0Tools = read(path.join(here, 'a0-tools.html'));
has(a0Tools, /ENGINEERING CAPABILITY RETURN · 11\.11\.2026/, 'A0 Builder return');

const mcReturn = read(path.join(mission, '00_LAB_RESEARCH_DIRECTOR_DESK/RETURN_2026-11-11_A0_ULLINIUM_METHODS_1_5_BUILDER_CAPABILITY.md'));
has(mcReturn, /NO_BUILD_ACTIVATION/, 'Mission Control hold');
has(mcReturn, /New nodes\s*`0`; relations\s*`0`; aliases\s*`0`/, 'Mission Control zero graph delta');

console.log(`A0 Ullinium Methods 1–5 Builder integration: ${checks} checks PASS`);
