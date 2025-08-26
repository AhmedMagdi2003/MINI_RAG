from fastapi import FastAPI, APIRouter,Depends
from helpers.config import get_settings,Settings
base_router = APIRouter()

@base_router.get('/')
async def welcom(app_settings: Settings = Depends(get_settings)):
    app_name = app_settings.APP_NAME
    app_version = app_settings.APP_VERSION
    return {'app_name':app_name,
            'app version': app_version}