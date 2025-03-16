import os
import google.generativeai as genai
import groq
from app.api.models import AIAnalysis, ModelInfo
from typing import List, Dict
import json
import aiohttp
from app.utils.cache import cache

class LLMService:
    def __init__(self):
        # Initialize Google Gemini
        self.gemini_api_key = os.getenv("GEMINI_API_KEY")
        if self.gemini_api_key:
            genai.configure(api_key=self.gemini_api_key)
        else:
            print("WARNING: GEMINI_API_KEY not found in environment variables")
        
        # Initialize Groq
        self.groq_api_key = os.getenv("GROQ_API_KEY")
        if not self.groq_api_key:
            print("WARNING: GROQ_API_KEY not found in environment variables")
        
        # Define available models - removed Claude models
        self.models = [
            ModelInfo(
                id="gemini-pro",
                name="Gemini 2.0 Flash",
                provider="Google",
                description="Google's Gemini 2.0 Flash model for general text generation and analysis."
            ),
            ModelInfo(
                id="llama3-70b-8192",
                name="Llama 3 70B",
                provider="Groq",
                description="Meta's Llama 3 70B model, optimized for speed on Groq's platform."
            )
        ]
    
    def get_available_models(self) -> List[ModelInfo]:
        """
        Return the list of available AI models.
        """
        return self.models
    
    async def analyze(self, query: str, content: str, ai_model_id: str) -> AIAnalysis:
        """
        Analyze the search results using the specified AI model.
        """
        prompt = self._generate_prompt(query, content)
        
        if ai_model_id == "gemini-pro":
            response = await self._call_gemini(prompt)
        elif ai_model_id in ["llama3-70b-8192"]:
            response = await self._call_groq(prompt, ai_model_id)
        else:
            response = f"Error: Unsupported model ID '{ai_model_id}'"
        
        return AIAnalysis(
            ai_model_id=ai_model_id,
            content=response
        )
    
    def _generate_prompt(self, query: str, content: str) -> str:
        """
        Generate a prompt for the AI model.
        """
        return f"""
        You are a helpful AI assistant tasked with analyzing search results and providing a comprehensive answer to a user's query.
        
        USER QUERY: {query}
        
        SEARCH RESULTS:
        {content}
        
        Please analyze the search results and provide a detailed, informative response to the user's query. Your response should:
        
        1. Directly address the user's query with the most relevant information from the search results
        2. Be well-structured, using markdown formatting for readability
        3. Any additional context that might be helpful
        
        If the search results don't contain enough information to answer the query, 
        please indicate what's missing and provide the best response you can with the available information.
        
        Format your response in markdown for readability.
        """
    
    async def _call_gemini(self, prompt: str) -> str:
        """
        Call the Google Gemini API.
        """
        try:
            model = genai.GenerativeModel('gemini-2.0-flash')
            response = await model.generate_content_async(prompt)
            return response.text
        except Exception as e:
            return f"Error calling Gemini API: {str(e)}"
    
    async def _call_groq(self, prompt: str, model_id: str) -> str:
        """
        Call the Groq API.
        """
        try:
            if self.groq_api_key:
                client = groq.Groq(api_key=self.groq_api_key)
                completion = client.chat.completions.create(
                    messages=[
                        {
                            "role": "user",
                            "content": prompt
                        }
                    ],
                    model=model_id
                )
                return completion.choices[0].message.content
            else:
                # If API key is not available, use the HTTP API directly
                headers = {
                    "Authorization": f"Bearer {self.groq_api_key}",
                    "Content-Type": "application/json"
                }
                
                payload = {
                    "messages": [
                        {
                            "role": "user",
                            "content": prompt
                        }
                    ],
                    "model": model_id
                }
                
                async with aiohttp.ClientSession() as session:
                    async with session.post(
                                        "https://api.groq.com/openai/v1/chat/completions", 
                                        headers=headers, 
                                        json=payload) as response:
                        if  response.status != 200:
                            error_text = await response.text()
                        return f"Error from Groq API: {error_text}"
                    
                    data = await response.json()
                    return data["choices"][0]["message"]["content"]
        except Exception as e:
            return f"Error calling Groq API: {str(e)}" 