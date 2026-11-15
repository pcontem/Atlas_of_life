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
    div:`how many genera of <b>${esc(sc.name)}</b> are known at each moment (thickness), with its <b>ghost lineage</b> (dashed) — the time it must already have existed because a sister group is securely recorded before its own first fossil`}[TLV];
  const head=`<h2>${esc(sc.name)} through time</h2><div class="tlbar"><span class="seg tlseg">${MODES.map(([k,l])=>`<button class="${TLV===k?"on":""}" onclick="TLV='${k}';renderTime()">${l}</button>`).join("")}</span>${up}</div>
    <p class="note">Shows ${what}${byId[c0].type!=="clade"?`, with <i>${esc(byId[c0].name)}</i> highlighted`:""}. Follows the entry selected in the encyclopedia; click a group to go down into it.</p>`;
  if(!R[scope]){$("#view").innerHTML=`<div class="tlv">${head}<div class="card" style="margin-top:12px"><p style="margin:0">No genus of ${esc(sc.name)} has stratigraphic ranges in the atlas yet — so far only the Pterosauria entries carry ages.</p></div></div>`;return}
  // rows: only the direct subdivisions (sub-groups as their total range, genera individually), oldest first
  const rows=TLV==="div"?[{id:scope}]:TLV==="genera"?allGenera(scope).filter(g=>R[g.name]).sort((p,q)=>q.fad-p.fad||q.lad-p.lad).map(g=>({id:g.name}))
    :children[scope].filter(k=>R[k]).sort((p,q)=>R[q].fad-R[p].fad||R[q].lad-R[p].lad).map(id=>({id}));
  // diversity: genera alive at each moment (range-through), per row
  const alive=(id,t)=>{const gs=byId[id].type==="genus"?[GN[id]]:allGenera(id).map(g=>GN[g.name]).filter(Boolean);let n=0;for(const g of gs)if(g.fad>=t&&g.lad<=t)n++;return n};
  const hlPath=new Set(path(c0).map(n=>n.id));
  // ghost lineage reference: the SISTER groups (the other subdivisions of the parent), each counted from the
  // youngest possible age of its oldest record (fad_firm), so imprecisely dated occurrences cannot stretch it
  const SIB=TLV==="div"&&sc.parent&&byId[sc.parent]?children[sc.parent].filter(k=>k!==scope).flatMap(k=>byId[k].type==="genus"?[GN[k]]:allGenera(k).map(g=>GN[g.name])).filter(Boolean):[];
  const REF=SIB.length?SIB.reduce((a,g)=>(g.fad_firm??g.fad)>(a.fad_firm??a.fad)?g:a):null,PF=REF?(REF.fad_firm??REF.fad):null;
  const A0=Math.max(R[scope].fad,PF||0),B0=R[scope].lad,pad=(A0-B0)*0.04+1,A=A0+pad,B=Math.max(B0-pad,0);
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
  const pal=["#a35a2d","#2f6150","#55607a","#7a4d7a","#8a7a2a","#2a6a8a","#8a3a3a","#4d6a2a","#b0702a","#3f7f7f"];let ci=0;
  const subOf=id=>{const p=path(id);const k=p.findIndex(n=>n.id===scope);return p[k+1]&&p[k+1].id!==id?p[k+1].id:null};
  const subs=children[scope].filter(k=>byId[k].type==="clade"&&R[k]).sort((p,q)=>R[q].fad-R[p].fad),subCol={};subs.forEach((k,i)=>subCol[k]=pal[i%pal.length]);
  const N=220,ts_=d3.range(N+1).map(i=>A-(A-B)*i/N);let maxN=1;
  if(TLV==="div")rows.forEach(r=>{r.c=ts_.map(t=>alive(r.id,t));maxN=Math.max(maxN,...r.c)});
  const legend=TLV==="genera"&&subs.length?`<p class="note">${subs.map(k=>`<span style="white-space:nowrap"><span style="display:inline-block;width:10px;height:10px;border-radius:2px;background:${subCol[k]}"></span> <a style="cursor:pointer" onclick="cur='${k}';renderTime()">${esc(byId[k].name)}</a></span>`).join(" &nbsp; ")} &nbsp; <span style="white-space:nowrap"><span style="display:inline-block;width:10px;height:10px;border-radius:2px;background:#8b8270"></span> placed directly in ${esc(sc.name)}</span></p>`:"";
  rows.forEach((r,i)=>{const n=byId[r.id],isC=n.type==="clade",y=HD+6+i*rowH,rg=R[r.id],a=x(rg.fad),b=Math.max(x(rg.lad),a+3);
    const on=TLV!=="div"&&(r.id===c0||hlPath.has(r.id)&&r.id!==scope),col=on?"#c0392b":TLV==="genera"?(subCol[subOf(r.id)]||"#8b8270"):TLV==="div"?"#55607a":isC?pal[ci++%pal.length]:"#8b8270";
    const lab=isC?`${esc(n.name.length>28?n.name.slice(0,27)+"…":n.name)} (${rg.n})`:esc(n.name),cy=y+rowH/2-2;
    let bar;
    if(TLV==="div"){const hh=rowH/2-8,mx=Math.max(...r.c),pts=r.c.map((c,k)=>[x(ts_[k]),c?Math.max(1,hh*c/mx):0]);
      const top=pts.map(p=>`${p[0].toFixed(1)},${(cy-p[1]).toFixed(1)}`),bot=pts.slice().reverse().map(p=>`${p[0].toFixed(1)},${(cy+p[1]).toFixed(1)}`);
      const st=[1,2,5,10,20,50,100].find(v=>mx/v<=5)||100;let guides="";
      for(let v=st;v<=mx;v+=st){const d=hh*v/mx;guides+=`<line x1="${L}" x2="${W-10}" y1="${cy-d}" y2="${cy-d}" stroke="#000" opacity=".08"/><line x1="${L}" x2="${W-10}" y1="${cy+d}" y2="${cy+d}" stroke="#000" opacity=".08"/><text x="${L-6}" y="${cy-d+3}" font-size="9.5" text-anchor="end" fill="#7a7266">${v}</text>`}
      // ghost lineage: from the oldest record of the parent group (the split from its sister groups happened by then) to this group's first record
      const pf=PF;
      const ghost=pf&&pf>rg.fad+0.01?`<line x1="${x(pf)}" x2="${a}" y1="${cy}" y2="${cy}" stroke="${col}" stroke-width="2" stroke-dasharray="5 4"/><text x="${x(pf)+3}" y="${cy-6}" font-size="9.5" fill="#7a7266">ghost lineage: sister group already present by ${fmtMa(pf)} (${esc(REF.name)})</text>`:"";
      const ki=r.c.indexOf(mx);
      bar=`${guides}${ghost}<polygon points="${top.join(" ")} ${bot.join(" ")}" fill="${col}" opacity=".8"/><text x="10" y="${cy+18}" font-size="10.5" fill="#7a7266">peak ${mx} genera</text><text x="10" y="${cy+32}" font-size="10.5" fill="#7a7266">around ${fmtMa(ts_[ki])}</text><text x="${L-6}" y="${cy+3}" font-size="9.5" text-anchor="end" fill="#7a7266">0</text>`}
    else bar=`<rect x="${a}" y="${y+(isC?0:1)}" width="${b-a}" height="${isC?11:9}" rx="2" fill="${col}" opacity="${isC&&!on?.7:1}"/>`;
    const ty=TLV==="div"?cy+4:y+9;
    s+=`<g class="bar" style="cursor:pointer" onclick="tlClick('${r.id}')"${isC?"":` ondblclick="tlOpen('${r.id}')"`}><title>${esc(n.name)}${isC?` — ${rg.n} genera · click to go into this group`:" · click: select · double-click: open its entry"}: ${rg.fad}–${rg.lad} Ma</title>${on?`<rect x="0" y="${y-2}" width="${W}" height="${rowH}" fill="#c0392b" opacity=".10"/>`:""}<text x="10" y="${ty}" font-size="${isC?11.5:11}" ${isC?'font-weight="600"':'font-style="italic"'} ${on?'fill="#b03a1e" data-on="1"':""}>${lab}</text>${bar}</g>`});
  s+="</svg>";
  $("#view").innerHTML=`<div class="tlv">${head}<p class="note">${TLV==="div"?`Thickness = number of genera of ${esc(sc.name)} known at that moment (a genus counts from its first to its last record); scale on the left. Dashed = ghost lineage.`:TLV==="genera"?"Each bar is a genus, coloured by the subdivision it belongs to. Click a row to select it; double-click a genus to open its entry.":"Bold = sub-group (genus count in brackets); italic = genus. Click a row to select it; double-click a genus to open its entry."}</p>${legend}<div style="overflow:auto">${ovs}${s}</div></div>`;
  const sb=document.querySelector(".tlv [data-on]");if(sb)sb.scrollIntoView({block:"center"});
  renderSide()}
