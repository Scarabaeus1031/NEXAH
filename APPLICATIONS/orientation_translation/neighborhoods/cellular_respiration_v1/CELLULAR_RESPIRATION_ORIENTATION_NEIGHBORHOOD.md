# CELLULAR RESPIRATION ORIENTATION NEIGHBORHOOD

## Research question

> What is the smallest inspectable local orientation structure justified by the fixed Cellular Respiration evidence body?

This neighborhood is constructed only from Wikipedia revision `1355541234`, the frozen Pilot 02 translation core, and the frozen Reflection. It does not inherit nodes, edges, topology, roles, or support from another pilot.

## Frozen inputs

- Source revision SHA-1: `c96af996f65545bcbadf4d732804efcb109aaee9`
- Reflection SHA-256: `65e3f5becaff546d43d751ffa6c91d7cf7f92cd2aa8515740753c2f54f897351`
- Translation core: twelve SHA-256-verified files listed in the Reflection manifest

## Structure summary

- **Nodes:** 21
- **Admitted directional edges:** 27
- **Support:** 27 Direct Source Support; 0 Indirect Source Support
- **Editorial bridges admitted:** 0
- **Topology:** asymmetric process-and-branch structure; no prescribed rings
- **Cross-scale edge:** ATP → cellular work is explicitly bounded from molecular representation to cellular function
- **Reciprocity:** no reverse edge inherited; every forward edge has an explicit reverse status

## Node register

| ID | Label | Representation type | Scale | Source basis | Relevance | Status | Ambiguity | Prohibited interpretation |
|---|---|---|---|---|---|---|---|---|
| CR-N01 | Cellular respiration | Bounded process | Molecular/cellular | Lead | Local orientation object | admitted | Broad term includes aerobic and anaerobic forms but excludes fermentation in source definition | Not all metabolism, breathing, or universal energy flow |
| CR-N02 | Biological fuels | Input class | Molecular | Lead | Establishes what is oxidized | admitted | Sugar, amino acids, and fatty acids are grouped unequally | Not glucose alone; not food-web energy |
| CR-N03 | External electron acceptor | Functional role | Molecular | Lead; Anaerobic respiration | Distinguishes respiration from fermentation and branches respiratory forms | admitted | Oxygen and other inorganic acceptors differ | Not a single interchangeable molecule |
| CR-N04 | ATP | Energy-coupling product and local input | Molecular | Lead; Glycolysis; cycles; Efficiency | Central output, investment, transport, and cellular-use representation | admitted | Source uses ATP in several roles and totals | Not “energy itself” or a universal yield |
| CR-N05 | Glycolysis | Pathway | Molecular/cellular | Glycolysis | Shared early transformation in source account | admitted | Occurs with or without oxygen; not equivalent to respiration as a whole | Not the complete process |
| CR-N06 | Pyruvate | Intermediate | Molecular | Glycolysis; Pyruvate oxidation; Fermentation | Branch point in source representation | admitted | Later handling depends on represented conditions | Not automatically acetyl-CoA or lactate |
| CR-N07 | Acetyl-CoA | Intermediate | Molecular | Pyruvate oxidation; Citric acid cycle | Connects pyruvate oxidation to cycle | admitted | Source also notes aerobic/anaerobic possibilities after formation | Not a universal destination for all pyruvate |
| CR-N08 | Citric acid cycle | Cyclic pathway | Molecular/subcellular | Citric acid cycle | Produces reduced carriers, CO2, and GTP/ATP | admitted | Named Krebs/TCA; cycle is not a linear stage internally | Not merely one reaction |
| CR-N09 | Reduced electron carriers | Carrier class | Molecular | Glycolysis; cycle; Oxidative phosphorylation | Connects substrate transformations to electron transport | admitted | Bundles NADH and FADH2 despite different entry/yield | Not identical carriers |
| CR-N10 | Electron transport chain | Membrane transfer process | Molecular/membrane | Aerobic respiration; Oxidative phosphorylation | Establishes gradient through electron transfer | admitted | Anaerobic chains are not developed in equal detail | Not ATP synthesis by itself |
| CR-N11 | Proton gradient | Stored electrochemical potential | Membrane | Aerobic respiration; Oxidative phosphorylation; Efficiency | Connects electron transport to ATP synthase | admitted | Source also discusses leak and transport use | Not a static container or universal efficiency |
| CR-N12 | ATP synthase | Enzyme/coupling mechanism | Molecular/membrane | Oxidative phosphorylation; Efficiency | Uses gradient to phosphorylate ADP | admitted | Stoichiometry varies in source discussion | Not the only ATP-production mechanism |
| CR-N13 | Cytosol | Spatial compartment | Cellular/subcellular | Glycolysis; Fermentation | Locates glycolysis and fermentation account | admitted | Prokaryotic/eukaryotic uses differ | Not the whole cell |
| CR-N14 | Mitochondrial matrix | Spatial compartment | Subcellular | Pyruvate oxidation; Citric acid cycle | Locates later aerobic stages in eukaryotic account | admitted | Source sometimes uses “mitochondria” broadly | Not present or required in prokaryotes |
| CR-N15 | Inner mitochondrial membrane / cristae | Spatial boundary | Subcellular | Oxidative phosphorylation; Efficiency | Locates electron transport, gradient, and ATP synthase | admitted | Combined source wording at different structural resolution | Not a universal respiratory membrane label |
| CR-N16 | Oxygen | Terminal acceptor instance | Molecular | Lead; Aerobic respiration; Oxidative phosphorylation | Distinguishes aerobic branch and water formation | admitted | Source wording around terminal acceptors is locally awkward | Not respiration itself or proof of rate |
| CR-N17 | Fermentation | Alternative metabolic process | Molecular/cellular | Lead; Fermentation | Preserves non-respiratory handling without external acceptor | admitted | Multiple organism-specific products | Not anaerobic respiration |
| CR-N18 | Anaerobic respiration | Respiratory subtype | Molecular to microbial context | Lead; Anaerobic respiration | Preserves respiration with non-oxygen acceptors | admitted | Section is brief and citation-limited | Not fermentation and not all oxygen-free metabolism |
| CR-N19 | Cellular work | Functional consequence class | Cellular | Lead | Records source uses of ATP in biosynthesis, locomotion, and transport | admitted | Broad grouped outcome | Not a measured organismal benefit |
| CR-N20 | Waste products | Output class | Molecular | Lead; cycle; Fermentation; Oxidative phosphorylation | Preserves outputs such as CO2, water, lactate, ethanol | admitted | Products differ across paths | Not one chemically uniform class |
| CR-N21 | Aerobic respiration | Respiratory subtype | Molecular/cellular | Lead; Aerobic respiration | Makes oxygen-dependent branch explicit | admitted | Detailed source account is mainly eukaryotic | Not the only form of respiration |

