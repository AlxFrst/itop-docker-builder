# iTop Docker Builder

Ce projet permet de générer automatiquement des images Docker pour différentes versions d'iTop avec différentes versions de PHP. Les images sont publiées sur GitHub Container Registry (ghcr.io).

## Structure du projet

```
itop-docker-builder/
├── .github/
│   └── workflows/
│       └── docker-build.yml
├── Dockerfile
├── itop-versions.json
├── build_images.py
└── README.md
```

## Configuration

1. Le fichier `itop-versions.json` contient la configuration des images à construire :
   - version : Version d'iTop
   - php_version : Version de PHP
   - archive_url : URL de téléchargement d'iTop

2. Permissions GitHub :
   - Le workflow utilise automatiquement `GITHUB_TOKEN` pour publier les images
   - Assurez-vous que les "Packages" sont activés dans les paramètres de votre repository

## Utilisation

1. Pour ajouter une nouvelle version d'iTop :
   - Modifiez le fichier `itop-versions.json`
   - Ajoutez une nouvelle entrée dans le tableau `images`
   - Committez et poussez les modifications

2. Pour supprimer une version :
   - Supprimez l'entrée correspondante dans `itop-versions.json`
   - Committez et poussez les modifications

Le workflow GitHub Actions se déclenchera automatiquement à chaque modification du Dockerfile ou du fichier JSON.

## Format des images

Les images sont publiées sous le format :
```
ghcr.io/[owner]/[repository]/itop:[version]-php[php_version]
```

Par exemple :
```
ghcr.io/username/itop-docker-builder/itop:3.2.0-php8.1
```

## Tests locaux

Pour tester localement :

```bash
# Installer les dépendances
pip install docker

# Définir les variables d'environnement
export GITHUB_OWNER="votre-username"
export GITHUB_REPOSITORY="votre-username/itop-docker-builder"

# Lancer le script de build
python build_images.py
```

## Maintenance

Les images obsolètes (qui ne sont plus dans le fichier JSON) seront automatiquement supprimées lors de l'exécution du script.
