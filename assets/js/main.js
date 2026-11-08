(function(){if(/[?&]static/.test(location.search))document.documentElement.classList.add('no-anim');
  var d=document,b=d.body,h=d.querySelector('.site-header');
  // header shadow
  function onScroll(){if(h)h.classList.toggle('is-scrolled',window.scrollY>8)}
  onScroll();window.addEventListener('scroll',onScroll,{passive:true});
  // burger
  var bg=d.querySelector('.burger');
  if(bg)bg.addEventListener('click',function(){var o=b.classList.toggle('nav-open');bg.setAttribute('aria-expanded',o)});
  // dropdown toggles (mobile + keyboard)
  d.querySelectorAll('.has-drop>button').forEach(function(btn){
    btn.addEventListener('click',function(e){var li=btn.parentNode;var o=li.classList.toggle('open');btn.setAttribute('aria-expanded',o)});
  });
  d.addEventListener('keydown',function(e){if(e.key==='Escape'){b.classList.remove('nav-open');d.querySelectorAll('.has-drop.open').forEach(function(x){x.classList.remove('open')})}});
  // reveal
  var els=d.querySelectorAll('.reveal');
  if('IntersectionObserver' in window){
    var io=new IntersectionObserver(function(en){en.forEach(function(x){if(x.isIntersecting){x.target.classList.add('in');io.unobserve(x.target)}})},{rootMargin:'0px 0px -8% 0px'});
    els.forEach(function(e){io.observe(e)});
  }else{els.forEach(function(e){e.classList.add('in')})}
  // filters (listing pages)
  var fs=d.querySelectorAll('.filters button');
  fs.forEach(function(btn){btn.addEventListener('click',function(){
    fs.forEach(function(x){x.setAttribute('aria-pressed','false')});btn.setAttribute('aria-pressed','true');
    var f=btn.getAttribute('data-f');
    d.querySelectorAll('[data-cat]').forEach(function(c){c.style.display=(f==='all'||c.getAttribute('data-cat')===f)?'':'none'});
  })});
  // year
  d.querySelectorAll('[data-year]').forEach(function(y){y.textContent=new Date().getFullYear()});
})();
