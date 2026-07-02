import requests
from .tokenManager import get_token

class UserAPI:

    def __init__(self):
        self.base_url = "https://oapi.dingtalk.com"
        self.headers = {
            "Content-Type": "application/json"
        }


    def get_user(self) -> dict:
        
        access_token = get_token()
        
        url = f"{self.base_url}/topapi/user/listsimple?access_token={access_token}"

        payload = {
            "dept_id":"1",
            "cursor":"0",
            "size":"20",
            "order_field":"modify_desc",
            "contain_access_limit":False,
            "language":"zh_CN"
        }

        response = requests.post(url, json=payload, headers=self.headers)
        
        return response.json()

    def get_user_id(self, name:str) -> list:

        user = self.get_user()
        user_list = user['result']['list']
        
        match_user = [user['userid'] for user in user_list if name in user['name']]

        return match_user
    
    def get_user_detail(self,u_id: str) -> dict:

        access_token = get_token()

        url= f"{self.base_url}/topapi/v2/user/get?access_token={access_token}"

        payload = {
            "userid":u_id,
            "language":"zh_CN"
        }

        response = requests.post(url, json=payload, headers=self.headers)

        return response.json()
    