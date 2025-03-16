from fastapi import APIRouter, HTTPException, Depends
from app.api.models import SearchRequest, SearchResponse, ModelInfo
from app.services.search_service import SearchService
from app.services.llm_service import LLMService
from app.services.content_service import ContentService
from typing import List

router = APIRouter()
search_service = SearchService()
llm_service = LLMService()
content_service = ContentService()

@router.post("/search", response_model=SearchResponse)
async def search(request: SearchRequest):
    try:
        # Get search results
        web_results = await search_service.search(request.query, request.num_results)
        
        # Extract content from top results
        content = await content_service.extract_content(web_results)
        
        # Get AI analyses for each selected model
        ai_analyses = {}
        for ai_model_id in request.ai_model_ids:
            analysis = await llm_service.analyze(
                query=request.query,
                content=content,
                ai_model_id=ai_model_id
            )
            ai_analyses[ai_model_id] = analysis
            
        return SearchResponse(
            query=request.query,
            web_results=web_results,
            ai_analyses=ai_analyses
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/models", response_model=List[ModelInfo])
async def get_models():
    try:
        return llm_service.get_available_models()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) 