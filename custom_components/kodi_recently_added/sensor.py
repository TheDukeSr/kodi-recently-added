import logging
from typing import Optional

from homeassistant import core
from homeassistant.components.kodi.const import DATA_KODI, DOMAIN as KODI_DOMAIN
from homeassistant.components.sensor import PLATFORM_SCHEMA
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import CONF_HOST
import homeassistant.helpers.config_validation as cv
import voluptuous as vol

from .entities import KodiRecentlyAddedMoviesEntity, KodiRecentlyAddedTVEntity

PLATFORM_SCHEMA = vol.Any(
    PLATFORM_SCHEMA.extend({vol.Required(CONF_HOST): cv.string}),
)
_LOGGER = logging.getLogger(__name__)


def find_matching_config_entry_for_host(
    hass: core.HomeAssistant, host: str
) -> Optional[ConfigEntry]:
    """Search existing config entries for one matching the host."""
    for entry in hass.config_entries.async_entries(KODI_DOMAIN):
        if entry.data[CONF_HOST] == host:
            return entry
    return None


async def async_setup_platform(
    hass: core.HomeAssistant, config: dict, async_add_entities, discovery_info=None
) -> None:
    """Setup the sensor platform."""
    host = config[CONF_HOST]
    config_entry = find_matching_config_entry_for_host(hass, host)
    if config_entry is None:
        _LOGGER.error(
            "Failed to setup sensor. Could not find config entry for kodi host %s", host
        )
        return

    data = hass.data[KODI_DOMAIN][config_entry.entry_id]
    kodi = data[DATA_KODI]

    tv_entity = KodiRecentlyAddedTVEntity(kodi, config_entry.data)
    movies_entity = KodiRecentlyAddedMoviesEntity(kodi, config_entry.data)
    async_add_entities([tv_entity, movies_entity])