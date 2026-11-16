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
  let h=`<div class="ficha"><div class="crumbs"><a onclick="location.hash='formations'">Formations</a> › ${esc(f.country)} · <a onclick="location.hash='biota/${f.id}'">show in Biota</a></div>
    <h2>${esc(f.name)}${/^Unnamed|Group \(/.test(f.name)?"":` <span class="fsub">Formation</span>`}</h2>
    <div class="auth">${f.group?esc(f.group)+" Group · ":""}${esc(f.country)}${f.regions.length?" ("+esc(f.regions.join(", "))+")":""} · ${esc(age(f.fad-0.01))}${age(f.lad+0.01)!==age(f.fad-0.01)?"–"+esc(age(f.lad+0.01)):""} · ${fmtMa(f.fad)}–${fmtMa(f.lad)}</div>
    <span class="badge" style="border-color:${e[2]}">${esc(e[1])}</span><span class="badge">${gs.length} atlas ${gs.length===1?"genus":"genera"}</span>
    <p class="lead">${f.sum?esc(f.sum):`<span class="note">No summary written yet for this formation (draft entry).</span>`}</p><div class="grid"><div>`;
  h+=`<div class="card"><h3>Palaeoenvironment</h3>${f.paleoenv?`<p style="margin:0">${esc(f.paleoenv)}</p>`:`<p class="note" style="margin:0">Not written yet. PBDB records these depositional environments: ${esc(f.env.map(s=>s.replace(/"/g,"")).join("; ")||"none")}.</p>`}</div>`;
  if(f.includes&&f.includes.length)h+=`<div class="card"><h3>Units grouped here</h3><ul class="diag">${f.includes.map(t=>`<li>${esc(t)}</li>`).join("")}</ul></div>`;
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

/* Encyclopedia section "Formations" (#formations): every formation entry, filterable by text,
   environment, period and the selected entry; grouped by period when sorted by age. */
const FS={q:"",env:"all",per:"all",sort:"age",mine:false};
function renderFormations(){const all=D.formations||[],sel=cur&&byId[cur]&&cur!=="vida"?byId[cur]:null;
  const per=f=>{const p=ivAt((f.fad+f.lad)/2,"period");return p?p.name:"—"};
  const pers=[...new Set(all.slice().sort((a,b)=>b.fad-a.fad).map(per))];
  const mineIds=new Set();if(sel){const gs=sel.type==="genus"?[sel]:D.genera.filter(g=>path(g.name).some(p=>p.id===sel.id));gs.forEach(g=>(g.formations||[]).forEach(f=>(f.ids||[]).forEach(i=>mineIds.add(i))))}
  $("#view").innerHTML=`<div class="xl fsec"><h2>Geological formations</h2>
    <p class="note">The rock units where atlas taxa were found — ${all.length} entries. Each has its age, depositional environment (PBDB), where it lay on the globe at the time, and the atlas taxa found in it. Click a row to open its entry; the map icon opens it in Biota.</p>
    <div class="fctl"><input id="fq" type="search" placeholder="Name, country, region or group…" value="${esc(FS.q)}">
      <select id="fper"><option value="all">All periods</option>${pers.map(p=>`<option${FS.per===p?" selected":""}>${esc(p)}</option>`).join("")}</select>
      <select id="fsort"><option value="age">Oldest first</option><option value="young">Youngest first</option><option value="name">Name</option><option value="gen">Most genera</option></select>
      ${sel?`<label class="fmine"><input type="checkbox" id="fmine"${FS.mine?" checked":""}> Only those of <b>${sel.type==="genus"?"<i>"+esc(sel.name)+"</i>":esc(sel.name)}</b></label>`:""}</div>
    <div class="fenv">${[["all","All environments","#26251f"],...[1,0,2,3].map(i=>BT.ENV[i]).map(e=>[e[0],e[1],e[2]])].map(([k,l,c])=>`<button data-e="${k}" class="${FS.env===k?"on":""}"><i style="background:${c}"></i>${l}</button>`).join("")}</div>
    <div id="flist"></div></div>`;
  $("#fsort").value=FS.sort;
  const list=()=>{const q=FS.q.trim().toLowerCase();
    let fs=all.filter(f=>(!q||[f.name,f.country,f.group,...f.regions].join(" ").toLowerCase().includes(q))&&(FS.env==="all"||BT.envClass(f)[0]===FS.env)&&(FS.per==="all"||per(f)===FS.per)&&(!FS.mine||!sel||mineIds.has(f.id)));
    const srt={age:(a,b)=>b.fad-a.fad||b.lad-a.lad,young:(a,b)=>a.lad-b.lad||a.fad-b.fad,name:(a,b)=>a.name.localeCompare(b.name),gen:(a,b)=>b.genera.length-a.genera.length||a.name.localeCompare(b.name)}[FS.sort];
    fs.sort(srt);
    const row=f=>{const e=BT.envClass(f),a=ivAt(f.fad-0.01,"age"),b=ivAt(f.lad+0.01,"age");
      return `<tr class="frow" data-f="${f.id}"><td><i class="fdot" style="background:${e[2]}" title="${esc(e[1])}"></i><b>${esc(f.name)}</b>${f.group?` <span class="note">${esc(f.group)} Gr.</span>`:""}</td>
        <td>${esc(f.country)}${f.regions.length?` <span class="note">${esc(f.regions.join(", "))}</span>`:""}</td>
        <td>${esc(a?a.name:"")}${b&&a&&b.name!==a.name?"–"+esc(b.name):""}<br><span class="note">${fmtMa(f.fad)}–${fmtMa(f.lad)}</span></td>
        <td>${f.genera.slice(0,4).map(g=>"<i>"+esc(g)+"</i>").join(", ")}${f.genera.length>4?` <span class="note">+${f.genera.length-4}</span>`:""}</td>
        <td class="fmapc"><a title="Open in Biota" onclick="event.stopPropagation();location.hash='biota/${f.id}'">◍</a></td></tr>`};
    const head=`<tr><th>Formation</th><th>Country</th><th>Age</th><th>Atlas taxa</th><th></th></tr>`;
    let h=`<p class="note">${fs.length} of ${all.length} formations</p>`;
    if(FS.sort==="age"||FS.sort==="young"){const groups=[];for(const f of fs){const p=per(f);if(!groups.length||groups[groups.length-1][0]!==p)groups.push([p,[]]);groups[groups.length-1][1].push(f)}
      h+=groups.map(([p,v])=>{const iv=TS().find(t=>t.type==="period"&&t.name===p);return `<h3 class="fper" style="border-color:${iv?iv.color:"#ccc"}">${esc(p)} <span class="note">(${v.length})</span></h3><table>${head}${v.map(row).join("")}</table>`}).join("")}
    else h+=`<table>${head}${fs.map(row).join("")}</table>`;
    $("#flist").innerHTML=fs.length?h:`<p class="note">No formation matches these filters.</p>`;
    document.querySelectorAll(".frow").forEach(r=>r.onclick=()=>location.hash="formation/"+r.dataset.f)};
  $("#fq").oninput=e=>{FS.q=e.target.value;list()};$("#fper").onchange=e=>{FS.per=e.target.value;list()};$("#fsort").onchange=e=>{FS.sort=e.target.value;list()};
  if($("#fmine"))$("#fmine").onchange=e=>{FS.mine=e.target.checked;list()};
  document.querySelectorAll(".fenv button").forEach(b=>b.onclick=()=>{FS.env=b.dataset.e;document.querySelectorAll(".fenv button").forEach(x=>x.classList.toggle("on",x===b));list()});
  list()}
