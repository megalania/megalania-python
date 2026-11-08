from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from typing_extensions import Self

if TYPE_CHECKING:
    from ..models.tier_capabilities import TierCapabilities
    from ..models.tier_pending_type_0 import TierPendingType0
    from ..models.tier_quotes import TierQuotes


T = TypeVar("T", bound="Tier")


@_attrs_define
class Tier:
    """
    Attributes:
        host (str):
        tier (int | None): The tier in effect today.
        temporary (bool | None): true while the host has too few requests for a measured tier. A temporary tier can rise
            at once.
        price (int | None): The quote for a typical page on this host, in credits, from its tier, before response types
            and premium geo. It is not the charge. Every request pays the price of the route that delivers the page, shown
            in quotes.
        pending (None | TierPendingType0): A scheduled change and the day it takes effect.
        quotes (TierQuotes): What a request to this host with this proxy_tier reserves today, in credits, with the
            country_code and response_types you pass; with neither, before response types and premium geo. The same quote
            /v1 makes, so a max_credits of this value is never refused for price. Always present, also for a host with no
            tier. A proxy_tier we cannot serve right now is left out. browser is what an engine=browser page costs within
            its included bytes; the request reserves more, for overage up to the byte cap, and a smaller max_credits cuts
            the byte cap instead of refusing. It is left out while the browser cannot serve you. browser_residential is the
            same for engine=browser with proxy_tier=residential. With no country_code or response_types, each quote equals
            the base price of that route on the Plan page, on every host. The host's tier never changes what a route costs.
        capabilities (TierCapabilities): The proxy tiers each engine can serve you on right now, from your key's rungs,
            our providers and running engines. An empty list means that engine cannot serve now. mobile appears only while a
            mobile provider serves.
    """

    host: str
    tier: int | None
    temporary: bool | None
    price: int | None
    pending: None | TierPendingType0
    quotes: TierQuotes
    capabilities: TierCapabilities
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.tier_pending_type_0 import TierPendingType0

        host = self.host

        tier: int | None
        tier = self.tier

        temporary: bool | None
        temporary = self.temporary

        price: int | None
        price = self.price

        pending: dict[str, Any] | None
        if isinstance(self.pending, TierPendingType0):
            pending = self.pending.to_dict()
        else:
            pending = self.pending

        quotes = self.quotes.to_dict()

        capabilities = self.capabilities.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "host": host,
                "tier": tier,
                "temporary": temporary,
                "price": price,
                "pending": pending,
                "quotes": quotes,
                "capabilities": capabilities,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        from ..models.tier_capabilities import TierCapabilities
        from ..models.tier_pending_type_0 import TierPendingType0
        from ..models.tier_quotes import TierQuotes

        d = dict(src_dict)
        host = d.pop("host")

        def _parse_tier(data: object) -> int | None:
            if data is None:
                return data
            return cast(int | None, data)

        tier = _parse_tier(d.pop("tier"))

        def _parse_temporary(data: object) -> bool | None:
            if data is None:
                return data
            return cast(bool | None, data)

        temporary = _parse_temporary(d.pop("temporary"))

        def _parse_price(data: object) -> int | None:
            if data is None:
                return data
            return cast(int | None, data)

        price = _parse_price(d.pop("price"))

        def _parse_pending(data: object) -> None | TierPendingType0:
            if data is None:
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                pending_type_0 = TierPendingType0.from_dict(data)

                return pending_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(None | TierPendingType0, data)

        pending = _parse_pending(d.pop("pending"))

        quotes = TierQuotes.from_dict(d.pop("quotes"))

        capabilities = TierCapabilities.from_dict(d.pop("capabilities"))

        tier = cls(
            host=host,
            tier=tier,
            temporary=temporary,
            price=price,
            pending=pending,
            quotes=quotes,
            capabilities=capabilities,
        )

        tier.additional_properties = d
        return tier

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
