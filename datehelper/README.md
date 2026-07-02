# DATEHELPER Python Library

A simple Python library to get Datehelper access tokens.

## Usage

```python
from dingtalk import DingTalkAPI

api = DingTalkAPI("your_app_key", "your_app_secret")
token_data = api.get_access_token()
print(token_data)
