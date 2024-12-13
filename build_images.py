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
            for tag in image.tags if 'itop:' in tag}

def build_image(config: Dict) -> None:
    cmd = [
        'docker', 'build',
        '--build-arg', f'PHP_VERSION={config["php_version"]}',
        '--build-arg', f'ITOP_VERSION={config["version"]}',
        '--build-arg', f'ITOP_URL={config["archive_url"]}',
        '-t', config["image_tag"],
        '.'
    ]
    subprocess.run(cmd, check=True)

def push_image(client: docker.DockerClient, tag: str) -> None:
    repository = f'{os.environ["DOCKER_USERNAME"]}/{tag}'
    client.images.push(repository)

def main():
    client = docker.from_env()
    config = load_versions()
    existing_images = get_existing_images(client)
    
    for image in config['images']:
        if image['image_tag'] not in existing_images:
            print(f"Building {image['image_tag']}")
            build_image(image)
            push_image(client, image['image_tag'])
            print(f"Successfully built and pushed {image['image_tag']}")
    
    # Cleanup obsolete images
    current_tags = {img['image_tag'] for img in config['images']}
    for existing in existing_images:
        if existing not in current_tags:
            print(f"Removing obsolete image: {existing}")
            client.images.remove(existing, force=True)

if __name__ == '__main__':
    main()
