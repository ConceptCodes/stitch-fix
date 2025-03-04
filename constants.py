from enum import Enum, auto

SCALE_FACTOR = 0.393701
TASK_PATH = "assets/pose_landmarker_heavy.task"
TASK_URL = "https://storage.googleapis.com/mediapipe-models/pose_landmarker/pose_landmarker_heavy/float16/1/pose_landmarker_heavy.task"
OUTPUT_PATH = "assets/output"


class ClothingItem(Enum):
    SHIRT = auto()
    PANTS = auto()
