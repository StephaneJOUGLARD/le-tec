# -*- coding: utf-8 -*-
import os, sys, json, datetime, re
sys.path.insert(0, os.path.dirname(__file__))
from common import *
from refs import REFS, svg, visual, photo
from posts import BLOG, ACTU
from metiers import SERVICES

MOIS = ["janvier","février","mars","avril","mai","juin","juillet","août","septembre","octobre","novembre","décembre"]
def fdate(d):
    y, m, j = map(int, d.split("-")); return f"{j}{'er' if j==1 else ''} {MOIS[m-1]} {y}"
REF = {r["slug"]: r for r in REFS}
pages = []

def ref_card(r, p="{P}", tag="a"):
    st = "wip" if r["status"] != "Livré" else ""
    facts = "".join(f'<span class="tag">{f}</span>' for f in r["facts"])
    ph = f'<div class="progress-l"><span>Phase en cours</span><b>{r["phase"]}</b></div>' if r.get("phase") else ""
    return f'''<a class="ref reveal" href="{p}references.html#{r["slug"]}" data-cat="{r.get("typo","")}">
<div class="ref-visual">{visual(r, r["slug"][:4], p)}<span class="status {st}">{r["status"]}</span></div>
<div class="ref-body"><span class="loc">{r["loc"]}</span><h3>{r["name"]}</h3><p>{r["typ"]}</p>{ph}<div class="ref-facts">{facts}</div></div></a>'''

def post_card(x, base, kind):
    cat = x["cat"] if kind == "blog" else x["catl"]
    cls = "" if kind == "blog" else (" jur" if x["cat"] == "jur" else (" tech" if x["cat"] == "tech" else ""))
    title = x["title"] if kind == "blog" else x["short"]
    dc = f' data-cat="{x["cat"]}"' if kind == "actu" else (f' data-cat="{x["ref"]}"' if kind == "blog" else "")
    th = ""
    if kind == "blog" and (x.get("img") or photo(x["ref"])):
        pre = base.split("blog/")[0] if base else "../"
        u = f'{pre}assets/img/blog/{x["img"]}-800.webp' if x.get("img") else f'{pre}assets/img/references/{x["ref"]}-800.webp'
        th = f'<div class="post-thumb"><img src="{u}" alt="" loading="lazy" width="800" height="500"></div>'
    return f'''<a class="post reveal{" has-thumb" if th else ""}" href="{base}{x["slug"]}.html"{dc}>{th}<div class="meta"><span class="cat{cls}">{cat}</span><time datetime="{x["date"]}">{fdate(x["date"])}</time></div><h3>{title}</h3><p>{x["desc"]}</p><span class="link-arrow more">Lire</span></a>'''

BLOG.sort(key=lambda x: x["date"], reverse=True)
ACTU.sort(key=lambda x: x["date"], reverse=True)

# ======================= ACCUEIL =======================
gantt_rows = [("Gros œuvre", 0, 34, "done"), ("Charpente · couverture", 30, 18, "done"), ("Menuiseries ext.", 38, 14, "done"),
              ("Cloisons · doublages", 46, 22, "live"), ("Fluides · électricité", 40, 40, "live"), ("Chapes · carrelage", 60, 18, ""),
              ("Peinture · finitions", 72, 18, ""), ("Réception", 93, 0, "ms")]
grows = "".join(f'<div class="g-row"><span>{n}</span><div class="g-track"><i class="g-bar {c}" style="left:{l}%;width:{w}%;animation-delay:{i*0.12:.2f}s"><i></i></i></div></div>' for i, (n, l, w, c) in enumerate(gantt_rows))
months = "".join(f"<span>{m}</span>" for m in ["J","F","M","A","M","J","J","A","S","O","N","D"])
met_cards = "".join(f'''<a class="card reveal" href="{{P}}{h}"><span class="go">{icon("arrow")}</span><span class="ico">{icon(ic)}</span><span class="num">0{i+1}</span><h3>{t}</h3><p>{d}</p></a>''' for i, (h, ic, t, d) in enumerate(METIERS))
steps = [("01","Conception","Faisabilité, esquisses, APD, autorisations"),("02","Consultation","DCE, CCTP, analyse des offres, marchés"),
         ("03","Préparation","Visas EXE, planning TCE, installation de chantier"),("04","Exécution","DET, OPC, réunions et comptes rendus hebdomadaires"),
         ("05","Réception","OPR, procès-verbaux, levée des réserves, DOE"),("06","Après livraison","Parfait achèvement, suivi des garanties")]
