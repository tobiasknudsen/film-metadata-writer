import argparse
import json
import os
import sys


def is_bad_version(image: str, picture_metadata: dict) -> bool:
    latitude = picture_metadata["location"].split(";")[0]
    longitude = picture_metadata["location"].split(";")[1]
    google_maps_url = f"https://www.google.com/maps/place/{latitude},{longitude}"
    response = None

    while response not in ["y", "n"]:
        response = input(
            "\n"
            f"Image: {image}\n"
            f"Date: {picture_metadata['time']}\n"
            f"Google Maps URL: {google_maps_url}\n"
            "Is this correct? (y/n) "
        )

    return response == "n"


def find_missing_metadata(images: list[str], pictures_metadata: list[dict]) -> int:
    left, right = 0, len(images) - 1

    while left < right:
        mid = (left + right) // 2

        if is_bad_version(images[mid], pictures_metadata[mid]):
            right = mid
        else:
            left = mid + 1

    return left


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

    args = parser.parse_args()

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

    missing_metadata = False
    missing_images = False

    if len(images) == len(pictures_metadata):
        print("All images should have metadata")
        sys.exit(1)
    elif len(images) < len(pictures_metadata):
        print(f"Missing {len(pictures_metadata) - len(images)} images")
        missing_images = True
    else:
        print(f"Missing metadata for {len(images) - len(pictures_metadata)} images")
        missing_metadata = True

    missing_metadata_index = find_missing_metadata(
        images=images, pictures_metadata=pictures_metadata
    )

    if missing_images:
        print(f"Missing image {images[missing_metadata_index]}")
    elif missing_metadata:
        print(f"Missing metadata for image {images[missing_metadata_index]}")


if __name__ == "__main__":
    main()
