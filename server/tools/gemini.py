import google.generativeai as genai
from shared.config import GEMINI_KEY,GEMINI_MODEL
import os


class GeminiAgent(object):
    def __new__(cls):
        if not hasattr(cls, 'instance'):
          cls.instance = super(GeminiAgent, cls).__new__(cls)
        return cls.instance
        
    def __init__(self):
        genai.configure(api_key=os.getenv(GEMINI_KEY))
        self.model = genai.GenerativeModel(GEMINI_MODEL)
        
    def execute(self, query:str)-> str:
        response = self.model.generate_content(query)
        return response.text
        