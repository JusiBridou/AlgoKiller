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

Le CSV doit contenir des en‑têtes avec *nom* et *email* (ex: `nom,email`). Les séparateurs `,` ou `;` sont acceptés.

### Fichier missions (TXT)

Une mission par ligne (les lignes vides sont ignorées). Il doit y avoir au moins autant de missions que de cibles.

### Exemples de commandes

- Générer et exporter les attributions sans envoyer d’email :

`python algo_killer.py --participants participants.csv --missions missions.txt --dry-run --output attributions.csv`

- Envoyer les emails (SMTP) :

`python algo_killer.py --participants participants.csv --missions missions.txt --smtp-host smtp.example.com --smtp-user moncompte --smtp-password monmdp --sender killer@example.com`

> Par defaut, un fichier `attributions.csv` est genere a chaque execution dans le dossier du script.
> Pour plus de confort, vous pouvez definir les variables d’environnement `SMTP_HOST`, `SMTP_PORT`, `SMTP_USER`, `SMTP_PASSWORD`, `SMTP_SENDER`.

## Règle d’arrêt

L’attribution se fait en **une seule boucle**. Une fois que tous les participants obtiennent une cible et une mission, l'algorithme s'arrête.

## Contraintes

Pour que l'envoie d'email fonctionne, il faut que tous les emails du fichier participants.csv soient uniques.