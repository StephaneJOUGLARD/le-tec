# -*- coding: utf-8 -*-
import os, sys, subprocess
sys.path.insert(0, os.path.dirname(__file__))
from common import icon, PHONE, EMAIL
from refs import REFS, svg, photo

S = "/home/claude/tec/site/assets"
logo_b = open(S + "/img/logo-tec-blanc.svg").read()
logo_c = open(S + "/img/logo-tec.svg").read()
R = {r["slug"]: r for r in REFS}

css = f"""
@font-face{{font-family:Archivo;src:url(file://{S}/fonts/archivo.woff2);font-weight:100 900;font-stretch:62% 125%}}
@font-face{{font-family:Archivo;src:url(file://{S}/fonts/archivo-ext.woff2);font-weight:100 900;font-stretch:62% 125%;unicode-range:U+0100-02AF}}
@font-face{{font-family:Inter Tight;src:url(file://{S}/fonts/intertight.woff2);font-weight:100 900}}
@font-face{{font-family:Inter Tight;src:url(file://{S}/fonts/intertight-ext.woff2);font-weight:100 900;unicode-range:U+0100-02AF}}
@page{{size:A4;margin:0}}
*{{box-sizing:border-box}}
body{{margin:0;font-family:'Inter Tight';color:#1a1f38;font-size:10.2pt;line-height:1.5;-webkit-print-color-adjust:exact;print-color-adjust:exact}}
.pg{{width:210mm;height:297mm;position:relative;overflow:hidden;page-break-after:always;background:#f6f5f0}}
.pg:last-child{{page-break-after:auto}}
h1,h2,h3,h4{{font-family:Archivo;font-stretch:115%;margin:0;color:#121836;line-height:1.08}}
.ink{{background:#121836;color:#c9cff0}}
.grid{{position:absolute;inset:0;background-image:linear-gradient(rgba(255,255,255,.05) 1px,transparent 1px),linear-gradient(90deg,rgba(255,255,255,.05) 1px,transparent 1px);background-size:14mm 14mm}}
.eb{{font-family:Archivo;font-stretch:120%;font-weight:700;font-size:7.6pt;letter-spacing:.18em;text-transform:uppercase;color:#3a4b95;display:flex;align-items:center;gap:2.2mm;margin-bottom:3mm}}
.eb:before{{content:"";width:2.2mm;height:2.2mm;border-radius:50%;background:#c42826}}
.ink .eb{{color:#aeb7ea}}
.pad{{padding:16mm 16mm}}
.foot{{position:absolute;left:16mm;right:16mm;bottom:9mm;display:flex;justify-content:space-between;font-size:7.4pt;color:#8a90ad;border-top:.3mm solid rgba(18,24,54,.15);padding-top:3mm}}
.ink .foot{{color:#7f88ba;border-color:rgba(255,255,255,.15)}}
/* cover */
.cover .logo{{position:absolute;left:16mm;top:20mm;width:62mm}}
.cover .sect{{position:absolute;right:16mm;top:24mm;text-align:right;font-family:Archivo;font-stretch:118%;font-weight:700;font-size:7.6pt;letter-spacing:.16em;color:#aeb7ea;line-height:1.9}}
.cover h1{{position:absolute;left:16mm;right:16mm;top:92mm;color:#fff;font-size:44pt;font-weight:800;letter-spacing:-.01em}}
.cover h1 span{{color:#c42826}}
.cover .sub{{position:absolute;left:16mm;width:150mm;top:150mm;font-size:12.5pt;color:#c3c9ea;line-height:1.5}}
.cover .gantt{{position:absolute;left:16mm;right:16mm;top:185mm;height:62mm;border:.3mm solid rgba(255,255,255,.14);border-radius:4mm;padding:6mm;background:rgba(255,255,255,.03)}}
.gr{{display:grid;grid-template-columns:38mm 1fr;height:6.4mm;align-items:center;border-top:.2mm dashed rgba(255,255,255,.1);font-size:7.6pt;color:#c3c9ea}}
.gt{{position:relative;height:100%}}
.gb{{position:absolute;top:1.8mm;height:2.8mm;border-radius:1mm;background:linear-gradient(90deg,#5a6bc0,#3a4b95)}}
.gb.ms{{width:2.4mm!important;height:2.4mm;transform:rotate(45deg);background:#c42826;top:2mm}}
.today{{position:absolute;top:5mm;bottom:5mm;width:.5mm;background:#c42826;left:calc(6mm + 38mm + (100% - 50mm)*.62)}}
.cover .bl{{position:absolute;left:16mm;right:16mm;bottom:18mm;display:flex;justify-content:space-between;align-items:end;color:#9aa3cf;font-size:8.2pt}}
.cover .bl b{{color:#fff;font-family:Archivo;font-stretch:112%}}
.dot{{position:absolute;width:120mm;height:120mm;border-radius:50%;right:-40mm;top:-50mm;background:radial-gradient(circle,rgba(58,75,149,.6),transparent 65%)}}
/* p2 */
.two{{display:grid;grid-template-columns:1fr 1fr;gap:9mm}}
.p2{{font-size:9.4pt}}.p2 .lead{{font-size:11pt}}.p2 .box{{padding:5mm}}.p2 h2{{font-size:25pt;font-weight:800;margin-bottom:6mm}}
.p2 p{{margin:0 0 3mm}}
.lead{{font-size:12pt;color:#5a6182;line-height:1.5}}
.box{{background:#fff;border:.3mm solid rgba(18,24,54,.12);border-radius:4mm;padding:6mm}}
.box h3{{font-size:12pt;margin-bottom:2.5mm}}
.quote{{font-family:Archivo;font-stretch:105%;font-size:11.5pt;line-height:1.4;color:#121836;border-left:1mm solid #c42826;padding-left:5mm;margin:6mm 0}}
.band{{background:#121836;color:#c9cff0;border-radius:5mm;padding:6mm;margin-top:6mm;display:grid;grid-template-columns:repeat(4,1fr);gap:4mm}}
.band b{{display:block;font-family:Archivo;font-stretch:125%;font-weight:800;font-size:22pt;color:#fff;line-height:1}}
.band b sup{{color:#c42826;font-size:11pt}}
.band span{{font-size:7.8pt;color:#a9b1db;display:block;margin-top:1.5mm}}
.who{{display:grid;grid-template-columns:repeat(4,1fr);gap:3mm;margin-top:5mm}}
.who div{{background:#fff;border:.3mm solid rgba(18,24,54,.12);border-radius:3mm;padding:4mm;font-size:8.4pt}}
.who b{{display:block;font-family:Archivo;font-stretch:110%;font-size:9pt;color:#121836;margin-bottom:1mm}}
/* p3 */
.mets{{display:grid;grid-template-columns:1fr 1fr;gap:4mm}}
.met{{background:#fff;border:.3mm solid rgba(18,24,54,.12);border-radius:4mm;padding:5.5mm;display:grid;grid-template-columns:12mm 1fr;gap:4mm}}
.met .ic{{width:12mm;height:12mm;border-radius:3mm;background:#3a4b95;color:#fff;display:grid;place-items:center}}
.met .ic svg{{width:6.5mm;height:6.5mm}}
.met h3{{font-size:11.5pt;margin-bottom:1.5mm}}
.met p{{margin:0;font-size:8.6pt;color:#5a6182}}
.met ul{{margin:2mm 0 0;padding-left:4mm;font-size:8.2pt;color:#1a1f38}}
.met li::marker{{color:#c42826}}
.met.wide{{grid-column:span 2}}
.eng{{display:grid;grid-template-columns:repeat(3,1fr);gap:3mm;margin-top:6mm}}
.eng div{{background:#121836;color:#c9cff0;border-radius:3mm;padding:4.5mm;font-size:8pt}}
.eng b{{display:block;color:#fff;font-family:Archivo;font-stretch:112%;font-size:9.4pt;margin:2mm 0 1mm}}
.eng svg{{width:6mm;height:6mm;color:#c42826}}
/* p4 */
.steps{{display:grid;grid-template-columns:repeat(6,1fr);position:relative;margin:4mm 0 8mm}}
.steps:before{{content:"";position:absolute;left:0;right:0;top:5mm;height:.6mm;background:linear-gradient(90deg,#3a4b95,#c42826)}}
.st{{position:relative;padding-right:3mm;font-size:7.6pt;color:#5a6182}}
.st i{{display:grid;place-items:center;width:10mm;height:10mm;border-radius:50%;background:#121836;color:#fff;font-style:normal;font-family:Archivo;font-stretch:120%;font-weight:800;font-size:9pt;margin-bottom:3mm;position:relative}}
.st:last-child i{{background:#c42826}}
.st b{{display:block;font-family:Archivo;font-stretch:110%;color:#121836;font-size:9pt;margin-bottom:1mm}}
.refs{{display:grid;grid-template-columns:repeat(3,1fr);gap:4mm}}
.ref{{background:#fff;border:.3mm solid rgba(18,24,54,.12);border-radius:4mm;overflow:hidden}}
.ref .v{{height:40mm;overflow:hidden}}
.ref .v svg{{width:100%;height:100%}}
.ref .t{{padding:3.5mm 4mm 4mm;font-size:7.8pt;color:#5a6182}}
.ref .t b{{display:block;font-family:Archivo;font-stretch:110%;color:#121836;font-size:10pt}}
.ref .t em{{font-style:normal;font-size:7pt;font-weight:600;color:#3a4b95;letter-spacing:.04em}}
.why{{display:grid;grid-template-columns:1fr 1fr;gap:3mm 8mm;margin-top:3mm;font-size:8.8pt}}.why div{{background:#fff;border:.3mm solid rgba(18,24,54,.12);border-radius:3mm;padding:3.5mm 4mm}}.why b{{display:block;font-family:Archivo;font-stretch:110%;color:#121836;font-size:9.6pt;margin-bottom:.8mm}}.others{{margin-top:3mm;font-size:8pt;color:#5a6182}}
.contact{{position:absolute;left:0;right:0;bottom:0;height:80mm;background:#121836;color:#c9cff0;padding:11mm 16mm;display:grid;grid-template-columns:1fr 1.25fr;gap:10mm}}
.contact h2{{color:#fff;font-size:19pt;margin-bottom:3mm}}
.contact .team{{display:grid;gap:2.2mm;font-size:8.6pt}}
.contact .team b{{color:#fff;font-family:Archivo;font-stretch:110%}}
.contact .co{{font-size:9pt;line-height:1.7}}
.contact .co b{{color:#fff}}
.contact .logo{{width:28mm;margin-bottom:2mm}}
"""

