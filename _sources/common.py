# -*- coding: utf-8 -*-
"""Gabarits communs du site le-tec.fr (générateur statique)."""
import json, html, os

SITE = "https://le-tec.fr"
NAME = "TEC — Pilotage & Ingénierie"
LEGAL = "Technique et Économie de la Construction (TEC)"
ADDR = {"street": "163 cours de la Libération et du Général de Gaulle", "bldg": "Immeuble Équinoxe",
        "zip": "38100", "city": "Grenoble"}
PHONE = "04 76 42 64 91"; PHONE_INTL = "+33476426491"
EMAIL = "contact@le-tec.fr"
PDF = "assets/docs/plaquette-TEC-pilotage-ingenierie.pdf"
OUT = "/home/claude/tec/site"

def esc(s): return html.escape(s, quote=True)

# ---------- icônes ----------
I = {
 "concept": '<path d="M3 21h18"/><path d="M5 21V8l7-5 7 5v13"/><path d="M9 21v-6h6v6"/><path d="M9 10h.01M15 10h.01"/>',
 "moe": '<path d="M2 18h20"/><path d="M4 18v-2a8 8 0 0 1 16 0v2"/><path d="M12 8V5"/><path d="M9 6h6"/><path d="M8 12l1.5 2M16 12l-1.5 2"/>',
 "suivi": '<rect x="4" y="3" width="16" height="18" rx="2"/><path d="M9 3v2h6V3"/><path d="M8 11l2 2 4-4"/><path d="M8 17h8"/>',
 "opc": '<path d="M3 4v16h18"/><rect x="6" y="6" width="7" height="3" rx="1"/><rect x="10" y="11" width="8" height="3" rx="1"/><rect x="8" y="16" width="5" height="2.5" rx="1"/>',
 "eco": '<rect x="5" y="2.5" width="14" height="19" rx="2"/><path d="M8 6.5h8"/><path d="M8 11h.01M12 11h.01M16 11h.01M8 14.5h.01M12 14.5h.01M16 14.5h.01M8 18h.01M12 18h4"/>',
 "amo": '<circle cx="12" cy="8" r="3.5"/><path d="M5 21v-1.5A5.5 5.5 0 0 1 10.5 14h3a5.5 5.5 0 0 1 5.5 5.5V21"/>',
 "arrow": '<path d="M5 12h14"/><path d="M13 6l6 6-6 6"/>',
 "down": '<path d="M12 4v12"/><path d="M6 11l6 6 6-6"/><path d="M5 20h14"/>',
 "chev": '<path d="M6 9l6 6 6-6"/>',
 "phone": '<path d="M5 4h4l2 5-2.5 1.5a11 11 0 0 0 5 5L15 13l5 2v4a2 2 0 0 1-2 2A16 16 0 0 1 3 6a2 2 0 0 1 2-2"/>',
 "mail": '<rect x="3" y="5" width="18" height="14" rx="2"/><path d="M3 7l9 6 9-6"/>',
 "pin": '<path d="M12 21s-7-6.2-7-11.5A7 7 0 0 1 19 9.5C19 14.8 12 21 12 21z"/><circle cx="12" cy="9.5" r="2.5"/>',
 "clock": '<circle cx="12" cy="12" r="9"/><path d="M12 7v5l3 2"/>',
 "shield": '<path d="M12 3l8 3v6c0 5-3.5 8-8 9-4.5-1-8-4-8-9V6z"/><path d="M8.5 12l2.5 2.5 4.5-5"/>',
 "euro": '<path d="M17 6.5A7 7 0 1 0 17 17.5"/><path d="M4 10h9M4 14h9"/>',
 "doc": '<path d="M7 3h7l5 5v13H7z"/><path d="M14 3v5h5"/><path d="M10 13h6M10 17h6"/>',
 "users": '<circle cx="9" cy="8" r="3.2"/><path d="M3 20v-1a5 5 0 0 1 5-5h2a5 5 0 0 1 5 5v1"/><circle cx="17" cy="9" r="2.5"/><path d="M17 14a4 4 0 0 1 4 4v2"/>',
 "eye": '<path d="M2 12s3.5-7 10-7 10 7 10 7-3.5 7-10 7S2 12 2 12z"/><circle cx="12" cy="12" r="3"/>',
}
def icon(n, cls=""):
    return f'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"{(" class=%s" % chr(34)+cls+chr(34)) if cls else ""}>{I[n]}</svg>'

