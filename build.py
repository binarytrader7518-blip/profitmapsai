#!/usr/bin/env python3
"""Static site generator for the ProfitMaps AI affiliate website.
Writes every page into ../site. Re-run after edits: python3 build.py"""
import json, os, html, datetime

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'site')
DOMAIN = 'https://profitmapsai.vercel.app'
AFF = 'https://jvz1.com/c/1834263/457277/'   # exact affiliate URL — do not modify
IMG = 'https://media.flexifunnels.io/sites/7455/1175331/images/'  # seller-hosted original artwork
TODAY = datetime.date(2026, 11, 11).isoformat()
NAME = 'ProfitMaps AI'
PAGES = []  # (path, title, desc)

# ---------------------------------------------------------------- helpers
def esc(s): return html.escape(s, quote=True)

ICONS = {
 'pin':'<path d="M12 21s-7-6.2-7-11.5A7 7 0 0 1 19 9.5C19 14.8 12 21 12 21z"/><circle cx="12" cy="9.5" r="2.6"/>',
 'grid':'<rect x="3" y="3" width="7" height="7" rx="1.5"/><rect x="14" y="3" width="7" height="7" rx="1.5"/><rect x="3" y="14" width="7" height="7" rx="1.5"/><rect x="14" y="14" width="7" height="7" rx="1.5"/>',
 'report':'<path d="M14 3H7a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h10a2 2 0 0 0 2-2V8z"/><path d="M14 3v5h5M9 13h6M9 17h4"/>',
 'globe':'<circle cx="12" cy="12" r="9"/><path d="M3 12h18M12 3a14 14 0 0 1 0 18M12 3a14 14 0 0 0 0 18"/>',
 'pen':'<path d="M12 20h9"/><path d="M16.5 3.5a2.1 2.1 0 0 1 3 3L7 19l-4 1 1-4z"/>',
 'search':'<circle cx="11" cy="11" r="7"/><path d="m20 20-3.5-3.5"/>',
 'users':'<path d="M17 21v-2a4 4 0 0 0-4-4H6a4 4 0 0 0-4 4v2"/><circle cx="9.5" cy="7" r="4"/><path d="M22 21v-2a4 4 0 0 0-3-3.9M16 3.1a4 4 0 0 1 0 7.8"/>',
 'bolt':'<path d="M13 2 4 14h7l-1 8 9-12h-7z"/>',
 'shield':'<path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/><path d="m9 12 2 2 4-4"/>',
 'clock':'<circle cx="12" cy="12" r="9"/><path d="M12 7v5l3 2"/>',
 'target':'<circle cx="12" cy="12" r="9"/><circle cx="12" cy="12" r="5"/><circle cx="12" cy="12" r="1.5"/>',
 'list':'<path d="M9 6h12M9 12h12M9 18h12"/><path d="m3 6 1 1 2-2M3 12l1 1 2-2M3 18l1 1 2-2"/>',
 'chart':'<path d="M3 3v18h18"/><path d="m7 15 4-4 3 3 6-7"/>',
 'tag':'<path d="M20.6 13.4 13.4 20.6a2 2 0 0 1-2.8 0L3 13V3h10l7.6 7.6a2 2 0 0 1 0 2.8z"/><circle cx="7.5" cy="7.5" r="1.5"/>',
 'plug':'<path d="M9 2v6M15 2v6M6 8h12v4a6 6 0 0 1-12 0zM12 18v4"/>',
 'layers':'<path d="m12 2 10 5-10 5L2 7z"/><path d="m2 17 10 5 10-5M2 12l10 5 10-5"/>',
 'chat':'<path d="M21 12a8 8 0 0 1-11.6 7.1L3 21l1.9-6.4A8 8 0 1 1 21 12z"/>',
 'download':'<path d="M12 3v12M7 10l5 5 5-5M5 21h14"/>',
}
def icon(n, wrap=True):
    s = f'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">{ICONS[n]}</svg>'
    return f'<div class="icon">{s}</div>' if wrap else s

ARROW = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M5 12h14M13 6l6 6-6 6"/></svg>'

def aff(label='Order Now', cls='btn', note=False, close=False):
    extra = ' data-close-after' if close else ''
    a = f'<a class="{cls}" href="{AFF}" target="_blank" rel="sponsored nofollow noopener"{extra}>{label} {ARROW}</a>'
    if note:
        a += '<span class="cta-note">Affiliate link · opens the official checkout on JVZoo</span>'
    return a

def pimg(file, alt, label='ProfitMaps AI', eager=False, w=400, h=460):
    load = 'eager" fetchpriority="high' if eager else 'lazy'
    return (f'<div class="pimg"><img data-orig src="{IMG}{file}" alt="{esc(alt)}" width="{w}" height="{h}" loading="{load}" decoding="async">'
            f'<div class="fbx" aria-hidden="true"><strong>{label}</strong><small>Original product image loads from the seller\'s server</small></div></div>')

def shot(file, alt, cap=''):
    c = f'<figcaption>{cap}</figcaption>' if cap else ''
    return (f'<figure class="shot-fig reveal"><img class="shot" data-orig src="{IMG}{file}" alt="{esc(alt)}" width="1200" height="760" loading="lazy" decoding="async">{c}</figure>')

def stage(inner, tilt=True):
    return f'<div class="stage"{" data-tilt" if tilt else ""}><div class="tilt"><div class="float">{inner}</div></div></div>'

def card(inner, cls=''): return f'<div class="card {cls} reveal">{inner}</div>'

LOGO = ('<svg viewBox="0 0 40 40" aria-hidden="true"><rect width="40" height="40" rx="11" fill="#03110B"/>'
        '<path d="M8 13h24M8 20h24M8 27h24M13 8v24M20 8v24M27 8v24" stroke="#1F5C40" stroke-width="1.2"/>'
        '<path d="M20 31s-7-6-7-11.2a7 7 0 0 1 14 0C27 25 20 31 20 31z" fill="#F2B530"/><circle cx="20" cy="19.6" r="2.6" fill="#03110B"/></svg>')

NAV = [('What Is It','product-overview.html'),('How It Works','how-it-works.html'),('Benefits','benefits.html'),
       ('Focus Areas','focus-areas/index.html'),('Reviews','reviews.html'),('Blog','blog/index.html'),('FAQ','faq.html')]

FOCUS = [
 ('map-rank-scans','Map Rank Scans','grid','See where a business shows up across a grid of points in its town, not just from one spot.'),
 ('client-reports','Reports & Action Plans','report','Turn a scan into a shareable report with competitors and a plain-English to-do list.'),
 ('ai-websites-content','AI Websites & Local Content','globe','Build a lead-capture site and draft Google Business Profile posts and local articles.'),
 ('business-finder','Business Finder & Prospecting','search','On Gold and Platinum, list businesses in a niche and town and score them 0–99.'),
 ('agency-white-label','Agency Workspaces & White Label','users','Client workspaces, team seats and white-label client accounts on the bundle plans.'),
]
POSTS = [
 ('google-maps-grid-rank-tracking-explained','Google Maps Grid Rank Tracking, Explained','Local SEO basics','7 min'),
 ('pitch-local-seo-without-promising-rankings','How to Pitch Local SEO Without Promising Rankings','Selling services','6 min'),
 ('google-business-profile-checklist','A Practical Google Business Profile Checklist','Google Business Profile','8 min'),
 ('ai-content-for-local-businesses','Using AI-Written Content for Local Businesses Responsibly','AI & content','6 min'),
]

def header(rel, current):
    items = ''.join(f'<li><a href="{rel}{u}"{" aria-current=\"page\"" if u==current else ""}>{l}</a></li>' for l,u in NAV)
    return f'''<a class="skip" href="#main">Skip to content</a>
<header class="site-header"><div class="container nav">
<a class="brand" href="{rel}index.html" aria-label="{NAME} home">{LOGO}<span>ProfitMaps <b>AI</b></span></a>
<nav aria-label="Main"><ul class="nav-links" id="nav-links">{items}</ul></nav>
<div class="nav-cta">{aff('Order Now','btn sm')}<button class="menu-btn" aria-controls="nav-links" aria-expanded="false" aria-label="Open menu"><span></span></button></div>
</div></header>'''

def footer(rel):
    ex = ''.join(f'<li><a href="{rel}{u}">{l}</a></li>' for l,u in [('Home','index.html')]+NAV[:3]+NAV[4:])
    fa = ''.join(f'<li><a href="{rel}focus-areas/{s}.html">{t}</a></li>' for s,t,_,_ in FOCUS)
    lg = ''.join(f'<li><a href="{rel}{u}">{l}</a></li>' for l,u in [('Pricing & Plans','index.html#pricing'),('Refund Guarantee','faq.html#refunds'),('Affiliate Disclosure','affiliate-disclosure.html'),('Privacy Policy','privacy-policy.html'),('Terms & Conditions','terms.html'),('Earnings & Results Disclaimer','disclaimer.html')])
    return f'''<footer class="site-footer"><div class="container">
<div class="foot-grid">
<div><a class="brand" href="{rel}index.html">{LOGO}<span>ProfitMaps <b>AI</b></span></a>
<p>An independent guide to {NAME}, the web app that scans Google Maps rankings for local businesses and turns them into reports, action plans and websites.</p>
<p>The seller offers a 30-day money-back guarantee through its support desk.</p></div>
<div><h4>Explore</h4><ul>{ex}</ul></div>
<div><h4>Focus Areas</h4><ul>{fa}</ul></div>
<div><h4>Support &amp; Legal</h4><ul>{lg}</ul></div>
</div>
<div class="legal">
<p><strong>Affiliate disclosure:</strong> This is an independent affiliate website, not the official {NAME} website. Orders are placed and processed on JVZoo, and we may receive a commission when you buy through our links. <a href="{rel}affiliate-disclosure.html">Read the full disclosure</a>.</p>
<p><strong>Results disclaimer:</strong> {NAME} is software. Neither this website nor the seller guarantees rankings, traffic, clients or income. Any examples are illustrations, and results depend on your own work and market. <a href="{rel}disclaimer.html">Full disclaimer</a>.</p>
<p>{NAME} is not affiliated with or endorsed by Google. Google, Google Maps and Google Business Profile are trademarks of Google LLC. {NAME} and its product artwork belong to their respective owner. JVZoo is a trademark of its respective owner.</p>
<p>© <span id="yr">2026</span> profitmapsai.vercel.app · Independent review and information site.</p>
</div></div></footer>'''

def modal(rel):
    return f'''<div class="pm-overlay" id="pm-overlay" hidden>
<div class="pm-modal" role="dialog" aria-modal="true" aria-labelledby="pm-title" aria-describedby="pm-desc">
<button class="pm-close" type="button" aria-label="Close offer">×</button>
{pimg('box-400.webp', 'ProfitMaps AI software box — original product artwork', w=400, h=460)}
<div class="kicker">{NAME}</div>
<h2 id="pm-title">Show local businesses where Maps misses them</h2>
<p id="pm-desc" class="small" style="margin-bottom:0">Scan a business across its town, send one clear report, and offer the fix. Three plans, each with the seller's 30-day money-back guarantee.</p>
<div class="pm-price">Plans listed from <strong>$37</strong></div>
<div class="pm-opts"><span class="pill">Basic</span><span class="pill">Gold Bundle</span><span class="pill">Platinum Bundle</span></div>
{aff('Check Current Offer','btn block',close=True)}
<span class="cta-note">Affiliate link · launch pricing on the sales page has closed, so checkout shows today's price</span>
</div></div>'''

