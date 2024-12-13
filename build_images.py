import json
import os
import docker
import subprocess
from typing import Dict, List

def load_versions() -> Dict:
    with open('itop-versions.json', 'r') as f:
        return json.load(f)

def get_existing_images(client: docker.DockerClient) -> set:
    return {tag for image in client.images.list() 
            for tag in image.tags if 'ghcr.io' in tag}

def get_image_name(config: Dict) -> str:
    # Format: ghcr.io/owner/repository/image:tag
    owner = os.environ['GITHUB_OWNER'].lower()
    repo = os.environ['GITHUB_REPOSITORY'].split('/')[1].lower()
    return f"ghcr.io/{owner}/{repo}/itop:{config['version']}-php{config['php_version']}"

def build_image(config: Dict) -> str:
    image_name = get_image_name(config)
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
    client.images.push(image_name)

def main():
    client = docker.from_env()
    config = load_versions()
    existing_images = get_existing_images(client)
    
    for image in config['images']:
        image_name = get_image_name(image)
        if image_name not in existing_images:
            print(f"Building {image_name}")
            build_image(image)
            push_image(client, image_name)
            print(f"Successfully built and pushed {image_name}")
    
    # Cleanup obsolete images
    current_images = {get_image_name(img) for img in config['images']}
    for existing in existing_images:
        if existing not in current_images:
            print(f"Removing obsolete image: {existing}")
            client.images.remove(existing, force=True)

if __name__ == '__main__':
    main()
