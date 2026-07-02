import requests
import json
import os
from datetime import datetime, timedelta


class TokenManagerAPI:
    TOKEN_FILE = "data/attendance/token_cache.json"

    def __init__(self, app_key: str, app_secret: str):
        self.app_key = app_key
        self.app_secret = app_secret
        self.base_url = "https://api.dingtalk.com"
        self.headers = {
            "Content-Type": "application/json"
        }
        self.access_token = None

    def _save_token(self, token_dict: dict):
        """Save access token and expiration time locally"""
        data = {
            "access_token": token_dict['accessToken'],
            "expires_at": (datetime.now() + timedelta(seconds=token_dict['expireIn'])).isoformat()
        }
        with open(self.TOKEN_FILE, "w") as f:
            json.dump(data, f)

    def _load_token(self):
        """Load token from cache if still valid"""
        if not os.path.exists(self.TOKEN_FILE):
            return None
        with open(self.TOKEN_FILE, "r") as f:
            data = json.load(f)
        expires_at = datetime.fromisoformat(data["expires_at"])
        if datetime.now() < expires_at:
            return data["access_token"]
        return None

    def get_access_token(self) -> dict:
        token = self._load_token()
        
        if token:
            self.access_token = token
            print("Using cached access token")
            return token
        
        print("Token missing or expired, requesting a new one...")

        url = f"{self.base_url}/v1.0/oauth2/accessToken"
        payload = {
            "appKey": self.app_key,
            "appSecret": self.app_secret
        }
        response = requests.post(url, json=payload, headers=self.headers)
        data = response.json()

        token = data.get("accessToken")
        if not token:
            raise Exception(f"Failed to get access token: {data}")

        self.access_token = token
        self._save_token(data)
        return token


token_manager = None
def init_token_manager(app_key: str, app_secret: str):
    """Initialize the global token manager"""
    global token_manager
    token_manager = TokenManagerAPI(app_key, app_secret)

def get_token() -> str:
    """Return a valid token, using the initialized manager"""
    if token_manager is None:
        raise Exception("Token manager not initialized. Call init_token_manager first.")
    return token_manager.get_access_token()