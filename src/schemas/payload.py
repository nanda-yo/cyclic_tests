from uuid import uuid4
from pydantic import BaseModel, AfterValidator, Field
from typing import Annotated, List
from decimal import Decimal

class ParamsModel(BaseModel):
    var1:str
    var2:str
    var3: Decimal = Field()


class Payload(BaseModel):
    sk: str
    description:str
    pk: uuid4 | Annotated[str,AfterValidator(lambda x:uuid4())]
    title:str
    author:str
    params:List[ParamsModel]









    # {
    #     "sk": "fkr",
    #     "description": "Risk few quality fill left simply. Doctor indeed might key.\nPm nothing prepare care many admit. Daughter pull night early large camera watch simply. Very issue hear back star boy.",
    #     "pk": "64ffa3e6-1d1a-43b0-b08d-3eaec537ad69",
    #     "params": [
    #         {
    #             "var2": "0-15-772663-0",
    #             "var1": "0-17-307269-0",
    #             "var3": 9118.412
    #         }
    #     ],
    #     "title": "Scene benefit management despite week.",
    #     "author": "Nicholas Parker"
    # },