# MITOSIS ORIENTATION NEIGHBORHOOD

## Research boundary

This directional neighborhood is constructed only from Wikipedia revision `1359310650`, the completed Mitosis Translation, and its Reflection. It is not an ontology, biological pathway, universal phase model, comparison, Atlas, or merged graph.

## Admission rules

A node is admitted only when the fixed source develops it enough to answer the local orientation questions. An edge requires an exact local predicate, direction, source code, support class, scale, confidence, reverse status, and prohibited inference. Temporal adjacency alone is insufficient.

## Node register

| ID | Local label | Local role | Source | Scale | Status / reason | Uncertainty and prohibited inference |
|---|---|---|---|---|---|---|
| M-N01 | Mitosis | focal process | LEAD, OV, PRO–TELO | cellular/process | admitted; source focal subject | not every form follows one geometry |
| M-N02 | replicated chromosome set | prerequisite state | LEAD, OV | molecular/cellular | admitted; source places duplication before Mitosis | not a full Interphase model |
| M-N03 | sister chromatids | structural relation | OV, PRO, ANA | molecular | admitted; source names paired chromatids | identity across names remains compressed |
| M-N04 | Prophase | phase landmark | PRO | cellular/process time | admitted; developed section | not one state or single event |
| M-N05 | chromosome condensation | state-change event | OV, PRO | molecular/subcellular | admitted; explicit event | not sufficient cause of progression |
| M-N06 | mitotic spindle | structural system | PRO–ANA | subcellular | admitted; repeated local mechanism | centrosomes are not universal prerequisites |
| M-N07 | Prometaphase | phase landmark | PROM | cellular/process time | admitted; developed section | open/closed boundary varies |
| M-N08 | nuclear-envelope configuration | boundary state | OV, PROM, TELO, VAR | subcellular | admitted; intact/broken/reformed distinctions | no universal breakdown |
| M-N09 | kinetochore attachment | attachment event | PROM, META | molecular/subcellular | admitted; explicit relation | attachment alone does not guarantee outcome |
| M-N10 | Metaphase | phase landmark | META | cellular/process time | admitted; developed section | not identical to alignment alone |
| M-N11 | metaphase plate/alignment | spatial arrangement | META | subcellular | admitted; explicit spatial account | “plate” is an imaginary alignment line, not an object ontology |
| M-N12 | metaphase checkpoint | continuation condition | META, ERR | molecular/subcellular | admitted; source links to proceeding | control network incomplete; no guarantee |
| M-N13 | Anaphase | phase landmark | ANA | cellular/process time | admitted; developed section | A/B suborder varies |
| M-N14 | cohesin cleavage | separation event | ANA | molecular | admitted; explicit event | not complete causal account |
| M-N15 | daughter chromosomes | transformed/named chromosome sets | ANA | molecular/subcellular | admitted; source renames separated chromatids | formal identity theory absent |
| M-N16 | opposite cell ends | spatial destination | OV, ANA | cellular | admitted; explicit movement destination | destination is not a causal actor |
| M-N17 | Telophase | phase landmark | TELO | cellular/process time | admitted; developed section | completion of Mitosis not always cell division |
| M-N18 | daughter nuclei | local result | LEAD, OV, TELO | cellular/subcellular | admitted; primary mitotic result | not equivalent to daughter cells |
| M-N19 | Cytokinesis | adjacent separate process | OV, CYTO | cellular/process | admitted; source explicitly separates it | not a phase of Mitosis; may be absent |
| M-N20 | daughter cells | cell-division outcome | LEAD, CYTO | cellular | admitted; source outcome when division completes | not guaranteed by Mitosis alone |
| M-N21 | open/closed/semi-open forms | variation class | LEAD, PROM, VAR | cellular/subcellular | admitted; source classifies envelope behavior | not a universal ontology |
| M-N22 | Mitosis without Cytokinesis | decoupled outcome | OV, CYTO, ERR | cellular | admitted; explicit multinucleate/coenocytic cases | not necessarily error in every context |
| M-N23 | nondisjunction | separation error | ERR | molecular/cellular | admitted; explicit failure of separation | not every error or disease cause |
| M-N24 | unequal chromosome complements | error outcome | ERR | cellular | admitted; trisomy/monosomy examples | no organismal prognosis |
| M-N25 | anaphase lag | movement error | ERR | subcellular/cellular | admitted; explicit source case | cause and frequency incomplete |
| M-N26 | tripolar/multipolar mitosis | spindle/division error form | LEAD, ERR | cellular | admitted; explicit source case | not all atypical division |
| M-N27 | more than two daughter cells | abnormal numerical outcome | LEAD, ERR | cellular | admitted; explicit outcome | viability/disease not inferred |