def gantt():
    rows = [("Gros œuvre",0,34,""),("Charpente · couverture",30,18,""),("Menuiseries extérieures",38,14,""),("Cloisons · doublages",46,22,""),("Fluides · électricité",40,40,""),("Finitions",62,26,""),("Réception",93,0,"ms")]
    return "".join(f'<div class="gr"><span>{n}</span><div class="gt"><i class="gb {c}" style="left:{l}%;width:{w}%"></i></div></div>' for n,l,w,c in rows) + '<div class="today"></div>'

foot = lambda n, ink=False: f'<div class="foot"><span>TEC — Technique et Économie de la Construction · Pilotage &amp; Ingénierie</span><span>le-tec.fr · {n}/4</span></div>'

p1 = f'''<section class="pg ink cover"><div class="grid"></div><div class="dot"></div>
<div class="logo">{logo_b}</div>
<div class="sect">MAÎTRISE D'ŒUVRE D'EXÉCUTION<br>OPC · SUIVI DE CHANTIER<br>ÉCONOMIE DE LA CONSTRUCTION</div>
<h1>Votre chantier,<br>notre pilotage<span>.</span></h1>
<div class="sub">Logements · Tertiaire · Industrie · Réhabilitation<br>De la conception à la réception, une ingénierie de chantier au service des maîtres d'ouvrage des Alpes.</div>
<div class="gantt">{gantt()}</div>
<div class="bl"><span><b>Immeuble Équinoxe</b><br>163 cours de la Libération et du Général de Gaulle · 38100 Grenoble</span><span style="text-align:right"><b>{PHONE}</b><br>{EMAIL} · le-tec.fr</span></div>
</section>'''

