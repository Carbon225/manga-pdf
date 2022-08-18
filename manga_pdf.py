from typing import List, Iterable
import os
import argparse
from PIL import Image
import pillow_avif
import re


def get_image_number(path: str) -> int:
    return int(re.match(r'^(\d+)\.(.+)$', os.path.basename(path)).group(1))


def find_files_in_directory(directory: str) -> Iterable[str]:
    for root, _, files in os.walk(directory):
        for file in files:
            if re.match(r'^\d+\..+$', file):
                yield os.path.join(root, file)
            else:
                print(f'Skipping {os.path.join(root, file)}')


def find_files_in_sources(sources: List[str]) -> Iterable[str]:
    for directory in sources:
        yield from sorted(find_files_in_directory(directory), key=get_image_number)


def create_pdf(output: str, sources: List[str]):
    print('Discovering files...')
    img_paths = list(find_files_in_sources(sources))
    if not img_paths:
        raise Exception('No images found')
    print(f'Found {len(img_paths)} images')

    images = []
    try:
        print('Loading images...')
        for path in img_paths:
            images.append(Image.open(path))
        print('Saving PDF...')
        images[0].save(output, save_all=True, append_images=images[1:])
        print('Done')
    finally:
        for img in images:
            img.close()


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('output')
    parser.add_argument('sources', nargs='+')
    args = parser.parse_args()
    create_pdf(args.output, args.sources)
