from fastapi import FastAPI, APIRouter, Depends, UploadFile , status,Request
from fastapi.responses import JSONResponse
import os 
import aiofiles
from helpers.config import Settings,get_settings
from controllers import DataController, ProjectController,ProcessController
from models.enums.ResponseEnums import ResponseSignal
import logging
from .schemes.data import ProcessRequest
from models.ProjectModel import ProjectModel
logger = logging.getLogger('uvicorn.error')

data_router = APIRouter(prefix='/api/v1/data',
                        tags=['api_v1','data'])

@data_router.post('/upload/{project_id}')
async def upload_data(request:Request,project_id : str, file: UploadFile,
                app_settings: Settings = Depends(get_settings)):

    project_model = ProjectModel(db_client=request.app.db_client)

    project = await project_model.get_project_or_create_one(project_id=project_id)

    is_valid, signal = DataController().validate_uploaded_file(file=file)

    if not is_valid:
        return JSONResponse(status_code=400,
                            content={'Signal':signal})

    project_dir_path = ProjectController().get_project_path(project_id= project_id)
    
    file_path, file_id = DataController().generate_unique_file_path(orig_filename=file.filename, # type: ignore
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
                        'file_id':file_id,
                        'project_id': str(project.id)
                        }
                        )

# data process
@data_router.post('/process/{project_id}')
async def Process_endpoint( project_id: str,
                            process_request:ProcessRequest
                            ):
    process_controller = ProcessController(project_id=project_id)

    file_id = process_request.file_id
    chunk_size = process_request.chunk_size
    overlap_size = process_request.overlap_size or 0  # Default to 0 if None

    file_content = process_controller.get_file_content(file_id=file_id)

    file_chunks = process_controller.process_file_content(
        file_content=file_content,
        file_id=file_id,
        chunk_size=chunk_size, # type: ignore
        overlap_size=overlap_size
    )
    if file_chunks is None or len(file_chunks) == 0:
        return JSONResponse(status_code=400,
                            content={
                                "signal":ResponseSignal.PROCESSING_FAILED.value
                            })
    
    return file_chunks