p2 = f'''<section class="pg p2"><div class="pad">
<div class="eb">Qui sommes-nous ?</div>
<div class="two">
<div><h2>Votre projet,<br>notre métier</h2>
<p class="lead">TEC — Technique et Économie de la Construction — est un bureau d'études d'exécution et d'économie de la construction. Créée à Grenoble en 2025, notre équipe pilote des opérations de logements et d'immobilier d'entreprise en Isère, Savoie, Haute-Savoie et Hautes-Alpes.</p>
<div class="quote">Un chantier réussi se prépare dès la conception et se gagne chaque semaine sur le terrain.</div>
<p>Architectes, bureaux d'études structure et fluides, bureau de contrôle, coordonnateur SPS, géotechnicien, concessionnaires, services instructeurs et jusqu'à 22 entreprises de travaux : sur une opération, les intervenants sont nombreux. Notre rôle est de les faire travailler ensemble, dans le bon ordre, au bon prix et au bon moment.</p></div>
<div>
<div class="box"><h3>Qu'est-ce qu'un maître d'œuvre d'exécution ?</h3><p>Il transforme le projet conçu en chantier maîtrisé : il prépare la consultation des entreprises, vise leurs plans d'exécution, dirige les travaux, valide les situations et organise la réception des ouvrages, pour le compte du maître d'ouvrage.</p></div>
<div class="box" style="margin-top:4mm"><h3>Et l'OPC ?</h3><p>L'ordonnancement, le pilotage et la coordination organisent le chantier dans le temps : planning tous corps d'état, enchaînement des lots, gestion des interfaces et des moyens communs. Chez TEC, MOE d'exécution et OPC sont assurés par la même équipe : un seul interlocuteur pour la qualité, le coût et le délai.</p></div>
<div class="box" style="margin-top:4mm"><h3>Interlocuteur unique</h3><p>Choisir TEC, c'est vous concentrer sur l'essentiel : votre programme et vos acquéreurs ou utilisateurs. Nous vous informons chaque semaine de l'avancement réel et vous alertons avant que les écarts ne deviennent des retards.</p></div>
</div></div>
<div class="band"><div><b>96</b><span>logements en cours de pilotage d'exécution</span></div><div><b>90<sup>+</sup></b><span>réunions et comptes rendus de chantier depuis 2025</span></div><div><b>22</b><span>lots séparés coordonnés sur une même opération</span></div><div><b>4</b><span>départements alpins : Isère, Savoie, Haute-Savoie, Hautes-Alpes</span></div></div>
<div class="eb" style="margin-top:6mm">Nos typologies</div>
<div class="who"><div><b>Logements collectifs</b>Accession libre et sociale</div><div><b>Programmes mixtes</b>Collectif et individuel</div><div><b>Industrie &amp; tertiaire</b>Y compris en site occupé</div><div><b>Réhabilitation</b>Bâtis existants</div></div>
</div>{foot(2)}</section>'''

