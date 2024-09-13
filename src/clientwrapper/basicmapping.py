from collections.abc import Mapping

from typing import Optional


class BasicMapping(Mapping):
    data: dict

    def __init__(self, data: dict):
        self.data = dict()
        for key, value in self._flatten_data_(data):
            self.data[key] = value
        super().__init__()

    def __len__(self):
        return len([key for key in self.data])

    def __getitem__(self, key):
        return self.data[key]

    def __iter__(self):
        for value in self.__items__():
            yield value

    def __items__(self):
        return [key for key in self.data]

    def __contains__(self, value):
        return value in self.data.values()

    def _flatten_data_(self, data: dict, parent_key: Optional[str] = None) -> dict:
        for key, value in data.items():
            joined_key = f"{parent_key}_{key}" if parent_key else key
            if isinstance(value, dict):
                yield from self._flatten_data_(value, joined_key).items()
            else:
                yield joined_key, value
