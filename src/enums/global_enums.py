from enum import Enum

class GlobalErrorMessages(Enum):
    WRONG_STATUS_CODE = "Received status code isnt equal to expected"
    WRONG_ELEMENT_COUNT = "Element count isnt equal to expected"
    WRONG_ITEM_CREATION_RESULT ="Created item isnt equal to sent out"