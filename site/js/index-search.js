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
    const m=res.querySelector("[data-more]");if(m)m.onmousedown=e=>{e.preventDefault();IDXM="name";IDXQ="";IDXFIL=[{m:"name",v:inp.value.trim()}];res.innerHTML="";location.hash="index";if(view==="index")renderIndex()}};
  const pick=id=>{inp.value="";res.innerHTML="";go(id)};
  inp.addEventListener("input",show);inp.addEventListener("blur",()=>setTimeout(()=>res.innerHTML="",150));
  inp.addEventListener("keydown",e=>{if(!hits.length)return;if(e.key==="ArrowDown"){hi=Math.min(hi+1,hits.length-1)}else if(e.key==="ArrowUp"){hi=Math.max(hi-1,0)}else if(e.key==="Enter"){pick(hits[hi].id);return}else return;
    e.preventDefault();res.querySelectorAll(".sr[data-id]").forEach((d,i)=>d.classList.toggle("on",i===hi))});
  $("#names").innerHTML=[...new Set(ALL.map(n=>n.name))].map(n=>`<option value="${esc(n)}">`).join("");
}
/* Index filters stack: each chip is {m:"name"|"clade"|"time", v:text}; all chips (and the text being typed) must match */
let IDXQ="",IDXF="ficha",IDXM="name",IDXFIL=[];
/* time search: an ICS interval name (Aptian, Late Jurassic, Cretaceous…) or Ma values ("125", "150-140") */
function parseTime(v){v=v.trim();if(!v)return null;
  const m=v.replace(/ma$/i,"").trim().match(/^(\d+(?:\.\d+)?)(?:\s*[-–]\s*(\d+(?:\.\d+)?))?$/);
  if(m){const a=+m[1],b=m[2]!=null?+m[2]:a;return{base:Math.max(a,b),top:Math.min(a,b),label:m[2]!=null?`${Math.max(a,b)}–${Math.min(a,b)} Ma`:`${a} Ma`}}
  const t=(D.timescale||[]).find(x=>x.name.toLowerCase()===v.toLowerCase());
  if(t){const par=(D.timescale||[]).find(x=>x.no===t.parent);return{base:t.base,top:t.top,label:`${t.name}${par&&t.type!=="period"&&t.type!=="era"?" ("+par.name+")":""}, ${t.type}: ${fmtMa(t.base)}–${fmtMa(t.top)}`}}
  return{bad:true}}
const ageOf=n=>n.type==="genus"?(n.fad!=null?[n.fad,n.lad]:null):(n.stat&&n.stat.fad!=null?[n.stat.fad,n.stat.lad]:null);
const cladeByName=v=>ALL.find(n=>n.type==="clade"&&n.name.toLowerCase()===v.trim().toLowerCase());
// turn one filter into {test, label} or null when it is not (yet) valid
function mkFilter(f){const v=(f.v||"").trim();if(!v)return null;
  if(f.m==="name"){const q=v.toLowerCase();return{test:n=>n.name.toLowerCase().includes(q),label:`Name contains “${esc(v)}”`}}
  if(f.m==="clade"){const c=cladeByName(v);if(!c)return null;const inC=new Set();(function r(k){inC.add(k);(children[k]||[]).forEach(r)})(c.id);inC.delete(c.id);
    return{test:n=>inC.has(n.id),label:`Inside <b>${esc(c.name)}</b>`}}
  const t=parseTime(v);if(!t||t.bad)return null;
  return{test:n=>{const a=ageOf(n);return a&&a[0]>t.top&&a[1]<t.base},label:`Lived in <b>${esc(t.label)}</b>`,time:true}}
/* Genus spotlight: a side column of genera with a life reconstruction (thumbnail + name); click opens the entry.
   It follows the active filters of the Index and can be shuffled. */
