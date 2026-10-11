from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from typing_extensions import Self

if TYPE_CHECKING:
    from ..models.map_result_urls_item import MapResultUrlsItem


T = TypeVar("T", bound="MapResult")


@_attrs_define
class MapResult:
    """
    Attributes:
        urls (list[MapResultUrlsItem]):
        truncated (bool): true when the limit, the byte cap or your balance stopped the map before every URL was read.
    """

    urls: list[MapResultUrlsItem]
    truncated: bool
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        urls = []
        for urls_item_data in self.urls:
            urls_item = urls_item_data.to_dict()
            urls.append(urls_item)

        truncated = self.truncated

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "urls": urls,
                "truncated": truncated,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        from ..models.map_result_urls_item import MapResultUrlsItem

        d = dict(src_dict)
        urls = []
        _urls = d.pop("urls")
        for urls_item_data in _urls:
            urls_item = MapResultUrlsItem.from_dict(urls_item_data)

            urls.append(urls_item)

        truncated = d.pop("truncated")

        map_result = cls(
            urls=urls,
            truncated=truncated,
        )

        map_result.additional_properties = d
        return map_result

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
