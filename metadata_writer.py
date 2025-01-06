import argparse
import json
import os
import sys

from exiftool import ExifToolHelper

from records import ExifRecord
from utils import ensure_exiftool


def write_metadata(
    *,
    images: list[str],
    pictures_metadata: list[dict],
    params: list[str],
):
    with ExifToolHelper() as et:
        for i in range(len(images)):
            image = images[i]
            picture_metadata = pictures_metadata[i]
            exif_data = ExifRecord.from_picture_metadata(picture_metadata)
            et.set_tags([image], exif_data.model_dump(), params=params)
            print(image + " Done")


def main():
    parser = argparse.ArgumentParser()

    parser.add_argument(
        dest="images_path",
        help="Path to images",
    )

    parser.add_argument(
        dest="metadata_path",
        help="Path to metadata file",
    )

    parser.add_argument(
        "-e",
        "--extension",
        dest="file_extension",
        help="File extension",
        required=False,
        default=".jpg",
    )

    parser.add_argument(
        "--overwrite-original",
        dest="overwrite_original",
        help="Overwrite original files",
        action="store_true",
        required=False,
        default=False,
    )

    args = parser.parse_args()

    if not ensure_exiftool():
        print("Exiftool is not installed")
        sys.exit(1)

    # Load the metadata from the metadata.json file
    with open(args.metadata_path, "r") as f:
        metadata = json.load(f)
        pictures_metadata = metadata["pictures"]
        pictures_metadata.sort(key=lambda p: p["frame_number"])

    # Get the files in the images folder
    images = [
        os.path.join(args.images_path, f)
        for f in sorted(os.listdir(args.images_path))
        if f.lower().endswith(args.file_extension.lower())
    ]

    if len(images) != len(pictures_metadata):
        print(
            f"""
            The number of images in the folder ({len(images)}) does not
            match the number of images in the metadata file ({len(pictures_metadata)})
            """
        )
        sys.exit(1)

    params = []
    if args.overwrite_original:
        params.append("-overwrite_original")

    write_metadata(images=images, pictures_metadata=pictures_metadata, params=params)


if __name__ == "__main__":
    main()
