from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from typing_extensions import Self

from ..models.tier_capabilities_browser_item import TierCapabilitiesBrowserItem
from ..models.tier_capabilities_http_item import TierCapabilitiesHttpItem

T = TypeVar("T", bound="TierCapabilities")


@_attrs_define
class TierCapabilities:
    """The proxy tiers each engine can serve you on right now, from your key's rungs, our providers and running engines. An
    empty list means that engine cannot serve now. mobile appears only while a mobile provider serves.

        Attributes:
            http (list[TierCapabilitiesHttpItem]):
            browser (list[TierCapabilitiesBrowserItem]):
    """

    http: list[TierCapabilitiesHttpItem]
    browser: list[TierCapabilitiesBrowserItem]

    def to_dict(self) -> dict[str, Any]:
        http = []
        for http_item_data in self.http:
            http_item = http_item_data.value
            http.append(http_item)

        browser = []
        for browser_item_data in self.browser:
            browser_item = browser_item_data.value
            browser.append(browser_item)

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "http": http,
                "browser": browser,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        d = dict(src_dict)
        http = []
        _http = d.pop("http")
        for http_item_data in _http:
            http_item = TierCapabilitiesHttpItem(http_item_data)

            http.append(http_item)

        browser = []
        _browser = d.pop("browser")
        for browser_item_data in _browser:
            browser_item = TierCapabilitiesBrowserItem(browser_item_data)

            browser.append(browser_item)

        tier_capabilities = cls(
            http=http,
            browser=browser,
        )

        return tier_capabilities
