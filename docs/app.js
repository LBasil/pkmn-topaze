// Pokémon Topaze — code partagé (FR/EN, recherche globale, tableaux)
let lang='en';try{lang=localStorage.getItem('lang')||((navigator.language||'').startsWith('fr')?'fr':'en')}catch(e){}
document.documentElement.lang=lang;
(function(){try{const th=localStorage.getItem('theme');if(th)document.documentElement.dataset.theme=th}catch(e){}})();
const UI={
 home:['Home','Accueil'],guide:['Player guide','Guide du joueur'],pokedex:['Pokédex','Pokédex'],movedex:['Moves','Attaques'],types:['Types','Types'],abilities:['Abilities','Talents'],
 champions:['Gym Champions','Champions d’arène'],wild:['Wild encounters','Rencontres sauvages'],dock:['The Dock','Le Quai'],kanto:['Kanto 151','Kanto 151'],itemsn:['Items & TMs','Objets & CT'],
 trainers:['Trainers','Dresseurs'],places:['Places','Lieux'],shops:['Shops','Boutiques'],dialogues:['Dialogues','Dialogues'],gifts:['Gifts & static','Cadeaux & fixes'],
 g_game:['The game','Le jeu'],g_mon:['Pokémon','Pokémon'],g_world:['The world','Le monde'],
 search:['Search…','Rechercher…'],search_all:['Search the whole wiki…','Chercher dans tout le wiki…'],noresult:['No result','Aucun résultat'],
 all_types:['All types','Tous les types'],all_methods:['All methods','Toutes les méthodes'],all_kinds:['All kinds','Tous les genres'],
 name:['Name','Nom'],type:['Type','Type'],category:['Category','Catégorie'],power:['Power','Puissance'],acc:['Acc.','Préc.'],pp:['PP','PP'],prio:['Priority','Priorité'],
 pokemon:['Pokémon','Pokémon'],location:['Location','Lieu'],method:['Method','Méthode'],levels:['Levels','Niveaux'],rate:['Rate','Taux'],
 physical:['Physical','Physique'],special:['Special','Spéciale'],status:['Status','Statut'],
 stats:['Base stats','Stats de base'],hp:['HP','PV'],atk:['Atk','Att'],def:['Def','Déf'],spa:['SpA','AtS'],spd:['SpD','DéS'],spe:['Spe','Vit'],bst:['Total','Total'],
 abilities_h:['Abilities','Talents'],levelup:['Level-up moves','Attaques par niveau'],tm:['TM / HM','CT / CS'],egg:['Egg moves','Attaques Œuf'],evo:['Evolution','Évolution'],evofrom:['Evolves from','Évolue depuis'],
 where:['Where to find it','Où le trouver'],nowhere:['Not found in the wild: evolve it, or get it as a gift / event.','Introuvable à l’état sauvage : fais-le évoluer, ou obtiens-le en cadeau / événement.'],
 lv:['Lv.','Niv.'],info:['Information','Informations'],growth:['Growth rate','Courbe de niveau'],catchrate:['Catch rate','Taux de capture'],
 height:['Height','Taille'],weight:['Weight','Poids'],cat:['Species','Espèce'],eggroups:['Egg groups','Groupes d’œufs'],female:['Female','Femelle'],genderless:['Genderless','Asexué'],
 ev:['EV yield','EV donnés'],basexp:['Base Exp.','Exp. de base'],friend:['Base friendship','Amitié de base'],dex:['Pokédex entry','Entrée du Pokédex'],
 learners:['Learned by','Appris par'],effect:['Effect','Effet'],back:['← Back to the list','← Retour à la liste'],
 ferry:['Ferry','Passeur'],zone:['Zone','Zone'],badges:['Badges','Badges'],nowild:['no wild Pokémon (story / shop / event)','aucun Pokémon sauvage (histoire / boutique / événement)'],
 gift:['Gift','Cadeau'],static:['Static','Fixe'],evoonly:['Evolution only','Évolution seulement'],wildc:['Wild','Sauvage'],
 foot:['Based on the pret/pokefirered decompilation. Pokémon is a trademark of Nintendo / Game Freak; this is a free fan project, not for sale.','Basé sur la décompilation pret/pokefirered. Pokémon est une marque de Nintendo / Game Freak ; projet de fans gratuit, non commercial.'],
 built:['Data generated from the game source on','Données générées depuis le code source du jeu le'],
 level:['level','niveau'],source:['Source','Source'],places_n:['Places','Lieux'],top:['Best spot','Meilleur endroit'],class:['Class','Classe'],team:['Team','Équipe'],
 pocket:['Pocket','Poche'],price:['Price','Prix'],obtain:['How to get','Où l’obtenir'],k_ground:['On the ground','Au sol'],k_hidden:['Hidden','Caché'],k_gift:['Given by an NPC','Donné par un PNJ'],k_shop:['Shop','Boutique'],k_prize:['Prize / reward','Lot / récompense'],k_item:['Item','Objet'],
 nosrc:['no known source in the map scripts','aucune source connue dans les scripts'],
 area:['Area','Zone'],kind:['Kind','Genre'],town:['Town','Ville'],city:['City','Ville'],route:['Route','Route'],cave:['Cave / dungeon','Grotte / donjon'],indoor:['Indoors','Intérieur'],
 npcs:['NPCs','PNJ'],trainers_n:['Trainers','Dresseurs'],texts:['Texts','Textes'],connections:['Connections','Connexions'],exits:['Exits & doors','Sorties & portes'],entrances:['Reached from','Accessible depuis'],
 samearea:['Other maps in this area','Autres cartes de cette zone'],signs:['Signs & objects','Panneaux & objets'],hiddenitems:['Hidden items','Objets cachés'],groundi:['Items on the ground','Objets au sol'],
 events:['Scripted events','Événements scriptés'],othertxt:['Other texts','Autres textes'],legend:['Legend','Légende'],zoom:['Zoom','Zoom'],music:['Music','Musique'],weather:['Weather','Météo'],
 up:['North','Nord'],down:['South','Sud'],left:['West','Ouest'],right:['East','Est'],speaker:['Speaker','Qui parle'],text:['Text','Texte'],map:['Map','Carte'],
 givenh:['Gifts & fixed encounters','Cadeaux & rencontres fixes'],shopsh:['Shops','Boutiques'],wildh:['Wild Pokémon','Pokémon sauvages'],trainersh:['Trainers','Dresseurs'],npch:['Characters','Personnages'],
 desc:['Description','Description'],holders:['Pokémon with this ability','Pokémon avec ce talent'],more:['Show more','Voir plus'],showing:['Showing','Affichage de'],
 item:['Item','Objet'],map_n:['maps','cartes'],
};
const t=k=>(UI[k]||[k,k])[lang==='fr'?1:0];
const L=x=>x&&typeof x==='object'&&!Array.isArray(x)&&'en' in x?(x[lang]||x.en):x;
const COL={Normal:'#9a9a8a',Fighting:'#b8402e',Flying:'#7f8fe0',Poison:'#8e47a8',Ground:'#c9a64a',Rock:'#a08d3a',Bug:'#8aa31c',Ghost:'#654d8e',Steel:'#8e8ea8',Fire:'#e8642a',Water:'#3f7fe0',Grass:'#4cae43',Electric:'#e0b800',Psychic:'#e0457a',Ice:'#4cc2c2',Dragon:'#5a3de0',Dark:'#5a463a',Fairy:'#e87fb4'};
const TFR={Normal:'Normal',Fighting:'Combat',Flying:'Vol',Poison:'Poison',Ground:'Sol',Rock:'Roche',Bug:'Insecte',Ghost:'Spectre',Steel:'Acier',Fire:'Feu',Water:'Eau',Grass:'Plante',Electric:'Électrik',Psychic:'Psy',Ice:'Glace',Dragon:'Dragon',Dark:'Ténèbres',Fairy:'Fée'};
const tn=x=>lang==='fr'?(TFR[x]||x):x;
const tb=x=>`<span class="t" style="background:${COL[x]||'#777'}">${tn(x)}</span>`;
const esc=s=>String(s==null?'':s).replace(/[&<>"]/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]));
const catn=c=>t({Physical:'physical',Special:'special',Status:'status'}[c]||c);
const POCK={ITEMS:['Items','Objets'],POKE_BALLS:['Poké Balls','Poké Balls'],TM_CASE:['TM Case','Boîte à CT'],BERRY_POUCH:['Berry Pouch','Sac à baies'],KEY_ITEMS:['Key items','Objets rares']};const pk=p=>(POCK[p]||[p,p])[lang==='fr'?1:0];
const norm=s=>String(s||'').normalize('NFD').replace(/[̀-ͯ]/g,'').toLowerCase();
function setLang(l){try{localStorage.setItem('lang',l)}catch(e){}location.reload()}
function setTheme(){const d=document.documentElement,cur=d.dataset.theme||(matchMedia('(prefers-color-scheme:dark)').matches?'dark':'light'),n=cur==='dark'?'light':'dark';d.dataset.theme=n;try{localStorage.setItem('theme',n)}catch(e){};const b=document.getElementById('thb');if(b)b.textContent=n==='dark'?'☀':'☾'}
// images / liens
const pimg=(n,c='thumb')=>n?`<img class="${c}" src="img/pokemon/${n}.png" alt="" loading="lazy" onerror="this.style.visibility='hidden'">`:'';
const iimg=(id,c='thumb')=>id?`<img class="${c}" src="img/items/${id}.png" alt="" loading="lazy" onerror="this.style.display='none'">`:'';
const pLink=(sp,n,img)=>`<a href="pokedex.html#${n}">${img?pimg(n):''}${esc(L(sp))}</a>`;
const mLink=m=>`<a href="movedex.html#${encodeURIComponent(m.en)}">${esc(L(m))}</a>`;
const placeLink=(id,name)=>id?`<a href="lieu.html#${id}">${esc(L(name))}</a>`:esc(L(name));
// navigation
const NAV=[['g_game',[['guide','guide'],['champions','champions'],['dock','dock'],['gifts','gifts']]],['g_mon',[['pokedex','pokedex'],['kanto','kanto'],['movedex','movedex'],['abilities','abilities'],['types','types'],['wild','wild']]],['g_world',[['lieux','places'],['trainers','trainers'],['shops','shops'],['items','itemsn'],['dialogues','dialogues']]]];
function nav(on){
 const menu=NAV.map(([g,ls])=>`<div class="grp${ls.some(l=>l[0]===on)?' on':''}"><button type="button">${t(g)} ▾</button><div class="drop">${ls.map(([h,k])=>`<a href="${h}.html"${h===on?' class="on"':''}>${t(k)}</a>`).join('')}</div></div>`).join('');
 document.body.insertAdjacentHTML('afterbegin',`<header class="top"><div class="bar"><button class="burger" aria-label="Menu" onclick="document.getElementById('mn').classList.toggle('open')">☰</button><a class="brand" href="index.html"><i></i><span>Pokémon Topaze</span></a><nav class="menu" id="mn">${menu}</nav>
 <div class="search"><input id="gs" type="search" placeholder="${esc(innerWidth<700?t('search'):t('search_all'))}" autocomplete="off" aria-label="Search"><div class="res" id="gr"></div></div>
 <div class="ctl"><button class="th" id="thb" onclick="setTheme()" title="Thème / Theme">☾</button><button ${lang==='fr'?'class="on"':''} onclick="setLang('fr')">FR</button><button ${lang==='en'?'class="on"':''} onclick="setLang('en')">EN</button></div></div></header>`);
 document.body.insertAdjacentHTML('beforeend','<footer>'+esc(t('foot'))+'</footer>');
 initSearch();
}
// recherche globale
let SEARCH_LOADED=null;
function loadScript(src){return new Promise((ok,ko)=>{const s=document.createElement('script');s.src=src;s.onload=ok;s.onerror=ko;document.head.appendChild(s)})}
const TYPE_LBL={pokemon:['Pokémon','Pokémon'],move:['Move','Attaque'],item:['Item','Objet'],ability:['Ability','Talent'],place:['Place','Lieu'],trainer:['Trainer','Dresseur']};
function runSearch(q){
 const words=norm(q).split(/\s+/).filter(Boolean);if(!words.length||!window.SEARCH)return[];const res=[];
 for(const e of SEARCH){const en=norm(e[1]),fr=norm(e[2]),sub=norm(e[4]);const hay=en+' '+fr+' '+sub;if(!words.every(w=>hay.includes(w)))continue;
  const nm=lang==='fr'?fr:en;let s=0;if(nm===words.join(' '))s=0;else if(nm.startsWith(words[0]))s=1;else if(en.startsWith(words[0])||fr.startsWith(words[0]))s=2;else if(nm.includes(words[0]))s=3;else s=4;
  s=s*10+({pokemon:0,move:1,item:2,ability:3,place:4,trainer:5}[e[0]]||0);res.push([s,e])}
 res.sort((a,b)=>a[0]-b[0]);return res.slice(0,14).map(x=>x[1])}
function initSearch(){
 const inp=document.getElementById('gs'),box=document.getElementById('gr');let sel=-1,list=[];
 const ensure=()=>SEARCH_LOADED||(SEARCH_LOADED=window.SEARCH?Promise.resolve():loadScript('data/search.js'));
 const draw=()=>{const q=inp.value.trim();if(!q){box.classList.remove('open');return}
  list=runSearch(q);sel=-1;box.innerHTML=list.length?list.map((e,i)=>`<a href="${e[3]}" data-i="${i}"><span class="ty">${(TYPE_LBL[e[0]]||[e[0],e[0]])[lang==='fr'?1:0]}</span><span>${esc(lang==='fr'?e[2]:e[1])}</span><small>${esc(e[4])}</small></a>`).join(''):`<div class="empty">${t('noresult')}</div>`;box.classList.add('open')};
 inp.addEventListener('focus',()=>ensure());inp.addEventListener('input',()=>ensure().then(draw));
 inp.addEventListener('keydown',ev=>{const as=[...box.querySelectorAll('a')];if(ev.key==='ArrowDown'||ev.key==='ArrowUp'){ev.preventDefault();sel=(sel+(ev.key==='ArrowDown'?1:-1)+as.length)%as.length;as.forEach((a,i)=>a.classList.toggle('sel',i===sel));as[sel]&&as[sel].scrollIntoView({block:'nearest'})}
  else if(ev.key==='Enter'){const a=as[Math.max(sel,0)];if(a)location.href=a.getAttribute('href')}else if(ev.key==='Escape'){box.classList.remove('open');inp.blur()}});
 document.addEventListener('click',e=>{if(!e.target.closest('.search'))box.classList.remove('open')});
 document.addEventListener('keydown',e=>{if(e.key==='/'&&!/INPUT|TEXTAREA|SELECT/.test(document.activeElement.tagName)){e.preventDefault();inp.focus()}});
 const th=document.documentElement.dataset.theme||(matchMedia('(prefers-color-scheme:dark)').matches?'dark':'light');const b=document.getElementById('thb');if(b)b.textContent=th==='dark'?'☀':'☾';
 window.addEventListener('hashchange',()=>box.classList.remove('open'));
}
// tableau générique : cols=[{h, get, html?, num?, first?}] ; opts {filters, max, hashSearch}
function table(el,rows,cols,opts={}){
 let sort=null,dir=1,q='';const box=document.getElementById(el),max=opts.max||150;let shown=max;
 const H=c=>UI[c.h]?t(c.h):c.h;
 box.innerHTML=`<div class="tools"><input type="search" placeholder="${esc(t('search'))}">${(opts.filters||[]).map((F,i)=>`<select data-f="${i}"><option value="">${esc(F.label)}</option>${F.values.map(v=>`<option value="${esc(Array.isArray(v)?v[0]:v)}">${esc(Array.isArray(v)?v[1]:v)}</option>`).join('')}</select>`).join('')}<span class="cnt"></span></div><div class="wrap"><table><thead><tr>${cols.map((c,i)=>`<th data-i="${i}">${H(c)}</th>`).join('')}</tr></thead><tbody></tbody></table></div><button class="more" style="display:none"></button>`;
 const tbody=box.querySelector('tbody'),fv=(opts.filters||[]).map(()=> ''),inp=box.querySelector('input'),more=box.querySelector('.more');
 const idx=rows.map(r=>norm(JSON.stringify(r)));
 function draw(){const hits=[];for(let i=0;i<rows.length;i++){if(q&&!q.every(w=>idx[i].includes(w)))continue;const x=rows[i];if((opts.filters||[]).every((F,k)=>!fv[k]||F.test(x,fv[k])))hits.push(x)}
  if(sort!==null){const g=cols[sort].get;hits.sort((a,b)=>{const A=g(a),B=g(b);return (A>B?1:A<B?-1:0)*dir})}
  box.querySelector('.cnt').textContent=hits.length+' / '+rows.length;
  tbody.innerHTML=hits.slice(0,shown).map(x=>'<tr>'+cols.map((c,i)=>`<td data-label="${esc(H(c))}" class="${c.num?'n':''} ${c.first?'first':''} ${c.nw?'nw':''} ${c.cls||''}">${c.html?c.html(x):esc(c.get(x))}</td>`).join('')+'</tr>').join('');
  more.style.display=hits.length>shown?'block':'none';more.textContent=t('more')+' ('+(hits.length-shown)+')'}
 inp.oninput=e=>{q=norm(e.target.value).split(/\s+/).filter(Boolean);shown=max;draw()};
 more.onclick=()=>{shown+=max*2;draw()};
 box.querySelectorAll('select').forEach(s=>s.onchange=e=>{fv[+s.dataset.f]=e.target.value;shown=max;draw()});
 box.querySelectorAll('th').forEach(th=>th.onclick=()=>{const i=+th.dataset.i;dir=sort===i?-dir:1;sort=i;draw()});
 if(opts.hashSearch&&location.hash.length>1){const v=decodeURIComponent(location.hash.slice(1));inp.value=v;q=norm(v).split(/\s+/).filter(Boolean)}
 draw();return {setQuery(v){inp.value=v;q=norm(v).split(/\s+/).filter(Boolean);draw()}}}
const fmtLv=(a,b)=>a==b?a:a+'–'+b;
