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
    const m=res.querySelector("[data-more]");if(m)m.onmousedown=e=>{e.preventDefault();IDXM="name";IDXQ=inp.value;res.innerHTML="";location.hash="index";if(view==="index")renderIndex()}};
  const pick=id=>{inp.value="";res.innerHTML="";go(id)};
  inp.addEventListener("input",show);inp.addEventListener("blur",()=>setTimeout(()=>res.innerHTML="",150));
  inp.addEventListener("keydown",e=>{if(!hits.length)return;if(e.key==="ArrowDown"){hi=Math.min(hi+1,hits.length-1)}else if(e.key==="ArrowUp"){hi=Math.max(hi-1,0)}else if(e.key==="Enter"){pick(hits[hi].id);return}else return;
    e.preventDefault();res.querySelectorAll(".sr[data-id]").forEach((d,i)=>d.classList.toggle("on",i===hi))});
  $("#names").innerHTML=[...new Set(ALL.map(n=>n.name))].map(n=>`<option value="${esc(n)}">`).join("");
}
let IDXQ="",IDXF="ficha",IDXC="",IDXM="name",IDXT="";
/* time search: an ICS interval name (Aptian, Late Jurassic, Cretaceous…) or Ma values ("125", "150-140") */
function parseTime(v){v=v.trim();if(!v)return null;
  const m=v.replace(/ma$/i,"").trim().match(/^(\d+(?:\.\d+)?)(?:\s*[-–]\s*(\d+(?:\.\d+)?))?$/);
  if(m){const a=+m[1],b=m[2]!=null?+m[2]:a;return{base:Math.max(a,b),top:Math.min(a,b),label:m[2]!=null?`${Math.max(a,b)}–${Math.min(a,b)} Ma`:`${a} Ma`}}
  const t=(D.timescale||[]).find(x=>x.name.toLowerCase()===v.toLowerCase());
  if(t){const par=(D.timescale||[]).find(x=>x.no===t.parent);return{base:t.base,top:t.top,label:`${t.name}${par&&t.type!=="period"&&t.type!=="era"?" ("+par.name+")":""}, ${t.type}: ${fmtMa(t.base)}–${fmtMa(t.top)}`}}
  return{bad:true}}
