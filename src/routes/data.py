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
from models.ChunkModel import ChunkModel
from models.db_schemes import DataChunk, Asset
from models.AssetModel import AssetModel
from bson import ObjectId
from models.enums.AssetTypeEnums import AssetTypeEnums
logger = logging.getLogger('uvicorn.error')

data_router = APIRouter(prefix='/api/v1/data',
                        tags=['api_v1','data'])

@data_router.post('/upload/{project_id}')
async def upload_data(request:Request,project_id : int, file: UploadFile,
                app_settings: Settings = Depends(get_settings)):

    project_model =  await ProjectModel.create_instance(db_client=request.app.db_client)

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

    # store the asset into the database 
    asset_model = await AssetModel.create_instance(
        db_client = request.app.db_client
    )

    asset_resources = Asset(
        asset_project_id= project.id if project.id is not None else ObjectId(),
        asset_type = AssetTypeEnums.FILE.value,
        asset_name = file_id,
        asset_size = os.path.getsize(file_path),
    )
    asset_record = await asset_model.create_asset(asset=asset_resources)


    return JSONResponse(
                        content={"Signal":ResponseSignal.FILE_UPLOAD_SUCCESS.value,
                        'file_id':str(asset_record.id ),
                        #'project_id': str(project.id) # i don't used to see it 
                        }
                        )

# data process
@data_router.post('/process/{project_id}')
async def Process_endpoint(request:Request, project_id: int,
                            process_request:ProcessRequest
                            ):
    
    project_model = await  ProjectModel.create_instance(db_client=request.app.db_client)
    project = await project_model.get_project_or_create_one(project_id=project_id)


    process_controller = ProcessController(project_id=project_id)

    #file_id = process_request.file_id
    chunk_size = process_request.chunk_size
    overlap_size = process_request.overlap_size or 0  # Default to 0 if None
    do_reset = process_request.do_reset
    chunk_model = ChunkModel(db_client=request.app.db_client)
    if do_reset ==1:
        await chunk_model.delete_project_by_projectid(project_id=project.id) # type: ignore


    project_files_ids = {}
    asset_model = await AssetModel.create_instance(
        db_client = request.app.db_client
    )
    
    if process_request.file_id:
        # file_id is the MongoDB ObjectId, need to get the actual asset_name
        try:
            asset_record = await asset_model.get_asset_record(
                asset_project_id=str(project.id),
                asset_name=process_request.file_id
            )
            if asset_record:
                project_files_ids = {asset_record.id: asset_record.asset_name}
            else:
                # Try treating it as ObjectId and search by ID instead
                asset = await asset_model.collection.find_one({
                    "_id": ObjectId(process_request.file_id) if isinstance(process_request.file_id, str) else process_request.file_id,
                    "asset_project_id": ObjectId(project.id) if isinstance(project.id, str) else project.id
                })
                if asset:
                    project_files_ids = {asset.get('_id'): asset.get('asset_name')}
        except Exception as e:
            logger.error(f"Error retrieving asset: {e}")
            return JSONResponse(status_code=400,
                                content={'Signal': ResponseSignal.NO_FILES_ERROR.value})
    else:
        project_files = await asset_model.get_all_project_assets(asset_project_id=str(project.id),
                                                                asset_type=AssetTypeEnums.FILE.value)
        
        project_files_ids = {record.asset_project_id: record.asset_name for record in project_files}

    if len(project_files_ids) == 0 :
            return JSONResponse(
        content={
            'Signal': ResponseSignal.NO_FILES_ERROR.value,
        })
    
    
    no_records = 0
    no_files = 0
    for asset_id, file_id in project_files_ids.items():
        file_content = process_controller.get_file_content(file_id=file_id) # pyright: ignore[reportArgumentType]

        if file_content is None:
            logger.error(f"Error while processing file: {file_id}")
            continue



        file_chunks = process_controller.process_file_content(
            file_content=file_content, # type: ignore
            file_id=file_id, # pyright: ignore[reportArgumentType]
            chunk_size=chunk_size, # type: ignore
            overlap_size=overlap_size
        )
        if file_chunks is None or len(file_chunks) == 0:
            return JSONResponse(status_code=400,
                                content={
                                    "signal":ResponseSignal.PROCESSING_FAILED.value
                                })
        
        file_chunks_records = [
            DataChunk(
                chunk_project_id = project.id, # type: ignore
                chunk_order= i+1,
                chunk_metadata= chunk.metadata,
                chunk_text= chunk.page_content,
                chunk_asset_id=ObjectId(asset_id) if isinstance(asset_id, str) else asset_id  # type: ignore
            )
            for i ,chunk in enumerate(file_chunks)
        ]
        chunk_model = await ChunkModel.create_instance(db_client=request.app.db_client)

        no_records = await chunk_model.insert_many_chunk(chunks=file_chunks_records)
        no_files  +=1

    return JSONResponse(
        content={
            'Signal': ResponseSignal.PROCESSING_SUCCES.value,
            'Inserted_chunks': no_records,
            'Processed_files': no_files
        })