steps_h = "".join(f'<div class="step reveal"><div class="dot">{n}</div><small>Étape {n}</small><h4>{t}</h4><p>{d}</p></div>' for n, t, d in steps)
home = f'''
<section class="hero"><div class="wrap">
 <div class="hero-grid">
  <div>
   <span class="eyebrow">Maître d'œuvre d'exécution et OPC · Alpes</span>
   <h1>Vos chantiers, pilotés du plan à la <em>réception</em></h1>
   <p class="lead">TEC assure la maîtrise d'œuvre d'exécution, l'OPC et l'économie de la construction de vos opérations de logements et d'immobilier d'entreprise, en Isère, Savoie, Haute-Savoie et Hautes-Alpes.</p>
   <div class="hero-actions"><a class="btn btn--red" href="{{P}}contact.html">Confier une mission {icon("arrow")}</a><a class="btn btn--ghost-l" href="{{P}}references.html">Voir nos chantiers</a></div>
   <div class="hero-meta"><span>Maîtrise d'œuvre d'exécution</span><span>OPC</span><span>Suivi de chantier</span><span>Économie de la construction</span></div>
  </div>
  <div class="gantt" aria-hidden="true">
   <div class="gantt-top"><div><b>Planning TCE — Résidence R+3</b><br><small>Mise à jour hebdomadaire · CR n°63</small></div><span class="pill">Chantier en cours</span></div>
   <div class="g-scale"><span></span>{months}</div>
   <div class="g-rows">{grows}<div class="g-today"></div></div>
   <div class="g-foot"><div><b>22</b><small>lots coordonnés</small></div><div><b>1/sem.</b><small>réunion de chantier</small></div><div><b>48 h</b><small>diffusion du CR</small></div></div>
  </div>
 </div>
 <div class="strip"><span>Logements · Tertiaire · Industrie · Réhabilitation</span><ul><li>Isère</li><li>Savoie</li><li>Haute-Savoie</li><li>Hautes-Alpes</li></ul></div>
</div></section>

<section class="section"><div class="wrap">
 <div class="head"><div><span class="eyebrow">Nos métiers</span><h2>Une ingénierie de chantier complète, un seul interlocuteur</h2></div>
 <p class="lead">De la faisabilité à la levée des réserves, nous réunissons les compétences qui font tenir un projet : la conception, l'exécution, le temps et le coût.</p></div>
 <div class="grid-5">{met_cards}</div>
</div></section>

<section class="section--tight section--white"><div class="wrap">
 <div class="stats reveal">
  <div class="stat"><b>96</b><span>logements en cours de pilotage d'exécution</span></div>
  <div class="stat"><b>90<sup>+</sup></b><span>réunions et comptes rendus de chantier depuis 2025</span></div>
  <div class="stat"><b>22</b><span>lots séparés coordonnés sur une même opération</span></div>
  <div class="stat"><b>4</b><span>départements alpins couverts : 38, 73, 74, 05</span></div>
 </div>
</div></section>

<section class="section section--ink"><div class="wrap">
 <div class="head"><div><span class="eyebrow">Notre méthode</span><h2>Six étapes, une même exigence de rigueur</h2></div>
 <p class="lead">Notre force : la continuité. L'équipe qui prépare le dossier de consultation est celle qui pilote le chantier et réceptionne les ouvrages.</p></div>
 <div class="steps">{steps_h}</div>
</div></section>

<section class="section section--white"><div class="wrap split split--top">
 <div class="reveal"><span class="eyebrow">Notre vision</span><h2>La maîtrise, du premier trait au dernier PV</h2></div>
 <div class="prose reveal"><p>Un projet de construction se joue rarement sur une grande décision. Il se gagne, ou se perd, sur des centaines de petits arbitrages : une réservation oubliée, un plan d'exécution visé trop tard, une situation validée sans contrôle, une interface entre deux lots que personne n'a anticipée.</p>
 <p>TEC est né de cette conviction. Notre métier est d'apporter au maître d'ouvrage <strong>la rigueur technique et la lucidité économique</strong> qui sécurisent chaque étape : un planning qui fait autorité, des comptes rendus qui engagent, des coûts suivis à l'euro près et une réception préparée dès le premier jour.</p>
 <blockquote>Piloter, c'est anticiper. Nous voulons que nos clients n'apprennent jamais une mauvaise nouvelle de chantier trop tard.</blockquote></div>
</div></section>

<section class="section"><div class="wrap">
 <div class="head"><div><span class="eyebrow">Références</span><h2>Des chantiers pilotés, de la Maurienne à l'Embrunais</h2></div>
 <div><p class="lead">Logements collectifs, programmes mixtes, rénovation industrielle et tertiaire : découvrez les opérations que nous pilotons.</p><p><a class="link-arrow" href="{{P}}references.html">Toutes les références</a></p></div></div>
 <div class="refs">{"".join(ref_card(REF[s]) for s in ["element-embrun","jardins-de-babylone","mti-claix"])}</div>
</div></section>

<section class="section section--white"><div class="wrap split">
 <div class="reveal"><span class="eyebrow">Pourquoi TEC</span><h2>La rigueur d'un pilote, l'œil d'un économiste</h2>
 <p class="lead">TEC est un bureau d'études spécialisé dans l'exécution et l'économie de la construction. Nous ne concevons pas des chantiers sur le papier : nous les faisons aboutir, au prix et au délai convenus, aux côtés du maître d'ouvrage.</p>
 <ul class="checks"><li>Une présence terrain hebdomadaire et des comptes rendus qui engagent.</li><li>Un planning tous corps d'état vivant, mis à jour chaque semaine.</li><li>Un contrôle financier rigoureux des situations et des avenants.</li><li>Une connaissance fine des entreprises et des contraintes de montagne.</li></ul>
 <p class="mt-2"><a class="btn btn--navy" href="{{P}}agence.html">Découvrir l'agence {icon("arrow")}</a></p></div>
 <div class="engage reveal">
  <div>{icon("clock")}<b>Délais tenus</b><span>Planning contractualisé, chemin critique suivi, alertes précoces.</span></div>
  <div>{icon("euro")}<b>Budget maîtrisé</b><span>Situations validées chaque mois, travaux modificatifs chiffrés avant exécution.</span></div>
  <div>{icon("shield")}<b>Qualité contrôlée</b><span>Visas EXE, autocontrôles, essais et réceptions de supports.</span></div>
  <div>{icon("doc")}<b>Traçabilité</b><span>Comptes rendus, indices de plans, PV et DOE archivés.</span></div>
 </div>
</div></section>

<section class="section"><div class="wrap">
 <div class="head"><div><span class="eyebrow">Blog chantiers</span><h2>Nouvelles du terrain</h2></div><div><p class="lead">L'avancement de nos chantiers, raconté par ceux qui les pilotent.</p><p><a class="link-arrow" href="{{P}}blog/index.html">Tout le blog</a></p></div></div>
 <div class="posts">{"".join(post_card(x, "{P}blog/", "blog") for x in BLOG[:3])}</div>
</div></section>

<section class="section section--white"><div class="wrap">
 <div class="head"><div><span class="eyebrow">Actualités juridiques &amp; techniques</span><h2>Ce qui change en 2026</h2></div><div><p class="lead">RE2020, facturation électronique, urbanisme, déchets de chantier : notre veille réglementaire, sourcée et décryptée.</p><p><a class="link-arrow" href="{{P}}actualites/index.html">Toutes les actualités</a></p></div></div>
 <div class="posts">{"".join(post_card(x, "{P}actualites/", "actu") for x in ACTU[:3])}</div>
</div></section>

<section class="section--tight"><div class="wrap"><div class="split reveal">
 <div class="plaquette"><div class="thumb"><img src="{{P}}assets/img/plaquette-cover.png" alt="Couverture de la plaquette TEC" width="150" height="212" loading="lazy"></div>
 <div><span class="eyebrow">Plaquette</span><h3 style="font-size:clamp(26px,2.6vw,36px)">Nos métiers en quatre pages</h3><p class="lead">Missions, méthode, engagements et références : la plaquette TEC à télécharger et à partager.</p><a class="btn btn--navy" href="{{P}}{PDF}" download>{icon("down")}Télécharger la plaquette (PDF)</a></div></div>
 <div><span class="eyebrow">Zone d'intervention</span><h3>Grenoble et l'arc alpin</h3><p>Depuis notre bureau grenoblois, nous intervenons dans la métropole, le Grésivaudan, l'Oisans, la Maurienne, le Chablais, le Champsaur et l'Embrunais.</p><div class="tag-list"><span class="tag">Isère (38)</span><span class="tag">Savoie (73)</span><span class="tag">Haute-Savoie (74)</span><span class="tag">Hautes-Alpes (05)</span></div></div>
</div></div></section>
{cta_band()}
'''
pages.append(page("index.html", "TEC — Maîtrise d'œuvre d'exécution et OPC à Grenoble",
  "Bureau d'ingénierie de chantier à Grenoble : maîtrise d'œuvre d'exécution, OPC, suivi de chantier, économie de la construction. Isère, Savoie, Hautes-Alpes.",
  home, ld=[{"@context":"https://schema.org","@type":"WebSite","@id":SITE+"/#site","url":SITE+"/","name":"TEC — Pilotage & Ingénierie","inLanguage":"fr-FR","publisher":{"@id":SITE+"/#organisation"}}]))

