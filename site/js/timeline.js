/* Atlas of Life — Timeline view, synced with the selected entry. */
/* ---------- timeline view ---------- */
let TLMODE="condensed";
function renderTime(){
  const c0=cur||"vida",scope=byId[c0]&&byId[c0].type==="clade"?c0:(byId[c0]?byId[c0].parent:"vida");
  const sc=byId[scope],GN={};D.genera.forEach(g=>{if(g.fad!=null)GN[g.name]=g});
  // aggregate ranges per node
  const R={};(function agg(id){const n=byId[id];if(n.type!=="clade"){const g=GN[id];R[id]=g?{fad:g.fad,lad:g.lad,n:1}:null;return R[id]}
    let r=null;for(const k of children[id]){const x=agg(k);if(!x)continue;r=r?{fad:Math.max(r.fad,x.fad),lad:Math.min(r.lad,x.lad),n:r.n+x.n}:{...x}}R[id]=r;return r})(scope);
  const up=sc.parent&&byId[sc.parent]?`<a style="cursor:pointer" onclick="cur='${sc.parent}';renderTime()">widen to ${esc(byId[sc.parent].name)}</a>`:"";
  const tog=`<span class="seg tlseg">${[["condensed","Condensed (3 levels)"],["all","All genera"]].map(([k,l])=>`<button class="${TLMODE===k?"on":""}" onclick="TLMODE='${k}';renderTime()">${l}</button>`).join("")}</span>`;
  const head=`<h2>${esc(sc.name)} through time</h2><p class="note">Stratigraphic ranges (PBDB) within <b>${esc(sc.name)}</b>${byId[c0].type!=="clade"?`, with <i>${esc(byId[c0].name)}</i> highlighted`:""}. This view follows the entry selected in the encyclopedia. ${up?"· "+up:""}</p>${tog}`;
  if(!R[scope]){$("#view").innerHTML=`<div class="tlv">${head}<div class="card" style="margin-top:12px"><p style="margin:0">No genus of ${esc(sc.name)} has stratigraphic ranges in the atlas yet — so far only the Pterosauria entries carry ages.</p></div></div>`;return}
  // rows
  const rows=[],MAXD=3,ord=ks=>ks.filter(k=>R[k]).sort((p,q)=>R[q].fad-R[p].fad||R[q].lad-R[p].lad);
  if(TLMODE==="all"){Object.keys(GN).filter(g=>path(g).some(n=>n.id===scope)).sort((p,q)=>GN[q].fad-GN[p].fad||GN[q].lad-GN[p].lad).forEach(g=>rows.push({id:g,d:0}))}
  else (function walk(id,d){const ks=ord(children[id]),cs=ks.filter(k=>byId[k].type==="clade"),gs=ks.filter(k=>byId[k].type!=="clade");
    if(!cs.length){if(id===scope)gs.forEach(k=>rows.push({id:k,d}));return}
    cs.forEach(k=>{rows.push({id:k,d});if(d<MAXD)walk(k,d+1)});
    if(gs.length===1)rows.push({id:gs[0],d});
    else if(gs.length){const r={fad:Math.max(...gs.map(k=>R[k].fad)),lad:Math.min(...gs.map(k=>R[k].lad)),n:gs.length};rows.push({id:id,d,grp:gs,rg:r})}})(scope,1);
  const hlPath=new Set(path(c0).map(n=>n.id));
  const A0=R[scope].fad,B0=R[scope].lad,pad=(A0-B0)*0.04+1,A=A0+pad,B=Math.max(B0-pad,0);
  const W=1000,L=230,rowH=15,x=v=>L+(A-v)/(A-B)*(W-L-10),Hh=rows.length*rowH,HD=40;
  // overview: the whole history of the Earth (Hadean to today) with this window marked
  const AGE=4567,xo=v=>L+(AGE-v)/AGE*(W-L-10),ov=tsRows(AGE,0,xo,0,14);
  const ovs=`<svg viewBox="0 0 ${W} 44" style="width:100%;min-width:760px;margin-bottom:6px">${ov.svg}<text x="${L-8}" y="11" font-size="10" text-anchor="end" fill="#7a7266">Earth history</text><text x="${L-8}" y="25" font-size="10" text-anchor="end" fill="#7a7266">4567 Ma → today</text>
    <rect x="${xo(A)-1}" y="-1" width="${Math.max(3,xo(B)-xo(A)+2)}" height="30" fill="none" stroke="#c0392b" stroke-width="2"/><text x="${Math.min(W-4,(xo(A)+xo(B))/2)}" y="41" font-size="10" text-anchor="${(xo(A)+xo(B))/2>W-90?"end":"middle"}" fill="#c0392b">this view: ${fmtMa(A)}–${fmtMa(B)}</text></svg>`;
  let s=`<svg viewBox="0 0 ${W} ${HD+28+Hh}" style="width:100%;min-width:760px">`;
  // ICS units for this window (era+period, period+epoch or epoch+age depending on its length), light columns behind the bars
  const ts=tsRows(A,B,x,0,20);s+=ts.svg;
  (ts.fine||[]).forEach((t,i)=>{const a=Math.min(t.base,A),b=Math.max(t.top,B);s+=`<rect x="${x(a)}" y="${HD}" width="${x(b)-x(a)}" height="${Hh+8}" fill="${t.color}" opacity="${i%2?.10:.18}"/>`});
  s+=tsTicks(A,B,x,HD+24+Hh,HD,HD+10+Hh);
  const kids=children[scope].filter(k=>byId[k].type==="clade"&&R[k]),pal=["#a35a2d","#2f6150","#55607a","#7a4d7a","#8a7a2a","#2a6a8a","#8a3a3a","#4d6a2a"];
  const colOf=id=>{const p=path(id);const i=kids.findIndex(k=>p.some(n=>n.id===k));return i<0?"#9a9184":pal[i%pal.length]};
  const shown=new Set(rows.filter(r=>!r.grp).map(r=>r.id));
  const deepest=rows.filter(r=>!r.grp&&hlPath.has(r.id)).map(r=>r.id).pop();
  rows.forEach((r,i)=>{const n=byId[r.id],isC=r.grp?true:n.type==="clade",y=HD+6+i*rowH,rg=r.rg||R[r.id],a=x(rg.fad),b=Math.max(x(rg.lad),a+3);
    const on=r.grp?r.grp.includes(c0):(r.id===c0||(byId[c0].type!=="clade"&&!shown.has(c0)&&!rows.some(q=>q.grp&&q.grp.includes(c0))&&r.id===deepest));
    const lab=r.grp?`${rg.n} other genera`:isC?`${esc(n.name.length>26?n.name.slice(0,25)+"…":n.name)} (${rg.n})`:esc(n.name),ix=(r.d?r.d-1:0)*12;
    const tip=r.grp?r.grp.join(", "):n.name+(isC?` — ${rg.n} genera`:"");
    s+=`<g class="bar" style="cursor:pointer" onclick="${r.grp?`cur='${r.grp.includes(c0)?c0:r.grp[0]}'`:`cur='${r.id}'`};renderTime()"><title>${esc(tip)}: ${rg.fad}–${rg.lad} Ma</title>${on?`<rect x="0" y="${y-2}" width="${W}" height="${rowH}" fill="#c0392b" opacity=".12"/>`:""}<text x="${10+ix}" y="${y+9}" font-size="${isC?11:10.5}" ${r.grp?'font-style="italic" fill="#7a7266"':isC?'font-weight="600"':'font-style="italic"'} ${on?'fill="#b03a1e" data-on="1"':""}>${lab}</text><rect x="${a}" y="${y+(isC?0:1)}" width="${b-a}" height="${isC?11:9}" rx="2" fill="${on?"#c0392b":r.grp?colOf(r.grp[0]):colOf(r.id)}" opacity="${isC?.55:1}"/></g>`});
  s+="</svg>";
  const leg=kids.map(k=>`<span style="white-space:nowrap"><span style="display:inline-block;width:10px;height:10px;border-radius:2px;background:${pal[kids.indexOf(k)%pal.length]}"></span> <a style="cursor:pointer" onclick="cur='${k}';renderTime()">${esc(byId[k].name)}</a></span>`).join(" &nbsp; ");
  $("#view").innerHTML=`<div class="tlv">${head}<p class="note">${leg}${leg?' &nbsp; <span style="white-space:nowrap"><span style="display:inline-block;width:10px;height:10px;border-radius:2px;background:#9a9184"></span> other</span> · ':""}Pale bars = whole range of a group (genus count in brackets). Click a row to select it; switch to <b>Entry</b> to read it.</p><div style="overflow:auto">${ovs}${s}</div></div>`;
  const sb=document.querySelector(".tlv [data-on]");if(sb)sb.scrollIntoView({block:"center"});
  renderSide()}
