# Growatt battery monitor

Affiche le niveau de batterie de l'onduleur WIT sur une page web,
mise à jour automatiquement toutes les 10 minutes.

## Mise en place (une seule fois)

### 1. Créer un compte GitHub (si tu n'en as pas)
https://github.com/signup — gratuit.

### 2. Créer un nouveau dépôt
- Sur github.com, clique sur le "+" en haut à droite > "New repository".
- Nom : `growatt-battery-monitor` (ou ce que tu veux).
- Visibilité : Private (recommandé, pour que le cookie et les identifiants
  restent invisibles publiquement — GitHub Secrets restent privés même
  sur un dépôt public, mais autant être prudent).
- Ne coche aucune case d'initialisation (pas de README, pas de .gitignore).
- Clique "Create repository".

### 3. Envoyer ces fichiers dans le dépôt
Sur ta machine, dans le dossier qui contient ce README :

```
git init
git add .
git commit -m "Initial setup"
git branch -M main
git remote add origin https://github.com/TON-UTILISATEUR/growatt-battery-monitor.git
git push -u origin main
```

(Remplace TON-UTILISATEUR par ton nom d'utilisateur GitHub. Il te
demandera de t'authentifier — suis les instructions à l'écran.)

### 4. Ajouter les secrets
Sur la page du dépôt GitHub : Settings > Secrets and variables > Actions
> "New repository secret". Ajoute ces trois secrets :

- `GROWATT_COOKIE` : le cookie complet copié depuis le navigateur
  (celui qu'on a utilisé pour les tests)
- `GROWATT_PLANT_ID` : 10229210
- `GROWATT_WIT_SN` : 0XJT10ZD21JF0001

### 5. Activer GitHub Pages
Settings > Pages > Source > choisis "Deploy from a branch" >
Branch : `main`, dossier : `/docs` > Save.

Après 1-2 minutes, ta page sera disponible à une adresse du type :
`https://TON-UTILISATEUR.github.io/growatt-battery-monitor/`

### 6. Lancer le workflow une première fois manuellement
Onglet "Actions" du dépôt > "Update battery data" > "Run workflow".
Ça va créer le premier `battery.json`. Ensuite il tournera tout seul
toutes les 10 minutes.

### 7. Sur ton iPhone 8+
Ouvre l'adresse GitHub Pages dans Safari > bouton Partager >
"Sur l'écran d'accueil". Tu auras une icône dédiée qui ouvre la page
en plein écran, comme une vraie appli.

## Quand le cookie/token expire

Si la page affiche "Accès Growatt indisponible", il faut récupérer un
nouveau cookie/token (reconnexion sur server.growatt.com dans un navigateur,
outils développeur > onglet Réseau > copier l'en-tête Cookie d'une
requête), puis mettre à jour le secret `GROWATT_COOKIE` sur GitHub
(Settings > Secrets > GROWATT_COOKIE > Update).

Si tu utilises un token permanent (Plant Manager > Settings > API Token),
utilise-le de la même façon dans le secret `GROWATT_COOKIE` — le script
l'envoie dans l'en-tête `Cookie` de la requête, exactement comme un
cookie de session classique. S'il s'avère qu'il faut l'envoyer autrement
(paramètre séparé, en-tête dédié...), dis-le à Claude pour ajuster le
script `fetch_battery.py`.

## Indicateurs affichés

- % batterie (SOC)
- Puissance produite par les panneaux
- Puissance envoyée à la batterie (charge/décharge)
- Puissance consommée par la maison
- Puissance injectée sur le réseau / soutirée du réseau

