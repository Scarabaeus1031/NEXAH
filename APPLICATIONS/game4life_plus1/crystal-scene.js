(function startLifeCrystalObservatory() {
  "use strict";
  const canvas = document.getElementById("crystalScene");
  if (!canvas) return;
  const byId = id => document.getElementById(id);
  const status = byId("crystalStatus"), layoutInput = byId("crystalLayout"), spacingInput = byId("crystalSpacing");
  const focusInput = byId("crystalFocus"), cameraButton = byId("crystalCamera"), rotateButton = byId("crystalRotate"), exportButton = byId("crystalExport");
  const selection = byId("crystalSelection"), proof = byId("crystalProof"), nodes = byId("crystalNodes"), interval = byId("crystalInterval"), residual = byId("crystalResidual"), hash = byId("crystalHash");
  if (!window.THREE || !THREE.OrbitControls || !THREE.GLTFExporter) {
    status.textContent = "3D RUNTIME UNAVAILABLE";
    exportButton.disabled = true;
    return;
  }

  const COLORS = { events: 0xeef7fb, births: 0x22d3ee, survivals: 0xf5bf42, deaths: 0xfb7185, controller: 0xa78bfa, residual: 0x4ade80 };
  const renderer = new THREE.WebGLRenderer({ canvas, antialias: true, alpha: false, preserveDrawingBuffer: true });
  renderer.setPixelRatio(Math.min(window.devicePixelRatio || 1, 2));
  renderer.setClearColor(0x040a10, 1);
  renderer.outputEncoding = THREE.sRGBEncoding;
  const scene = new THREE.Scene();
  scene.fog = new THREE.FogExp2(0x040a10, 0.012);
  const camera = new THREE.PerspectiveCamera(42, 1, 0.1, 600);
  const controls = new THREE.OrbitControls(camera, canvas);
  controls.enableDamping = true; controls.dampingFactor = 0.07; controls.minDistance = 5; controls.maxDistance = 260;
  scene.add(new THREE.HemisphereLight(0xb9eaff, 0x12091b, 1.25));
  const keyLight = new THREE.DirectionalLight(0xffffff, 1.2); keyLight.position.set(8, 16, 10); scene.add(keyLight);
  const rim = new THREE.PointLight(0x22d3ee, 1.7, 80); rim.position.set(-14, 8, -8); scene.add(rim);
  const raycaster = new THREE.Raycaster(), pointer = new THREE.Vector2();
  let root = null, latest = null, selectedId = null, autoRotate = false, cameraReady = false;

  const materials = {};
  for (const [name, color] of Object.entries(COLORS)) materials[name] = new THREE.MeshStandardMaterial({ color, emissive: color, emissiveIntensity: 0.28, roughness: 0.36, metalness: 0.08 });
  const ghostMaterial = new THREE.MeshStandardMaterial({ color: 0x203c4b, emissive: 0x081a24, transparent: true, opacity: 0.32, roughness: 0.6 });
  const cellGeometry = new THREE.BoxGeometry(.28, .16, .28), nodeGeometry = new THREE.SphereGeometry(.12, 9, 7), smallGeometry = new THREE.SphereGeometry(.075, 7, 5);
  const cellPosition = (item, size, scale = .24) => new THREE.Vector3((item.x - (size - 1) / 2) * scale, 0, (item.y - (size - 1) / 2) * scale);
  const eventMeta = event => ({
    schema: "nexah.life-crystal.event-node.v1", persistent_event_id: event.id,
    generation: event.generation, lattice_x: event.x, lattice_y: event.y,
    event_type: event.type, event_symbol: event.symbol, register_slot: event.slot, phase_degrees: event.phase
  });
  function mesh(geometry, material, name, position, userData) {
    const object = new THREE.Mesh(geometry, material); object.name = name; object.position.copy(position); object.userData = userData || {}; return object;
  }
  function line(points, color, opacity = .5) {
    const geometry = new THREE.BufferGeometry().setFromPoints(points);
    return new THREE.Line(geometry, new THREE.LineBasicMaterial({ color, transparent: opacity < 1, opacity }));
  }
  function frame(width, depth, color) {
    const points = [new THREE.Vector3(-width/2,0,-depth/2),new THREE.Vector3(width/2,0,-depth/2),new THREE.Vector3(width/2,0,depth/2),new THREE.Vector3(-width/2,0,depth/2),new THREE.Vector3(-width/2,0,-depth/2)];
    return line(points, color, .34);
  }
  function labelMarker(name, color) {
    const marker = mesh(new THREE.TorusGeometry(.25,.035,7,24), materials[color], `${name}_marker`, new THREE.Vector3(), { projection_label: name });
    marker.rotation.x = Math.PI/2; return marker;
  }

  function buildSource(snapshot) {
    const group = new THREE.Group(); group.name = "SOURCE_FIELD"; group.userData = { view: "source", meaning: "current Conway state" };
    group.add(frame(snapshot.size*.24, snapshot.size*.24, COLORS.events));
    for (const item of snapshot.source) group.add(mesh(cellGeometry, materials.events, `source_x${item.x}_y${item.y}`, cellPosition(item,snapshot.size), { lattice_x:item.x,lattice_y:item.y,generation:item.generation,view:"source" }));
    const mark=labelMarker("SOURCE_FIELD","events"); mark.position.set(-snapshot.size*.12-.55,.2,-snapshot.size*.12); group.add(mark); return group;
  }
  function buildRegister(snapshot) {
    const group = new THREE.Group(); group.name = "REGISTER_4P1"; group.userData = { view:"register", meaning:"exact 4+1 event register" };
    const lanes = [{key:"scalar",name:"1_EVENTS",material:"events"},{key:"births",name:"i_BIRTH",material:"births"},{key:"survivals",name:"j_SURVIVE",material:"survivals"},{key:"deaths",name:"k_DEATH",material:"deaths"}];
    const spacing = Number(spacingInput.value)/4;
    lanes.forEach((lane,index)=>{
      const y=(1.5-index)*spacing, plane=frame(snapshot.size*.19,snapshot.size*.19,COLORS[lane.material]); plane.position.y=y; plane.name=`${lane.name}_PLANE`; group.add(plane);
      const source = lane.key === "scalar" ? snapshot.rosette : snapshot.register[lane.key];
      for (const event of source) { const p=cellPosition(event,snapshot.size,.19); p.y=y; group.add(mesh(nodeGeometry,materials[lane.material],`${lane.name}_${event.id}`,p,{...eventMeta(event),view:"register",lane:lane.name})); }
    });
    const q=labelMarker("Q_CONTROLLER","controller"); q.position.y=-2.5*spacing; q.scale.setScalar(1.6); q.userData={...snapshot.register.controller,view:"controller",schema:"nexah.life-crystal.q-controller.v1"}; group.add(q); return group;
  }
  function buildRosette(snapshot) {
    const group=new THREE.Group(); group.name="TRANSITION_ROSETTE"; group.userData={view:"rosette",meaning:"phase translation of the event register"};
    const phases={births:Math.PI/2,survivals:0,deaths:-Math.PI/2};
    group.add(mesh(new THREE.TorusGeometry(3.1,.025,6,72),ghostMaterial,"ROSETTE_RING",new THREE.Vector3(),{view:"rosette"}));
    for(const type of Object.keys(phases)){
      const angle=phases[type], tip=new THREE.Vector3(Math.cos(angle)*3.35,0,Math.sin(angle)*3.35); group.add(line([new THREE.Vector3(),tip],COLORS[type],.55));
      for(const event of snapshot.register[type]){
        const radial=1.15+2.0*(event.x+1)/(snapshot.size+1),spread=(event.y/(snapshot.size-1)-.5)*1.35;
        const p=new THREE.Vector3(Math.cos(angle)*radial-Math.sin(angle)*spread,.12*Math.sin((event.x+event.y)*.9),Math.sin(angle)*radial+Math.cos(angle)*spread);
        group.add(mesh(nodeGeometry,materials[type],`rosette_${event.id}`,p,{...eventMeta(event),view:"rosette"}));
      }
    }
    const q=labelMarker("ROSETTE_Q","controller"); q.scale.setScalar(1.7); group.add(q); return group;
  }
  function buildBraid(snapshot) {
    const group=new THREE.Group(); group.name="EVENT_BRAID"; group.userData={view:"braid",meaning:"cell-address event histories"};
    const height=Math.max(1,snapshot.generation-snapshot.firstGeneration+1)*.15, byAddress=new Map();
    for(const event of snapshot.braid){
      const lane=event.type==="births"?-1:event.type==="survivals"?0:1;
      const p=new THREE.Vector3((event.x-(snapshot.size-1)/2)*.17,(event.generation-snapshot.firstGeneration)*.15-height/2,lane*1.55+(event.y/(snapshot.size-1)-.5)*1.1);
      group.add(mesh(smallGeometry,materials[event.type],`braid_${event.id}`,p,{...eventMeta(event),view:"braid"}));
      const address=`${event.x},${event.y}`; if(!byAddress.has(address))byAddress.set(address,[]); byAddress.get(address).push({event,p});
    }
    for(const chain of byAddress.values()){
      chain.sort((a,b)=>a.event.generation-b.event.generation); let segment=[];
      for(let i=0;i<chain.length;i++){
        if(i&&chain[i].event.generation!==chain[i-1].event.generation+1){if(segment.length>1)group.add(line(segment,0x8b9baa,.18));segment=[]}
        segment.push(chain[i].p);
      }
      if(segment.length>1)group.add(line(segment,0x8b9baa,.18));
    }
    group.add(frame(snapshot.size*.17,3.8,COLORS.controller)); return group;
  }
  function buildResidual(snapshot) {
    const group=new THREE.Group(); group.name="BOUNDARY_RESIDUAL"; group.userData={view:"residual",meaning:"symmetric cell difference against finite-dead"};
    group.add(frame(snapshot.size*.2,snapshot.size*.2,COLORS.residual));
    for(const item of snapshot.residual) group.add(mesh(cellGeometry,materials.residual,`residual_x${item.x}_y${item.y}`,cellPosition(item,snapshot.size,.2),{...item,view:"residual",comparison:"finite-dead"}));
    const mark=labelMarker("BOUNDARY_RESIDUAL","residual"); mark.position.set(-snapshot.size*.1-.5,.2,-snapshot.size*.1); group.add(mark); return group;
  }
  function positions(layout){
    if(layout==="superposition")return {source:[0,0,0],register:[0,0,0],rosette:[0,0,0],braid:[0,0,0],residual:[0,0,0]};
    if(layout==="exploded")return {source:[-16,0,0],register:[0,0,0],rosette:[16,0,0],braid:[0,0,-18],residual:[0,0,18]};
    return {source:[-11,0,0],register:[0,0,0],rosette:[11,0,0],braid:[-5,0,-12],residual:[7,0,-12]};
  }
  function disposeRoot(object){if(!object)return;const geometries=new Set(),mats=new Set();object.traverse(child=>{if(child.geometry&&!([cellGeometry,nodeGeometry,smallGeometry].includes(child.geometry)))geometries.add(child.geometry);if(child.material&&!Object.values(materials).includes(child.material)&&child.material!==ghostMaterial)mats.add(child.material)});geometries.forEach(g=>g.dispose());mats.forEach(m=>m.dispose());scene.remove(object)}
  function applyLayout(shouldFit=true){if(!root)return;const p=positions(layoutInput.value);for(const [key,value] of Object.entries(p)){const room=root.getObjectByName(key==="source"?"SOURCE_FIELD":key==="register"?"REGISTER_4P1":key==="rosette"?"TRANSITION_ROSETTE":key==="braid"?"EVENT_BRAID":"BOUNDARY_RESIDUAL");room.position.set(...value);room.visible=focusInput.value==="all"||focusInput.value===key}if(shouldFit)fitCamera()}
  function build(snapshot){
    latest=snapshot;disposeRoot(root);root=new THREE.Group();root.name="NEXAH_LIFE_CRYSTAL_OBSERVATORY";root.userData={schema:snapshot.schema,authority:snapshot.authority,run_id:snapshot.runId,rule:snapshot.rule,boundary:snapshot.boundary,generation:snapshot.generation,event_join:"persistent_event_id"};
    root.add(buildSource(snapshot),buildRegister(snapshot),buildRosette(snapshot),buildBraid(snapshot),buildResidual(snapshot));scene.add(root);applyLayout(!cameraReady);cameraReady=true;
    const eventNodes=snapshot.rosette.length*3+snapshot.braid.length;
    nodes.textContent=eventNodes.toLocaleString();interval.textContent=snapshot.generation?`g${snapshot.firstGeneration}–g${snapshot.generation}`:"g0";residual.textContent=`Δ ${snapshot.residual.length} cells`;
    const ok=Object.values(snapshot.audit).every(Boolean);proof.textContent=ok?"PASS · unique IDs · channel sum · exact inverse":"PROJECTION AUDIT FAILED";proof.style.borderColor=ok?"#4ade80":"#fb7185";status.textContent=ok?"REVERSIBLE PROJECTION READY":"AUDIT FAILED";
    if(selectedId)highlight(selectedId);
  }
  function fitCamera(){if(!root)return;const bounds=new THREE.Box3().setFromObject(root);if(bounds.isEmpty())return;const center=bounds.getCenter(new THREE.Vector3()),size=bounds.getSize(new THREE.Vector3()),radius=Math.max(size.x,size.y,size.z,8);controls.target.copy(center);camera.position.copy(center).add(new THREE.Vector3(radius*.72,radius*.55,radius*.9));camera.near=Math.max(.05,radius/1000);camera.far=Math.max(300,radius*15);camera.updateProjectionMatrix();controls.update();scene.fog.density=Math.max(.003,Math.min(.014,.22/radius))}
  function highlight(id){
    selectedId=id;let found=null,count=0;root.traverse(object=>{if(!object.isMesh)return;const match=object.userData.persistent_event_id===id;object.scale.setScalar(match?1.9:1);if(match){count++;found=object.userData}});
    if(found)selection.textContent=`${found.event_symbol} ${found.event_type.toUpperCase()} · g${found.generation} · cell (${found.lattice_x}, ${found.lattice_y}) · linked in ${count} views`;
  }
  function resize(){const rect=canvas.getBoundingClientRect();const width=Math.max(1,Math.round(rect.width)),height=Math.max(1,Math.round(rect.height));renderer.setSize(width,height,false);camera.aspect=width/height;camera.updateProjectionMatrix()}
  async function exportGlb(){if(!root)return;status.textContent="EXPORTING GLB…";new THREE.GLTFExporter().parse(root,async result=>{const bytes=result instanceof ArrayBuffer?result:new TextEncoder().encode(JSON.stringify(result)).buffer,digest=await crypto.subtle.digest("SHA-256",bytes),hex=Array.from(new Uint8Array(digest),v=>v.toString(16).padStart(2,"0")).join("");const blob=new Blob([bytes],{type:"model/gltf-binary"}),url=URL.createObjectURL(blob),link=document.createElement("a");link.href=url;link.download=`nexah-life-crystal-${latest.runId.toLowerCase()}-g${String(latest.generation).padStart(4,"0")}.glb`;link.click();setTimeout(()=>URL.revokeObjectURL(url),1000);hash.textContent=`${bytes.byteLength.toLocaleString()} B · ${hex.slice(0,16)}…`;status.textContent="GLB EXPORTED · SHA-256 RECORDED"},error=>{status.textContent="EXPORT FAILED";hash.textContent=String(error&&error.message||error)},{binary:true,trs:true,onlyVisible:true})}
  canvas.addEventListener("pointerdown",event=>{if(!root)return;const rect=canvas.getBoundingClientRect();pointer.x=(event.clientX-rect.left)/rect.width*2-1;pointer.y=-(event.clientY-rect.top)/rect.height*2+1;raycaster.setFromCamera(pointer,camera);const hit=raycaster.intersectObject(root,true).find(item=>item.object.userData.persistent_event_id);if(hit)highlight(hit.object.userData.persistent_event_id)});
  window.addEventListener("lifecrystal:render",event=>build(event.detail));
  layoutInput.addEventListener("change",()=>applyLayout(true));focusInput.addEventListener("change",()=>applyLayout(true));spacingInput.addEventListener("input",()=>{if(latest){cameraReady=false;build(latest)}});cameraButton.addEventListener("click",fitCamera);exportButton.addEventListener("click",exportGlb);
  rotateButton.addEventListener("click",()=>{autoRotate=!autoRotate;rotateButton.textContent=`Orbit: ${autoRotate?"on":"off"}`;rotateButton.setAttribute("aria-pressed",String(autoRotate))});window.addEventListener("resize",resize);resize();camera.position.set(24,18,29);
  (function animate(){requestAnimationFrame(animate);controls.autoRotate=autoRotate;controls.autoRotateSpeed=.45;controls.update();renderer.render(scene,camera)}());
}());
