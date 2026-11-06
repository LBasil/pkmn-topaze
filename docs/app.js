// Pokémon Topaze wiki — shared code (bilingual FR/EN)
let lang='en';try{lang=localStorage.getItem('lang')||((navigator.language||'').startsWith('fr')?'fr':'en')}catch(e){}
document.documentElement.lang=lang;
const UI={
 home:['Home','Accueil'],guide:['Player guide','Guide du joueur'],pokedex:['Pokédex','Pokédex'],movedex:['Movedex','Attaques'],types:['Types','Types'],
 champions:['Gym Champions','Champions d’arène'],wild:['Wild Encounters','Rencontres sauvages'],dock:['The Dock','Le Quai'],kanto:['Kanto 151','Kanto 151'],class:['Class','Classe'],team:['Team','Équipe'],trainers:['Trainers','Dresseurs'],itemsn:['Items & TMs','Objets & CT'],pocket:['Pocket','Poche'],price:['Price','Prix'],obtain:['How to get','Où l’obtenir'],k_ground:['On the ground','Au sol'],k_hidden:['Hidden','Caché'],k_gift:['Given by an NPC','Donné par un PNJ'],k_shop:['Shop','Boutique'],k_prize:['Prize / reward','Lot / récompense'],nosrc:['no known source in the map scripts','aucune source connue dans les scripts'],
 search:['Search…','Rechercher…'],all_types:['All types','Tous les types'],all_methods:['All methods','Toutes les méthodes'],
 name:['Name','Nom'],type:['Type','Type'],abilities:['Abilities','Talents'],category:['Category','Catégorie'],power:['Power','Puissance'],acc:['Acc.','Préc.'],pp:['PP','PP'],prio:['Priority','Priorité'],
 pokemon:['Pokémon','Pokémon'],location:['Location','Lieu'],method:['Method','Méthode'],levels:['Levels','Niveaux'],rate:['Rate','Taux'],
 physical:['Physical','Physique'],special:['Special','Spéciale'],status:['Status','Statut'],
 stats:['Base stats','Stats de base'],hp:['HP','PV'],atk:['Atk','Att'],def:['Def','Déf'],spa:['SpA','AtS'],spd:['SpD','DéS'],spe:['Spe','Vit'],bst:['Total','Total'],
 levelup:['Level-up moves','Attaques par niveau'],tm:['TM / HM','CT / CS'],egg:['Egg moves','Attaques Œuf'],evo:['Evolution','Évolution'],evofrom:['Evolves from','Évolue depuis'],
 where:['Where to find it','Où le trouver'],nowhere:['Not found in the wild: evolve it, or get it as a gift / event.','Introuvable à l’état sauvage : fais-le évoluer, ou obtiens-le en cadeau / événement.'],
 lv:['Lv.','Niv.'],info:['Information','Informations'],ability_h:['Abilities','Talents'],growth:['Growth rate','Courbe de niveau'],catchrate:['Catch rate','Taux de capture'],
 height:['Height','Taille'],weight:['Weight','Poids'],cat:['Species','Espèce'],eggroups:['Egg groups','Groupes d’œufs'],female:['Female','Femelle'],genderless:['Genderless','Asexué'],
 ev:['EV yield','EV donnés'],basexp:['Base Exp.','Exp. de base'],friend:['Base friendship','Amitié de base'],dex:['Pokédex entry','Entrée du Pokédex'],
 learners:['Learned by','Appris par'],learnby:['by level / egg','niveau / œuf'],effect:['Effect','Effet'],back:['← Back to the list','← Retour à la liste'],
 ferry:['Ferry','Passeur'],zone:['Zone','Zone'],badges:['Badges','Badges'],nowild:['no wild Pokémon (story / shop / event)','aucun Pokémon sauvage (histoire / boutique / événement)'],
 gift:['Gift','Cadeau'],static:['Static','Fixe'],evoonly:['Evolution only','Évolution seulement'],wildc:['Wild','Sauvage'],
 foot:['Based on the pret/pokefirered decompilation. Pokémon is a trademark of Nintendo / Game Freak; this is a free fan project, not for sale.','Basé sur la décompilation pret/pokefirered. Pokémon est une marque de Nintendo / Game Freak ; projet de fans gratuit, non commercial.'],
 built:['Data generated from the game source on','Données générées depuis le code source du jeu le'],
 level:['level','niveau'],item:['item','objet'],items:['items','objets'],of:['of','sur'],source:['Source','Source'],places:['Places','Lieux'],top:['Best spot','Meilleur endroit'],name2:['',''],
};
const t=k=>(UI[k]||[k,k])[lang==='fr'?1:0];
const L=x=>x&&typeof x==='object'&&!Array.isArray(x)&&'en' in x?x[lang]||x.en:x;
const COL={Normal:'#9a9a8a',Fighting:'#b8402e',Flying:'#7f8fe0',Poison:'#8e47a8',Ground:'#c9a64a',Rock:'#a08d3a',Bug:'#8aa31c',Ghost:'#654d8e',Steel:'#8e8ea8',Fire:'#e8642a',Water:'#3f7fe0',Grass:'#4cae43',Electric:'#e0b800',Psychic:'#e0457a',Ice:'#4cc2c2',Dragon:'#5a3de0',Dark:'#5a463a',Fairy:'#e87fb4'};
const TFR={Normal:'Normal',Fighting:'Combat',Flying:'Vol',Poison:'Poison',Ground:'Sol',Rock:'Roche',Bug:'Insecte',Ghost:'Spectre',Steel:'Acier',Fire:'Feu',Water:'Eau',Grass:'Plante',Electric:'Électrik',Psychic:'Psy',Ice:'Glace',Dragon:'Dragon',Dark:'Ténèbres',Fairy:'Fée'};
const tn=x=>lang==='fr'?(TFR[x]||x):x;
const tb=x=>`<span class="t" style="background:${COL[x]||'#777'}">${tn(x)}</span>`;
const esc=s=>String(s==null?'':s).replace(/[&<>"]/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]));
const POCK={ITEMS:['Items','Objets'],POKE_BALLS:['Poké Balls','Poké Balls'],TM_CASE:['TM Case','Boîte à CT'],BERRY_POUCH:['Berry Pouch','Sac à baies'],KEY_ITEMS:['Key items','Objets rares']};const pk=p=>(POCK[p]||[p,p])[lang==='fr'?1:0];
const catn=c=>t({Physical:'physical',Special:'special',Status:'status'}[c]||c);
function setLang(l){try{localStorage.setItem('lang',l)}catch(e){}location.reload()}
function nav(on){
 const p=[['index','home'],['guide','guide'],['pokedex','pokedex'],['kanto','kanto'],['movedex','movedex'],['types','types'],['champions','champions'],['items','itemsn'],['trainers','trainers'],['wild','wild'],['dock','dock']];
 document.body.insertAdjacentHTML('afterbegin','<header><nav><b>Pokémon Topaze</b>'+p.map(([h,k])=>`<a href="${h}.html"${h===on?' class="on"':''}>${t(k)}</a>`).join('')+
 `<span class="lang"><button ${lang==='fr'?'class="on"':''} onclick="setLang('fr')">FR</button><button ${lang==='en'?'class="on"':''} onclick="setLang('en')">EN</button></span></nav></header>`);
 document.body.insertAdjacentHTML('beforeend','<footer>'+esc(t('foot'))+'</footer>');
}
// generic table: cols=[{h:key|string, get, html?, num?}]
function table(el,rows,cols,opts={}){
 let sort=null,dir=1,q='',f='';const box=document.getElementById(el);
 const H=c=>UI[c.h]?t(c.h):c.h;
 box.innerHTML=`<div class="tools"><input type="search" placeholder="${esc(t('search'))}">${(opts.filters||[]).map((F,i)=>`<select data-f="${i}"><option value="">${esc(F.label)}</option>${F.values.map(v=>`<option value="${esc(Array.isArray(v)?v[0]:v)}">${esc(Array.isArray(v)?v[1]:v)}</option>`).join('')}</select>`).join('')}<span class="mut cnt"></span></div><div class="wrap"><table><thead><tr>${cols.map((c,i)=>`<th data-i="${i}">${H(c)}</th>`).join('')}</tr></thead><tbody></tbody></table></div>`;
 const tbody=box.querySelector('tbody'),fv=(opts.filters||[]).map(()=> '');
 function draw(){let r=rows.filter(x=>(!q||JSON.stringify(x).toLowerCase().includes(q))&&(opts.filters||[]).every((F,i)=>!fv[i]||F.test(x,fv[i])));
  if(sort!==null){const g=cols[sort].get;r=[...r].sort((a,b)=>{const A=g(a),B=g(b);return (A>B?1:A<B?-1:0)*dir})}
  box.querySelector('.cnt').textContent=r.length+' / '+rows.length;
  tbody.innerHTML=r.slice(0,opts.max||800).map(x=>'<tr>'+cols.map(c=>`<td${c.num?' class="n"':''}>${c.html?c.html(x):esc(c.get(x))}</td>`).join('')+'</tr>').join('')}
 box.querySelector('input').oninput=e=>{q=e.target.value.toLowerCase();draw()};
 box.querySelectorAll('select').forEach(s=>s.onchange=e=>{fv[+s.dataset.f]=e.target.value;draw()});
 box.querySelectorAll('th').forEach(th=>th.onclick=()=>{const i=+th.dataset.i;dir=sort===i?-dir:1;sort=i;draw()});
 draw()}
const pLink=(sp,n)=>`<a href="pokedex.html#${n}">${esc(L(sp))}</a>`;
const mLink=m=>`<a href="movedex.html#${encodeURIComponent(m.en)}">${esc(L(m))}</a>`;