# ======================= MÉTIERS (hub) =======================
hub = page_hero([("Accueil","index.html"),("Nos métiers","nos-metiers.html")], "Nos métiers", "Une ingénierie de chantier complète",
  "Conception, maîtrise d'œuvre d'exécution, suivi de chantier, OPC et économie de la construction : cinq expertises complémentaires portées par une même équipe.")
hub += f'''<section class="section"><div class="wrap"><div class="grid-5">{met_cards}</div></div></section>
<section class="section section--white"><div class="wrap split split--top">
<div><span class="eyebrow">Missions à la carte ou complètes</span><h2>Une mission adaptée à chaque maître d'ouvrage</h2></div>
<div class="prose"><p>Promoteurs, bailleurs, collectivités, entreprises : nos missions se combinent selon votre organisation. Vous disposez d'un architecte et d'une équipe de conception ? Nous assurons la maîtrise d'œuvre d'exécution et l'OPC. Vous démarrez un projet ? Nous vous accompagnons dès la faisabilité, en assistance à maîtrise d'ouvrage.</p>
<table><thead><tr><th>Votre besoin</th><th>Notre mission</th></tr></thead><tbody>
<tr><td>Étudier un terrain, chiffrer un programme</td><td>Faisabilité, AMO, estimation</td></tr>
<tr><td>Consulter les entreprises</td><td>DCE, CCTP, analyse des offres (ACT)</td></tr>
<tr><td>Diriger les travaux</td><td>Maîtrise d'œuvre d'exécution (VISA, DET)</td></tr>
<tr><td>Tenir les délais en lots séparés</td><td>OPC</td></tr>
<tr><td>Réceptionner et livrer</td><td>AOR, levée des réserves, DOE</td></tr></tbody></table></div>
</div></section>{cta_band()}'''
pages.append(page("nos-metiers.html", "Nos métiers : MOE d'exécution, OPC, suivi de chantier | TEC",
  "Conception, maîtrise d'œuvre d'exécution, suivi de chantier, OPC et économie de la construction : les métiers de TEC pour vos opérations alpines.",
  hub, crumbs=[("Accueil",""),("Nos métiers","nos-metiers.html")]))

# ======================= PAGES SERVICES =======================
for path, s in SERVICES.items():
    name = [t for h, ic, t, d in METIERS if h == path][0]
    b = page_hero([("Accueil","index.html"),("Nos métiers","nos-metiers.html"),(s["eyebrow"],path)], s["eyebrow"], s["h1"], s["lead"],
        f'<div class="hero-actions mt-2"><a class="btn btn--red" href="{{P}}contact.html">Demander une proposition {icon("arrow")}</a></div>')
    checks = "".join(f"<li>{c}</li>" for c in s["checks"])
    phases = "".join(f'<div class="phase reveal"><span class="code">{c}</span><div><h3>{t}</h3><p>{d}</p></div></div>' for c, t, d in s["phases"])
    others = "".join(f'<li><a href="{{P}}{h}">{t}</a></li>' for h, ic, t, d in METIERS if h != path)
    b += f'''<section class="section"><div class="wrap layout">
<div>
 <div class="prose">{s["intro"]}</div>
 <div class="callout red mt-2"><h3>Ce que comprend la mission</h3><ul class="checks">{checks}</ul></div>
 <h2 class="mt-3">Les étapes</h2>
 <div class="phases">{phases}</div>
 <h2 class="mt-3">Questions fréquentes</h2>
 {faq_html(s["faq"])}
</div>
<aside class="aside">
 <div class="box box--ink"><h4>Un projet à confier ?</h4><p>Décrivez-nous votre opération : nous revenons vers vous sous 48 heures ouvrées.</p><a class="btn btn--red" href="{{P}}contact.html">Nous consulter</a></div>
 <div class="box"><h4>Nos autres métiers</h4><ul>{others}</ul></div>
 <div class="box"><h4>Plaquette</h4><p class="note">Toutes nos missions en 4 pages.</p><a class="link-arrow" href="{{P}}{PDF}" download>Télécharger le PDF</a></div>
</aside>
</div></section>
<section class="section section--white"><div class="wrap"><div class="head"><div><span class="eyebrow">Références</span><h2>Exemples de chantiers</h2></div><p class="lead"><a class="link-arrow" href="{{P}}references.html">Toutes nos références</a></p></div>
<div class="refs">{"".join(ref_card(REF[r]) for r in s["refs"])}</div></div></section>
{cta_band()}'''
    ld = [faq_ld(s["faq"]), {"@context":"https://schema.org","@type":"Service","name":name,"serviceType":s["eyebrow"],"provider":{"@id":SITE+"/#organisation"},"areaServed":["Isère","Savoie","Haute-Savoie","Hautes-Alpes"],"description":s["desc"],"url":SITE+"/"+path}]
    pages.append(page(path, s["title"], s["desc"], b, ld=ld, crumbs=[("Accueil",""),("Nos métiers","nos-metiers.html"),(s["eyebrow"],path)]))

