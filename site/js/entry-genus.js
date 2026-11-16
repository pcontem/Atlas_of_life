/* Atlas of Life — Genus entry page and the size diagram (human = 1.8 m). */
/* ---------- size diagram ---------- */
const HUMAN="M50 0c7 0 12 6 12 13s-5 13-12 13-12-6-12-13 5-13 12-13zM34 30h32c8 0 13 6 14 13l7 52c1 5-3 8-7 7-3 0-5-3-6-6l-6-40-2 0v136c0 6-4 9-9 9s-8-3-8-9v-82h-2v82c0 6-4 9-8 9s-9-3-9-9V56l-2 0-6 40c-1 3-3 6-6 6-4 1-8-2-7-7l7-52c1-7 6-13 14-13z"; // ~ 1.8 m tall in a 0..195 box
const WING="M0 24 C30 18 70 12 92 13 L97 6 C99 3 101 3 103 6 L108 13 C130 12 170 18 200 24 C170 26 135 30 110 31 L106 46 L102 40 L98 40 L94 46 L90 31 C65 30 30 26 0 24Z"; // generic front view, wings spread
function sizeDiagram(g){
  const ws=g.ws?g.ws[1]:null,s=g.silhouette;
  if(!ws){const s2=g.silhouette;return `<p class="note">No published wingspan estimate in the sources used — size diagram not drawn.</p>`+(s2?`<figure style="display:flex;gap:12px;align-items:center"><img src="${silSrc(s2)}" alt="" style="max-width:150px;max-height:90px;opacity:.85"><figcaption style="margin:0">Silhouette (not to scale)${s2.genus_level?"":` of a related form: <i>${esc(s2.depicts||"")}</i> (${esc(s2.matched)})`}. By ${esc(s2.attribution)}, ${lic(licName(s2.license),s2.license)}, via <a href="${esc(s2.page)}" target="_blank" rel="noopener">PhyloPic</a>.</figcaption></figure>`:"")}
  const H=210,unit=Math.max(ws,1.8)*1.15,W=520,pxm=Math.min((W-90)/unit,H*0.82/1.8);
  const human=1.8*pxm,hs=human/195;let svg=`<svg viewBox="0 0 ${W} ${H+30}" style="width:100%;max-width:560px">`;
  const ground=H;svg+=`<line x1="0" x2="${W}" y1="${ground}" y2="${ground}" stroke="#bbb1"/>`;
  // grid 1 m
  for(let m=0;m*pxm<W;m++)svg+=`<line x1="${20+m*pxm}" x2="${20+m*pxm}" y1="${ground}" y2="${ground+5}" stroke="#a99f88"/>${m%(ws>6?2:1)===0?`<text x="${20+m*pxm}" y="${ground+16}" font-size="9" text-anchor="middle" fill="#756f60">${m} m</text>`:""}`;
  svg+=`<g transform="translate(${20},${ground-human}) scale(${hs})"><path d="${HUMAN}" fill="#5e5a4f"/></g>`;
  svg+=`<text x="${20+50*hs}" y="${ground-human-6}" font-size="10" text-anchor="middle" fill="#5e5a4f">1.8 m</text>`;
  const x0=20+110*hs+20,wpx=ws*pxm;
  {const hpx=wpx*0.3,y=ground-human*0.62-hpx/2;svg+=`<g transform="translate(${x0},${y}) scale(${wpx/200},${hpx/60})"><path d="${WING}" fill="#7a5a44" opacity=".85"/></g>`}
  svg+=`<line x1="${x0}" x2="${x0+wpx}" y1="${ground-6}" y2="${ground-6}" stroke="var(--accent)" stroke-width="2"/><line x1="${x0}" x2="${x0}" y1="${ground-11}" y2="${ground-1}" stroke="var(--accent)" stroke-width="2"/><line x1="${x0+wpx}" x2="${x0+wpx}" y1="${ground-11}" y2="${ground-1}" stroke="var(--accent)" stroke-width="2"/>`;
  svg+=`<text x="${x0+wpx/2}" y="${ground-14}" font-size="11" text-anchor="middle" fill="var(--accent)">wingspan ${g.ws[0]!==g.ws[1]?"up to ":""}${ws} m</text></svg>`;
  let note="",side="";
  if(s){side=`<figure style="margin-top:10px;display:flex;gap:12px;align-items:center"><img src="${silSrc(s)}" alt="" style="max-width:150px;max-height:90px;opacity:.85"><figcaption style="margin:0">Silhouette (not to scale)${s.genus_level?` of <i>${esc(s.depicts||g.name)}</i>`:` of a related form: <i>${esc(s.depicts||"")}</i> (${esc(s.matched)}) — none exists yet for <i>${esc(g.name)}</i>`}. By ${esc(s.attribution)}, ${lic(licName(s.license),s.license)}, via <a href="${esc(s.page)}" target="_blank" rel="noopener">PhyloPic</a>.</figcaption></figure>`}
  note="Brown outline: schematic pterosaur scaled to the maximum wingspan (not genus-specific). Human figure 1.8 m. ";
  return svg+`<p class="note">${note}${esc(g.wsnote||"")}</p>`+side}

