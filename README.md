# iTop Docker Builder

Ce projet permet de générer automatiquement des images Docker pour différentes versions d'iTop avec différentes versions de PHP.

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
   - image_tag : Tag de l'image Docker

2. Configurez les secrets GitHub suivants :
   - `DOCKERHUB_USERNAME` : Votre nom d'utilisateur Docker Hub
   - `DOCKERHUB_TOKEN` : Votre token d'accès Docker Hub

## Utilisation

1. Pour ajouter une nouvelle version d'iTop :
   - Modifiez le fichier `itop-versions.json`
   - Ajoutez une nouvelle entrée dans le tableau `images`
   - Committez et poussez les modifications

2. Pour supprimer une version :
   - Supprimez l'entrée correspondante dans `itop-versions.json`
   - Committez et poussez les modifications

Le workflow GitHub Actions se déclenchera automatiquement à chaque modification du Dockerfile ou du fichier JSON.

## Tests locaux

Pour tester localement :

```bash
# Installer les dépendances
pip install docker

# Lancer le script de build
python build_images.py
```

## Maintenance

Les images obsolètes (qui ne sont plus dans le fichier JSON) seront automatiquement supprimées lors de l'exécution du script.
