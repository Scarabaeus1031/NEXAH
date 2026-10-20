(()=>{"use strict";
const E=window.LifeCylinder,R=window.LIFE08_RESULT,P=window.LifeCrystalProjection,$=id=>document.getElementById(id);
const specs=[
 {id:"BLOCK-C",label:"Block · still life",kind:"pattern",pattern:"block",size:32,horizon:120},
 {id:"BLINKER-C",label:"Blinker · oscillator",kind:"pattern",pattern:"blinker",size:32,horizon:120},
 {id:"TOAD-C",label:"Toad · oscillator",kind:"pattern",pattern:"toad",size:32,horizon:120},
 {id:"BEEHIVE-C",label:"Beehive · still life",kind:"pattern",pattern:"beehive",size:32,horizon:120},
 {id:"BEEHIVE-BLOOM",label:"Beehive bloom · settles to four",kind:"pattern",pattern:"beehiveBloom",size:32,horizon:120},
 {id:"GLIDER-C",label:"Glider · spaceship",kind:"pattern",pattern:"glider",size:32,horizon:240},
 {id:"R-PENTOMINO",label:"R-pentomino · methuselah",kind:"pattern",pattern:"rPentomino",size:48,horizon:360},
 {id:"ACORN",label:"Acorn · methuselah",kind:"pattern",pattern:"acorn",size:56,horizon:520},
 {id:"LWSS",label:"Lightweight spaceship",kind:"pattern",pattern:"lwss",size:40,horizon:180},
 {id:"GLIDER-X-SEAM",label:"Glider · X seam",kind:"explicit",size:32,cells:[[29,1],[30,2],[28,3],[29,3],[30,3]],horizon:160},
 {id:"GLIDER-Y-SEAM",label:"Glider · Y seam",kind:"explicit",size:32,cells:[[1,29],[2,30],[0,31],[1,31],[2,31]],horizon:160},
 {id:"RANDOM-17",label:"Seeded random · 17%",kind:"random",size:32,density:.17,seed:510017,horizon:200}
];
const fixture=$("fixture"),boundary=$("boundary"),channel=$("channel"),generation=$("generation"),projection=$("projectionMode"),componentOutlines=$("componentOutlines"),playPause=$("playPause"),speed=$("speed"),runLength=$("runLength"),loopPlayback=$("loopPlayback"),observeMode=$("observeMode");
for(const s of specs)fixture.add(new Option(s.label,s.id));
const cache=new Map();
const run=(spec,b)=>{const k=spec.id+":"+b+":"+spec.horizon;if(!cache.has(k))cache.set(k,E.run(spec,b));return cache.get(k)};
const colors={live:"#eef7fb",births:"#22d3ee",survivals:"#f5bf42",deaths:"#fb7185",residual:"#a78bfa"};
let timer=null;
function chosen(){return specs.find(s=>s.id===fixture.value)}
function activeSpec(){const spec=chosen(),selected=runLength.value==="fixture"?spec.horizon:Number(runLength.value);return {...spec,horizon:selected}}
function key(c){return c.join(",")}
function cellsAt(r,g,k){if(k==="live")return r.states[g].live;if(!g)return[];return r.rows[g-1].sets[k]}
function symmetricDifference(a,b){const A=new Set(a.map(key)),B=new Set(b.map(key)),out=[];for(const c of a)if(!B.has(key(c)))out.push(c);for(const c of b)if(!A.has(key(c)))out.push(c);return out}
function componentGroups(cells,n,b){
  const pool=new Map(cells.map(c=>[key(c),c])),seen=new Set(),groups=[];
  for(const [startKey,start] of pool){
    if(seen.has(startKey))continue;
    const group=[],queue=[start];seen.add(startKey);
    while(queue.length){
      const cell=queue.pop();group.push(cell);const[x,y]=cell;
      for(let dy=-1;dy<=1;dy++)for(let dx=-1;dx<=1;dx++){
        if(!dx&&!dy)continue;const mapped=E.mapCoord(x+dx,y+dy,n,b);if(!mapped)continue;
        const k=key(mapped);if(pool.has(k)&&!seen.has(k)){seen.add(k);queue.push(pool.get(k))}
      }
    }
    groups.push(group);
  }
  return groups;
}
function hull(points){
  if(points.length<3)return points;
  const p=[...points].sort((a,b)=>a.x-b.x||a.y-b.y),cross=(o,a,b)=>(a.x-o.x)*(b.y-o.y)-(a.y-o.y)*(b.x-o.x),lo=[],hi=[];
  for(const x of p){while(lo.length>1&&cross(lo[lo.length-2],lo[lo.length-1],x)<=0)lo.pop();lo.push(x)}
  for(let i=p.length-1;i>=0;i--){const x=p[i];while(hi.length>1&&cross(hi[hi.length-2],hi[hi.length-1],x)<=0)hi.pop();hi.push(x)}
  lo.pop();hi.pop();return lo.concat(hi);
}
function outlineGroups(c,cells,n,b,project,color){
  if(!componentOutlines.checked||!cells.length)return;
  c.strokeStyle=color;c.lineWidth=1.5;c.globalAlpha=.72;
  for(const group of componentGroups(cells,n,b)){
    const shape=hull(group.map(project));if(shape.length===1){c.beginPath();c.arc(shape[0].x,shape[0].y,8,0,Math.PI*2);c.stroke();continue}
    c.beginPath();c.moveTo(shape[0].x,shape[0].y);for(let i=1;i<shape.length;i++)c.lineTo(shape[i].x,shape[i].y);if(shape.length>2)c.closePath();c.stroke();
  }
  c.globalAlpha=1;
}
function layersAt(r,dead,g,kind){
  if(kind==="all"){
    if(!g)return[{kind:"live",cells:r.states[0].live}];
    return["deaths","survivals","births"].map(k=>({kind:k,cells:cellsAt(r,g,k)}));
  }
  if(kind==="residual")return[{kind:"residual",cells:symmetricDifference(r.states[g].live,dead.states[g].live)}];
  return[{kind,cells:cellsAt(r,g,kind)}];
}
function context(canvas){const c=canvas.getContext("2d");c.clearRect(0,0,canvas.width,canvas.height);c.fillStyle="#071018";c.fillRect(0,0,canvas.width,canvas.height);return c}
function drawGrid(c,n,b,pad=44){const w=(c.canvas.width-2*pad)/n,h=(c.canvas.height-2*pad)/n;c.strokeStyle="#203441";c.lineWidth=1;const stride=Math.max(2,Math.floor(n/8));for(let i=0;i<=n;i+=stride){c.beginPath();c.moveTo(pad+i*w,pad);c.lineTo(pad+i*w,pad+n*h);c.stroke();c.beginPath();c.moveTo(pad,pad+i*h);c.lineTo(pad+n*w,pad+i*h);c.stroke()}c.strokeStyle="#f5bf42";c.lineWidth=3;c.setLineDash([7,7]);if(b==="cylinder-x")c.strokeRect(pad-2,pad-2,n*w+4,n*h+4);else{c.beginPath();c.moveTo(pad,pad);c.lineTo(pad+n*w,pad);c.moveTo(pad,pad+n*h);c.lineTo(pad+n*w,pad+n*h);c.stroke()}c.setLineDash([]);return{pad,w,h}}
function drawFlat(c,layers,n,b){const g=drawGrid(c,n,b);for(const layer of layers){c.fillStyle=colors[layer.kind];for(const[x,y]of layer.cells)c.fillRect(g.pad+x*g.w+1,g.pad+y*g.h+1,Math.max(2,g.w-2),Math.max(2,g.h-2))}}
function cylinderPoints(cells,n,b,cx,top,bottom,rx,ry){return cells.map(([x,y])=>{const around=b==="cylinder-x"?x:y,axis=b==="cylinder-x"?y:x,a=2*Math.PI*around/n,z=top+(bottom-top)*axis/(n-1);return{x:cx+rx*Math.cos(a),y:z+ry*Math.sin(a),front:Math.sin(a)}}).sort((a,b)=>a.front-b.front)}
function drawCylinder(c,layers,n,b){const cx=c.canvas.width/2,rx=250,ry=76,top=90,bottom=530;c.strokeStyle="#294451";c.lineWidth=1;for(let j=0;j<=8;j++){const y=top+(bottom-top)*j/8;c.beginPath();c.ellipse(cx,y,rx,ry,0,0,Math.PI*2);c.stroke()}for(let i=0;i<16;i++){const a=2*Math.PI*i/16;c.beginPath();c.moveTo(cx+rx*Math.cos(a),top+ry*Math.sin(a));c.lineTo(cx+rx*Math.cos(a),bottom+ry*Math.sin(a));c.stroke()}c.strokeStyle="#f5bf42";c.lineWidth=3;c.beginPath();c.moveTo(cx+rx,top);c.lineTo(cx+rx,bottom);c.stroke();for(const layer of layers)for(const p of cylinderPoints(layer.cells,n,b,cx,top,bottom,rx,ry)){c.globalAlpha=.28+.72*(p.front+1)/2;c.fillStyle=colors[layer.kind];c.beginPath();c.arc(p.x,p.y,layer.kind==="residual"?5:3.6,0,Math.PI*2);c.fill()}c.globalAlpha=1}
function planeProject(cell,n,y){const[x,yy]=cell,left=112,right=648,height=78,skew=34;return{x:left+skew+(right-left-2*skew)*x/(n-1)-2*skew*yy/(n-1),y:y-height/2+height*yy/(n-1)}}
function drawPlane(c,cells,n,y,label,color,b){const left=112,right=648,height=78,skew=34;c.fillStyle="rgba(16,31,43,.76)";c.strokeStyle="#294451";c.lineWidth=1;c.beginPath();c.moveTo(left+skew,y-height/2);c.lineTo(right+skew,y-height/2);c.lineTo(right-skew,y+height/2);c.lineTo(left-skew,y+height/2);c.closePath();c.fill();c.stroke();c.fillStyle=color;c.font="600 13px Inter,system-ui,sans-serif";c.fillText(label,38,y+4);for(const cell of cells){const p=planeProject(cell,n,y);c.globalAlpha=.86;c.beginPath();c.arc(p.x,p.y,2.8,0,Math.PI*2);c.fill()}c.globalAlpha=1;outlineGroups(c,cells,n,b,cell=>planeProject(cell,n,y),color)}
function drawFourPlusOne(c,r,g,n,b){const row=g?r.rows[g-1]:null,sets=row?row.sets:{births:[],survivals:[],deaths:[]},all=row?[...sets.births,...sets.survivals,...sets.deaths]:r.states[0].live;drawPlane(c,all,n,104,"1 · EVENTS",colors.live,b);drawPlane(c,sets.births,n,222,"i · BIRTH",colors.births,b);drawPlane(c,sets.survivals,n,340,"j · SURVIVE",colors.survivals,b);drawPlane(c,sets.deaths,n,458,"k · DEATH",colors.deaths,b);c.strokeStyle="#a78bfa";c.lineWidth=3;c.beginPath();c.moveTo(100,570);c.lineTo(660,570);c.stroke();c.fillStyle="#a78bfa";c.font="600 13px Inter,system-ui,sans-serif";c.fillText(`Q° · ${b} · B3/S23 · generation ${g}`,190,598)}
const phaseLanes=[
  {key:"births",label:"+90° · BIRTH · IN",color:colors.births,end:{x:660,y:130}},
  {key:"survivals",label:"0° · SURVIVE · HOLD",color:colors.survivals,end:{x:660,y:310}},
  {key:"deaths",label:"−90° · DEATH · OUT",color:colors.deaths,end:{x:660,y:490}}
];
function phaseProject(cell,n,lane){const[x,y]=cell,start={x:125,y:310},dx=lane.end.x-start.x,dy=lane.end.y-start.y,len=Math.hypot(dx,dy),ux=dx/len,uy=dy/len,px=-uy,py=ux,t=.08+.9*x/(n-1),offset=(y/(n-1)-.5)*82;return{x:start.x+dx*t+px*offset,y:start.y+dy*t+py*offset}}
function phaseLaneShape(c,lane){const start={x:125,y:310},dx=lane.end.x-start.x,dy=lane.end.y-start.y,len=Math.hypot(dx,dy),px=-dy/len*48,py=dx/len*48;c.fillStyle="rgba(16,31,43,.62)";c.strokeStyle="#294451";c.lineWidth=1;c.beginPath();c.moveTo(start.x+px,start.y+py);c.lineTo(lane.end.x+px,lane.end.y+py);c.lineTo(lane.end.x-px,lane.end.y-py);c.lineTo(start.x-px,start.y-py);c.closePath();c.fill();c.stroke();c.fillStyle=lane.color;c.font="600 13px Inter,system-ui,sans-serif";c.fillText(lane.label,lane.end.x-172,lane.end.y-58)}
function drawPhaseRegister(c,r,g,n,b){
  c.fillStyle="#a78bfa";c.beginPath();c.arc(105,310,22,0,Math.PI*2);c.fill();c.fillStyle="#071018";c.font="600 12px Inter,system-ui,sans-serif";c.fillText("Δt",96,314);
  for(const lane of phaseLanes){
    phaseLaneShape(c,lane);
    for(let age=3;age>=0;age--){const index=g-1-age;if(index<0)continue;const cells=r.rows[index].sets[lane.key];c.fillStyle=lane.color;c.globalAlpha=age===0?.96:.12+(3-age)*.11;for(const cell of cells){const p=phaseProject(cell,n,lane);c.beginPath();c.arc(p.x,p.y,age===0?3.2:2.1,0,Math.PI*2);c.fill()}}
    c.globalAlpha=1;const current=g?r.rows[g-1].sets[lane.key]:[];outlineGroups(c,current,n,b,cell=>phaseProject(cell,n,lane),lane.color);
  }
  c.fillStyle="#a78bfa";c.font="600 13px Inter,system-ui,sans-serif";c.fillText(`Q° · temporal phase view · t−3 … t · generation ${g}`,188,590);
}
function drawTransitionRosette(c,r,g,n,b){
  const center={x:380,y:305},row=g?r.rows[g-1]:null,sets=row?row.sets:{births:[],survivals:[],deaths:[]},lanes=[{key:"births",angle:-Math.PI/2,label:"+90° · BIRTH",color:colors.births},{key:"survivals",angle:0,label:"0° · SURVIVE",color:colors.survivals},{key:"deaths",angle:Math.PI/2,label:"−90° · DEATH",color:colors.deaths}];
  c.strokeStyle="#294451";c.lineWidth=1;for(const radius of [80,145,210]){c.beginPath();c.arc(center.x,center.y,radius,0,Math.PI*2);c.stroke()}
  for(const lane of lanes){const ex=center.x+Math.cos(lane.angle)*238,ey=center.y+Math.sin(lane.angle)*238;c.strokeStyle=lane.color;c.lineWidth=2;c.beginPath();c.moveTo(center.x,center.y);c.lineTo(ex,ey);c.stroke();c.fillStyle=lane.color;c.font="600 12px Inter,system-ui,sans-serif";c.fillText(lane.label,Math.max(18,Math.min(635,ex-55)),Math.max(24,Math.min(600,ey)));
    for(const cell of sets[lane.key]){const[x,y]=cell,radial=74+145*(x+1)/(n+1),spread=(y/(n-1)-.5)*1.18,angle=lane.angle+spread,p={x:center.x+Math.cos(angle)*radial,y:center.y+Math.sin(angle)*radial};c.beginPath();c.arc(p.x,p.y,3.4,0,Math.PI*2);c.fill()}
  }
  c.fillStyle=colors.residual;c.beginPath();c.arc(center.x,center.y,19,0,Math.PI*2);c.fill();c.fillStyle="#071018";c.font="700 12px Inter,system-ui,sans-serif";c.fillText("Q°",center.x-9,center.y+4);c.fillStyle="#a78bfa";c.font="600 13px Inter,system-ui,sans-serif";c.fillText(`same event addresses · phase translation · ${b} · g${g}`,188,598);
}
function status(){const running=Boolean(timer),loop=loopPlayback.checked?" · loop on":"";$("playbackStatus").textContent=`${running?"Running":"Paused"}${loop} at generation ${generation.value} / ${generation.max}`}
function setPlayback(active){if(timer){clearInterval(timer);timer=null}if(active){playPause.textContent="Pause";timer=setInterval(()=>{const max=Number(generation.max);if(Number(generation.value)>=max){if(loopPlayback.checked){generation.value=0;update();return}setPlayback(false);return}generation.value=Number(generation.value)+1;update()},Number(speed.value))}else playPause.textContent="Start";status()}
function update(){
  const spec=activeSpec(),mode=document.querySelector('input[name="viewMode"]:checked').value,b=boundary.value,g=Number(generation.value),dynBoundary=mode==="view"?"finite-dead":b,r=run(spec,dynBoundary),dead=run(spec,"finite-dead"),layers=layersAt(r,dead,g,channel.value),flat=context($("flat")),cyl=context($("cylinder"));
  drawFlat(flat,layers,spec.size,b);
  const row=g?r.rows[g-1]:null,eventCells=row?[...row.sets.births,...row.sets.survivals,...row.sets.deaths]:r.states[0].live,componentCount=componentGroups(eventCells,spec.size,dynBoundary).length;
  if(projection.value==="four-plus-one")drawFourPlusOne(cyl,r,g,spec.size,dynBoundary);
  else if(projection.value==="phase-register")drawPhaseRegister(cyl,r,g,spec.size,dynBoundary);
  else if(projection.value==="transition-rosette")drawTransitionRosette(cyl,r,g,spec.size,dynBoundary);
  else drawCylinder(cyl,layers,spec.size,b);
  const isEvent=projection.value==="four-plus-one",isPhase=projection.value==="phase-register",isRosette=projection.value==="transition-rosette";
  $("projectionTitle").textContent=isEvent?"4+1 event register":isPhase?"Temporal phase register":isRosette?"Transition rosette":"Cylinder projection";
  $("generationValue").textContent=g;$("flatLabel").textContent=`${dynBoundary} · ${channel.value}`;
  $("cylinderLabel").textContent=isEvent?`${componentCount} components · identity + position`:isPhase?`${componentCount} components · +90° / 0° / −90°`:isRosette?`${componentCount} components · joined phase view`:`projection on ${b}`;
  $("live").textContent=r.states[g].live.length;$("eventCount").textContent=layers.reduce((n,l)=>n+l.cells.length,0);$("seamBirths").textContent=row?row.seamBirths:0;
  const residual=symmetricDifference(r.states[g].live,dead.states[g].live).length;$("residual").textContent=residual?`Δ ${residual} cells`:"0 · same state";$("residual").style.color=residual?colors.deaths:"#4ade80";$("quaternion").textContent=row?`${row.quaternion.scalar} + ${row.quaternion.i}i + ${row.quaternion.j}j + ${row.quaternion.k}k`:"0";
  $("modeNote").innerHTML=mode==="view"?"<b>VIEW WRAP:</b> finite-dead dynamics are unchanged; only the representation is placed on a cylinder.":"<b>DYNAMICS WRAP:</b> neighbours cross the declared seam; the state trajectory is compared cell-for-cell with finite-dead.";
  if(P&&typeof window.dispatchEvent==="function")window.dispatchEvent(new CustomEvent("lifecrystal:render",{detail:P.buildSnapshot(r,dead,g,{fixture:spec.label,historyWindow:$("crystalHistory")?$("crystalHistory").value:60,displayBoundary:b,dynamicsMode:mode})}));status();
}
function resetHorizon(){setPlayback(false);generation.max=activeSpec().horizon;generation.value=0;update()}
fixture.onchange=resetHorizon;runLength.onchange=resetHorizon;loopPlayback.onchange=status;boundary.onchange=update;channel.onchange=update;projection.onchange=update;componentOutlines.onchange=update;generation.oninput=update;speed.onchange=()=>{if(timer)setPlayback(true)};for(const x of document.querySelectorAll('input[name="viewMode"]'))x.onchange=update;
if($("crystalHistory"))$("crystalHistory").onchange=update;
playPause.onclick=()=>setPlayback(!timer);$("stepForward").onclick=()=>{setPlayback(false);generation.value=Number(generation.value)>=Number(generation.max)&&loopPlayback.checked?0:Math.min(Number(generation.max),Number(generation.value)+1);update()};$("reset").onclick=()=>{setPlayback(false);generation.value=0;update()};
observeMode.onclick=()=>{setPlayback(false);fixture.value="R-PENTOMINO";runLength.value="1000";loopPlayback.checked=true;channel.value="all";projection.value="four-plus-one";generation.max=activeSpec().horizon;generation.value=0;update();setPlayback(true)};
if($("boundaryDemo"))$("boundaryDemo").onclick=()=>{setPlayback(false);fixture.value="GLIDER-X-SEAM";boundary.value="cylinder-x";for(const radio of document.querySelectorAll('input[name="viewMode"]'))radio.checked=radio.value==="dynamics";generation.max=activeSpec().horizon;generation.value=10;channel.value="all";projection.value="four-plus-one";if($("boundaryReading"))$("boundaryReading").value="event-skin";update();if($("boundaryReading"))$("boundaryReading").dispatchEvent(new Event("change"))};
$("decision").textContent=R.decision;$("gates").innerHTML=Object.entries(R.gates).map(([k,v])=>`<div class="gate"><span>${k.replace(/([A-Z])/g," $1")}</span><b>${v?"PASS":"FAIL"}</b></div>`).join("");fixture.value="BEEHIVE-BLOOM";boundary.value="cylinder-x";channel.value="all";projection.value="four-plus-one";componentOutlines.checked=true;resetHorizon();generation.value=120;update();
})();
