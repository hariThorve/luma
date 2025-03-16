from pydantic import BaseModel, ConfigDict
from typing import List, Optional, Dict, Any

class SearchRequest(BaseModel):
    model_config = ConfigDict(protected_namespaces=())
    
    query: str
    ai_model_ids: List[str]
    num_results: Optional[int] = 5

class SearchResult(BaseModel):
    model_config = ConfigDict(protected_namespaces=())
    
    title: str
    url: str
    snippet: str

class ModelInfo(BaseModel):
    model_config = ConfigDict(protected_namespaces=())
    
    id: str
    name: str
    provider: str
    description: str

class AIAnalysis(BaseModel):
    model_config = ConfigDict(protected_namespaces=())
    
    ai_model_id: str
    content: str

class SearchResponse(BaseModel):
    model_config = ConfigDict(protected_namespaces=())
    
    query: str
    web_results: List[SearchResult]
    ai_analyses: Dict[str, AIAnalysis] 