def toast(rel):
    msgs = [
      {'t':'Compare the three plans','d':'Basic, Gold Bundle and Platinum Bundle differ in limits and agency tools.','l':'See plans','h':f'{rel}index.html#pricing'},
      {'t':'30-day money-back guarantee','d':'The seller refunds on request through its support desk within 30 days.','l':'Refund details','h':f'{rel}faq.html#refunds'},
      {'t':'Scans take a few minutes','d':'Per the seller, a map scan finishes in minutes and needs no client log-in.','l':'How it works','h':f'{rel}how-it-works.html'},
      {'t':'Need to find prospects?','d':'Business Finder is included with the Gold and Platinum bundles.','l':'Business Finder','h':f'{rel}focus-areas/business-finder.html'},
    ]
    data = esc(json.dumps(msgs))
    return f'''<div class="toast" id="pm-toast" role="status" aria-live="polite" data-messages="{data}">
<div class="ok"><svg viewBox="0 0 24 24" fill="none" stroke="#fff" stroke-width="3" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M5 12l5 5L20 7"/></svg></div>
<div><strong></strong><span></span><a href="#"></a></div>
<button class="toast-x" type="button" aria-label="Dismiss notification">×</button></div>'''

def write(path, title, desc, body, current='', schema=None, og_type='website'):
    assert len(title) <= 55, (path, len(title), title)
    assert len(desc) <= 155, (path, len(desc), desc)
    depth = path.count('/')
    rel = '../' * depth
    canon = DOMAIN + '/' + ('' if path == 'index.html' else path)
    PAGES.append((path, title, desc))
    sch = ''
    for s in (schema or []):
        sch += f'<script type="application/ld+json">{json.dumps(s, ensure_ascii=False)}</script>\n'
    doc = f'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(title)}</title>
<meta name="description" content="{esc(desc)}">
<link rel="canonical" href="{canon}">
<meta name="robots" content="index, follow">
<meta name="theme-color" content="#03110B">
<meta property="og:type" content="{og_type}">
<meta property="og:site_name" content="{NAME}">
<meta property="og:title" content="{esc(title)}">
<meta property="og:description" content="{esc(desc)}">
<meta property="og:url" content="{canon}">
<meta property="og:image" content="{IMG}og-profitmaps-ai.jpg">
<meta name="twitter:card" content="summary_large_image">
<link rel="icon" href="data:image/svg+xml,{LOGO.replace('<svg ','<svg xmlns=%27http://www.w3.org/2000/svg%27 ').replace('"',"'").replace('#','%23')}">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Hind:wght@400;500;600&family=Urbanist:ital,wght@0,600;0,700;0,800;1,700;1,800&display=swap" rel="stylesheet">
<link rel="stylesheet" href="{rel}assets/css/style.css">
<script>document.documentElement.classList.add("js")</script>
{sch}</head>
<body>
{header(rel, current)}
<main id="main">
{body}
</main>
{footer(rel)}
{modal(rel)}
{toast(rel)}
<script src="{rel}assets/js/main.js" defer></script>
</body>
</html>
'''
    full = os.path.join(OUT, path)
    os.makedirs(os.path.dirname(full), exist_ok=True)
    with open(full, 'w') as f: f.write(doc)

def cta_band(rel, h='Ready to run your first map scan?', p='Pick a plan on the official checkout, scan a business you already know, and see what the report shows.'):
    return f'''<section class="section"><div class="container"><div class="cta-band reveal">
<div><span class="eyebrow">{NAME}</span><h2>{h}</h2><p>{p}</p>
<ul class="checks"><li>Map scans with competitor view and an AI action plan</li><li>Reports and share links with your name and logo</li><li>AI website builder and local content writer</li><li>30-day money-back guarantee from the seller</li></ul>
<div class="btn-row">{aff('Get Instant Access','btn gold')}<a class="btn ghost" style="color:#fff;border-color:rgba(255,255,255,.3)" href="{rel}index.html#pricing">Compare plans</a></div>
<span class="cta-note">Affiliate link · opens the official checkout on JVZoo</span></div>
{stage(pimg('box-400.webp','ProfitMaps AI software box — original seller artwork'), tilt=False)}
</div></div></section>'''

def faq_html(items, prefix='q'):
    out = []
    for i,(q,a,*anchor) in enumerate(items):
        aid = f' id="{anchor[0]}"' if anchor else ''
        out.append(f'<div class="faq-item"{aid}><h3 style="margin:0"><button class="faq-q" aria-expanded="false" aria-controls="{prefix}{i}">{q}</button></h3><div class="faq-a" id="{prefix}{i}" hidden>{a}</div></div>')
    return ''.join(out)

def faq_schema(items):
    import re
    return {'@context':'https://schema.org','@type':'FAQPage','mainEntity':[
        {'@type':'Question','name':q,'acceptedAnswer':{'@type':'Answer','text':re.sub('<[^>]+>','',a)}} for q,a,*_ in items]}

# ---------------------------------------------------------------- plans (verified from profitmapsai.com/sales)
PLANS = [
 dict(key='basic', name='Basic', badge='Start here', img='plan-box-basic.webp', alt='ProfitMaps AI Basic plan box — original seller artwork',
      price='$37', strike='', unit='one-time launch price (listed)', for_='For trying scans and reports on businesses you pick yourself',
      feats=['10 businesses, 2 keywords each','5×5 map scans with competitor view','AI action plan for every scan','Reports and share links with your name and logo','Up to 10 AI websites and 50 AI articles/pages a month*','2,500 starter credits (first 500 buyers)','30-day money-back guarantee']),
 dict(key='gold', name='Gold Bundle', badge='Adds prospecting', img='plan-box-gold.webp', alt='ProfitMaps AI Gold Bundle box — original seller artwork', featured=True,
      price='$297', strike='', unit='one-time launch price (listed)', for_='For freelancers who also need to find and pitch prospects',
      feats=['50 businesses, 5 keywords each','Larger 9×9 map scans','Business Finder: 30 searches a month','Pitch Pack: one-page PDF, cold email, text and 3 follow-ups','50 websites and 500 AI articles/pages a month','10 client workspaces, 3 team members','10 white-label client accounts','3-Day Live Workshop access included','20,500 starter credits (first 500 buyers)','30-day money-back guarantee']),
 dict(key='platinum', name='Platinum Bundle', badge='Highest limits', img='plan-box-platinum.webp', alt='ProfitMaps AI Platinum Bundle box — original seller artwork',
      price='$697', strike='$797', unit='one-time launch price with the seller’s auto-applied $100 coupon', for_='For agencies managing many clients and locations',
      feats=['Unlimited businesses, keywords and websites (fair use)','Unlimited AI articles/pages (fair use)','Unlimited Business Finder (fair use)','1,000 prospects a month','100 white-label client accounts','3-Day Live Workshop access included','63,000 starter credits (first 500 buyers)','30-day money-back guarantee']),
]
def pricing(rel):
    cards = ''
    for p in PLANS:
        s = f'<s>{p["strike"]}</s>' if p['strike'] else ''
        f = ''.join(f'<li>{x}</li>' for x in p['feats'])
        cards += f'''<article class="plan{' featured' if p.get('featured') else ''} reveal"><span class="badge">{p['badge']}</span>
{pimg(p['img'], p['alt'], label=p['name'], w=400, h=400)}
<h3>{p['name']}</h3><p class="for">{p['for_']}</p>
<div class="price">{s}<strong>{p['price']}</strong><small>{p['unit']}</small></div>
<ul class="checks">{f}</ul>
{aff('Check Current Price','btn block' if p.get('featured') else 'btn ghost block')}</article>'''
    return f'''<section class="section mint" id="pricing"><div class="container">
<div class="sec-head center"><span class="eyebrow">Plans &amp; pricing</span><h2>Choose the {NAME} plan that fits your work</h2>
<p>Three plans, all built on the same map scanner. The bundles add prospecting, agency seats and white-label client accounts.</p></div>
<div class="pricing">{cards}</div>
<p class="small center" style="margin-top:28px;max-width:760px;margin-inline:auto">Prices are the one-time launch prices on the official sales page. The seller says launch pricing ended on 27 October and that plans are billed monthly after that, so the checkout page shows today's price. *The seller's FAQ says Basic drops to 5 websites and 10 AI articles a month after the first 500 buyers. Starter credits never expire, and in-app credit top-ups start at $10.</p>
</div></section>'''

GUARANTEE_SEAL = '''<svg class="seal" viewBox="0 0 160 160" role="img" aria-label="30-day money-back guarantee seal"><defs><linearGradient id="sg" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#F7C95A"/><stop offset="1" stop-color="#D99A12"/></linearGradient></defs>
<circle cx="80" cy="80" r="76" fill="url(#sg)"/><circle cx="80" cy="80" r="62" fill="#03110B"/><circle cx="80" cy="80" r="56" fill="none" stroke="#F2B530" stroke-width="1.5" stroke-dasharray="3 4"/>
<text x="80" y="82" text-anchor="middle" font-family="Urbanist,sans-serif" font-weight="800" font-size="44" fill="#fff">30</text>
<text x="80" y="104" text-anchor="middle" font-family="Urbanist,sans-serif" font-weight="700" font-size="11" letter-spacing="2" fill="#F2B530">DAY MONEY-BACK</text>
<text x="80" y="54" text-anchor="middle" font-family="Urbanist,sans-serif" font-weight="700" font-size="10" letter-spacing="2" fill="#9FB3A7">SELLER GUARANTEE</text></svg>'''

def guarantee(rel):
    return f'''<section class="section"><div class="narrow"><div class="guarantee reveal">{GUARANTEE_SEAL}
<div><span class="eyebrow">Seller guarantee</span><h2 style="font-size:clamp(1.6rem,2.6vw,2.1rem)">30 days to decide if it fits your work</h2>
<p>The sales page says every plan includes a 30-day money-back guarantee. If {NAME} isn't right for you, contact the seller's support desk within 30 days of buying for a full refund. The seller says you don't need to fill in forms or give a reason.</p>
<a class="textlink" href="{rel}faq.html#refunds">How refunds work</a></div></div></div></section>'''

# ---------------------------------------------------------------- HOME
def home():
    rel = ''
    fa_cards = ''.join(card(f'{icon(ic)}<span class="tag">Focus area {i+1:02d}</span><h3><a class="stretch" href="focus-areas/{s}.html">{t}</a></h3><p>{d}</p>','linked') for i,(s,t,ic,d) in enumerate(FOCUS[:4]))
    blog_cards = ''.join(post_card(p, 'blog/') for p in POSTS[:3])
    home_faq = [
      ('What is ProfitMaps AI?', f'<p>{NAME} is a web app for people who sell marketing services to local businesses. It scans how a business ranks on Google Maps across a grid of points in its town, compares it with competitors, and writes an action plan you can share as a report. <a href="product-overview.html">Read the full overview</a>.</p>'),
      ('Do I need a website or technical skills?', '<p>No. The seller says you don\'t need your own website or special skills, and you don\'t need access to a client\'s Google account to run scans or reports.</p>'),
      ('Is it a one-time payment or monthly?', '<p>During launch the plans were sold as one-time payments. The seller says plans are billed monthly once launch pricing ends, so check the checkout page for the current terms. <a href="#pricing">See the plans</a>.</p>'),
      ('Is there a money-back guarantee?', '<p>Yes. The seller offers a 30-day money-back guarantee, and you ask for a refund through its support desk. <a href="faq.html#refunds">Refund details</a>.</p>'),
      ('Can I promise clients #1 rankings?', '<p>No, and the seller advises against it too. The tool shows where a business stands and what to work on. It doesn\'t guarantee rankings, traffic or income.</p>'),
    ]
    body = f'''
