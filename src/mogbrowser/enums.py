from enum import StrEnum

class PathType(StrEnum):
    DIRECTORY = "directory"
    IMAGE = "image"
    VIDEO = "video"
    OTHER = "other"