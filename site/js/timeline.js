/* Atlas of Life — Timeline view, synced with the selected entry. */
/* ---------- timeline view ---------- */
// a click selects (re-drawing the timeline) only after a short wait, so a double-click on a genus can open its entry instead
let tlTimer=null,TLV="ranges",TLRES="genus";/* TLV: ranges | div (diversity). TLRES: "genus" or a depth 1..n of sub-groups below the selected group */
function tlClick(id){clearTimeout(tlTimer);tlTimer=setTimeout(()=>{cur=id;renderTime()},230)}
function tlOpen(id){clearTimeout(tlTimer);location.hash=id}
function renderTime(){
  const c0=cur||"vida",scope=byId[c0]&&byId[c0].type==="clade"?c0:(byId[c0]?byId[c0].parent:"vida");
  const sc=byId[scope],GN={};D.genera.forEach(g=>{if(g.fad!=null)GN[g.name]=g});
  // aggregate ranges per node
  const R={};(function agg(id){const n=byId[id];if(n.type!=="clade"){const g=GN[id];R[id]=g?{fad:g.fad,lad:g.lad,n:1}:null;return R[id]}
    let r=null;for(const k of children[id]){const x=agg(k);if(!x)continue;r=r?{fad:Math.max(r.fad,x.fad),lad:Math.min(r.lad,x.lad),n:r.n+x.n}:{...x}}R[id]=r;return r})(scope);
  const up=sc.parent&&byId[sc.parent]?`<button class="ixbtn" onclick="cur='${sc.parent}';renderTime()" title="Show the group that contains ${esc(sc.name)}">↑ Parent group: ${esc(byId[sc.parent].name)}</button>`:"";
  // resolution = a taxonomic rank (from PBDB) present among the dated groups below the selected one
  const RANKS=["genus","subfamily","family","superfamily","infraorder","suborder","order","subclass","class"];
  const below=new Set();(function d(k){for(const c of children[k]||[])if(byId[c].type==="clade"&&R[c]){if(byId[c].trank)below.add(byId[c].trank);d(c)}})(scope);
  const resOpts=RANKS.filter(r=>r==="genus"||below.has(r)).map(r=>[r,r==="genus"?"Genus":r[0].toUpperCase()+r.slice(1)]);
  if(!resOpts.some(o=>o[0]===TLRES))TLRES="genus";
  const what=TLV==="div"?`how many ${TLRES==="genus"?"genera":TLRES==="family"?"families":TLRES+" taxa"} of <b>${esc(sc.name)}</b> are known at each moment (thickness), with <b>ghost lineages</b> (dashed) — stretches between its first and last record where none of its genera is known, although the group must have existed`
    :TLRES==="genus"?`the range of every genus in <b>${esc(sc.name)}</b>, oldest first`:`the range of every ${TLRES} in <b>${esc(sc.name)}</b> (genera outside any ${TLRES} are shown on their own)`;
  const head=`<h2>${esc(sc.name)} through time</h2><div class="tlbar"><span class="seg tlseg">${[["ranges","Ranges"],["div","Diversity"]].map(([k,l])=>`<button class="${TLV===k?"on":""}" onclick="TLV='${k}';renderTime()">${l}</button>`).join("")}</span>${true?`<label class="note">Resolution <select id="tlres">${resOpts.map(([k,l])=>`<option value="${k}"${String(TLRES)===String(k)?" selected":""}>${l}</option>`).join("")}</select></label>`:""}${up}</div>
    <p class="note">Shows ${what}${byId[c0].type!=="clade"?`, with <i>${esc(byId[c0].name)}</i> highlighted`:""}. Follows the entry selected in the encyclopedia; click a group to go down into it.</p>`;
  if(!R[scope]){$("#view").innerHTML=`<div class="tlv">${head}<div class="card" style="margin-top:12px"><p style="margin:0">No genus of ${esc(sc.name)} has stratigraphic ranges in the atlas yet — so far only the Pterosauria entries carry ages.</p></div></div>`;return}
  // rows: only the direct subdivisions (sub-groups as their total range, genera individually), oldest first
  // rows at the chosen rank: each genus is replaced by its nearest ancestor of that rank below the selected group
  const unitOf=g=>{if(TLRES==="genus")return g;const p=path(g);const k=p.findIndex(n=>n.id===scope);for(let i=p.length-2;i>k;i--)if(p[i].trank===TLRES)return p[i].id;return g};
  const pick=[...new Set(allGenera(scope).filter(g=>R[g.name]).map(g=>unitOf(g.name)))];
  const units=pick.slice();// the taxa counted in Diversity at this resolution
  const rows=TLV==="div"?[{id:scope}]:pick.sort((p,q)=>R[q].fad-R[p].fad||R[q].lad-R[p].lad).map(id=>({id}));
  // diversity: genera alive at each moment (range-through), per row
  const alive=(id,t)=>{const gs=byId[id].type==="genus"?[GN[id]]:allGenera(id).map(g=>GN[g.name]).filter(Boolean);let n=0;for(const g of gs)if(g.fad>=t&&g.lad<=t)n++;return n};
  const hlPath=new Set(path(c0).map(n=>n.id));
  const A0=R[scope].fad,B0=R[scope].lad,pad=(A0-B0)*0.04+1,A=A0+pad,B=Math.max(B0-pad,0);
  const W=1000,L=230,rowH=TLV==="div"?190:15,x=v=>L+(A-v)/(A-B)*(W-L-10),Hh=rows.length*rowH,HD=40;
  // overview: the whole history of the Earth (Hadean to today) with this window marked
  // logarithmic scale on (age + OFF): recent, finely divided time gets more room; the offset keeps the
  // Cenozoic from swamping the strip (OFF=50 Myr: Cenozoic ≈ 19 %, Mesozoic ≈ 21 %, Precambrian ≈ 45 %)
  const AGE=4567,OFF=50,LG=v=>Math.log10(v+OFF),xo=v=>L+(1-(LG(v)-LG(0))/(LG(AGE)-LG(0)))*(W-L-10),ov=tsRows(AGE,0,xo,0,13,0.95,["eon","era","period"]);
  const otk=[4000,2000,1000,500,250,100,50,0].map(v=>`<line x1="${xo(v)}" x2="${xo(v)}" y1="39" y2="43" stroke="#7a7266"/><text x="${xo(v)}" y="52" font-size="9" text-anchor="middle" fill="#7a7266">${v}</text>`).join("");
  const ovs=`<svg viewBox="0 0 ${W} 66" style="width:100%;min-width:760px;margin-bottom:6px">${ov.svg}<text x="${L-8}" y="11" font-size="10" text-anchor="end" fill="#7a7266">Earth history</text><text x="${L-8}" y="24" font-size="10" text-anchor="end" fill="#7a7266">log scale, Ma</text>${otk}
    <rect x="${xo(A)-1}" y="-1" width="${Math.max(3,xo(B)-xo(A)+2)}" height="42" fill="none" stroke="#c0392b" stroke-width="2"/><text x="${Math.min(W-4,(xo(A)+xo(B))/2)}" y="63" font-size="10" text-anchor="${(xo(A)+xo(B))/2>W-90?"end":"middle"}" fill="#c0392b">this view: ${fmtMa(A)}–${fmtMa(B)}</text></svg>`;
  let s=`<svg viewBox="0 0 ${W} ${HD+28+Hh}" style="width:100%;min-width:760px">`;
  // ICS units for this window (era+period, period+epoch or epoch+age depending on its length), light columns behind the bars
  const ts=tsRows(A,B,x,0,20);s+=ts.svg;
  (ts.fine||[]).forEach((t,i)=>{const a=Math.min(t.base,A),b=Math.max(t.top,B);s+=`<rect x="${x(a)}" y="${HD}" width="${x(b)-x(a)}" height="${Hh+8}" fill="${t.color}" opacity="${i%2?.10:.18}"/>`});
  s+=tsTicks(A,B,x,HD+24+Hh,HD,HD+10+Hh);
  const pal=["#e4572e","#17a398","#f2b134","#3a86ff","#8f5bd6","#e83f6f","#4caf50","#ff8c42","#00a6d6","#c2185b"];let ci=0;
  const subOf=id=>{const p=path(id);const k=p.findIndex(n=>n.id===scope);return p[k+1]&&p[k+1].type==="clade"?p[k+1].id:null};
  const subs=children[scope].filter(k=>byId[k].type==="clade"&&R[k]).sort((p,q)=>R[q].fad-R[p].fad),subCol={};subs.forEach((k,i)=>subCol[k]=pal[i%pal.length]);
  const N=220,ts_=d3.range(N+1).map(i=>A-(A-B)*i/N);let maxN=1;
  // a unit (genus or sub-group) is alive at t when its range covers t
  if(TLV==="div")rows.forEach(r=>{r.c=ts_.map(t=>TLRES==="genus"?alive(r.id,t):units.filter(u=>R[u].fad>=t&&R[u].lad<=t).length);maxN=Math.max(maxN,...r.c)});
  const unitName=TLRES==="genus"?"genera":`${TLRES==="family"?"families":TLRES+" taxa"} (plus genera outside any ${TLRES})`;
  const legend=TLV==="ranges"&&subs.length?`<p class="note">${subs.map(k=>`<span style="white-space:nowrap"><span style="display:inline-block;width:10px;height:10px;border-radius:2px;background:${subCol[k]}"></span> <a style="cursor:pointer" onclick="cur='${k}';renderTime()">${esc(byId[k].name)}</a></span>`).join(" &nbsp; ")} &nbsp; <span style="white-space:nowrap"><span style="display:inline-block;width:10px;height:10px;border-radius:2px;background:#8b8270"></span> placed directly in ${esc(sc.name)}</span></p>`:"";
  rows.forEach((r,i)=>{const n=byId[r.id],isC=n.type==="clade",y=HD+6+i*rowH,rg=R[r.id],a=x(rg.fad),b=Math.max(x(rg.lad),a+3);
    const on=TLV!=="div"&&(r.id===c0||hlPath.has(r.id)&&r.id!==scope),col=on?"#c0392b":TLV==="div"?"#3a86ff":(subCol[subOf(r.id)]||"#8b8270");
    const lab=isC?`${esc(n.name.length>28?n.name.slice(0,27)+"…":n.name)} (${rg.n})`:esc(n.name),cy=y+rowH/2-2;
    let bar;
    if(TLV==="div"){const hh=rowH/2-8,mx=Math.max(...r.c),pts=r.c.map((c,k)=>[x(ts_[k]),c?Math.max(1,hh*c/mx):0]);
      const top=pts.map(p=>`${p[0].toFixed(1)},${(cy-p[1]).toFixed(1)}`),bot=pts.slice().reverse().map(p=>`${p[0].toFixed(1)},${(cy+p[1]).toFixed(1)}`);
      const st=[1,2,5,10,20,50,100].find(v=>mx/v<=5)||100;let guides="";
      for(let v=st;v<=mx;v+=st){const d=hh*v/mx;guides+=`<line x1="${L}" x2="${W-10}" y1="${cy-d}" y2="${cy-d}" stroke="#000" opacity=".08"/><line x1="${L}" x2="${W-10}" y1="${cy+d}" y2="${cy+d}" stroke="#000" opacity=".08"/><text x="${L-6}" y="${cy-d+3}" font-size="9.5" text-anchor="end" fill="#7a7266">${v}</text>`}
      // ghost lineage inside the group only: between its first and last record the group must have existed, so any stretch
      // with no genus on record is drawn dashed (no comparison with sister groups, whose relationships are unresolved here)
      let ghost="",g0=null;r.c.forEach((c,k)=>{const t=ts_[k];const inside=t<=rg.fad&&t>=rg.lad;
        if(inside&&c===0&&g0===null)g0=k;if((!inside||c>0||k===r.c.length-1)&&g0!==null){const k1=inside&&c===0?k:k-1;
          ghost+=`<line x1="${x(ts_[g0])}" x2="${x(ts_[k1])}" y1="${cy}" y2="${cy}" stroke="${col}" stroke-width="2" stroke-dasharray="5 4"/>`;g0=null}});
      const ki=r.c.indexOf(mx);
      bar=`${guides}${ghost}<polygon points="${top.join(" ")} ${bot.join(" ")}" fill="${col}" opacity=".8"/><text x="10" y="${cy+18}" font-size="10.5" fill="#7a7266">peak ${mx} ${TLRES==="genus"?"genera":TLRES==="family"?"families":TLRES+" taxa"}</text><text x="10" y="${cy+32}" font-size="10.5" fill="#7a7266">around ${fmtMa(ts_[ki])}</text><text x="${L-6}" y="${cy+3}" font-size="9.5" text-anchor="end" fill="#7a7266">0</text>`}
    else bar=`<rect x="${a}" y="${y+(isC?0:1)}" width="${b-a}" height="${isC?11:9}" rx="2" fill="${col}" opacity="${isC&&!on?.85:1}"/>`;
    const ty=TLV==="div"?cy+4:y+9;
    s+=`<g class="bar" style="cursor:pointer" onclick="tlClick('${r.id}')"${isC?"":` ondblclick="tlOpen('${r.id}')"`}><title>${esc(n.name)}${isC?` — ${rg.n} genera · click to go into this group`:" · click: select · double-click: open its entry"}: ${rg.fad}–${rg.lad} Ma</title>${on?`<rect x="0" y="${y-2}" width="${W}" height="${rowH}" fill="#c0392b" opacity=".10"/>`:""}<text x="10" y="${ty}" font-size="${isC?11.5:11}" ${isC?'font-weight="600"':'font-style="italic"'} ${on?'fill="#b03a1e" data-on="1"':""}>${lab}</text>${bar}</g>`});
  s+="</svg>";
  $("#view").innerHTML=`<div class="tlv">${head}<p class="note">${TLV==="div"?`Thickness = number of ${unitName} of ${esc(sc.name)} known at that moment (each counts from its first to its last record); scale on the left. Dashed = ghost lineage (gap in the group's own record).`:"Bars are coloured by the direct subdivision they belong to. Bold = sub-group (genus count in brackets); italic = genus. Click a row to select it; double-click a genus to open its entry."}</p>${legend}<div style="overflow:auto">${ovs}${s}</div></div>`;
  const rs=$("#tlres");if(rs)rs.onchange=e=>{TLRES=e.target.value;renderTime()};
  const sb=document.querySelector(".tlv [data-on]");if(sb)sb.scrollIntoView({block:"center"});
  renderSide()}
