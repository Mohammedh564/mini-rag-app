from BaseLLMProvider import BaseLLMProvider
from openai import OpenAI
import logging
from ..LLMEnums import OpemAiEnum

class OpenAiProvider (BaseLLMProvider) : 
    def __init__(self, api_url: str,api_key: str, **kwargs):
        super().__init__(api_key=api_key, **kwargs)
        self.api_url = api_url

        self.client = OpenAI (
            api_key = self.api_key,
            base_url = self.api_url 
        )
    
    def generate_text(self,prompt: str,
                            max_output_tokens: int,
                            chat_history: list,
                            temperature:float = None):
        if not self.client:
            self.logger.error("openai client was not set")
            return None 
                
        if not self.generation_model_id:
            self.logger.error("generation model for openai was not set")
            return None
        max_output_tokens = max_output_tokens if  max_output_tokens else self.default_generation_max_tokens
        temperature = temperature if temperature != None else self.default_generation_temprature

        chat_history.append(
            self.construct_prompt(prompt=prompt, 
                                role=OpemAiEnum.USER.value)
        )

        response = self.client.chat.completions.create(
            model= self.generation_model_id,
            messages= chat_history, 
            max_completion_tokens= max_output_tokens,
            temperature=temperature 
        )

        if not response or not response.choices or len(response.choices) == 0 or not response.choices[0].message:
            self.logger.error("Error while generating text with OpenAI")
            return None

        return response.choices[0].message.content
    def embed_text(self, text, document_type = None):
        if not self.client:
            self.logger.error("openai client was not set")
            return None 
        
        if not self.emdeding_model_id:
            self.logger.error("emdeding model for openai was not set")
            return None
        
        response = self.client.embeddings.create(
            input=text, 
            model=self.emdeding_model_id
            )
        if not response or not response.data or len(response.data) == 0 or  response.data[0].embedding == None :
            self.logger.error("error while embedding with openai")
            return None
        
        return response.data[0].embedding
    
