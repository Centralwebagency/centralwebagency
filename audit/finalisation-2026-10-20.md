# Finalisation technique, commerciale et SEO — 20 octobre 2026

Ce rapport complète l'[audit du 19 octobre](rapport-2026-10-19.md). Il décrit les corrections locales de finalisation, les validations et les décisions restantes. **Aucun déploiement ni envoi de formulaire externe n'a été effectué.**

## Résultat

- Les **38 pages existantes** sont conservées. URL, canoniques, directives robots, sitemap et redirections sont inchangés.
- Les prix des offres restent identiques. Les chiffres de marché non vérifiés ont été retirés du guide de comparaison ; ce retrait ne modifie aucun tarif CWA.
- Les contradictions entre création et maintenance ont été corrigées, suivant les confirmations reçues pendant cette finalisation.
- Les textes SEO trop affirmatifs ont été corrigés, les liens entre articles et fiches métier renforcés et les données structurées réalignées.
- Les polices et icônes existantes sont désormais servies localement. Les couleurs, les glyphes, les graisses et les animations du site sont conservés ; aucun visuel ni vidéo n'a été remplacé.
- La compilation SCSS réussit sans l'ancien avertissement `@import`. Son remplacement par `@use` produit un CSS strictement identique avant/après cette seule modification.

L'audit initial n'avait pas établi de blocage général d'indexation. Cette conclusion reste inchangée. Le code permet de confirmer les réparations réalisées, mais ne permet pas d'attribuer la faible visibilité à une cause unique ni d'annoncer de futures positions.

## Corrections commerciales et CGV

Le modèle désormais explicite dans l'accueil, les articles concernés et les CGV est le suivant : **création facturée séparément, maintenance facultative dès 39 €/mois après livraison, création initiale exclue de la mensualité, droits effectivement acquis conservés après résiliation**.

L'ancienne carte d'accueil « Site vitrine + abonnement » pouvait laisser penser que 39 €/mois finançaient la création. Elle présente maintenant la maintenance et l'hébergement ; ses éléments reprennent des services déjà annoncés dans les offres existantes. Le guide de prix, l'article artisan, le guide de choix d'agence et l'article sur l'utilité d'un site ne proposent plus de financer la création par la maintenance.

Arbitrages reçus et appliqués :

| Point | Décision du propriétaire | Mise en œuvre |
|---|---|---|
| Quotas des CGV | Retenir les durées de la page maintenance | 30 min / 1 h / 2 h pour les vitrines ; 30 min / 1 h / 3 h pour les formules dynamiques existantes |
| Interventions ponctuelles | 30 €/h et 40 €/h correspondent à des prestations distinctes | Montants conservés ; libellés rattachés à maintenance et clé en main, sans inventer de nouveaux services |
| Délai simple | Estimation commerciale de 1 à 3 semaines | Retrait des 3–8 jours ouvrés ; aucune phase de développement distincte inventée |
| Projet complexe | Délai déterminé sur devis | Formulation explicite dans les CGV |
| Retouches | 30 jours, 45 pour Signature, selon le périmètre de l'offre | Distinction des retouches, des défauts techniques et des nouvelles fonctionnalités |

Les modifications de `cgv.html` sont **une proposition à valider juridiquement avant publication**. La [fiche de validation des CGV](cgv-validation-2026-10-20.md) expose les clauses touchées et les questions restantes : étendue précise des droits, remise/transfert, article de rétractation existant et portée des garanties/limitations. Aucun nouveau prix de transfert, délai de conservation ou engagement juridique non confirmé n'a été ajouté.

## Référencement : changements justifiés

### Intentions et ciblage local

L'accueil mentionne désormais Heyrieux, sa proximité avec Lyon, l'Est lyonnais et le Nord-Isère, tout en conservant l'accompagnement national. Son titre et sa description reflètent cette implantation réelle. L'H1 principal et la structure du hero sont conservés ; aucune page locale supplémentaire n'a été créée.

