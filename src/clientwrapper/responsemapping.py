from requests import Response

from .basicmapping import BasicMapping


class ResultMapping(BasicMapping):
    def __init__(self, data: dict):
        super().__init__(data)


class ResponseMapping:
    response: Response
    results: list[ResultMapping] = []

    def __init__(self, response: Response, data_key: str = None):
        self.response = response
        response_json = response.json()
        if data_key is None:
            self.results += [ResultMapping(response_json)]
        else:
            response_data = response_json[data_key]
            if isinstance(response_data, dict):
                self.results += [ResultMapping(response_data)]
            elif isinstance(response_data, list):
                for result in response_data:
                    self.results += [ResultMapping(result)]