All 27 nodes are admitted from the fixed source. Their local roles remain heterogeneous; they are not normalized into one node class.

## Edge register

All admitted edges have **Direct Source Support**. Reverse status tests the exact inverse relation.

| ID | From → To | Exact predicate | Direction | Source | Support | Scale | Confidence | Reverse | Prohibited inference |
|---|---|---|---|---|---|---|---|---|---|
| M-E01 | N02 → N01 | replicated chromosome state precedes Mitosis | prerequisite→process | LEAD, OV | Direct Source Support | cellular time | high | unsupported | Mitosis causes prior replication |
| M-E02 | N02 → N03 | replicated chromosomes contain paired sister chromatids | whole→parts | OV | Direct Source Support | molecular | high | supported | chromatids are separate daughter chromosomes already |
| M-E03 | N01 → N04 | Mitosis includes Prophase as a named phase | process→phase | LEAD, PRO | Direct Source Support | process | high | supported | Prophase contains all of Mitosis |
| M-E04 | N04 → N05 | Prophase includes chromosome condensation | phase→event | PRO | Direct Source Support | subcellular | high | supported | condensation alone defines Prophase |
| M-E05 | N04 → N06 | Prophase initiates spindle formation in the described account | phase→structure formation | PRO | Direct Source Support | subcellular | high | supported | centrosome dependence is universal |
| M-E06 | N04 → N07 | source orders Prophase before Prometaphase | temporal precedence | LEAD, PRO, PROM | Direct Source Support | process time | high | supported | precedence supplies causality |
| M-E07 | N07 → N08 | Prometaphase changes nuclear-envelope configuration in open Mitosis | phase→boundary event | PROM | Direct Source Support | subcellular | medium | unsupported | all Mitosis opens the envelope |
| M-E08 | N07 → N09 | Prometaphase includes kinetochore attachment | phase→event | PROM | Direct Source Support | molecular/subcellular | high | supported | attachment is instantly complete |
| M-E09 | N07 → N10 | source orders Prometaphase before Metaphase | temporal precedence | PROM, META | Direct Source Support | process time | high | supported | precedence supplies causality |
| M-E10 | N09 → N11 | attachment and resulting tension contribute to alignment | event→spatial arrangement | PROM, META | Direct Source Support | subcellular | medium | unresolved | alignment proves every attachment is correct |
| M-E11 | N10 → N11 | Metaphase is characterized by alignment at the metaphase plate | phase→spatial state | META | Direct Source Support | subcellular | high | supported | plate is a material boundary |
| M-E12 | N10 → N12 | Metaphase contains the represented checkpoint boundary | phase→condition | META | Direct Source Support | molecular/subcellular | medium | supported | one checkpoint explains all control |
| M-E13 | N12 → N13 | successful checkpoint passage permits progression to Anaphase in the source | condition→continuation | META | Direct Source Support | process transition | medium | unsupported | permission guarantees normal completion |
| M-E14 | N10 → N13 | source orders Metaphase before Anaphase | temporal precedence | META, ANA | Direct Source Support | process time | high | supported | sequence alone is causal |
| M-E15 | N13 → N14 | Anaphase includes cohesin cleavage | phase→event | ANA | Direct Source Support | molecular | high | supported | cleavage explains all movement |
| M-E16 | N14 → N15 | cohesin cleavage forms separated daughter chromosomes in the source account | transformation | ANA | Direct Source Support | molecular | high | not meaningful | daughter chromosomes cause prior cleavage |
| M-E17 | N13 → N16 | Anaphase moves daughter chromosomes toward opposite cell ends | phase/event→destination | OV, ANA | Direct Source Support | cellular | high | unsupported | destinations cause movement |
| M-E18 | N13 → N17 | source orders Anaphase before Telophase | temporal precedence | ANA, TELO | Direct Source Support | process time | high | supported | sequence alone is causal |
| M-E19 | N17 → N18 | Telophase reconstructs envelopes around chromosome sets, forming daughter nuclei | boundary reconstruction→result | TELO | Direct Source Support | subcellular/cellular | high | not meaningful | nuclei reverse Telophase |
| M-E20 | N01 → N19 | Mitosis may coordinate with the separate process Cytokinesis | process adjacency | LEAD, OV, CYTO | Direct Source Support | cellular/process | high | unresolved | Cytokinesis is a mitotic phase |
| M-E21 | N13 → N19 | Cytokinesis may begin after Anaphase onset | temporal relation | OV, CYTO | Direct Source Support | process time | medium | unresolved | every Cytokinesis proves a particular Anaphase state |
| M-E22 | N19 → N20 | Cytokinesis divides cellular material to produce daughter cells | process→outcome | CYTO | Direct Source Support | cellular | high | not meaningful | daughter cells cause Cytokinesis |
| M-E23 | N01 → N21 | Mitosis has open, closed, and semi-open forms | process→variation class | LEAD, PROM, VAR | Direct Source Support | cellular/subcellular | high | supported | three labels exhaust all variation |
| M-E24 | N21 → N08 | forms are classified partly by nuclear-envelope behavior | class→boundary criterion | VAR | Direct Source Support | subcellular | high | supported | envelope state is the only criterion |
| M-E25 | N01 → N22 | Mitosis may occur without Cytokinesis | process→decoupled outcome | OV, CYTO | Direct Source Support | cellular | high | not meaningful | absence of Cytokinesis is always pathological |
| M-E26 | N01 → N23 | Mitosis can exhibit nondisjunction | process→error | ERR | Direct Source Support | cellular | high | supported | all mitotic errors are nondisjunction |
| M-E27 | N23 → N24 | nondisjunction can produce unequal chromosome complements | error→outcome | ERR | Direct Source Support | cellular | high | unsupported | every unequal complement proves nondisjunction |
| M-E28 | N01 → N25 | Mitosis can exhibit anaphase lag | process→error | ERR | Direct Source Support | subcellular/cellular | high | supported | lag explains every chromosome loss |
| M-E29 | N25 → N24 | loss of a lagging chromatid can leave a daughter cell monosomic | error→outcome | ERR | Direct Source Support | cellular | medium | unsupported | every monosomy arose by lag |
| M-E30 | N01 → N26 | Mitosis can be tripolar or multipolar | process→error form | LEAD, ERR | Direct Source Support | cellular | high | supported | every extra pole has one cause |
| M-E31 | N26 → N27 | tripolar/multipolar division can produce more than two daughter cells | error form→outcome | LEAD, ERR | Direct Source Support | cellular | high | unsupported | every >2-cell outcome has this mechanism |

