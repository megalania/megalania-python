from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from typing_extensions import Self

from ..models.geos_routes_item_engine import GeosRoutesItemEngine
from ..models.geos_routes_item_proxy_tier import GeosRoutesItemProxyTier

T = TypeVar("T", bound="GeosRoutesItem")


@_attrs_define
class GeosRoutesItem:
    """
    Attributes:
        route (str): The route's name, like h:dc (HTTP, datacenter).
        engine (GeosRoutesItemEngine):
        proxy_tier (GeosRoutesItemProxyTier):
        countries (list[str]): Uppercase ISO 3166-1 alpha-2 codes this route exits from.
    """

    route: str
    engine: GeosRoutesItemEngine
    proxy_tier: GeosRoutesItemProxyTier
    countries: list[str]
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        route = self.route

        engine = self.engine.value

        proxy_tier = self.proxy_tier.value

        countries = self.countries

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "route": route,
                "engine": engine,
                "proxy_tier": proxy_tier,
                "countries": countries,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        d = dict(src_dict)
        route = d.pop("route")

        engine = GeosRoutesItemEngine(d.pop("engine"))

        proxy_tier = GeosRoutesItemProxyTier(d.pop("proxy_tier"))

        countries = cast(list[str], d.pop("countries"))

        geos_routes_item = cls(
            route=route,
            engine=engine,
            proxy_tier=proxy_tier,
            countries=countries,
        )

        geos_routes_item.additional_properties = d
        return geos_routes_item

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