Les articles coach et restaurant avaient un titre presque commercial, proche des fiches métier. Leurs titres, descriptions et H1 expriment maintenant leur fonction de **préparation des contenus et de conseil**, tandis que les fiches restent les pages de **création de site pour la profession**. Le titre du guide SEO local ne promet plus la première place. Le guide de coût présente des critères pour comparer des devis au lieu d'annoncer des fourchettes de marché non sourcées. Les descriptions de présentation et d'utilité du site ont été resserrées pour correspondre au contenu réellement conservé.

Ces changements rendent la répartition des intentions plus claire ; **ils ne démontrent pas qu'une cannibalisation existait**. Aucun mot-clé, volume, position ou résultat concurrentiel non mesuré n'est présenté comme acquis.

| Page | Rôle principal après finalisation |
|---|---|
| Accueil | Agence implantée à Heyrieux près de Lyon, clientèle locale et nationale |
| `/services` | Présentation des solutions web |
| `/offres` | Comparaison commerciale et séparation création/maintenance |
| `/sites-cle-en-main` | Périmètre et prix de départ des formules de création |
| `/sites-abonnement` | Maintenance et hébergement après livraison |
| Fiches métier | Prestation de création adaptée à chaque profession |
| Articles métier | Conseils, contenus et préparation d'un projet |
| Conseils SEO / guide SEO local | Initiation générale / approfondissement local |

### Maillage interne

Liens contextuels ajoutés dans les paragraphes existants :

- article artisan → fiche artisan du bâtiment ;
- article coach → fiche coach sportif ;
- article restaurant → fiche restaurant ;
- article mode → fiches esthéticienne et photographe ;
- fiches artisan, coach et restaurant → guide correspondant ;
- guide de coût → formules clé en main ;
- choix d'agence → offres ;
- conseil SEO → guide SEO local.

Les cinq fiches citées par les articles passent chacune de **1 à 2 pages internes sources**. Les autres fiches restent reliées à leur hub métier. Aucune liaison artificielle n'a été créée entre professions sans rapport. Les pages restent toutes accessibles ; aucune page orpheline n'est détectée.

### Affirmations corrigées

- Les PDF peuvent être indexés par Google. Le conseil restaurant recommande l'HTML pour la lecture mobile sans présenter le PDF comme non indexable. [Formats indexables — Google](https://developers.google.com/search/docs/crawling-indexing/indexable-file-types?hl=fr).
- Retrait des pourcentages 80 % / 70 %, des volumes « milliers de recherches », de concurrence supposée faible et des équivalences chiffrées entre liens locaux et génériques.
- Retrait des scores PageSpeed systématiquement supérieurs à 90, des chargements universels sous une seconde et des comparaisons non mesurées avec WordPress.
- Révision des promesses de rentabilité, de première page et de classement quasi déterminé par les avis ou la seule fréquence de publication.
- Distinction entre mise à jour utile et publication fréquente ; entre présence dans Google Business Profile et présence organique du site ; entre site statique et projet dynamique.
- Les pages sociales peuvent apparaître dans Google ; elles ne sont plus présentées comme systématiquement absentes des résultats.
- Les landing pages ne sont plus exclues par principe du SEO.
- La présentation de l'éco-conception a été remplacée par une démarche de sobriété sans économie carbone chiffrée ni supériorité environnementale supposée.

Les pages privilégient des informations utiles et vérifiables. Ni l'allongement artificiel des contenus ni une fréquence de publication ne constituent une garantie de classement. [Contenus utiles — Google Search Central](https://developers.google.com/search/docs/fundamentals/creating-helpful-content?hl=fr).

### Données structurées et signaux techniques

Les JSON-LD ont été analysés sur les 38 pages. La FAQ de la fiche coach présentait plusieurs questions reformulées par rapport à la FAQ visible : questions et réponses structurées ont été synchronisées avec le texte affiché. L'audit vérifie maintenant cette correspondance pour toutes les FAQ balisées.

Les descriptions Article correspondent aux descriptions des pages retouchées. Les articles et conseils dont le contenu a été substantiellement modifié portent `dateModified: 2026-10-20` ; les dates de publication ont été conservées. Aucune date de publication artificielle ni référence client n'a été ajoutée.