# ======================= RÉFÉRENCES =======================
b = page_hero([("Accueil","index.html"),("Références","references.html")], "Références chantiers", "Nos références",
  "Logements collectifs, programme mixte en accession sociale, bâtiments industriels et tertiaires en site occupé, réhabilitation : les opérations pilotées par TEC.")
det = ""
for r in REFS:
    posts = [x for x in BLOG if x["ref"] == r["slug"]]
    pl = "".join(f'<li><a href="{{P}}blog/{x["slug"]}.html">{x["title"]}</a></li>' for x in posts)
    pl = f'<h4 class="mt-2">Sur le blog</h4><ul>{pl}</ul>' if pl else ""
    dl = "".join(f"<dt>{k}</dt><dd>{v}</dd>" for k, v in [("Programme", r["typ"]), ("Maître d'ouvrage", r["mo"]), ("Maîtrise d'œuvre", r["archi"]) if r["archi"] != "—" else (None, None), ("Mission TEC", r["mission"]), ("Lots", r["lots"]), ("Calendrier", r["dates"])] if k)
    det += f'''<article class="ref-detail" id="{r["slug"]}" data-cat="{r.get("typo","")}">
<div class="ref-visual reveal">{visual(r, r["slug"][:4]+"d")}<span class="status{"" if r["status"]=="Livré" else " wip"}">{r["status"]}</span></div>
<div class="reveal"><span class="eyebrow">{r["loc"]}</span><h2>{r["name"]}</h2><p class="lead">{r["text"]}</p><dl class="kv">{dl}</dl>
<div class="tag-list mt-2">{"".join(f'<span class="tag">{f}</span>' for f in r["facts"])}</div>{pl}</div>
</article>'''
filt = '<div class="filters" role="group" aria-label="Filtrer par typologie"><button data-f="all" aria-pressed="true">Toutes</button><button data-f="logement" aria-pressed="false">Logements</button><button data-f="industrie" aria-pressed="false">Industrie &amp; tertiaire</button><button data-f="rehab" aria-pressed="false">Réhabilitation</button></div>'
b += f'''<section class="section"><div class="wrap">{filt}{det}
<p class="note mt-2">Perspectives non contractuelles et illustrations schématiques.</p></div></section>
<section class="section section--ink"><div class="wrap split">
<div><span class="eyebrow">Nos typologies</span><h2>Du collectif de montagne au bâtiment d'activité</h2><p class="lead">Nos chantiers couvrent des contextes très différents : résidences en altitude soumises aux intempéries, programmes en accession sociale au calendrier contraint, sites industriels qui ne peuvent pas s'arrêter, bâtis anciens à réhabiliter.</p></div>
<div><ul class="checks"><li><b>Logements collectifs</b> en accession libre et sociale</li><li><b>Programmes mixtes</b> collectif et individuel</li><li><b>Industrie et tertiaire</b>, y compris en site occupé, pour des contractants généraux</li><li><b>Réhabilitation</b> de bâtis existants</li></ul></div>
</div></section>{cta_band()}'''
pages.append(page("references.html", "Références chantiers en Isère, Savoie, Hautes-Alpes | TEC",
  "Élément à Embrun, Les Jardins de Babylone, Horizon Belledonne, MTI, SiPearl, AD Santé et Soliha pour CGBI : les opérations pilotées par TEC.",
  b, current="references.html", crumbs=[("Accueil",""),("Références","references.html")]))

# ======================= AGENCE =======================
team = [("BC","Benjamin Camerino","Directeur général","Associé fondateur de TEC, il dirige l'agence et porte ses engagements auprès des maîtres d'ouvrage. Il apporte une solide culture de la conception-réalisation et de l'immobilier d'entreprise."),
        ("DD","David Durigon","Responsable technique","Il conduit la maîtrise d'œuvre d'exécution et l'OPC des chantiers : réunions hebdomadaires, comptes rendus, visas, situations de travaux et coordination des entreprises."),
        ("SO","Sandra Olandese","Cheffe de projet conception","Elle pilote les études de conception : faisabilité, plans, dossiers d'autorisation et coordination avec les architectes et bureaux d'études.")]
th = "".join(f'<article class="member reveal"><div class="avatar" aria-hidden="true">{i}</div><span class="role">{r}</span><h3>{n}</h3><p>{d}</p></article>' for i, n, r, d in team)
b = page_hero([("Accueil","index.html"),("L'agence","agence.html")], "L'agence", "Technique et Économie de la Construction",
  "TEC est un bureau d'études d'exécution et d'économie de la construction : une équipe resserrée, basée à Grenoble, qui pilote des opérations de logements et d'immobilier d'entreprise dans tout l'arc alpin.")
