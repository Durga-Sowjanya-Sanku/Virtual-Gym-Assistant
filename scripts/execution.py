import numpy as np
from app.scripts.body_part_angle import BodyPartAngle
from app.scripts.utils import *
import app.scripts.voice_assisstant as va

class TypeOfExercise(BodyPartAngle):
    def _init_(self, landmarks):
        super()._init_(landmarks)
        self.calories_spent = 0.0

    def calculate_calories(self, exercise_type, repetitions):
        # Example calorie burn rates (these are rough estimates)
        calories_per_rep = {
            "push-up": 0.29,  # Example value: calories per push-up
            "pull-up": 0.8,   # Example value: calories per pull-up
            "squat": 0.32,    # Example value: calories per squat
            "walk": 0.04,     # Example value: calories per step
            "sit-up": 0.15    # Example value: calories per sit-up
        }
        return calories_per_rep.get(exercise_type, 0) * repetitions

    def push_up(self, counter, status):
        left_arm_angle = self.angle_of_the_left_arm()
        right_arm_angle = self.angle_of_the_right_arm()
        avg_arm_angle = (left_arm_angle + right_arm_angle) // 2

        if status:
            if avg_arm_angle < 70:
                counter += 1
                status = False
        else:
            if avg_arm_angle > 160:
                status = True

        calories = self.calculate_calories("push-up", counter)
        return [counter, status, calories]

    def pull_up(self, counter, status):
        nose = detection_body_part(self.landmarks, "NOSE")
        left_elbow = detection_body_part(self.landmarks, "LEFT_ELBOW")
        right_elbow = detection_body_part(self.landmarks, "RIGHT_ELBOW")
        avg_shoulder_y = (left_elbow[1] + right_elbow[1]) / 2

        if status:
            if nose[1] > avg_shoulder_y:
                counter += 1
                status = False
        else:
            if nose[1] < avg_shoulder_y:
                status = True

        calories = self.calculate_calories("pull-up", counter)
        return [counter, status, calories]

    def squat(self, counter, status):
        left_leg_angle = self.angle_of_the_left_leg()
        right_leg_angle = self.angle_of_the_right_leg()
        avg_leg_angle = (left_leg_angle + right_leg_angle) // 2

        if status:
            if avg_leg_angle < 70:
                counter += 1
                status = False
        else:
            if avg_leg_angle > 160:
                status = True

        calories = self.calculate_calories("squat", counter)
        return [counter, status, calories]

    def walk(self, counter, status):
        right_knee = detection_body_part(self.landmarks, "RIGHT_KNEE")
        left_knee = detection_body_part(self.landmarks, "LEFT_KNEE")

        if status:
            if left_knee[0] > right_knee[0]:
                counter += 1
                status = False
        else:
            if left_knee[0] < right_knee[0]:
                counter += 1
                status = True

        calories = self.calculate_calories("walk", counter)
        return [counter, status, calories]

    def sit_up(self, counter, status):
        angle = self.angle_of_the_abdomen()
        if status:
            if angle < 55:
                counter += 1
                status = False
        else:
            if angle > 105:
                status = True

        calories = self.calculate_calories("sit-up", counter)
        return [counter, status, calories]

    def calculate_exercise(self, exercise_type, counter, status):
        if exercise_type == "push-up":
            counter, status,calories = TypeOfExercise(self.landmarks).push_up(
                counter, status)
        elif exercise_type == "pull-up":
            counter, status,calories = TypeOfExercise(self.landmarks).pull_up(
                counter, status)
        elif exercise_type == "squat":
            counter, status,calories = TypeOfExercise(self.landmarks).squat(
                counter, status)
        elif exercise_type == "walk":
            counter, status,calories = TypeOfExercise(self.landmarks).walk(
                counter, status)
        elif exercise_type == "sit-up":
            counter, status,calories = TypeOfExercise(self.landmarks).sit_up(
                counter, status)

        return [counter, status,calories]