## Edge register

All admitted edges are directional. `Reverse` records the status of the exact inverse relation, not general conceptual association.

| ID | From → To | Neighborhood role | Relation statement | Support | Source basis | Scope / scale transition | Unsupported implications | Reverse | Decision |
|---|---|---|---|---|---|---|---|---|---|
| CR-E01 | N01 → N02 | input | Cellular respiration oxidizes biological fuels. | Direct Source Support | Lead | process → molecular input | All fuels enter through identical steps | unsupported | admitted |
| CR-E02 | N01 → N03 | defining function | Cellular respiration uses an external inorganic electron acceptor. | Direct Source Support | Lead | process → molecular role | Every acceptor is oxygen | unsupported | admitted |
| CR-E03 | N01 → N04 | principal orientation output | Cellular respiration drives production of ATP. | Direct Source Support | Lead | process → molecular product | One fixed ATP yield | editorial reverse only | admitted |
| CR-E04 | N04 → N19 | cross-scale consequence | ATP can drive biosynthesis, locomotion, and membrane transport. | Direct Source Support | Lead | molecular → cellular function; source explicitly connects them | ATP alone explains organismal performance | unresolved | admitted |
| CR-E05 | N01 → N21 | subtype | Aerobic respiration is a form of cellular respiration using oxygen. | Direct Source Support | Lead | process classification | Aerobic form represents all respiration | independently supported as category membership only, not same predicate | admitted |
| CR-E06 | N21 → N16 | condition | Aerobic respiration requires oxygen in the source account. | Direct Source Support | Aerobic respiration | subtype → molecular condition | Oxygen concentration predicts rate | unsupported | admitted |
| CR-E07 | N21 → N05 | initial pathway | The aerobic account includes glycolysis as its initial pathway. | Direct Source Support | Aerobic respiration; Glycolysis | subtype → pathway | Glycolysis requires oxygen | unsupported | admitted |
| CR-E08 | N05 → N06 | transformation | Glycolysis converts glucose to pyruvate. | Direct Source Support | Glycolysis | molecular pathway | Pyruvate has only one destination | unsupported | admitted |
| CR-E09 | N05 → N04 | substrate-level output | Glycolysis produces net ATP while also investing ATP. | Direct Source Support | Glycolysis | molecular | Gross and net ATP are identical | independently supported in the distinct ATP-investment sense only | admitted |
| CR-E10 | N05 → N09 | carrier production | Glycolysis produces NADH, represented within the carrier class. | Direct Source Support | Glycolysis | molecular | FADH2 is produced by glycolysis | unsupported | admitted |
| CR-E11 | N05 → N13 | location | Glycolysis occurs in the cytosol. | Direct Source Support | Glycolysis | pathway → cellular compartment | Location explains the pathway | unsupported | admitted |
| CR-E12 | N06 → N07 | transformation | Pyruvate oxidation produces acetyl-CoA. | Direct Source Support | Pyruvate oxidation | molecular | All pyruvate follows this path | unsupported | admitted |
| CR-E13 | N07 → N08 | pathway entry | Acetyl-CoA enters the citric acid cycle in the aerobic account. | Direct Source Support | Citric acid cycle | molecular → cyclic pathway | Acetyl-CoA determines oxygen availability | unsupported | admitted |
| CR-E14 | N08 → N09 | carrier production | The cycle produces NADH and FADH2. | Direct Source Support | Citric acid cycle | molecular | The carriers are equivalent | unsupported | admitted |
| CR-E15 | N08 → N20 | output | The cycle produces CO2 and water as represented waste products. | Direct Source Support | Citric acid cycle | molecular | All waste products arise here | unsupported | admitted |
| CR-E16 | N08 → N14 | location | The eukaryotic cycle is located in the mitochondrial matrix. | Direct Source Support | Citric acid cycle | pathway → subcellular compartment | Same location in prokaryotes | unsupported | admitted |
| CR-E17 | N09 → N10 | electron supply | Reduced carriers supply potential to the electron transport chain. | Direct Source Support | Aerobic respiration; Oxidative phosphorylation | molecular → membrane process | Identical yield per carrier | unsupported | admitted |
| CR-E18 | N10 → N11 | coupling step | Electron transport establishes a proton gradient. | Direct Source Support | Oxidative phosphorylation | membrane process → membrane potential | Gradient is ATP | unsupported | admitted |
| CR-E19 | N10 → N15 | location | Eukaryotic electron transport occurs at the inner mitochondrial membrane/cristae. | Direct Source Support | Oxidative phosphorylation | process → subcellular boundary | Universal mitochondrial location | unsupported | admitted |
| CR-E20 | N11 → N12 | coupling step | The proton gradient drives ATP synthase. | Direct Source Support | Oxidative phosphorylation | membrane potential → enzyme | No leak or competing use | unsupported | admitted |
| CR-E21 | N12 → N04 | ATP synthesis | ATP synthase produces ATP from ADP and phosphate using the gradient. | Direct Source Support | Oxidative phosphorylation | molecular | Fixed H+/ATP ratio | unresolved | admitted |
| CR-E22 | N10 → N16 | terminal transfer | Electrons are finally transferred to oxygen in the aerobic account. | Direct Source Support | Oxidative phosphorylation | molecular | Oxygen is the acceptor in anaerobic respiration | unsupported | admitted |
| CR-E23 | N16 → N20 | product formation | Oxygen with electrons and protons forms water in the source account. | Direct Source Support | Oxidative phosphorylation | molecular | Oxygen produces every waste product | unsupported | admitted |
| CR-E24 | N01 → N18 | subtype | Anaerobic respiration is a cellular-respiration form using non-oxygen acceptors. | Direct Source Support | Lead; Anaerobic respiration | process classification | Equivalent to fermentation | independently supported as category membership only, not same predicate | admitted |
| CR-E25 | N18 → N03 | acceptor condition | Anaerobic respiration uses external inorganic acceptors other than oxygen. | Direct Source Support | Lead; Anaerobic respiration | subtype → molecular role | Claim independently validated despite citation-needed signal | unsupported | admitted |
| CR-E26 | N06 → N17 | alternative handling | Without oxygen in the source account, pyruvate may undergo fermentation. | Direct Source Support | Citric acid cycle; Fermentation | molecular intermediate → process | Fermentation is respiration or the only alternative | unsupported | admitted |
| CR-E27 | N17 → N20 | variable output | Fermentation produces organism-dependent waste products such as lactate or ethanol/CO2. | Direct Source Support | Fermentation | process → molecular outputs | Same product or yield in every organism | unsupported | admitted |

