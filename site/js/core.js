/* Atlas of Life — Shared state, helpers, routing between views. */
const ERAS=[["Triassic",251.9,201.4,"#8e5f8f"],["Jurassic",201.4,145,"#3d7f9b"],["Cretaceous",145,66,"#6f9a45"]];
const EPOCHS=[["Early",251.9,247.2],["Middle",247.2,237],["Late",237,201.4],["Early",201.4,174.7],["Middle",174.7,161.5],["Late",161.5,145],["Early",145,100.5],["Late",100.5,66]];
let D,LIFE,byId={},byName={},children={},open=new Set(["vida"]),cur=null,view="tree";
const $=s=>document.querySelector(s);
const esc=s=>String(s??"").replace(/[&<>"]/g,c=>({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;"}[c]));
const fmtMa=v=>v==null?"?":(v>=10?v.toFixed(1).replace(/\.0$/,""):v.toFixed(2))+" Ma";
const era=ma=>{for(const e of ERAS)if(ma<=e[1]&&ma>e[2])return e;return ERAS[2]};
const imgKey=(g,k)=>"img/"+g.replace(/[^A-Za-z]/g,"")+"_"+k+".webp";
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
  document.querySelectorAll("nav button").forEach(b=>b.onclick=()=>{const v=b.dataset.v;location.hash=v==="tree"?(cur||"vida"):v==="clado"?"cladogram":v});
  addEventListener("hashchange",route);route();
}
function route(){
  const h=decodeURIComponent(location.hash.slice(1));
  if(["time","excluded","about","index"].includes(h)){view=h}else if(h==="cladogram"){view="clado"}else{view="tree";cur=byId[h]?h:(cur||"vida");reveal(cur)}
  document.querySelector("main").classList.toggle("full",view==="clado");
  $(".encnav").style.display=view==="clado"?"none":"";
  document.querySelectorAll("nav button").forEach(b=>b.classList.toggle("on",b.dataset.v===view));
  document.querySelector('.seg [data-v="tree"]').classList.toggle("on",view!=="clado");
  if(view!=="clado")renderSide();
  ({tree:()=>renderFicha(cur),clado:()=>CL.render(cur||"vida"),index:renderIndex,time:renderTime,excluded:renderExcluded,about:renderAbout})[view]();
  $("#view").scrollTop=0;
}
function go(id){if(view==="time"&&byId[id]){cur=id;renderTime()}else location.hash=id}
function path(id){const p=[];let n=byId[id];while(n){p.unshift(n);n=byId[n.parent]}return p}
function reveal(id){path(id).forEach(n=>{if(n.type==="clade")open.add(n.id)})}
