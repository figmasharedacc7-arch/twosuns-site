# -*- coding: utf-8 -*-
"""Wire Capabilities to Use Cases, and give Use Cases its two missing filter dimensions."""
import re

p = "build.py"
b = open(p).read()

# 1. imports
old_imp = "from content2 import BUILT, USECASES, UC_THEMES, UC_ITEMS, COMPANY, DISCUSS"
new_imp = ("from content2 import (BUILT, USECASES, UC_THEMES, UC_ITEMS, COMPANY, DISCUSS,\n"
           "                      UC_AREA_LABELS, UC_GROUP_LABELS, UC_TAGS, CAP_LINKS)")
assert b.count(old_imp) == 1
b = b.replace(old_imp, new_imp)

# 2. a stable anchor for every use case
old_ticks = "def ticks(items):"
new_slug = '''def slug(title):
    """Stable anchor for a use case, so capability groups can link straight to it."""
    s = "".join(c.lower() if c.isalnum() else "-" for c in title)
    while "--" in s:
        s = s.replace("--", "-")
    return "uc-" + s.strip("-")


def ticks(items):'''
assert b.count(old_ticks) == 1
b = b.replace(old_ticks, new_slug, 1)

# 3. capability groups gain a Related use cases block
start = b.find("def acc_group")
end = b.find("\n\ndef ", start + 1)
assert start > 0 and end > start
b = b[:start] + '''def acc_group(groups, base_accent):
    out = ""
    for i, (name, desc, bullets) in enumerate(groups):
        col = ACCENTS[(base_accent + i) % len(ACCENTS)]
        rel = ""
        if name in CAP_LINKS:
            items = "".join(
                '<li><a href="use-cases.html#%s">%s</a></li>' % (slug(t), e(t))
                for t in CAP_LINKS[name])
            rel = ('<div class="acc-rel"><div class="k">Related use cases</div>'
                   '<ul>%s</ul></div>') % items
        out += """<details class="acc">
  <summary>
    <span class="acc-bar" style="background:%s;"></span>
    <span><span class="acc-title">%s</span><span class="acc-desc">%s</span></span>
  </summary>
  <div class="acc-body">%s%s</div>
</details>
""" % (col, e(name), e(desc), ticks(bullets), rel)
    return out''' + b[end:]

