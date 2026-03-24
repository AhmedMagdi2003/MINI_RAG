from enum import Enum

class ResponseSignal(Enum):
    FILE_VALIDATED_SUCCESS = "file_validate_successfully"
    FILE_TYPE_NOT_SUPPORTED = "file_type_not_supported"
    FILE_SIZE_EXCEEDED = "file_size_exceeded"
    FILE_UPLOAD_SUCCESS = "file_upload_success"
    FILE_UPLOAD_FAILED = "file_upload_failed"
    PROCESSING_FAILED = "processing failed"
    PROCESSING_SUCCES= 'processing successed'
    NO_FILES_ERROR = 'No files found'
    PROJECT_NOT_FOUND_ERROR = "Project not found"
    INSERT_INTO_VECTORDB_ERROR= "insert into vectordb error"
    INSERT_INTO_VECTORDB_SUCCESS = "sucsses inserted chuncks"
    VECTORDB_COLLECTION_RETRIEVED = "Vectordb_collection_retrieved sucssefully"