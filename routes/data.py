from fastapi import FastAPI, APIRouter, Depends, UploadFile , status
from fastapi.responses import JSONResponse
import os 
import aiofiles
from helpers.config import Settings,get_settings
from controllers import DataController, ProjectController
from models.enums.ResponseEnums import ResponseSignal
import logging

logger = logging.getLogger('uvicorn.error')

data_router = APIRouter(prefix='/api/v1/data',
                        tags=['api_v1','data'])

@data_router.post('/upload/{project_id}')
async def data(project_id : str, file: UploadFile,
                app_settings: Settings = Depends(get_settings)):

    is_valid, signal = DataController().validate_uploaded_file(file=file)

    if not is_valid:
        return JSONResponse(status_code=400,
                            content={'Signal':signal})

    project_dir_path = ProjectController().get_project_path(project_id= project_id)
    
    file_path, file_id = DataController().generate_unique_file_path(orig_filename=file.filename,
                                                            project_id=project_id)
    
    try:
        async with aiofiles.open(file_path,'wb') as f :
            while chunk := await file.read(app_settings.FILE_DEFAULT_CHUNK_SIZE):
                await f.write(chunk)
    except Exception as e:
        logger.error(f"Error while uploading file: {e}")
        return JSONResponse(status_code=400,
                            content={'Signal':signal})


    return JSONResponse(
                        content={"Signal":ResponseSignal.FILE_UPLOAD_SUCCESS.value,
                        'File_id':file_id}
                        )