## Edge summary and reverse audit

- admitted edges: 31;
- Direct Source Support: 31;
- Indirect Source Support: 0;
- reverse `supported`: 17;
- reverse `unsupported`: 7;
- reverse `not meaningful`: 4;
- reverse `unresolved`: 3.

Reverse support does not create a second admitted edge unless its predicate is independently needed by the local orientation question.

## Editorial bridges excluded from the graph

| ID | Proposed bridge | Existing basis | Missing support / reason for exclusion |
|---|---|---|---|
| M-B01 | Mitosis → full Cell Cycle regulation | Interphase and checkpoint statements | broader source and complete control model excluded |
| M-B02 | Mitosis → live-cell imaging/microscopy | lead, video, gallery | method/evidence pathway not developed |
| M-B03 | Mitosis → development, regeneration, replacement | Function section | cellular-to-organismal intermediate relations absent |
| M-B04 | Mitosis → diagnostic pathology | Diagnostic marker | clinical scope and citation-needed claims require new source audit |
| M-B05 | Mitosis → evolution of division forms | Variations/Evolution | comparative evolutionary model exceeds local process question |

These five records have support class **Editorial Bridge** and are not admitted edges.

## Rejection register

| ID | Rejected candidate | Pressure / reason | Required boundary |
|---|---|---|---|
| M-R01 | full Cell Cycle as local graph | broader linked content | new fixed source required |
| M-R02 | Meiosis comparison | familiar neighboring process | comparison explicitly prohibited; source not developed for it |
| M-R03 | Mitosis causes cancer | article names associations and mutations | causality and clinical scope unsupported |
| M-R04 | developmental-biology graph | Function mentions growth/regeneration | intermediate mechanisms absent |
| M-R05 | genetics beyond chromosome-set statements | familiar domain expansion | outside source scope |
| M-R06 | universal phase model | standard diagram pressure | organismal and suborder variations contradict universality |
| M-R07 | checkpoint guarantees success | source uses guarantee language | later errors and incomplete mechanism prevent promotion |
| M-R08 | organism-wide consequence edges | scale expansion | intermediate representations absent |
| M-R09 | social/historical analogy | metaphor pressure | no source evidence |
| M-R10 | computational state-machine analogy | sequence vocabulary | no source evidence |
| M-R11 | closed cyclical graph | cell-cycle familiarity | no closure admitted; Interphase model excluded |
| M-R12 | Prophase → daughter cells shortcut | reachability through path | transitive relation is not a direct edge |
| M-R13 | nuclear envelope always breaks down | open-mitosis default | closed/semi-open forms preserved |
| M-R14 | centrosomes universally required | animal-cell description | source explicitly qualifies them |
| M-R15 | Cytokinesis as mitotic phase | diagram/order pressure | source explicitly calls it separate |
| M-R16 | diagnostic/prognostic recommendation | Diagnostic marker section | citation-needed and no decision authority |
| M-R17 | universal transition operator, Orientation Hypothesis, or Atlas entry | abstract pattern pressure | prohibited and unsupported by one case |

