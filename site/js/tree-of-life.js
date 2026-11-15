/* Atlas of Life — Tree of life view (D3). Not a cladogram: an outline of the classification. */
const CL=(()=>{let svg,g,zoom,t=null,sel=null,timer=null,pos={},layout="linear",rroot="vida";
  const DX=22,DY=270,RING=150;
  function visTree(id){const n=byId[id];return{id,children:n.type==="clade"&&open.has(id)?children[id].map(visTree):null}}
  function render(focusId){
    $("#view").innerHTML=`<div id="cwrap"><svg id="csvg"><defs><clipPath id="cc"><circle r="10"/></clipPath></defs><g id="cg"></g></svg>
      <div class="ctools"><span class="cbox"><input id="csearch" type="search" placeholder="Search a clade or genus…" autocomplete="off"><div id="cres"></div></span><button data-a="go">Search</button><button data-a="prune" title="Close every node except the path to the highlighted one">Prune</button><button data-a="root">Root</button><button data-a="collapse">Collapse all</button><button data-a="up" class="ronly" title="Centre the radial view on the parent group">↑ Parent group</button><span class="lay"><button data-l="linear">Linear</button><button data-l="radial">Radial</button></span></div>
      <div class="chint">Search: opens all subgroups of a clade and collapses the rest · Prune: closes everything except the path to the highlighted node · Linear / Radial: switch the layout (radial is centred on the selected group; ↑ Parent group widens it) · Click: select · Double-click: open / close a group · Double-click the info card or switch to Encyclopedia (top menu) to read the selected node · Drag and scroll to move and zoom</div><div id="cinfo"></div></div>`;
    svg=d3.select("#csvg");g=d3.select("#cg");
    zoom=d3.zoom().scaleExtent([0.08,3]).on("zoom",e=>{t=e.transform;g.attr("transform",t)});
    svg.call(zoom).on("dblclick.zoom",null);
    // search box: ranked suggestions (clades first), arrows + Enter, Enter without a pick takes the best match
    const inp=$("#csearch"),res=$("#cres");let hits=[],hi=0;
    const rank=q=>matches(q,40).sort((x,y)=>{const k=n=>(n.name.toLowerCase().startsWith(q.trim().toLowerCase())?0:2)+(n.type==="clade"?0:1);return k(x)-k(y)}).slice(0,12);
    const show=()=>{const q=inp.value;hits=rank(q);hi=0;
      res.innerHTML=hits.map((n,i)=>`<div class="sr${i===hi?" on":""}" data-id="${n.id}">${n.type==="genus"?"<i>"+esc(n.name)+"</i>":esc(n.name)}${n.ficha?' <span class="fb">entry</span>':""}<small>${n.type==="clade"?"clade · "+n.stat.g+" genera":"genus"} · in ${esc(parentName(n))}</small></div>`).join("")
        ||(q.trim().length>=2?`<div class="sr none">No clade or genus matches “${esc(q.trim())}”</div>`:"");
      res.querySelectorAll(".sr[data-id]").forEach(d=>d.onmousedown=e=>{e.preventDefault();pick(d.dataset.id)})};
    const pick=id=>{inp.value=byId[id].name;res.innerHTML="";inp.blur();isolate(id)};
    const runSearch=()=>{const q=inp.value.trim();if(q.length<2){$("#cinfo").innerHTML=q?`<div class="ci"><div>Type at least two letters.</div></div>`:"";return}
      const exact=byName[q.toLowerCase()];const id=hits.length?hits[hi].id:exact||(rank(q)[0]||{}).id;
      if(id)pick(id);else $("#cinfo").innerHTML=`<div class="ci"><div>No clade or genus matches “${esc(q)}”.</div></div>`};
    inp.addEventListener("input",show);inp.addEventListener("focus",()=>{if(inp.value.trim().length>=2)show()});
    inp.addEventListener("blur",()=>setTimeout(()=>res.innerHTML="",150));
    inp.addEventListener("keydown",e=>{if(e.key==="Enter"){e.preventDefault();runSearch();return}
      if(e.key==="Escape"){res.innerHTML="";return}if(!hits.length)return;
      if(e.key==="ArrowDown")hi=Math.min(hi+1,hits.length-1);else if(e.key==="ArrowUp")hi=Math.max(hi-1,0);else return;
      e.preventDefault();res.querySelectorAll(".sr[data-id]").forEach((d,i)=>d.classList.toggle("on",i===hi))});
    const setLay=()=>{document.querySelectorAll(".lay button").forEach(b=>b.classList.toggle("on",b.dataset.l===layout));$("#cwrap").classList.toggle("radial",layout==="radial")};setLay();
    document.querySelectorAll(".lay button").forEach(b=>b.onclick=()=>{if(layout===b.dataset.l)return;layout=b.dataset.l;setLay();
      const id=sel||cur||"vida";if(layout==="radial")setRoot(id);g.selectAll("*").remove();draw();
      if(layout==="radial")fit(rroot);else if(byId[id].type==="clade"&&open.has(id))fit(id);else center(id)});
    document.querySelectorAll(".ctools button[data-a]").forEach(b=>b.onclick=()=>{const a=b.dataset.a;
      if(a==="go")runSearch();else if(a==="collapse"){open=new Set(["vida"]);rroot="vida";draw();center("vida")}
      else if(a==="root"){if(layout==="radial"){rroot="vida";draw();fit("vida")}else center("vida")}
      else if(a==="up"){const p=byId[rroot].parent;if(p){rroot=p;open.add(p);draw();fit(p)}}else if(a==="prune")prune()});
    if(t)svg.call(zoom.transform,t);
    // sync with the encyclopedia: the entry being read becomes the highlighted node
    if(focusId&&byId[focusId]){reveal(focusId);sel=focusId;draw();center(focusId);info(focusId)}
    else{draw();if(!t)center("vida");if(sel)info(sel)}
  }
  function draw(anchor){
    const rad=layout==="radial",root=d3.hierarchy(visTree(rad?rroot:"vida"));
    if(rad){// radial: angle from the leaves, one ring per level; big enough that leaves keep ~DX px apart
      const R=Math.max(root.height*RING,root.leaves().length*DX*1.15/(2*Math.PI));
      d3.tree().size([2*Math.PI,R]).separation((a,b)=>(a.parent===b.parent?1:2)/Math.max(1,a.depth))(root);
      root.y_step=root.height?R/root.height:R;root.each(d=>{d.px=d.y*Math.sin(d.x);d.py=-d.y*Math.cos(d.x)})}
    else{d3.tree().nodeSize([DX,DY]).separation((a,b)=>{const o=x=>x.children?1.6:1;return Math.max(o(a),o(b))*(a.parent===b.parent?1:1.25)})(root);
      root.each(d=>{d.px=d.y;d.py=d.x})}
    const old=anchor&&pos[anchor];pos={};root.each(d=>pos[d.data.id]=[d.px,d.py]);
    const L=g.selectAll("path.lk").data(root.links(),d=>d.target.data.id);
    // radial: one ring per level; each child's branch leaves its parent's ring along an arc, then runs straight out to its own ring
    const P=(a,r)=>`${(r*Math.sin(a)).toFixed(1)},${(-r*Math.cos(a)).toFixed(1)}`;
    const elbow=l=>{const s=l.source,c=l.target;return `M${P(s.x,s.y)}A${s.y},${s.y} 0 0 ${c.x>s.x?1:0} ${P(c.x,s.y)}L${P(c.x,c.y)}`};
    g.selectAll("circle.ring").data(rad?d3.range(1,root.height+1).map(i=>i*root.y_step):[]).join("circle").attr("class","ring").attr("r",d=>d).lower();
    L.join("path").attr("class","lk").attr("d",rad?elbow:d3.linkHorizontal().x(d=>d.y).y(d=>d.x));
    const N=g.selectAll("g.nd").data(root.descendants(),d=>d.data.id).join(enter=>{const e=enter.append("g").attr("class","nd");
        e.append("circle").attr("class","c");e.append("image").attr("class","im");e.append("text").attr("class","tx");e.append("title");return e});
    N.attr("transform",d=>`translate(${d.px},${d.py})`).each(function(d){const n=byId[d.data.id],el=d3.select(this),isC=n.type==="clade",closed=isC&&!open.has(n.id)&&children[n.id].length;
      const img=n.ficha&&n.images&&n.images.length?imgKey(n.name,n.images[0].kind):null;
      const col=n.status==="v"?"#2f7350":n.status==="e"?"#a8622f":"#8b8371";
      el.classed("sel",n.id===sel).classed("ficha",n.ficha);
      el.select("circle.c").attr("r",img?11:isC?5:3.5).attr("fill",closed?col:"#fbf8f1").attr("stroke",col).attr("stroke-width",isC?1.6:1.2);
      el.select("image.im").attr("href",img).attr("x",-10).attr("y",-10).attr("width",20).attr("height",20).attr("preserveAspectRatio","xMidYMid slice").attr("clip-path","url(#cc)").style("display",img?null:"none");
      const inner=isC&&open.has(n.id)&&children[n.id].length;
      const tx=el.select("text.tx").attr("class","tx"+(isC?" cl":" gn")+(n.ficha?" fi":""));
      if(rad){const deg=d.x*180/Math.PI-90,flip=d.x>Math.PI,off=img?15:9;// labels point outwards, never upside down
        tx.attr("transform",d.depth?`rotate(${flip?deg+180:deg})`:null).attr("x",d.depth?(flip?-off:off):-4).attr("dy",!d.depth?"-0.9em":inner?"-0.45em":"0.32em").attr("text-anchor",d.depth&&flip?"end":"start")}
      else tx.attr("transform",null).attr("x",inner?-4:img?15:9).attr("dy",inner?"-0.75em":"0.32em").attr("text-anchor","start");
      tx
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
    sel=id;cur=id;setRoot(id);draw();fit(layout==="radial"?rroot:id);info(id)}
  // the radial view is drawn around one group: the selected clade, or the group of a selected genus
  function setRoot(id){const n=byId[id];rroot=n.type==="clade"?id:(n.parent||"vida");open.add(rroot)}
  function prune(){const id=sel||cur||"vida";const keep=new Set();let p=byId[byId[id].parent];while(p){keep.add(p.id);p=byId[p.parent]}
    if(open.has(id))keep.add(id);keep.add("vida");open=keep;sel=id;cur=id;draw();center(id);info(id)}
  function fit(id){const ids=[];(function r(k){if(!pos[k])return;ids.push(k);if(byId[k].type==="clade"&&open.has(k))children[k].forEach(r)})(id);
    const xs=ids.map(k=>pos[k][0]),ys=ids.map(k=>pos[k][1]);const rad=layout==="radial",P=rad?190:20,x0=Math.min(...xs)-P,x1=Math.max(...xs)+(rad?P:230),y0=Math.min(...ys)-P,y1=Math.max(...ys)+P;
    const r=$("#csvg").getBoundingClientRect(),top=60,bottom=40,W=r.width-40,H=r.height-top-bottom;
    const k=Math.max(0.08,Math.min(1.2,Math.min(W/(x1-x0||1),H/(y1-y0||1))));
    svg.call(zoom.transform,d3.zoomIdentity.translate(20+(W-(x1-x0)*k)/2-x0*k,top+(H-(y1-y0)*k)/2-y0*k).scale(k))}
  function focus(id){reveal(id);if(byId[id].type==="clade")open.add(id);sel=id;draw();center(id);info(id)}
  function info(id){const n=byId[id];if(!n){return}const path=(()=>{const p=[];let m=byId[n.parent];while(m&&p.length<4){p.unshift(m.name);m=byId[m.parent]}return p.join(" › ")})();
    const im=n.ficha&&n.images&&n.images[0];
    $("#cinfo").innerHTML=`<div class="ci">${im?`<img src="${imgKey(n.name,im.kind)}" alt="">`:""}<div><div class="cpath">${esc(path)}</div><div class="cname">${n.type==="genus"?"<i>":""}${esc(n.name)}${n.type==="genus"?"</i>":""}</div>
      <div class="note">${n.type==="clade"?n.stat.g+" genera":""}${n.ficha&&n.type==="genus"?esc(n.early||"")+" · "+(n.ws?"wingspan "+n.ws[1]+" m":""):""}${!n.ficha&&n.status?(n.status==="e"?" · extinct":" · living"):""}</div>
      ${n.ficha?`<p style="margin:6px 0 0;font-size:13px">${esc(n.sum)}</p>`:n.note?`<p style="margin:6px 0 0;font-size:13px">${esc(n.note)}</p>`:""}
      <div class="note" style="margin-top:6px">Double-click this card (or switch to <b>Encyclopedia</b> above) to read ${n.ficha?"its entry":"its basic page"}.</div></div></div>`;
    const card=$("#cinfo .ci");card.title="Double-click to open in the encyclopedia";card.ondblclick=()=>{location.hash=id}}
  function show(id){location.hash="tree-of-life";setTimeout(()=>isolate(id),30)}
  return{render,focus,show,isolate};
})();
