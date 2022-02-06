import requests
import json 
import string
from typing import Dict
from requests import Response


class CommunicationController:
    
    def __init__(self, params : Dict) -> None:
        
        # Store box_id for authentication
        with open("resources/config.json") as config_json:
            self.box_id = json.load(config_json)["ID"]

        # Store foward ngrok URLs
        self.forward_url_port_8080 = "http://0574-2003-cd-df25-768d-9f37-1a79-2826-deb5.ngrok.io"
        self.forward_url_port_8081 = "http://6cc0-2003-cd-df25-768d-9f37-1a79-2826-deb5.ngrok.io"
        
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
        #return self._httpRequest('POST', "<URL>", self.params, self._getBaseHeaders, (user_id, self.box_id), True).status_code == 200
        userRoleData = self.session.get(f"{self.forward_url_port_8081}/api/cas/users/{user_id}/role")
        if userRoleData.status_code != 200:
            return False
        response = '[]'
        if userRoleData.text == '"DELIVERER"':
            response = self.session.put(f"{self.forward_url_port_8080}/api/ds/deliveries/deliverer/{user_id}/deposited/box/{self.box_id}")
        elif userRoleData.text == '"CUSTOMER"':
            response = self.session.put(f"{self.forward_url_port_8080}/api/ds/deliveries/user/{user_id}/delivered/box/{self.box_id}")
        
        return response.status_code == 200 and response.text != '[]'
            
    


    """
    def authenticate(self, user_id : string) -> bool:
        with open("resources/user_ids.json") as user_ids_json:
            user_ids = json.load(user_ids_json)
            return {"id": user_id.strip()} in user_ids
    """


    def sendNotificationToCustomer(self, id : string) -> bool:
        return self._httpRequest('POST', "<URL>", self.params, self._getBaseHeaders, (id, self.box_id)).status_code == 200 
