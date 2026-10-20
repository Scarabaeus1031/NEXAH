const assert=require("node:assert/strict");
const gear=require("./logarithmic-gearbox.js");
let passed=0;
function test(name,fn){fn();passed+=1;console.log(`PASS ${name}`);}
for(const id of Object.keys(gear.BASES)){
  test(`${id}: keystone 0 maps to 1`,()=>assert.equal(gear.buildState(id,0).geometric.current,1));
  test(`${id}: +1 equals multiplication by base`,()=>{const s=gear.buildState(id,3);assert.ok(gear.nearlyEqual(s.geometric.next,s.geometric.current*s.base.value));});
  test(`${id}: P/Q mirror product returns 1`,()=>assert.ok(gear.buildState(id,-4).mirror.pass));
}
test("natural log handle reconstructs pi phi and root2",()=>{for(const item of gear.naturalHandle())assert.ok(gear.nearlyEqual(item.constant,item.reconstructed));});
test("Napier ten-million-step ratio approaches e^-1",()=>{const n=gear.napierLimit();assert.ok(Math.abs(n.ratio-n.targetRatio)<2e-8);});
test("zero insertion ladder reaches 100000001",()=>{const z=gear.buildState("two",0).zeroInsertion;assert.deepEqual(z.sequence,[11,101,1001,10001,100001,1000001,10000001,100000001]);assert.equal(z.target,100000001);assert.equal(z.pass,true);});
test("zero insertion closed form and recurrence agree",()=>{const z=gear.zeroInsertion();z.sequence.forEach((value,n)=>assert.equal(value,10**(n+1)+1));for(let n=0;n<z.sequence.length-1;n+=1)assert.equal(10*z.sequence[n]-9,z.sequence[n+1]);});
test("decimal boundary and 110 111 continuation are retained",()=>{const z=gear.zeroInsertion();assert.deepEqual(z.addressWindow,[97,98,99,100,101]);assert.deepEqual(z.continuation,[109,110,111]);});
test("XI hinge and Janus axis keep distinct exact centers",()=>{const a=gear.primeAxis();assert.deepEqual(a.hinge,{id:"hinge",left:97,center:99,right:101,radius:2});assert.deepEqual(a.janus,{id:"janus",left:97,center:100,right:103,radius:3});assert.equal(a.centerShift,1);assert.equal(a.pass,true);});
test("prime-index approach and selected 101 doubling channel are retained",()=>{const a=gear.primeAxis();assert.deepEqual(a.primeIndexPath,[73,79,83,89,97,101]);assert.deepEqual(a.channel,[101,202,404,808,1616,3232]);assert.deepEqual(a.consecutivePrimeGaps,[4,2]);assert.deepEqual(a.zeroInsertionJoin,{index:1,value:101});});
test("base-50 mirror pairs 53 and 97 around fixed point 75",()=>{const m=gear.base50Mirror(53);assert.equal(m.mirror,97);assert.equal(m.fixedPoint,75);assert.equal(m.pass,true);assert.equal(gear.base50Mirror(75).mirror,75);});
test("prime channel follows generation mod 6 and opens the Base-50 gate at 97",()=>{assert.deepEqual(gear.primeChannelProjection(2),{generation:2,k:2,primeOrdinal:23,primeValue:83,channelValue:404,base50GateActive:false,formula:"k=g mod 6; c_k=101*2^k"});assert.deepEqual(gear.primeChannelProjection(4),{generation:4,k:4,primeOrdinal:25,primeValue:97,channelValue:1616,base50GateActive:true,formula:"k=g mod 6; c_k=101*2^k"});assert.equal(gear.primeChannelProjection(6).k,0);});
test("Life clock projects every generation onto the eight-step gearbox",()=>{const a=gear.lifeClockProjection(120),b=gear.lifeClockProjection(121),c=gear.lifeClockProjection(127),d=gear.lifeClockProjection(128);assert.deepEqual([a.phase,b.phase,c.phase,d.phase],[0,1,7,0]);assert.deepEqual([a.axisMode,b.axisMode,c.axisMode,d.axisMode],["hinge","janus","janus","hinge"]);assert.deepEqual([a.primeChannel.k,b.primeChannel.k,c.primeChannel.k,d.primeChannel.k],[0,1,1,2]);assert.equal(a.formula,"n=g mod 8; axis=g mod 2; k=g mod 6");});
test("Life clock rejects invalid generations",()=>{assert.throws(()=>gear.lifeClockProjection(-1),RangeError);assert.throws(()=>gear.lifeClockProjection(1.5),RangeError);assert.throws(()=>gear.primeChannelProjection(-1),RangeError);});
test("unknown base and fractional address are rejected",()=>{assert.throws(()=>gear.buildState("unknown",0),RangeError);assert.throws(()=>gear.buildState("two",.5),TypeError);});
console.log(`PASS ${passed}/${passed}`);
