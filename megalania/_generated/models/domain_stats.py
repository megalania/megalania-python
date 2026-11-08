from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from typing_extensions import Self

if TYPE_CHECKING:
    from ..models.domain_stats_breakdown_item import DomainStatsBreakdownItem


T = TypeVar("T", bound="DomainStats")


@_attrs_define
class DomainStats:
    """
    Attributes:
        host (str): The host the answer is for, lowercase and without www.
        days (int):
        requests (int):
        breakdown (list[DomainStatsBreakdownItem]):
    """

    host: str
    days: int
    requests: int
    breakdown: list[DomainStatsBreakdownItem]
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        host = self.host

        days = self.days

        requests = self.requests

        breakdown = []
        for breakdown_item_data in self.breakdown:
            breakdown_item = breakdown_item_data.to_dict()
            breakdown.append(breakdown_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "host": host,
                "days": days,
                "requests": requests,
                "breakdown": breakdown,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        from ..models.domain_stats_breakdown_item import (
            DomainStatsBreakdownItem,
        )

        d = dict(src_dict)
        host = d.pop("host")

        days = d.pop("days")

        requests = d.pop("requests")

        breakdown = []
        _breakdown = d.pop("breakdown")
        for breakdown_item_data in _breakdown:
            breakdown_item = DomainStatsBreakdownItem.from_dict(breakdown_item_data)

            breakdown.append(breakdown_item)

        domain_stats = cls(
            host=host,
            days=days,
            requests=requests,
            breakdown=breakdown,
        )

        domain_stats.additional_properties = d
        return domain_stats

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