L'ensemble des corrections techniques du 19 octobre est conservé : liens réparés, ancre des réalisations, logos et icônes correctement référencés, formulaire et FAQ lisibles sans JavaScript, gestion du menu et du focus, comportement de mouvement réduit. Les canoniques et les règles de redirection correctes n'ont pas été modifiées.

## Performance et conservation du rendu

Les 38 pages utilisent les copies locales des **mêmes polices Cormorant Garamond et Outfit et de Font Awesome 6.5.0**. Les fichiers de polices complets, les styles, les plages Unicode et les graisses existants sont conservés. Il n'y a ni substitution graphique ni sous-ensemble de glyphes susceptible de supprimer des caractères. Les licences et la provenance avec empreintes SHA-256 sont incluses dans `css/vendor/`.

Les appels aux feuilles Google Fonts et cdnjs ont été remplacés par des ressources du site ; les connexions externes préalables correspondantes ont été retirées. Le script commun est différé sur les pages qui ne l'étaient pas encore. Les titres H4 des petits composants et du pied de page sont devenus H3/H2 appropriés, avec maintien explicite des tailles, couleurs et marges.

### Mesures comparées

Deux passages avant et deux après, en alternance, avec Lighthouse 12.8.2, Chrome mobile simulé et le même serveur local utilisant gzip. Le point « avant » est une copie du projet au début de cette finalisation, comprenant les corrections du 19 octobre. **Ce n'est pas une comparaison entre la production du 19 octobre et un nouveau déploiement.**

| Indicateur | Avant, 2 passages | Après, 2 passages |
|---|---:|---:|
| Performance Lighthouse | 74 / 74 | 100 / 100 |
| LCP simulé | 4,46 s / 4,42 s | 1,515 s / 1,516 s |
| FCP simulé | 4,38 s / 4,26 s | 1,065 s / 1,066 s |
| TBT | 0 ms / 0 ms | 0 ms / 0 ms |
| CLS du test | 0 / 0,020 | 0,030 / 0,030 |
| Accessibilité automatique de l'accueil | 98 / 98 | 100 / 100 |
| Bonnes pratiques / SEO Lighthouse | 100 / 100 | 100 / 100 |

Le LCP médian de ces deux passages passe de **4,44 s à 1,52 s**. Le CLS observé après reste faible mais n'est pas inférieur à toutes les mesures avant. Le transfert des vidéos varie avec les plages téléchargées : aucun pourcentage de réduction durable de bande passante n'est déduit de ces passages.

Le contrôle comparé des métriques des polices et des styles calculés des composants vérifiés ne détecte aucun changement de famille, taille, graisse, hauteur de ligne, couleur ou marges. Les images et vidéos existantes sont identiques aux fichiers initiaux. Les tests d'animations et captures portent aussi sur le contact, les offres et une fiche métier.

Preuves : [comparaison et styles](mobile-comparison-2026-10-20.json), rapports [avant 1](mobile-before-1.json), [avant 2](mobile-before-2.json), [après 1](mobile-after-1.json), [après 2](mobile-after-2.json).

**Limites** : le serveur local n'a pas la latence, le cache et les conditions de Netlify. Les polices externes de l'état initial dépendent aussi du réseau au moment des tests. Ces résultats montrent l'intérêt de retirer ces dépendances du chemin critique ; ils ne garantissent ni un score identique en production ni une progression de positions. Les Core Web Vitals terrain LCP/INP/CLS restent à mesurer avec GSC/CrUX quand les données sont disponibles.

## Tests finaux

