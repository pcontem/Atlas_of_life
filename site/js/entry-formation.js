/* Atlas of Life — Encyclopedia entry of a geological formation (#formation/<id>): what it is, its
   palaeoenvironment, where it lay at the time (palaeogeographic map), the atlas taxa found there, sources. */
let curF=null;
function renderFormation(fid){const f=(D.formations||[]).find(x=>x.id===fid);
  if(!f){$("#view").innerHTML=`<div class="empty">No formation entry “${esc(fid)}”.</div>`;return}
  const e=BT.envClass(f),gs=f.genera.map(n=>byId[n]).filter(Boolean),ts=Object.keys(f.pp||{}).map(Number).sort((a,b)=>a-b);
  const mid=ts.length?ts[Math.floor((ts.length-1)/2)]:null,age=v=>{const a=ivAt(v,"age");return a?a.name:""};
  const groups={};for(const g of gs){const p=byId[g.parent];(groups[p?p.name:"—"]=groups[p?p.name:"—"]||[]).push(g)}
  const thumb=g=>{const im=(g.images||[]).find(i=>i.kind==="life")||(g.images||[])[0];
    return im?`<img src="${imgSrc(g.name,im)}" alt="" style="max-height:96px;max-width:100%;opacity:1">`:(g.silhouette?`<img src="${silSrc(g.silhouette)}" alt="">`:"")};
  let h=`<div class="ficha"><div class="crumbs"><a onclick="location.hash='biota/${f.id}'">Biota</a> › Formations › ${esc(f.country)}</div>
    <h2>${esc(f.name)}${/^Unnamed/.test(f.name)?"":` <span class="fsub">Formation</span>`}</h2>
    <div class="auth">${f.group?esc(f.group)+" Group · ":""}${esc(f.country)}${f.regions.length?" ("+esc(f.regions.join(", "))+")":""} · ${esc(age(f.fad-0.01))}${age(f.lad+0.01)!==age(f.fad-0.01)?"–"+esc(age(f.lad+0.01)):""} · ${fmtMa(f.fad)}–${fmtMa(f.lad)}</div>
    <span class="badge" style="border-color:${e[2]}">${esc(e[1])}</span><span class="badge">${gs.length} atlas ${gs.length===1?"genus":"genera"}</span>
    <p class="lead">${f.sum?esc(f.sum):`<span class="note">No summary written yet for this formation (draft entry).</span>`}</p><div class="grid"><div>`;
  h+=`<div class="card"><h3>Palaeoenvironment</h3>${f.paleoenv?`<p style="margin:0">${esc(f.paleoenv)}</p>`:`<p class="note" style="margin:0">Not written yet. PBDB records these depositional environments: ${esc(f.env.map(s=>s.replace(/"/g,"")).join("; ")||"none")}.</p>`}</div>`;
  h+=`<div class="card"><h3>Atlas taxa found here (${gs.length})</h3><p class="note" style="margin-top:0">Only taxa with atlas entries are listed; other groups will appear as new volumes are added. Click to open.</p>
    ${Object.entries(groups).sort().map(([k,v])=>`<div class="bgrp">${esc(k)}</div><div class="members">${v.sort((a,b)=>a.name.localeCompare(b.name)).map(g=>
      `<div class="mem" onclick="go('${esc(g.name)}')"><div class="th">${thumb(g)}</div><div class="nm"><i>${esc(g.name)}</i><small>${fmtMa(g.fad)}–${fmtMa(g.lad)}</small></div></div>`).join("")}</div>`).join("")}</div>`;
  h+=`<div class="card"><h3>Sources</h3><ol class="src">${f.sources.map(s=>`<li><span class="kind">${esc(s.kind)}</span>${esc(s.text)}${s.url?` <a href="${esc(s.url)}" target="_blank" rel="noopener">link</a>`:""}</li>`).join("")}
    <li><span class="kind">model</span>${esc(D.paleo.citation)} (${esc(D.paleo.licence)}). ${esc(D.paleo.via)}</li></ol></div>`;
  h+=`</div><div>`;
  h+=`<div class="card"><h3>Time range</h3><div class="tl">${timeline([[f.fad,f.lad,era(f.fad)[3]]],48)}</div><p class="note">${esc(f.agenote)}</p></div>`;
  h+=`<div class="card"><h3>Where it lay${mid!=null?` · ${mid} Ma`:""}</h3>${mid!=null?`<svg id="fmap" viewBox="0 0 460 240" style="width:100%;display:block"></svg>
      <p class="note">Palaeolatitude ${Math.abs(f.pp[mid][1]).toFixed(0)}° ${f.pp[mid][1]>=0?"N":"S"} at ${mid} Ma (longitudes of the plate model are not constrained). <a style="cursor:pointer" onclick="location.hash='biota/${f.id}'">Explore in Biota →</a></p>`:`<p class="note">No palaeo-position available.</p>`}</div>`;
  h+=`<div class="card"><h3>Geology (PBDB)</h3><dl class="kv"><dt>Environment</dt><dd>${esc(f.env.map(s=>s.replace(/"/g,"")).join("; ")||"—")}</dd>
    <dt>Rock types</dt><dd>${esc(f.lith.map(s=>s.replace(/"/g,"")).join(", ")||"—")}</dd>
    <dt>Location today</dt><dd>${Math.abs(f.lat).toFixed(2)}° ${f.lat>=0?"N":"S"}, ${Math.abs(f.lng).toFixed(2)}° ${f.lng>=0?"E":"W"}<br><span class="note">${esc(f.basis)}</span></dd>
    <dt>PBDB collections</dt><dd>${f.ncol}</dd></dl></div>`;
  h+=`</div></div></div>`;
  $("#view").innerHTML=h;
  if(mid!=null)fetch(`paleo/${mid}.json`).then(r=>r.json()).then(polys=>{if(curF!==fid)return;
    const svg=d3.select("#fmap"),proj=d3.geoEqualEarth().fitExtent([[4,4],[456,236]],{type:"Sphere"}),gp=d3.geoPath(proj);
    svg.append("path").attr("d",gp({type:"Sphere"})).attr("class","bocean");
    svg.append("path").attr("d",gp(d3.geoGraticule10())).attr("class","bgrat");
    svg.append("path").attr("d",gp({type:"MultiPolygon",coordinates:polys.map(p=>p.map(r=>r.map(([x,y])=>[x/10,y/10])))})).attr("class","bland");
    const[x,y]=proj(f.pp[mid]);svg.append("circle").attr("cx",x).attr("cy",y).attr("r",9).attr("fill","none").attr("stroke",e[2]).attr("stroke-width",2);
    svg.append("circle").attr("cx",x).attr("cy",y).attr("r",4.5).attr("fill",e[2]).attr("stroke","#fffdf8")}).catch(()=>{})}
