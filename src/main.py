from fastapi import FastAPI
from routes import base , data
from motor.motor_asyncio import AsyncIOMotorClient
from helpers.config import get_settings
from .stores.llm import LLMProviderFactory

app = FastAPI()
async def startup_db_client():
    settings = get_settings()
    app.mongo_conn = AsyncIOMotorClient(settings.MONGODB_URL)
    app.db_client = app.mongo_conn[settings.MONGODB_DATABASE]
    llm_provider_factory =LLMProviderFactory(settings)
    # generation client
    app.generation_client = llm_provider_factory.create(provider=settings.GENERATION_BACKEND)
    app.generation_client.set_generation_model(model_id= settings.GENERATION_MODEL_ID)
    # embbeding client
    app.emmbeding_client = llm_provider_factory.create(provider=settings.EMBEDDING_BACKEND)
    app.emmbeding_client.set_emdeding_model(model_id=settings.EMBEDDING_MODEL_ID)


async def shutdown_db_client():
    app.mongo_conn.close()

app.router.lifespan.on_startup.append(startup_db_client)
app.router.lifespan.on_shutdown.append(shutdown_db_client)

app.include_router(base.base_router)
app.include_router(data.data_router)
