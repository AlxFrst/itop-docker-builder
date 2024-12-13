import json
import os
import docker
import subprocess
from typing import Dict, List

def load_versions() -> Dict:
    with open('itop-versions.json', 'r') as f:
        return json.load(f)

def get_image_name(config: Dict) -> str:
    owner = os.environ.get('GITHUB_OWNER', 'local').lower()
    repo = os.environ.get('GITHUB_REPOSITORY', 'local/itop-docker-builder').split('/')[1].lower()
    return f"ghcr.io/{owner}/{repo}/itop:{config['version']}-php{config['php_version']}"

def get_existing_images(client: docker.DockerClient, owner: str) -> set:
    pattern = f"ghcr.io/{owner}"
    all_images = client.images.list()
    existing = set()
    
    for image in all_images:
        if image.tags:
            for tag in image.tags:
                if pattern in tag:
                    existing.add(tag)
    
    return existing

def build_image(config: Dict) -> str:
    image_name = get_image_name(config)
    print(f"Configuration de build pour {image_name}")
    cmd = [
        'docker', 'build',
        '--build-arg', f'PHP_VERSION={config["php_version"]}',
        '--build-arg', f'ITOP_VERSION={config["version"]}',
        '--build-arg', f'ITOP_URL={config["archive_url"]}',
        '-t', image_name,
        '.'
    ]
    subprocess.run(cmd, check=True)
    return image_name

def push_image(client: docker.DockerClient, image_name: str) -> None:
    print(f"Pushing image {image_name}")
    client.images.push(image_name)

def main():
    client = docker.from_env()
    config = load_versions()
    
    owner = os.environ.get('GITHUB_OWNER', 'local').lower()
    existing_images = get_existing_images(client, owner)
    
    print(f"Images existantes trouvées: {existing_images}")
    
    # Vérifie si on doit tout rebuilder (Dockerfile modifié)
    rebuild_all = os.environ.get('REBUILD_ALL', '').lower() == 'true'
    
    if rebuild_all:
        print("Reconstruction de toutes les images (Dockerfile modifié)")
        for image in config['images']:
            image_name = get_image_name(image)
            build_image(image)
            if 'GITHUB_OWNER' in os.environ:
                push_image(client, image_name)
            print(f"Image construite avec succès: {image_name}")
    else:
        print("Mode incrémental - construction uniquement des nouvelles images")
        for image in config['images']:
            image_name = get_image_name(image)
            if image_name not in existing_images:
                print(f"Construction de la nouvelle image: {image_name}")
                build_image(image)
                if 'GITHUB_OWNER' in os.environ:
                    push_image(client, image_name)
                print(f"Image construite avec succès: {image_name}")
            else:
                print(f"L'image existe déjà, ignorée: {image_name}")
    
    # Nettoyage des images obsolètes
    current_images = {get_image_name(img) for img in config['images']}
    for existing in existing_images:
        if existing not in current_images:
            print(f"Suppression de l'image obsolète: {existing}")
            client.images.remove(existing, force=True)

if __name__ == '__main__':
    main()