let SPOT=[],SPOTKEY=null;const SPOTN=25;
const spotImg=n=>(n.images||[]).find(i=>i.kind==="life"&&i.review!=="outdated");
function spotPick(tests){const pool=ALL.filter(n=>n.type==="genus"&&n.ficha&&spotImg(n)&&tests.every(F=>F.test(n)));
  for(let i=pool.length-1;i>0;i--){const j=Math.floor(Math.random()*(i+1));[pool[i],pool[j]]=[pool[j],pool[i]]}
  SPOT=pool.slice(0,SPOTN);SPOTPOOL=pool.length}
let SPOTPOOL=0;
function drawSpot(){const el=$("#spotlist");if(!el)return;
  el.innerHTML=SPOT.length?SPOT.map(n=>`<a class="sc" onclick="go('${n.id}')" title="Open the entry of ${esc(n.name)}"><div class="sci" style="background-image:url('${esc(thumbSrc(n.name,spotImg(n)))}')"></div><div class="sct"><i>${esc(n.name)}</i><small>${esc(parentName(n))}</small></div></a>`).join(""):`<p class="note">No genus with a life reconstruction matches the current filters.</p>`}
function renderIndex(){
  const modes=[["name","Name"],["clade","Clade"],["time","Time"]];
  const ph={name:"Name contains…",clade:"Clade (e.g. Tapejaridae)…",time:"Interval (Aptian, Late Jurassic…) or Ma (125, 150-140)…"};
  $("#view").innerHTML=`<div class="ixwrap"><div class="xl ixmain"><h2>Index</h2><p class="note">Every clade and genus in the atlas, A–Z. Entries marked <span class="fb">entry</span> have a full encyclopedia page; the others have a basic page. Filters stack: add as many as you like (e.g. a clade <i>and</i> a time interval); entries must match all of them.</p>
    <div class="ixbar"><label class="note" for="ixmode">Search by</label><select id="ixmode">${modes.map(([k,l])=>`<option value="${k}"${IDXM===k?" selected":""}>${l}</option>`).join("")}</select>
      <input id="ixq" type="search" autocomplete="off" placeholder="${esc(ph[IDXM])}" value="${esc(IDXQ)}" list="${IDXM==="clade"?"clnames":IDXM==="time"?"tnames":""}"><button id="ixadd" class="ixbtn" title="Add this filter (Enter)">+ Add filter</button>
      <datalist id="clnames">${ALL.filter(n=>n.type==="clade").map(n=>`<option value="${esc(n.name)}">`).join("")}</datalist>
      <datalist id="tnames">${TS().filter(t=>t.type!=="eon"||t.name!=="Phanerozoic").map(t=>`<option value="${esc(t.name)}">${esc(t.type)} · ${fmtMa(t.base)}–${fmtMa(t.top)}</option>`).join("")}</datalist></div>
    <div id="ixchips" class="ixchips"></div>
    <div class="ixbar" style="margin-top:0"><span class="seg">${[["ficha","Full entries"],["clade","Clades"],["genus","Genera"],["all","All"]].map(([k,l])=>`<button data-f="${k}" class="${IDXF===k?"on":""}">${l}</button>`).join("")}</span><span id="ixn" class="note"></span></div>
    <p id="ixinfo" class="note"></p><div id="ixletters" class="ixletters"></div><div id="ixlist"></div></div>
    <aside class="spot"><div class="spoth"><h3>Genus spotlight</h3><button id="spotbtn" class="ixbtn" title="Show other genera">↻ Shuffle</button></div><div id="spotlist"></div><p class="note spotn">Life reconstructions of genera with a full entry. Follows the filters; click to open.</p></aside></div>`;
  const draw=()=>{const act=IDXFIL.map(f=>({f,F:mkFilter(f)})).filter(x=>x.F);const live=mkFilter({m:IDXM,v:IDXQ});
    $("#ixchips").innerHTML=act.map((x,i)=>`<span class="chip"><span class="cm">${x.f.m}</span>${x.F.label}<a title="Remove" data-rm="${IDXFIL.indexOf(x.f)}">✕</a></span>`).join("")+(act.length>1?`<a class="chipclr" id="ixclr">clear all</a>`:"");
    $("#ixchips").querySelectorAll("[data-rm]").forEach(a=>a.onclick=()=>{IDXFIL.splice(+a.dataset.rm,1);draw()});
    const cl=$("#ixclr");if(cl)cl.onclick=()=>{IDXFIL=[];draw()};
    const tests=[...act.map(x=>x.F),...(live?[live]:[])],timed=tests.some(F=>F.time);
    const skey=act.map(x=>x.f.m+":"+x.f.v).join("|");if(skey!==SPOTKEY||!SPOT.length){SPOTKEY=skey;spotPick(act.map(x=>x.F))}drawSpot();
    const bad=IDXQ.trim()&&!live&&IDXM!=="name";
    $("#ixinfo").innerHTML=bad?(IDXM==="clade"?`No clade called “${esc(IDXQ)}” — pick one from the suggestions.`:`“${esc(IDXQ)}” is not an ICS interval name or an age in Ma.`)
      :live?`Typing: ${live.label} — press Enter or “+ Add filter” to keep it and add another.`:(timed?"Only taxa with dated fossils in the atlas can be found by time.":"");
    const L=ALL.filter(n=>(IDXF==="all"||(IDXF==="ficha"?n.ficha:n.type===IDXF))&&tests.every(F=>F.test(n)));
    $("#ixn").textContent=L.length+" entries";
    const groups={};for(const n of L){const c=n.name[0].toUpperCase();(groups[c]=groups[c]||[]).push(n)}
    const ks=Object.keys(groups).sort();
    $("#ixletters").innerHTML=ks.map(k=>`<a data-l="${k}">${k}</a>`).join("");
    $("#ixlist").innerHTML=ks.map(k=>`<div class="ixg" id="ix-${k}"><h3>${k}</h3><div class="ixcols">${groups[k].slice(0,1500).map(n=>{const a=timed&&ageOf(n);
      return `<a class="ixe" onclick="go('${n.id}')">${n.type==="genus"?"<i>"+(n.status==="e"&&!n.ficha?"† ":"")+esc(n.name)+"</i>":"<b>"+esc(n.name)+"</b>"}${n.ficha?' <span class="fb">entry</span>':""}<small>${esc(parentName(n))}${a?" · "+fmtMa(a[0])+"–"+fmtMa(a[1]):""}</small></a>`}).join("")}</div></div>`).join("")||`<p class="note">Nothing matches.</p>`;
    $("#ixletters").querySelectorAll("a").forEach(a=>a.onclick=()=>document.getElementById("ix-"+a.dataset.l).scrollIntoView({behavior:"smooth"}))};
  const setF=f=>{IDXF=f;document.querySelectorAll(".ixbar [data-f]").forEach(x=>x.classList.toggle("on",x.dataset.f===f))};
  const add=()=>{const f={m:IDXM,v:IDXQ.trim()};if(!mkFilter(f))return;
    if(f.m==="clade"&&IDXF==="ficha"&&!IDXFIL.some(x=>x.m==="clade"))setF("genus");
    IDXFIL.push(f);IDXQ="";$("#ixq").value="";draw();$("#ixq").focus()};
  $("#ixmode").addEventListener("change",e=>{IDXM=e.target.value;IDXQ="";renderIndex();$("#ixq").focus()});
  $("#ixq").addEventListener("input",e=>{IDXQ=e.target.value;draw()});
  $("#ixq").addEventListener("keydown",e=>{if(e.key==="Enter"){e.preventDefault();add()}});
  $("#ixadd").onclick=add;
  $("#spotbtn").onclick=()=>{spotPick(IDXFIL.map(mkFilter).filter(Boolean));drawSpot()};
  document.querySelectorAll(".ixbar [data-f]").forEach(b=>b.onclick=()=>{setF(b.dataset.f);draw()});
  draw();
}
