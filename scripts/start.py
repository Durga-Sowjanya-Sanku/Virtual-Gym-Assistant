import mediapipe as mp
import cv2 as cv
import pandas as pd
import numpy as np
from app.scripts.body_part_angle import BodyPartAngle
from app.scripts.types_of_exercise import TypeOfExercise
from app.scripts.utils import *
import app.scripts.voice_assisstant as va
import datetime

mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose

video_path = "C:\\Users\\srini\\OneDrive\\Desktop\\nithya\\squat.mp4"

def exercise(exercise_name):
    va.speak("starting"+exercise_name)
    st=datetime.datetime.now()
    global results
    with mp_pose.Pose(min_detection_confidence=0.5,  # initializing the body pose estimation model
                      min_tracking_confidence=0.5) as pose:
        counter = 0
        status = True
        cam = cv.VideoCapture(video_path)
        cam.set(3, 800)
        cam.set(4, 480)

        while cam.isOpened():
            check, video = cam.read()
            if not check:
                break

            video = cv.resize(video, (800, 480), interpolation=cv.INTER_AREA)
            video = cv.cvtColor(video, cv.COLOR_BGR2RGB)
            video.flags.writeable = False
            results = pose.process(video)
            video.flags.writeable = True
            video = cv.cvtColor(video, cv.COLOR_RGB2BGR)

            try:
                landmarks = results.pose_landmarks.landmark
                counter, status = TypeOfExercise(landmarks).calculate_exercise(
                    exercise_name, counter, status)
            except:
                pass

            video = score_table(exercise_name, video, counter, status)

            mp_drawing.draw_landmarks(
                video,
                results.pose_landmarks,
                mp_pose.POSE_CONNECTIONS,
                mp_drawing.DrawingSpec(color=(255, 255, 255),
                                       thickness=2,
                                       circle_radius=2),
                mp_drawing.DrawingSpec(color=(174, 139, 45),
                                       thickness=2,
                                       circle_radius=2),
            )

            cv.imshow('Video', video)
            key = cv.waitKey(1)
            if key == ord('q'):
                break
        en=datetime.datetime.now()
        calories=calculate_calories(exercise_name,counter)
        values=[exercise_name,st,en,counter,calories]
        cam.release()
        cv.destroyAllWindows()
    return values



def calculate_calories(exercise_type, repetitions):
        # Example calorie burn rates (these are rough estimates)
        calories_per_rep = {
            "push-up": 0.29,  # Example value: calories per push-up
            "pull-up": 0.8,   # Example value: calories per pull-up
            "squat": 0.32,    # Example value: calories per squat
            "walk": 0.04,     # Example value: calories per step
            "sit-up": 0.15    # Example value: calories per sit-up
        }
        return calories_per_rep.get(exercise_type, 0) * repetitions