| Contrôle | Résultat et portée |
|---|---|
| Audit statique | 38 pages, 38 URL de sitemap, aucune anomalie dans les vérifications implémentées |
| Liens et ressources | Liens, ancres, images, scripts et nouvelles références CSS/polices résolus ; pas de ressource locale en erreur dans le parcours navigateur |
| JSON-LD | JSON analysable ; prix d'offres conservés ; FAQ structurées identiques aux FAQ visibles |
| Pages navigateur | 38 pages en HTTP 200 sur le serveur local, sans erreur JavaScript |
| Responsive | Contrôles des 38 pages à 390, 768 et 1440 px ; captures/animations complémentaires à 320, 768 et 1440 px sur 4 pages représentatives |
| Menu | Ouverture, fermeture, Échap, clavier, retour du focus et déblocage du scroll après changement de largeur vérifiés |
| FAQ / animations | Accordéons et révélation des contenus contrôlés ; parcours sans JavaScript conservé |
| Formulaire | Champs obligatoires, adresse invalide, formulaire valide et événement de soumission testés ; aucun POST externe effectué |
| SCSS | Compilation réussie ; `@use` remplace l'import déprécié sans changer le CSS produit par cette seule migration |
| JavaScript | `node --check js/script.js` valide |
| Invariants | 38 pages, URL, canoniques, robots, sitemap, redirections et prix structurés inchangés ; images/vidéos d'origine conservées |
| Git | Différences revues ; `git diff --check` sans erreur de whitespace |

Les tests automatiques couvrent les comportements indiqués, pas tous les appareils, lecteurs d'écran ou états possibles. Le score d'accessibilité de l'accueil n'est pas une certification WCAG du site.

Preuves : [état avant finalisation](finalisation-before.json), [audit final](finalisation-after.json), [tests navigateur](finalisation-browser.json), [animations et captures](finalisation-visual.json), [invariants](finalisation-invariants.json). L'audit statique a été étendu aux références CSS et à l'intégrité des ressources de polices.

Commandes utilisées :

```text
python scripts/audit_site.py --check --output audit/finalisation-after.json
python scripts/verify_invariants.py
python scripts/browser_audit.py --output audit/finalisation-browser.json
python scripts/browser_audit.py --visual --output audit/finalisation-visual.json
python scripts/measure_mobile.py
sass.cmd css/styles.scss css/styles.css
node --check js/script.js
git diff --check
```

`measure_mobile.py` nécessite la copie temporaire initiale et Lighthouse ; elle a été créée avant les changements de finalisation. `vendor_fonts.py` est un outil de préparation des ressources, pas une étape de téléchargement à exécuter automatiquement lors de chaque publication. Les fichiers fournis sont déjà locaux et les pages n'en dépendent plus sur les domaines tiers.

## Réception réelle du formulaire

La [procédure préparée](test-reception-formulaire.md) prévoit un marqueur de test, une adresse contrôlée par le propriétaire, un envoi unique autorisé et le rapprochement avec Formspree et la boîte destinataire. La réception, le quota et la configuration du compte restent inconnus tant que ce test n'a pas été autorisé et exécuté. La validation locale ne les prouve pas.

## Recommandations et décisions restantes

### Priorité de publication — validation nécessaire

1. Faire valider la version des CGV et les points décrits dans la fiche juridique. Les décisions commerciales de cette conversation ont été appliquées ; les choix de cession de droits et la légalité des autres clauses existantes ne sont pas inventés par cette finalisation.
2. Autoriser séparément un test de réception réelle du formulaire, ou l'effectuer vous-même avec la procédure fournie.
3. Valider le contenu et le déploiement. Lors de la publication, ne livrer que les fichiers du site : **exclure `audit/`, `scripts/`, caches et copies de comparaison**. Aucune publication n'a été lancée.

### Important — nécessite des données supplémentaires

- Export GSC requête × page, marque/hors marque, appareils, pays et dates comparables pour mesurer l'effet des changements. Contrôler les URL réellement indexées et les canoniques choisies par Google.
- Identifier les recherches commerciales qui obtiennent des impressions sur accueil, offres, fiches et articles. Une page d'information et une page commerciale sur le même métier peuvent être complémentaires ; leur éventuelle concurrence doit être vérifiée dans ces données.
- Vérifier la fiche Google Business Profile réelle, ses informations et ses résultats. Aucune validation de fiche ni performance locale n'a été inventée.
- Mesurer plusieurs passages en production après mise en ligne autorisée et consulter les données terrain disponibles. Les scores locaux ne remplacent pas cette étape.
- Documenter des réalisations, références ou témoignages réellement autorisés. Les vidéos sont conservées, sans ajouter de nom client, résultat ou preuve commerciale fictive.

