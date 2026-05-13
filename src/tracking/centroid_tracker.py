import math

from src.config.settings import TRACKING_MAX_DISTANCE


class CentroidTracker:
    """
    Lightweight centroid-based
    face tracking system.

    Maintains persistent track IDs
    across frames by matching
    face centroids using Euclidean
    distance.

    Designed for realtime webcam
    tracking with low computational
    overhead.
    """

    def __init__(self):

        self.next_track_id = 0

        self.tracked_faces = {}

        self.max_distance = TRACKING_MAX_DISTANCE

        self.active_track_ids = set()

    def calculate_centroid(
        self,
        bbox,
    ):

        x, y, w, h = bbox

        centroid_x = x + (w // 2)

        centroid_y = y + (h // 2)

        return (
            centroid_x,
            centroid_y,
        )

    def calculate_distance(
        self,
        centroid1,
        centroid2,
    ):

        return math.dist(
            centroid1,
            centroid2,
        )

    def update(
        self,
        detections,
    ):

        updated_tracks = {}

        used_track_ids = set()

        for det in detections:

            bbox = det["bbox"]

            centroid = self.calculate_centroid(bbox)

            matched_track_id = None

            min_distance = float("inf")

            # loop over old tracks to  Find nearest old track
            for (
                track_id,
                old_centroid,
            ) in self.tracked_faces.items():

                if track_id in used_track_ids:
                    continue

                distance = self.calculate_distance(
                    centroid,
                    old_centroid,
                )

                if distance < min_distance:

                    min_distance = distance

                    matched_track_id = track_id

            # Reuse existing track
            if matched_track_id is not None and min_distance < self.max_distance:

                track_id = matched_track_id

            else:

                # Create new track
                track_id = self.next_track_id

                self.next_track_id += 1

            updated_tracks[track_id] = centroid

            used_track_ids.add(track_id)

            det["track_id"] = track_id

        self.tracked_faces = updated_tracks

        self.active_track_ids = set(updated_tracks.keys())

        return detections
