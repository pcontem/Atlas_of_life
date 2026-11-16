/* Atlas of Life — Shared state, helpers, routing between views. */
/* geological time: ICS chart v2024/12 (D.timescale, from PBDB), Hadean to Holocene */
const TS=()=>(D&&D.timescale)||[];
const ivAt=(ma,type)=>TS().find(t=>t.type===type&&ma<=t.base&&ma>t.top)||TS().find(t=>t.type===type&&ma<=t.base&&ma>=t.top);
const TICKS=[0.01,0.02,0.05,0.1,0.2,0.5,1,2,5,10,20,25,50,100,200,250,500,1000];
// the two rows of time units to draw for a window of `span` Myr (coarse above, fine below)
const tsLevels=span=>span>1500?["eon","era"]:span>400?["era","period"]:span>60?["period","epoch"]:["epoch","age"];
// SVG: two labelled rows of ICS units between A (older, Ma) and B (younger), x = Ma→px; returns {svg,fine}
function tsRows(A,B,x,y=0,h=18,fs=1,levels){let s="";const lv=levels||tsLevels(A-B),rows=[];
  lv.forEach((type,r)=>{const units=TS().filter(t=>t.type===type&&t.base>B&&t.top<A);rows.push(units);
    for(const t of units){const a=Math.min(t.base,A),b=Math.max(t.top,B),w=x(b)-x(a),yy=y+r*h,lab=w>t.name.length*6.2*fs+6?t.name:w>22*fs&&t.name.length>3?t.name.slice(0,3)+"…":"";
      s+=`<rect x="${x(a)}" y="${yy}" width="${w}" height="${h}" fill="${t.color}" stroke="#fffdf8" stroke-width=".6"><title>${esc(t.name)} (${t.type}) ${fmtMa(t.base)}–${fmtMa(t.top)}</title></rect>`+
        (lab?`<text x="${x(a)+w/2}" y="${yy+h*0.68}" font-size="${(r?10:11)*fs}" text-anchor="middle" fill="#2b2620" pointer-events="none">${esc(lab)}</text>`:"")}});
  return{svg:s,fine:rows[rows.length-1]}}
function tsTicks(A,B,x,y,y0,y1,fs=1){const st=TICKS.find(v=>(A-B)/v<=12)||1000;let s="";
  for(let v=Math.ceil(B/st)*st;v<=A+1e-9;v+=st){const vv=+v.toFixed(3);s+=`<line x1="${x(vv)}" x2="${x(vv)}" y1="${y0}" y2="${y1}" stroke="#000" opacity=".07"/><text x="${x(vv)}" y="${y}" font-size="${9.5*fs}" text-anchor="middle" fill="#7a7266">${vv} Ma</text>`}
  return s}
let D,LIFE,byId={},byName={},children={},open=new Set(["vida"]),cur=null,view="tree";
const $=s=>document.querySelector(s);
const esc=s=>String(s??"").replace(/[&<>"]/g,c=>({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;"}[c]));
const fmtMa=v=>v==null?"?":(v>=10?v.toFixed(1).replace(/\.0$/,""):v.toFixed(2))+" Ma";
// [name, base, top, colour] of the period containing `ma` (colour used for genus bars)
const era=ma=>{const p=ivAt(ma,"period")||ivAt(ma,"era")||ivAt(ma,"eon");return p?[p.name,p.base,p.top,p.color]:["",0,0,"#9a9184"]};
const imgKey=(g,k)=>"img/"+g.replace(/[^A-Za-z]/g,"")+"_"+k+".webp";
const imgSrc=(g,im)=>im.local||imgKey(g,im.kind);
const thumbSrc=(g,im)=>"img/thumb/"+imgSrc(g,im).slice(4);/* 240-px copy made by scripts/media.py, for lists, cards and maps *//* gallery images carry their own local path */
const silSrc=s=>s?"sil/"+s.page.split("/images/")[1]+".webp":null;