### Secondaire — amélioration possible après mesure

- Étudier des variantes d'images responsives et le chargement des vidéos avec une comparaison visuelle dédiée. Les fichiers actuels n'ont pas été altérés pour obtenir artificiellement un meilleur score.
- Poursuivre la précision des conseils à partir de questions réelles des prospects, sans produire une série de pages locales similaires.
- Centraliser à terme les composants répétés et les informations d'offres pour éviter de nouvelles divergences. Aucune refonte du système de pages n'est nécessaire pour profiter des corrections présentes.

## Fichiers modifiés — liste exacte

Le [manifeste détaillé](finalisation-files.json) distingue les **41 fichiers de production modifiés pendant cette finalisation**, les **43 fichiers suivis modifiés au cumul depuis l'état initial de l'audit**, les 26 nouvelles ressources sous `css/vendor/` et les outils. Les deux fichiers qui portent seulement des corrections du 19 octobre au cumul sont `js/script.js` et `images/site.webmanifest`.

Les 41 fichiers modifiés pendant cette reprise sont :

```text
blog.html
blog/choisir-agence-web-lyon.html
blog/cout-site-vitrine-lyon.html
blog/importance-site-internet-2026.html
blog/landing-page-one-page-site-vitrine.html
blog/pourquoi-site-vitrine-artisan-lyon.html
blog/qui-sommes-nous-central-web-agency.html
blog/seo-local-apparaitre-premier-google.html
blog/site-vitrine-coach-sportif-lyon.html
blog/site-vitrine-mode-lyon.html
blog/site-vitrine-restaurant.html
cgv.html
conseils-backlinks.html
conseils-bouche-a-oreille.html
conseils-collaboration.html
conseils-google-business.html
conseils-reseaux-sociaux.html
conseils-seo.html
conseils-tenir-site-a-jour.html
conseils.html
contact.html
css/styles.css
css/styles.css.map
css/styles.scss
fiches-metiers/artisan-batiment.html
fiches-metiers/coach-sportif.html
fiches-metiers/coiffeur-barbier.html
fiches-metiers/estheticienne.html
fiches-metiers/metiers-du-droit.html
fiches-metiers/photographe.html
fiches-metiers/praticien-bien-etre.html
fiches-metiers/professionnels-sante.html
fiches-metiers/restaurant.html
fiches-metiers/vtc.html
index.html
mentions-legales.html
metiers.html
offres.html
services.html
sites-abonnement.html
sites-cle-en-main.html
```

Toutes les pages ont reçu les références locales des polices/icônes, le chargement différé du script et la correction sémantique des titres du pied de page. Les changements éditoriaux se limitent aux pages décrites dans ce rapport : accueil, hub du blog, CGV, dix articles, quatre conseils et trois fiches métier ; les autres contenus principaux sont conservés.

Nouveaux fichiers de ressources : `css/vendor/google-fonts.css`, `css/vendor/fontawesome.css`, vingt fichiers de polices et compatibilité dans `css/vendor/fonts/`, trois fichiers de licence et `css/vendor/sources.json`. Le manifeste donne chaque nom exact ; les polices ne sont pas résumées par une liste de noms approximatifs.

Outils mis à jour : `scripts/audit_site.py`, `scripts/browser_audit.py`. Outils ajoutés : `scripts/vendor_fonts.py`, `scripts/measure_mobile.py`, `scripts/verify_invariants.py`. `scripts/check_live.py` est conservé. Les scripts temporaires d'application des corrections ont été retirés.

Documents et preuves ajoutés : ce rapport, `cgv-validation-2026-10-20.md`, `test-reception-formulaire.md`, `finalisation-files.json`, `finalisation-before.json`, `finalisation-after.json`, `finalisation-invariants.json`, `finalisation-browser.json`, `finalisation-visual.json`, `mobile-comparison-2026-10-20.json` et les quatre rapports `mobile-before-1.json`, `mobile-before-2.json`, `mobile-after-1.json`, `mobile-after-2.json`.

Les documents du 19 octobre sont conservés comme référence. Aucun engagement de classement Google n'est formulé.
