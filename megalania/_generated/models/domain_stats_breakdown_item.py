from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from typing_extensions import Self

T = TypeVar("T", bound="DomainStatsBreakdownItem")


@_attrs_define
class DomainStatsBreakdownItem:
    """
    Attributes:
        engine (str):
        tier (str):
        requests (int):
        success_rate (float):
        mean_target_ms (float | None):
        block_share (float):
    """

    engine: str
    tier: str
    requests: int
    success_rate: float
    mean_target_ms: float | None
    block_share: float
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        engine = self.engine

        tier = self.tier

        requests = self.requests

        success_rate = self.success_rate

        mean_target_ms: float | None
        mean_target_ms = self.mean_target_ms

        block_share = self.block_share

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "engine": engine,
                "tier": tier,
                "requests": requests,
                "success_rate": success_rate,
                "mean_target_ms": mean_target_ms,
                "block_share": block_share,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        d = dict(src_dict)
        engine = d.pop("engine")

        tier = d.pop("tier")

        requests = d.pop("requests")

        success_rate = d.pop("success_rate")

        def _parse_mean_target_ms(data: object) -> float | None:
            if data is None:
                return data
            return cast(float | None, data)

        mean_target_ms = _parse_mean_target_ms(d.pop("mean_target_ms"))

        block_share = d.pop("block_share")

        domain_stats_breakdown_item = cls(
            engine=engine,
            tier=tier,
            requests=requests,
            success_rate=success_rate,
            mean_target_ms=mean_target_ms,
            block_share=block_share,
        )

        domain_stats_breakdown_item.additional_properties = d
        return domain_stats_breakdown_item

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
