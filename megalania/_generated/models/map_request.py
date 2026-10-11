from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from typing_extensions import Self

from ..types import UNSET, Unset

T = TypeVar("T", bound="MapRequest")


@_attrs_define
class MapRequest:
    """
    Attributes:
        url (str): The page to map from, http or https. Its host is the site.
        limit (int | Unset): The most URLs to return. Default: 500.
        search (str | Unset): Keep only URLs that contain this text.
        include_subdomains (bool | Unset): Also keep URLs on subdomains of the site's host. Default: False.
    """

    url: str
    limit: int | Unset = 500
    search: str | Unset = UNSET
    include_subdomains: bool | Unset = False

    def to_dict(self) -> dict[str, Any]:
        url = self.url

        limit = self.limit

        search = self.search

        include_subdomains = self.include_subdomains

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "url": url,
            }
        )
        if limit is not UNSET:
            field_dict["limit"] = limit
        if search is not UNSET:
            field_dict["search"] = search
        if include_subdomains is not UNSET:
            field_dict["include_subdomains"] = include_subdomains

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        d = dict(src_dict)
        url = d.pop("url")

        limit = d.pop("limit", UNSET)

        search = d.pop("search", UNSET)

        include_subdomains = d.pop("include_subdomains", UNSET)

        map_request = cls(
            url=url,
            limit=limit,
            search=search,
            include_subdomains=include_subdomains,
        )

        return map_request
