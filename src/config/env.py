import os

from dotenv import load_dotenv

load_dotenv()


DATABASE_URL = os.getenv("DATABASE_URL")

DEBUG_TIMING = os.getenv("DEBUG_TIMING", "False") == "True"

TRACKING_MAX_DISTANCE = int(os.getenv("TRACKING_MAX_DISTANCE", 80))
