from __future__ import annotations

import datetime
from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from typing_extensions import Self

T = TypeVar("T", bound="TierPendingType0")


@_attrs_define
class TierPendingType0:
    """A scheduled change and the day it takes effect.

    Attributes:
        tier (int):
        effective_on (datetime.date):
        price (int):
    """

    tier: int
    effective_on: datetime.date
    price: int
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        tier = self.tier

        effective_on = self.effective_on.isoformat()

        price = self.price

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "tier": tier,
                "effective_on": effective_on,
                "price": price,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        d = dict(src_dict)
        tier = d.pop("tier")

        effective_on = datetime.date.fromisoformat(d.pop("effective_on"))

        price = d.pop("price")

        tier_pending_type_0 = cls(
            tier=tier,
            effective_on=effective_on,
            price=price,
        )

        tier_pending_type_0.additional_properties = d
        return tier_pending_type_0

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
