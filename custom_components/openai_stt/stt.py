"""Speech-to-Text implementation using OpenAI."""
import logging

from homeassistant.components.stt import Provider, SpeechToTextEntity

_LOGGER = logging.getLogger(__name__)

async def async_setup_platform(hass, config, async_add_entities, discovery_info=None):
    """Set up the OpenAI STT platform."""
    # Placeholder implementation
    pass
