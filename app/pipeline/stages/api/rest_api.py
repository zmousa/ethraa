import requests
from .model.search_result import SearchResult
from .model.create_body import CreateBody, FormRepresentation, Lemma


# swagger: https://siwar.ksaa.gov.sa/api-brmjn#/
class ApiController:
    BASE_URL = "https://siwar.ksaa.gov.sa/api/alriyadh"
    
    def __init__(self, settings):
        self.API_KEY = settings.API_KEY
        

    def api_search(self, query):
        endpoint = "/search"
        url = self.BASE_URL + endpoint

        params = {
            "query": query
        }
        
        headers = {
            "apikey": self.API_KEY
        }

        try:
            print(params)
            response = requests.get(url, params=params, headers=headers, verify=False)
            print(f"API Response: {response.json()}")
            
            if response.status_code == 200:
                return SearchResult.FOUND
            elif response.status_code == 404:
                return SearchResult.NOT_FOUND
            else:
                return SearchResult.ERROR
            
        except requests.exceptions.RequestException as e:
            print(f"Error making request: {e}")
            return None

    def api_create(self, create_body):
        endpoint = "/create/entry"
        url = self.BASE_URL + endpoint

        headers = {
            "apikey": self.API_KEY
        }
        
        try:
            response = requests.post(url, headers=headers, json=create_body.__dict__, verify=False)
            return response.status_code == 201
        except requests.exceptions.RequestException as e:
            print(f"Error making request: {e}")
            return False
        
if __name__ == "__main__":
    search_result = api_search("كلمة")
    print(search_result)

    form_representation = FormRepresentation("string", "string", "string", "string")
    lemma = Lemma([form_representation], "string")

    create_body = CreateBody(
        lemma=lemma,
        stems=[],
        wordForms=[],
        senses=[],
        morphologicalPatterns="string",
        pos="N",
        plain="string",
        verbOrigin="s",
        nounOrigin="s",
        originality="M",
        hasTanween=True
    )
    success = api_create(create_body)
    if success:
        print("Create successful: Status Code 201")
    else:
        print("Create failed: Status Code not 201")
