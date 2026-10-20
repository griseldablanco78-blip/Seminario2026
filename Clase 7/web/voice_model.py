"""Whisper automatic speech recognition for Expensa House."""
from functools import lru_cache
from typing import Any


MODEL_ID = "openai/whisper-tiny"


class VoiceModelUnavailableError(RuntimeError):
    """Whisper could not be loaded for speech transcription."""


@lru_cache(maxsize=1)
def _load_asr() -> Any:
    try:
        from transformers import pipeline
    except ImportError as exc:
        raise VoiceModelUnavailableError(
            "Falta Transformers para usar Whisper. Instalá las dependencias de Clase 7."
        ) from exc

    try:
        return pipeline(
            "automatic-speech-recognition",
            model=MODEL_ID,
            device=-1,
        )
    except (OSError, RuntimeError, ValueError) as exc:
        raise VoiceModelUnavailableError(
            "No se pudo cargar Whisper. Revisá Internet, memoria y FFmpeg."
        ) from exc


def transcribe_audio(path: str) -> str:
    result = _load_asr()(
        path,
        generate_kwargs={"language": "spanish", "task": "transcribe"},
    )
    text = result.get("text", "").strip()
    if not text:
        raise ValueError("Whisper no reconoció palabras en el audio.")
    return text