# 4. Use Cases: filter rows, tags, anchors, deep-link highlight
start = b.find("def build_usecases")
end = b.find("\n\n# ================================================================ COMPANY")
assert start > 0 and end > start
b = b[:start] + '''def build_usecases():
    d = USECASES
    s = head(d["title"], d["desc"]) + chrome_nav("use-cases.html")
    s += hero(d, wide=True) % (btn(d["primary"]) + btn(d["secondary"], ghost=True))

    def frow(label, dim, opts, prefix):
        btns = '<button class="uc-filter on" data-dim="%s" data-f="all">All</button>' % dim
        for i, t in enumerate(opts):
            btns += ('<button class="uc-filter" data-dim="%s" data-f="%s%d">%s</button>'
                     % (dim, prefix, i, e(t)))
        return ('<div class="uc-frow"><div class="lab">%s</div>'
                '<div class="uc-filters" style="margin-top:0;">%s</div></div>') % (e(label), btns)

    filters = (frow("Objective", "theme", UC_THEMES, "t")
               + frow("Industry area", "area", UC_AREA_LABELS, "a")
               + frow("User group", "group", UC_GROUP_LABELS, "g")
               + frow("Platform", "lens", ["Horizon", "Pulse", "Core", "Ray"], "l"))

    LENSES = ["Horizon", "Pulse", "Core", "Ray"]
    cards = ""
    for (ti, title, users, inputs, wf, out, lens) in UC_ITEMS:
        areas, groups = UC_TAGS[title]
        tags = ["t%d" % ti]
        tags += ["a%d" % a for a in areas]
        tags += ["g%d" % g for g in groups]
        tags += ["l%s" % L for L in LENSES if L in lens]
        chips = "".join('<span class="uc-tag">%s</span>' % e(UC_AREA_LABELS[a]) for a in areas[:2])
        chips += "".join('<span class="uc-tag">%s</span>' % e(UC_GROUP_LABELS[g]) for g in groups[:1])
        cards += """<article class="uc" id="%s" data-tags="%s">
  <h3>%s</h3>
  <dl>
    <dt>Typical users</dt><dd>%s</dd>
    <dt>Inputs</dt><dd>%s</dd>
    <dt>Configured workflow</dt><dd>%s</dd>
    <dt>Outputs and value</dt><dd>%s</dd>
  </dl>
  <span class="uc-lens">%s</span>
  <div class="uc-tags">%s</div>
</article>
""" % (slug(title), " ".join(tags), e(title), e(users), e(inputs), e(wf), e(out), e(lens), chips)

    s += """<section>
  <div class="container">
    <div class="section-tag">Filter</div>
    <h2 class="section-heading">Representative workflows</h2>
    <p class="section-sub">Filter by objective, by where you sit in the built industry, by who does
      the work, or by the part of the platform involved. Filters combine.</p>
    <div class="uc-filterset">%s</div>
    <button class="uc-clear" id="ucclear" hidden type="button">Clear all filters</button>
    <div class="uc-grid" id="ucgrid">%s</div>
    <p class="form-note" id="uccount"></p>
  </div>
</section>
""" % (filters, cards)

    s += """<section class="band-warm">
  <div class="container">
    <div class="section-tag">Your workflow</div>
    <h2 class="section-heading">%s</h2>
    %s
  </div>
</section>
""" % (e(d["close_h"]), "".join('<p class="lede">%s</p>' % e(p) for p in d["close_p"]))

    s += cta_band("Configure TwoSuns around the work you need to advance",
                  "Start from a use case described here or bring us a workflow of your own.",
                  d["close_primary"], d["close_secondary"])

    s += """<script>
(function(){
  var grid=document.getElementById('ucgrid'),
      cards=[].slice.call(grid.querySelectorAll('.uc')),
      cnt=document.getElementById('uccount'),
      clear=document.getElementById('ucclear'),
      btns=[].slice.call(document.querySelectorAll('.uc-filter')),
      picked={theme:'all',area:'all',group:'all',lens:'all'};

  function apply(){
    var wanted=[];
    for(var k in picked){ if(picked[k]!=='all') wanted.push(picked[k]); }
    var shown=0;
    cards.forEach(function(c){
      var tags=' '+c.getAttribute('data-tags')+' ', ok=true;
      wanted.forEach(function(w){ if(tags.indexOf(' '+w+' ')<0) ok=false; });
      c.style.display = ok ? '' : 'none';
      if(ok) shown++;
    });
    cnt.textContent = shown===cards.length
      ? 'Showing all ' + cards.length + ' use cases.'
      : 'Showing ' + shown + ' of ' + cards.length + ' use cases.';
    clear.hidden = !wanted.length;
  }

  btns.forEach(function(b){
    b.addEventListener('click',function(){
      var dim=b.getAttribute('data-dim');
      picked[dim]=b.getAttribute('data-f');
      btns.forEach(function(o){
        if(o.getAttribute('data-dim')===dim) o.classList.toggle('on', o===b);
      });
      apply();
    });
  });

  clear.addEventListener('click',function(){
    for(var k in picked) picked[k]='all';
    btns.forEach(function(o){ o.classList.toggle('on', o.getAttribute('data-f')==='all'); });
    apply();
  });

  apply();

  // arriving from a capability group: reveal that card whatever the filters say
  function jump(){
    var id=location.hash.slice(1); if(!id) return;
    var el=document.getElementById(id); if(!el) return;
    for(var k in picked) picked[k]='all';
    btns.forEach(function(o){ o.classList.toggle('on', o.getAttribute('data-f')==='all'); });
    apply();
    el.classList.add('flash');
    setTimeout(function(){ el.scrollIntoView({block:'center',behavior:'smooth'}); }, 60);
    setTimeout(function(){ el.classList.remove('flash'); }, 2600);
  }
  jump();
  window.addEventListener('hashchange', jump);
})();
</script>
"""
''' + b[end:]

open(p, "w").write(b)
print("build.py patched")
