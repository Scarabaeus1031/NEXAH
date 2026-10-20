(function(root,factory){
  const api=factory(typeof module==="object"&&module.exports?require("../domain-engine.js"):root.ThreeDomainEngine);
  if(typeof module==="object"&&module.exports)module.exports=api;
  root.ThreeDomainReplication=api;
}(typeof globalThis!=="undefined"?globalThis:this,function(E){
  "use strict";
  const DEFAULT_THRESHOLDS=[.14,.18,.22,.26,.30,.34];
  const makeAcc=()=>({auc:0,peak:0,detected:0,events:0,beta0:0,beta1:0,finalDelta:0});
  function add(acc,s,cells){const ratio=s.residual.length/cells;acc.auc+=ratio;acc.peak=Math.max(acc.peak,ratio);acc.detected+=ratio>0?1:0;acc.events+=s.events.all.length;acc.beta0+=s.topology.beta0;acc.beta1+=s.topology.beta1;acc.finalDelta=s.residual.length}
  function finish(acc,horizon){return{response:acc.auc/horizon,peak:acc.peak,detection:acc.detected/horizon,meanEvents:acc.events/horizon,meanBeta0:acc.beta0/horizon,meanBeta1:acc.beta1/horizon,finalDelta:acc.finalDelta}}
  function runSeed(seed,options={}){
    const n=options.n||24,horizon=options.horizon||60,thresholds=options.thresholds||DEFAULT_THRESHOLDS,cells=n*n;
    const chemistry=Object.fromEntries(thresholds.map(t=>[t.toFixed(2),makeAcc()])),life=makeAcc(),physics=makeAcc();
    const pairs={chemistry:E.createPair("chemistry",{n,seed,boundary:"cylinder-x",threshold:thresholds[0]}),life:E.createPair("life",{n,seed:seed+101,boundary:"cylinder-x"}),physics:E.createPair("physics",{n,seed:seed+202,boundary:"cylinder-x"})};
    for(let g=0;g<horizon;g++){
      E.stepPair(pairs.chemistry);E.stepPair(pairs.life);E.stepPair(pairs.physics);
      for(const t of thresholds){pairs.chemistry.threshold=t;add(chemistry[t.toFixed(2)],E.observe(pairs.chemistry),cells)}
      add(life,E.observe(pairs.life),cells);add(physics,E.observe(pairs.physics),cells);
    }
    return{seed,chemistry:Object.fromEntries(thresholds.map(t=>[t.toFixed(2),finish(chemistry[t.toFixed(2)],horizon)])),life:finish(life,horizon),physics:finish(physics,horizon)};
  }
  const mean=values=>values.reduce((a,b)=>a+b,0)/Math.max(1,values.length);
  function aggregate(rows,thresholds){
    const chemistry=Object.fromEntries(thresholds.map(t=>{const key=t.toFixed(2),items=rows.map(r=>r.chemistry[key]);return[key,{response:mean(items.map(x=>x.response)),peak:mean(items.map(x=>x.peak)),detection:mean(items.map(x=>x.detection)),meanBeta0:mean(items.map(x=>x.meanBeta0)),meanBeta1:mean(items.map(x=>x.meanBeta1)),seedDetection:mean(items.map(x=>x.peak>0?1:0))}]}));
    const domain=name=>{const items=rows.map(r=>r[name]);return{response:mean(items.map(x=>x.response)),peak:mean(items.map(x=>x.peak)),detection:mean(items.map(x=>x.detection)),meanBeta0:mean(items.map(x=>x.meanBeta0)),meanBeta1:mean(items.map(x=>x.meanBeta1)),seedDetection:mean(items.map(x=>x.peak>0?1:0))}};
    return{chemistry,life:domain("life"),physics:domain("physics")};
  }
  function fnv(text){let h=0x811c9dc5;for(let i=0;i<text.length;i++){h^=text.charCodeAt(i);h=Math.imul(h,0x01000193)}return(h>>>0).toString(16).padStart(8,"0")}
  function buildResult(rows,config){const summary=aggregate(rows,config.thresholds),base={schema:"nexah.life08.three-domain-replication.v1",authority:"UNADMITTED_MODEL_ONLY",config,rows,summary};return{...base,fingerprint:fnv(JSON.stringify(base))}}
  return Object.freeze({DEFAULT_THRESHOLDS,runSeed,aggregate,buildResult,fnv});
}));
