from fastapi import FastAPI
from routes import base,data
from motor.motor_asyncio import AsyncIOMotorClient
from helpers.config import get_settings
from stores.llm.LLMProviderFactory import LLMProviderFactory
app = FastAPI()

async def startup_db_client():
    settings = get_settings()
    app.mongo_conn = AsyncIOMotorClient(settings.MONGODB_URL)
    app.db_client = app.mongo_conn[settings.MONGODB_DATABASE]
    llm_provider_factory = LLMProviderFactory(settings)
    app.generation_client = llm_provider_factory.create(provider=settings.GENERATION_BACKEND)
    app.embedding_client = llm_provider_factory.create(provider=settings.EMBEDDING_BACKEND)
async def shutdown_db_clinet():
    app.mongo_conn.close()

app.router.lifespan.on_startup.append(startup_db_client)
app.router.lifespan.on_shutdown.append(shutdown_db_clinet)

app.include_router(base.base_router)
app.include_router(data.data_router)
