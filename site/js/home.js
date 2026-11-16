/* Atlas of Life — start page (the root of the tree, "Life"): an introduction to life on Earth with
   pictures of very different groups. Content and credits come from entries/home.yaml (D.home). */
function renderHome(){const h=D.home,lic=i=>i.license_url?`<a href="${esc(i.license_url)}" target="_blank" rel="noopener">${esc(i.license)}</a>`:esc(i.license);
  const credit=i=>`${esc(i.artist)}, ${lic(i)}, <a href="${esc(i.page)}" target="_blank" rel="noopener">Wikimedia Commons</a>`;
  const nodes=Object.values(byId),ng=D.genera.length,nf=(D.formations||[]).length;
  const count=id=>byId[id]&&byId[id].stat?byId[id].stat.g:0;
  $("#view").innerHTML=`<div class="home">
    <h2>${esc(h.title)}</h2><p class="lead">${esc(h.lead)}</p>
    <div class="hgrid"><div>${h.intro.map(t=>`<p>${esc(t)}</p>`).join("")}
      <div class="hgo"><button onclick="location.hash='index'">Browse the encyclopedia</button><button onclick="location.hash='tree-of-life'">Explore the tree of life</button><button onclick="location.hash='biota'">Travel through time (Biota)</button></div>
      <div class="stat hstat"><div><b>${nodes.length.toLocaleString("en")}</b><span>taxa in the tree</span></div><div><b>${ng}</b><span>genera with full entries</span></div><div><b>${nf}</b><span>geological formations</span></div></div></div>
      <figure class="hhero"><img src="${esc(h.hero.local)}" alt="${esc(h.hero.caption)}"><figcaption>${esc(h.hero.caption)}. ${credit(h.hero)}.</figcaption></figure></div>
    <h3 class="hsec">The diversity of life</h3>
    <div class="hgroups">${h.groups.map(g=>`<div class="hg" onclick="go('${g.node}')" title="Open ${esc(g.label)} in the tree">
      <div class="hgi" style="background-image:url('${esc(thumbSrc("",g.image))}')"></div>
      <div class="hgt"><b>${esc(g.label)}</b>${count(g.node)?`<span class="note">${count(g.node).toLocaleString("en")} ${count(g.node)===1?"genus":"genera"} in the tree</span>`:""}<small>${esc(g.image.caption)}</small></div></div>`).join("")}</div>
    <div class="card" style="margin-top:22px"><h3>Sources</h3><ol class="src">${h.sources.map(s=>`<li><span class="kind">${esc(s.kind)}</span>${esc(s.text)}${s.url?` <a href="${esc(s.url)}" target="_blank" rel="noopener">link</a>`:""}</li>`).join("")}</ol>
      <h3 style="margin-top:14px">Picture credits</h3><ul class="hcred">${[h.hero,...h.groups.map(g=>g.image)].map(i=>`<li><b>${esc(i.caption)}</b> — ${credit(i)}</li>`).join("")}</ul></div></div>`}