METIERS = [
 ("conception-architecturale.html", "concept", "Conception architecturale", "Faisabilité, esquisses, plans et dossiers d'autorisation, en lien avec l'architecte."),
 ("maitrise-oeuvre-execution.html", "moe", "Maîtrise d'œuvre d'exécution", "DCE, marchés, visas EXE, direction de l'exécution des travaux et réception."),
 ("suivi-de-chantier.html", "suivi", "Suivi de chantier", "Présence terrain, réunions hebdomadaires, comptes rendus et contrôle qualité."),
 ("opc-ordonnancement-pilotage-coordination.html", "opc", "OPC — Ordonnancement, pilotage, coordination", "Planning tous corps d'état, synchronisation des lots et tenue des délais."),
 ("economie-de-la-construction.html", "eco", "Économie de la construction & AMO", "Estimations, CCTP, consultation des entreprises, budget et assistance MOA."),
]

def nav(p, current):
    def cur(href): return ' aria-current="page"' if current == href else ''
    drop = "".join(f'<a href="{p}{h}"><span class="ico">{icon(ic)}</span><span><b>{t}</b><small>{d}</small></span></a>' for h, ic, t, d in METIERS)
    return f'''<a class="skip" href="#contenu">Aller au contenu</a>
<header class="site-header">
 <div class="wrap nav">
  <a class="brand" href="{p}index.html" aria-label="TEC Pilotage &amp; Ingénierie — accueil"><img src="{p}assets/img/logo-tec.svg" alt="TEC — Pilotage &amp; Ingénierie" width="73" height="46"><span>Maîtrise d'œuvre d'exécution &amp; OPC</span></a>
  <nav aria-label="Navigation principale">
   <ul class="menu">
    <li class="has-drop"><button class="top" aria-expanded="false" aria-haspopup="true">Métiers {icon("chev")}</button><div class="drop">{drop}<a href="{p}nos-metiers.html"><span class="ico">{icon("arrow")}</span><span><b>Tous nos métiers</b><small>Une ingénierie de chantier complète</small></span></a></div></li>
    <li><a class="top" href="{p}references.html"{cur("references.html")}>Références</a></li>
    <li><a class="top" href="{p}agence.html"{cur("agence.html")}>L'agence</a></li>
    <li><a class="top" href="{p}blog/index.html"{cur("blog")}>Blog chantiers</a></li>
    <li><a class="top" href="{p}actualites/index.html"{cur("actualites")}>Actualités</a></li>
   </ul>
  </nav>
  <div class="nav-cta">
   <a class="btn btn--ghost" href="{p}{PDF}" download>{icon("down")}Plaquette</a>
   <a class="btn btn--red" href="{p}contact.html">Nous consulter</a>
   <button class="burger" aria-label="Ouvrir le menu" aria-expanded="false"><span></span></button>
  </div>
 </div>
</header>'''

