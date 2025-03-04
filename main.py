import argparse
import mediapipe as mp
from halo import Halo

from utils import (
    download_task_file,
    get_detector,
    get_landmark,
    calculate_distance,
    consolidate,
)
from models import Measurements
from constants import ClothingItem, OUTPUT_PATH


def setup_cli():
    parser = argparse.ArgumentParser(description="ML sewing pattern generator")
    parser.add_argument(
        "-i",
        "--image",
        type=str,
        required=True,
        help="Path to the image file",
    )
    parser.add_argument(
        "-o",
        "--output",
        type=str,
        required=False,
        default=OUTPUT_PATH,
        help="Path to the output file",
    )
    parser.add_argument(
        "-g",
        "--garment",
        type=ClothingItem,
        required=True,
        help="Garment type",
    )

    return parser.parse_args()


if __name__ == "__main__":
    args = setup_cli()

    download_task_file()

    mp_image = mp.Image.create_from_file(args.image)
    mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=mp_image)

    spinner = Halo(text="Loading pose landmark model", spinner="dots")
    spinner.start()

    detector = get_detector()
    spinner.stop()

    spinner = Halo(text="Detecting pose landmarks from image", spinner="dots")
    spinner.start()

    detection_result = detector.detect(mp_image)
    landmarks = detection_result.pose_landmarks[0]

    spinner.stop()

    # Calculate distance between shoulder blades
    left_shoulder = get_landmark(landmarks, "LEFT_SHOULDER")
    right_shoulder = get_landmark(landmarks, "RIGHT_SHOULDER")
    shoulder_distance = calculate_distance(
        left_shoulder.x, left_shoulder.y, right_shoulder.x, right_shoulder.y
    )
    print(f"Shoulder distance: {shoulder_distance}")

    # Calculate distance between hips
    left_hip = get_landmark(landmarks, "LEFT_HIP")
    right_hip = get_landmark(landmarks, "RIGHT_HIP")
    waist_distance = calculate_distance(
        left_hip.x, left_hip.y, right_hip.x, right_hip.y
    )
    print(f"Waist distance: {waist_distance}")

    # Calculate distance between left shoulder to elbow
    left_elbow = get_landmark(landmarks, "LEFT_ELBOW")
    left_shoulder_to_elbow_distance = calculate_distance(
        left_shoulder.x, left_shoulder.y, left_elbow.x, left_elbow.y
    )
    print(f"Left Shoulder to elbow distance: {left_shoulder_to_elbow_distance}")

    right_elbow = get_landmark(landmarks, "RIGHT_ELBOW")
    right_shoulder_to_elbow_distance = calculate_distance(
        right_shoulder.x, right_shoulder.y, right_elbow.x, right_elbow.y
    )
    print(f"Right Shoulder to elbow distance: {right_shoulder_to_elbow_distance}")

    # Calculate distance between left elbow to wrist
    left_wrist = get_landmark(landmarks, "LEFT_WRIST")
    left_elbow_to_wrist_distance = calculate_distance(
        left_elbow.x, left_elbow.y, left_wrist.x, left_wrist.y
    )
    print(f"Left Elbow to wrist distance: {left_elbow_to_wrist_distance}")

    # Calculate distance between right shoulder to elbow
    shoulder_to_elbow_distance = calculate_distance(
        right_shoulder.x, right_shoulder.y, right_elbow.x, right_elbow.y
    )
    print(f"Right Shoulder to elbow distance: {shoulder_to_elbow_distance}")

    # Calculate distance between right elbow to wrist
    right_wrist = get_landmark(landmarks, "RIGHT_WRIST")
    right_elbow_to_wrist_distance = calculate_distance(
        right_elbow.x, right_elbow.y, right_wrist.x, right_wrist.y
    )

    # Calculate distance between left shoulder to hip
    left_shoulder_to_hip_distance = calculate_distance(
        left_shoulder.x, left_shoulder.y, left_hip.x, left_hip.y
    )
    print(f"Left Shoulder to hip distance: {left_shoulder_to_hip_distance}")

    # Calculate distance between right shoulder to hip
    right_shoulder_to_hip_distance = calculate_distance(
        right_shoulder.x, right_shoulder.y, right_hip.x, right_hip.y
    )
    print(f"Right Shoulder to hip distance: {right_shoulder_to_hip_distance}")

    # Calculate distance between left hip to knee
    left_knee = get_landmark(landmarks, "LEFT_KNEE")
    left_hip_to_knee_distance = calculate_distance(
        left_hip.x, left_hip.y, left_knee.x, left_knee.y
    )
    print(f"Left Hip to knee distance: {left_hip_to_knee_distance}")

    # Calculate distance between right hip to knee
    right_knee = get_landmark(landmarks, "RIGHT_KNEE")
    right_hip_to_knee_distance = calculate_distance(
        right_hip.x, right_hip.y, right_knee.x, right_knee.y
    )
    print(f"Right Hip to knee distance: {right_hip_to_knee_distance}")

    # Calculate distance between left knee to ankle
    left_ankle = get_landmark(landmarks, "LEFT_ANKLE")
    left_knee_to_ankle_distance = calculate_distance(
        left_knee.x, left_knee.y, left_ankle.x, left_ankle.y
    )
    print(f"Left Knee to ankle distance: {left_knee_to_ankle_distance}")

    # Calculate distance between right knee to ankle
    right_ankle = get_landmark(landmarks, "RIGHT_ANKLE")
    right_knee_to_ankle_distance = calculate_distance(
        right_knee.x, right_knee.y, right_ankle.x, right_ankle.y
    )
    print(f"Right Knee to ankle distance: {right_knee_to_ankle_distance}")

    measurements = Measurements(
        wrist_to_elbow=consolidate(
            left_elbow_to_wrist_distance, right_elbow_to_wrist_distance
        ),
        elbow_to_shoulder=consolidate(
            left_shoulder_to_elbow_distance, right_shoulder_to_elbow_distance
        ),
        shoulder_to_shoulder=shoulder_distance,
        waist_to_knee=consolidate(
            left_hip_to_knee_distance, right_hip_to_knee_distance
        ),
        knee_to_ankle=consolidate(
            left_knee_to_ankle_distance, right_knee_to_ankle_distance
        ),
        waist=waist_distance,
    )

    print(measurements)
