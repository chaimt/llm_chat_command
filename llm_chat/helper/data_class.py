from typing import Any, Dict

from mashumaro.mixins.json import DataClassJSONMixin
from mashumaro.mixins.yaml import DataClassYAMLMixin


class DataClassYAMLMixinNullRemoval(DataClassYAMLMixin):
    def __post_serialize__(self, d: Dict[Any, Any]) -> Dict[Any, Any]:
        return dict(filter(lambda item: item[1] is not None, d.items()))


class DataClassJSONMixinNullRemoval(DataClassJSONMixin):
    def __post_serialize__(self, d: Dict[Any, Any]) -> Dict[Any, Any]:
        return dict(filter(lambda item: item[1] is not None, d.items()))