def footer(p):
    met = "".join(f'<li><a href="{p}{h}">{t.split(" — ")[0]}</a></li>' for h, ic, t, d in METIERS)
    return f'''<footer class="site-footer">
 <div class="wrap">
  <div class="f-top">
   <div>
    <img src="{p}assets/img/logo-tec-blanc.svg" alt="TEC — Pilotage &amp; Ingénierie" width="92" height="58" loading="lazy">
    <p>Maîtrise d'œuvre d'exécution, OPC, suivi de chantier et économie de la construction pour les maîtres d'ouvrage publics et privés des Alpes.</p>
    <p class="group-line">Une société du <a href="https://novelia-residences.fr" rel="noopener">Groupe Novélia</a>, aux côtés de <a href="https://www.cgbi.fr" rel="noopener">CGBI</a> et <a href="https://albedia.eu" rel="noopener">ALBEDIA</a>.</p>
   </div>
   <div><h4>Métiers</h4><ul>{met}</ul></div>
   <div><h4>Explorer</h4><ul>
    <li><a href="{p}references.html">Références chantiers</a></li>
    <li><a href="{p}agence.html">L'agence &amp; l'équipe</a></li>
    <li><a href="{p}blog/index.html">Blog chantiers</a></li>
    <li><a href="{p}actualites/index.html">Actualités juridiques &amp; techniques</a></li>
    <li><a href="{p}{PDF}" download>Plaquette (PDF)</a></li>
   </ul></div>
   <div><h4>Contact</h4><ul>
    <li>{ADDR["bldg"]}<br>{ADDR["street"]}<br>{ADDR["zip"]} {ADDR["city"]}</li>
    <li><a href="tel:{PHONE_INTL}">{PHONE}</a></li>
    <li><a href="mailto:{EMAIL}">{EMAIL}</a></li>
    <li><a href="{p}contact.html">Formulaire de contact →</a></li>
   </ul></div>
  </div>
  <div class="f-bot">
   <span>© <span data-year>2026</span> TEC — Technique et Économie de la Construction. Tous droits réservés.</span>
   <ul><li><a href="{p}mentions-legales.html">Mentions légales</a></li><li><a href="{p}confidentialite.html">Confidentialité</a></li><li><a href="{p}plan-du-site.html">Plan du site</a></li></ul>
  </div>
 </div>
</footer>
<script src="{p}assets/js/main.js" defer></script>'''