mets = [("concept","Conception architecturale","En lien avec l'architecte et les bureaux d'études.",["Faisabilité, capacité, esquisses","APS / APD, estimation par phase","Dossiers de permis de construire et d'aménager"]),
        ("moe","Maîtrise d'œuvre d'exécution","De la consultation à la réception des ouvrages.",["DCE, CCTP, analyse des offres (ACT)","Visa des plans d'exécution","Direction de l'exécution (DET), AOR, DOE"]),
        ("suivi","Suivi de chantier","Présence terrain chaque semaine.",["Réunion hebdomadaire et compte rendu","Contrôle qualité, essais, situations","Sécurité, propreté, intempéries"]),
        ("opc","OPC","Ordonnancement, pilotage, coordination.",["Planning tous corps d'état","Interfaces entre lots, moyens communs","Concessionnaires, OPR et livraisons"]),
        ("eco","Économie de la construction & AMO","Maîtriser le coût, de l'esquisse au décompte.",["Estimations, métrés, CCTP","Consultation et négociation","Suivi budgétaire, avenants, DGD"])]
mh = "".join(f'<div class="met{" wide" if i==4 else ""}"><div class="ic">{icon(ic)}</div><div><h3>{t}</h3><p>{d}</p><ul>{"".join(f"<li>{x}</li>" for x in l)}</ul></div></div>' for i,(ic,t,d,l) in enumerate(mets))
engs = [("clock","Planning contractuel","Calendrier détaillé intégré aux marchés et mis à jour chaque semaine."),("doc","Comptes rendus hebdomadaires","Actions datées, avancement par lot, photos ; diffusés sous 48 h."),
        ("shield","Visa & contrôle qualité","Plans EXE visés en lien avec le bureau de contrôle, essais, autocontrôles."),("euro","Situations validées","Avancement contrôlé chaque mois avant facturation des entreprises."),
        ("users","Sous-traitance maîtrisée","Instruction des demandes d'agrément et des pièces obligatoires."),("eye","Réception & garanties","OPR, procès-verbaux, levée des réserves, DOE, parfait achèvement.")]
