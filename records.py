import pydantic

from utils import (
    get_aperture,
    get_capture_datetime,
    get_iso,
    get_shutter_speed,
)


class LatLngRecord(pydantic.BaseModel):
    latitude: float
    longitude: float


class ExifRecord(pydantic.BaseModel):
    Make: str  # Canon
    Model: str  # Canon EOS 6D
    ExposureTime: float  # 0.03333333333
    FNumber: float  # 3.2
    ISO: int  # 640
    DateTimeOriginal: str  # 2024:12:05 10:14:58
    CreatedTime: str  # 2024:12:05 10:14:58
    ShutterSpeedValue: float  # 0.03333333333
    ApertureValue: float  # 3.2
    FocalLength: int  # 28
    LensModel: str  # Canon FD 28mm 1:2.8
    LensInfo: str  # 28 28 undef undef
    GPSLatitudeRef: str = "N"
    GPSLatitude: float  # 62.0
    GPSLongitudeRef: str = "E"
    GPSLongitude: float  # 10.0

    @classmethod
    def from_picture_metadata(cls, picture: dict) -> "ExifRecord":
        return cls(
            Make=picture["camera"]["name"].split(" ")[0],
            Model=picture["camera"]["name"],
            ExposureTime=get_shutter_speed(picture),
            FNumber=get_aperture(picture["aperture"]),
            ISO=get_iso(picture),
            CreatedTime=get_capture_datetime(picture),
            DateTimeOriginal=get_capture_datetime(picture),
            ShutterSpeedValue=get_shutter_speed(picture),
            ApertureValue=get_aperture(picture["aperture"]),
            FocalLength=picture["lens"]["focal_length"],
            LensModel=picture["lens"]["name"],
            LensInfo=picture["lens"]["name"],
            GPSLatitude=float(picture["location"].split(";")[0]),
            GPSLongitude=float(picture["location"].split(";")[1]),
        )
