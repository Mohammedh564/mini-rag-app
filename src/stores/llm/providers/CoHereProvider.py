from BaseLLMProvider import BaseLLMProvider
from ..LLMEnums import CoHereEnum
import cohere
import logging

class CoHereProvider(BaseLLMProvider) :
    def __init__(self, api_key: str,**kwargs):
        super().__init__(api_key=api_key,**kwargs)
        
        self.client =cohere.ClientV2(api_key=self.api_key)

    def generate_text(self, prompt, max_output_tokens, chat_history = [],
                    temperature = None):
        if not self.client:
                self.logger.error("cohere client was not set")
                return None
        if not self.generation_model_id:
                self.logger.error("generation model for cohere was not set")
                return None
        chat_history.append(
                    self.construct_prompt(prompt=prompt, 
                                        role=CoHereEnum.USER.value)
                )
        response = self.client.chat(
            model=self.generation_model_id,
            messages=chat_history,
            temperature = temperature,
            max_tokens = max_output_tokens
        )
        if not response or not response.message.content :
            self.logger.error("Error while generating text with cohere")
            return None

        return response.message.content

    def embed_text(self, text, document_type = None):
        if not self.client:
            self.logger.error("cohere client was not set")
            return None 
    
        if not self.emdeding_model_id:
            self.logger.error("emdeding model for cohere was not set")
            return None
        input_type = document_type if document_type==CoHereEnum.QUERY.value else CoHereEnum.DOCUMENT.value
        
        response = self.client.embed(
            texts=[self.process_text(text)],
            model=self.emdeding_model_id,
            input_type=input_type,
            output_dimension=self.emdeding_size,
            embedding_types=["float"],
        )
        if not response or not response.embeddings or not response.embeddings.float :
            self.logger.error("error while embedding with cohere")
            return None


        return response.embeddings.float[0]

