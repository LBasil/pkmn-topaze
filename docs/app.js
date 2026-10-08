const COL={Normal:'#9a9a8a',Fighting:'#b8402e',Flying:'#7f8fe0',Poison:'#8e47a8',Ground:'#c9a64a',Rock:'#a08d3a',Bug:'#8aa31c',Ghost:'#654d8e',Steel:'#8e8ea8',Fire:'#e8642a',Water:'#3f7fe0',Grass:'#4cae43',Electric:'#e0b800',Psychic:'#e0457a',Ice:'#4cc2c2',Dragon:'#5a3de0',Dark:'#5a463a',Fairy:'#e87fb4'};
const tb=t=>`<span class="t" style="background:${COL[t]||'#777'}">${t}</span>`;
const esc=s=>String(s).replace(/[&<>]/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;'}[c]));
function nav(on){const p=[['index','Home'],['guide','Player guide'],['pokedex','Pokédex'],['movedex','Movedex'],['types','Types'],['champions','Gym Champions'],['wild','Wild Encounters']];
document.body.insertAdjacentHTML('afterbegin','<header><nav><b>Pokémon Topaze</b>'+p.map(([h,l])=>`<a href="${h}.html"${h===on?' class="on"':''}>${l}</a>`).join('')+'</nav></header>')}
// table générique : cols=[{h,get,html?,num?}]
function table(el,rows,cols,opts={}){
 let sort=null,dir=1,q='',f='';const box=document.getElementById(el);
 box.innerHTML=`<div class="tools"><input type="search" placeholder="Search…" id="${el}q">${opts.filter?`<select id="${el}f"><option value="">${opts.filter.label}</option>${opts.filter.values.map(v=>`<option>${v}</option>`).join('')}</select>`:''}<span class="mut" id="${el}c"></span></div><div class="wrap"><table><thead><tr>${cols.map((c,i)=>`<th data-i="${i}">${c.h}</th>`).join('')}</tr></thead><tbody></tbody></table></div>`;
 const tbody=box.querySelector('tbody');
 function draw(){let r=rows.filter(x=>(!q||JSON.stringify(x).toLowerCase().includes(q))&&(!f||opts.filter.test(x,f)));
  if(sort!==null){const g=cols[sort].get;r=[...r].sort((a,b)=>{const A=g(a),B=g(b);return (A>B?1:A<B?-1:0)*dir})}
  document.getElementById(el+'c').textContent=r.length+' / '+rows.length;
  tbody.innerHTML=r.slice(0,opts.max||800).map(x=>'<tr>'+cols.map(c=>`<td${c.num?' class="n"':''}>${c.html?c.html(x):esc(c.get(x))}</td>`).join('')+'</tr>').join('')}
 box.querySelector('input').oninput=e=>{q=e.target.value.toLowerCase();draw()};
 const s=box.querySelector('select');if(s)s.onchange=e=>{f=e.target.value;draw()};
 box.querySelectorAll('th').forEach(th=>th.onclick=()=>{const i=+th.dataset.i;dir=sort===i?-dir:1;sort=i;draw()});
 draw()}