## Cross-scale audit

Only CR-E04 intentionally crosses from a molecular representation to a cellular-function class. The source explicitly states that ATP can drive biosynthesis, locomotion, and membrane transport. The edge does not imply measured organismal performance, ecological consequence, or that ATP alone explains those functions.

The narrow plant-respiration/ecosystem statement was not admitted because the local question can be answered without expanding to ecosystem flux, and the source does not provide the intermediate representations required for an inspectable scale transition.

## Non-transitivity audit

The following tempting shortcuts were not admitted:

- Glycolysis → citric acid cycle from Glycolysis → Pyruvate → Acetyl-CoA → Cycle.
- Reduced carriers → ATP from Carriers → ETC → Gradient → ATP synthase → ATP.
- Electron transport chain → ATP from ETC → Gradient → ATP synthase → ATP.
- Oxygen → ATP from Oxygen's terminal role and ATP production elsewhere.
- Cellular respiration → cellular work from Respiration → ATP → Cellular work.
- Glycolysis → mitochondrial matrix from the later aerobic stages.

Each shortcut would require its own relation statement and scope. Their apparent plausibility does not create admission.

## Rejection register

| ID | Proposed element or relation | Rejection class | Reason | Local meaning |
|---|---|---|---|---|
| CR-R01 | Photosynthesis as a neighborhood node | irrelevant under local question | One narrow plant statement does not develop the relationship needed for this local mechanism map. | Not a claim that the scientific relation is false. |
| CR-R02 | Terrestrial ecosystem CO2 as a node | insufficiently supported for local scale expansion | The source gives one quantitative-context sentence without intermediate scale structure. | Requires a new source audit. |
| CR-R03 | Respirometry / measurement | editorial only | Appears in See also; linked content is outside the fixed evidence body. | Candidate question, not admitted representation. |
| CR-R04 | Electron transport chain → ATP | transitive overreach / compressed mechanism | The admitted local path preserves gradient and ATP synthase. | A high-level summary may use the shortcut, but this graph does not. |
| CR-R05 | ATP → Cellular respiration as inverse of E03 | reciprocity assumption | ATP is also invested locally, but that is not the inverse of “respiration produces ATP.” | Reverse predicate requires its own audit. |
| CR-R06 | Oxygen → Aerobic respiration as inverse of E06 | reciprocity assumption | Presence of oxygen alone does not establish occurrence or rate. | Reverse edge unsupported. |
| CR-R07 | Physiological respiration / breathing identity | semantic ambiguity | The fixed article does not develop physiological respiration. | Shared word is not identity. |
| CR-R08 | Food webs, climate, and global carbon cycle | source-external knowledge | Not developed by the fixed evidence body. | Potential future subjects only. |
| CR-R09 | A balanced branch for every pathway stage | visual or symmetry pressure | The source has unequal detail and an asymmetric process. | Visual balance has no authority. |
| CR-R10 | Universal mitochondrial pathway | scale collapse | Prokaryotic location differs and the source's detailed spatial map is eukaryotic. | No universal organelle requirement. |
| CR-R11 | Alternative fuels mapped into exact pathway entry points | insufficiently supported | Fuels are named, but their entry pathways are not developed. | Requires additional evidence. |
| CR-R12 | Evolutionary hierarchy among respiratory forms | unsupported interpretation | No adequate evolutionary account in the fixed source. | No ranking or origin claim. |
| CR-R13 | Earth–Sun–Moon patterns, universal functional triads, recurring operator classes, universal transition roles, cross-domain equivalence, or cosmological analogy | Unsupported cross-domain interpretation — outside Pilot 02 scope | No support in the fixed evidence body or declared procedure. | No hypothesis may be created. |

