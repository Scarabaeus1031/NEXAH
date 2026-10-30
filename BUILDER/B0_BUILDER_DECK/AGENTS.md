# B0 Builder Desk operating rule

Read `BUILDER_POLICY.md` before any Builder task. For website, preview, staging,
commit, push or deployment work also read, in this order:

1. `/Users/tho2020/Documents/NEXAH ECOSYSTEM/00 EXECUTIVE/NEXAH-Mission-Control/MISSION_CONTROL_ENTRYPOINT.md`
   for the controlling cold start, authority matrix and routing;
2. `/Users/tho2020/Documents/NEXAH ECOSYSTEM/00 EXECUTIVE/NEXAH-Mission-Control/CURRENT/RETURN_INGESTION_AND_PUBLICATION_BOUNDARY_PROTOCOL.md`
   for return, staging and release policy.

B0 routes and builds; it does not create a second website master. Work in the
canonical source repository, expose the exact candidate inside the single A0
Owner frame, and treat standalone pages and temporary hosts as diagnostic only.
Human Owner acceptance binds only the framed revision. Commit, push and deploy
remain separate gates. Return the production revision and live smoke result to
A0. Stop with `VERSION_AMBIGUOUS` when source, projection, artifact or live
channel disagree.
