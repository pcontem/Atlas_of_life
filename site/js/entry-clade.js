/* Atlas of Life — Clade entry page and the basic page for groups without an entry. */
/* ---------- clade entry ---------- */
function allGenera(id){const out=[];(function r(k){const n=byId[k];if(n.type==="genus")out.push(n);else children[k].forEach(r)})(id);return out}
function thumb(g){const im=(g.images||[])[0];if(im)return `<div class="th" style="background-image:url('${thumbSrc(g.name,im)}')"></div>`;
  return `<div class="th">${g.silhouette?`<img src="${silSrc(g.silhouette)}" alt="">`:""}</div>`}
function renderClade(id){const c=byId[id],gs=allGenera(id),s=c.stat;
  const direct=children[id].filter(k=>byId[k].type==="genus");
  let h=`<div class="ficha">${crumbs(id)}<h2>${esc(c.name)}</h2><div class="auth">Clade · ${s.g} genera in this volume · ${fmtMa(s.fad)}–${fmtMa(s.lad)}</div>${curBadge(c.cur)}<p class="lead">${esc(c.sum)}</p>`;
  h+=`<div class="card"><div class="stat"><div><b>${s.g}</b><span>genera</span></div><div><b>${gs.reduce((a,g)=>a+(g.nsp??g.species.length),0)}</b><span>valid species</span></div><div><b>${fmtMa(s.fad).replace(" Ma","")}–${fmtMa(s.lad).replace(" Ma","")}</b><span>million years ago</span></div><div><b>${s.cc.size}</b><span>countries with fossils</span></div></div></div>`;
  h+=`<div class="grid"><div><div class="card"><h3>Diagnostic features</h3><ul class="diag">${c.diag.map(d=>`<li>${esc(d)}</li>`).join("")}</ul></div></div><div><div class="card"><h3>Notes on classification</h3><p style="margin:0">${esc(c.notes)}</p></div></div></div>`;
  h+=`<p class="note" style="margin:-6px 0 14px">How these genera are spread through time: <a style="cursor:pointer" onclick="TLV='ranges';TLRES='genus';location.hash='time'">see the Timeline</a>.</p>`;
  const sub=children[id].filter(k=>byId[k].type==="clade");
  if(sub.length)h+=`<div class="card"><h3>Subgroups</h3><div class="members">${sub.map(k=>{const sc=byId[k];const rep=allGenera(k).find(g=>g.images&&g.images.some(i=>i.kind==="life"))||allGenera(k)[0];return `<div class="mem" onclick="go('${k}')">${rep?thumb(rep):""}<div class="nm">${esc(sc.name)}<small>${sc.stat.g} genera</small></div></div>`}).join("")}</div></div>`;
  // genera sitting directly in this clade: those with an uncertain position are shown apart, as "Incertae sedis"
  const gcard=(title,ks,note)=>ks.length?`<div class="card"><h3>${title}</h3>${note?`<p class="note" style="margin:-4px 0 10px">${note}</p>`:""}<div class="members">${ks.sort().map(k=>{const g=byId[k];return `<div class="mem" onclick="go('${k}')">${thumb(g)}<div class="nm"><i>${esc(k)}</i><small>${esc(g.early)}</small></div></div>`}).join("")}</div></div>`:"";
  h+=gcard("Genera placed directly here",direct.filter(k=>!byId[k].isd),"");
  h+=gcard("Incertae sedis",direct.filter(k=>byId[k].isd),`Genera that belong to ${esc(c.name)} but whose position inside it is uncertain.`);
  h+=`<div class="card"><h3>Sources</h3>${sources(c.sources)}</div>${curCard(c.cur,c.name,false)}</div>`;
  $("#view").innerHTML=h}

