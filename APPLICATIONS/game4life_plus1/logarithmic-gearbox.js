(function(root,factory){
  const api=factory();
  if(typeof module==="object"&&module.exports) module.exports=api;
  else root.LogarithmicGearbox=api;
})(typeof globalThis!=="undefined"?globalThis:this,function(){
  "use strict";
  const PHI=(1+Math.sqrt(5))/2;
  const BASES=Object.freeze({
    two:Object.freeze({id:"two",label:"2",value:2,step:"×2"}),
    euler:Object.freeze({id:"euler",label:"e",value:Math.E,step:"×e"}),
    phi:Object.freeze({id:"phi",label:"φ",value:PHI,step:"×φ"}),
    root2:Object.freeze({id:"root2",label:"√2",value:Math.SQRT2,step:"×√2"}),
    napier:Object.freeze({id:"napier",label:"1−10⁻⁷",value:1-1e-7,step:"×(1−10⁻⁷)"})
  });
  const ZERO_INSERTION=Object.freeze(Array.from({length:8},(_,zeroCount)=>Math.pow(10,zeroCount+1)+1));
  function nearlyEqual(a,b,tolerance=1e-11){return Math.abs(a-b)<=tolerance*Math.max(1,Math.abs(a),Math.abs(b));}
  function isPrime(value){if(!Number.isInteger(value)||value<2)return false;for(let d=2;d*d<=value;d+=1)if(value%d===0)return false;return true;}
  function assertBase(id){const base=BASES[id];if(!base)throw new RangeError(`Unknown logarithmic base: ${id}`);return base;}
  function power(base,n){return Math.pow(base.value,n);}
  function naturalHandle(){return [{symbol:"π",constant:Math.PI},{symbol:"φ",constant:PHI},{symbol:"√2",constant:Math.SQRT2}].map(item=>Object.freeze({...item,coordinate:Math.log(item.constant),reconstructed:Math.exp(Math.log(item.constant))}));}
  function napierLimit(){const steps=10000000,factor=BASES.napier.value,ratio=Math.pow(factor,steps);return Object.freeze({steps,start:steps,factor,ratio,value:steps*ratio,targetRatio:Math.exp(-1)});}
  function zeroInsertion(){
    const sequence=ZERO_INSERTION.slice();
    return Object.freeze({sequence,formula:"a_n=10^(n+1)+1",recurrence:"a_(n+1)=10*a_n-9",target:100000001,targetZeroCount:7,addressWindow:Object.freeze([97,98,99,100,101]),continuation:Object.freeze([109,110,111]),pass:sequence.every((value,n)=>value===Math.pow(10,n+1)+1)&&(10*sequence[6]-9===sequence[7])});
  }
  function primeAxis(){
    const hinge=Object.freeze({id:"hinge",left:97,center:99,right:101,radius:2});
    const janus=Object.freeze({id:"janus",left:97,center:100,right:103,radius:3});
    const primeIndexPath=Object.freeze([73,79,83,89,97,101]);
    const channel=Object.freeze([101,202,404,808,1616,3232]);
    return Object.freeze({
      hinge,janus,centerShift:janus.center-hinge.center,
      consecutivePrimeGaps:Object.freeze([101-97,103-101]),
      primeIndexPath,channel,zeroInsertionJoin:Object.freeze({index:1,value:ZERO_INSERTION[1]}),
      pass:[97,101,103].every(isPrime)&&hinge.center===(hinge.left+hinge.right)/2&&janus.center===(janus.left+janus.right)/2&&channel.every((value,index)=>index===0||value===2*channel[index-1])&&ZERO_INSERTION[1]===101
    });
  }
  function base50Mirror(value=53){
    if(!Number.isFinite(value))throw new TypeError("Base-50 mirror input must be finite");
    const sum=150,mirror=sum-value,fixedPoint=sum/2;
    return Object.freeze({value,mirror,sum,fixedPoint,formula:"J_50(x)=150-x",pass:nearlyEqual(value+mirror,sum)&&nearlyEqual(sum-fixedPoint,fixedPoint)});
  }
  function primeChannelProjection(generation){
    if(!Number.isInteger(generation)||generation<0)throw new RangeError("Prime-channel generation must be a non-negative integer");
    const axis=primeAxis(),k=generation%axis.channel.length,primeValue=axis.primeIndexPath[k],channelValue=axis.channel[k];
    return Object.freeze({generation,k,primeOrdinal:21+k,primeValue,channelValue,base50GateActive:primeValue===97,formula:"k=g mod 6; c_k=101*2^k"});
  }
  function lifeClockProjection(generation){
    if(!Number.isInteger(generation)||generation<0)throw new RangeError("Life generation must be a non-negative integer");
    const phase=generation%8;
    return Object.freeze({generation,phase,exponent:phase,zeroCount:phase,axisMode:generation%2===0?"hinge":"janus",primeChannel:primeChannelProjection(generation),formula:"n=g mod 8; axis=g mod 2; k=g mod 6"});
  }
  function buildState(baseId="two",n=0){
    if(!Number.isInteger(n))throw new TypeError("Exponent address n must be an integer");
    const base=assertBase(baseId),magnitude=power(base,n),nextMagnitude=power(base,n+1),radius=Math.abs(n),pValue=power(base,radius),qValue=power(base,-radius);
    return Object.freeze({schema:"nexah.game4life.logarithmic-gearbox.v1",base,address:Object.freeze({current:n,next:n+1}),geometric:Object.freeze({current:magnitude,next:nextMagnitude,multiplier:base.value}),keystone:Object.freeze({arithmetic:0,geometric:1,pass:power(base,0)===1}),mirror:Object.freeze({pExponent:radius,bExponent:0,qExponent:-radius,pValue,bValue:1,qValue,product:pValue*qValue,pass:nearlyEqual(pValue*qValue,1)}),returnCheck:Object.freeze({addressPass:n+1-n===1,valuePass:nearlyEqual(nextMagnitude,magnitude*base.value),keystonePass:power(base,0)===1}),naturalHandle:Object.freeze(naturalHandle()),napier:napierLimit(),zeroInsertion:zeroInsertion(),primeAxis:primeAxis(),base50Mirror:base50Mirror()});
  }
  function formatNumber(value){const a=Math.abs(value);if(value===1)return"1";if(a>=10000||(a>0&&a<0.0001))return value.toExponential(3).replace("e+","e");return value.toLocaleString("en-US",{maximumFractionDigits:6,useGrouping:false});}
  function renderRail(container,base,activeN){container.innerHTML="";for(let n=0;n<=7;n+=1){const cell=document.createElement("div");cell.className="gear-cell"+(n===activeN?" is-active":"")+(n===0?" is-keystone":"");cell.dataset.n=String(n);cell.innerHTML=`<span>${n}</span><b>${formatNumber(power(base,n))}</b>`;container.appendChild(cell);}}
  function renderZeroLadder(container,activeZeroCount){container.innerHTML="";ZERO_INSERTION.forEach((value,zeroCount)=>{const cell=document.createElement("div");cell.className="zero-ladder-cell"+(zeroCount===activeZeroCount?" is-active":"");cell.innerHTML=`<span>${zeroCount} zero${zeroCount===1?"":"s"}</span><b>${value}</b>`;container.appendChild(cell);});}
  function init(doc=document){
    const host=doc.getElementById("logGearbox");if(!host)return null;
    const $=id=>doc.getElementById(id),slider=$("gearExponent"),zeroSlider=$("gearZeroCount"),lifeSync=$("gearLifeSync"),lifeGeneration=$("generation"),state={baseId:"two",n:Number(slider.value),zeroCount:Number(zeroSlider.value),zeroInsertion:true,axisMode:"hinge",channelIndex:0,lifeSync:true,lifeGeneration:lifeGeneration?Number(lifeGeneration.value):0};
    const render=()=>{const model=buildState(state.baseId,state.n),zeroValue=model.zeroInsertion.sequence[state.zeroCount],axis=model.primeAxis[state.axisMode],channel=primeChannelProjection(state.lifeSync?state.lifeGeneration:state.channelIndex);host.dataset.base=model.base.id;host.dataset.clock=state.lifeSync?"life":"local";$("gearExponentValue").textContent=`+${state.n}`;$("gearArithmeticReadout").textContent=`${state.n} → ${state.n+1}`;$("gearGeometricReadout").textContent=`${formatNumber(model.geometric.current)} → ${formatNumber(model.geometric.next)}`;$("gearOperatorReadout").textContent=`+1  ⇄  ${model.base.step}`;$("gearFormula").textContent=`Gₙ = ${model.base.label}ⁿ · log${model.base.label}(Gₙ) = n`;renderRail($("gearRail"),model.base,state.n);$("gearP").textContent=`+${model.mirror.pExponent} · ${formatNumber(model.mirror.pValue)}`;$("gearQ").textContent=`${model.mirror.qExponent} · ${formatNumber(model.mirror.qValue)}`;$("gearMirrorProduct").textContent=`${formatNumber(model.mirror.pValue)} × ${formatNumber(model.mirror.qValue)} = ${formatNumber(model.mirror.product)}`;$("gearReturnStatus").textContent=model.returnCheck.addressPass&&model.returnCheck.valuePass&&model.returnCheck.keystonePass?"3/3 RETURN CHECKS PASS":"RETURN CHECK FAILED";$("gearZeroGate").classList.toggle("is-hidden",!state.zeroInsertion);$("gearZeroCountValue").textContent=String(state.zeroCount);$("gearZeroValue").textContent=String(zeroValue);$("gearZeroChamber").innerHTML="<i>0</i>".repeat(state.zeroCount);$("gearZeroChamber").classList.toggle("is-empty",state.zeroCount===0);renderZeroLadder($("gearZeroLadder"),state.zeroCount);$("gearNapier").classList.toggle("is-active",model.base.id==="napier");$("gearNapierValue").textContent=`10⁷(1−10⁻⁷)¹⁰⁰⁰⁰⁰⁰ = ${formatNumber(model.napier.value)}`;$("gearPrimeAxis").dataset.mode=state.axisMode;$("gearAxisName").textContent=state.axisMode==="hinge"?"XI HINGE":"JANUS AXIS";$("gearAxisEquation").textContent=`${axis.left} — ${axis.center} — ${axis.right}`;$("gearAxisRadius").textContent=`±${axis.radius}`;$("gearPrimeChannelReadout").textContent=`k${channel.k} · P${channel.primeOrdinal}=${channel.primeValue} · c${channel.k}=${channel.channelValue}`;doc.querySelectorAll("[data-prime-step]").forEach(node=>node.classList.toggle("is-active",Number(node.dataset.primeStep)===channel.k));doc.querySelectorAll("[data-channel-step]").forEach(node=>node.classList.toggle("is-active",Number(node.dataset.channelStep)===channel.k));$("gearBase50Lane").classList.toggle("is-gate-active",channel.base50GateActive);$("gearCoupler").dataset.mode=state.lifeSync?"life":"local";$("gearLifeGeneration").textContent=state.lifeSync?`g${state.lifeGeneration}`:"local";$("gearLifePhase").textContent=`n${state.n}`;$("gearLifeZero").textContent=String(zeroValue);$("gearLifeAxis").textContent=state.axisMode==="hinge"?"99":"100";doc.querySelectorAll("[data-gear-base]").forEach(button=>{const pressed=button.dataset.gearBase===state.baseId;button.classList.toggle("is-active",pressed);button.setAttribute("aria-pressed",String(pressed));});doc.querySelectorAll("[data-axis-mode]").forEach(button=>{const pressed=button.dataset.axisMode===state.axisMode;button.classList.toggle("is-active",pressed);button.setAttribute("aria-pressed",String(pressed));});return model;};
    const detach=()=>{state.lifeSync=false;lifeSync.checked=false;};
    const syncFromLife=generation=>{const projection=lifeClockProjection(Number(generation));state.lifeGeneration=projection.generation;state.n=projection.exponent;state.zeroCount=projection.zeroCount;state.axisMode=projection.axisMode;state.channelIndex=projection.primeChannel.k;slider.value=String(state.n);zeroSlider.value=String(state.zeroCount);return render();};
    doc.querySelectorAll("[data-gear-base]").forEach(button=>button.addEventListener("click",()=>{state.baseId=button.dataset.gearBase;render();}));doc.querySelectorAll("[data-axis-mode]").forEach(button=>button.addEventListener("click",()=>{detach();state.axisMode=button.dataset.axisMode;render();}));slider.addEventListener("input",()=>{detach();state.n=Number(slider.value);state.channelIndex=state.n%6;render();});zeroSlider.addEventListener("input",()=>{detach();state.zeroCount=Number(zeroSlider.value);render();});$("gearStep").addEventListener("click",()=>{if(state.lifeSync&&$("stepForward")){$("stepForward").click();return;}state.n=(state.n+1)%8;state.zeroCount=state.n;state.axisMode=state.n%2===0?"hinge":"janus";state.channelIndex=(state.channelIndex+1)%6;slider.value=String(state.n);zeroSlider.value=String(state.zeroCount);render();});$("gearInsertZero").addEventListener("click",()=>{if(state.lifeSync&&$("stepForward")){$("stepForward").click();return;}state.zeroCount=(state.zeroCount+1)%8;zeroSlider.value=String(state.zeroCount);render();});$("gearZeroToggle").addEventListener("change",event=>{state.zeroInsertion=event.target.checked;render();});lifeSync.addEventListener("change",()=>{state.lifeSync=lifeSync.checked;if(state.lifeSync)syncFromLife(lifeGeneration?Number(lifeGeneration.value):state.lifeGeneration);else render();});if(typeof window!=="undefined")window.addEventListener("lifecrystal:render",event=>{if(state.lifeSync&&event.detail)syncFromLife(event.detail.generation);});const model=state.lifeSync?syncFromLife(state.lifeGeneration):render();return Object.freeze({state,render,syncFromLife,model});
  }
  if(typeof document!=="undefined"){if(document.readyState==="loading")document.addEventListener("DOMContentLoaded",()=>init(document),{once:true});else init(document);}
  return Object.freeze({BASES,ZERO_INSERTION,buildState,zeroInsertion,primeAxis,base50Mirror,primeChannelProjection,lifeClockProjection,isPrime,naturalHandle,napierLimit,nearlyEqual,formatNumber,init});
});