b += f'''<section class="section"><div class="wrap split split--top">
<div class="reveal"><span class="eyebrow">Notre histoire</span><h2>Née du terrain, en 2025</h2></div>
<div class="prose reveal"><p>TEC — Technique et Économie de la Construction — a été créée à Grenoble en mars 2025 par des professionnels de la promotion et de la construction, autour de <strong>Benjamin Camerino</strong>. Son ambition : offrir aux maîtres d'ouvrage un interlocuteur unique pour l'exécution, le pilotage et l'économie de leurs chantiers.</p>
<p>Le nom dit l'essentiel : la <strong>technique</strong>, pour que l'ouvrage soit conforme et durable ; l'<strong>économie</strong>, pour que le budget soit tenu. Deux exigences que nous appliquons à chaque opération, du collectif de montagne au bâtiment industriel en site occupé.</p>
<blockquote>Un chantier réussi se prépare dès la conception et se gagne chaque semaine sur le terrain.</blockquote></div>
</div></section>
<section class="section section--white"><div class="wrap">
<div class="head"><div><span class="eyebrow">L'équipe</span><h2>Des interlocuteurs directs</h2></div><p class="lead">Pas d'intermédiaire : les personnes qui vous répondent sont celles qui pilotent votre opération.</p></div>
<div class="team">{th}</div></div></section>
<section class="section section--ink"><div class="wrap split">
<div><span class="eyebrow">Nos valeurs</span><h2>Rigueur, transparence, engagement</h2><p class="lead">Être à l'écoute, être force de proposition et informer chaque partie prenante, chaque semaine. Sur un chantier, communiquer, c'est anticiper.</p>
<div class="zone"><span>Grenoble</span><span>Grésivaudan</span><span>Oisans</span><span>Maurienne</span><span>Chablais</span><span>Champsaur</span><span>Embrunais</span></div></div>
<div><ul class="checks"><li><b>Transparence :</b> des comptes rendus clairs et des chiffres partagés.</li><li><b>Réactivité :</b> des décisions prises en direct, sans circuit inutile.</li><li><b>Exigence :</b> qualité, sécurité et propreté sur chaque chantier.</li><li><b>Respect :</b> des entreprises, des riverains et des futurs occupants.</li></ul></div>
</div></section>
<section class="section"><div class="wrap split split--top">
<div class="reveal"><span class="eyebrow">Nous rejoindre</span><h2>Conducteurs de travaux, pilotes OPC, économistes</h2></div>
<div class="prose reveal"><p>TEC se développe et accueille des profils qui aiment le terrain et la rigueur : conducteurs de travaux, pilotes OPC, économistes de la construction, chargés d'études. Vous partagez notre exigence ? Envoyez-nous votre candidature spontanée.</p>
<p><a class="btn btn--navy" href="mailto:{EMAIL}?subject=Candidature%20spontan%C3%A9e">{icon("mail")}Candidature spontanée</a></p></div>
</div></section>{cta_band()}'''
pages.append(page("agence.html", "L'agence TEC à Grenoble : équipe, histoire, valeurs",
  "TEC, bureau d'études d'exécution et d'économie de la construction à Grenoble. L'équipe : Benjamin Camerino, David Durigon, Sandra Olandese.",
  b, current="agence.html", crumbs=[("Accueil",""),("L'agence","agence.html")]))

# ======================= BLOG & ACTUALITÉS =======================
def listing(kind, items, path, title, desc, h1, lead, eyebrow):
    base = ""
    if kind == "blog":
        cats = [("all","Tous")] + [(r["slug"], r["name"]) for r in REFS if any(x["ref"] == r["slug"] for x in items)]
    else:
        cats = [("all","Toutes"),("jur","Juridique"),("tech","Technique"),("guide","Guides")]
    f = "".join(f'<button data-f="{k}" aria-pressed="{"true" if k=="all" else "false"}">{n}</button>' for k, n in cats)
    b = page_hero([("Accueil","index.html"),(eyebrow, path)], eyebrow, h1, lead)
    b += f'<section class="section"><div class="wrap"><div class="filters" role="group" aria-label="Filtrer">{f}</div><div class="posts">{"".join(post_card(x, base, kind) for x in items)}</div></div></section>{cta_band()}'
    ld = [{"@context":"https://schema.org","@type":"Blog" if kind=="blog" else "CollectionPage","name":h1,"url":SITE+"/"+path,"publisher":{"@id":SITE+"/#organisation"}}]
    pages.append(page(path, title, desc, b, current=kind if kind=="blog" else "actualites", ld=ld, crumbs=[("Accueil",""),(eyebrow, path)]))

listing("blog", BLOG, "blog/index.html", "Blog chantiers : l'avancement de nos opérations | TEC",
  "L'avancement des chantiers pilotés par TEC : Élément à Embrun, Les Jardins de Babylone, Horizon Belledonne, chantiers CGBI.",
  "Le blog de nos chantiers", "Comptes rendus, étapes clés, méthodes : l'actualité des opérations que nous pilotons, racontée depuis le terrain.", "Blog chantiers")
listing("actu", ACTU, "actualites/index.html", "Actualités juridiques et techniques du bâtiment 2026 | TEC",
  "RE2020, facturation électronique, loi Huwart, loi SVE, DPE, REP PMCB, EPBD : la veille réglementaire 2026 de TEC, sourcée et décryptée.",
  "Actualités juridiques &amp; techniques", "Notre veille réglementaire pour les maîtres d'ouvrage et les entreprises : ce qui change, et ce que cela implique concrètement sur vos opérations.", "Actualités")

def cut(t, n=58):
    return t if len(t) <= n else t[:n].rsplit(" ", 1)[0] + "…"