/* ---------- clade entry for a group of the tree backbone (entries/tree/clades): no volume genera yet ---------- */
function treeKids(id){const kids=children[id];return{cl:kids.filter(k=>byId[k].type==="clade"),gs:kids.filter(k=>byId[k].type==="genus")}}
function kidChips(id){const{cl,gs}=treeKids(id);let h="";
  if(cl.length)h+=`<div class="card"><h3>Subgroups</h3><div class="chips">${cl.map(k=>`<a class="chip${byId[k].ficha?" has":""}" onclick="go('${k}')">${esc(byId[k].name)} <small>${byId[k].stat.g}</small></a>`).join("")}</div></div>`;
  const chip=k=>`<a class="chip${byId[k].ficha?" has":""}" onclick="go('${k}')"><i>${byId[k].status==="e"?"† ":""}${esc(byId[k].name)}</i></a>`;
  const inc=gs.filter(k=>/^Incertae sedis/.test(byId[k].note||"")),sure=gs.filter(k=>!inc.includes(k));
  if(sure.length)h+=`<div class="card"><h3>Genera placed directly here (${sure.length})</h3><div class="chips">${sure.map(chip).join("")}</div></div>`;
  if(inc.length)h+=`<div class="card"><h3>Incertae sedis (${inc.length})</h3><p class="note" style="margin-top:0">Genera whose position inside this group is not resolved.</p><div class="chips">${inc.map(chip).join("")}</div></div>`;
  return h}
function renderTreeClade(id){const c=byId[id],s=c.stat,{cl}=treeKids(id);
  const st=c.status==="e"?"Extinct":c.status==="v"?"Living (extant)":"";
  const rk=c.trank?c.trank.charAt(0).toUpperCase()+c.trank.slice(1):"Clade";
  let h=`<div class="ficha">${crumbs(id)}<h2>${esc(c.name)}</h2><div class="auth" title="${esc(c.trank_src||"")}">${esc(rk)}${st?" · "+st:""}</div>${curBadge(c.cur)}<p class="lead">${esc(c.sum)}</p>`;
  h+=`<div class="card"><div class="stat"><div><b>${s.g}</b><span>genera in the tree</span></div><div><b>${s.e}</b><span>extinct</span></div><div><b>${s.g-s.e}</b><span>living or unspecified</span></div><div><b>${cl.length}</b><span>direct subgroups</span></div></div></div>`;
  h+=`<div class="grid"><div><div class="card"><h3>Diagnostic features</h3><ul class="diag">${c.diag.map(d=>`<li>${esc(d)}</li>`).join("")}</ul></div></div><div><div class="card"><h3>Notes on classification</h3><p style="margin:0">${esc(c.notes)}</p></div></div></div>`;
  h+=kidChips(id);
  h+=`<p class="note">Genera shown here come from the tree outline; only genera of the volumes written so far have full entries.</p>`;
  h+=`<div class="card"><h3>Sources</h3>${sources(c.sources)}</div>${curCard(c.cur,c.name,false)}</div>`;
  $("#view").innerHTML=h}

/* ---------- basic entry for groups not yet covered ---------- */
function renderBasic(id){const n=byId[id],kids=children[id],cl=kids.filter(k=>byId[k].type==="clade"),gs=kids.filter(k=>byId[k].type==="genus");
  const st=n.status==="e"?"Extinct":n.status==="v"?"Living (extant)":"";
  let h=`<div class="ficha">${crumbs(id)}<h2>${n.type==="genus"?"<i>"+esc(n.name)+"</i>":esc(n.name)}</h2><div class="auth">${n.type==="clade"?"Clade":"Genus"}${st?" · "+st:""}</div>`;
  h+=`<div class="card" style="margin-top:16px;background:#f7f0e0"><p style="margin:0">This ${n.type==="clade"?"group":"genus"} is in the tree of life but does not have an entry yet. ${n.note?`<br><br><b>Note:</b> ${esc(n.note)}`:""}</p></div>`;
  if(n.type==="clade"){const s=n.stat;
    h+=`<div class="card"><div class="stat"><div><b>${s.g}</b><span>genera listed</span></div><div><b>${s.e}</b><span>extinct</span></div><div><b>${s.g-s.e}</b><span>living or unspecified</span></div><div><b>${cl.length}</b><span>direct subgroups</span></div></div></div>`;
    if(cl.length)h+=`<div class="card"><h3>Subgroups</h3><div class="chips">${cl.map(k=>`<a class="chip" onclick="go('${k}')">${esc(byId[k].name)} <small>${byId[k].stat.g}</small></a>`).join("")}</div></div>`;
    if(gs.length)h+=`<div class="card"><h3>Genera placed directly here (${gs.length})</h3><div class="chips">${gs.map(k=>`<a class="chip" onclick="go('${k}')"><i>${byId[k].status==="e"?"† ":""}${esc(byId[k].name)}</i></a>`).join("")}</div></div>`}
  h+=`<p class="note">Tree data from the earlier version of the atlas (your genus list and clade backbone).</p></div>`;
  $("#view").innerHTML=h}