All 17 candidates are rejected from the admitted graph. Rejection does not assert that the wider subject is false; it asserts that this version cannot admit the proposed local relation.

## Non-transitivity and sequence audit

The named phase route is available as editorial navigation. It does not create direct edges from early phases to final outcomes. Consecutive phases use temporal-precedence predicates only where the source orders them. Causal predicates are admitted separately and locally.

## Stopping rationale

The neighborhood stops because it already answers the declared local questions: where the source places named landmarks; how chromosome descriptions change; where spatial reorganization occurs; what condition is associated with continuation; how Mitosis is bounded from Cytokinesis; and which source-developed deviations challenge normal completion.

Further molecular detail would require phase-specific linked sources. Full Cell Cycle, development, diagnostic pathology, evolution, Meiosis, and disease would require separately fixed evidence bodies. Additional nodes would otherwise become encyclopedic, transitive, cross-scale, or editorially bridged. The stop is evidential and question-bound, not visual.

Another analyst could split chromosome states, omit error nodes, or stop before wider outcomes. Such alternatives would need a new version and explicit reasons; they cannot silently modify this neighborhood.

## Disposition

The source supports a finite directional neighborhood with heterogeneous nodes and local predicates. It does not support comparison, Atlas membership, hypothesis formation, ontology, or a universal phase architecture.