def article(kind, x, items):
    folder = "blog" if kind == "blog" else "actualites"
    path = f"{folder}/{x['slug']}.html"
    sec = "Blog chantiers" if kind == "blog" else "Actualités"
    cat = x["cat"] if kind == "blog" else x["catl"]
    meta = f'<div class="meta"><span>{cat}</span><span>·</span><time datetime="{x["date"]}">Publié le {fdate(x["date"])}</time><span>·</span><span>Par l\'équipe TEC</span></div>'
    b = page_hero([("Accueil","index.html"),(sec, f"{folder}/index.html"),(cut(x.get("short", x["title"])), path)], cat, x["title"], x["desc"], meta)
    src = ""
    if x.get("sources"):
        src = '<div class="sources"><h2>Sources</h2><ol>' + "".join(f'<li><a href="{u}" rel="noopener" target="_blank">{t}</a></li>' for t, u in x["sources"]) + '</ol><p class="note">Article d\'information générale rédigé à partir des sources citées ; il ne constitue pas un conseil juridique. Vérifiez les textes applicables à votre opération.</p></div>'
    fig = ""
    if kind == "blog" and x.get("img"):
        u = f'{{P}}assets/img/blog/{x["img"]}'
        fig = (f'<figure class="art-fig"><img src="{u}-800.webp" srcset="{u}-800.webp 800w, {u}.webp 1600w" sizes="(max-width: 900px) 100vw, 60vw" '
               f'alt="{x["cap"]}" width="1600" height="1000"><figcaption>{x["cap"]}</figcaption></figure>')
    elif kind == "blog" and photo(x["ref"]):
        rr = REF[x["ref"]]
        fig = f'<figure class="art-fig">{visual(rr, "f", "{P}", eager=True)}<figcaption>{rr["name"]}, {rr["loc"].split(" · ")[0]} — perspective non contractuelle</figcaption></figure>'
    others = [y for y in items if y["slug"] != x["slug"]][:4]
    ol = "".join(f'<li><a href="{y["slug"]}.html">{y.get("short", y["title"])}</a></li>' for y in others)
    side_ref = ""
    if kind == "blog":
        r = REF[x["ref"]]
        side_ref = f'<div class="box"><h4>{r["name"]}</h4><dl class="kv"><dt>Lieu</dt><dd>{r["loc"].split(" · ")[0]}</dd><dt>Programme</dt><dd>{r["typ"]}</dd><dt>Mission</dt><dd>{r["mission"]}</dd></dl><p class="mt-2"><a class="link-arrow" href="{{P}}references.html#{r["slug"]}">Fiche référence</a></p></div>'
    b += f'''<section class="section"><div class="wrap layout">
<article class="prose">{fig}{x["body"]}{src}</article>
<aside class="aside">{side_ref}
<div class="box"><h4>À lire aussi</h4><ul>{ol}</ul></div>
<div class="box box--ink"><h4>Besoin d'un pilote pour votre chantier ?</h4><p>Maîtrise d'œuvre d'exécution, OPC, économie : parlons de votre opération.</p><a class="btn btn--red" href="{{P}}contact.html">Nous consulter</a></div>
</aside></div></section>'''
    ld = [{"@context":"https://schema.org","@type":"BlogPosting" if kind=="blog" else "NewsArticle","headline":x["title"][:110],"description":x["desc"],"datePublished":x["date"],"dateModified":x["date"],"inLanguage":"fr-FR","mainEntityOfPage":SITE+"/"+path,"image":(SITE+f"/assets/img/blog/{x['img']}.webp" if x.get("img") else SITE+f"/assets/img/references/{x['ref']}.webp" if kind=="blog" and photo(x.get("ref","")) else SITE+"/assets/img/og-tec.png"),"author":{"@type":"Organization","name":"TEC — Pilotage & Ingénierie","url":SITE+"/"},"publisher":{"@id":SITE+"/#organisation"},
           **({"citation":[u for t,u in x["sources"]]} if x.get("sources") else {})}]
    pages.append(page(path, (x.get("short") or x["title"]) + " | TEC", x["desc"], b, current=kind if kind=="blog" else "actualites", ld=ld, og_type="article",
                      crumbs=[("Accueil",""),(sec, f"{folder}/index.html"),(x.get("short", x["title"]), path)]))
for x in BLOG: article("blog", x, BLOG)
for x in ACTU: article("actu", x, ACTU)

# ======================= CONTACT =======================
b = page_hero([("Accueil","index.html"),("Contact","contact.html")], "Contact", "Parlons de votre opération",
  "Une mission de maîtrise d'œuvre d'exécution, d'OPC, d'économie de la construction ou d'accompagnement à la conception ? Décrivez-nous votre projet.")
b += f'''<section class="section"><div class="wrap contact-grid">
<div><h2>Nos coordonnées</h2><p class="lead">Nous vous répondons sous 48 heures ouvrées.</p>
<div class="coords">
<a href="tel:{PHONE_INTL}"><span class="i">{icon("phone")}</span><span><small>Téléphone</small><b>{PHONE}</b></span></a>
<a href="mailto:{EMAIL}"><span class="i">{icon("mail")}</span><span><small>E-mail</small><b>{EMAIL}</b></span></a>
<a href="https://www.openstreetmap.org/search?query=163%20cours%20de%20la%20Lib%C3%A9ration%20Grenoble" rel="noopener" target="_blank"><span class="i">{icon("pin")}</span><span><small>Adresse</small><b>{ADDR["bldg"]}, {ADDR["street"]}, {ADDR["zip"]} {ADDR["city"]}</b></span></a>
<div><span class="i">{icon("clock")}</span><span><small>Horaires</small><b>Du lundi au vendredi, 8 h 30 – 18 h 30</b></span></div>
</div>
<div class="plaquette mt-3"><div class="thumb"><img src="{{P}}assets/img/plaquette-cover.png" alt="Plaquette TEC" width="150" height="212" loading="lazy"></div><div><h3>La plaquette TEC</h3><p>Nos métiers, notre méthode et nos références.</p><a class="btn btn--navy" href="{{P}}{PDF}" download>{icon("down")}Télécharger</a></div></div>
</div>
<form class="form" action="contact.php" method="post">
<h2>Votre demande</h2>
<div class="row"><label>Nom et prénom *<input name="nom" required autocomplete="name"></label><label>Société / organisme<input name="societe" autocomplete="organization"></label></div>
<div class="row"><label>E-mail *<input type="email" name="email" required autocomplete="email"></label><label>Téléphone<input type="tel" name="tel" autocomplete="tel"></label></div>
<div class="row"><label>Vous êtes<select name="profil"><option>Promoteur / maître d'ouvrage privé</option><option>Collectivité / maître d'ouvrage public</option><option>Bailleur social</option><option>Entreprise (immobilier d'entreprise)</option><option>Architecte / bureau d'études</option><option>Entreprise de travaux</option><option>Autre</option></select></label>
<label>Mission envisagée<select name="mission"><option>Maîtrise d'œuvre d'exécution</option><option>OPC</option><option>Suivi de chantier</option><option>Économie de la construction / AMO</option><option>Conception</option><option>Mission complète</option><option>Autre / je ne sais pas</option></select></label></div>
<label>Votre projet *<textarea name="message" required placeholder="Localisation, nature de l'opération, surface ou nombre de logements, calendrier…"></textarea></label>
<label class="hp" aria-hidden="true">Ne pas remplir<input name="site_web" tabindex="-1" autocomplete="off"></label>
<label class="consent"><input type="checkbox" name="rgpd" required><span>J'accepte que mes données soient utilisées par TEC pour traiter ma demande, conformément à la <a href="{{P}}confidentialite.html">politique de confidentialité</a>.</span></label>
<div><button class="btn btn--red" type="submit">Envoyer ma demande {icon("arrow")}</button></div>
</form>
</div></section>'''
pages.append(page("contact.html", "Contact — TEC Pilotage & Ingénierie, Grenoble", "Contactez TEC pour une mission de maîtrise d'œuvre d'exécution, d'OPC, de suivi de chantier ou d'économie de la construction. Immeuble Équinoxe, Grenoble.",
  b, current="contact.html", crumbs=[("Accueil",""),("Contact","contact.html")],
  ld=[{"@context":"https://schema.org","@type":"ContactPage","url":SITE+"/contact.html","about":{"@id":SITE+"/#organisation"}}]))

