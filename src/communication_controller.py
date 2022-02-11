import requests
import json 
import string
from typing import Dict
from requests import Response


class CommunicationController:
    
    def __init__(self, params : Dict) -> None:
        
        # Store box_id for authentication
        with open("resources/config.json") as config_json:
            box_config = json.load(config_json)
            self.box_id = box_config["ID"]
            self.api_gateway_url = box_config["API_GATEWAY_URL"]
        
        # Use session so it is not necessary to rewrite cookies and JWT for every request
        self.session = requests.Session()

        # Save parameters
        self.params = params


    def _httpRequest(self, method : string, url : string, params : Dict, headers="", content="", is_auth=False) -> Response:
        # Perform GET request
        if method == 'GET':
            return self.session.get(url=url, params=params)
        # Perform POST request
        elif method == 'POST':
            return self.session.post(url=url, params=params, headers=headers, auth=content) if is_auth else self.session.post(url, params=params, headers=headers, json=content)
        else:
            raise ValueError("CommunicationController._httpRequest(): method not found.")


    def _getBaseHeaders(self, xsrf_token : string) -> Dict:
        # Return base header containing XSRF token
        return {
            "Content-Type": "application/json",
            "X-XSRF-TOKEN": xsrf_token
        }
    

    def _getXSRFToken(self) -> Response:
        # Get XSRF token from GET request
        r = self._httpRequest('GET', "<URL>", self.params)

        # Check status code
        if r.status_code == 200:
            return r  
        else:
            raise ValueError("CommunicationController._getXSRFToken(): Request unsuccessful")


    def authenticate(self, user_id : string) -> bool:
        # Perform basic authentication by using user_id and box_id
        response = self.session.put(f"{self.api_gateway_url}/api/ds/deliveries/user/{user_id}/update/box/{self.box_id}")
        return response.status_code == 200 and response.text != '[]'


    def sendNotificationToCustomer(self, id : string) -> bool:
        return self._httpRequest('POST', "<URL>", self.params, self._getBaseHeaders, (id, self.box_id)).status_code == 200 
