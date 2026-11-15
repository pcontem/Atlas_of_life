/* Atlas of Life — Timeline view, synced with the selected entry. */
/* ---------- timeline view ---------- */
// a click selects (re-drawing the timeline) only after a short wait, so a double-click on a genus can open its entry instead
let tlTimer=null,TLV="sub";/* Timeline modes: sub = direct subdivisions, genera = every genus, div = diversity through time */
function tlClick(id){clearTimeout(tlTimer);tlTimer=setTimeout(()=>{cur=id;renderTime()},230)}
function tlOpen(id){clearTimeout(tlTimer);location.hash=id}
function renderTime(){
  const c0=cur||"vida",scope=byId[c0]&&byId[c0].type==="clade"?c0:(byId[c0]?byId[c0].parent:"vida");
  const sc=byId[scope],GN={};D.genera.forEach(g=>{if(g.fad!=null)GN[g.name]=g});
  // aggregate ranges per node
  const R={};(function agg(id){const n=byId[id];if(n.type!=="clade"){const g=GN[id];R[id]=g?{fad:g.fad,lad:g.lad,n:1}:null;return R[id]}
    let r=null;for(const k of children[id]){const x=agg(k);if(!x)continue;r=r?{fad:Math.max(r.fad,x.fad),lad:Math.min(r.lad,x.lad),n:r.n+x.n}:{...x}}R[id]=r;return r})(scope);
  const up=sc.parent&&byId[sc.parent]?`<button class="ixbtn" onclick="cur='${sc.parent}';renderTime()" title="Show the group that contains ${esc(sc.name)}">↑ Parent group: ${esc(byId[sc.parent].name)}</button>`:"";
  const MODES=[["sub","Subdivisions"],["genera","All genera"],["div","Diversity"]];
  const what={sub:`the stratigraphic ranges (PBDB) of the direct subdivisions of <b>${esc(sc.name)}</b>`,genera:`the range of every genus in <b>${esc(sc.name)}</b>, oldest first`,
    div:`how many genera of each direct subdivision of <b>${esc(sc.name)}</b> are known at each moment (bar thickness), with <b>ghost lineages</b> (dashed) — the time each subdivision must already have existed, because the group it belongs to is older than its own first fossil`}[TLV];
  const head=`<h2>${esc(sc.name)} through time</h2><div class="tlbar"><span class="seg tlseg">${MODES.map(([k,l])=>`<button class="${TLV===k?"on":""}" onclick="TLV='${k}';renderTime()">${l}</button>`).join("")}</span>${up}</div>
    <p class="note">Shows ${what}${byId[c0].type!=="clade"?`, with <i>${esc(byId[c0].name)}</i> highlighted`:""}. Follows the entry selected in the encyclopedia; click a group to go down into it.</p>`;
  if(!R[scope]){$("#view").innerHTML=`<div class="tlv">${head}<div class="card" style="margin-top:12px"><p style="margin:0">No genus of ${esc(sc.name)} has stratigraphic ranges in the atlas yet — so far only the Pterosauria entries carry ages.</p></div></div>`;return}
  // rows: only the direct subdivisions (sub-groups as their total range, genera individually), oldest first
  const rows=TLV==="genera"?allGenera(scope).filter(g=>R[g.name]).sort((p,q)=>q.fad-p.fad||q.lad-p.lad).map(g=>({id:g.name}))
    :children[scope].filter(k=>R[k]).sort((p,q)=>R[q].fad-R[p].fad||R[q].lad-R[p].lad).map(id=>({id}));
  // diversity: genera alive at each moment (range-through), per row
  const alive=(id,t)=>{const gs=byId[id].type==="genus"?[GN[id]]:allGenera(id).map(g=>GN[g.name]).filter(Boolean);let n=0;for(const g of gs)if(g.fad>=t&&g.lad<=t)n++;return n};
  const hlPath=new Set(path(c0).map(n=>n.id));
  const A0=R[scope].fad,B0=R[scope].lad,pad=(A0-B0)*0.04+1,A=A0+pad,B=Math.max(B0-pad,0);
  const W=1000,L=230,rowH=TLV==="div"?34:15,x=v=>L+(A-v)/(A-B)*(W-L-10),Hh=rows.length*rowH,HD=40;
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
  const pal=["#a35a2d","#2f6150","#55607a","#7a4d7a","#8a7a2a","#2a6a8a","#8a3a3a","#4d6a2a"];let ci=0;
  const N=160,ts_=d3.range(N+1).map(i=>A-(A-B)*i/N);let maxN=1;
  if(TLV==="div")rows.forEach(r=>{r.c=ts_.map(t=>alive(r.id,t));maxN=Math.max(maxN,...r.c)});
  rows.forEach((r,i)=>{const n=byId[r.id],isC=n.type==="clade",y=HD+6+i*rowH,rg=R[r.id],a=x(rg.fad),b=Math.max(x(rg.lad),a+3);
    const on=r.id===c0||hlPath.has(r.id)&&r.id!==scope,col=on?"#c0392b":isC?pal[ci++%pal.length]:"#8b8270";
    const lab=isC?`${esc(n.name.length>28?n.name.slice(0,27)+"…":n.name)} (${rg.n})`:esc(n.name),cy=y+rowH/2-2;
    let bar;
    if(TLV==="div"){const hh=rowH/2-3,pts=r.c.map((c,k)=>[x(ts_[k]),c?Math.max(1.2,hh*c/maxN):0]);
      const top=pts.map(p=>`${p[0].toFixed(1)},${(cy-p[1]).toFixed(1)}`),bot=pts.slice().reverse().map(p=>`${p[0].toFixed(1)},${(cy+p[1]).toFixed(1)}`);
      // ghost lineage: from the oldest record of the group shown (the subdivisions must have split by then) to this row's first record
      const g0=R[scope].fad,ghost=rg.fad<g0-0.01?`<line x1="${x(g0)}" x2="${a}" y1="${cy}" y2="${cy}" stroke="${col}" stroke-width="1.6" stroke-dasharray="4 3"/>`:"";
      const peak=Math.max(...r.c);
      bar=`${ghost}<polygon points="${top.join(" ")} ${bot.join(" ")}" fill="${col}" opacity=".8"/><text x="10" y="${cy+16}" font-size="9.5" fill="#7a7266">peak ${peak} genera</text>`}
    else bar=`<rect x="${a}" y="${y+(isC?0:1)}" width="${b-a}" height="${isC?11:9}" rx="2" fill="${col}" opacity="${isC&&!on?.7:1}"/>`;
    const ty=TLV==="div"?cy+2:y+9;
    s+=`<g class="bar" style="cursor:pointer" onclick="tlClick('${r.id}')"${isC?"":` ondblclick="tlOpen('${r.id}')"`}><title>${esc(n.name)}${isC?` — ${rg.n} genera · click to go into this group`:" · click: select · double-click: open its entry"}: ${rg.fad}–${rg.lad} Ma</title>${on?`<rect x="0" y="${y-2}" width="${W}" height="${rowH}" fill="#c0392b" opacity=".10"/>`:""}<text x="10" y="${ty}" font-size="${isC?11.5:11}" ${isC?'font-weight="600"':'font-style="italic"'} ${on?'fill="#b03a1e" data-on="1"':""}>${lab}</text>${bar}</g>`});
  s+="</svg>";
  $("#view").innerHTML=`<div class="tlv">${head}<p class="note">${TLV==="div"?`Thickness = number of genera known at that moment (range-through; thickest = ${maxN}). Dashed = ghost lineage. `:"Bold = sub-group (genus count in brackets); italic = genus. "}Click a row to select it; double-click a genus to open its entry.</p><div style="overflow:auto">${ovs}${s}</div></div>`;
  const sb=document.querySelector(".tlv [data-on]");if(sb)sb.scrollIntoView({block:"center"});
  renderSide()}
