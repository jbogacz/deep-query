import os


class Config:
    def __init__(self):
        self.model_name: str = os.getenv(
            "COGNITION_MODEL_NAME", "allegro/herbert-base-cased"
        )
