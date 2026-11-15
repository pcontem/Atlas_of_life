/* Atlas of Life — start-up: load data, then init() (core.js). Must be the last script. */
Promise.all([fetch("data.json").then(r=>r.json()),fetch("life.json").then(r=>r.json())]).then(([d,l])=>{D=d;LIFE=l;init()}).catch(e=>{$("#view").innerHTML='<div class="empty">Could not load the data file.</div>'});