eh = "".join(f'<div>{icon(i)}<b>{t}</b>{d}</div>' for i,t,d in engs)
p3 = f'''<section class="pg"><div class="pad">
<div class="eb">Nos métiers</div><h2 style="font-size:25pt;font-weight:800;margin-bottom:3mm">Une ingénierie de chantier complète</h2>
<p class="lead" style="margin:0 0 6mm;max-width:150mm">Cinq expertises complémentaires, mobilisables à la carte ou en mission complète, en neuf comme en réhabilitation.</p>
<div class="mets">{mh}</div>
<div class="eb" style="margin-top:8mm">Nos engagements</div>
<div class="eng">{eh}</div>
</div>{foot(3)}</section>'''

steps = [("01","Conception","Faisabilité, esquisses, APD, autorisations"),("02","Consultation","DCE, CCTP, analyse des offres, marchés"),("03","Préparation","Visas EXE, planning TCE, installation"),("04","Exécution","DET, OPC, réunions hebdomadaires"),("05","Réception","OPR, PV, levée des réserves, DOE"),("06","Après livraison","Parfait achèvement, garanties")]
sh = "".join(f'<div class="st"><i>{n}</i><b>{t}</b>{d}</div>' for n,t,d in steps)
rh = "".join(f'<div class="ref"><div class="v">{('<img src="file://'+S+'/img/references/'+s+'-800.webp" style="width:100%;height:100%;object-fit:cover">') if photo(s) else svg(R[s]["kind"], s[:3]+"p")}</div><div class="t"><em>{R[s]["loc"].split(" · ")[0].upper()}</em><b>{R[s]["name"]}</b>{R[s]["typ"]}<br>Mission : {R[s]["mission"].split(",")[0]}</div></div>' for s in ["element-embrun","jardins-de-babylone","horizon-belledonne"])
p4 = f'''<section class="pg"><div class="pad">
<div class="eb">Les étapes clés de votre projet, avec TEC</div>
<div class="steps">{sh}</div>
<div class="eb">Références — chantiers en cours</div>
<div class="refs">{rh}</div>
<p class="others"><b>Industrie et tertiaire, pour CGBI :</b> MTI à Claix (bâtiment industriel réaménagé en site occupé en 7 mois, livré en 2026) · SiPearl à Grenoble (500 m² de bureaux en moins de 7 semaines) · AD Santé à Domène (extension et rénovation complète en site occupé) · Soliha à Eybens (plateaux de bureaux).</p>
<div class="eb" style="margin-top:7mm">Pourquoi nous confier votre chantier</div>
<div class="why"><div><b>Continuité</b>L'équipe qui prépare la consultation est celle qui pilote et réceptionne.</div><div><b>Présence terrain</b>Une réunion de chantier chaque semaine, des comptes rendus qui engagent.</div><div><b>Maîtrise des coûts</b>Situations validées chaque mois, travaux modificatifs chiffrés avant exécution.</div><div><b>Ancrage alpin</b>Métropole grenobloise, Grésivaudan, Maurienne, Chablais, Champsaur, Embrunais.</div></div>
</div>
<div class="contact">
<div><div class="logo">{logo_b}</div><h2>Parlons de votre opération</h2><div class="co"><b>Immeuble Équinoxe</b><br>163 cours de la Libération et du Général de Gaulle<br>38100 Grenoble<br><b>{PHONE}</b> · {EMAIL}<br><b>le-tec.fr</b></div></div>
<div><div class="eb">L'équipe</div><div class="team"><div><b>Benjamin Camerino</b> — Directeur général</div><div><b>David Durigon</b> — Responsable technique</div><div><b>Sandra Olandese</b> — Cheffe de projet conception</div></div>
<p style="font-size:7.4pt;color:#7f88ba;margin-top:6mm">TEC — Technique et Économie de la Construction, SAS au capital de 5 000 € · RCS Grenoble 941 810 749 · Illustrations schématiques non contractuelles.</p></div>
</div></section>'''

html = f'<!DOCTYPE html><html lang="fr"><head><meta charset="utf-8"><title>Plaquette TEC — Pilotage & Ingénierie</title><style>{css}</style></head><body>{p1}{p2}{p3}{p4}</body></html>'
open("/home/claude/tec/work/plaquette.html", "w").write(html)
out = S + "/docs/plaquette-TEC-pilotage-ingenierie.pdf"
subprocess.run(["google-chrome", "--headless=new", "--no-sandbox", "--disable-gpu", "--no-pdf-header-footer", "--virtual-time-budget=3000", f"--print-to-pdf={out}", "file:///home/claude/tec/work/plaquette.html"], stderr=subprocess.DEVNULL)
print(out, os.path.getsize(out))
