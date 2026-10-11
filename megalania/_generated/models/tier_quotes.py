from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from typing_extensions import Self

from ..types import UNSET, Unset

T = TypeVar("T", bound="TierQuotes")


@_attrs_define
class TierQuotes:
    """What a request to this host with this proxy_tier reserves today, in credits, with the country_code and
    response_types you pass; with neither, before response types and premium geo. The same quote /v1 makes, so a
    cost_budget of this value is never refused for price. Always present, also for a host with no tier. A proxy_tier we
    cannot serve right now is left out. browser is what an engine=browser page costs within its included bytes; the
    request reserves more, for overage up to the byte cap, and a smaller cost_budget cuts the byte cap instead of
    refusing. It is left out while the browser cannot serve you. browser_residential is the same for engine=browser with
    proxy_tier=residential.

        Attributes:
            datacenter (int | Unset):
            residential (int | Unset):
            browser (int | Unset):
            browser_residential (int | Unset):
            mobile (int | Unset):
    """

    datacenter: int | Unset = UNSET
    residential: int | Unset = UNSET
    browser: int | Unset = UNSET
    browser_residential: int | Unset = UNSET
    mobile: int | Unset = UNSET

    def to_dict(self) -> dict[str, Any]:
        datacenter = self.datacenter

        residential = self.residential

        browser = self.browser

        browser_residential = self.browser_residential

        mobile = self.mobile

        field_dict: dict[str, Any] = {}

        field_dict.update({})
        if datacenter is not UNSET:
            field_dict["datacenter"] = datacenter
        if residential is not UNSET:
            field_dict["residential"] = residential
        if browser is not UNSET:
            field_dict["browser"] = browser
        if browser_residential is not UNSET:
            field_dict["browser_residential"] = browser_residential
        if mobile is not UNSET:
            field_dict["mobile"] = mobile

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        d = dict(src_dict)
        datacenter = d.pop("datacenter", UNSET)

        residential = d.pop("residential", UNSET)

        browser = d.pop("browser", UNSET)

        browser_residential = d.pop("browser_residential", UNSET)

        mobile = d.pop("mobile", UNSET)

        tier_quotes = cls(
            datacenter=datacenter,
            residential=residential,
            browser=browser,
            browser_residential=browser_residential,
            mobile=mobile,
        )

        return tier_quotes