function init(){
  const cl={},gn={};D.clades.forEach(c=>cl[c.id]=c);D.genera.forEach(g=>gn[g.name]=g);
  for(const[id,name,parent,st,note,k,f]of LIFE){const n={id,name,parent:parent||null,status:st,note,type:k==="c"?"clade":"genus",ficha:!!f};
    if(f)Object.assign(n,k==="c"?cl[id]:gn[id]);n.parent=parent||null;n.id=id;byId[id]=n;children[id]=[]}
  for(const n of Object.values(byId))if(n.parent)children[n.parent].push(n.id);
  for(const k in children)children[k].sort((a,b)=>{const A=byId[a],B=byId[b];return (A.type===B.type?0:A.type==="clade"?-1:1)||A.name.localeCompare(B.name)});
  const stat=id=>{const n=byId[id];if(n.type==="genus")return{g:1,fad:n.fad??null,lad:n.lad??null,cc:n.formations?n.formations.map(f=>f.country):[],e:n.status==="e"?1:0};
    let s={g:0,fad:0,lad:999,cc:new Set(),e:0};for(const k of children[id]){const t=stat(k);s.g+=t.g;s.e+=t.e;if(t.fad!=null){s.fad=Math.max(s.fad,t.fad);s.lad=Math.min(s.lad,t.lad)}t.cc.forEach(c=>s.cc.add(c))}
    if(!s.fad){s.fad=null;s.lad=null}n.stat=s;return{...s,cc:[...s.cc]}};
  stat("vida");
  const names=new Map();Object.values(byId).forEach(n=>{const k=n.name.toLowerCase();if(!byName[k])byName[k]=n.id;names.set(n.name,1)});
  $("#names").innerHTML=[...names.keys()].map(n=>`<option value="${esc(n)}">`).join("");
  initSearch();
  document.querySelectorAll("nav button").forEach(b=>b.onclick=()=>{const v=b.dataset.v;location.hash=v==="tree"?(cur||"vida"):v==="clado"?"tree-of-life":v});
  const bt=$('.seg [data-v="biota"]');if(bt&&!(D.formations||[]).length)bt.style.display="none";
  addEventListener("hashchange",route);route();
}
function route(){
  const h=decodeURIComponent(location.hash.slice(1));
  if(["time","excluded","about","index","biota","formations"].includes(h)){view=h}else if(h.startsWith("biota/")){view="biota";BT.focus(h.slice(6))}else if(h.startsWith("formation/")){view="formation";curF=h.slice(10)}else if(h==="tree-of-life"||h==="cladogram"){view="clado"}else{view="tree";cur=byId[h]?h:(cur||"vida");reveal(cur)}
  const full=view==="clado"||view==="biota";
  document.querySelector("main").classList.toggle("full",full);
  $(".encnav").style.display=full?"none":"";
  document.querySelectorAll("nav button").forEach(b=>b.classList.toggle("on",b.dataset.v===view||(view==="formation"&&b.dataset.v==="formations")));
  document.querySelector('.seg [data-v="tree"]').classList.toggle("on",!full);
  if(!full)renderSide();
  ({tree:()=>renderFicha(cur),clado:()=>CL.render(cur||"vida"),biota:renderBiota,formation:()=>renderFormation(curF),index:renderIndex,formations:renderFormations,time:renderTime,excluded:renderExcluded,about:renderAbout})[view]();
  $("#view").scrollTop=0;
}
// full genus entries are loaded on demand (site/g/<Name>.json); the index in data.json has what lists and maps need
const GLOAD={};
function loadGenus(id){const n=byId[id];if(!n||n.type!=="genus"||!n.ficha||n.full)return Promise.resolve(n);
  return GLOAD[id]=GLOAD[id]||fetch(`g/${encodeURIComponent(id)}.json`).then(r=>{if(!r.ok)throw r.status;return r.json()})
    .then(d=>{Object.assign(n,d,{full:true});return n}).catch(e=>{delete GLOAD[id];throw e})}
// taxa of a place, grouped by volume (Pterosauria, Dinosauria…) and then by parent clade; collapsible <details>.
// Small lists (≤ 12 taxa) open fully; larger ones open the volumes but close the clade groups (counts shown).
function taxaBlock(gs,tile,gridClass){const big=gs.length>12,vols={};
  for(const g of gs){const v=byId[g.vol]?byId[g.vol].name:(g.vol||"Other"),p=byId[g.parent];((vols[v]=vols[v]||{})[p?p.name:"—"]=(vols[v][p?p.name:"—"]||[])).push(g)}
  const inner=groups=>Object.entries(groups).sort((a,b)=>b[1].length-a[1].length||a[0].localeCompare(b[0])).map(([k,v])=>
    `<details class="tgrp"${big?"":" open"}><summary>${esc(k)} <span class="note">${v.length}${big?" · "+v.slice(0,3).map(g=>"<i>"+esc(g.name)+"</i>").join(", ")+(v.length>3?"…":""):""}</span></summary><div class="${gridClass}">${v.sort((a,b)=>a.name.localeCompare(b.name)).map(tile).join("")}</div></details>`).join("");
  const vs=Object.entries(vols);
  return vs.length===1?inner(vs[0][1]):vs.map(([v,groups])=>`<details class="tvol" open><summary>${esc(v)} <span class="note">${Object.values(groups).flat().length}</span></summary>${inner(groups)}</details>`).join("")}
function go(id){if(view==="time"&&byId[id]){cur=id;renderTime()}else if(view==="excluded"&&byId[id]){cur=id;renderExcluded();renderSide()}else location.hash=id}
function path(id){const p=[];let n=byId[id];while(n){p.unshift(n);n=byId[n.parent]}return p}
function reveal(id){path(id).forEach(n=>{if(n.type==="clade")open.add(n.id)})}