b = page_hero([("Accueil","index.html"),("Merci","merci.html")], "Message envoyé", "Merci, votre demande est bien partie", "Nous revenons vers vous sous 48 heures ouvrées. En attendant, découvrez nos chantiers en cours.",
  f'<div class="hero-actions mt-2"><a class="btn btn--red" href="{{P}}references.html">Nos références</a><a class="btn btn--ghost-l" href="{{P}}index.html">Retour à l\'accueil</a></div>')
pages.append(page("merci.html", "Merci — TEC Pilotage & Ingénierie", "Votre message a bien été envoyé à TEC.", b, extra_head='<meta name="robots" content="noindex">\n'))

# ======================= LÉGAL =======================
b = page_hero([("Accueil","index.html"),("Mentions légales","mentions-legales.html")], "Informations légales", "Mentions légales", "Conformément à l'article 6 de la loi n° 2004-575 du 21 juin 2004 pour la confiance dans l'économie numérique.")
b += f'''<section class="section"><div class="wrap prose">
<h2>Éditeur du site</h2>
<p><strong>TECHNIQUE ET ÉCONOMIE DE LA CONSTRUCTION</strong> (sigle et nom commercial : TEC)<br>Société par actions simplifiée au capital de 5 000 €<br>Siège social : 163 cours de la Libération et du Général de Gaulle, 38100 Grenoble<br>RCS Grenoble 941 810 749 — EUID FR3801.941810749<br>N° de TVA intracommunautaire : FR60941810749<br>Téléphone : {PHONE} — E-mail : <a href="mailto:{EMAIL}">{EMAIL}</a></p>
<h2>Directeur de la publication</h2>
<p>M. Stéphane JOUGLARD.</p>
<h2>Hébergement</h2>
<p>OVH SAS — 2 rue Kellermann, 59100 Roubaix, France — <a href="https://www.ovhcloud.com" rel="noopener">www.ovhcloud.com</a></p>
<h2>Propriété intellectuelle</h2>
<p>L'ensemble des contenus de ce site (textes, logotypes, illustrations, plaquette) est la propriété de TEC, sauf mention contraire. Toute reproduction, totale ou partielle, sans autorisation écrite préalable est interdite. Les marques et logos des partenaires cités restent la propriété de leurs titulaires. Les polices de caractères Archivo et Inter Tight sont distribuées sous licence SIL Open Font License.</p>
<h2>Contenus d'information</h2>
<p>Les articles de la rubrique Actualités sont fournis à titre d'information générale, à partir des sources publiques citées dans chaque article, et ne constituent pas un conseil juridique ou technique. Les illustrations des références sont schématiques et non contractuelles.</p>
<h2>Liens</h2>
<p>Le site peut contenir des liens vers des sites tiers, dont TEC ne maîtrise pas le contenu et n'assume pas la responsabilité.</p>
<h2>Données personnelles</h2>
<p>Voir notre <a href="{{P}}confidentialite.html">politique de confidentialité</a>.</p>
</div></section>'''
pages.append(page("mentions-legales.html", "Mentions légales — TEC Pilotage & Ingénierie", "Mentions légales du site le-tec.fr : éditeur, directeur de la publication, hébergeur.", b, crumbs=[("Accueil",""),("Mentions légales","mentions-legales.html")]))

b = page_hero([("Accueil","index.html"),("Confidentialité","confidentialite.html")], "Données personnelles", "Politique de confidentialité", "Comment TEC traite les données que vous lui confiez via ce site.")
b += f'''<section class="section"><div class="wrap prose">
<h2>Responsable du traitement</h2><p>TECHNIQUE ET ÉCONOMIE DE LA CONSTRUCTION (TEC), 163 cours de la Libération et du Général de Gaulle, 38100 Grenoble — <a href="mailto:{EMAIL}">{EMAIL}</a>.</p>
<h2>Données collectées et finalités</h2><p>Le formulaire de contact collecte vos nom, société, coordonnées, profil et message, dans le seul but de répondre à votre demande et, le cas échéant, d'établir une proposition commerciale. Base légale : votre consentement et nos mesures précontractuelles.</p>
<h2>Durée de conservation</h2><p>Les demandes sans suite sont conservées au maximum trois ans à compter du dernier contact. Les données liées à un contrat sont conservées pendant la durée légale applicable.</p>
<h2>Destinataires</h2><p>Les données sont destinées aux seules équipes de TEC. Elles ne sont ni vendues ni cédées. Le site est hébergé par OVH SAS en France.</p>
<h2>Cookies et mesure d'audience</h2><p>Ce site n'utilise aucun cookie publicitaire ni outil de suivi tiers. Les polices de caractères sont hébergées localement : aucune donnée n'est transmise à un service tiers lors de votre visite.</p>
<h2>Vos droits</h2><p>Vous disposez d'un droit d'accès, de rectification, d'effacement, de limitation, d'opposition et de portabilité de vos données. Pour l'exercer : <a href="mailto:{EMAIL}">{EMAIL}</a>. Vous pouvez introduire une réclamation auprès de la CNIL (<a href="https://www.cnil.fr" rel="noopener">www.cnil.fr</a>).</p>
</div></section>'''
pages.append(page("confidentialite.html", "Politique de confidentialité — TEC", "Politique de confidentialité et de protection des données personnelles du site le-tec.fr.", b, crumbs=[("Accueil",""),("Confidentialité","confidentialite.html")]))

b = page_hero([("Accueil","index.html"),("Page introuvable","404.html")], "Erreur 404", "Cette page n'est pas sur le planning", "La page demandée n'existe pas ou a été déplacée.",
  f'<div class="hero-actions mt-2"><a class="btn btn--red" href="/index.html">Retour à l\'accueil</a><a class="btn btn--ghost-l" href="/references.html">Nos références</a></div>')
