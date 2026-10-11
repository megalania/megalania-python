from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from typing_extensions import Self

from ..models.error_error_code import ErrorErrorCode
from ..types import UNSET, Unset

T = TypeVar("T", bound="ErrorError")


@_attrs_define
class ErrorError:
    """
    Attributes:
        code (ErrorErrorCode):
        message (str):
        report_url (str): A dashboard page to tell us about this error. It holds only the request id, after a
        field (str | Unset): The parameter to change. On 400, on 422 and on some 503s.
    """

    code: ErrorErrorCode
    message: str
    report_url: str
    field: str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        code = self.code.value

        message = self.message

        report_url = self.report_url

        field = self.field

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "code": code,
                "message": message,
                "report_url": report_url,
            }
        )
        if field is not UNSET:
            field_dict["field"] = field

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        d = dict(src_dict)
        code = ErrorErrorCode(d.pop("code"))

        message = d.pop("message")

        report_url = d.pop("report_url")

        field = d.pop("field", UNSET)

        error_error = cls(
            code=code,
            message=message,
            report_url=report_url,
            field=field,
        )

        error_error.additional_properties = d
        return error_error

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
