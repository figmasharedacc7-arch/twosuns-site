# -*- coding: utf-8 -*-
"""Scroll-triggered reveals.

Additive by design. The hiding only happens under an `.rv` class that a tiny
head script adds, and only when the browser supports it and the visitor has not
asked for reduced motion. If the script never runs, or the observer never
fires, everything stays visible. No markup changes, so removing this is one
CSS block and one script.
"""

TARGETS = [
    ".section-tag", ".section-heading", ".section-sub", ".lede",
    ".card", ".cardimg", ".person", ".step", ".callout", ".layer",
    ".arch3", ".ecl", ".ecl-fallback", ".a3-ray",
    ".acc", ".uc-frow", ".split2-panel", ".grid2 > *", ".grid3 > *",
]

CSS = """
  /* SCROLL REVEALS (only active once the head script adds .rv) */
  .rv %s{opacity:0;transform:translateY(20px);
    transition:opacity .68s cubic-bezier(.22,1,.36,1),transform .68s cubic-bezier(.22,1,.36,1);}
  .rv .in.in{opacity:1;transform:none;}
  .rv .hero .hero-eyebrow,.rv .hero h1,.rv .hero .hero-sub,.rv .hero .hero-actions{
    opacity:0;transform:translateY(16px);
    transition:opacity .8s cubic-bezier(.22,1,.36,1),transform .8s cubic-bezier(.22,1,.36,1);}
  .rv .hero .in.in{opacity:1;transform:none;}

""" % (", .rv ".join(TARGETS))

# runs in <head>, before first paint, so nothing flashes in then out
HEAD = """<script>
(function(){
  try{
    var reduce = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;
    if(!reduce && 'IntersectionObserver' in window) document.documentElement.classList.add('rv');
  }catch(e){}
})();
</script>"""

BODY = """<script>
(function(){
  var root=document.documentElement;
  if(!root.classList.contains('rv')) return;

  var SEL = %s;
  var els = [];
  SEL.forEach(function(s){
    [].forEach.call(document.querySelectorAll(s), function(el){
      if(els.indexOf(el)<0) els.push(el);
    });
  });

  // never hide something that already contains a revealed ancestor's job
  els = els.filter(function(el){
    return !els.some(function(other){ return other!==el && other.contains(el); });
  });

  var JOINED = SEL.join(', ');
  function show(el, delay){
    if(delay) el.style.transitionDelay = delay + 'ms';
    el.classList.add('in');
    // the CSS hides by selector, so anything matching inside must come with it
    [].forEach.call(el.querySelectorAll(JOINED), function(kid){ kid.classList.add('in'); });
  }

  // the hero plays on load, not on scroll
  var hero = document.querySelector('.hero');
  if(hero){
    [].forEach.call(hero.querySelectorAll('.hero-eyebrow, h1, .hero-sub, .hero-actions'),
      function(el,i){ setTimeout(function(){ show(el, 0); }, 90 + i*110); });
  }

  var seen = new WeakMap();
  var io = new IntersectionObserver(function(entries){
    entries.forEach(function(e){
      if(!e.isIntersecting) return;
      var el = e.target;
      // stagger siblings that arrive together, capped so nothing waits long
      var parent = el.parentNode, sibs = seen.get(parent) || 0;
      seen.set(parent, sibs+1);
      show(el, Math.min(sibs, 5) * 70);
      io.unobserve(el);
    });
  }, {rootMargin: '0px 0px -8%% 0px', threshold: 0.12});

  els.forEach(function(el){
    if(hero && hero.contains(el)) return;      // hero handled above
    io.observe(el);
  });

  // failsafe: if anything is still hidden after 3s, show it
  setTimeout(function(){
    els.forEach(function(el){ if(!el.classList.contains('in')) show(el, 0); });
  }, 1500);
})();
</script>"""


def body_script():
    import json
    return BODY % json.dumps(TARGETS)