pages.append(page("404.html", "Page introuvable — TEC", "Page introuvable.", b, extra_head='<meta name="robots" content="noindex">\n'))

# plan du site
links = [("Accueil","index.html"),("Nos métiers","nos-metiers.html")] + [(t,h) for h,ic,t,d in METIERS] + [("Références","references.html"),("L'agence","agence.html"),("Blog chantiers","blog/index.html")] \
  + [("— "+x["title"], "blog/"+x["slug"]+".html") for x in BLOG] + [("Actualités","actualites/index.html")] + [("— "+x["title"], "actualites/"+x["slug"]+".html") for x in ACTU] \
  + [("Contact","contact.html"),("Mentions légales","mentions-legales.html"),("Confidentialité","confidentialite.html"),("Plaquette (PDF)", PDF)]
b = page_hero([("Accueil","index.html"),("Plan du site","plan-du-site.html")], "Navigation", "Plan du site", "Toutes les pages du site le-tec.fr.")
b += '<section class="section"><div class="wrap prose"><ul>' + "".join(f'<li><a href="{{P}}{u}">{n}</a></li>' for n, u in links) + '</ul></div></section>'
pages.append(page("plan-du-site.html", "Plan du site — TEC", "Plan du site le-tec.fr.", b, crumbs=[("Accueil",""),("Plan du site","plan-du-site.html")]))

# ======================= FICHIERS TECHNIQUES =======================
today = "2026-11-07"
def lastmod(pth):
    m = re.search(r"/(.+)\.html", "/"+pth)
    for x in BLOG + ACTU:
        if pth.endswith(x["slug"]+".html"): return x["date"]
    return today
sm = ['<?xml version="1.0" encoding="UTF-8"?>','<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
for pth in pages:
    if pth in ("404.html","merci.html"): continue
    loc = SITE + "/" + ("" if pth == "index.html" else pth)
    pr = "1.0" if pth == "index.html" else ("0.9" if pth in SERVICES or pth=="references.html" else "0.7")
    sm.append(f"<url><loc>{loc}</loc><lastmod>{lastmod(pth)}</lastmod><priority>{pr}</priority></url>")
sm.append(f"<url><loc>{SITE}/{PDF}</loc><lastmod>{today}</lastmod><priority>0.6</priority></url>")
sm.append("</urlset>")
open(OUT+"/sitemap.xml","w").write("\n".join(sm))
open(OUT+"/robots.txt","w").write(f"User-agent: *\nAllow: /\nDisallow: /contact.php\n\nSitemap: {SITE}/sitemap.xml\n")

items = sorted([("blog",x) for x in BLOG]+[("actualites",x) for x in ACTU], key=lambda t: t[1]["date"], reverse=True)
def rfc(d):
    dt = datetime.datetime.strptime(d, "%Y-%m-%d"); return dt.strftime("%a, %d %b %Y 08:00:00 +0100")
rss = ['<?xml version="1.0" encoding="UTF-8"?>','<rss version="2.0"><channel>',f'<title>TEC — Blog chantiers et actualités</title><link>{SITE}/</link><description>Actualités des chantiers pilotés par TEC et veille juridique et technique du bâtiment.</description><language>fr-fr</language>']
for f, x in items:
    rss.append(f'<item><title>{esc(x["title"])}</title><link>{SITE}/{f}/{x["slug"]}.html</link><guid>{SITE}/{f}/{x["slug"]}.html</guid><pubDate>{rfc(x["date"])}</pubDate><description>{esc(x["desc"])}</description></item>')
rss.append("</channel></rss>")
open(OUT+"/feed.xml","w").write("\n".join(rss))

# llms.txt : résumé pour les moteurs de réponse IA
llms = f"""# TEC — Pilotage & Ingénierie (le-tec.fr)

> TEC (Technique et Économie de la Construction) est un bureau d'ingénierie de chantier basé à Grenoble (38). TEC assure la maîtrise d'œuvre d'exécution (MOEX : DCE, ACT, VISA, DET, AOR), l'OPC (ordonnancement, pilotage, coordination), le suivi de chantier, l'économie de la construction, l'assistance à maîtrise d'ouvrage et l'accompagnement à la conception architecturale, pour des opérations de logements et d'immobilier d'entreprise en Isère, Savoie, Haute-Savoie et Hautes-Alpes.

- Directeur général : Benjamin Camerino. Responsable technique : David Durigon. Cheffe de projet conception : Sandra Olandese.
- Adresse : Immeuble Équinoxe, 163 cours de la Libération et du Général de Gaulle, 38100 Grenoble. Téléphone : {PHONE}. E-mail : {EMAIL}.
- SAS au capital de 5 000 €, RCS Grenoble 941 810 749, créée en mars 2025.
- Références : Élément (Embrun, 44 logements), Les Jardins de Babylone (Saint-Jean-de-Maurienne, 17 logements), Horizon Belledonne (La Terrasse, 35 logements dont 30 en PSLA), MTI à Claix (bâtiment industriel réaménagé en site occupé pour CGBI, livré en 2026), SiPearl à Grenoble (500 m² de bureaux en moins de 7 semaines, pour CGBI), AD Santé à Domène (extension puis réhabilitation de l'existant en site occupé, pour CGBI), Soliha à Eybens (bureaux, pour CGBI).

## Métiers
""" + "\n".join(f"- [{t}]({SITE}/{h}): {d}" for h, ic, t, d in METIERS) + f"""

## Pages clés
- [Références]({SITE}/references.html)
- [L'agence et l'équipe]({SITE}/agence.html)
- [Blog chantiers]({SITE}/blog/index.html)
- [Actualités juridiques et techniques 2026]({SITE}/actualites/index.html)
- [Plaquette PDF]({SITE}/{PDF})
- [Contact]({SITE}/contact.html)

## Actualités
""" + "\n".join(f"- [{x['title']}]({SITE}/actualites/{x['slug']}.html)" for x in ACTU) + "\n"
open(OUT+"/llms.txt","w").write(llms)

print(len(pages), "pages générées")
