# le-tec.fr

Site statique de TEC — Pilotage & Ingénierie.
Hébergement OVH, déploiement via l'intégration Git d'OVH (branche main, racine du dépôt).

_sources/ : générateur Python des pages (ne pas publier, protégé par .htaccess).

Déploiement : intégration Git OVH (hébergement le-tec.fr, dossier www) + webhook GitHub → mise en ligne automatique à chaque push sur main.
