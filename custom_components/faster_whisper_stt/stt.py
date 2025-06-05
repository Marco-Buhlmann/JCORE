"""Speech-to-Text implementation using Faster Whisper."""
import logging

from homeassistant.components.stt import Provider, SpeechToTextEntity

_LOGGER = logging.getLogger(__name__)

async def async_setup_platform(hass, config, async_add_entities, discovery_info=None):
    """Set up the Faster Whisper STT platform."""
    # Placeholder implementation
    pass
