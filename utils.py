import subprocess
from datetime import datetime


def ensure_exiftool():
    try:
        subprocess.run(
            ["exiftool", "--version"], check=True, capture_output=True, encoding="utf-8"
        )
        return True
    except FileNotFoundError:
        return False


def get_iso(picture) -> int:
    # "400" -> 400
    return int(picture["speed"])


def get_aperture(aperture_string: str) -> float:
    # f/5.6 -> 5.6
    return float(aperture_string.split("/")[-1])


def get_shutter_speed(picture) -> float:
    # 1/250 -> 0,004
    return 1 / float(picture["shutterspeed"].split("/")[1])


def get_capture_datetime(picture) -> datetime:
    # "2024-12-05T10:14:58+01:00" -> "2024-12-05 10:14:58"
    return datetime.strptime(picture["time"], "%Y-%m-%dT%H:%M:%S%z").strftime(
        "%Y:%m:%d %H:%M:%S"
    )


def get_lens_info(picture) -> str:
    focal_length = picture["lens"]["focal_length"]
    min_focal_length = picture["lens"]["min_focal_length"]
    max_focal_length = picture["lens"]["max_focal_length"]
    min_aperture = get_aperture(picture["lens"]["min_aperture"])
    max_aperture = get_aperture(picture["lens"]["max_aperture"])

    if max_focal_length == 0 and min_focal_length == -1:
        return f"{focal_length} {focal_length} undef undef"
    else:
        return f"{min_focal_length} {max_focal_length} {min_aperture} {max_aperture}"
