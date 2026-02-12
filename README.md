# Algorithme de génération de Killer
## Règles du jeu

Chacun reçoit une cible 🎯 et une action à lui faire réaliser 🤫 sans se faire repérer. Une fois ta cible 'éliminée 💀', tu récupères sa mission et tu continues jusqu’à ce qu’il ne reste qu’un survivant 🏆. 

Pas de violence, pas de mise en danger 🚫⚠️, juste de la ruse 🕵️, de la créativité 🎨 et beaucoup de finesse.

## Exemple

Jusi reçoit la cible "Loga" 🎯 et la mission "Me servir à boire 🍹". 

Sa mission est donc de se faire servir à boire par Loga 🤫. Imaginons que durant le week‑end Loga décide de servir à boire à Jusi : elle a perdu ❌,
et Jusi récupère alors la cible de Loga 🎯 et la mission de Loga 📜. 

Loga ne peut plus jouer, mais elle peut encore aider les autres 🕵️‍♀️ à éliminer leurs cibles.

## Utilisation rapide

### Fichier participants (CSV)

Le CSV doit contenir des en-tetes avec *nom* et *email* (ex: `nom,email`). Les separateurs `,` ou `;` sont acceptes.

Pour rendre le jeu plus accessible il est possible d'ajouter une colonne `categories_bannies` au fichier CSV. Cette colonne peut servir à bannir certaines missions pour certaines cibles. Par exemple, si une des missions disponible est "Faire 100 pompes" et  qu'un des particpants ne peut pas en faire alors il peut bannir la catégorie "sport" pour ne pas avoir à faire cette mission.

Un participant peut bannir plusieurs catégories, ou aucune.

Exemple :

| nom  | email             | categories_bannies |
| ---- | ----------------- | ------------------ |
| Jusi | jusi@example.com  | prank              |
| Loga | loga@example.com  | sport,social       |
| Ino  | ino@example.com   |                    |
### Fichier missions (CSV)

Le CSV doit contenir une colonne `mission`. Une colonne `categories` optionnelle peut lister des categories. Il doit y avoir au moins autant de missions que de cibles.

Exemple :

| mission  | categories             |
| ---- | ----------------- |
| te laisser faire son vernis | art  |
| faire 5 pompes ou 1 seconde de gainage | sport  |
| porter tes chaussures  | prank   |
| hurler de toutes ses forces  | social   |
| imiter les gestes de quelqu'un devant lui  | social   |

### Exemples de commandes

- Générer et exporter les attributions sans envoyer d’email :

`python algo_killer.py --participants participants.csv --missions missions.csv --dry-run --output attributions.csv`

- Envoyer les emails (SMTP) :

`python algo_killer.py --participants participants.csv --missions missions.csv --smtp-host smtp.example.com --smtp-user moncompte --smtp-password monmdp --sender killer@example.com`

> Par defaut, un fichier `attributions.csv` est genere a chaque execution dans le dossier du script.
> Pour plus de confort, vous pouvez definir les variables d’environnement `SMTP_HOST`, `SMTP_PORT`, `SMTP_USER`, `SMTP_PASSWORD`, `SMTP_SENDER`.

## Règle d’arrêt

L’attribution se fait en **une seule boucle**. Une fois que tous les participants obtiennent une cible et une mission, l'algorithme s'arrête.

## Contraintes

Pour que l'envoie d'email fonctionne, il faut que tous les emails du fichier participants.csv soient uniques.