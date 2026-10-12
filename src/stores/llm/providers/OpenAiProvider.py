from ..LLMInterface import LLMInterface
from openai import OpenAI
import logging
from ..LLMEnum import OpemAiEnum

class OpenAiProvider (LLMInterface) : 
    def __init__(self, api_key: str, api_url: str,
                default_input_max_characters: int = 1000,
                default_generation_max_tokens: int =1000,
                default_generation_temprature: float = 0.1
                ):
        self.api_key = api_key
        self.api_url = api_url
        self.default_input_max_characters = default_input_max_characters
        self.default_generation_max_tokens = default_generation_max_tokens
        self.default_generation_temprature = default_generation_temprature

        self.generation_model_id = None

        self.emdeding_model_id = None
        self.emdeding_size = None

        self.client = OpenAI (
            api_key = self.api_key,
            base_url = self.api_url 
        )

        self.logger = logging.getLogger(__name__)
    
    def set_generation_model(self, model_id: str):
        self.generation_model_id = model_id
    
    def set_emdeding_model(self, model_id, embedding_size: int):
        self.emdeding_model_id = model_id
        self.emdeding_size = embedding_size
    def process_text(self,text: str):
        return text[self.default_input_max_characters].strip()
    
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
            max_tokens= max_output_tokens 
        )

        if not response or not response.choices or len(response.choices) == 0 or not response.choices[0].message:
            self.logger.error("Error while generating text with OpenAI")
            return None

        return response.choices[0].message["content"]
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
            self.logger.error("error while embedding with openai ")
            return None
        
        return response.data[0].embedding

    def construct_prompt(self, prompt: str, role: str ):
            return {
                "role" : role,
                "content" : self.process_text(prompt)
            }