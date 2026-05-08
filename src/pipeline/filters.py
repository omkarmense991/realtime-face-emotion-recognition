def keep_largest_face(detections):

    if not detections:
        return []

    return [max(detections, key=lambda d: d["bbox"][2] * d["bbox"][3])]


def is_valid_detection(det, min_confidence):

    return det["confidence"] >= min_confidence


def is_valid_face_size(w, h, min_face_size):

    return w >= min_face_size and h >= min_face_size