<section class="hero"><div class="container hero-grid">
<div>
<span class="eyebrow">Google Maps rank report software</span>
<h1>Show local businesses where <em>Google Maps</em> can't find them</h1>
<p class="lead">{NAME} scans a business's Maps rankings across its whole town, shows who beats it in each spot, and turns the result into a report and a step-by-step fix you can offer as a service.</p>
<ul class="spec">
<li><b>Format</b><span>Web app (app.profitmapsai.com), nothing to install</span></li>
<li><b>Core tool</b><span>Grid scans, 5×5 by default and up to 9×9 on higher plans</span></li>
<li><b>Best for</b><span>Freelancers, consultants and agencies serving local businesses</span></li>
<li><b>Plans</b><span>Basic, Gold Bundle, Platinum Bundle</span></li>
<li><b>Guarantee</b><span>30-day money-back guarantee from the seller</span></li>
</ul>
<div class="btn-row">{aff('Get Instant Access','btn')}<a class="btn ghost" href="#pricing">Compare plans</a></div>
<span class="cta-note">Affiliate link · opens the official checkout on JVZoo</span>
<div class="stats"><div class="stat"><strong>3</strong><span>steps: scan, send, offer the fix</span></div><div class="stat"><strong>9×9</strong><span>largest scan grid (higher plans)</span></div><div class="stat"><strong>30</strong><span>day money-back guarantee</span></div></div>
</div>
{stage(pimg('box-400.webp','ProfitMaps AI software box — original product artwork from the seller', eager=True))}
</div></section>

<section class="section alt"><div class="container split">
<div class="reveal"><span class="eyebrow">At a glance</span><h2>One scan, one picture, one clear next step</h2>
<p>Most local business owners only check their ranking from their own shop or phone. A map scan checks the same search from many points across their service area and shows the result as a coloured grid, so they can see where they show up and where they don't.</p>
<p>{NAME} adds a list of competitors, an AI-written action plan in plain English, and a share link carrying your name and logo. You choose the business, send the link and set your own price.</p>
<div class="btn-row"><a class="btn ghost" href="product-overview.html">What's inside {NAME}</a></div></div>
<div class="reveal">{shot('app-map-full.webp','ProfitMaps AI scan result showing a 5 by 5 grid of Google Maps ranks for a sample salon in Las Vegas','Seller screenshot: a sample 5×5 scan. The seller describes the businesses and figures on its page as illustrations.')}</div>
</div></section>

<section class="section"><div class="container">
<div class="sec-head"><span class="eyebrow">The idea</span><h2>Why a map report gets a business owner's attention</h2></div>
<div class="grid g4">
{card('<span class="num">01</span><h3>It shows the problem</h3><p>A grid of rankings makes weak areas easy to see without explaining search algorithms.</p>')}
{card('<span class="num">02</span><h3>It names the competition</h3><p>The competitor view shows which businesses rank ahead in the same searches.</p>')}
{card('<span class="num">03</span><h3>It suggests the fix</h3><p>The AI action plan lists tasks with numbered steps, written in plain English.</p>')}
{card('<span class="num">04</span><h3>It tracks progress</h3><p>Recurring scans and ranking history show whether the work is moving the grid.</p>')}
</div>
<p style="margin-top:28px"><a class="textlink" href="product-overview.html">Read the full product overview</a></p>
</div></section>

<section class="section alt"><div class="container">
<div class="sec-head"><span class="eyebrow">Focus areas</span><h2>What {NAME} helps you do</h2><p>Five feature groups make up the app. Each one has its own page with plan availability and details.</p></div>
<div class="grid g4">{fa_cards}</div>
<p style="margin-top:28px"><a class="textlink" href="focus-areas/index.html">See all five focus areas</a></p>
</div></section>

<section class="section"><div class="container split">
<div class="reveal"><span class="eyebrow">Benefits</span><h2>Less time on research, more time selling the work</h2>
<ul class="checks two"><li>No client log-ins needed for scans</li><li>Scans finish in a few minutes</li><li>Reports carry your own branding</li><li>AI drafts posts and local pages</li><li>Keyword finder and CSV export</li><li>Works on your own business too</li><li>Starter credits never expire</li><li>Connects to AI assistants via MCP</li></ul>
<div class="btn-row">{aff('Order Now','btn')}<a class="textlink" href="benefits.html">All benefits</a></div></div>
<div class="reveal">{shot('app-todo-full.webp','ProfitMaps AI action plan listing seven tasks with numbered steps to rank higher','Seller screenshot: the AI action plan.')}</div>
</div>
<div class="container"><div class="timeline reveal">
<div><h4>Scan</h4><p>Enter a business and keyword, and the grid scan runs in a few minutes.</p></div>
<div><h4>Review</h4><p>Check the competitors and the AI action plan before you share anything.</p></div>
<div><h4>Send</h4><p>Share a branded report link. No log-in to the client's Google account is needed.</p></div>
<div><h4>Re-scan</h4><p>Recurring scans and ranking history show whether the work is paying off.</p></div>
</div></div></section>

<section class="section dark"><div class="container">
<div class="sec-head"><span class="eyebrow">How it works</span><h2>Three steps from scan to conversation</h2></div>
<div class="steps">
{card('<h3>Scan a business</h3><p>Pick any local business and a keyword it should rank for. The tool checks Maps results across a grid of points around it.</p>','step')}
{card('<h3>Send one picture</h3><p>Share the report: the grid, the competitors and the action plan, under your name and logo.</p>','step')}
{card('<h3>Let them ask for the fix</h3><p>If the owner wants help, you set the price and do the work, using the action plan and the AI tools as a starting point.</p>','step')}
</div>
<p style="margin-top:28px"><a class="textlink" style="color:var(--accent)" href="how-it-works.html">See the full workflow</a></p>
</div></section>

<section class="section"><div class="container">
<div class="sec-head"><span class="eyebrow">The foundation</span><h2>Good local SEO habits the tool supports</h2><p>Software can point out what to work on. Steady habits are what move rankings. These guides cover the basics.</p></div>
<div class="grid g3">
{card(f'{icon("pin")}<h3>A complete Business Profile</h3><p>Categories, hours, services and photos are the base every action plan builds on. <a href="blog/google-business-profile-checklist.html">Use the checklist</a>.</p>')}
{card(f'{icon("grid")}<h3>Measure from many points</h3><p>One search from one location tells you very little. <a href="blog/google-maps-grid-rank-tracking-explained.html">Learn how grid tracking works</a>.</p>')}
{card(f'{icon("chat")}<h3>Honest pitches</h3><p>Show the evidence, offer the work, and never promise a position. <a href="blog/pitch-local-seo-without-promising-rankings.html">Read the pitching guide</a>.</p>')}
</div></div></section>

<section class="section alt"><div class="container split">
<div class="reveal"><span class="eyebrow">Reviews</span><h2>What we know, and what we couldn't verify</h2>
<p>The official sales page has no customer testimonials, and we couldn't find independent, verifiable customer reviews of {NAME} when this page was published. We'd rather show nothing than make reviews up.</p>
<p>What we can offer is a clear summary of the documented features and limits, with points to check before you buy.</p>
<a class="btn ghost" href="reviews.html">Read our pre-purchase notes</a></div>
<div class="grid">
{card('<h3>Documented strengths</h3><ul class="checks"><li>A clear three-step workflow</li><li>Branded reports and share links on every plan</li><li>A 30-day refund window with no forms, per the seller</li></ul>')}
{card('<h3>Things to weigh</h3><ul class="checks xlist"><li>Launch pricing has ended, so check today\'s terms</li><li>Business Finder and white label need a bundle plan</li><li>AI writing needs fact-checking before you publish</li></ul>')}
</div></div></section>

{pricing(rel)}
{guarantee(rel)}

<section class="section alt"><div class="container">
<div class="sec-head"><span class="eyebrow">From the blog</span><h2>Local SEO guides for service sellers</h2></div>
<div class="grid g3">{blog_cards}</div>
<div class="center" style="margin-top:36px"><a class="btn ghost" href="blog/index.html">Visit the blog</a></div>
</div></section>

<section class="section"><div class="narrow">
<div class="sec-head center"><span class="eyebrow">FAQ</span><h2>Quick answers</h2></div>
{faq_html(home_faq,'hq')}
<div class="center" style="margin-top:28px"><a class="btn ghost" href="faq.html">All questions</a></div>
</div></section>

{cta_band(rel, 'Show your next prospect where they disappear on the map', 'Choose a plan on the official checkout and run your first scan on a business you already know.')}
'''
    write('index.html', 'ProfitMaps AI | Google Maps Rank Report Software',
          'ProfitMaps AI scans Google Maps rankings across a local business’s town and turns them into branded reports, action plans and websites. Compare plans.',
          body, '', [{'@context':'https://schema.org','@type':'WebSite','name':NAME,'url':DOMAIN+'/'}])

def post_card(p, prefix):
    slug,title,cat,rt = p
    return f'''<article class="card post-card reveal"><div class="thumb">{icon('pin',False)}<span>{cat}</span></div>
<div class="body"><div class="meta">{rt} read</div><h3><a href="{prefix}{slug}.html">{title}</a></h3><p>{POST_DESC[slug]}</p></div></article>'''

POST_DESC = {
 'google-maps-grid-rank-tracking-explained':'Why one ranking check misleads, and how a grid of search points shows a business’s real visibility on the map.',
 'pitch-local-seo-without-promising-rankings':'A simple way to open a conversation with a local business owner using evidence, not guarantees.',
 'google-business-profile-checklist':'The profile settings, content and routines worth checking before any other local SEO work.',
 'ai-content-for-local-businesses':'How to use AI drafts for posts and local pages without publishing errors or generic filler.',
}

# ---------------------------------------------------------------- PRODUCT OVERVIEW
def overview():
    rel=''
    body=f'''
<section class="hero sub"><div class="container hero-grid">
<div><nav class="breadcrumb" aria-label="Breadcrumb"><a href="index.html">Home</a> / What Is It</nav>
<span class="eyebrow">Product overview</span>
<h1>What is <em>{NAME}</em>?</h1>
<p class="lead">{NAME} is local SEO software that runs in your browser. It checks how a business ranks on Google Maps across its area, explains what to fix, and gives you the reports, websites and copy to sell that work as a service.</p>
<div class="btn-row">{aff('View Offer','btn')}<a class="btn ghost" href="benefits.html">See the benefits</a></div>
<span class="cta-note">Affiliate link · opens the official checkout on JVZoo</span></div>
{stage(pimg('box-400.webp','ProfitMaps AI software box shown at an angle — original seller artwork', eager=True))}
</div></section>

