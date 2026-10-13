from ..LLMInterface import LLMInterface
import logging
class BaseLLMProvider (LLMInterface):
    def __init__(self, api_key: str,
                    default_input_max_characters: int = 1000,
                    default_generation_max_output_tokens: int =1000,
                    default_generation_temprature: float = 0.1
                    ):
            self.api_key = api_key
            self.default_input_max_characters = default_input_max_characters
            self.default_generation_max_output_tokens = default_generation_max_output_tokens
            self.default_generation_temprature = default_generation_temprature
    
            self.generation_model_id = None
    
            self.emdeding_model_id = None
            self.emdeding_size = None

            self.logger = logging.getLogger(__name__)
    def set_generation_model(self, model_id: str):
        self.generation_model_id = model_id
    
    def set_emdeding_model(self, model_id, embedding_size: int):
        self.emdeding_model_id = model_id
        self.emdeding_size = embedding_size
    def process_text(self,text: str):
        return text[:self.default_input_max_characters].strip()

    def construct_prompt(self, prompt: str, role: str ):
            return {
                "role" : role,
                "content" : self.process_text(prompt)
                }