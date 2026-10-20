(()=>{"use strict";
const names=["chemistry","life","physics"],ids={chemistry:"Chemistry",life:"Life",physics:"Physics"};
const colors={c00:"#647786",c01:"#22d3ee",c10:"#fb7185",c11:"#f5bf42",line:"#294451",muted:"#91a8b5",text:"#edf8fb",violet:"#a78bfa"};
const pct=(value,total)=>`${(100*value/Math.max(1,total)).toFixed(1)}%`;
function label(ctx,text,x,y,color=colors.text,size=12,align="left"){ctx.fillStyle=color;ctx.font=`600 ${size}px Inter,system-ui,sans-serif`;ctx.textAlign=align;ctx.fillText(text,x,y);ctx.textAlign="left"}
function rect(ctx,x,y,w,h,color,code,count,total){
  if(w<=0||h<=0)return;ctx.fillStyle=color;ctx.globalAlpha=.72;ctx.fillRect(x,y,w,h);ctx.globalAlpha=1;ctx.strokeStyle="#061019";ctx.lineWidth=2;ctx.strokeRect(x,y,w,h);
  if(w>62&&h>42){label(ctx,code,x+w/2,y+h/2-3,"#061019",13,"center");label(ctx,`${count} · ${pct(count,total)}`,x+w/2,y+h/2+15,"#061019",10,"center")}
}
function area(ctx,L){
  const x=32,y=68,w=276,h=330,total=Math.max(1,L.total),top=L.previous.zero/total*h,bottom=h-top;
  label(ctx,"EXACT AREA",x,y-24,colors.muted,10);label(ctx,"source state t",x+w,y-24,colors.muted,10,"right");
  const topSplit=L.previous.zero?L.c00/L.previous.zero*w:0,bottomSplit=L.previous.one?L.c10/L.previous.one*w:0;
  rect(ctx,x,y,topSplit,top,colors.c00,"C₀₀",L.c00,L.total);rect(ctx,x+topSplit,y,w-topSplit,top,colors.c01,"C₀₁",L.c01,L.total);
  rect(ctx,x,y+top,bottomSplit,bottom,colors.c10,"C₁₀",L.c10,L.total);rect(ctx,x+bottomSplit,y+top,w-bottomSplit,bottom,colors.c11,"C₁₁",L.c11,L.total);
  ctx.strokeStyle="#bdd2da";ctx.lineWidth=1.2;ctx.strokeRect(x,y,w,h);label(ctx,"0 at t",x-7,y+Math.max(12,top/2),colors.muted,10,"right");label(ctx,"1 at t",x-7,y+top+Math.max(12,bottom/2),colors.muted,10,"right");
}
function channel(ctx,x1,y1,x2,y2,count,total,color){if(!count)return;ctx.save();ctx.strokeStyle=color;ctx.globalAlpha=.42+Math.min(.45,count/Math.max(1,total)*2);ctx.lineWidth=Math.max(1.5,52*count/Math.max(1,total));ctx.beginPath();ctx.moveTo(x1,y1);ctx.bezierCurveTo(x1+72,y1,x2-72,y2,x2,y2);ctx.stroke();ctx.restore()}
function pillar(ctx,x,y,w,h,zero,one,total,title){const split=zero/Math.max(1,total)*h;ctx.fillStyle=colors.c00;ctx.globalAlpha=.72;ctx.fillRect(x,y,w,split);ctx.fillStyle=colors.c11;ctx.fillRect(x,y+split,w,h-split);ctx.globalAlpha=1;ctx.strokeStyle="#bdd2da";ctx.lineWidth=1.2;ctx.strokeRect(x,y,w,h);label(ctx,title,x+w/2,y-13,colors.text,12,"center");label(ctx,`0 · ${zero}`,x+w/2,y+Math.max(16,split/2),"#061019",10,"center");if(h-split>22)label(ctx,`1 · ${one}`,x+w/2,y+split+(h-split)/2,"#061019",10,"center")}
function graph(ctx,L){
  const sx=390,tx=642,y=79,w=24,h=292,total=Math.max(1,L.total),s0=L.previous.zero/total*h,t0=L.current.zero/total*h;
  label(ctx,"FOUR-CHANNEL GRAPH",sx,y-35,colors.muted,10);label(ctx,"weighted relation",tx+w,y-35,colors.muted,10,"right");
  const sy0=y+s0/2,sy1=y+s0+(h-s0)/2,ty0=y+t0/2,ty1=y+t0+(h-t0)/2;
  channel(ctx,sx+w,sy0,tx,ty0,L.c00,total,colors.c00);channel(ctx,sx+w,sy0,tx,ty1,L.c01,total,colors.c01);channel(ctx,sx+w,sy1,tx,ty0,L.c10,total,colors.c10);channel(ctx,sx+w,sy1,tx,ty1,L.c11,total,colors.c11);
  pillar(ctx,sx,y,w,h,L.previous.zero,L.previous.one,total,"t");pillar(ctx,tx,y,w,h,L.current.zero,L.current.one,total,"t+1");
  const ly=410;ctx.strokeStyle=colors.violet;ctx.lineWidth=2;ctx.beginPath();ctx.moveTo(sx,ly);ctx.lineTo(tx+w,ly);ctx.stroke();label(ctx,"Q°",sx-13,ly+4,colors.violet,11,"right");
}
function draw(name,snapshot){
  const canvas=document.getElementById(`montage${ids[name]}`);if(!canvas||!snapshot.ledger)return;const ctx=canvas.getContext("2d"),L=snapshot.ledger;ctx.clearRect(0,0,canvas.width,canvas.height);ctx.fillStyle="#040a10";ctx.fillRect(0,0,canvas.width,canvas.height);area(ctx,L);graph(ctx,L);label(ctx,`${snapshot.model} · ${snapshot.boundary} · generation ${snapshot.generation}`,32,470,colors.muted,10);label(ctx,L.exact?"EXACT PARTITION":"LEDGER ERROR",668,470,L.exact?"#4ade80":colors.c10,10,"right");
  const out=document.getElementById(`montage${ids[name]}Equation`);if(out)out.textContent=`${L.c00} + ${L.c01} + ${L.c10} + ${L.c11} = ${L.total} · t[0:${L.previous.zero},1:${L.previous.one}] → t+1[0:${L.current.zero},1:${L.current.one}]`;
}
window.addEventListener("threedomain:render",event=>{for(const name of names)draw(name,event.detail.snapshots[name])});
})();
