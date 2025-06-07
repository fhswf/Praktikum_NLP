from dataclasses import dataclass


@dataclass
class SpeechItem:
    top_id: str
    speech_id: str
    speaker_id: str
    date: str
    type: str
    text: str