## Stopping decision

### Why the local question is sufficiently represented

The neighborhood contains the minimum roles needed to navigate the fixed source's core definition, aerobic transformation chain, spatial/coupling mechanism, alternative acceptor branch, fermentation distinction, cellular ATP use, and variable outputs. Every admitted edge is directly source-supported and directionally inspectable. Adding further detail would shift from orientation into pathway encyclopedism or require new sources.

### Open branches

- regulation and pathway control;
- experimental measurement and respirometry;
- detailed alternative-fuel entry;
- prokaryotic membrane organization;
- organism-specific fermentation and anaerobic pathways;
- quantitative ATP reconciliation;
- physiological and ecological scaling;
- source claims requiring independent scientific review.

### Limits

- **Epistemic:** one tertiary revision, uneven citation strength, excluded linked content.
- **Editorial:** bundled carrier and waste-product nodes; selected local process chain; one explicit cross-scale edge.
- **Practical:** enzyme-level detail and every intermediate are omitted to preserve inspectability.

### Could another analyst stop elsewhere?

Yes. Another analyst might split carrier classes, omit spatial nodes, add directly supported individual products, or stop before cellular work. Such differences would require explicit reasons and would not inherit this graph. Finite size does not prove stability.

### Reopening condition

Reopen only with a newly declared orientation question or independently fixed source body. Preserve this version, audit every proposed node and edge again, record rejections, and issue a new stopping decision. Do not silently extend this neighborhood.

## Neighborhood boundary

This is not an ontology, complete metabolic network, comparison result, Atlas, hypothesis, or scientific validation.

## Disposition

**EVIDENCE-BOUNDED NEIGHBORHOOD IDENTIFIED**
