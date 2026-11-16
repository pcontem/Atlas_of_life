/* Atlas of Life — Biota mode: a time slider, the continents of that time (Merdith et al. 2021 plate model via
   GPlates) and the formations with atlas taxa as points. Double-click a point: its environment and the atlas
   taxa found there (only taxa with atlas entries are listed). */
const BT=(()=>{const ZMAX=96;let T=null,selF=null,openF=null,openC=null,lastK=1,proj,gpath,cache={},tok=0,zoom,zt=d3.zoomIdentity;
  const ENV=[["coast","Coastal & lagoon","#4fa59a",/lagoon|estuar|coastal|peritidal|intertidal|delta|bay|marginal|beach/],
    ["marine","Marine","#3f7fa8",/marine|offshore|subtidal|basinal|deep|shelf|slope|reef|carbonate|pelagic/],
    ["lake","Lake","#7c8fd1",/lacustrine|lake|pond/],
    ["land","River & land","#b0773b",/fluvial|flood|terrestrial|alluvial|dune|crevasse|channel|eolian|swamp|cave|soil/]];
  const envOf=f=>{const e=(f.env||[]).map(s=>s.replace(/"/g,"")),first=e[0]||"";
    if(/lacustrine/.test(first))return ENV[2];return ENV.find(x=>x[3].test(first))||["unknown","Unknown","#9a9184",/$^/]};
  const times=()=>D.paleo?D.paleo.times:[];
  // slider and strip use a gently non-linear scale (power 0.6) so recent times get more room; 0 = oldest map, 1 = present
  const K=0.6,AMAX=()=>times()[times().length-1],pos=t=>1-Math.pow(t/AMAX(),K),ageAt=p=>AMAX()*Math.pow(1-p,1/K);
  const near=t=>times().reduce((a,b)=>Math.abs(b-t)<Math.abs(a-t)?b:a,times()[0]);
  const visible=()=>D.formations.filter(f=>f.pp&&f.pp[T]);
  const F=id=>D.formations.find(f=>f.id===id);
  const curForms=()=>{const n=cur&&byId[cur];if(!n)return new Set();
    const gs=n.type==="genus"?[n]:D.genera.filter(g=>path(g.name).some(p=>p.id===cur));
    return new Set(gs.flatMap(g=>(g.formations||[]).flatMap(f=>f.ids||[])))};
  // a sensible starting time: the middle of the selected entry's range, else the first time with formations
  function startTime(){const n=cur&&byId[cur];
    if(n&&n.type==="genus"&&n.fad)return near((n.fad+n.lad)/2);
    if(n&&n.stat&&n.stat.fad){const fs=D.formations.filter(f=>curForms().has(f.id));if(fs.length)return near(fs[0].fad/2+fs[0].lad/2)}
    const t=times().find(t=>D.formations.some(f=>f.pp&&f.pp[t]));return t??0}
  function render(){
    if(!D.paleo){$("#view").innerHTML='<div class="empty">No palaeogeographic maps in this build.</div>';return}
    if(T==null)T=startTime();
    $("#view").innerHTML=`<div class="bio"><div class="biomain">
      <div class="biobar"><div class="biot"><b id="btime"></b><span id="bunits"></span></div>
        <div class="bioctl"><button data-s="-1" title="Older (←)">◀ Older</button><input id="bslider" type="range" min="0" max="1000" step="1"><button data-s="1" title="Younger (→)">Younger ▶</button>
        <button id="bjump" title="Go to the time of the selected entry">⌖ Selected entry</button><button id="bnext" title="Next older time with formations">Next formations ⟶</button></div>
        <svg id="bstrip" height="44"></svg></div>
      <div id="bmapw"><svg id="bmap"></svg><div id="btip"></div>
        <div class="bzoom"><button data-z="in" title="Zoom in (or scroll); deepest zoom fans out points at the same site">+</button><button data-z="out" title="Zoom out">−</button><span id="bzk" class="bzk"></span><button data-z="reset" title="Whole globe">⟲</button></div></div>
      <div class="biolegend" id="blegend"></div></div>
      <div class="bioside" id="bside"></div></div>`;
    const sl=$("#bslider");
    // slider runs from the oldest map (left) to the present (right), like the Timeline; buttons step one map
    sl.oninput=()=>setT(near(ageAt(+sl.value/1000)));
    document.querySelectorAll(".bioctl [data-s]").forEach(b=>b.onclick=()=>{const i=Math.min(times().length-1,Math.max(0,times().indexOf(T)- +b.dataset.s));setT(times()[i])});
    $("#bjump").onclick=()=>setT(startTime());
    // next older time where formations not shown now appear (wraps to the youngest such time)
    $("#bnext").onclick=()=>{const fresh=t=>D.formations.some(f=>f.pp&&f.pp[t]&&!f.pp[T]);
      setT(times().find(t=>t>T&&fresh(t))??times().find(t=>fresh(t)))};
    document.onkeydown=e=>{if(view!=="biota"||/INPUT|TEXTAREA/.test(document.activeElement.tagName))return;
      if(e.key==="ArrowLeft")document.querySelector('.bioctl [data-s="-1"]').click();if(e.key==="ArrowRight")document.querySelector('.bioctl [data-s="1"]').click()};
    $("#blegend").innerHTML=[ENV[1],ENV[0],ENV[2],ENV[3]].map(e=>`<span><i style="background:${e[2]}"></i>${e[1]}</span>`).join("")+
      `<span><i class="ring"></i>Formation of the selected entry</span><span class="note">Point size = atlas genera found there</span>`;
    const box=$("#bmapw").getBoundingClientRect();
    proj=d3.geoEqualEarth().fitExtent([[10,10],[box.width-10,box.height-10]],{type:"Sphere"});gpath=d3.geoPath(proj);
    // zoom: scroll or the +/− buttons, drag to pan; kept while the time changes; points keep their size on screen
    const svg=d3.select("#bmap");
    zoom=d3.zoom().scaleExtent([1,ZMAX]).translateExtent([[0,0],[box.width,box.height]]).on("zoom",e=>{zt=e.transform;applyZoom()}).on("end",()=>{if(zt.k!==lastK)drawPoints()});
    svg.call(zoom).on("dblclick.zoom",null);svg.call(zoom.transform,zt);
    document.querySelectorAll(".bzoom button").forEach(b=>b.onclick=()=>{const z=b.dataset.z;
      if(z==="reset")svg.transition().duration(300).call(zoom.transform,d3.zoomIdentity);else{// zoom towards the highlighted formation if there is one, else the centre of the view
        const n=selF&&[...document.querySelectorAll("#bmap .bpt")].find(n=>n.dataset.fs.split(" ").includes(selF)),p=n?zt.apply([+n.dataset.x,+n.dataset.y]):null;
        svg.transition().duration(250).call(zoom.scaleBy,z==="in"?1.6:1/1.6,p||undefined)}});
    drawStrip();setT(T,true)}
  function applyZoom(){const l=d3.select("#bzl");if(l.empty())return;l.attr("transform",zt);const zk=$("#bzk");if(zk)zk.textContent=zt.k<1.05?"":"×"+(zt.k<10?zt.k.toFixed(1):Math.round(zt.k));
    l.selectAll(".bpt").attr("transform",function(){return `translate(${this.dataset.x},${this.dataset.y}) scale(${1/zt.k}) translate(${this.dataset.ox||0},${this.dataset.oy||0})`});
    if(zt.k!==lastK)l.selectAll(".bfan").remove();}
  function drawStrip(){const s=$("#bstrip"),W=s.getBoundingClientRect().width||600,A=AMAX(),x=v=>W*pos(Math.min(v,A));
    s.innerHTML=tsRows(A,0,x,0,16,.85,["era","period"]).svg+`<line id="bmark" y1="0" y2="40" stroke="#26251f" stroke-width="2"/>`;
    s.onclick=e=>{const r=s.getBoundingClientRect();setT(near(ageAt((e.clientX-r.left)/r.width)))}}
  async function setT(t,force){if(t==null)return;T=t;const my=++tok;
    $("#bslider").value=Math.round(pos(T)*1000);
    const per=ivAt(T||0.001,"period"),ep=ivAt(T||0.001,"epoch"),age=ivAt(T||0.001,"age");
    $("#btime").textContent=T===0?"Present day":`${T} million years ago`;
    $("#bunits").textContent=[age&&age.name,ep&&ep.name,per&&per.name].filter(Boolean).join(" · ");
    const W=$("#bstrip").getBoundingClientRect().width||600,m=$("#bmark");if(m){m.setAttribute("x1",W*pos(T));m.setAttribute("x2",W*pos(T))}
    if(!cache[T])cache[T]=await fetch(`paleo/${T}.json`).then(r=>r.json()).catch(()=>[]);
    if(my!==tok)return;draw();side()}
  function draw(){const svg0=d3.select("#bmap"),polys=cache[T]||[];svg0.selectAll("*").remove();const svg=svg0.append("g").attr("id","bzl");
    svg.append("path").attr("d",gpath({type:"Sphere"})).attr("class","bocean");
    svg.append("path").attr("d",gpath(d3.geoGraticule10())).attr("class","bgrat");
    const land={type:"MultiPolygon",coordinates:polys.map(p=>p.map(r=>r.map(([x,y])=>[x/10,y/10])))};
    svg.append("path").attr("d",gpath(land)).attr("class","bland");
    svg.append("g").attr("id","bpts");drawPoints();
    applyZoom();
    svg0.on("click",ev=>{if(ev.defaultPrevented)return;if(ev.target.tagName!=="circle"&&ev.target.tagName!=="text"&&(selF||openF||openC)){openF=null;openC=null;history.replaceState(null,"","#biota");highlight(null);side()}})}
  // points closer than ~16 px on screen (at the current zoom) are drawn as one cluster marker with a count;
  // click lists its formations beside the map, double-click zooms in until they separate
  function drawPoints(){const g=d3.select("#bpts");if(g.empty())return;g.selectAll("*").remove();lastK=zt.k;
    const mine=curForms(),vis=visible().sort((a,b)=>b.genera.length-a.genera.length),cl=[];
    for(const f of vis){const[x,y]=proj(f.pp[T]),[sx,sy]=zt.apply([x,y]);
      const c=cl.find(c=>Math.hypot(c.sx-sx,c.sy-sy)<16);if(c)c.m.push({f,x,y});else cl.push({sx,sy,m:[{f,x,y}]})}
    cl.sort((a,b)=>a.m.some(o=>o.f.id===selF)-b.m.some(o=>o.f.id===selF));
    // at the deepest zoom, points that still overlap (same or neighbouring sites) are fanned out around their spot
    const fan=zt.k>=ZMAX*0.95;
    for(const c of cl){
      if(fan&&c.m.length>1){const x0=d3.mean(c.m,o=>o.x),y0=d3.mean(c.m,o=>o.y),R=14+3*c.m.length;
        c.m.forEach((o,i)=>{const a=-Math.PI/2+2*Math.PI*i/c.m.length;
          g.append("line").attr("class","bfan").attr("x1",x0).attr("y1",y0).attr("x2",x0+R*Math.cos(a)/zt.k).attr("y2",y0+R*Math.sin(a)/zt.k);
          marker(g,[o.f],x0,y0,mine,[R*Math.cos(a),R*Math.sin(a)])});continue}
      marker(g,c.m.map(o=>o.f),d3.mean(c.m,o=>o.x),d3.mean(c.m,o=>o.y),mine)}}
  function marker(g,fs,x,y,mine,off){const n=fs.reduce((s,f)=>s+f.genera.length,0);
      const env=d3.rollups(fs,v=>d3.sum(v,f=>f.genera.length||1),f=>envOf(f)[2]).sort((a,b)=>b[1]-a[1])[0][0],r=4+Math.sqrt(n)*3;
      const ids=fs.map(f=>f.id),one=fs.length===1,ox=off?off[0]:0,oy=off?off[1]:0;
      const e=g.append("g").attr("class","bpt"+(one?"":" bcl")+(ids.includes(selF)?" sel":"")).attr("data-f",one?ids[0]:null).attr("data-fs",ids.join(" "))
        .attr("data-x",x).attr("data-y",y).attr("data-ox",ox).attr("data-oy",oy).attr("transform",`translate(${x},${y}) scale(${1/zt.k}) translate(${ox},${oy})`);
      if(ids.some(i=>mine.has(i)))e.append("circle").attr("r",r+4).attr("class","bring");
      e.append("circle").attr("r",one?r:r+2).attr("fill",env);
      if(!one)e.append("text").attr("class","bcnt").attr("dy","0.35em").text(fs.length);
      e.on("mouseenter",ev=>tip(ev,fs)).on("mouseleave",()=>$("#btip").style.display="none");
      if(one)e.on("click",()=>openCard(ids[0])).on("dblclick",ev=>{ev.stopPropagation();location.hash="formation/"+ids[0]});
      else e.on("click",()=>{openC=ids;openF=null;highlight(null);side()})
            .on("dblclick",ev=>{ev.stopPropagation();const k=Math.min(ZMAX,zt.k*4)/zt.k;d3.select("#bmap").transition().duration(400).call(zoom.scaleBy,k,zt.apply([x,y]))})}
  // highlight without redrawing, so that a double-click still reaches the same element
  // click: open the formation's card beside the map (no redraw, so a double-click still lands on the point)
  function openCard(id){history.replaceState(null,"","#biota/"+id);openF=id;highlight(id);side()}
  function highlight(id){selF=id;document.querySelectorAll("#bmap .bpt").forEach(n=>n.classList.toggle("sel",!!id&&n.dataset.fs.split(" ").includes(id)));
    document.querySelectorAll("#bside .bfl").forEach(n=>n.classList.toggle("sel",n.dataset.f===id))}
  function tip(ev,fs){const t=$("#btip"),b=$("#bmapw").getBoundingClientRect();
    if(fs.length>1){t.innerHTML=`<b>${fs.length} formations here</b><br>${fs.map(f=>esc(f.name)).join("<br>")}<br><small>Click: list · double-click: zoom in</small>`;
      t.style.display="block";t.style.left=(ev.clientX-b.left+12)+"px";t.style.top=(ev.clientY-b.top+12)+"px";return}
    const f=fs[0];t.innerHTML=`<b>${esc(f.name)}</b><br>${esc(f.country)} · ${fmtMa(f.fad)}–${fmtMa(f.lad)}<br>${f.genera.length} atlas ${f.genera.length===1?"genus":"genera"} · ${esc(envOf(f)[1].toLowerCase())}<br><small>Click: card · double-click: entry</small>`;
    t.style.display="block";t.style.left=(ev.clientX-b.left+12)+"px";t.style.top=(ev.clientY-b.top+12)+"px"}
  function side(){const s=$("#bside");const f=openF&&F(openF);
    if(f&&f.pp&&f.pp[T]){s.innerHTML=formationCard(f);wire(s);return}
    openF=null;
    if(openC){const fs=openC.map(F).filter(f=>f&&f.pp&&f.pp[T]);if(fs.length>1){
      s.innerHTML=`<button class="bback">← All formations at ${T} Ma</button><h2>${fs.length} formations at this spot</h2>
        <p class="note">Their points overlap at this zoom. Click one for its card, double-click for its entry; or zoom in to separate them.</p>`+
        fs.map(f=>`<div class="bfl" data-f="${f.id}"><i style="background:${envOf(f)[2]}"></i><span>${esc(f.name)}<small>${esc(f.country)} · ${fmtMa(f.fad)}–${fmtMa(f.lad)} · ${f.genera.length} ${f.genera.length===1?"genus":"genera"}</small></span></div>`).join("");
      s.querySelector(".bback").onclick=()=>{openC=null;side()};
      s.querySelectorAll(".bfl").forEach(d=>{d.onclick=()=>openCard(d.dataset.f);d.ondblclick=()=>location.hash="formation/"+d.dataset.f});return}openC=null}
    const vis=visible().sort((a,b)=>a.name.localeCompare(b.name));
    s.innerHTML=`<h3>${vis.length} formation${vis.length===1?"":"s"} at this time</h3>`+
      (vis.length?`<p class="note">Formations whose dated beds overlap ${T} ± 2.5 Ma. Click: show its card · double-click: open its entry.</p>`+
        vis.map(f=>`<div class="bfl${f.id===selF?" sel":""}" data-f="${f.id}"><i style="background:${envOf(f)[2]}"></i><span>${esc(f.name)}<small>${esc(f.country)} · ${f.genera.length} ${f.genera.length===1?"genus":"genera"}</small></span></div>`).join("")
      :`<p class="note">No formation with atlas taxa at this time. Use “Next formations” or drag the slider.</p>`)+about();
    s.querySelectorAll(".bfl").forEach(d=>{d.onclick=()=>openCard(d.dataset.f);d.ondblclick=()=>location.hash="formation/"+d.dataset.f})}
  function formationCard(f){const e=envOf(f);
    const gs=f.genera.map(n=>byId[n]).filter(Boolean),groups={};
    for(const g of gs){const p=byId[g.parent];(groups[p?p.name:"—"]=groups[p?p.name:"—"]||[]).push(g)}
    const thumb=g=>{const im=(g.images||[]).find(i=>i.kind==="life")||(g.images||[])[0];return im?`<img src="${imgSrc(g.name,im)}" alt="">`:(g.silhouette?`<img class="sil" src="${silSrc(g.silhouette)}" alt="">`:"")};
    const tsn=v=>{const a=ivAt(v,"age");return a?a.name:""};
    return `<button class="bback">← All formations at ${T} Ma</button>
      <h2>${esc(f.name)}</h2><a class="bopen" href="#formation/${f.id}">Open the full entry →</a><div class="note">${f.group?esc(f.group)+" Group · ":""}${esc(f.country)}${f.regions.length?" ("+esc(f.regions.join(", "))+")":""}</div>
      <div class="badge" style="border-color:${e[2]}">${esc(e[1])}</div>
      ${f.sum?`<p class="lead2">${esc(f.sum)}</p>`:""}
      <dl class="kv"><dt>Age of the beds</dt><dd>${fmtMa(f.fad)}–${fmtMa(f.lad)} (${esc(tsn(f.fad-0.01))}${tsn(f.lad+0.01)!==tsn(f.fad-0.01)?"–"+esc(tsn(f.lad+0.01)):""})<br><span class="note">${esc(f.agenote)}</span></dd>
      <dt>Environment</dt><dd>${f.env.length?esc(f.env.map(s=>s.replace(/"/g,"")).join("; ")):"—"}<br><span class="note">Depositional environments recorded in PBDB</span></dd>
      <dt>Rock types</dt><dd>${esc(f.lith.map(s=>s.replace(/"/g,"")).join(", ")||"—")}</dd>
      <dt>Position</dt><dd>${fmtLat(f.pp[T][1])} palaeolatitude at ${T} Ma<br><span class="note">Today ${fmtLat(f.lat)}, ${fmtLng(f.lng)} — ${esc(f.basis)}</span></dd></dl>
      <h4>Palaeoenvironment</h4>${f.paleoenv?`<p>${esc(f.paleoenv)}</p>`:`<p class="note">Not written yet for this formation (draft entry).</p>`}
      <h4>Atlas taxa found here (${gs.length})</h4><p class="note">Only taxa with entries in the atlas are listed; more groups will appear as new volumes are added.</p>
      ${Object.entries(groups).sort().map(([k,v])=>`<div class="bgrp">${esc(k)}</div><div class="bgen">${v.sort((a,b)=>a.name.localeCompare(b.name)).map(g=>
        `<div class="mem" data-g="${esc(g.name)}" title="Double-click to open the entry"><div class="th">${thumb(g)}</div><div class="nm"><i>${esc(g.name)}</i><small>${fmtMa(g.fad)}–${fmtMa(g.lad)}</small></div></div>`).join("")}</div>`).join("")}
      <h4>Sources</h4><ol class="src">${f.sources.map(s=>`<li><span class="kind">${esc(s.kind)}</span>${esc(s.text)}${s.url?` <a href="${esc(s.url)}" target="_blank" rel="noopener">link</a>`:""}</li>`).join("")}<li><span class="kind">model</span>${esc(D.paleo.citation)} ${esc(D.paleo.licence)}. ${esc(D.paleo.via)}</li></ol>`}
  function wire(s){s.querySelector(".bback").onclick=()=>{openF=null;openC=null;history.replaceState(null,"","#biota");highlight(null);side()};
    s.querySelectorAll(".mem[data-g]").forEach(d=>{d.onclick=()=>{cur=d.dataset.g;s.querySelectorAll(".mem").forEach(m=>m.classList.toggle("sel",m===d))};d.ondblclick=()=>location.hash=d.dataset.g})}
  const fmtLat=v=>`${Math.abs(v).toFixed(0)}° ${v>=0?"N":"S"}`,fmtLng=v=>`${Math.abs(v).toFixed(1)}° ${v>=0?"E":"W"}`;
  const about=()=>`<div class="bnote"><b>About the map.</b> ${esc(D.paleo.note)} Plate model: ${esc(D.paleo.citation)} (${esc(D.paleo.licence)}), ${esc(D.paleo.via)}</div>`;
  // deep link #biota/<formation id>: open that formation at the middle of its record
  function focus(fid){const f=F(fid);if(!f||!f.pp)return;const ts=Object.keys(f.pp).map(Number).sort((a,b)=>a-b);
    T=ts[Math.floor((ts.length-1)/2)];openF=selF=fid}
  const envClass=envOf;
  return{render,focus,envClass,ENV}})();
function renderBiota(){BT.render()}
