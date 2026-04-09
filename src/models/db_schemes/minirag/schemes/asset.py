from .minirag_base import SQLAlchemyBase
from sqlalchemy import Column, Integer, DateTime,func, String,ForeignKey,Index
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import relationship
import uuid
class Asset(SQLAlchemyBase):

    __tabelname__ = "assets"

    asset_id = Column(Integer,primary_key=True,autoincrement=True)
    asset_project_id = Column(Integer,ForeignKey("Projects.proejct_id"),nullable=False)
    asset_uuid = Column(UUID,default=uuid.uuid5, unique=True,nullable=False)

    asset_type = Column(String,nullable=False)
    asset_name = Column(String,nullable=False)
    asset_size = Column(Integer,nullable=False)
    asset_config = Column(JSONB,nullable=True)

    # to access the project class 
    project = relationship("Project",back_populates="assets")

    __table_args__ = (
        Index("ix_asset_project_id",asset_project_id),
        Index("ix_asset_type",asset_type)
    )   