/* ---------- genus entry ---------- */
function renderFicha(id){const n=byId[id];if(id==="vida"&&D.home)return renderHome();if(!n.ficha)return renderBasic(id);if(n.type==="clade")return renderClade(id);
  if(!n.full){$("#view").innerHTML=`<div class="empty">Loading <i>${esc(n.name)}</i>…</div>`;
    loadGenus(id).then(()=>{if(cur===id&&view==="tree")renderFicha(id)}).catch(()=>{if(cur===id)$("#view").innerHTML=`<div class="empty">Could not load the entry of <i>${esc(n.name)}</i>.</div>`});return}
  const g=n;
  const imgs=g.images||[];let gi=0;
  const pathC=path(id).slice(0,-1).filter(c=>c.ficha);
  let h=`<div class="ficha">${crumbs(id)}<h2><i>${esc(g.name)}</i></h2><div class="auth">${esc(g.author||"")} · ${esc(g.early)}${g.late?"–"+esc(g.late):""} · ${fmtMa(g.fad)}–${fmtMa(g.lad)}</div>`;
  h+=`${g.type_species?`<span class="badge">Type species: <i>${esc(g.type_species)}</i></span>`:""}<span class="badge">${esc(g.completeness)} material</span>`;
  if(g.isd)h+=`<span class="badge warn">incertae sedis in ${esc(byId[g.clade].name)}</span>`;
  h+=curBadge(g.cur);
  h+=`<p class="lead">${esc(g.sum)}</p><div class="grid"><div>`;
  // images
  // gallery: one tab per kind (life restorations, fossils, skeletal reconstructions), thumbnails below the main image
  const KINDS=[["life","Life restorations"],["fossil","Fossils"],["skeletal","Skeletal reconstructions"]].filter(([k])=>imgs.some(im=>im.kind===k));
  h+=`<div class="card"><h3>Images${imgs.length>1?` <span class="note">(${imgs.length})</span>`:""}</h3>`;
  if(imgs.length){h+=`<div class="imgtabs">${KINDS.map(([k,l],i)=>`<button data-k="${k}" class="${i?"":"on"}">${l} (${imgs.filter(im=>im.kind===k).length})</button>`).join("")}</div>`;
    h+=`<figure id="fig"></figure><div id="thumbs" class="thumbs"></div>`}else h+=`<p class="note">No openly licensed restoration or fossil photograph was found for this genus. The silhouette below is the only image.</p>`;
  // links to artwork that may not be copied (no local copy, no thumbnail): title, artist, site, opens in a new tab
  const ext=g.external||[];
  if(ext.length)h+=`<div class="extart"><h4>More reconstructions elsewhere <span class="note">(links, not reproduced here)</span></h4><ul>${ext.map(x=>`<li><a href="${esc(x.url)}" target="_blank" rel="noopener">${esc(x.title)}</a> — ${esc(x.artist)} <span class="note">· ${esc(x.site)} · ${x.kind==="life"?"life restoration":x.kind==="skeletal"?"skeletal reconstruction":"fossil"}${x.review==="accepted"?"":" · not reviewed"}</span></li>`).join("")}</ul></div>`;
  h+=`</div>`;
  h+=`<div class="card"><h3>Size</h3>${sizeDiagram(g)}</div>`;
  h+=`<div class="card"><h3>Biology</h3><p style="margin:0">${esc(g.biology)}</p></div>`;
  h+=`</div><div>`;
  h+=`<div class="card"><h3>Time range</h3><div class="tl">${timeline([[g.fad,g.lad,era(g.fad)[3]]],48)}</div>${g.dates_note?`<p class="note">${esc(g.dates_note)}</p>`:""}</div>`;
  h+=`<div class="card"><h3>Fossil material</h3><dl class="kv"><dt>Holotype</dt><dd>${esc(g.holotype)}</dd><dt>Known material</dt><dd>${esc(g.material)}</dd><dt>Completeness</dt><dd>${esc(g.completeness)}</dd>${g.exceptional?`<dt>Exceptional</dt><dd>${esc(g.exceptional)}</dd>`:""}</dl></div>`;
  h+=`<div class="card"><h3>Classification</h3><p style="margin:0 0 6px">${pathC.map(c=>`<a style="cursor:pointer" onclick="go('${c.id}')">${esc(c.name)}</a>`).join(" › ")}</p>${g.isnote?`<p class="note" style="margin:0">${esc(g.isnote)}</p>`:""}</div>`;
  h+=`</div></div>`;
  // formations
  h+=`<div class="card"><h3>Geological formations (${g.formations.length})</h3><table><tr><th>Formation</th><th>Member / unit</th><th>Country · region</th><th>Interval</th><th>Occ.</th></tr>${g.formations.map(f=>`<tr><td>${(f.ids||[]).filter(Boolean).length?(f.ids.length===1?`<a style="cursor:pointer" onclick="location.hash='formation/${f.ids[0]}'">${esc(f.formation)}</a>`:`${esc(f.formation)} <span class="note">(${f.ids.map(i=>{const x=(D.formations||[]).find(y=>y.id===i);return `<a style="cursor:pointer" onclick="location.hash='formation/${i}'">${esc(x?x.name:i)}</a>`}).join(", ")})</span>`):esc(f.formation)}${f.group?` <span class="note">(${esc(f.group)} Gr.)</span>`:""}</td><td>${esc(f.members.join(", "))}</td><td>${esc(f.country)}${f.regions.length?" · "+esc(f.regions.join(", ")):""}</td><td>${esc(f.interval)}${f.ma?` <span class="note">${f.ma[1]}–${f.ma[0]} Ma</span>`:""}</td><td>${f.n??""}</td></tr>`).join("")}</table><p class="note">Occurrences from the Paleobiology Database unless noted; “Unnamed unit” = no formation recorded.</p></div>`;
  // species
  h+=`<div class="card"><h3>Species (${g.species.length})</h3><table><tr><th>Species</th><th>Authority</th><th>Interval</th></tr>${g.species.map(s=>`<tr><td><i>${esc(s.name)}</i></td><td>${esc(s.author)}</td><td>${esc(s.interval)}${s.fad?` <span class="note">${fmtMa(s.fad)}–${fmtMa(s.lad)}</span>`:""}</td></tr>`).join("")}</table><p class="note">Valid species only; nomina dubia are listed under “Excluded names”.</p></div>`;
  h+=`<div class="card"><h3>Sources</h3>${sources(g.sources)}</div>${curCard(g.cur,g.name,true)}</div>`;
  $("#view").innerHTML=h;
  const srcOf=im=>im.local||imgKey(g.name,im.kind);
  const show=i=>{const im=imgs[i];if(!im)return;$("#fig").innerHTML=`<div class="hero"><img src="${srcOf(im)}" alt="${esc(im.caption)}" onerror="this.replaceWith(Object.assign(document.createElement('p'),{className:'note',textContent:'Image unavailable offline — see the source link.'}))"></div><figcaption>${esc(im.caption)}. ${im.artist?"By "+esc(im.artist)+", ":""}${lic(im.license,im.licurl)}${im.date?", "+esc(String(im.date).slice(0,10)):""} — <a href="${esc(im.page)}" target="_blank" rel="noopener">${/doi\.org/.test(im.page||"")?"Open-access article":"Wikimedia Commons"}</a>.${im.kind!=="fossil"?` <br>Reconstruction: interpretive${im.review==="accepted"?", reviewed for this atlas":", not yet reviewed for this atlas"}.`:""}</figcaption>`;
    document.querySelectorAll("#thumbs img").forEach(t=>t.classList.toggle("on",+t.dataset.i===i))};
  const tab=k=>{const ix=imgs.map((im,i)=>[im,i]).filter(([im])=>im.kind===k).map(([,i])=>i);
    $("#thumbs").innerHTML=ix.length>1?ix.map(i=>`<img data-i="${i}" src="${thumbSrc(g.name,imgs[i])}" alt="" loading="lazy">`).join(""):"";
    document.querySelectorAll("#thumbs img").forEach(t=>t.onclick=()=>show(+t.dataset.i));
    document.querySelectorAll(".imgtabs button").forEach(b=>b.classList.toggle("on",b.dataset.k===k));show(ix[0])};
  document.querySelectorAll(".imgtabs button").forEach(b=>b.onclick=()=>tab(b.dataset.k));if(KINDS.length)tab(KINDS[0][0]);
}
