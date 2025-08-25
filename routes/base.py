from fastapi import FastAPI, APIRouter
import os
base_router = APIRouter()

@base_router.get('/')
async def welcom():
    app_name = os.getenv('APP_NAME')
    app_version = os.getenv('APP_VERSION')
    return {'app_name':app_name,
            'app version': app_version}