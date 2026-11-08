# Site le-tec.fr — mode d'emploi pour Claude

Site statique de TEC (Technique et Économie de la Construction), Grenoble. Interlocuteur : Stéphane JOUGLARD (directeur de la publication). Répondre en français.

## Déploiement
- Chaque push sur `main` est déployé automatiquement sur l'hébergement OVH (webhook). Un push publie donc le site.
- Racine du dépôt = racine du site. `_sources/` contient le générateur Python (non servi, `.htaccess` « Require all denied ») ; `*.md` et `*.py` sont bloqués à la racine.
- TEC a sa propre identité : ne jamais mentionner le groupe ni la holding qui la détient.

## Régénérer le site
Le générateur écrit dans `/home/claude/tec/site` (constante `OUT` de `_sources/common.py`). Pour travailler :

```bash
mkdir -p /home/claude/tec/build /home/claude/tec/site /home/claude/tec/work
cp _sources/*.py /home/claude/tec/build/
find . -mindepth 1 -maxdepth 1 ! -name .git ! -name _sources ! -name README.md ! -name CLAUDE.md -exec cp -a {} /home/claude/tec/site/ \;
cd /home/claude/tec/build && python3 build.py          # génère les 35+ pages, sitemap, RSS, llms.txt
```

Puis recopier le résultat dans le dépôt :

```bash
cd <dépôt> && find . -mindepth 1 -maxdepth 1 ! -name .git ! -name README.md ! -name CLAUDE.md ! -name _sources -exec rm -rf {} + \
  && cp -a /home/claude/tec/site/. ./ && cp /home/claude/tec/build/*.py _sources/
```

La plaquette PDF (`plaquette.py`) n'est à régénérer que si son contenu change (nécessite google-chrome et pdftoppm).

## Contenus
- `posts.py` → `BLOG` (articles chantiers) et `ACTU` (actualités juridiques et techniques).
- Format d'une entrée `ACTU` : `slug`, `date` (ISO), `cat` (`jur` ou `tech`), `catl` (« Juridique » / « Technique »), `title`, `short` (titre court), `desc` (≈150 caractères, sert de meta description), `body` (HTML : `<p>`, `<h2>`, `<ul>`, `<div class="callout"><h4>…</h4><p>…</p></div>`), `sources` (liste de tuples `("Libellé — média, date", "URL")`).
- Chaque actualité se termine par ce que cela change pour un maître d'ouvrage ou un chantier (angle TEC : maîtrise d'œuvre d'exécution, OPC, économie de la construction).
- Mettre à jour `today = "AAAA-MM-JJ"` dans `build.py` (lastmod du sitemap) à chaque mise à jour.
- Sources officielles en priorité (Légifrance, ministères, ADEME, CSTB, FFB, Cerema, EUR-Lex) ; vérifier dates, numéros de textes et chiffres ; rédaction originale, jamais recopiée ; aucun chiffre sans source.

## Vérification
Servir `/home/claude/tec/site` (`python3 -m http.server 8765`) et faire des captures avec `google-chrome --headless=new --screenshot` (ajouter `?static` à l'URL pour désactiver les animations) : `actualites/index.html`, chaque nouvel article, l'accueil (encart actualités), en 1300 px et en 390 px de large.