<section class="section alt"><div class="container">
<div class="sec-head"><span class="eyebrow">Specifications</span><h2>{NAME} at a glance</h2></div>
<div class="table-wrap reveal"><table>
<tbody>
<tr><th scope="row">Product name</th><td>{NAME}</td></tr>
<tr><th scope="row">Product type</th><td>Web application (software), accessed at app.profitmapsai.com</td></tr>
<tr><th scope="row">Main purpose</th><td>Scanning Google Maps rankings for local businesses and turning them into reports, action plans, websites and marketing copy</td></tr>
<tr><th scope="row">Scan grid</th><td>5×5 by default, up to 9×9 on higher plans</td></tr>
<tr><th scope="row">Scan time</th><td>A few minutes, according to the seller</td></tr>
<tr><th scope="row">Client access needed</th><td>None for scans or reports (no log-in to the client's Google account)</td></tr>
<tr><th scope="row">Plans</th><td>Basic, Gold Bundle, Platinum Bundle</td></tr>
<tr><th scope="row">Credits</th><td>Starter credits never expire. Scans and Business Finder searches use credits. Websites and AI writing don't, up to plan limits. Top-ups start at $10.</td></tr>
<tr><th scope="row">Sold through</th><td>JVZoo (the retailer named on the sales page)</td></tr>
<tr><th scope="row">Guarantee</th><td>30-day money-back guarantee through the seller's support desk</td></tr>
<tr><th scope="row">Google affiliation</th><td>None. The seller states it is not affiliated with or endorsed by Google.</td></tr>
</tbody></table></div>
</div></section>

<section class="section"><div class="container">
<div class="sec-head"><span class="eyebrow">What's inside</span><h2>The tools included in {NAME}</h2><p>This is the full feature list from the official sales page, grouped by job. Some tools need the Gold or Platinum bundle, as marked.</p></div>
<div class="grid g3">
{card(f'{icon("grid")}<h3>Scanning &amp; tracking</h3><ul class="checks"><li>Grid map scans</li><li>Competitor view</li><li>Keyword finder</li><li>Ranking history and recurring scans</li><li>CSV export</li></ul>')}
{card(f'{icon("report")}<h3>Reporting</h3><ul class="checks"><li>AI action plan with numbered steps</li><li>Reports and share links with your name and logo</li><li>Full white label (Gold &amp; Platinum)</li><li>Pitch Pack (Gold)</li></ul>')}
{card(f'{icon("globe")}<h3>Websites &amp; content</h3><ul class="checks"><li>AI website builder and site planner</li><li>Lead capture</li><li>Google Business Profile post writer</li><li>Local article writer</li></ul>')}
{card(f'{icon("search")}<h3>Prospecting</h3><ul class="checks"><li>Business Finder lists businesses by niche and town (Gold &amp; Platinum)</li><li>Scores each business from 0 to 99</li></ul>')}
{card(f'{icon("users")}<h3>Agency tools</h3><ul class="checks"><li>Client workspaces</li><li>Team members</li><li>White-label client accounts (Gold &amp; Platinum)</li></ul>')}
{card(f'{icon("plug")}<h3>Integrations</h3><ul class="checks"><li>Connects to AI assistants through MCP (Model Context Protocol)</li></ul>')}
</div></div></section>

<section class="section alt"><div class="container">
<div class="sec-head"><span class="eyebrow">Plan comparison</span><h2>Basic vs Gold vs Platinum</h2></div>
<div class="table-wrap reveal"><table>
<thead><tr><th>Feature</th><th>Basic</th><th>Gold Bundle</th><th>Platinum Bundle</th></tr></thead>
<tbody>
<tr><th scope="row">Businesses</th><td>10</td><td>50</td><td>Unlimited (fair use)</td></tr>
<tr><th scope="row">Keywords per business</th><td>2</td><td>5</td><td>Unlimited (fair use)</td></tr>
<tr><th scope="row">Scan grid</th><td>5×5</td><td>Up to 9×9</td><td>Higher-plan grids</td></tr>
<tr><th scope="row">Websites</th><td>10*</td><td>50</td><td>Unlimited (fair use)</td></tr>
<tr><th scope="row">AI articles / pages per month</th><td>50*</td><td>500</td><td>Unlimited (fair use)</td></tr>
<tr><th scope="row">Business Finder</th><td>—</td><td>30 searches / month</td><td>Unlimited (fair use)</td></tr>
<tr><th scope="row">Prospects per month</th><td>—</td><td>100</td><td>1,000</td></tr>
<tr><th scope="row">White-label client accounts</th><td>—</td><td>10</td><td>100</td></tr>
<tr><th scope="row">Client workspaces / team</th><td>—</td><td>10 workspaces, 3 team members</td><td>Listed with the bundle</td></tr>
<tr><th scope="row">Starter credits (first 500 buyers)</th><td>2,500</td><td>20,500</td><td>63,000</td></tr>
<tr><th scope="row">3-Day Live Workshop</th><td>—</td><td>Included</td><td>Included</td></tr>
<tr><th scope="row">Listed launch price</th><td>$37 one-time</td><td>$297 one-time</td><td>$697 one-time (with $100 coupon)</td></tr>
</tbody></table></div>
<p class="small" style="margin-top:14px">*The seller's FAQ says Basic drops to 5 websites and 10 AI articles a month after the first 500 buyers. White-label client accounts switch on 26 November 2026, according to the sales page. Where the seller doesn't list a Platinum figure separately, the table says so rather than guessing.</p>
</div></section>

<section class="section"><div class="container split">
<div class="reveal"><span class="eyebrow">Intended purpose</span><h2>Who {NAME} is made for</h2>
<p>The seller aims {NAME} at freelancers, marketers, consultants and agency owners who work with local service businesses: plumbers, dentists, roofers, salons, restaurants, gyms, repair shops and similar trades.</p>
<p>It's also open to business owners who want to check their own Maps visibility. The seller says plainly that it isn't for anyone expecting guaranteed rankings or income.</p>
<p><a class="textlink" href="benefits.html">See what that means in practice on the benefits page</a></p></div>
<div class="reveal">{shot('app-sites-full.webp','ProfitMaps AI business sites screen listing websites built by the AI website builder','Seller screenshot: websites built with the AI builder.')}</div>
</div></section>

<section class="section alt"><div class="container">
<div class="sec-head"><span class="eyebrow">Launch bonuses</span><h2>Bonuses listed on the sales page</h2><p>These were offered during launch. Check the sales page for what's available now.</p></div>
<div class="grid g2">
{card(pimg('bonus-gbp-course.webp','Bonus 1: Google Business Profile Course box — seller artwork',label='GBP Course',w=400,h=400)+'<h3>Google Business Profile course</h3><p>A short, practical course on setting up and optimising a Google Business Profile.</p>')}
{card('<div class="pimg"><img data-orig src="https://media.flexifunnels.io/7455/images/bonus-1day-training_zxqyfd0w.webp" alt="Bonus 2: The One-Day Live Training box — seller artwork" width="400" height="400" loading="lazy"><div class="fbx" aria-hidden="true"><strong>Live Training</strong><small>Original product image loads from the seller\'s server</small></div></div><h3>One-day live training with Chad</h3><p>A single Zoom training session held during launch week.</p>')}
</div></div></section>

{cta_band(rel)}
'''
    write('product-overview.html','What Is ProfitMaps AI? | Local SEO Software Overview',
          'What ProfitMaps AI is, who it’s for, every feature, plan limits and specs for this Google Maps rank scanning and local SEO reporting web app.',
          body,'product-overview.html')

# ---------------------------------------------------------------- HOW IT WORKS
def how():
    rel=''
    body=f'''
<section class="hero sub"><div class="container hero-grid">
<div><nav class="breadcrumb" aria-label="Breadcrumb"><a href="index.html">Home</a> / How It Works</nav>
<span class="eyebrow">How it works</span>
<h1>How {NAME} works, <em>step by step</em></h1>
<p class="lead">The workflow is simple: scan a business, send it one clear picture, and let the owner ask for the fix. The app handles the scanning and reporting. You choose the clients, set the price and check the work.</p>
<div class="btn-row">{aff('Get Instant Access','btn')}<a class="btn ghost" href="#steps">Walk through the steps</a></div>
<span class="cta-note">Affiliate link · opens the official checkout on JVZoo</span></div>
{stage(pimg('box-400.webp','ProfitMaps AI software box — original seller artwork', eager=True))}
</div></section>

<section class="section" id="steps"><div class="container">
<div class="split" style="margin-bottom:72px">
<div class="reveal"><span class="eyebrow">Step 1</span><h2>Scan a business</h2>
<p>Enter a local business and a keyword its customers search, such as "emergency plumber". The scanner checks Google Maps results from a grid of points across the area: 5×5 by default, or up to 9×9 on higher plans.</p>
<p>The seller says a scan takes a few minutes. You don't need the owner's permission or log-in to run it, because the scan reads public search results.</p></div>
<div class="reveal">{shot('app-map-full.webp','A ProfitMaps AI grid scan showing rank positions over a city map for a sample salon','Seller screenshot (illustrative sample data).')}</div></div>
<div class="split" style="margin-bottom:72px">
<div class="reveal" style="order:2"><span class="eyebrow">Step 2</span><h2>Send one picture</h2>
<p>Every scan becomes a report: the ranking grid, the competitors that show up ahead, and an AI action plan of tasks with numbered steps. Share it as a link with your name and logo. Gold and Platinum add full white label.</p>
<p>Read the action plan before you send it. You know the business, and the AI doesn't.</p></div>
<div class="reveal" style="order:1">{shot('app-todo-full.webp','ProfitMaps AI action plan screen with seven numbered tasks for improving Maps visibility','Seller screenshot: the AI action plan.')}</div></div>
<div class="split">
<div class="reveal"><span class="eyebrow">Step 3</span><h2>Let them ask for the fix</h2>
<p>If the owner wants help, you agree the scope and the price. The app's website builder, Google Business Profile post writer and local article writer give you drafts to work from. Re-run the scan later to see whether the grid has changed.</p>
<p><a class="textlink" href="blog/pitch-local-seo-without-promising-rankings.html">How to pitch without over-promising</a></p></div>
<div class="reveal">{shot('app-sites-full.webp','ProfitMaps AI websites list showing AI-built sites for local businesses','Seller screenshot: AI-built business sites.')}</div></div>
</div></section>

<section class="section alt"><div class="container">
<div class="sec-head center"><span class="eyebrow">Who does what</span><h2>The tool's job and your job</h2></div>
<div class="grid g2">
{card(f'{icon("bolt")}<h3>{NAME} handles</h3><ul class="checks"><li>Running the grid scan</li><li>Finding the competitors</li><li>Writing the report and action plan in plain English</li><li>Drafting websites, posts and local articles</li><li>Tracking rankings over time</li></ul>')}
{card(f'{icon("target")}<h3>You handle</h3><ul class="checks"><li>Choosing which businesses to approach</li><li>Sending the report link</li><li>Setting your price and scope</li><li>Checking AI-written content before it goes live</li><li>Doing the work, and keeping promises realistic</li></ul>')}
</div></div></section>

<section class="section"><div class="container">
<div class="sec-head"><span class="eyebrow">Your routine</span><h2>A sensible weekly workflow</h2><p>The app doesn't need daily attention. Here's a steady rhythm for using it alongside client work.</p></div>
<div class="timeline reveal">
<div><h4>Monday: prospect</h4><p>Pick a niche and town. On Gold and Platinum, use Business Finder to build a shortlist.</p></div>
<div><h4>Tuesday: scan</h4><p>Scan the shortlist and read each action plan before sharing it.</p></div>
<div><h4>Midweek: outreach</h4><p>Send the reports with a short, honest note. On Gold, use the Pitch Pack follow-ups.</p></div>
<div><h4>Friday: deliver</h4><p>Do client work, publish checked content, and set up recurring scans.</p></div>
</div></div></section>

<section class="section mint"><div class="container split">
<div class="reveal"><span class="eyebrow">Credits explained</span><h2>What uses credits, and what doesn't</h2>
<ul class="checks"><li><strong>Use credits:</strong> map scans and Business Finder searches</li><li><strong>Don't use credits:</strong> websites and AI writing, up to your plan's limits</li><li>Starter credits never expire</li><li>Credit top-ups are sold in the app, starting at $10</li></ul></div>
<div class="reveal"><h3>Explore each part of the workflow</h3>
<p>Each part of the workflow has its own focus-area page covering what it does and which plan includes it.</p>
<a class="btn" href="focus-areas/index.html">Browse the focus areas</a></div>
</div></section>

{cta_band(rel)}
'''
    write('how-it-works.html','How ProfitMaps AI Works | Scan, Report, Pitch',
          'See how ProfitMaps AI works: run a Google Maps grid scan, send a branded report with an AI action plan, and offer the fix. Steps, credits and workflow.',
          body,'how-it-works.html')

# ---------------------------------------------------------------- BENEFITS
def benefits():
    rel=''
    B = [
     ('clock','Fast research','The seller says a scan finishes in a few minutes, replacing hours of manual checks from different locations.','map-rank-scans'),
     ('grid','Evidence owners understand','A coloured grid of rankings is easier to explain than a spreadsheet of keyword positions.','map-rank-scans'),
     ('report','Branded reports','Share links carry your name and logo on every plan, and Gold and Platinum add full white label.','client-reports'),
     ('list','A plan, not just data','The AI action plan turns a scan into tasks with numbered steps you can quote for.','client-reports'),
     ('globe','Websites included','The AI website builder and site planner add lead capture without needing another tool.','ai-websites-content'),
     ('pen','Content drafts','The Business Profile post writer and local article writer give you a starting point, ready for editing.','ai-websites-content'),
     ('search','Built-in prospecting','On the bundles, Business Finder lists businesses in a niche and town and scores each one from 0 to 99.','business-finder'),
     ('users','Room to grow','Client workspaces, team seats and white-label client accounts support a small agency.','agency-white-label'),
    ]
    cards=''.join(card(f'{icon(i)}<h3>{t}</h3><p>{d}</p><a class="textlink" href="focus-areas/{s}.html">Related focus area</a>') for i,t,d,s in B)
    body=f'''
<section class="hero sub"><div class="container hero-grid">
<div><nav class="breadcrumb" aria-label="Breadcrumb"><a href="index.html">Home</a> / Benefits</nav>
<span class="eyebrow">Benefits</span>
<h1>The practical benefits of <em>{NAME}</em></h1>
<p class="lead">These are the benefits of the documented feature set: what the tool helps you do faster or more clearly. They don't include ranking or income promises, which neither we nor the seller make.</p>
<div class="btn-row">{aff('Order Now','btn')}<a class="btn ghost" href="#plans-fit">Which plan fits?</a></div>
<span class="cta-note">Affiliate link · opens the official checkout on JVZoo</span></div>
{stage(pimg('box-400.webp','ProfitMaps AI product box — original seller artwork', eager=True))}
</div></section>

<section class="section alt"><div class="container">
<div class="sec-head"><span class="eyebrow">Eight benefits</span><h2>What you get from the toolkit</h2></div>
<div class="grid g4">{cards}</div>
</div></section>

<section class="section"><div class="container split">
<div class="reveal"><span class="eyebrow">Beginner friendly</span><h2>No website or technical background needed</h2>
<p>The seller says you don't need your own website or special skills to start. Because scans read public Maps results, you don't need a client's Google log-in either. That lowers the barrier for a first conversation with a business owner.</p>
<ul class="checks"><li>Works in a web browser</li><li>Plain-English action plans</li><li>Can be used on your own business</li><li>Connects to AI assistants via MCP if you use one</li></ul></div>
<div class="reveal">{stage(pimg('plan-box-gold.webp','ProfitMaps AI Gold Bundle box — original seller artwork',label='Gold Bundle',w=400,h=400), tilt=False)}</div>
</div></section>

<section class="section dark"><div class="container">
<div class="sec-head"><span class="eyebrow">Straight talk</span><h2>What {NAME} won't do for you</h2><p>The seller is upfront about these limits, and so are we.</p></div>
<div class="grid g3">
{card('<h3>Guarantee rankings</h3><p>Rankings depend on Google and on the work done. The seller advises against promising #1 positions.</p>')}
{card('<h3>Guarantee income</h3><p>The sales page carries a no-income-guarantee disclaimer. Clients come from your outreach and service.</p>')}
{card('<h3>Publish perfect copy</h3><p>AI writing is a starting point. Check facts, prices and claims before anything goes live.</p>')}
</div></div></section>

<section class="section mint" id="plans-fit"><div class="container">
<div class="sec-head center"><span class="eyebrow">Plan fit</span><h2>Which plan matches your benefits?</h2></div>
<div class="grid g3">
{card('<span class="tag">Basic</span><h3>You pick the businesses</h3><p>Scans, action plans, branded reports, websites and AI writing for up to 10 businesses.</p>')}
{card('<span class="tag">Gold Bundle</span><h3>You also need prospects</h3><p>Adds Business Finder, the Pitch Pack, larger scans, workspaces and white-label accounts.</p>')}
{card('<span class="tag">Platinum Bundle</span><h3>You run many clients</h3><p>The highest limits: unlimited businesses, keywords, websites and Business Finder under fair use.</p>')}
</div>
<div class="center" style="margin-top:32px"><a class="btn" href="index.html#pricing">Compare plan details</a></div>
</div></section>

{cta_band(rel)}
'''
    write('benefits.html','ProfitMaps AI Benefits | Local SEO Agency Tool',
          'The real benefits of ProfitMaps AI for freelancers and agencies: fast Maps scans, branded reports, AI action plans, websites and prospecting tools.',
          body,'benefits.html')

# ---------------------------------------------------------------- FOCUS AREAS
FA_DETAIL = {
 'map-rank-scans': dict(title='Google Maps Grid Scans | ProfitMaps AI', desc='How ProfitMaps AI grid scans check Google Maps rankings from 5×5 to 9×9 points, with competitor view, keyword finder, history and CSV export.',
   h1='Map rank scans', eyebrow='Focus area 01', shot=('app-map-full.webp','ProfitMaps AI 5 by 5 grid scan of Google Maps rankings for a sample salon in Las Vegas'),
   lead='A single ranking check only tells you what one searcher in one spot sees. A grid scan repeats the same search from many points across a town and plots the results, so you can see where the business appears and where it drops out.',
   what=['Grid scans: 5×5 by default, up to 9×9 on higher plans','Competitor view showing who ranks in each spot','Keyword finder to choose what to scan','Ranking history and recurring scans','CSV export of results'],
   plans='All plans include scans. Basic runs 5×5 grids; Gold runs up to 9×9. Scans use credits, and starter credits never expire.',
   related=('google-maps-grid-rank-tracking-explained','Google Maps grid rank tracking, explained')),
 'client-reports': dict(title='White-Label Local SEO Reports | ProfitMaps AI', desc='ProfitMaps AI turns each map scan into a shareable report with competitors and an AI action plan, branded with your name and logo.',
   h1='Reports & action plans', eyebrow='Focus area 02', shot=('app-todo-full.webp','ProfitMaps AI action plan with seven tasks and numbered steps'),
   lead='The report is the part you put in front of a business owner. It combines the ranking grid, the competitors and an AI-written action plan, and sends it as one link under your name.',
   what=['Share links and reports with your name and logo','AI action plan: tasks with numbered steps in plain English','Full white label on Gold and Platinum','Pitch Pack on Gold: one-page PDF, cold email, text and 3 follow-ups'],
   plans='Branded reports are on every plan. White label is on Gold and Platinum, and the sales page lists the Pitch Pack with Gold.',
   related=('pitch-local-seo-without-promising-rankings','How to pitch local SEO without promising rankings')),
 'ai-websites-content': dict(title='AI Websites & Local Content | ProfitMaps AI', desc='Build lead-capture websites and draft Google Business Profile posts and local articles with ProfitMaps AI’s builder and writing tools.',
   h1='AI websites & local content', eyebrow='Focus area 03', shot=('app-sites-full.webp','ProfitMaps AI list of business websites created with the AI website builder'),
   lead='Many local businesses need the basics done: a simple site that captures leads, regular Business Profile posts and pages that mention the areas they serve. These tools draft that work for you to review.',
   what=['AI website builder and site planner','Lead capture on the sites you build','Google Business Profile post writer','Local article writer','Websites and AI writing don’t use credits, up to plan limits'],
   plans='Basic: 10 websites and 50 AI articles/pages a month (the seller’s FAQ says 5 and 10 after the first 500 buyers). Gold: 50 and 500. Platinum: unlimited under fair use.',
   related=('ai-content-for-local-businesses','Using AI-written content for local businesses responsibly')),
 'business-finder': dict(title='Business Finder Prospecting | ProfitMaps AI', desc='ProfitMaps AI Business Finder lists local businesses by niche and town and scores them 0–99. Available on the Gold and Platinum bundles.',
   h1='Business Finder & prospecting', eyebrow='Focus area 04', shot=None,
   lead='On Basic, you choose which business to scan. Business Finder, included with the Gold and Platinum bundles, builds the list for you: pick a niche and a town, and it lists the businesses and gives each a score from 0 to 99.',
   what=['Lists businesses for a chosen niche and town','Scores each business 0–99','Gold: 30 searches a month and 100 prospects a month','Platinum: unlimited searches (fair use) and 1,000 prospects a month','Business Finder searches use credits'],
   plans='Not on Basic. Included with the Gold and Platinum bundles.',
   related=('pitch-local-seo-without-promising-rankings','Turning a prospect list into honest outreach')),
 'agency-white-label': dict(title='Agency Workspaces & White Label | ProfitMaps AI', desc='Client workspaces, team members and white-label client accounts in ProfitMaps AI’s Gold and Platinum bundles, plus MCP AI-assistant support.',
   h1='Agency workspaces & white label', eyebrow='Focus area 05', shot=None,
   lead='Once you have several clients, you need to keep them organised. The bundle plans add separate client workspaces, seats for team members and white-label client accounts, so clients can log in to a branded view.',
   what=['Client workspaces (10 on Gold)','Team members (3 on Gold)','White-label client accounts: 10 on Gold, 100 on Platinum','White-label accounts switch on 26 November 2026, per the sales page','AI assistant connection via MCP'],
   plans='Workspaces and white-label client accounts are on Gold and Platinum. Where the seller doesn’t list a Platinum figure, we don’t guess one.',
   related=('google-business-profile-checklist','A practical Google Business Profile checklist for client onboarding')),
}

def focus():
    cards=''.join(card(f'{icon(ic)}<span class="tag">Focus area {i+1:02d}</span><h3><a class="stretch" href="{s}.html">{t}</a></h3><p>{d}</p><span class="textlink">Explore</span>','linked') for i,(s,t,ic,d) in enumerate(FOCUS))
    rel='../'
    body=f'''
<section class="hero sub"><div class="container hero-grid">
<div><nav class="breadcrumb" aria-label="Breadcrumb"><a href="../index.html">Home</a> / Focus Areas</nav>
<span class="eyebrow">Focus areas</span>
<h1>The five focus areas of <em>{NAME}</em></h1>
<p class="lead">{NAME} brings five jobs into one app: measuring Maps visibility, reporting it, building the fix, finding prospects and managing clients. Pick an area to see what it includes and which plan you need.</p>
<div class="btn-row">{aff('View Offer','btn')}<a class="btn ghost" href="../how-it-works.html">How it all connects</a></div>
<span class="cta-note">Affiliate link · opens the official checkout on JVZoo</span></div>
{stage(pimg('box-400.webp','ProfitMaps AI software box — original seller artwork', eager=True))}
</div></section>
<section class="section alt"><div class="container"><div class="grid g3">{cards}</div></div></section>
<section class="section"><div class="container">
<div class="sec-head"><span class="eyebrow">At a glance</span><h2>Which plan unlocks each area</h2></div>
<div class="table-wrap reveal"><table><thead><tr><th>Focus area</th><th>Basic</th><th>Gold Bundle</th><th>Platinum Bundle</th></tr></thead><tbody>
<tr><th scope="row"><a href="map-rank-scans.html">Map rank scans</a></th><td>5×5</td><td>Up to 9×9</td><td>Included</td></tr>
<tr><th scope="row"><a href="client-reports.html">Reports &amp; action plans</a></th><td>Branded</td><td>White label + Pitch Pack</td><td>White label</td></tr>
<tr><th scope="row"><a href="ai-websites-content.html">AI websites &amp; content</a></th><td>10 sites / 50 pieces*</td><td>50 sites / 500 pieces</td><td>Unlimited (fair use)</td></tr>
<tr><th scope="row"><a href="business-finder.html">Business Finder</a></th><td>—</td><td>30 searches / month</td><td>Unlimited (fair use)</td></tr>
<tr><th scope="row"><a href="agency-white-label.html">Agency &amp; white label</a></th><td>—</td><td>10 client accounts</td><td>100 client accounts</td></tr>
</tbody></table></div>
<p class="small" style="margin-top:14px">*Lower after the first 500 buyers, per the seller's FAQ.</p>
</div></section>
{cta_band(rel)}'''
    write('focus-areas/index.html','ProfitMaps AI Features | Focus Areas Explained',
          'Explore ProfitMaps AI’s five focus areas: map rank scans, reports and action plans, AI websites, Business Finder and agency white-label tools.',
          body,'focus-areas/index.html')
    for i,(s,t,ic,d) in enumerate(FOCUS):
        D=FA_DETAIL[s]
        others=''.join(f'<li><a href="{o}.html">{ot}</a></li>' for o,ot,_,_ in FOCUS if o!=s)
        visual = shot(*D['shot'], cap='Seller screenshot. The seller describes the data on its page as illustrative.') if D['shot'] else stage(pimg('plan-box-platinum.webp','ProfitMaps AI Platinum Bundle box — original seller artwork',label='Platinum Bundle',w=400,h=400), tilt=False)
        body=f'''
<section class="hero sub"><div class="container hero-grid">
<div><nav class="breadcrumb" aria-label="Breadcrumb"><a href="../index.html">Home</a> / <a href="index.html">Focus Areas</a> / {D['h1']}</nav>
<span class="eyebrow">{D['eyebrow']}</span><h1>{D['h1']}</h1>
<p class="lead">{D['lead']}</p>
<div class="btn-row">{aff('Get Instant Access','btn')}<a class="btn ghost" href="../index.html#pricing">Compare plans</a></div>
<span class="cta-note">Affiliate link · opens the official checkout on JVZoo</span></div>
{stage(pimg('box-400.webp','ProfitMaps AI software box — original seller artwork', eager=True))}
</div></section>
<section class="section alt"><div class="container split">
<div class="reveal"><span class="eyebrow">What's included</span><h2>What this part of {NAME} does</h2><ul class="checks">{''.join(f'<li>{w}</li>' for w in D['what'])}</ul>
<div class="callout"><p><strong>Plan availability:</strong> {D['plans']}</p></div></div>
<div class="reveal">{visual}</div></div></section>
<section class="section"><div class="container grid g2">
{card(f'{icon("chat")}<h3>Learn more</h3><p>Background reading on this topic from our blog:</p><p><a class="textlink" href="../blog/{D["related"][0]}.html">{D["related"][1]}</a></p>')}
{card(f'{icon("layers")}<h3>Other focus areas</h3><ul>{others}</ul>')}
</div></section>
{cta_band(rel)}'''
        write(f'focus-areas/{s}.html', D['title'], D['desc'], body, 'focus-areas/index.html')

# ---------------------------------------------------------------- REVIEWS
def reviews():
    rel=''
    body=f'''
<section class="hero sub"><div class="container hero-grid">
<div><nav class="breadcrumb" aria-label="Breadcrumb"><a href="index.html">Home</a> / Reviews</nav>
<span class="eyebrow">Reviews</span>
<h1>{NAME} review: <em>pre-purchase notes</em></h1>
<p class="lead">This page sets out what we could verify about {NAME}, what we couldn't, and the questions worth answering before you buy. It contains no invented testimonials, star ratings or review counts.</p>
<div class="btn-row">{aff('View Offer','btn')}<a class="btn ghost" href="faq.html">Read the FAQ</a></div>
<span class="cta-note">Affiliate link · opens the official checkout on JVZoo</span></div>
{stage(pimg('box-400.webp','ProfitMaps AI software box — original seller artwork', eager=True))}
</div></section>

<section class="section alt"><div class="narrow">
<div class="callout warn reveal"><p><strong>Customer review status:</strong> The official sales page has no customer testimonials, and we found no independent, verifiable customer reviews of {NAME} when this page was published ({TODAY}). We'll only add customer feedback here if it can be checked and we're allowed to reuse it.</p></div>
</div></section>

<section class="section"><div class="container">
<div class="sec-head"><span class="eyebrow">Our notes</span><h2>Strengths and trade-offs from the documented features</h2><p>This is an editorial summary based on the official sales page, not a customer rating or a test of results.</p></div>
<div class="grid g2">
{card('<h3>Strengths</h3><ul class="checks"><li>A focused workflow: scan, report, offer the fix</li><li>Grid scans show visibility across a whole area</li><li>Branded reports and share links on every plan</li><li>Websites and AI writing don’t use credits, up to plan limits</li><li>Starter credits never expire</li><li>No client log-in needed for scans or reports</li><li>A 30-day money-back guarantee with no forms, per the seller</li></ul>')}
{card('<h3>Trade-offs to weigh</h3><ul class="checks xlist"><li>Launch pricing has ended. The seller says plans become monthly after launch, so confirm today’s terms.</li><li>Business Finder, white label and client accounts need a bundle plan</li><li>Basic limits drop after the first 500 buyers, per the seller’s FAQ</li><li>Scans use credits, and top-ups cost extra</li><li>AI copy needs fact-checking before publishing</li><li>No rankings or income guarantee</li></ul>')}
</div></div></section>

<section class="section mint"><div class="container">
<div class="sec-head"><span class="eyebrow">Before you buy</span><h2>A six-point checklist</h2></div>
<div class="grid g3">
{card('<span class="num">1</span><h3>Know your buyer</h3><p>Do you already have local businesses in mind, or do you need Business Finder (Gold or Platinum)?</p>')}
{card('<span class="num">2</span><h3>Check today’s price</h3><p>Look at whether checkout shows a one-time or monthly charge, and the exact plan you’re buying.</p>')}
{card('<span class="num">3</span><h3>Estimate credit use</h3><p>Scans and Business Finder searches use credits. Plan how often you’ll re-scan.</p>')}
{card('<span class="num">4</span><h3>Plan your offer</h3><p>Decide what you’ll sell after the report, whether that’s profile work, a website or content, and at what price.</p>')}
{card('<span class="num">5</span><h3>Note the refund window</h3><p>You have 30 days to ask for a refund. Try the main features early.</p>')}
{card('<span class="num">6</span><h3>Keep claims honest</h3><p>Show evidence and offer work. Don’t promise rankings, as the seller also advises.</p>')}
</div></div></section>

<section class="section"><div class="container split">
<div class="reveal"><span class="eyebrow">Related reading</span><h2>Dig deeper before deciding</h2>
<ul class="checks"><li><a href="product-overview.html">Full feature list and specifications</a></li><li><a href="focus-areas/index.html">Plan-by-plan focus areas</a></li><li><a href="blog/google-maps-grid-rank-tracking-explained.html">How grid rank tracking works</a></li><li><a href="faq.html">Pricing, refunds and usage FAQ</a></li></ul></div>
<div class="reveal">{shot('app-map-full.webp','Sample ProfitMaps AI grid scan for a salon, from the seller','Seller screenshot (illustrative sample).')}</div>
</div></section>
{pricing(rel)}
{guarantee(rel)}'''
    write('reviews.html','ProfitMaps AI Review | Honest Pre-Purchase Notes',
          'An honest ProfitMaps AI review: documented strengths, trade-offs, review status and a pre-purchase checklist. No fake ratings or testimonials.',
          body,'reviews.html')

# ---------------------------------------------------------------- FAQ
FAQ = [
 ('What is ProfitMaps AI?', f'<p>{NAME} is a web app that scans Google Maps rankings for local businesses. It turns each scan into a report with competitors and an AI action plan, and includes tools for building websites and writing local marketing copy. <a href="product-overview.html">Full overview</a>.</p>'),
 ('Who is ProfitMaps AI for?', '<p>Freelancers, marketers, consultants and agency owners who work with local businesses such as plumbers, dentists, roofers, salons, restaurants, gyms and repair shops. You can also use it on your own business. It isn\'t suited to anyone looking for guaranteed rankings or income.</p>'),
 ('How does a ProfitMaps AI map scan work?', '<p>You enter a business and a keyword. The app checks Google Maps results from a grid of points across the area (5×5 by default, up to 9×9 on higher plans) and shows the business\'s position at each point. The seller says a scan takes a few minutes. <a href="how-it-works.html">See the workflow</a>.</p>'),
 ('Is ProfitMaps AI software or a supplement? What’s "inside" it?', '<p>It\'s software, so there are no ingredients. The "contents" are features: grid scans, competitor view, AI action plans, branded reports, an AI website builder, a Business Profile post writer, a local article writer, a keyword finder, ranking history, recurring scans and CSV export. The bundles add Business Finder, client workspaces and white label. <a href="focus-areas/index.html">Browse the focus areas</a>.</p>'),
 ('Do I need a website, skills or access to the client’s Google account?', '<p>The seller says no website or special skills are needed, and you don\'t need access to a client\'s Google account for scans or reports.</p>'),
 ('What plans are available and what do they cost?', '<p>There are three plans. The sales page lists these one-time launch prices: Basic at $37, Gold Bundle at $297, and Platinum Bundle at $797, or $697 with the auto-applied $100 coupon. The seller says launch pricing ended on 27 October and that plans become a monthly charge afterwards (Platinum is listed at $297 a month). Check the checkout page for the current price. <a href="index.html#pricing">Compare plans</a>.</p>','pricing-q'),
 ('What’s the difference between Basic, Gold and Platinum?', '<p>Basic covers scans, reports and AI tools for up to 10 businesses. Gold adds Business Finder, the Pitch Pack, 9×9 scans, workspaces, team seats and 10 white-label client accounts. Platinum has the highest limits, with unlimited businesses, keywords, websites and Business Finder under fair use, and 100 white-label client accounts. <a href="product-overview.html">See the comparison table</a>.</p>'),
 ('How do credits work?', '<p>Map scans and Business Finder searches use credits. Websites and AI writing don\'t, up to your plan\'s limits. Starter credits never expire, and you can buy top-ups in the app from $10.</p>'),
 ('Can I promise clients first-page or #1 rankings?', '<p>No. The seller advises against it, and neither the seller nor this site guarantees rankings, traffic, clients or income. Use the report as evidence and the action plan as a scope of work. <a href="blog/pitch-local-seo-without-promising-rankings.html">How to pitch honestly</a>.</p>'),
 ('Is the AI-written content ready to publish?', '<p>Treat it as a draft. The seller recommends checking facts before publishing, especially prices, services, locations and anything a business owner would need to approve. <a href="blog/ai-content-for-local-businesses.html">Our guide to using AI content</a>.</p>'),
 ('Is there a money-back guarantee? How do refunds work?', '<p>Yes. The seller offers a 30-day money-back guarantee on every plan. Contact the seller\'s support desk within 30 days of purchase to ask for a full refund. The sales page says you don\'t need to prove anything, fill in forms or do an interview. Refunds are handled by the seller, not by this website.</p>','refunds'),
 ('How do I order, and who processes the payment?', f'<p>Click any order button on this site to go to the official checkout. The sales page names JVZoo as the retailer. Access to the web app is described as instant after purchase. This is an independent affiliate site, so we don\'t process orders or hold your payment details. <a href="affiliate-disclosure.html">Affiliate disclosure</a>.</p>'),
 ('Is ProfitMaps AI affiliated with Google?', '<p>No. The seller states that {NAME} is not affiliated with or endorsed by Google.</p>'.replace('{NAME}',NAME)),
 ('Is shipping involved?', '<p>No. {NAME} is a web app, so there\'s nothing physical to ship. You use it in your browser.</p>'.replace('{NAME}',NAME)),
]
def faq():
    rel=''
    body=f'''
<section class="hero sub"><div class="container hero-grid">
<div><nav class="breadcrumb" aria-label="Breadcrumb"><a href="index.html">Home</a> / FAQ</nav>
<span class="eyebrow">FAQ</span>
<h1>{NAME} <em>questions</em>, answered</h1>
<p class="lead">Answers on features, plans, pricing, credits, refunds and ordering, based on the official sales page. Where something couldn't be verified, we say so.</p>
<div class="btn-row">{aff('Order Now','btn')}</div><span class="cta-note">Affiliate link · opens the official checkout on JVZoo</span></div>
{stage(pimg('box-400.webp','ProfitMaps AI software box — original seller artwork', eager=True))}
</div></section>
<section class="section alt"><div class="narrow">
<label class="small" for="faq-search">Search the questions</label>
<input id="faq-search" class="faq-search" type="search" placeholder="Try “refund”, “credits” or “Gold”" autocomplete="off">
{faq_html(FAQ)}
<p class="faq-empty">No matching questions. Try another word, or read the <a href="product-overview.html">product overview</a>.</p>
</div></section>
{cta_band(rel,'Still deciding? Start with the plan you can use this week','Every plan comes with the seller’s 30-day money-back guarantee.')}'''
    write('faq.html','ProfitMaps AI FAQ | Pricing, Plans & Refunds',
          'ProfitMaps AI FAQ: how map scans work, plan differences, launch pricing, credits, the 30-day money-back guarantee, ordering and Google affiliation.',
          body,'faq.html',[faq_schema(FAQ)])

# ---------------------------------------------------------------- BLOG
ARTICLES = {
'google-maps-grid-rank-tracking-explained': ('Google Maps Grid Rank Tracking Explained',
 'Why a single Google Maps rank check misleads, how grid rank tracking works, and how to read a scan before you show it to a business owner.',
 f'''<p>Ask a local business owner where they rank on Google Maps and they'll usually give you one answer, often based on a search from their own shop. That answer is real, but it describes one spot. Map results change with the searcher's location, so a business can rank near the top a few streets away and not appear at all across town.</p>
<h2>Why location changes the result</h2>
<p>Google's local results weigh how relevant a business is to the search, how prominent it is, and how close it is to the person searching. Proximity matters most in a Maps search: as the searcher moves, the set of nearby options changes, and so does the order. That's why one check can't describe a service area.</p>
<h2>What a grid scan does differently</h2>
<p>A grid scan runs the same keyword search from many evenly spaced points over an area, such as a 5×5 or 9×9 layout, and records the business's position at each point. The result is a map of coloured cells:</p>
<ul><li><strong>Strong cells</strong> show where the business appears near the top.</li><li><strong>Weak or empty cells</strong> show where it ranks low or not at all.</li><li><strong>The pattern</strong> often shows a "home zone" around the address that fades with distance.</li></ul>
<p>Tools like <a href="../focus-areas/map-rank-scans.html">{NAME}'s map rank scans</a> automate this and add the competitors that appear in each cell.</p>
<h2>How to read a scan responsibly</h2>
<ol><li><strong>Check the keyword.</strong> One scan covers one search phrase. "Dentist" and "emergency dentist" can look very different.</li><li><strong>Check the grid size against the service area.</strong> A grid that's too small or too large can flatter or exaggerate the gaps.</li><li><strong>Look at who wins the weak cells.</strong> Competitors' categories, reviews and profile completeness suggest what to work on.</li><li><strong>Re-scan before you claim progress.</strong> Rankings move for many reasons, so compare like with like over time.</li></ol>
<div class="callout"><p>A scan is a snapshot of public search results on one day. It's evidence for a conversation, not a forecast and not a promise.</p></div>
<h2>Turning the map into a plan</h2>
<p>The useful question isn't "why aren't we first?" but "what's within the business's control?" That usually starts with the <a href="google-business-profile-checklist.html">Google Business Profile basics</a>, then consistent business details across the web, steady reviews, and pages that clearly describe services and areas served.</p>
<p>Want to see how one tool packages this into a report? Read <a href="../how-it-works.html">how {NAME} works</a>.</p>'''),
'pitch-local-seo-without-promising-rankings': ('How to Pitch Local SEO Without Promising Rankings',
 'A simple, honest way to open a conversation with a local business owner using evidence from a map scan, with no guarantees or pressure tactics.',
 f'''<p>Local business owners hear from marketers all the time, and many of those pitches promise "page one" or "#1 on Google". Nobody can honestly guarantee that, and owners have learned to ignore it. The pitches that get answered tend to do the opposite: they show something specific and offer a clear, limited piece of work.</p>
<h2>1. Lead with something they can see</h2>
<p>A picture of where a business appears on the map, and where it doesn't, is easier to grasp than a list of keyword positions. Keep the first message short: what you checked, what you noticed, and a link to the report.</p>
<h2>2. Be specific about the search</h2>
<p>Name the keyword and the area. "When someone searches for 'roof repair' on the east side, your business doesn't show in most of the results we checked" is clear and checkable. Vague alarm isn't.</p>
<h2>3. Offer work, not outcomes</h2>
<p>Describe what you'll do: tidy the Business Profile, fix inconsistent listings, publish regular posts, and build a page for each service area. Price the work. Rankings may improve as a result, but say plainly that they can't be guaranteed.</p>
<div class="callout warn"><p>Avoid: guaranteed positions, fake deadlines, invented competitor claims, or implying you work for Google.</p></div>
<h2>4. Follow up a few times, then stop</h2>
<p>Two or three polite follow-ups spaced over a couple of weeks are normal. After that, move on. If you use templates, such as the <a href="../focus-areas/client-reports.html">Pitch Pack included with {NAME} Gold</a>, edit them so they sound like you and refer to the actual business.</p>
<h2>5. Re-scan and report honestly</h2>
<p>Once you start the work, run the same scan on the same keyword at regular intervals. Share what improved and what didn't. That honesty is what keeps a client for longer than one month.</p>
<p>Next: <a href="google-maps-grid-rank-tracking-explained.html">understand what a grid scan does and doesn't show</a>.</p>'''),
'google-business-profile-checklist': ('A Practical Google Business Profile Checklist',
 'A practical Google Business Profile checklist for local businesses: categories, details, services, photos, reviews and posting habits.',
 f'''<p>Before you work on anything else in local SEO, look at the Google Business Profile. It's often where the quickest, most visible fixes are, and it's what the searcher sees first in Maps. Use this checklist when you onboard a new client or audit your own business.</p>
<h2>Core details</h2>
<ul><li><strong>Business name</strong> matches the real-world name, with no added keywords. Keyword-stuffed names break Google's guidelines.</li><li><strong>Primary category</strong> is the most specific one that describes the main service. Add relevant secondary categories, but don't overdo it.</li><li><strong>Address or service area</strong> is set correctly. Service-area businesses that don't serve customers at their address should hide it and list their areas instead.</li><li><strong>Phone number and website</strong> work and match what's on the business's own site.</li><li><strong>Hours</strong>, including holiday hours, are current.</li></ul>
<h2>Services and description</h2>
<ul><li>Add the services the business actually offers, using the words customers use.</li><li>Write a plain description of what the business does and where. Avoid hype and links.</li><li>Fill in relevant attributes, such as accessibility details or online appointments, where they apply.</li></ul>
<h2>Photos</h2>
<ul><li>Use a clear logo and cover photo.</li><li>Add real photos of the premises, team and finished work.</li><li>Add new photos from time to time instead of all at once.</li></ul>
<h2>Reviews</h2>
<ul><li>Ask happy customers for reviews as part of normal service. Never buy reviews, offer incentives for them, or write them yourself.</li><li>Reply to reviews, positive and negative, briefly and professionally.</li></ul>
<h2>Ongoing habits</h2>
<ul><li>Publish updates or offers through profile posts on a regular schedule. A post writer, like <a href="../focus-areas/ai-websites-content.html">the one in {NAME}</a>, can draft them, but a person should approve each one.</li><li>Keep business details consistent across directories and the website.</li><li>Re-check the profile after any change to the business, such as a move, new services or new hours.</li></ul>
<div class="callout"><p>Google's own Business Profile guidelines are the final word and can change. Check them before making changes for a client.</p></div>
<p>Once the profile is in order, a <a href="google-maps-grid-rank-tracking-explained.html">grid scan</a> shows where it's starting to pay off.</p>'''),
'ai-content-for-local-businesses': ('Using AI-Written Content for Local Businesses',
 'How to use AI drafts for local business posts, service pages and area pages without publishing errors, generic filler or claims the owner can’t back up.',
 f'''<p>AI writing tools make it much faster to draft Business Profile posts, service pages and area pages. Used carelessly, they also make it faster to publish mistakes: wrong prices, services the business doesn't offer, and pages so generic they could describe any company in any town.</p>
<h2>Treat every draft as a draft</h2>
<p>Even the seller of {NAME} says to treat its AI writing as a starting point and check facts. That applies to every AI tool. Before anything goes live, confirm:</p>
<ul><li>Services, prices and opening hours</li><li>Areas served, and that the business really travels there</li><li>Any claims about experience, licences, awards or guarantees</li><li>Names of staff, products or brands</li></ul>
<h2>Add what only the business knows</h2>
<p>The difference between filler and useful content is detail: the problems customers actually call about, how the job is done, what affects the cost, and real photos. Ask the owner a few questions and add their answers to the draft.</p>
<h2>One page per real service or area</h2>
<p>A focused page for each main service, and for each area the business genuinely serves, helps customers find the right information. Pages that only swap the town name are thin, and search engines treat them that way.</p>
<div class="callout warn"><p>Don't publish health, legal or financial claims, or any "guaranteed result", unless the business can back it up and is allowed to make it.</p></div>
<h2>Get sign-off</h2>
<p>Agree a simple approval step with each client: you draft, they check, you publish. It protects both of you and builds trust.</p>
<p>Related: <a href="google-business-profile-checklist.html">Google Business Profile checklist</a> · <a href="../focus-areas/ai-websites-content.html">{NAME} websites &amp; content tools</a></p>'''),
}
def blog():
    rel='../'
    cards=''.join(post_card(p,'') for p in POSTS)
    body=f'''
<section class="hero sub"><div class="container">
<nav class="breadcrumb" aria-label="Breadcrumb"><a href="../index.html">Home</a> / Blog</nav>
<span class="eyebrow">Blog</span><h1>Local SEO guides for <em>service sellers</em></h1>
<p class="lead">Practical, original articles on Google Maps visibility, Business Profiles, honest pitching and AI content, for anyone selling local marketing.</p>
</div></section>
<section class="section alt" style="padding-top:48px"><div class="container"><div class="grid g2">{cards}</div></div></section>
{cta_band(rel,'Put the guides into practice','Use {0} to run the scans and build the reports these articles describe.'.format(NAME))}'''
    write('blog/index.html','Local SEO Blog | ProfitMaps AI',
          'Original local SEO guides on Google Maps grid tracking, Google Business Profile, honest pitching and responsible AI content for local businesses.',
          body,'blog/index.html')
    for slug,title,cat,rt in POSTS:
        st,desc,content = ARTICLES[slug]
        seo = f'{st} | Blog'
        if len(seo)>55: seo = st
        others=''.join(post_card(p,'') for p in POSTS if p[0]!=slug)
        body=f'''
<section class="hero sub" style="padding-bottom:40px"><div class="narrow">
<nav class="breadcrumb" aria-label="Breadcrumb"><a href="../index.html">Home</a> / <a href="index.html">Blog</a> / {cat}</nav>
<span class="eyebrow">{cat}</span><h1 style="font-size:clamp(2rem,4vw,3rem)">{title}</h1>
<p class="article-meta">Published {datetime.date(2026,11,11).strftime('%d %B %Y')} · {rt} read</p>
</div></section>
<section class="section" style="padding-top:24px"><div class="narrow article">{content}
<div class="callout" style="margin-top:40px"><p><strong>About {NAME}:</strong> a web app for Google Maps grid scans, reports and action plans. <a href="../product-overview.html">Read the overview</a> or <a href="../index.html#pricing">compare plans</a>.</p></div>
</div></section>
<section class="section alt"><div class="container"><div class="sec-head"><h2>More from the blog</h2></div><div class="grid g3">{others}</div></div></section>
{cta_band(rel)}'''
        schema=[{'@context':'https://schema.org','@type':'Article','headline':title,'description':desc,'datePublished':TODAY,'dateModified':TODAY,
                 'mainEntityOfPage':f'{DOMAIN}/blog/{slug}.html','author':{'@type':'Organization','name':'ProfitMaps AI review site'}}]
        write(f'blog/{slug}.html', seo, desc, body, 'blog/index.html', schema, 'article')

