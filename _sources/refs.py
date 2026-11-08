# -*- coding: utf-8 -*-
"""Références chantiers et illustrations « plan » générées en SVG."""

def _grid():
    return ('<defs><pattern id="g{k}" width="20" height="20" patternUnits="userSpaceOnUse"><path d="M20 0H0V20" fill="none" stroke="rgba(255,255,255,.06)"/></pattern></defs>'
            '<rect width="640" height="400" fill="#1b2350"/><rect width="640" height="400" fill="url(#g{k})"/>')

def _bldg(x, y0, w, floors, fh=34, roof="flat", win=4):
    h = floors * fh
    y = y0 - h
    s = [f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="rgba(58,75,149,.35)" stroke="#e8ebff" stroke-width="2"/>']
    for f in range(floors):
        fy = y + f * fh
        if f: s.append(f'<line x1="{x}" y1="{fy}" x2="{x+w}" y2="{fy}" stroke="rgba(232,235,255,.35)" stroke-dasharray="4 4"/>')
        gap = w / win
        for i in range(win):
            wx = x + gap * i + gap * 0.28
            s.append(f'<rect x="{wx:.1f}" y="{fy+9}" width="{gap*0.44:.1f}" height="{fh-18}" fill="none" stroke="#e8ebff" stroke-width="1.4"/>')
        if f < floors - 1 and f > 0:
            s.append(f'<line x1="{x-8}" y1="{fy+fh}" x2="{x+w*0.45}" y2="{fy+fh}" stroke="#e8ebff" stroke-width="2"/>')
    if roof == "pitch":
        s.append(f'<path d="M{x-10} {y} L{x+w/2} {y-38} L{x+w+10} {y}" fill="none" stroke="#e8ebff" stroke-width="2"/>')
    elif roof == "mono":
        s.append(f'<path d="M{x-8} {y} L{x+w+8} {y-24}" fill="none" stroke="#e8ebff" stroke-width="2"/>')
    else:
        s.append(f'<line x1="{x-4}" y1="{y}" x2="{x+w+4}" y2="{y}" stroke="#e8ebff" stroke-width="4"/>')
    return "".join(s)

def _crane(x, top=70, base=340, jib=230):
    return (f'<g stroke="#c42826" stroke-width="2" fill="none"><line x1="{x}" y1="{base}" x2="{x}" y2="{top}"/>'
            f'<line x1="{x+10}" y1="{base}" x2="{x+10}" y2="{top}"/>'
            + "".join(f'<line x1="{x}" y1="{yy}" x2="{x+10}" y2="{yy+18}"/>' for yy in range(top, base - 18, 18)) +
            f'<line x1="{x-60}" y1="{top}" x2="{x+jib}" y2="{top}"/><line x1="{x-60}" y1="{top+10}" x2="{x+jib}" y2="{top+10}"/>'
            f'<line x1="{x+5}" y1="{top-26}" x2="{x+jib}" y2="{top}"/><line x1="{x+5}" y1="{top-26}" x2="{x-60}" y2="{top}"/>'
            f'<line x1="{x+jib*0.7}" y1="{top+10}" x2="{x+jib*0.7}" y2="{top+70}"/></g>'
            f'<rect x="{x-60}" y="{top+10}" width="22" height="16" fill="#c42826"/>')

def svg(kind, k="a", wip=True):
    g = _grid().replace("{k}", k)
    ground = '<line x1="0" y1="340" x2="640" y2="340" stroke="#e8ebff" stroke-width="2"/><g stroke="rgba(232,235,255,.25)">' + "".join(f'<line x1="{i}" y1="340" x2="{i-12}" y2="354"/>' for i in range(10, 640, 18)) + '</g>'
    sun = '<circle cx="%d" cy="78" r="22" fill="#c42826"/>' % (90 if kind == "babylone" else 560)
    body = ""
    if kind == "element":   # deux bâtiments R+3 + sous-sol
        body = _bldg(70, 340, 210, 4, win=5, roof="mono") + _bldg(330, 340, 230, 4, win=5, roof="mono") + '<rect x="70" y="340" width="490" height="26" fill="none" stroke="rgba(232,235,255,.4)" stroke-dasharray="6 5"/>'
        if wip: body += _crane(300, top=64, jib=220)
    elif kind == "babylone":  # R+3, toiture à pans
        body = _bldg(150, 340, 330, 4, win=6, roof="pitch")
    elif kind == "belledonne":  # collectif + maisons
        body = _bldg(60, 340, 240, 4, win=5) + _bldg(330, 340, 70, 2, win=1, roof="pitch") + _bldg(420, 340, 70, 2, win=1, roof="pitch") + _bldg(510, 340, 70, 2, win=1, roof="pitch")
    elif kind == "industrie":
        body = ('<path d="M70 340V180l120-50v50l120-50v50l120-50v50l120-50v210" fill="rgba(58,75,149,.35)" stroke="#e8ebff" stroke-width="2"/>'
                + "".join(f'<rect x="{x}" y="250" width="70" height="90" fill="none" stroke="#e8ebff" stroke-width="1.6"/>' for x in (110, 230, 350, 470)))
    elif kind == "bureaux":
        body = _bldg(120, 340, 400, 5, fh=40, win=8) + '<rect x="290" y="300" width="60" height="40" fill="#121836" stroke="#e8ebff" stroke-width="2"/>'
    if kind == "babylone" and wip:
        body = _bldg(150, 340, 330, 4, win=6, roof="pitch") + _crane(500, top=70, jib=120)
    # cotes
    cote = '<g stroke="rgba(232,235,255,.45)" fill="rgba(232,235,255,.6)" font-family="Inter Tight,Arial" font-size="11"><line x1="40" y1="372" x2="600" y2="372"/><line x1="40" y1="366" x2="40" y2="378"/><line x1="600" y1="366" x2="600" y2="378"/></g>'
    return f'<svg viewBox="0 0 640 400" xmlns="http://www.w3.org/2000/svg" role="img" aria-hidden="true" preserveAspectRatio="xMidYMid slice">{g}{sun}{body}{ground}{cote}</svg>'

REFS = [
 dict(slug="element-embrun", kind="element", name="Élément", loc="Embrun (05) · Hautes-Alpes",
      typ="44 logements collectifs en accession libre", mo="SCCV Élément — Novélia Résidences",
      archi="Architectes & Ko", mission="Maîtrise d'œuvre d'exécution (DET), OPC, visa des plans EXE, validation des situations de travaux",
      dates="Ordre de service : 12 mai 2025 · Livraison prévue début 2027", status="En travaux", phase="Finitions, façades et VRD",
      lots="22 lots séparés, du désamiantage aux enrobés",
      text="Deux bâtiments en R+3 sur sous-sol commun, raccordés au réseau de chaleur de la ville. TEC dirige l'exécution des travaux depuis l'ordre de service : réunion hebdomadaire le lundi sur la base vie, plus de 60 comptes rendus diffusés, tests d'étanchéité à l'air intermédiaires et coordination avec les concessionnaires (Enedis, chauffage urbain, eau de l'Embrunais).",
      facts=["44 logements", "R+3 + sous-sol", "22 lots", "Réseau de chaleur"]),
 dict(slug="jardins-de-babylone", kind="babylone", name="Les Jardins de Babylone", loc="Saint-Jean-de-Maurienne (73) · Savoie",
      typ="17 logements collectifs en accession libre", mo="SCCV Les Jardins de Babylone — Novélia Résidences",
      archi="Architectes & Ko", mission="Maîtrise d'œuvre d'exécution, OPC, contrôle des situations, agrément des sous-traitants",
      dates="Ordre de service : 14 janvier 2026", status="En travaux", phase="Second œuvre",
      lots="19 lots séparés",
      text="Résidence en R+3 au cœur de la Maurienne. Le gros œuvre a été mené en un peu plus de quatre mois ; le bâtiment est aujourd'hui hors d'eau et hors d'air et le second œuvre progresse étage par étage. TEC anime la réunion de chantier chaque jeudi et pilote la synchronisation des lots de finition.",
      facts=["17 logements", "R+3", "19 lots", "Charpente lamellé-collé"]),
 dict(slug="horizon-belledonne", kind="belledonne", name="Horizon Belledonne", loc="La Terrasse (38) · Isère",
      typ="25 appartements et 10 maisons, dont 30 logements en accession sociale (PSLA)", mo="Novélia Résidences, en partenariat avec SOLIHA",
      archi="—", mission="Pilotage de l'exécution et coordination des entreprises",
      dates="Mission en cours", status="En cours", phase="",
      lots="Opération mixte collectif + individuel",
      text="Programme mixte dans le Grésivaudan, face à la chaîne de Belledonne : un collectif et des maisons, majoritairement en prêt social location-accession (PSLA). Le pilotage doit concilier deux typologies de chantier sur un même site et un calendrier de commercialisation sociale.",
      facts=["35 logements", "PSLA", "Collectif + maisons"]),
 dict(slug="mti-claix", kind="industrie", name="MTI", loc="Claix (38) · Isère",
      typ="Rénovation lourde de locaux industriels en site occupé", mo="MTI — opération réalisée avec CGBI, contractant général",
      archi="—", mission="Pilotage d'exécution et coordination en site occupé",
      dates="Mission en cours", status="En cours", phase="",
      lots="Travaux phasés, activité maintenue",
      text="Rénovation lourde de bâtiments industriels sans interrompre la production : phasage par zones, coordination des accès, consignations et sécurité des personnels de l'entreprise au quotidien.",
      facts=["Industrie", "Site occupé", "Avec CGBI"]),
 dict(slug="soliha-eybens", kind="bureaux", name="Soliha", loc="Eybens (38) · Isère",
      typ="Aménagement et réorganisation de plateaux de bureaux", mo="SOLIHA — opération réalisée avec CGBI, contractant général",
      archi="—", mission="Pilotage d'exécution et coordination des corps d'état",
      dates="Mission en cours", status="En cours", phase="",
      lots="Cloisonnement, CVC, électricité, finitions",
      text="Réaménagement de plateaux tertiaires : cloisonnement, réseaux et finitions, organisés pour limiter la gêne des équipes en place et tenir un calendrier de réintégration précis.",
      facts=["Tertiaire", "Plateaux de bureaux", "Avec CGBI"]),
]
