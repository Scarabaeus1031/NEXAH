(function(root,factory){
  const api=factory();
  if(typeof module==="object"&&module.exports)module.exports=api;
  root.ThreeDomainEngine=api;
}(typeof globalThis!=="undefined"?globalThis:this,function(){
  "use strict";
  const MODELS=["chemistry","life","physics"];
  const BOUNDARIES=["open","cylinder-x"];
  const idx=(x,y,n)=>y*n+x;
  const mod=(x,n)=>(x%n+n)%n;
  function hash01(seed,g,k,c=0){let x=(seed^Math.imul(g+1,0x9e3779b1)^Math.imul(k+1,0x85ebca6b)^Math.imul(c+1,0xc2b2ae35))>>>0;x^=x>>>16;x=Math.imul(x,0x7feb352d);x^=x>>>15;x=Math.imul(x,0x846ca68b);x^=x>>>16;return(x>>>0)/4294967296}
  function mapped(x,y,n,boundary){if(boundary==="cylinder-x")x=mod(x,n);if(x<0||y<0||x>=n||y>=n)return null;return[x,y]}
  function seededBinary(n,seed,density){const a=new Uint8Array(n*n);for(let k=0;k<a.length;k++)a[k]=hash01(seed,0,k)<density?1:0;return a}
  function createChemistry(n,seed,boundary){
    const u=new Float64Array(n*n).fill(1),v=new Float64Array(n*n),r=Math.max(2,Math.floor(n/9)),cx=Math.floor(n/2),cy=Math.floor(n/2);
    for(let y=cy-r;y<=cy+r;y++)for(let x=cx-r;x<=cx+r;x++){const k=idx(x,y,n);u[k]=.48+.04*hash01(seed,1,k);v[k]=.24+.08*hash01(seed,2,k)}
    for(let p=0;p<4;p++){const px=3+Math.floor(hash01(seed,3,p)*Math.max(1,n-6)),py=3+Math.floor(hash01(seed,4,p)*Math.max(1,n-6));for(let y=py-1;y<=py+1;y++)for(let x=px-1;x<=px+1;x++){const k=idx(x,y,n);u[k]=.52;v[k]=.31}}
    return{model:"chemistry",n,seed,boundary,generation:0,u,v,params:{du:.16,dv:.08,feed:.0545,kill:.062,dt:1,substeps:5}};
  }
  function chemSample(a,x,y,s){const m=mapped(x,y,s.n,s.boundary);if(m)return a[idx(m[0],m[1],s.n)];const cx=Math.max(0,Math.min(s.n-1,x)),cy=Math.max(0,Math.min(s.n-1,y));return a[idx(cx,cy,s.n)]}
  function stepChemistry(s){
    const n=s.n,p=s.params;let u=s.u,v=s.v;
    for(let q=0;q<p.substeps;q++){
      const nu=new Float64Array(n*n),nv=new Float64Array(n*n);
      for(let y=0;y<n;y++)for(let x=0;x<n;x++){
        const k=idx(x,y,n),uc=u[k],vc=v[k];let lu=-uc,lv=-vc;
        for(const [dx,dy,w]of [[1,0,.2],[-1,0,.2],[0,1,.2],[0,-1,.2],[1,1,.05],[-1,1,.05],[1,-1,.05],[-1,-1,.05]]){lu+=w*chemSample(u,x+dx,y+dy,s);lv+=w*chemSample(v,x+dx,y+dy,s)}
        const reaction=uc*vc*vc;nu[k]=Math.max(0,Math.min(1,uc+(p.du*lu-reaction+p.feed*(1-uc))*p.dt));nv[k]=Math.max(0,Math.min(1,vc+(p.dv*lv+reaction-(p.feed+p.kill)*vc)*p.dt));
      }
      u=nu;v=nv;
    }
    return{...s,generation:s.generation+1,u,v};
  }
  function createLife(n,seed,boundary){
    const cells=seededBinary(n,seed,.19);
    for(let x=0;x<n;x++){cells[idx(x,0,n)]=hash01(seed,7,x)<.34?1:0;cells[idx(x,n-1,n)]=hash01(seed,8,x)<.34?1:0}
    return{model:"life",n,seed,boundary,generation:0,cells};
  }
  function stepLife(s){
    const next=new Uint8Array(s.n*s.n);
    for(let y=0;y<s.n;y++)for(let x=0;x<s.n;x++){
      let count=0;for(let dy=-1;dy<=1;dy++)for(let dx=-1;dx<=1;dx++){if(!dx&&!dy)continue;const m=mapped(x+dx,y+dy,s.n,s.boundary);if(m)count+=s.cells[idx(m[0],m[1],s.n)]}
      const k=idx(x,y,s.n);next[k]=count===3||(count===2&&s.cells[k])?1:0;
    }
    return{...s,generation:s.generation+1,cells:next};
  }
  function createPhysics(n,seed,boundary){const spins=new Int8Array(n*n);for(let k=0;k<spins.length;k++)spins[k]=hash01(seed,9,k)<.5?-1:1;return{model:"physics",n,seed,boundary,generation:0,spins,temperature:1.85}}
  function stepPhysics(s){
    const spins=new Int8Array(s.spins),n=s.n,total=n*n,g=s.generation;
    for(let q=0;q<total;q++){
      const k=Math.floor(hash01(s.seed,g,q,11)*total),x=k%n,y=Math.floor(k/n);let field=0;
      for(const[dx,dy]of[[1,0],[-1,0],[0,1],[0,-1]]){const m=mapped(x+dx,y+dy,n,s.boundary);if(m)field+=spins[idx(m[0],m[1],n)]}
      const dE=2*spins[k]*field;if(dE<=0||hash01(s.seed,g,q,12)<Math.exp(-dE/s.temperature))spins[k]*=-1;
    }
    return{...s,generation:g+1,spins};
  }
  function createModel(model,n=36,seed=34017,boundary="open"){if(!MODELS.includes(model))throw new TypeError("unknown model");if(!BOUNDARIES.includes(boundary))throw new TypeError("unknown boundary");return model==="chemistry"?createChemistry(n,seed,boundary):model==="life"?createLife(n,seed,boundary):createPhysics(n,seed,boundary)}
  function step(model){return model.model==="chemistry"?stepChemistry(model):model.model==="life"?stepLife(model):stepPhysics(model)}
  function binary(model,threshold=.22){if(model.model==="chemistry"){const out=new Uint8Array(model.n*model.n);for(let k=0;k<out.length;k++)out[k]=model.v[k]>=threshold?1:0;return out}if(model.model==="life")return new Uint8Array(model.cells);const out=new Uint8Array(model.n*model.n);for(let k=0;k<out.length;k++)out[k]=model.spins[k]>0?1:0;return out}
  function events(previous,current){if(previous.length!==current.length)throw new TypeError("comparable fields required");const positive=[],hold=[],negative=[],all=[];for(let k=0;k<current.length;k++){if(!previous[k]&&current[k]){positive.push(k);all.push(k)}else if(previous[k]&&current[k]){hold.push(k);all.push(k)}else if(previous[k]&&!current[k]){negative.push(k);all.push(k)}}return{all,positive,hold,negative}}
  function transitionLedger(previous,current){
    if(previous.length!==current.length)throw new TypeError("comparable fields required");
    const event=events(previous,current),c00=current.length-event.all.length,c01=event.positive.length,c10=event.negative.length,c11=event.hold.length,total=current.length;
    return{c00,c01,c10,c11,total,exact:c00+c01+c10+c11===total,previous:{zero:c00+c01,one:c10+c11},current:{zero:c00+c10,one:c01+c11}};
  }
  function topology(field,n,boundary="open"){
    const seen=new Uint8Array(field.length);let beta0=0;
    for(let start=0;start<field.length;start++)if(field[start]&&!seen[start]){beta0++;seen[start]=1;const queue=[start];while(queue.length){const k=queue.pop(),x=k%n,y=Math.floor(k/n);for(const[dx,dy]of[[1,0],[-1,0],[0,1],[0,-1]]){const m=mapped(x+dx,y+dy,n,boundary);if(!m)continue;const q=idx(m[0],m[1],n);if(field[q]&&!seen[q]){seen[q]=1;queue.push(q)}}}}
    const vertices=new Set(),edges=new Set();let faces=0;const vk=(x,y)=>`${boundary==="cylinder-x"?mod(x,n):x},${y}`;
    for(let y=0;y<n;y++)for(let x=0;x<n;x++)if(field[idx(x,y,n)]){faces++;const vs=[[x,y],[x+1,y],[x+1,y+1],[x,y+1]].map(([a,b])=>vk(a,b));vs.forEach(v=>vertices.add(v));for(let e=0;e<4;e++){const pair=[vs[e],vs[(e+1)%4]].sort();edges.add(pair.join("|"))}}
    const chi=vertices.size-edges.size+faces,beta1=Math.max(0,beta0-chi);return{beta0,beta1,chi,active:faces};
  }
  function residual(a,b){const out=[];for(let k=0;k<a.length;k++)if(a[k]!==b[k])out.push(k);return out}
  function createPair(model,options={}){const n=options.n||36,seed=options.seed||34017,boundary=options.boundary||"cylinder-x";return{model,boundary,threshold:options.threshold||.22,current:createModel(model,n,seed,boundary),baseline:createModel(model,n,seed,"open"),previous:null,previousBaseline:null}}
  function stepPair(pair){pair.previous=pair.current;pair.previousBaseline=pair.baseline;pair.current=step(pair.current);pair.baseline=step(pair.baseline);return pair}
  function observe(pair){const now=binary(pair.current,pair.threshold),base=binary(pair.baseline,pair.threshold),before=pair.previous?binary(pair.previous,pair.threshold):new Uint8Array(now.length),event=events(before,now);return{model:pair.model,generation:pair.current.generation,n:pair.current.n,boundary:pair.boundary,raw:pair.current.model==="chemistry"?pair.current.v:pair.current.model==="life"?pair.current.cells:pair.current.spins,binary:now,events:event,ledger:transitionLedger(before,now),topology:topology(now,pair.current.n,pair.boundary),residual:residual(now,base),controller:{model:pair.model,boundary:pair.boundary,generation:pair.current.generation,threshold:pair.model==="chemistry"?pair.threshold:null}}}
  return Object.freeze({MODELS,BOUNDARIES,hash01,mapped,createModel,step,binary,events,transitionLedger,topology,residual,createPair,stepPair,observe});
}));
