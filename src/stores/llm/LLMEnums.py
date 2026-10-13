from enum import Enum

class LLMEnum (Enum):
    COHERE = "COHERE"
    OPENAI = "OPENAI"


class OpemAiEnum (Enum) :
    SYSTEM = "system"
    USER = "user"
    ASSITANT = "assistant"

class CoHereEnum (Enum) :
    SYSTEM = "SYSTEM"
    USER = "USER"
    ASSITANT = "CHATBOT"
    
    DOCUMENT = "search_document"
    QUERY = "search_query"

class DocumentTypeENum(Enum) :
    DOCUMENT = "document" 
    QUERY= "query"