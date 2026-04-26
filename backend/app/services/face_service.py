import face_recognition
import base64
import numpy as np
import cv2
import re

def base64_to_image(base64_str):
    base64_str = re.sub('^data:image/.+;base64,', '', base64_str)

    image_bytes = base64.b64decode(base64_str)
    np_arr = np.frombuffer(image_bytes, np.uint8)

    image = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)

    return image


def get_face_encodings(image_base64):
    image = base64_to_image(image_base64)

    if image is None:
        return []

    rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    face_locations = face_recognition.face_locations(rgb)
    encodings = face_recognition.face_encodings(rgb, face_locations)

    return encodings  # return list


def compare_faces(known_encodings, unknown_encoding):
    results = face_recognition.compare_faces(known_encodings, unknown_encoding)
    face_distances = face_recognition.face_distance(known_encodings, unknown_encoding)

    if len(face_distances) == 0:
        return None

    best_match_index = np.argmin(face_distances)

    if results[best_match_index]:
        return best_match_index

    return None