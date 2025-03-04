from pydantic import BaseModel


class Measurements(BaseModel):
    wrist_to_elbow: float
    elbow_to_shoulder: float
    shoulder_to_shoulder: float
    waist_to_knee: float
    knee_to_ankle: float
    waist: float
