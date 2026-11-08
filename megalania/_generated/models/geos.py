from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from typing_extensions import Self

if TYPE_CHECKING:
    from ..models.geos_routes_item import GeosRoutesItem


T = TypeVar("T", bound="Geos")


@_attrs_define
class Geos:
    """
    Attributes:
        default_country (str): The country a request without country_code exits from.
        premium (list[str]): Countries that add their price.
        routes (list[GeosRoutesItem]):
    """

    default_country: str
    premium: list[str]
    routes: list[GeosRoutesItem]
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        default_country = self.default_country

        premium = self.premium

        routes = []
        for routes_item_data in self.routes:
            routes_item = routes_item_data.to_dict()
            routes.append(routes_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "default_country": default_country,
                "premium": premium,
                "routes": routes,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        from ..models.geos_routes_item import GeosRoutesItem

        d = dict(src_dict)
        default_country = d.pop("default_country")

        premium = cast(list[str], d.pop("premium"))

        routes = []
        _routes = d.pop("routes")
        for routes_item_data in _routes:
            routes_item = GeosRoutesItem.from_dict(routes_item_data)

            routes.append(routes_item)

        geos = cls(
            default_country=default_country,
            premium=premium,
            routes=routes,
        )

        geos.additional_properties = d
        return geos

    @property
    def additional_keys(self) -> list[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> Any:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: Any) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
