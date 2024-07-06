# Create API routes and include them in the main application
from fastapi import APIRouter

from app.api.endpoints import ask_openai

api_router = APIRouter()

api_router.include_router(ask_openai.router, prefix="/ask-openai")
# api_router.include_router(get_lua_file.router, tags=["Raw Files"], prefix="/lua/file")
# api_router.include_router(list_files.router, tags=["Raw Files"], prefix="/lua/list")
# api_router.include_router(post_lua_file.router, tags=["Raw Files"], prefix="/lua/file")
