from crewai import LLM
import os

class BaseCrew:
    @property
    def llm(self):
        return LLM(
            model="groq/llama-3.3-70b-versatile",
            temperature=0.1,
            api_key=os.getenv("GROQ_API_KEY"),
            tool_choice="auto"
        )
    
    @property
    def llm_rapido(self):
        return LLM(model="groq/llama-3.1-8b-instant", 
                   temperature=0.1,
                   api_key=os.getenv("GROQ_API_KEY"), 
                   tool_choice="auto"
                   )