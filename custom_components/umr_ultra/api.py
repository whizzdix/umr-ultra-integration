import asyncio
import aiohttp
import json
import logging

_LOGGER = logging.getLogger(__name__)

class UmrUltraApiError(Exception):
    pass

class UmrUltraAuthError(UmrUltraApiError):
    pass

class UmrUltraApi:
    def __init__(self, host: str, username: str, password: str, session: aiohttp.ClientSession):
        self.host = host
        self.username = username
        self.password = password
        self.session = session
        self.base_url = f"https://{self.host}/ubus/call"
        self._token = None

    async def login(self):
        """Perform login and get authorization token."""
        url = f"{self.base_url}/session"
        headers = {"Content-Type": "application/json"}
        payload = {
            "jsonrpc": "2.0",
            "method": "login",
            "params": {
                "username": self.username,
                "password": self.password,
                "timeout": 2129920
            }
        }
        
        try:
            # We use ssl=False because routers typically use self-signed certificates
            async with self.session.post(url, json=payload, headers=headers, ssl=False) as response:
                response.raise_for_status()
                data = await response.json()
                
                # Check for successful token in response array format 
                # (usually ubus rpc responses look like {"jsonrpc":"2.0","id":null,"result":[0,{"ubus_rpc_session":"token",...}]})
                # We need to extract the exact token as requested
                # Depending strictly on response format... Assuming it returns the token directly in the result or result[1].ubus_rpc_session
                # But for now let's assume it returns an ID object string directly based on user's instruction or in result array.
                
                if "result" in data:
                    if isinstance(data["result"], list) and len(data["result"]) > 1:
                        if "ubus_rpc_session" in data["result"][1]:
                            self._token = data["result"][1]["ubus_rpc_session"]
                        elif isinstance(data["result"][1], dict):
                            vals = list(data["result"][1].values())
                            self._token = vals[0] if vals else None
                    elif isinstance(data["result"], dict):
                        if "ubus_rpc_session" in data["result"]:
                            self._token = data["result"]["ubus_rpc_session"]
                    elif isinstance(data["result"], str):
                        self._token = data["result"]
                        
                if not self._token or not isinstance(self._token, str):
                    raise UmrUltraAuthError("Failed to parse token from login response.")
                    
                _LOGGER.debug("Successfully logged in.")
                return self._token
        except aiohttp.ClientResponseError as e:
            raise UmrUltraApiError(f"HTTP error during login: {e}")
        except Exception as e:
            raise UmrUltraApiError(f"Error during login: {e}")

    async def get_data(self):
        """Fetch the InfoHighDump from uimqtt ubus."""
        if not self._token:
            await self.login()

        url = f"{self.base_url}/uimqtt"
        headers = {
            "Content-Type": "application/json",
            "authorization": f"Bearer {self._token}"
        }
        payload = {
            "jsonrpc": "2.0",
            "method": "InfoHighDump",
            "params": {}
        }

        try:
            async with self.session.post(url, json=payload, headers=headers, ssl=False) as response:
                if response.status in (401, 403):
                    # Token might be expired, clear and retry
                    self._token = None
                    await self.login()
                    headers["authorization"] = f"Bearer {self._token}"
                    async with self.session.post(url, json=payload, headers=headers, ssl=False) as retry_response:
                        retry_response.raise_for_status()
                        return await retry_response.json()
                        
                response.raise_for_status()
                data = await response.json()
                
                if "error" in data:
                    # Sometimes UBUS returns error in JSON
                    self._token = None
                    await self.login()
                    headers["authorization"] = f"Bearer {self._token}"
                    async with self.session.post(url, json=payload, headers=headers, ssl=False) as retry_response:
                        retry_response.raise_for_status()
                        return await retry_response.json()

                if "result" in data:
                    # Depending on how the uimqtt returns data, it might be result directly or result[1].
                    # According to the prompt JSON example, result is directly the dictionary.
                    return data["result"]
                return data
                
        except UmrUltraApiError:
            raise
        except Exception as e:
            raise UmrUltraApiError(f"Error fetching data: {e}")
