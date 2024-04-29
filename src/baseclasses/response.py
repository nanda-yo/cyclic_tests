from src.enums.global_enums import GlobalErrorMessages


class Response:
    def __init__(self, response):
        self.response = response
        self.response_json = response.json()
        self.response_status = response.status_code

    def validate(self, schema):
        if isinstance(self.response_json, list):
            for item in self.response_json:
                schema.model_validate(item)
        else:
            schema.model_validate(self.response_json)
        return self

    def assert_status_code(self, status_code):
        if isinstance(status_code, list):
            assert self.response_status in status_code, GlobalErrorMessages.WRONG_STATUS_CODE.value
        else:
            assert self.response_status == status_code, GlobalErrorMessages.WRONG_STATUS_CODE.value
        return self

    def validate_created_item(self, valuestorage):
        if isinstance(self.response_json, list):
            isequal = False
            for k in valuestorage.valid_item_object.keys():   # k is 'sk'  ValueStorage.valid_item_object[k] == self.response_json[0][k]
                if k in self.response_json[0]:
                    if k == 'pk':
                        continue
                    else:
                        if {k: valuestorage.valid_item_object[k]} == {k: self.response_json[0][k]}:
                            isequal = True
                        else:
                            return 'Missing value for k/v pair'
                else:
                    return 'Missing key for k/v pair'
            assert isequal == True, GlobalErrorMessages.WRONG_ITEM_CREATION_RESULT.value
            return self
