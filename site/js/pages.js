/* Atlas of Life — Excluded names and About & sources pages. */
/* ---------- excluded ---------- */
// only the names placed DIRECTLY in the selected node; sub-groups that hold more are listed to go down into
function renderExcluded(){const node=byId[cur]?cur:"vida",n=byId[node];
  const here=D.excluded.filter(e=>e.parent===node).sort((a,b)=>a.name.localeCompare(b.name));
  const cnt={};for(const e of D.excluded){let k=e.parent;while(k&&byId[k]){cnt[k]=(cnt[k]||0)+1;k=byId[k].parent}}
  const subs=(children[node]||[]).filter(k=>cnt[k]).sort((a,b)=>byId[a].name.localeCompare(byId[b].name));
  const up=n.parent&&byId[n.parent]?`<button class="ixbtn" onclick="cur='${n.parent}';renderExcluded();aboutTabs('excluded');renderSide()">↑ Parent group: ${esc(byId[n.parent].name)}</button>`:"";
  const nm=x=>byId[x].type==="genus"?`<i>${esc(byId[x].name)}</i>`:esc(byId[x].name);
  $("#view").innerHTML=`<div class="xl"><h2>Excluded names in ${nm(node)}</h2><p class="note">Names not accepted as valid taxa and therefore left out of the tree: <i>nomina dubia</i> (not diagnosable) and <i>nomina nuda</i> (published without a valid description), as recorded by the Paleobiology Database. Only names placed <b>directly</b> in ${nm(node)} are listed; each is placed in the deepest group of the atlas that PBDB assigns it to. This page follows the entry selected in the encyclopedia.</p>${up}
    ${subs.length?`<h3 style="margin-top:14px">Sub-groups with excluded names</h3><div>${subs.map(k=>`<a class="pill" onclick="cur='${k}';renderExcluded();aboutTabs('excluded');renderSide()">${nm(k)} <span class="note">${cnt[k]}</span></a>`).join("")}</div>`:""}
    ${here.length?`<table style="margin-top:14px"><tr><th>Name</th><th>Author</th><th>Status</th><th>Source</th></tr>${here.map(e=>`<tr><td><i>${esc(e.name)}</i></td><td>${esc(e.author)}</td><td>${esc(e.status)}</td><td class="note">${esc(e.ref||e.source)}</td></tr>`).join("")}</table>`
      :`<p class="note" style="margin-top:14px">No excluded names are placed directly in ${nm(node)}.${subs.length?" See the sub-groups above.":""}</p>`}</div>`}

/* ---------- about ---------- */
function renderAbout(){const n=D.genera.length,li=D.genera.filter(g=>(g.images||[]).some(i=>i.kind==="life")).length,fo=D.genera.filter(g=>(g.images||[]).length&&!(g.images||[]).some(i=>i.kind==="life")).length,gl=D.genera.filter(g=>g.silhouette&&g.silhouette.genus_level).length;
  $("#view").innerHTML=`<div class="xl"><h2>About this volume</h2>
  <p>Pilot volume of the Atlas of Life: ${n} pterosaur genera and ${D.clades.length} clades, built ${esc(D.meta.built)}.</p>
  <div class="card"><h3>Coverage</h3><dl class="kv"><dt>Genera</dt><dd>${n}</dd><dt>Life restoration</dt><dd>${li} genera</dd><dt>Fossil image only</dt><dd>${fo} genera</dd><dt>No image</dt><dd>${n-li-fo} genera (silhouette only)</dd><dt>Genus-level silhouette</dt><dd>${gl} genera; the rest use a silhouette of a related form, labelled as such</dd><dt>With size estimate</dt><dd>${D.genera.filter(g=>g.ws||g.len||g.kg).length} genera (wingspan for pterosaurs, body length for the others; mass where published)</dd></dl></div>
  <div class="card"><h3>Method</h3><ul class="diag"><li>Authority, age range, species list and geological occurrences: <a href="https://paleobiodb.org" target="_blank" rel="noopener">Paleobiology Database</a> (data service 1.2, downloaded 15 Nov 2026). Only taxa marked valid are included.</li><li>Descriptions, sizes, fossil material and biology: paraphrased from the original descriptions and redescriptions cited in each entry, via the English Wikipedia articles (exact revision linked).</li><li>Placement: each genus sits under the most inclusive clade on which analyses agree; disputed placements are marked <i>incertae sedis</i> with the competing hypotheses.</li><li>Images: Wikimedia Commons (life restorations and fossil photographs, with author and licence) and <a href="https://www.phylopic.org" target="_blank" rel="noopener">PhyloPic</a> silhouettes. No AI-generated images.</li></ul></div>
  <div class="card"><h3>Known limitations</h3><ul class="diag"><li>Life restorations are those used on English Wikipedia; they have not been independently reviewed for this atlas, and some may be outdated.</li><li>PBDB records can lag behind recent taxonomic changes (e.g. the proposed synonymy of <i>Aurorazhdarcho</i> with <i>Gnathosaurus</i>).</li><li>PBDB stratigraphic ranges include tentatively referred occurrences and can therefore be wider than the securely dated record (see the note on each entry).</li><li>Twelve recently named or renamed genera are not yet in PBDB; their ages are given as stage brackets.</li></ul></div></div>`}

/* "About & excluded names" tab: one tab, two parts (About & sources · Excluded names) */
function aboutTabs(which){const x=document.querySelector("#view .xl");if(!x)return;
  x.insertAdjacentHTML("afterbegin",`<div class="atabs"><button data-a="about" class="${which==="about"?"on":""}">About &amp; sources</button><button data-a="excluded" class="${which==="excluded"?"on":""}">Excluded names</button></div>`);
  x.querySelectorAll(".atabs button").forEach(b=>b.onclick=()=>location.hash=b.dataset.a)}
