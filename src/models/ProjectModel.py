from .BaseDataModel import BaseDataModel
from .db_schemes import Project
from .enums.DataBaseEnums import DataBaseEnums

class ProjectModel(BaseDataModel):
    def __init__(self,db_client:object):
        super().__init__(db_client=db_client)
        self.collection = self.db_client[DataBaseEnums.COLLECTION_PROJECT_NAME.value] # pyright: ignore[reportIndexIssue]
    @classmethod
    async def create_instance(cls,db_client:object):
        instance  = cls(db_client)
        await instance.init_collection()
        return instance


    async def init_collection(self):
        all_collections = await self.db_client.list_collection_names()  # type: ignore

        if DataBaseEnums.COLLECTION_PROJECT_NAME.value  not in all_collections:
            self.collection = self.db_client[DataBaseEnums.COLLECTION_PROJECT_NAME.value] # pyright: ignore[reportIndexIssue]
            indexes = Project.get_indexes()
            for index in indexes:
                await self.collection.create_index(
                    index['key'],
                    name= index['name'],
                    unique = index['unique']
                )



    async def create_project(self,project:Project):
        result = await self.collection.insert_one(project.dict())
        project_data = project.dict()
        project_data['_id'] = result.inserted_id
        return Project(**project_data)
    
    async def get_project_or_create_one(self,project_id:str):

        record = await self.collection.find_one({
            "project_id": project_id
        })

        if record == None:
            project = Project(project_id = project_id) # type: ignore
            project = await self.create_project(project)
            return project
        return Project(**record)
    
    async def get_all_projects(self, page:int=1, page_size:int=10):

        total_documents = await self.collection.count_documents({})

        total_pages = total_documents //page_size
        if total_documents% page_size >1:
            total_pages += 1

        cursor = self.collection.find().skip( (page -1)*page_size).limit(page_size)
        projects = []
        async for documnet in cursor:
            projects.append(Project(**documnet))
        
        return projects, total_pages