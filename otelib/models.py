from typing import Dict, Optional, List, Tuple
from pydantic import BaseModel, AnyUrl
from datetime import datetime

class FilterConfig(BaseModel):
    """ Resource Specific Data Filter Configuration
    query - define a query operation
    condition - logical statement indicating when a filter should be appliced
    limit - number of items remaining after a filter expression
    """
    filterType: str
    query: Optional[str]
    condition: Optional[str]
    limit: Optional[int]
    configuration: Optional[Dict]

class MappingConfig(BaseModel):
    """ Mapping data model """
    mappingType: str
    prefixes: Optional[Dict[str, str]]
    triples: Optional[List[Tuple[str, str, str]]]
    configuration: Optional[Dict]

class ResourceConfig(BaseModel):
    """ Dataset distributrion """
    downloadUrl: AnyUrl = None
    mediaType: str = None
    accessUrl: AnyUrl = None
    accessService: str = None
    license: Optional[str] = None
    accessRights: Optional [str] = None
    description: Optional [str] = None
    published: Optional [str] = None
    configuration: Optional[Dict] = None

class TransformationConfig(BaseModel):
    """ Transformation data model """
    transformation_type: str
    name: Optional[str]
    description: Optional[str]
    due: Optional[datetime]
    priority: Optional[int]
    secret: Optional[str]
    configuration: Optional[Dict]
