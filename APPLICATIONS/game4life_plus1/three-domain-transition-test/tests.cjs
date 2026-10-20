const assert=require("node:assert/strict");
const E=require("./domain-engine.js");
const V=require("./euler-view.js");

for(const model of E.MODELS){
  const a=E.createModel(model,20,1701,"cylinder-x"),b=E.createModel(model,20,1701,"cylinder-x");
  const an=E.step(a),bn=E.step(b);
  assert.deepEqual(Array.from(E.binary(an)),Array.from(E.binary(bn)),`${model} replay deterministic`);
}

const ring=new Uint8Array(25);for(const k of[6,7,8,11,13,16,17,18])ring[k]=1;
assert.deepEqual(E.topology(ring,5,"open"),{beta0:1,beta1:1,chi:0,active:8});
const seam=new Uint8Array(25);seam[10]=1;seam[14]=1;
assert.equal(E.topology(seam,5,"open").beta0,2);
assert.equal(E.topology(seam,5,"cylinder-x").beta0,1);

const prev=Uint8Array.from([0,1,1,0]),next=Uint8Array.from([1,1,0,0]),events=E.events(prev,next);
assert.deepEqual(events.positive,[0]);assert.deepEqual(events.hold,[1]);assert.deepEqual(events.negative,[2]);assert.equal(events.all.length,3);
assert.deepEqual(E.residual(prev,prev),[]);assert.deepEqual(E.residual(prev,next),[0,2]);
const ledger=E.transitionLedger(Uint8Array.from([0,0,1,1]),Uint8Array.from([0,1,0,1]));
assert.deepEqual({c00:ledger.c00,c01:ledger.c01,c10:ledger.c10,c11:ledger.c11},{c00:1,c01:1,c10:1,c11:1});
assert.equal(ledger.total,4);assert.equal(ledger.exact,true);
assert.deepEqual(ledger.previous,{zero:2,one:2});assert.deepEqual(ledger.current,{zero:2,one:2});

for(const model of E.MODELS){const pair=E.createPair(model,{n:24,seed:881,boundary:"open"});for(let i=0;i<5;i++)E.stepPair(pair);const s=E.observe(pair);assert.equal(s.residual.length,0);assert.equal(s.events.all.length,s.events.positive.length+s.events.hold.length+s.events.negative.length);assert.equal(s.generation,5);assert.equal(s.ledger.total,24*24);assert.equal(s.ledger.exact,true);assert.equal(s.ledger.previous.zero+s.ledger.previous.one,s.ledger.total);assert.equal(s.ledger.current.zero+s.ledger.current.one,s.ledger.total)}

const lifePair=E.createPair("life",{n:24,seed:881,boundary:"cylinder-x"});let detected=false;for(let i=0;i<24;i++){E.stepPair(lifePair);if(E.observe(lifePair).residual.length)detected=true}assert.equal(detected,true);
const exactLedger={c00:1,c01:2,c10:3,c11:4,total:10};
const phasor=V.eulerPhasor(exactLedger);assert.equal(phasor.re,.3);assert.equal(phasor.im,-.1);assert.ok(Math.abs(phasor.magnitude-Math.sqrt(.1))<1e-12);
const snapshots=Object.fromEntries(E.MODELS.map((name,index)=>[name,{ledger:{c00:1+index,c01:2,c10:1,c11:6-index,total:10},events:{all:Array(4+index).fill(0)}}]));
const view=V.buildEulerView(snapshots,121);assert.equal(view.schema,"nexah.three-domain.euler-view.v1");assert.equal(view.clock.phase,1);assert.equal(view.clock.axisMode,"janus");assert.equal(view.gear.base.id,"euler");assert.equal(view.eventTotal,15);assert.equal(view.boundary,"COMMON_COMPLEX_READOUT_ONLY_NO_SHARED_OPERATOR");assert.throws(()=>V.buildEulerView({life:snapshots.life},0),TypeError);
console.log("PASS THREE-DOMAIN 40/40");
