"""
Home Assistant STT provider for Faster Whisper.
"""

import asyncio
import io
import logging
from pathlib import Path
from typing import Optional, Tuple

from homeassistant.components.stt import ProviderEntity
from homeassistant.components.stt.const import RESULT_SUCCESS
from homeassistant.const import CONF_MODEL, CONF_DEFAULT_LANGUAGE
import voluptuous as vol
from homeassistant.helpers import config_validation as cv
from homeassistant.core import HomeAssistant

from faster_whisper import WhisperModel

_LOGGER = logging.getLogger(__name__)

DOMAIN = "faster_whisper_stt"

CONFIG_SCHEMA = {
    DOMAIN: {
        vol.Optional(CONF_MODEL, default="small"): cv.string,
        vol.Optional(CONF_DEFAULT_LANGUAGE, default="en"): cv.string,
    }
}

async def async_setup_platform(hass, config, async_add_entities, discovery_info=None):
    """Set up the Faster Whisper STT provider from YAML config."""
    model_size = config.get(CONF_MODEL, "small")
    default_language = config.get(CONF_DEFAULT_LANGUAGE, "en")

    provider = FasterWhisperProvider(hass, model_size, default_language)
    async_add_entities([provider])

class FasterWhisperProvider(ProviderEntity):
    """Implementation of an STT provider using the Faster Whisper library."""

    def __init__(self, hass: HomeAssistant, model_size: str, default_language: str):
        """Initialize the provider."""
        self.hass = hass
        self._model_size = model_size
        self._default_language = default_language
        self._name = "Faster Whisper"
        self._model: Optional[WhisperModel] = None
        self._model_load_lock = asyncio.Lock()

    @property
    def name(self) -> str:
        """Return the name of the provider."""
        return self._name

    @property
    def default_language(self) -> str:
        """Return the default language code."""
        return self._default_language

    @property
    def supported_languages(self) -> list[str]:
        """Return list of supported language codes."""
        return ["en", "es", "de", "fr", "it", "pt", "nl", "sv", "zh"]

    async def async_get_supported_languages(self) -> list[str]:
        """Return supported languages."""
        return self.supported_languages

    async def async_process_audio(
        self, audio_bytes: bytes, language: str | None = None
    ) -> Tuple[int, str]:
        """
        Transcribe the given audio bytes (in WAV/RAW format).
        Returns (status, text).
        """
        # 1) Ensure model is loaded once
        async with self._model_load_lock:
            if self._model is None:
                _LOGGER.info("Loading Faster Whisper model '%s'...", self._model_size)
                # Load model in CPU mode; change to device="cuda" if you have a GPU
                self._model = WhisperModel(self._model_size, device="cpu", compute_type="int8")
                _LOGGER.info("Faster Whisper model loaded.")

        # 2) Write bytes to a temporary file (faster-whisper expects a path)
        tmp_path = Path("/tmp/hass_whisper.wav")
        tmp_path.write_bytes(audio_bytes)

        _LOGGER.debug("Transcribing %s ...", tmp_path)
        segments, info = self._model.transcribe(
            str(tmp_path),
            language=language or self._default_language,
            beam_size=5,
            best_of=5,
            suppress_blank=True,
        )

        # 3) Concatenate all segment texts
        text = "".join([segment.text for segment in segments])
        _LOGGER.debug("Transcription result: %s", text)

        # 4) Clean up temp file
        try:
            tmp_path.unlink()
        except Exception:
            pass

        return RESULT_SUCCESS, text

def async_setup(hass: HomeAssistant, config: dict):
    """Set up the Faster Whisper STT component."""
    hass.async_create_task(
        hass.config_entries.async_forward_entry_setup(DOMAIN, DOMAIN)
    )
    return True
