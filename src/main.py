from fastapi import FastAPI
from routes import base,data,nlp
from motor.motor_asyncio import AsyncIOMotorClient
from helpers.config import get_settings
from stores.llm.LLMProviderFactory import LLMProviderFactory
from stores.vectordb.VectorDBProviderFactory import VectorDBProviderFactory

app = FastAPI()

async def startup_span():
    settings = get_settings()
    app.mongo_conn = AsyncIOMotorClient(settings.MONGODB_URL)
    app.db_client = app.mongo_conn[settings.MONGODB_DATABASE]
    #llm provider 
    llm_provider_factory = LLMProviderFactory(settings)
    app.generation_client = llm_provider_factory.create(provider=settings.GENERATION_BACKEND)
    app.embedding_client = llm_provider_factory.create(provider=settings.EMBEDDING_BACKEND)

    # vector db provider 
    vectordb_factory_provider = VectorDBProviderFactory(settings)
    app.vectordb_client = vectordb_factory_provider.create(provider=settings.VECTOR_DB_BACKEND)
    app.vectordb_client.connect()
async def shutdown_span():
    app.mongo_conn.close()
    app.vectordb_client.disconnect()


#app.router.lifespan.on_startup.append(startup_span)
#app.router.lifespan.on_shutdown.append(shutdown_span)

app.on_event("startup")(startup_span)
app.on_event("shutdown")(shutdown_span)

app.include_router(base.base_router)
app.include_router(data.data_router)
app.include_router(nlp.nlp_router)