ORG_LD = {
 "@context": "https://schema.org", "@type": "ProfessionalService", "@id": SITE + "/#organisation",
 "name": "TEC — Pilotage & Ingénierie", "legalName": "Technique et Économie de la Construction",
 "alternateName": ["TEC", "T.E.C"], "url": SITE + "/", "logo": SITE + "/assets/img/logo-tec.svg",
 "image": SITE + "/assets/img/og-tec.png", "email": EMAIL, "telephone": PHONE_INTL,
 "description": "Bureau d'ingénierie de chantier : maîtrise d'œuvre d'exécution, OPC (ordonnancement, pilotage, coordination), suivi de chantier, économie de la construction et assistance à la conception architecturale en Isère, Savoie, Haute-Savoie et Hautes-Alpes.",
 "address": {"@type": "PostalAddress", "streetAddress": "Immeuble Équinoxe, 163 cours de la Libération et du Général de Gaulle", "postalCode": "38100", "addressLocality": "Grenoble", "addressRegion": "Auvergne-Rhône-Alpes", "addressCountry": "FR"},
 "geo": {"@type": "GeoCoordinates", "latitude": 45.1696, "longitude": 5.7166},
 "areaServed": [{"@type": "AdministrativeArea", "name": n} for n in ["Isère", "Savoie", "Haute-Savoie", "Hautes-Alpes", "Auvergne-Rhône-Alpes", "Provence-Alpes-Côte d'Azur"]],
 "knowsAbout": ["Maîtrise d'œuvre d'exécution", "MOEX", "Direction de l'exécution des travaux (DET)", "Ordonnancement pilotage coordination (OPC)", "Suivi de chantier", "Économie de la construction", "Assistance à maîtrise d'ouvrage", "Conception architecturale", "RE2020", "Réception des travaux (AOR)"],
 "founder": {"@type": "Organization", "name": "Groupe Novélia"},
 "parentOrganization": {"@type": "Organization", "name": "Groupe Novélia", "url": "https://novelia-residences.fr"},
 "employee": [
   {"@type": "Person", "name": "Benjamin Camerino", "jobTitle": "Directeur général"},
   {"@type": "Person", "name": "David Durigon", "jobTitle": "Responsable technique"},
   {"@type": "Person", "name": "Sandra Olandese", "jobTitle": "Cheffe de projet conception"}],
 "openingHoursSpecification": [{"@type": "OpeningHoursSpecification", "dayOfWeek": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"], "opens": "08:30", "closes": "18:30"}],
 "vatID": "FR60941810749", "taxID": "941 810 749 RCS Grenoble",
}

def crumbs_ld(items):
    return {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": i + 1, "name": n, "item": SITE + "/" + u} for i, (n, u) in enumerate(items)]}

import re as _re
def nbsp(t):
    # espaces insécables françaises avant : ; ? ! hors balises
    parts=_re.split(r'(<[^>]+>)',t)
    return "".join(x if x.startswith("<") else _re.sub(r" ([:;?!»])",lambda m:"\u00a0"+m.group(1),x) for x in parts)

def page(path, title, desc, body, current="", ld=None, og_type="website", crumbs=None, extra_head=""):
    depth = path.count("/")
    p = "../" * depth
    url = SITE + "/" + ("" if path == "index.html" else path)
    lds = [ORG_LD] + ([crumbs_ld(crumbs)] if crumbs else []) + (ld or [])
    ldtxt = "\n".join(f'<script type="application/ld+json">{json.dumps(x, ensure_ascii=False)}</script>' for x in lds)
    doc = f'''<!DOCTYPE html>
<html lang="fr">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(title)}</title>
<meta name="description" content="{esc(desc)}">
<link rel="canonical" href="{url}">
<meta name="robots" content="index, follow, max-image-preview:large">
<meta name="author" content="TEC — Technique et Économie de la Construction">
<meta name="theme-color" content="#121836">
<meta property="og:type" content="{og_type}">
<meta property="og:locale" content="fr_FR">
<meta property="og:site_name" content="TEC — Pilotage &amp; Ingénierie">
<meta property="og:title" content="{esc(title)}">
<meta property="og:description" content="{esc(desc)}">
<meta property="og:url" content="{url}">
<meta property="og:image" content="{SITE}/assets/img/og-tec.png">
<meta name="twitter:card" content="summary_large_image">
<link rel="icon" href="{p}favicon.svg" type="image/svg+xml">
<link rel="icon" href="{p}favicon-32.png" sizes="32x32" type="image/png">
<link rel="apple-touch-icon" href="{p}apple-touch-icon.png">
<link rel="preload" href="{p}assets/fonts/archivo.woff2" as="font" type="font/woff2" crossorigin>
<link rel="preload" href="{p}assets/fonts/intertight.woff2" as="font" type="font/woff2" crossorigin>
<link rel="stylesheet" href="{p}assets/css/style.css">
<link rel="alternate" type="application/rss+xml" title="Actualités TEC" href="{SITE}/feed.xml">
{extra_head}{ldtxt}
</head>
<body>
{nav(p, current)}
<main id="contenu">
{nbsp(body.replace("{P}", p))}
</main>
{footer(p)}
</body>
</html>'''
    full = os.path.join(OUT, path)
    os.makedirs(os.path.dirname(full), exist_ok=True)
    open(full, "w", encoding="utf-8").write(doc)
    return path

def page_hero(crumbs_list, eyebrow, h1, lead, meta=""):
    cr = "".join((f'<li><a href="{{P}}{u}">{n}</a></li>' if i < len(crumbs_list) - 1 else f'<li aria-current="page">{n}</li>') for i, (n, u) in enumerate(crumbs_list))
    return f'''<section class="page-hero"><div class="wrap">
<nav aria-label="Fil d'Ariane"><ol class="crumbs">{cr}</ol></nav>
<span class="eyebrow">{eyebrow}</span>
<h1>{h1}</h1>
<p class="lead">{lead}</p>{meta}
</div></section>'''

def cta_band(title="Un projet, un chantier à piloter ?", text="Parlons de votre opération : nous vous répondons sous 48 heures ouvrées avec une proposition de mission adaptée."):
    return f'''<section class="section--tight"><div class="wrap"><div class="cta reveal">
<div><h2>{title}</h2><p>{text}</p></div>
<div class="actions"><a class="btn btn--red" href="{{P}}contact.html">Nous consulter {icon("arrow")}</a><a class="btn btn--ghost-l" href="{{P}}{PDF}" download>{icon("down")}Plaquette PDF</a></div>
</div></div></section>'''

def faq_html(items):
    return '<div class="faq">' + "".join(f'<details><summary>{q}</summary><div><p>{a}</p></div></details>' for q, a in items) + '</div>'

def faq_ld(items):
    import re
    return {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
        {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": re.sub("<[^>]+>", "", a)}} for q, a in items]}
