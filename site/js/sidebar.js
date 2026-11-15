/* Atlas of Life — Encyclopedia sidebar tree and shared page bits. */
/* ---------- side tree ---------- */
function renderSide(){const p=path(cur||"vida").filter(n=>n.type==="clade");const rootN=p.length>7?p[p.length-7]:byId["vida"];
  const up=rootN.id!=="vida"?`<div class="sup">${p.slice(0,p.indexOf(rootN)).slice(-3).map(n=>`<a onclick="go('${n.id}')">${esc(n.name)}</a>`).join(" › ")} <a onclick="go('vida')" title="Go to the root">↑ root</a></div>`:"";
  $("#stree").innerHTML=up+nodeHTML(rootN.id);
  $("#stree").querySelectorAll(".row").forEach(r=>r.onclick=e=>{const id=r.dataset.id;
    if(e.target.classList.contains("tog")&&byId[id].type==="clade"){open.has(id)?open.delete(id):open.add(id);renderSide();return}
    go(id)});
  const s=$("#stree .sel");if(s)s.scrollIntoView({block:"nearest"})}
function nodeHTML(id){const n=byId[id];
  if(n.type==="genus"){const c=n.ficha?era(n.fad||100)[3]:n.status==="v"?"#2f7350":n.status==="e"?"#a8622f":"#b9b09c";return `<div class="node"><div class="row ${cur===id&&view==="tree"?"sel":""}" data-id="${esc(id)}"><span class="tog"></span><span class="dot" style="background:${c}"></span><i>${n.status==="e"&&!n.ficha?"† ":""}${esc(n.name)}</i></div></div>`}
  const isOpen=open.has(id);const kids=children[id];
  const cl=kids.filter(k=>byId[k].type==="clade"),gs=kids.filter(k=>byId[k].type==="genus").sort();
  const isd=gs.filter(g=>byId[g].isd),reg=gs.filter(g=>!byId[g].isd);
  let h=`<div class="node"><div class="row ${cur===id&&view==="tree"?"sel":""}" data-id="${id}"><span class="tog">${isOpen?"▾":"▸"}</span><span class="cl" style="${n.ficha?"":"font-weight:500"}">${esc(n.name)}</span><span class="cnt">${n.stat.g}</span></div>`;
  if(isOpen){h+=`<div class="kids">`+cl.map(nodeHTML).join("")+reg.map(nodeHTML).join("");
    if(isd.length)h+=`<div class="is" style="padding-left:22px">incertae sedis</div>`+isd.map(nodeHTML).join("");h+="</div>"}
  return h+"</div>"}

/* ---------- shared bits ---------- */
function crumbs(id){const p=path(id).slice(0,-1);const lk=n=>`<a onclick="go('${n.id}')">${esc(n.name)}</a>`;
  const short=p.length>6?[lk(p[0]),`<a title="${esc(p.slice(1,-4).map(n=>n.name).join(" › "))}" onclick="this.parentNode.innerHTML=this.parentNode.dataset.full">…</a>`,...p.slice(-4).map(lk)]:p.map(lk);
  return `<div class="crumbs" data-full="${esc(p.map(lk).join(" › "))}">${short.join(" › ")}</div>`}
// small time bar used on entry pages: the window covers the periods containing the spans
function timeline(spans,h=58){const W=600,P=12,ok=spans.filter(s=>s[0]!=null);if(!ok.length)return "";
  const hi=Math.max(...ok.map(s=>s[0])),lo=Math.min(...ok.map(s=>s[1])),pa=era(hi),pb=era(lo>0?lo+1e-6:lo);
  let A=pa[1]||hi,B=pb[2]!=null&&pb[1]?pb[2]:lo;if(A-B>(hi-lo)*8&&hi-lo>0){A=Math.min(A,hi+(hi-lo)*0.6);B=Math.max(B,lo-(hi-lo)*0.6)}
  const x=v=>P+(A-v)/(A-B)*(W-2*P),top=tsRows(A,B,x,0,20,1.5),H=h+34;let s=`<svg viewBox="0 0 ${W} ${H}" style="max-height:${Math.max(80,H*0.95)}px">`+top.svg;
  for(const t of top.fine||[])s+=`<line x1="${x(Math.min(t.base,A))}" x2="${x(Math.min(t.base,A))}" y1="40" y2="${H-20}" stroke="#e2d9c6"/>`;
  ok.forEach((sp,i)=>{const a=x(sp[0]),b=Math.max(x(sp[1]),a+3);s+=`<rect x="${a}" y="${46+i*8}" width="${b-a}" height="7" rx="2" fill="${sp[2]||"var(--accent)"}"/>`});
  return s+tsTicks(A,B,x,H-3,40,H-20,1.4)+"</svg>"}
function sources(list){return `<ol class="src">${list.map(s=>`<li><span class="kind">${esc(s.kind)}</span>${esc(s.text)}${s.url?` <a href="${esc(s.url)}" target="_blank" rel="noopener">link</a>`:""}</li>`).join("")}</ol>`}
const lic=(l,u)=>u?`<a href="${esc(u)}" target="_blank" rel="noopener">${esc(l)}</a>`:esc(l);
const licName=u=>{const m=String(u).match(/licenses\/([a-z-]+)\/([\d.]+)/);if(m)return "CC "+m[1].toUpperCase()+" "+m[2];if(/zero/.test(u))return "CC0 1.0";if(/mark/.test(u))return "Public domain mark";return u};
