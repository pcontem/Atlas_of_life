/* Atlas of Life — Cladogram view (D3). */
/* ---------- cladogram ---------- */
const CL=(()=>{let svg,g,zoom,t=null,sel=null,timer=null,pos={};
  const DX=22,DY=270;
  function visTree(id){const n=byId[id];return{id,children:n.type==="clade"&&open.has(id)?children[id].map(visTree):null}}
  function render(focusId){
    $("#view").innerHTML=`<div id="cwrap"><svg id="csvg"><defs><clipPath id="cc"><circle r="10"/></clipPath></defs><g id="cg"></g></svg>
      <div class="ctools"><input id="csearch" type="search" placeholder="Search a clade or genus…" list="names" autocomplete="off"><button data-a="go">Search</button><button data-a="prune" title="Close every node except the path to the highlighted one">Prune</button><button data-a="root">Root</button><button data-a="collapse">Collapse all</button></div>
      <div class="chint">Search: opens all subgroups of a clade and collapses the rest · Prune: closes everything except the path to the highlighted node · Click: select · Double-click: open / close a group · Switch to Encyclopedia (top menu) to read the selected node · Drag and scroll to move and zoom</div><div id="cinfo"></div></div>`;
    svg=d3.select("#csvg");g=d3.select("#cg");
    zoom=d3.zoom().scaleExtent([0.08,3]).on("zoom",e=>{t=e.transform;g.attr("transform",t)});
    svg.call(zoom).on("dblclick.zoom",null);
    const runSearch=()=>{const v=$("#csearch").value.trim().toLowerCase();if(v.length<2){if(v.length)$("#cinfo").innerHTML=`<div class="ci"><div>Type at least two letters.</div></div>`;return}const id=byName[v]||Object.keys(byName).filter(k=>k.startsWith(v)).map(k=>byName[k])[0];
      if(id)isolate(id);else $("#cinfo").innerHTML=`<div class="ci"><div>No clade or genus matches “${esc(v)}”.</div></div>`};
    $("#csearch").addEventListener("change",runSearch);$("#csearch").addEventListener("keydown",e=>{if(e.key==="Enter")runSearch()});
    document.querySelectorAll(".ctools button").forEach(b=>b.onclick=()=>{const a=b.dataset.a;
      if(a==="go")runSearch();else if(a==="collapse"){open=new Set(["vida"]);draw();center("vida")}else if(a==="root"){center("vida")}else if(a==="prune")prune()});
    if(t)svg.call(zoom.transform,t);
    // sync with the encyclopedia: the entry being read becomes the highlighted node
    if(focusId&&byId[focusId]){reveal(focusId);sel=focusId;draw();center(focusId);info(focusId)}
    else{draw();if(!t)center("vida");if(sel)info(sel)}
  }
  function draw(anchor){
    const root=d3.hierarchy(visTree("vida"));d3.tree().nodeSize([DX,DY]).separation((a,b)=>{const o=x=>x.children?1.6:1;return Math.max(o(a),o(b))*(a.parent===b.parent?1:1.25)})(root);
    const old=anchor&&pos[anchor];pos={};root.each(d=>pos[d.data.id]=[d.y,d.x]);
    const L=g.selectAll("path.lk").data(root.links(),d=>d.target.data.id);
    L.join("path").attr("class","lk").attr("d",d3.linkHorizontal().x(d=>d.y).y(d=>d.x));
    const N=g.selectAll("g.nd").data(root.descendants(),d=>d.data.id).join(enter=>{const e=enter.append("g").attr("class","nd");
        e.append("circle").attr("class","c");e.append("image").attr("class","im");e.append("text").attr("class","tx");e.append("title");return e});
    N.attr("transform",d=>`translate(${d.y},${d.x})`).each(function(d){const n=byId[d.data.id],el=d3.select(this),isC=n.type==="clade",closed=isC&&!open.has(n.id)&&children[n.id].length;
      const img=n.ficha&&n.images&&n.images.length?imgKey(n.name,n.images[0].kind):null;
      const col=n.status==="v"?"#2f7350":n.status==="e"?"#a8622f":"#8b8371";
      el.classed("sel",n.id===sel).classed("ficha",n.ficha);
      el.select("circle.c").attr("r",img?11:isC?5:3.5).attr("fill",closed?col:"#fbf8f1").attr("stroke",col).attr("stroke-width",isC?1.6:1.2);
      el.select("image.im").attr("href",img).attr("x",-10).attr("y",-10).attr("width",20).attr("height",20).attr("preserveAspectRatio","xMidYMid slice").attr("clip-path","url(#cc)").style("display",img?null:"none");
      const inner=isC&&open.has(n.id)&&children[n.id].length;
      el.select("text.tx").attr("x",inner?-4:img?15:9).attr("dy",inner?"-0.75em":"0.32em").attr("text-anchor","start").attr("class","tx"+(isC?" cl":" gn")+(n.ficha?" fi":""))
        .text((n.status==="e"&&!isC&&!n.ficha?"† ":"")+(n.name.length>32?n.name.slice(0,30)+"…":n.name)+(closed?`  (${n.stat.g})`:""));
      el.select("title").text(n.name+(n.ficha?" — full entry available":"")+"\nClick: select"+(isC?" · Double-click: open/close":""));
    }).on("click",(e,d)=>{e.stopPropagation();const id=d.data.id;if(sel===id)return;sel=id;cur=id;draw();info(id)})
      .on("dblclick",(e,d)=>{e.stopPropagation();const id=d.data.id;sel=id;cur=id;
        if(byId[id].type==="clade"&&children[id].length){open.has(id)?open.delete(id):open.add(id);draw(id)}else draw();info(id)});
    if(old&&pos[anchor]){const nw=pos[anchor],k=t?t.k:1;svg.call(zoom.translateBy,(old[0]-nw[0]),(old[1]-nw[1]))}
  }
  function center(id){const p=pos[id];if(!p)return;const r=$("#csvg").getBoundingClientRect(),k=t?Math.max(t.k,0.6):0.9;
    svg.call(zoom.transform,d3.zoomIdentity.translate(r.width*0.45-p[0]*k,r.height/2-p[1]*k).scale(k))}
  function isolate(id){const n=byId[id];open=new Set();let p=byId[n.parent];while(p){open.add(p.id);p=byId[p.parent]}
    if(n.type==="clade")(function r(k){if(byId[k].type!=="clade")return;open.add(k);children[k].forEach(r)})(id);
    sel=id;cur=id;draw();fit(id);info(id)}
  function prune(){const id=sel||cur||"vida";const keep=new Set();let p=byId[byId[id].parent];while(p){keep.add(p.id);p=byId[p.parent]}
    if(open.has(id))keep.add(id);keep.add("vida");open=keep;sel=id;cur=id;draw();center(id);info(id)}
  function fit(id){const ids=[];(function r(k){if(!pos[k])return;ids.push(k);if(byId[k].type==="clade"&&open.has(k))children[k].forEach(r)})(id);
    const xs=ids.map(k=>pos[k][0]),ys=ids.map(k=>pos[k][1]);const x0=Math.min(...xs),x1=Math.max(...xs)+220,y0=Math.min(...ys)-20,y1=Math.max(...ys)+20;
    const r=$("#csvg").getBoundingClientRect();const k=Math.max(0.08,Math.min(1.2,Math.min((r.width-380)/(x1-x0||1),(r.height-60)/(y1-y0||1))));
    svg.call(zoom.transform,d3.zoomIdentity.translate(30-x0*k,(r.height-(y1-y0)*k)/2-y0*k).scale(k))}
  function focus(id){reveal(id);if(byId[id].type==="clade")open.add(id);sel=id;draw();center(id);info(id)}
  function info(id){const n=byId[id];if(!n){return}const path=(()=>{const p=[];let m=byId[n.parent];while(m&&p.length<4){p.unshift(m.name);m=byId[m.parent]}return p.join(" › ")})();
    const im=n.ficha&&n.images&&n.images[0];
    $("#cinfo").innerHTML=`<div class="ci">${im?`<img src="${imgKey(n.name,im.kind)}" alt="">`:""}<div><div class="cpath">${esc(path)}</div><div class="cname">${n.type==="genus"?"<i>":""}${esc(n.name)}${n.type==="genus"?"</i>":""}</div>
      <div class="note">${n.type==="clade"?n.stat.g+" genera":""}${n.ficha&&n.type==="genus"?esc(n.early||"")+" · "+(n.ws?"wingspan "+n.ws[1]+" m":""):""}${!n.ficha&&n.status?(n.status==="e"?" · extinct":" · living"):""}</div>
      ${n.ficha?`<p style="margin:6px 0 0;font-size:13px">${esc(n.sum)}</p>`:n.note?`<p style="margin:6px 0 0;font-size:13px">${esc(n.note)}</p>`:""}
      <div class="note" style="margin-top:6px">Switch to <b>Encyclopedia</b> above to read ${n.ficha?"its entry":"its basic page"}.</div></div></div>`}
  function show(id){location.hash="cladogram";setTimeout(()=>isolate(id),30)}
  return{render,focus,show,isolate};
})();
