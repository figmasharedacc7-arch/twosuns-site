# -*- coding: utf-8 -*-
"""The home page film band.

Two columns in the Zema style: the copy on the left, a 16:9 still on the right
with a play button over it. Nothing loads until someone clicks, so the page cost
is the poster and nothing else. The video only gets its controls once it starts.
"""

CSS = r"""
  /* HOME FILM BAND */
  .film-in{display:grid;grid-template-columns:1fr 1.15fr;gap:60px;align-items:center;}
  .film-copy .section-heading{margin-top:14px;}
  .film-accent{display:block;color:var(--sun-deep);}
  .film-stage{position:relative;aspect-ratio:16/9;border-radius:14px;overflow:hidden;
    background:#F3E3C4;box-shadow:0 26px 60px rgba(60,45,20,.20);}
  .film-stage video,.film-stage img{position:absolute;inset:0;width:100%;height:100%;
    object-fit:cover;display:block;}
  .film-stage video{opacity:0;transition:opacity .3s ease;}
  .film-stage.on video{opacity:1;}
  .film-stage.on img,.film-stage.on .film-play{opacity:0;pointer-events:none;}
  .film-play{position:absolute;inset:0;width:100%;height:100%;border:0;background:none;
    cursor:pointer;display:flex;align-items:center;justify-content:center;padding:0;
    transition:opacity .3s ease;}
  .film-play i{width:82px;height:82px;border-radius:50%;background:rgba(255,255,255,.92);
    box-shadow:0 10px 30px rgba(60,45,20,.28);display:flex;align-items:center;
    justify-content:center;transition:transform .2s ease,background .2s ease;}
  .film-play i::after{content:"";width:0;height:0;margin-left:6px;
    border-left:24px solid var(--sun-deep);border-top:15px solid transparent;
    border-bottom:15px solid transparent;}
  .film-play:hover i{transform:scale(1.07);background:#fff;}
  .film-play:focus-visible i{outline:3px solid var(--sun-deep);outline-offset:4px;}
  .film-note{margin-top:16px;font-size:13px;font-weight:700;letter-spacing:.14em;
    text-transform:uppercase;color:#8C6500;}

  @media(max-width:900px){
    .film-in{grid-template-columns:1fr;gap:30px;}
    .film-play i{width:64px;height:64px;}
    .film-play i::after{border-left-width:19px;border-top-width:12px;border-bottom-width:12px;}
  }
"""

SCRIPT = """<script>
(function(){
  var st=document.querySelector('.film-stage'); if(!st) return;
  var b=st.querySelector('.film-play'), v=st.querySelector('video');
  b.addEventListener('click',function(){
    st.classList.add('on'); v.controls=true; v.play();
  });
})();
</script>"""


def section(tag, heading, accent, sub, note, src, poster, band="band-warm"):
    return """<section class="%s">
  <div class="container film-in">
    <div class="film-copy">
      <div class="section-tag">%s</div>
      <h2 class="section-heading">%s <span class="film-accent">%s</span></h2>
      <p class="section-sub">%s</p>
      <div class="film-note">%s</div>
    </div>
    <div class="film-stage">
      <video src="%s" poster="%s" preload="none" playsinline
             aria-label="%s"></video>
      <img src="%s" alt="" width="1600" height="900" loading="lazy">
      <button class="film-play" type="button" aria-label="Play the film">
        <i aria-hidden="true"></i>
      </button>
    </div>
  </div>
</section>
""" % (band, tag, heading, accent, sub, note, src, poster, heading + " " + accent,
       poster)
