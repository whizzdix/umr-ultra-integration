import voluptuous as vol
from homeassistant import config_entries
from homeassistant.const import CONF_HOST, CONF_USERNAME, CONF_PASSWORD
from homeassistant.helpers.aiohttp_client import async_get_clientsession

from .const import DOMAIN, CONF_UPDATE_INTERVAL, DEFAULT_UPDATE_INTERVAL, DEFAULT_HOST
from .api import UmrUltraApi, UmrUltraAuthError, UmrUltraApiError

class UmrUltraConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for UMR-Ultra."""
    
    VERSION = 1

    async def async_step_user(self, user_input=None):
        errors = {}

        if user_input is not None:
            session = async_get_clientsession(self.hass)
            api = UmrUltraApi(
                host=user_input[CONF_HOST],
                username=user_input[CONF_USERNAME],
                password=user_input[CONF_PASSWORD],
                session=session
            )
            
            try:
                await api.login()
                return self.async_create_entry(title=f"UMR-Ultra ({user_input[CONF_HOST]})", data=user_input)
            except UmrUltraAuthError:
                errors["base"] = "invalid_auth"
            except UmrUltraApiError:
                errors["base"] = "cannot_connect"
            except Exception:
                errors["base"] = "unknown"

        data_schema = vol.Schema({
            vol.Required(CONF_HOST, default=DEFAULT_HOST): str,
            vol.Required(CONF_USERNAME): str,
            vol.Required(CONF_PASSWORD): str,
            vol.Optional(CONF_UPDATE_INTERVAL, default=DEFAULT_UPDATE_INTERVAL): int,
        })

        return self.async_show_form(
            step_id="user", data_schema=data_schema, errors=errors
        )