const ageOf=n=>n.type==="genus"?(n.fad!=null?[n.fad,n.lad]:null):(n.stat&&n.stat.fad!=null?[n.stat.fad,n.stat.lad]:null);
function renderIndex(){
  const modes=[["name","Name"],["clade","Clade"],["time","Time"]];
  const ph={name:"Filter by name…",clade:"Pick a clade…",time:"Interval (e.g. Aptian, Late Jurassic) or Ma (125, 150–140)…"};
  const val=()=>IDXM==="name"?IDXQ:IDXM==="clade"?(IDXC?byId[IDXC].name:""):IDXT;
  $("#view").innerHTML=`<div class="xl" style="max-width:1100px"><h2>Index</h2><p class="note">Every clade and genus in the atlas, A–Z. Entries marked <span class="fb">entry</span> have a full encyclopedia page; the others have a basic page.</p>
    <div class="ixbar"><label class="note" for="ixmode">Search by</label><select id="ixmode">${modes.map(([k,l])=>`<option value="${k}"${IDXM===k?" selected":""}>${l}</option>`).join("")}</select>
      <input id="ixq" type="search" autocomplete="off" placeholder="${esc(ph[IDXM])}" value="${esc(val())}" list="${IDXM==="clade"?"clnames":IDXM==="time"?"tnames":""}">
      <datalist id="clnames">${ALL.filter(n=>n.type==="clade").map(n=>`<option value="${esc(n.name)}">`).join("")}</datalist>
      <datalist id="tnames">${(D.timescale||[]).filter(t=>t.type!=="eon").map(t=>`<option value="${esc(t.name)}">${esc(t.type)} · ${fmtMa(t.base)}–${fmtMa(t.top)}</option>`).join("")}</datalist></div>
    <div class="ixbar" style="margin-top:0"><span class="seg">${[["ficha","Full entries"],["clade","Clades"],["genus","Genera"],["all","All"]].map(([k,l])=>`<button data-f="${k}" class="${IDXF===k?"on":""}">${l}</button>`).join("")}</span><span id="ixn" class="note"></span></div>
    <p id="ixinfo" class="note"></p><div id="ixletters" class="ixletters"></div><div id="ixlist"></div></div>`;
  const draw=()=>{let test=()=>true,info="";
    if(IDXM==="name"){const q=IDXQ.trim().toLowerCase();if(q)test=n=>n.name.toLowerCase().includes(q)}
    else if(IDXM==="clade"){if(IDXC){const inC=new Set();(function r(k){inC.add(k);(children[k]||[]).forEach(r)})(IDXC);inC.delete(IDXC);test=n=>inC.has(n.id);
        info=`Showing everything inside <b>${esc(byId[IDXC].name)}</b> · <a style="cursor:pointer" id="ixclr">clear</a>`}else info="Pick a clade to list everything inside it."}
    else{const t=parseTime(IDXT);
      if(!t)info="Type a geological interval (stage, epoch, period or era of the ICS chart) or an age in millions of years. Entries whose known range overlaps it are listed.";
      else if(t.bad)info=`“${esc(IDXT)}” is not an ICS interval name or an age in Ma.`;
      else{test=n=>{const a=ageOf(n);return a&&a[0]>t.top&&a[1]<t.base};
        info=`Entries known from <b>${esc(t.label)}</b> (stratigraphic range overlaps the interval). Only taxa with dated fossils in the atlas can be found by time. · <a style="cursor:pointer" id="ixclr">clear</a>`}}
    $("#ixinfo").innerHTML=info;const cl=$("#ixclr");if(cl)cl.onclick=()=>{IDXC="";IDXT="";$("#ixq").value="";draw()};
    const L=ALL.filter(n=>(IDXF==="all"||(IDXF==="ficha"?n.ficha:n.type===IDXF))&&test(n));
    $("#ixn").textContent=L.length+" entries";
    const groups={};for(const n of L){const c=n.name[0].toUpperCase();(groups[c]=groups[c]||[]).push(n)}
    const ks=Object.keys(groups).sort(),tm=IDXM==="time"&&IDXT;
    $("#ixletters").innerHTML=ks.map(k=>`<a data-l="${k}">${k}</a>`).join("");
    $("#ixlist").innerHTML=ks.map(k=>`<div class="ixg" id="ix-${k}"><h3>${k}</h3><div class="ixcols">${groups[k].slice(0,1500).map(n=>{const a=tm&&ageOf(n);
      return `<a class="ixe" onclick="go('${n.id}')">${n.type==="genus"?"<i>"+(n.status==="e"&&!n.ficha?"† ":"")+esc(n.name)+"</i>":"<b>"+esc(n.name)+"</b>"}${n.ficha?' <span class="fb">entry</span>':""}<small>${esc(parentName(n))}${a?" · "+fmtMa(a[0])+"–"+fmtMa(a[1]):""}</small></a>`}).join("")}</div></div>`).join("")||`<p class="note">Nothing matches.</p>`;
    $("#ixletters").querySelectorAll("a").forEach(a=>a.onclick=()=>document.getElementById("ix-"+a.dataset.l).scrollIntoView({behavior:"smooth"}))};
  const setF=f=>{IDXF=f;document.querySelectorAll(".ixbar [data-f]").forEach(x=>x.classList.toggle("on",x.dataset.f===f))};
  $("#ixmode").addEventListener("change",e=>{IDXM=e.target.value;renderIndex();$("#ixq").focus()});
  $("#ixq").addEventListener("input",e=>{const v=e.target.value;
    if(IDXM==="name"){IDXQ=v;draw()}
    else if(IDXM==="time"){IDXT=v;const t=parseTime(v);if(t&&!t.bad)draw();else if(!v.trim())draw()}
    else{const w=v.trim().toLowerCase();if(!w){if(IDXC){IDXC="";draw()}return}
      const c=ALL.find(n=>n.type==="clade"&&n.name.toLowerCase()===w);if(c&&c.id!==IDXC){IDXC=c.id;setF("genus");draw()}}});
  $("#ixq").addEventListener("keydown",e=>{if(e.key==="Enter"&&IDXM==="time"){IDXT=e.target.value;draw()}});
  document.querySelectorAll(".ixbar [data-f]").forEach(b=>b.onclick=()=>{setF(b.dataset.f);draw()});
  draw();
}
