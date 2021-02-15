# To use this code, make sure you
#
#     import json
#
# and then, to convert JSON from a string, do
#
#     result = feature_collection_from_dict(json.loads(json_string))

from enum import Enum
from typing import List, Union, Any, Optional, TypeVar, Callable, Type, cast


T = TypeVar("T")
EnumT = TypeVar("EnumT", bound=Enum)


def from_list(f: Callable[[Any], T], x: Any) -> List[T]:
    assert isinstance(x, list)
    return [f(y) for y in x]


def from_float(x: Any) -> float:
    assert isinstance(x, (float, int)) and not isinstance(x, bool)
    return float(x)


def from_union(fs, x):
    for f in fs:
        try:
            return f(x)
        except:
            pass
    assert False


def to_enum(c: Type[EnumT], x: Any) -> EnumT:
    assert isinstance(x, c)
    return x.value


def to_float(x: Any) -> float:
    assert isinstance(x, float)
    return x


def from_int(x: Any) -> int:
    assert isinstance(x, int) and not isinstance(x, bool)
    return x


def from_none(x: Any) -> Any:
    assert x is None
    return x


def to_class(c: Type[T], x: Any) -> dict:
    assert isinstance(x, c)
    return cast(Any, x).to_dict()


def from_str(x: Any) -> str:
    assert isinstance(x, str)
    return x


class GeometryType(Enum):
    MULTI_POLYGON = "MultiPolygon"
    POLYGON = "Polygon"


class Geometry:
    type: GeometryType
    coordinates: List[List[List[Union[List[float], float]]]]

    def __init__(self, type: GeometryType, coordinates: List[List[List[Union[List[float], float]]]]) -> None:
        self.type = type
        self.coordinates = coordinates

    @staticmethod
    def from_dict(obj: Any) -> 'Geometry':
        assert isinstance(obj, dict)
        type = GeometryType(obj.get("type"))
        coordinates = from_list(lambda x: from_list(lambda x: from_list(lambda x: from_union([from_float, lambda x: from_list(from_float, x)], x), x), x), obj.get("coordinates"))
        return Geometry(type, coordinates)

    def to_dict(self) -> dict:
        result: dict = {}
        result["type"] = to_enum(GeometryType, self.type)
        result["coordinates"] = from_list(lambda x: from_list(lambda x: from_list(lambda x: from_union([to_float, lambda x: from_list(to_float, x)], x), x), x), self.coordinates)
        return result


class Classification(Enum):
    ACCÈS_AUTOROUTE = "Accès Autoroute"
    APRES_2016 = "Apres_2016"
    ARTHÈRE = "Arthère"
    AUTOROUTE = "Autoroute"
    LOCALE = "Locale"
    PRIVÉ = "Privé"
    PROJETÉE = "Projetée"
    SEPAQ = "SEPAQ"
    VILLE = "Ville"


class Geom(Enum):
    POLYGONE = "Polygone"


class TYPEEnum(Enum):
    CHAUSSÉE = "Chaussée"
    INTERSECTION = "Intersection"
    STATIONNEMENT = "Stationnement"
    TROTTOIR = "Trottoir"


class Properties:
    objectid: int
    type: Optional[TYPEEnum]
    superficie: float
    geom: Geom
    classification: Optional[Classification]

    def __init__(self, objectid: int, type: Optional[TYPEEnum], superficie: float, geom: Geom, classification: Optional[Classification]) -> None:
        self.objectid = objectid
        self.type = type
        self.superficie = superficie
        self.geom = geom
        self.classification = classification

    @staticmethod
    def from_dict(obj: Any) -> 'Properties':
        assert isinstance(obj, dict)
        objectid = from_int(obj.get("OBJECTID"))
        type = from_union([from_none, TYPEEnum], obj.get("TYPE"))
        superficie = from_float(obj.get("SUPERFICIE"))
        geom = Geom(obj.get("GEOM"))
        classification = from_union([from_none, Classification], obj.get("CLASSIFICATION"))
        return Properties(objectid, type, superficie, geom, classification)

    def to_dict(self) -> dict:
        result: dict = {}
        result["OBJECTID"] = from_int(self.objectid)
        result["TYPE"] = from_union([from_none, lambda x: to_enum(TYPEEnum, x)], self.type)
        result["SUPERFICIE"] = to_float(self.superficie)
        result["GEOM"] = to_enum(Geom, self.geom)
        result["CLASSIFICATION"] = from_union([from_none, lambda x: to_enum(Classification, x)], self.classification)
        return result


class FeatureType(Enum):
    FEATURE = "Feature"


class Feature:
    type: FeatureType
    geometry: Geometry
    properties: Properties

    def __init__(self, type: FeatureType, geometry: Geometry, properties: Properties) -> None:
        self.type = type
        self.geometry = geometry
        self.properties = properties

    @staticmethod
    def from_dict(obj: Any) -> 'Feature':
        assert isinstance(obj, dict)
        type = FeatureType(obj.get("type"))
        geometry = Geometry.from_dict(obj.get("geometry"))
        properties = Properties.from_dict(obj.get("properties"))
        return Feature(type, geometry, properties)

    def to_dict(self) -> dict:
        result: dict = {}
        result["type"] = to_enum(FeatureType, self.type)
        result["geometry"] = to_class(Geometry, self.geometry)
        result["properties"] = to_class(Properties, self.properties)
        return result


class FeatureCollection:
    type: str
    name: str
    features: List[Feature]

    def __init__(self, type: str, name: str, features: List[Feature]) -> None:
        self.type = type
        self.name = name
        self.features = features

    @staticmethod
    def from_dict(obj: Any) -> 'FeatureCollection':
        assert isinstance(obj, dict)
        type = from_str(obj.get("type"))
        name = from_str(obj.get("name"))
        features = from_list(Feature.from_dict, obj.get("features"))
        return FeatureCollection(type, name, features)

    def to_dict(self) -> dict:
        result: dict = {}
        result["type"] = from_str(self.type)
        result["name"] = from_str(self.name)
        result["features"] = from_list(lambda x: to_class(Feature, x), self.features)
        return result


def feature_collection_from_dict(s: Any) -> FeatureCollection:
    return FeatureCollection.from_dict(s)


def feature_collection_to_dict(x: FeatureCollection) -> Any:
    return to_class(FeatureCollection, x)
