
# from pydantic import BaseModel
# from typing import Any


# class PayloadSchema(BaseModel):

#     data: Any


from pydantic import BaseModel
from typing import Any, List, Dict

class Payload(BaseModel):
    data: Any

class QueryRequest(BaseModel):
    database: str
    query: Dict = {}