# ---------------------------------------------------------------- LEGAL
def legal_page(path,title,desc,h1,content):
    body=f'''<section class="hero sub" style="padding-bottom:32px"><div class="narrow"><nav class="breadcrumb" aria-label="Breadcrumb"><a href="index.html">Home</a> / {h1}</nav><h1 style="font-size:clamp(2rem,4vw,3rem)">{h1}</h1><p class="article-meta">Last updated {datetime.date(2026,11,11).strftime('%d %B %Y')}</p></div></section>
<section class="section" style="padding-top:16px"><div class="narrow article">{content}</div></section>'''
    write(path,title,desc,body)

def legal():
    legal_page('affiliate-disclosure.html','Affiliate Disclosure | ProfitMaps AI',
     'How this independent ProfitMaps AI information site earns money through affiliate links, and what that means for you as a buyer.',
     'Affiliate Disclosure', f'''<p>profitmapsai.vercel.app is an independent website that gives information about {NAME}. It is <strong>not</strong> the official {NAME} website, and it isn't run by the product's creator or seller.</p>
<h2>How we earn money</h2><p>Order buttons on this site are affiliate links. When you click one, you go to the official checkout, which is processed by JVZoo. If you buy, we may receive a commission from the sale. That doesn't change the price you pay.</p>
<h2>Our editorial approach</h2><ul><li>Product facts come from the official sales page and are written in our own words.</li><li>We don't publish invented testimonials, ratings, review counts, countdowns or discounts.</li><li>Where information couldn't be verified, we say so.</li></ul>
<h2>Orders, support and refunds</h2><p>We don't take payments, hold customer data or provide product support. Questions about access, billing or the 30-day money-back guarantee go to the seller's support desk. See our <a href="faq.html#refunds">refund FAQ</a>.</p>
<p>This disclosure is made in line with common advertising rules, such as the US FTC's endorsement guides, that require material connections to be disclosed.</p>''')
    legal_page('privacy-policy.html','Privacy Policy | ProfitMaps AI',
     'Privacy policy for the independent ProfitMaps AI information website: what data is and isn’t collected, local storage use and third-party links.',
     'Privacy Policy', f'''<p>This policy explains how profitmapsai.vercel.app handles information.</p>
<h2>Information we collect</h2><p>This is a static information website. It has no account sign-up, contact form or newsletter, and it doesn't ask you for personal information.</p>
<h2>Hosting logs</h2><p>Our hosting provider may automatically process technical data, such as IP addresses, browser type and the pages requested, to deliver and secure the site. That data is handled under the hosting provider's own privacy policy.</p>
<h2>Browser storage</h2><p>The site saves one item in your browser's local storage: the time you closed the offer pop-up, so it isn't shown again for 24 hours. It isn't sent to us, and you can clear it at any time in your browser settings.</p>
<h2>Fonts</h2><p>Fonts are loaded from Google Fonts, which may receive your IP address as part of delivering them. Some product images load from the seller's image server.</p>
<h2>Third-party links</h2><p>Order buttons take you to the official checkout on JVZoo. Anything you enter there is governed by JVZoo's and the seller's own policies.</p>
<h2>Changes</h2><p>We may update this policy. The date at the top shows the latest version.</p>''')
    legal_page('terms.html','Terms & Conditions | ProfitMaps AI',
     'Terms and conditions for using this independent ProfitMaps AI information website, including limits of liability and third-party purchases.',
     'Terms & Conditions', f'''<p>By using profitmapsai.vercel.app you agree to these terms.</p>
<h2>Information only</h2><p>Content on this site is general information about {NAME}, taken from the seller's public sales page and written in our own words. It isn't professional, legal, financial or business advice. Product features, limits and prices can change without notice. The official checkout and sales page are the final word.</p>
<h2>Purchases</h2><p>We don't sell {NAME}. Purchases happen on a third-party checkout (JVZoo) under the seller's terms, including its 30-day money-back guarantee.</p>
<h2>Intellectual property</h2><p>Our original text and design belong to this site. {NAME}'s name, product artwork and screenshots belong to their owner and are shown to identify the product. Google and Google Maps are trademarks of Google LLC.</p>
<h2>Limitation of liability</h2><p>This site is provided "as is". We aren't responsible for any loss arising from using this site, from third-party websites, or from using the product.</p>
<h2>Changes</h2><p>We may update these terms at any time by publishing a new version on this page.</p>''')
    legal_page('disclaimer.html','Earnings & Results Disclaimer | ProfitMaps AI',
     'Earnings and results disclaimer: ProfitMaps AI and this site make no guarantee of Google rankings, traffic, clients or income. Results vary.',
     'Earnings &amp; Results Disclaimer', f'''<h2>No guaranteed results</h2><p>{NAME} is software for scanning and reporting on Google Maps visibility. Neither this website nor the seller guarantees rankings, traffic, leads, clients or income. The seller's own sales page says the same.</p>
<h2>Illustrations</h2><p>Screenshots, sample businesses, maps and figures shown on the seller's page, and repeated here, are described by the seller as illustrations, not real results.</p>
<h2>Your results depend on you</h2><p>Any business results depend on your skills, effort, market, pricing, the services you deliver and factors outside anyone's control, including changes to Google's search systems.</p>
<h2>Not affiliated with Google</h2><p>{NAME} is not affiliated with or endorsed by Google. Google, Google Maps and Google Business Profile are trademarks of Google LLC.</p>
<h2>AI-generated content</h2><p>AI-written drafts can contain mistakes. Check every fact before you publish anything for yourself or a client.</p>''')

