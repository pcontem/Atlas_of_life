/* Atlas of Life — Encyclopedia search box and the Index view. */
/* ---------- encyclopedia search & index ---------- */
let ALL=[];
function matches(q,limit){q=q.trim().toLowerCase();if(q.length<2)return[];
  const r=[];for(const n of ALL){const k=n.name.toLowerCase();const i=k.indexOf(q);if(i<0)continue;r.push([(i===0?0:1)+(n.ficha?0:2),n])}
  r.sort((a,b)=>a[0]-b[0]||a[1].name.localeCompare(b[1].name));return r.slice(0,limit).map(x=>x[1])}
function parentName(n){const p=byId[n.parent];return p?p.name:""}
function initSearch(){ALL=Object.values(byId).sort((a,b)=>a.name.localeCompare(b.name));
  const inp=$("#ssearch"),res=$("#sres");let hits=[],hi=0;
  const show=()=>{hits=matches(inp.value,14);hi=0;
    res.innerHTML=hits.length?hits.map((n,i)=>`<div class="sr${i===hi?" on":""}" data-id="${n.id}">${n.type==="genus"?"<i>"+esc(n.name)+"</i>":esc(n.name)}${n.ficha?' <span class="fb">entry</span>':""}<small>${n.type==="clade"?"clade":"genus"} · ${esc(parentName(n))}</small></div>`).join("")+(inp.value.trim().length>=2?`<div class="sr more" data-more="1">All results in the index →</div>`:""):(inp.value.trim().length>=2?`<div class="sr none">No match</div>`:"");
    res.querySelectorAll(".sr[data-id]").forEach(d=>d.onmousedown=e=>{e.preventDefault();pick(d.dataset.id)});
    const m=res.querySelector("[data-more]");if(m)m.onmousedown=e=>{e.preventDefault();IDXQ=inp.value;res.innerHTML="";location.hash="index";if(view==="index")renderIndex()}};
  const pick=id=>{inp.value="";res.innerHTML="";go(id)};
  inp.addEventListener("input",show);inp.addEventListener("blur",()=>setTimeout(()=>res.innerHTML="",150));
  inp.addEventListener("keydown",e=>{if(!hits.length)return;if(e.key==="ArrowDown"){hi=Math.min(hi+1,hits.length-1)}else if(e.key==="ArrowUp"){hi=Math.max(hi-1,0)}else if(e.key==="Enter"){pick(hits[hi].id);return}else return;
    e.preventDefault();res.querySelectorAll(".sr[data-id]").forEach((d,i)=>d.classList.toggle("on",i===hi))});
  $("#names").innerHTML=[...new Set(ALL.map(n=>n.name))].map(n=>`<option value="${esc(n)}">`).join("");
}
let IDXQ="",IDXF="ficha",IDXC="";
function renderIndex(){
  $("#view").innerHTML=`<div class="xl" style="max-width:1100px"><h2>Index</h2><p class="note">Every clade and genus in the atlas, A–Z. Entries marked <span class="fb">entry</span> have a full encyclopedia page; the others have a basic page.</p>
    <div class="ixbar"><input id="ixq" type="search" placeholder="Filter by name…" value="${esc(IDXQ)}"><span class="seg">${[["ficha","Full entries"],["clade","Clades"],["genus","Genera"],["all","All"]].map(([k,l])=>`<button data-f="${k}" class="${IDXF===k?"on":""}">${l}</button>`).join("")}</span><span id="ixn" class="note"></span></div>
    <div class="ixbar" style="margin-top:0"><input id="ixc" type="search" placeholder="Filter by clade…" list="clnames" value="${esc(IDXC?byId[IDXC].name:"")}" autocomplete="off"><datalist id="clnames">${ALL.filter(n=>n.type==="clade").map(n=>`<option value="${esc(n.name)}">`).join("")}</datalist><span id="ixcn" class="note"></span></div>
    <div id="ixletters" class="ixletters"></div><div id="ixlist"></div></div>`;
  const draw=()=>{const q=IDXQ.trim().toLowerCase();
    let inC=null;if(IDXC){inC=new Set();(function r(k){inC.add(k);(children[k]||[]).forEach(r)})(IDXC);inC.delete(IDXC)}
    $("#ixcn").innerHTML=IDXC?`Showing everything inside <b>${esc(byId[IDXC].name)}</b> · <a style="cursor:pointer" id="ixcclr">clear</a>`:"Pick a clade to list all genera inside it.";
    const cl=$("#ixcclr");if(cl)cl.onclick=()=>{IDXC="";$("#ixc").value="";draw()};
    const L=ALL.filter(n=>(IDXF==="all"||(IDXF==="ficha"?n.ficha:n.type===IDXF))&&(!q||n.name.toLowerCase().includes(q))&&(!inC||inC.has(n.id)));
    $("#ixn").textContent=L.length+" entries";
    const groups={};for(const n of L){const c=n.name[0].toUpperCase();(groups[c]=groups[c]||[]).push(n)}
    const ks=Object.keys(groups).sort();
    $("#ixletters").innerHTML=ks.map(k=>`<a data-l="${k}">${k}</a>`).join("");
    $("#ixlist").innerHTML=ks.map(k=>`<div class="ixg" id="ix-${k}"><h3>${k}</h3><div class="ixcols">${groups[k].slice(0,1500).map(n=>`<a class="ixe" onclick="go('${n.id}')">${n.type==="genus"?"<i>"+(n.status==="e"&&!n.ficha?"† ":"")+esc(n.name)+"</i>":"<b>"+esc(n.name)+"</b>"}${n.ficha?' <span class="fb">entry</span>':""}<small>${esc(parentName(n))}</small></a>`).join("")}</div></div>`).join("")||`<p class="note">Nothing matches.</p>`;
    $("#ixletters").querySelectorAll("a").forEach(a=>a.onclick=()=>document.getElementById("ix-"+a.dataset.l).scrollIntoView({behavior:"smooth"}))};
  $("#ixq").addEventListener("input",e=>{IDXQ=e.target.value;draw()});
  const setF=f=>{IDXF=f;document.querySelectorAll(".ixbar [data-f]").forEach(x=>x.classList.toggle("on",x.dataset.f===f))};
  $("#ixc").addEventListener("input",e=>{const v=e.target.value.trim().toLowerCase();
    if(!v){if(IDXC){IDXC="";draw()}return}
    const c=ALL.find(n=>n.type==="clade"&&n.name.toLowerCase()===v);if(c&&c.id!==IDXC){IDXC=c.id;setF("genus");draw()}});
  document.querySelectorAll(".ixbar [data-f]").forEach(b=>b.onclick=()=>{IDXF=b.dataset.f;document.querySelectorAll(".ixbar [data-f]").forEach(x=>x.classList.toggle("on",x===b));draw()});
  draw();
}
