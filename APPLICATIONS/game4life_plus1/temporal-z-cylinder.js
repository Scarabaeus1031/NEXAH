(function(root,factory){
  const api=factory();
  if(typeof module==="object"&&module.exports)module.exports=api;
  root.LifeTemporalZ=api;
}(typeof globalThis!=="undefined"?globalThis:this,function(){
  "use strict";
  const SCHEMA="nexah.life.temporal-z-cylinder.v1";
  const clamp=(v,a,b)=>Math.max(a,Math.min(b,v));

  function axes(boundary){
    return boundary==="cylinder-y"?{theta:"y",radius:"x"}:{theta:"x",radius:"y"};
  }

  function map(event,size,boundary,firstGeneration,lastGeneration,options={}){
    if(!event||!Number.isFinite(event.x)||!Number.isFinite(event.y)||!Number.isFinite(event.generation))throw new TypeError("addressed event required");
    if(!Number.isInteger(size)||size<2)throw new RangeError("size must be at least 2");
    const a=axes(boundary),span=Math.max(1,lastGeneration-firstGeneration),height=Number(options.height)||10;
    const theta=2*Math.PI*event[a.theta]/size,radius=(Number(options.baseRadius)||2.15)+(Number(options.laneDepth)||1.7)*(event[a.radius]/(size-1));
    const z=-height/2+height*clamp((event.generation-firstGeneration)/span,0,1);
    return Object.freeze({x:Math.cos(theta)*radius,y:Math.sin(theta)*radius,z,theta,radius,generation:event.generation,thetaSource:a.theta,radiusSource:a.radius});
  }

  function addressKey(event){return `${event.x},${event.y}`;}

  function consecutiveSegments(events,size,boundary,firstGeneration,lastGeneration,options={}){
    const lanes=new Map(),segments=[];
    for(const event of events){const key=addressKey(event);if(!lanes.has(key))lanes.set(key,[]);lanes.get(key).push(event);}
    for(const lane of lanes.values()){
      lane.sort((a,b)=>a.generation-b.generation);
      for(let i=1;i<lane.length;i++)if(lane[i].generation===lane[i-1].generation+1)segments.push(Object.freeze({from:map(lane[i-1],size,boundary,firstGeneration,lastGeneration,options),to:map(lane[i],size,boundary,firstGeneration,lastGeneration,options),address:addressKey(lane[i]),fromId:lane[i-1].id,toId:lane[i].id}));
    }
    return Object.freeze(segments);
  }

  function metadata(snapshot,firstGeneration,lastGeneration){
    const boundary=snapshot.displayBoundary==="finite-dead"?"cylinder-x":snapshot.displayBoundary,a=axes(boundary);
    return Object.freeze({schema:SCHEMA,projection_only:true,rule_unchanged:true,rule:"B3/S23",boundary,axis_semantics:"world Z = discrete generation",theta_source:a.theta,radius_source:a.radius,z_source:"generation",generation_interval:[firstGeneration,lastGeneration],interpolation:"visual sweep only; no intermediate Life states",source_schema:snapshot.schema});
  }

  return Object.freeze({SCHEMA,axes,map,addressKey,consecutiveSegments,metadata});
}));
