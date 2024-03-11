
from abc import ABC, abstractmethod
class LLM(ABC):
    """Abstract class of an LLM"""

 
    def __init__(self):
        super().__init__()
    
    @abstractmethod
    def ask(self, messages):
        """Prompting the LLM by passing a list of messages. Returns the answer of the LLM."""
        pass

from openai import OpenAI as OriginalOpenAI
class ChatGPT_private_subscription(LLM):
    """gpt-4-vision-preview model instance that is based on an usual private open ai subscription"""
 
    def __init__(self):
        self.client = OriginalOpenAI()
        super().__init__()
    
    def ask(self, messages):
        response = self.client.chat.completions.create(
            model="gpt-4-vision-preview",
            messages=messages,
            max_tokens=4096,
        )
        print(response.choices[0].finish_reason)
        print(response.usage)
        return response.choices[0].message.content

import requests, json
class ChatGPT_hosted_subscription(LLM):
    """gpt-4-vision-preview model instance that is based on an hosted open ai subscription, for example on azure"""
 
    def __init__(self, openai_authorization_token, client_id, url_access_token, url_model):

        def get_token():
            headers = {
                'Content-Type': 'application/x-www-form-urlencoded',
                'Authorization': openai_authorization_token,
            }
            data = {
                'client_id': client_id,
                'grant_type': 'client_credentials',
            }
            response = requests.post(url_access_token, headers=headers, data=data)
            return response.json()['access_token']

        self.token = get_token()
        self.url_model = url_model
        super().__init__()
    
    def ask(self, messages):
        url = self.url_model

        # gpt-4-turbo example, prompt uses Chat Completions API format, note the use of messages array instead of prompt
        payload = {
            "deployment_id": "gpt-4-turbo",
            "messages": messages,
            "max_tokens": 4096,
            #"temperature": 0.7
        }
        
        headers = {'Authorization': 'Bearer'+' '+ self.token}
        
        response = requests.request("POST", url, headers=headers, json=payload)
        try: 
            response_content = json.loads(response._content)
            return response_content["choices"][0]["message"]["content"]
        except Exception as e:
            print(e)
            return response
        
