"""Hero video rotation.

The hero cycles through several clips instead of looping one. Only the first
clip is in the document with a source, so first paint and the largest
contentful paint are unchanged; the rest are attached once the page is idle and
are never fetched at all by someone who leaves inside the first hold.

It stays quiet when it should. Reduced motion falls back to the poster still,
Save-Data and 2g keep the single clip, playback pauses when the hero scrolls
away or the tab is hidden, and a browser that refuses to autoplay at all (iOS
low power) drops back to one clip and its poster rather than rotating to a
video that will not play.

The first clip carries the visible class in the markup, so with no JavaScript
at all the hero looks exactly as it did before the rotation existed.
"""

HOLD = 7500      # ms a clip holds before handing over
FADE = 1400      # ms crossfade, matches the CSS transition

CSS = """
  /* HERO VIDEO ROTATION */
  .hero-vid video{position:absolute;inset:0;width:100%;height:100%;object-fit:cover;
    display:block;opacity:0;transition:opacity FADEms ease-in-out;}
  .hero-vid video.on{opacity:1;}
  .hero-vid.solo video{opacity:1;transition:none;}
  /* after the rules above, so the still wins over display:block */
  @media(prefers-reduced-motion:reduce){
    .hero-vid video{display:none;}
    .hero-vid{background:url('hero-build-poster.jpg') center/cover no-repeat;}
  }
""".replace("FADE", str(FADE))


SCRIPT = """<script>
(function(){
  var box = document.querySelector('.hero-vid');
  if (!box) return;
  var vids = [].slice.call(box.querySelectorAll('video'));
  if (!vids.length) return;

  function solo(){
    box.classList.add('solo');
    for (var i = vids.length - 1; i > 0; i--) vids[i].parentNode.removeChild(vids[i]);
    vids = [vids[0]];
  }
  function reduced(){
    return window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  }
  function thin(){
    var c = navigator.connection;
    if (!c) return false;
    return c.saveData === true || /^(slow-)?2g$/.test(c.effectiveType || '');
  }
  if (vids.length < 2 || reduced() || thin()){ solo(); return; }

  var at = 0, visible = true;

  function attach(){
    for (var i = 1; i < vids.length; i++){
      var v = vids[i];
      if (!v.getAttribute('src') && v.getAttribute('data-src')){
        v.setAttribute('src', v.getAttribute('data-src'));
        v.load();
      }
    }
  }
  function ready(v){ return v.readyState >= 3; }

  function step(){
    if (!visible){ setTimeout(step, %(hold)d); return; }
    var next = (at + 1) %% vids.length, tries = 0;
    // a clip that has not buffered yet waits its turn rather than flashing black
    while (!ready(vids[next]) && tries < vids.length){
      next = (next + 1) %% vids.length;
      tries++;
    }
    if (next !== at){
      var cur = vids[at], nx = vids[next];
      try { nx.currentTime = 0; } catch (e) {}
      var p = nx.play();
      if (p && p.catch) p.catch(function(){});
      nx.classList.add('on');
      cur.classList.remove('on');
      (function(c){ setTimeout(function(){
        if (!c.classList.contains('on')) c.pause();
      }, %(fade)d); })(cur);
      at = next;
    }
    setTimeout(step, %(hold)d);
  }

  function pauseAll(){ for (var i = 0; i < vids.length; i++) vids[i].pause(); }
  function resume(){
    var p = vids[at].play();
    if (p && p.catch) p.catch(function(){});
  }

  document.addEventListener('visibilitychange', function(){
    if (document.hidden) pauseAll(); else if (visible) resume();
  });
  // the observer can report a false miss before the first frame settles, so the
  // box's own rect gets the last word
  function inView(){
    var r = box.getBoundingClientRect();
    return r.bottom > 0 && r.top < (window.innerHeight || document.documentElement.clientHeight);
  }
  if (window.IntersectionObserver){
    new IntersectionObserver(function(es){
      visible = es[0].isIntersecting || inView();
      if (visible){ if (!document.hidden) resume(); } else pauseAll();
    }, {threshold: 0.01}).observe(box);
  }

  function start(){
    // nothing is playing, so the browser is refusing autoplay outright
    if (vids[0].paused && vids[0].readyState >= 2){ solo(); return; }
    attach();
    setTimeout(step, %(hold)d);
  }
  if (window.requestIdleCallback) requestIdleCallback(start, {timeout: 2500});
  else setTimeout(start, 1200);
})();
</script>
""" % {"hold": HOLD, "fade": FADE}


def markup(clips):
    """clips: list of (mp4, poster). The first is eager and visible without
    JavaScript, the rest are deferred and start hidden."""
    out = []
    for i, (mp4, poster) in enumerate(clips):
        if i == 0:
            out.append('<video class="on" autoplay muted loop playsinline preload="auto" '
                       'poster="%s" aria-hidden="true"><source src="%s" type="video/mp4"></video>'
                       % (poster, mp4))
        else:
            out.append('<video muted loop playsinline preload="none" poster="%s" '
                       'data-src="%s" aria-hidden="true"></video>' % (poster, mp4))
    return "\n    ".join(out)