# ---------------------------------------------------------------- SEO files
def seo_files():
    urls=[]
    for path,_,_ in PAGES:
        loc = DOMAIN+'/' + ('' if path=='index.html' else path)
        pr = '1.0' if path=='index.html' else ('0.8' if path.count('/')==0 and not any(x in path for x in ['privacy','terms','disclaimer','affiliate']) else '0.6')
        if any(x in path for x in ['privacy','terms','disclaimer','affiliate']): pr='0.3'
        urls.append(f'  <url>\n    <loc>{loc}</loc>\n    <lastmod>{TODAY}</lastmod>\n    <priority>{pr}</priority>\n  </url>')
    with open(os.path.join(OUT,'sitemap.xml'),'w') as f:
        f.write('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'+'\n'.join(urls)+'\n</urlset>\n')
    with open(os.path.join(OUT,'robots.txt'),'w') as f:
        f.write(f'User-agent: *\nAllow: /\n\nSitemap: {DOMAIN}/sitemap.xml\n')
    with open(os.path.join(OUT,'404.html'),'w') as f:
        f.write(f'<!DOCTYPE html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Page not found | {NAME}</title><meta name="robots" content="noindex"><link rel="stylesheet" href="/assets/css/style.css"></head><body><main class="section"><div class="narrow center"><h1>Page not found</h1><p>The page you were looking for doesn\'t exist.</p><a class="btn" href="/">Back to the homepage</a></div></main></body></html>')

if __name__=='__main__':
    home(); overview(); how(); benefits(); focus(); reviews(); faq(); blog(); legal(); seo_files()
    print(f'Built {len(PAGES)} pages')
    with open(os.path.join(os.path.dirname(os.path.abspath(__file__)),'pages.json'),'w') as f: json.dump(PAGES,f,indent=1)
