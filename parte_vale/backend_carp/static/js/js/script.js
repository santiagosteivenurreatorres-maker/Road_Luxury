document.addEventListener('DOMContentLoaded', function(){
  const sidebar = document.getElementById('sidebar');
  const hamb = document.getElementById('hamb');
  hamb.addEventListener('click', ()=> sidebar.classList.toggle('active'));
  let current = 0;
  const slides = document.querySelectorAll('.hero-slide');
  function show(i){ slides.forEach((s,idx)=> s.style.display = idx===i?'block':'none'); }
  show(0);
  setInterval(()=>{ current=(current+1)%slides.length; show(current); },5000);
  const catalogArea = document.getElementById('catalog-area');
  function renderCatalog(cat){
    catalogArea.style.display = 'block'; catalogArea.innerHTML = '';
    const items = window.CATALOGS[cat] || [];
    const grid = document.createElement('div'); grid.className='grid-3';
    items.forEach(it=>{
      const card = document.createElement('div'); card.className='card';
      const img = document.createElement('img'); img.src='img/'+it.image;
      const h = document.createElement('h4'); h.textContent = it.name;
      const p = document.createElement('p'); p.textContent = it.desc;
      const price = document.createElement('div'); price.className='price'; price.textContent = it.price;
      const btn = document.createElement('button'); btn.className='btn-gold'; btn.textContent='Cotizar'; btn.onclick = ()=> location.href='cotizador.html';
      card.appendChild(img); card.appendChild(h); card.appendChild(p); card.appendChild(price); card.appendChild(btn);
      grid.appendChild(card);
    });
    catalogArea.appendChild(grid);
    window.scrollTo({top:catalogArea.offsetTop-80,behavior:'smooth'});
  }
  document.querySelectorAll('[data-cat]').forEach(el=> el.addEventListener('click', ()=>{
    const cat = el.getAttribute('data-cat');
    if(cat==='quienes'){ document.getElementById('about').scrollIntoView({behavior:'smooth'}); sidebar.classList.remove('active'); return; }
    renderCatalog(cat); sidebar.classList.remove('active');
  }));
});